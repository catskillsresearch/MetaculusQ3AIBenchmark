# https://pypi.org/project/hugchat/
from config import config
from hugchat import hugchat
from hugchat.login import Login
from LLM import LLM

class HuggingChat(LLM):

    def __init__(self, system_role = "Nice talker"):
        # Log in to huggingface and grant authorization to huggingchat
        EMAIL = config.HUGGINGFACE_USERNAME
        PASSWD = config.HUGGINGFACE_PASSWORD
        cookie_path_dir = "./cookies/" # NOTE: trailing slash (/) is required to avoid errors
        sign = Login(EMAIL, PASSWD)
        cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)
        self.chatbot = hugchat.ChatBot(cookies=cookies.get_dict()) 
        super().__init__(system_role)
        
    def message(self):
        result = ''.join([x['token'] for x in self.chatbot.chat(self.system_role + '\n\n' + self.messages[-1]['content']) if x])
        return result

    def web_search(self, query):
        query_result = self.chatbot.query(query, web_search=True)
        return query_result
        print(query_result)
        for source in query_result.web_search_sources:
            print(source.link)
            print(source.title)
            print(source.hostname)

    def available_models(self):
        return [(i,str(x)) for i,x in enumerate(self.chatbot.get_available_llm_models())]

    def switch_llm(self, i):
        self.chatbot.switch_llm(i)

    def conversation_info(self):
        info = self.chatbot.get_conversation_info()
        # print(info.id, info.title, info.model, info.system_prompt, info.history)
        return info

if __name__=="__main__":
    hc = HuggingChat()
    hc.switch_llm(1)
    print(hc.chat(ifp.title))