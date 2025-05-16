# agents/user_agent.py

from lecode_util.call_llm import ask_llm
import os
# from logging_system.logger import Logger

class UserAgent:
    def __init__(self, user_prompt,user_mode):
        self.prompt = user_prompt
        self.user_mode = user_mode
        # self.logger = logger
        # self.key_fact_dict = key_fact_dict


    def get_response(self, dialogue_context,key_fact_dict,model_name,lawyer_question):
        if self.user_mode == "direct_answer":
            try:
                # Check if the question can be answered with key_fact_dict
                # answer = self.extract_answer(lawyer_question)
                p = self.prompt.replace("{current_dialogue}",dialogue_context).replace("{key_factor}",str(key_fact_dict))
                reply,token_information =  ask_llm(p, model=model_name)
                # ask_tyqw(p)

                # Log the response
                # self.logger.log("User", reply)
                return reply,token_information
            except Exception as e:
                # self.logger.log("Error", f"UserAgent Error: {str(e)}")
                return "抱歉，我遇到了问题无法继续。",{"used_time":None,"input_tokens":None,"output_tokens":None}
        elif (self.user_mode == "instruct_answer_question") or (self.user_mode == "instruct_answer_dialogue") :
            try:
                # Check if the question can be answered with key_fact_dict
                # answer = self.extract_answer(lawyer_question)
                if self.user_mode == "instruct_answer_question":
                    p = self.prompt.replace("{lawyer_question}",lawyer_question).replace("{key_factor}",str(key_fact_dict))
                elif self.user_mode == "instruct_answer_dialogue":
                    p = self.prompt.replace("{lawyer_question}",dialogue_context).replace("{key_factor}",str(key_fact_dict))
                reply,token_information =  ask_llm(p, model=model_name)
                # ask_tyqw(p)

                # Log the response
                # self.logger.log("User", reply)
                return reply,token_information
            except Exception as e:
                # self.logger.log("Error", f"UserAgent Error: {str(e)}")
                return "抱歉，我遇到了问题无法继续。",{"used_time":None,"input_tokens":None,"output_tokens":None}

    # def extract_answer(self, question):
    #     """
    #     简单的关键字匹配来从key_fact_dict中提取答案。
    #     可根据实际需求增强此方法的逻辑。
    #     """
    #     for key, value in self.key_fact_dict.items():
    #         if key in question:
    #             return value
    #     return None
