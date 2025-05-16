import argparse
import os

def get_args():
    parser = argparse.ArgumentParser(description="LeCoDe Benchmark.")
    parser.add_argument('--input_data', type=str, default="./data/LeCoDe_testset.jsonl", help='input filename, a path with jsonl')
    parser.add_argument('--dataset_type', type=str, default="hard", help='[easy, hard]')
    parser.add_argument('--output_file', type=str, default='./outputs/output_file_qwen_max/', help='output filename, just a file fold name')
    
    parser.add_argument('--MAX_TURNS', type=int, default=10, help='input filename, a path with jsonl')
    
    parser.add_argument('--lawyer_mode', type=str, default="direct_ask", help='lawyer how to ask and answer, can be set:[direct_ask, decision]. direct_ask means only use llm ask capability. ')
    parser.add_argument('--lawyer_model', type=str, default='qwen-max', help='Lawyer model_name, can be a commercial model by OpenAI module, or local model call vllm by 0.0.0.0 or ./xxx/llm_path.')
    
    parser.add_argument('--user_mode', type=str, default="direct_answer", help='user how to ask and answer, can be set:[direct_answer, ...]. direct_ask means only use llm ask capability. ')
    
    parser.add_argument('--user_model', type=str, default='qwen-max', help='user model_name, can be a commercial model by OpenAI module, or local model call vllm by 0.0.0.0 or ./xxx/llm_path.')
    
    args =  parser.parse_args()


    return args