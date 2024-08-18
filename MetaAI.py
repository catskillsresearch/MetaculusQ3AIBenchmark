# https://pypi.org/project/meta-ai-api/1.0.6/

from meta_ai_api import MetaAI as mai
from LLM import LLM

class MetaAI(LLM):

    def __init__(self, system_role = "Nice talker"):
        self.ai = mai()
        super().__init__(system_role)
        
    def message(self):
        self.response = self.ai.prompt(message=self.messages[-1]['content'])
        return self.response['message']

if __name__=="__main__":
    ai = MetaAI()
    r = ai.chat(ifp.title)
    print(r)