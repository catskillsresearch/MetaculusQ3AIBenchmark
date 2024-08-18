import json, requests
from config import config
from LLM import LLM

class MetacGPT(LLM):

    def __init__(self, system_role):
        super().__init__(system_role)
        
    def message(self):
        url = "https://www.metaculus.com/proxy/openai/v1/chat/completions"
        headers =  {"Authorization": f"Token {config.METACULUS_TOKEN}",
                    "content-type": "application/json"}
        data = {"model": "gpt-4o",
                "max_tokens": 1024,
                "messages": self.messages}
        response = requests.post(url, headers=headers, data = json.dumps(data))
        # Check the response status code
        if response.status_code != 200:
            print("Request failed with status code", response.status_code)
            print(response.text)
        self.rec = response.json()
        return self.rec ['choices'][0]['message']['content']

if __name__=="__main__":
    mgpt = MetacGPT('Please help me')
    print(mgpt.chat('Bruce Bueno de Mesquita'))