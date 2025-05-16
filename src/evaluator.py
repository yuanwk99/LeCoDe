# from args import get_args
import json
from tqdm import tqdm
from agent.lawyer_agent import LawyerAgent
from agent.user_agent import UserAgent
from lecode_util.PROMPT_TEMPLATE import LAWYER_PROMPT_direct,USER_PROMPT_direct,LAWYER_SUGGESTION_PROMPT_direct
import os

import argparse
import pandas as pd


from rouge_chinese import Rouge
from tqdm import tqdm
import jieba # you can use any other word cutting library
from bert_score_package.bert_score import score
import numpy as np
rouge = Rouge()

from typing import List, Tuple

from transformers import BertTokenizer


def compute_bertscore(hypothesis, reference) -> float:
    tokenizer = BertTokenizer.from_pretrained("../../../BERT_baseline/models/bert-base-chinese")
    max_length = 510
    # 截断文本
    hypothesis = tokenizer.encode(hypothesis, truncation=True, max_length=max_length)
    hypothesis = tokenizer.decode(hypothesis)
    reference = tokenizer.encode(reference, truncation=True, max_length=max_length)
    reference = tokenizer.decode(reference)
    
    P, R, F1 = score([hypothesis], [reference],model_type="../../../BERT_baseline/models/bert-base-chinese",lang="zh")
    # P, R, F1 = score([hypothesis], [reference],model_type="../../../hf-model/Lawformer",lang="zh")
    # print(F1)
    return F1.tolist()[0]
def compute_rouge(hypothesis,reference):
    # hypothesis = ''
    hypothesis = ' '.join(jieba.cut(hypothesis)) 

    # reference = ''
    reference = ' '.join(jieba.cut(reference))

    
    scores = rouge.get_scores(hypothesis, reference)
    
    return scores[0]['rouge-l']['f']

# 读取数据集
def load_data():
    with open(args.input_data) as f:
        data = f.readlines()
    data = [json.loads(i) for i in data]
    return data


def load_evaluation_data(evaluation_data_path):
    '''输入是一个待评估的文件夹地址 --> list
        输出是该文件夹下所有json 文件 --> return_dict
    '''
    return_dict = {}
    for path in evaluation_data_path:
        with open(path) as f:
            file_data = json.load(f)
        file_id = path.replace(args.evaluation_data,"").replace(".json","")
        file_data = pd.DataFrame(file_data)
        
        file_data.columns = ['user',"text","usage"]
        return_dict[file_id] = file_data
    return return_dict

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LeCoDe evaluation.")
    parser.add_argument('--input_data', required=True, type=str, help='')
    parser.add_argument('--evaluation_data', required=True, type=str, help='')
    
    args =  parser.parse_args()
    
    # 读取版本
    with open(args.evaluation_data+"config.txt") as f:
        test_config_dict = f.readlines()
    test_config_dict={i.split(": ")[0]:i.split(": ")[1].strip() for i in test_config_dict}
    # print(test_config_dict)
    
    data = load_data()
    data = pd.DataFrame(data)

    # print(data.columns)
    evaluation_data_path = [args.evaluation_data+i for i in os.listdir(args.evaluation_data) if '.json' in i]
    # print(evaluation_data_path[0])
    evaluation_data = load_evaluation_data(evaluation_data_path)
    
    # 获取每个evaluation的id
    evaluation_id_li = list(evaluation_data.keys())
    
    gt_pred_li = []
    for eval_id in evaluation_id_li:
        data[data['id'] == eval_id]
        # evaluation_data[eval_id]
        gt_suggestion = "".join(data[data['id'] == eval_id]['suggestion'].values.tolist())
        # 预测的对话数据和预测的建议
        
        gt_key_fact = data[data['id'] == eval_id][f"key_fact_dict_{test_config_dict['dataset_type']}_version"].values[0]
        gt_key_fact['原子事实']
        gt_key_fact['重要性分数']
        
        pred_dialogue = evaluation_data[eval_id][["user","text"]].values.tolist()
        ask_turn = len(pred_dialogue)
        ## 不知道的数量:
        yonghu_conv_len = 0
        idontknow_num = 0
        for diag in pred_dialogue:
            if diag[0] =="用户":
                if diag[1]==None:
                    diag[1]='不知道'
                yonghu_conv_len = yonghu_conv_len+1
                if ("不知道" in diag[1]) and (len(diag[1])<=6):
                    idontknow_num=idontknow_num+1
        
        pred_suggestion = pred_dialogue[-1][1]
        
        gt_pred_li.append([eval_id,gt_suggestion,gt_key_fact['原子事实'],gt_key_fact['重要性分数'],pred_dialogue,pred_suggestion,ask_turn,idontknow_num/yonghu_conv_len])
    gt_pred_df = pd.DataFrame(gt_pred_li)
    gt_pred_df.columns = ['id',"gt_suggestion","gt_key_fact","gt_key_fact_importance","pred_dialogue","pred_suggestion","ask_turn","dont_know_num"]
    
    # gt_pred_df
    gt_pred_df['rouge'] = gt_pred_df.apply(lambda row: compute_rouge(row['pred_suggestion'], row['gt_suggestion']), axis=1)
    print(gt_pred_df["rouge"].mean())
    # print(compute_bertscore("adasd","diadac"))
    gt_pred_df['bertscore'] = gt_pred_df.apply(lambda row: compute_bertscore(row['pred_suggestion'], row['gt_suggestion']), axis=1)
    # print(pred_dialogue)
    print("bertscore:",gt_pred_df["bertscore"].mean())
    
    print("i dont know:",gt_pred_df["dont_know_num"].mean())
    
    
    o_file_name = args.evaluation_data.replace("./outputs/","").replace("/","")
    gt_pred_df.to_csv(f"./outputs/evaluation_output/{o_file_name}.csv",index=False)
    # print(data[data['id'] == eval_id])
    # print(f"gt_suggestion:{gt_suggestion}")
    # print(f"pred_suggestion:{pred_suggestion}")
    # print(compute_semantic_similarity(gt_suggestion,pred_suggestion))
    # print(f"gt_key_fact:{gt_key_fact}")
    # print(evaluation_data['00d9900df86f4825aaadfd39a8b95081'])
    # for filepath in evaluation_data_path:
