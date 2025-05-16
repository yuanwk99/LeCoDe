# encoding=utf-8
import requests
import json
import os
import dashscope
from dashscope import Generation
from http import HTTPStatus
import time


def ask_llm(prompt, model='qwen-max'):
    if "gpt" in model:
        return ask_gpt(prompt, model)
    elif "deepseek" in model:
        return ask_deepseek(prompt, model)
    elif ("localhost" in model) or ("/mnt/workspace" in model): # -> you need to revise the local path to modify your path
        return call_diy_llm(prompt,model) # vllm :"/path/Qwen2.5-14B-Instruct/"

    else:
        return ask_tyqw(prompt, model)
    
def ask_deepseek(prompt, model):
    dashscope.api_key = os.getenv("DASHSCOPE_API_KEY", "your dashscope api key")
    s_time = time.time()
    response = Generation.call(model,
                               prompt=prompt
                               )
    e_time = time.time()
    
    if response.status_code == HTTPStatus.OK:
        used_time = e_time-s_time
        input_tokens = response['usage'].input_tokens
        output_tokens = response['usage'].output_tokens
        token_infomration = {"used_time":used_time,"input_tokens":input_tokens,"output_tokens":output_tokens}
        return response["output"]['choices'][0]['message'].content,token_infomration
    
    return None,{"used_time":None,"input_tokens":None,"output_tokens":None}

    

def ask_tyqw(prompt, model='qwen-max'):
    dashscope.api_key = os.getenv("DASHSCOPE_API_KEY", "your dashscope api key")
    if type(prompt) is str:
        s_time = time.time()
        response = Generation.call(model,
                                   prompt=prompt,
                                   )
        e_time = time.time()
        if response.status_code == HTTPStatus.OK:
            used_time = e_time-s_time
            input_tokens = response['usage'].input_tokens
            output_tokens = response['usage'].output_tokens
            token_infomration = {"used_time":used_time,"input_tokens":input_tokens,"output_tokens":output_tokens}
            return response["output"]["text"],token_infomration
                
        
        return None,{"used_time":None,"input_tokens":None,"output_tokens":None}

    elif type(prompt) is list:
        response = Generation.call(model,
                                   messages=prompt,
                                   result_format='message'  # 设置输出为'message'格式
                                   )
        if response.status_code == HTTPStatus.OK:
            return response["output"]["choices"][0]["message"]["content"]
        else:
            return None
        
def ask_gpt(prompt, model='gpt-4'):
    #
    url ="openaiurl/v1/chat/completions"
    
    if type(prompt) is str:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "n": 1,
            "temperature": 1.0
        }
    elif type(prompt) is list:
        payload = {
            "model": model,
            "messages": prompt,
            "n": 1,
            "temperature": 1.0
        }
        

    token ="Your api Key"
    
    headers = {
                'Authorization': token,
                'Content-Type': 'application/json'
            }
    
    try:
        s_time = time.time()
        response = requests.request("POST", url, headers=headers,
                                                data=json.dumps(payload, ensure_ascii=False).encode('utf-8'))
        e_time = time.time()
        text = response.json()['choices'][0]['message']['content']
        input_tokens = response.json()['usage']['prompt_tokens']
        output_tokens=response.json()['usage']['completion_tokens']
        used_time = e_time-s_time
        token_infomration = {"used_time":used_time,"input_tokens":input_tokens,"output_tokens":output_tokens}
        return text,token_infomration
    except:
        return None,{"used_time":None,"input_tokens":None,"output_tokens":None}        
        

from openai import OpenAI

def call_diy_llm(prompt,model_name): # for vllm api call
    if "Qwen3" in model_name:
        s_time = time.time()
        client = OpenAI(base_url= "http://localhost:8000/v1",api_key='EMPTY')
        completion = client.chat.completions.create(model =model_name ,
                                 messages = [
                    {"role": "user", "content": prompt}
                ],
                                                  temperature=0.7,
    extra_body={"chat_template_kwargs": {"enable_thinking": False},"top_p":0.8,"top_k":20,"presence_penalty":1.5}
        )
        e_time = time.time()
        used_time = e_time-s_time
        text = completion.choices[0].message.content
        input_tokens=completion.usage.prompt_tokens
        output_tokens = completion.usage.completion_tokens
        token_infomration = {"used_time":used_time,"input_tokens":input_tokens,"output_tokens":output_tokens}
        return text,token_infomration  
    
    else:
        s_time = time.time()
        client = OpenAI(base_url= "http://localhost:8000/v1",api_key='EMPTY')
        completion = client.chat.completions.create(model =model_name ,
                                 messages = [
                    {"role": "user", "content": prompt}
                ],
                                                    temperature=0.7,
                                                    extra_body={ "repetition_penalty": 1.05,}


        )
        e_time = time.time()
        used_time = e_time-s_time
        text = completion.choices[0].message.content
        input_tokens=completion.usage.prompt_tokens
        output_tokens = completion.usage.completion_tokens
        token_infomration = {"used_time":used_time,"input_tokens":input_tokens,"output_tokens":output_tokens}
        return text,token_infomration

