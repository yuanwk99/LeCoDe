# agents/lawyer_agent.py

import os
# from logging_system.logger import Logger
from lecode_util.call_llm import ask_llm

class LawyerAgent:
    def __init__(self, lawyer_prompt, suggestion_prompt,lawyer_mode):
        self.prompt = lawyer_prompt
        self.suggestion_prompt = suggestion_prompt
        self.lawyer_mode = lawyer_mode
        # self.logger = logger


    def get_response(self, dialogue_context,question_turn_num,model_name,max_dialoge_turn):
        if self.lawyer_mode== "direct_ask":
            try:
                # messages = [
                #     {"role": "system", "content": self.prompt},
                #     {"role": "user", "content": dialogue_context}
                # ]
                if question_turn_num<=max_dialoge_turn:

                    p = self.prompt.replace("{current_dialogue}",dialogue_context)

                    response,token_infomration = ask_llm(p, model=model_name)#ask_tyqw(p)
                else:
                    p = self.suggestion_prompt.replace("{current_dialogue}",dialogue_context)
                    response,token_infomration = ask_llm(p, model=model_name)#ask_tyqw(p)

                # Log the response
                # self.logger.log("Lawyer", response)
                return response,token_infomration
            except Exception as e:
                # self.logger.log("Error", f"LawyerAgent Error: {str(e)}")
                return "抱歉，我遇到了问题无法继续。",{"used_time":None,"input_tokens":None,"output_tokens":None}
            
            
        elif self.lawyer_mode== "fewshot_ask":
            try:
                # messages = [
                #     {"role": "system", "content": self.prompt},
                #     {"role": "user", "content": dialogue_context}
                # ]
                if question_turn_num<=max_dialoge_turn:

                    p = self.prompt.replace("{current_dialogue}",dialogue_context)

                    response,token_infomration = ask_llm(p, model=model_name)#ask_tyqw(p)
                else:
                    p = self.suggestion_prompt.replace("{current_dialogue}",dialogue_context)
                    response,token_infomration = ask_llm(p, model=model_name)#ask_tyqw(p)

                # Log the response
                # self.logger.log("Lawyer", response)
                return response,token_infomration
            except Exception as e:
                # self.logger.log("Error", f"LawyerAgent Error: {str(e)}")
                return "抱歉，我遇到了问题无法继续。",{"used_time":None,"input_tokens":None,"output_tokens":None}

        elif self.lawyer_mode== "mediq_ask":
            prompt_dict = self.prompt
            # prompt_initial = prompt_dict['initial_assessment']
            prompt_abstain = prompt_dict['abstain']
            prompt_ask = prompt_dict['ask']
            prompt_suggestion = prompt_dict['suggestion']
            try:
                # messages = [
                #     {"role": "system", "content": self.prompt},
                #     {"role": "user", "content": dialogue_context}
                # ]
#                 if question_turn_num==0:
#                     # 不要有response response_initial_assessment，把这个写在外边
#                     initial_p = prompt_initial.replace("{current_dialogue}",dialogue_context)
#                     response_initial_assessment,token_infomration = ask_llm(p, model=model_name)
                    
                    
                if question_turn_num<=max_dialoge_turn:

                    abstain_p = prompt_abstain.replace("{current_dialogue}",dialogue_context)
                    

                    response_p,token_infomration = ask_llm(abstain_p, model=model_name)#ask_tyqw(p)
                    
                    if "yes" in response_p.lower():
                        p = prompt_suggestion.replace("{current_dialogue}",dialogue_context)
                        response,token_infomration = ask_llm(p, model=model_name)#ask_tyqw(p)
                    else:
                        p = prompt_ask.replace("{current_dialogue}",dialogue_context)
                        response,token_infomration = ask_llm(p, model=model_name)#ask_tyqw(p)
                        
                        
                else:
                    p = self.suggestion_prompt.replace("{current_dialogue}",dialogue_context)
                    response,token_infomration = ask_llm(p, model=model_name)#ask_tyqw(p)

                # Log the response
                # self.logger.log("Lawyer", response)
                return response,token_infomration
            except Exception as e:
                # self.logger.log("Error", f"LawyerAgent Error: {str(e)}")
                return "抱歉，我遇到了问题无法继续。",{"used_time":None,"input_tokens":None,"output_tokens":None}
