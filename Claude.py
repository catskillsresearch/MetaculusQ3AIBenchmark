import json, requests
from config import config
from LLM import LLM

class Claude(LLM):
       
    def message(self):
        content = self.messages[-1]['content']
        url = "https://www.metaculus.com/proxy/anthropic/v1/messages"
        headers =  {"Authorization": f"Token {config.METACULUS_TOKEN}",
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"}
        data = {"model": "claude-3-5-sonnet-20240620",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": self.system_role + '\n\n' + content}]}
        response = requests.post(url, headers=headers, data = json.dumps(data))
        # Check the response status code
        if response.status_code != 200:
            print("Request failed with status code", response.status_code)
            print(response.text)
        return response.json()['content'][0]['text']

if __name__=="__main__":
    claude = Claude('Please help me.')
    print(claude.chat(ifp.title))