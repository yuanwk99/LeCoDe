from args import get_args
import json
from tqdm import tqdm
from agent.lawyer_agent import LawyerAgent
from agent.user_agent import UserAgent
from lecode_util.PROMPT_TEMPLATE import LAWYER_PROMPT_direct,USER_PROMPT_direct,LAWYER_SUGGESTION_PROMPT_direct,LAWYER_PROMPT_mediq_abstain,LAWYER_PROMPT_mediq_ask,LAWYER_PROMPT_mediq_suggestion,LAWYER_PROMPT_fewshot,LAWYER_SUGGESTION_PROMPT_fewshot
import os


from logging_system.logger import Logger
logger = Logger()

# 读取数据集
def load_data():
    with open(args.input_data) as f:
        data = f.readlines()
    data = [json.loads(i) for i in data]
    return data


def ensure_dir(file_path):
    """
    确保文件路径的目录存在，如果不存在则创建
    
    Args:
        file_path: 文件的完整路径
    
    Returns:
        bool: 目录是否成功创建或已存在
    """
    try:
        directory = os.path.dirname(file_path)
        
        # 如果是空目录路径，直接返回True
        if not directory:
            return True
            
        # 如果目录已存在
        if os.path.exists(directory):
            print(f"Directory already exists: {directory}")
            return True
            
        # 创建目录
        os.makedirs(directory)
        print(f"Successfully created directory: {directory}")
        return True
        
    except Exception as e:
        print(f"Error creating directory for {file_path}: {str(e)}")
        return False

def process_data(data_item):

    conversation_id = data_item['id']
    
    initial_query = data_item['initial_query']
    initial_query = initial_query.replace("\n","")
    
    if args.dataset_type == 'hard':
        key_fact_dict = data_item['key_fact_dict_hard_version']
        key_fact_dict = key_fact_dict['原子事实']

    
    turn_num = 0
    MAX_TURNS = args.MAX_TURNS
    
    res_data = []
    
    need_log_content = f"***********************START***********************\nconversation_id:{conversation_id}\n"


    dialogue_context = f"用户:{initial_query}\n"
    initial_token = {"used_time":None,"input_tokens":None,"output_tokens":None}
    need_log_content = need_log_content+ "##用户##"+ f"{initial_query}\n##token_information##{initial_token}\n"
    res_data.append(["用户",initial_query,initial_token])
    

    while turn_num<=MAX_TURNS+1: 
        lawyer_response,token_information = lawyer.get_response(dialogue_context,question_turn_num=turn_num+1,model_name=args.lawyer_model,max_dialoge_turn=MAX_TURNS)
        
        need_log_content = need_log_content+ "##律师##"+ f"{lawyer_response}\n##token_information##{token_information}\n"
        res_data.append(["律师",lawyer_response,token_information])
        
        
        dialogue_context = dialogue_context + f"律师:{lawyer_response}\n"
        if "建议:" in lawyer_response or "建议：" in lawyer_response :
            break
        if "提问" in lawyer_response:
            user_reply,user_token_information = user.get_response(dialogue_context=dialogue_context,key_fact_dict=key_fact_dict,model_name =args.user_model,lawyer_question=lawyer_response)
            need_log_content = need_log_content+ "##用户##"+ f"{user_reply}\n##token_information##{user_token_information}\n"
            res_data.append(["用户",user_reply,user_token_information])

            dialogue_context = dialogue_context+f"用户:{user_reply}\n"

        turn_num +=1
    need_log_content = need_log_content+f"***********************END***********************\nconversation_id:{conversation_id}\n\n"
    logger.log("",need_log_content)
    
    # 直接写入JSON文件
    with open(args.output_file+f'{conversation_id}.json', 'w', encoding='utf-8') as f:
        json.dump(res_data, f, ensure_ascii=False, indent=4)

        
def save_args(args, filename='args.txt'):
    with open(filename, 'w', encoding='utf-8') as f:
        for key, value in vars(args).items():
            f.write(f'{key}: {value}\n')


if __name__ == "__main__":
    args = get_args()
    
    # 使用示例
    if ensure_dir(args.output_file):
        # 继续处理
        print("Proceeding with file operations...")
    else:
        # 处理错误
        print("Failed to ensure directory exists")
        
    save_args(args, args.output_file+'config.txt')
    
    # 读取数据
    data = load_data()
    # print(len(data))

    
    exsiting_data = os.listdir(args.output_file)
    exsiting_data = [i.replace(".json","") for i in exsiting_data if ".json" in i ]

    data = [i for i in data if i['id'] not in exsiting_data]
    

       
    
    
    lawyer_mode = args.lawyer_mode
    user_mode = args.user_mode
    
    usr_prompt_dict = {"direct_answer":USER_PROMPT_direct}
    lawyer_prompt_dict = {"direct_ask":LAWYER_PROMPT_direct,'fewshot_ask':LAWYER_PROMPT_fewshot,'mediq_ask':{"abstain":LAWYER_PROMPT_mediq_abstain,"ask":LAWYER_PROMPT_mediq_ask,"suggestion":LAWYER_PROMPT_mediq_suggestion}}
    lawyer_suggestion_dict = {"direct_ask":LAWYER_SUGGESTION_PROMPT_direct,"mediq_ask":LAWYER_SUGGESTION_PROMPT_direct,'fewshot_ask':LAWYER_SUGGESTION_PROMPT_fewshot}
    
    lawyer = LawyerAgent(lawyer_prompt=lawyer_prompt_dict[lawyer_mode],suggestion_prompt=lawyer_suggestion_dict[lawyer_mode],lawyer_mode=lawyer_mode)
    user = UserAgent(user_prompt=usr_prompt_dict[user_mode],user_mode=user_mode)

    
    from concurrent.futures import ThreadPoolExecutor, as_completed
    error_li = []
    final_res = []
    # results = []
    # 使用 ThreadPoolExecutor 创建一个线程池
    
    if "gpt" in args.lawyer_model:
        max_worker = 20
    elif "qwen" in args.lawyer_model:
        max_worker = 50
    elif "farui-plus" in args.lawyer_model:
        max_worker = 2
    elif "deepseek" in args.lawyer_model:
        max_worker = 50
    else:
        max_worker = 50
    with ThreadPoolExecutor(max_workers=max_worker) as executor:
        futures = {executor.submit(process_data, item): item for item in data}
        for future in tqdm(as_completed(futures)):
            item = futures[future]
            try:
                result = future.result()
                # print(item)
 
            except Exception as e:
                error_li.append([item['id']])
                print(f"Exception occurred for item {item['id']}: {e}")

