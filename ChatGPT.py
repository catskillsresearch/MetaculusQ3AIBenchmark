from config import config
from LLM import LLM
from openai import OpenAI

class ChatGPT(LLM):
    def __init__(self, system_role):
        super().__init__(system_role)
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)

    def message(self):
        chat_completion = self.client.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages= self.messages)
        return chat_completion.choices[0].message.content

if __name__=="__main__":
    oai = ChatGPT('You are the most deeply knowledgeable web search engine and insightful analyst')
    print(oai.chat(ifp.title))