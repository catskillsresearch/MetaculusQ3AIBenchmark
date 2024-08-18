from config import config
from LLM import LLM

class Perplexity(LLM):
    def message(self):
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {config.PERPLEXITY_API_KEY}",
            "content-type": "application/json"  }
        payload = {"model": config.PERPLEXITY_MODEL, "messages": self.messages }
        response = requests.post(url=url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

if __name__=="__main__":
    perp = Perplexity('You are the most deeply knowledgeable web search engine and insightful analyst')
    print(perp.chat(ifp.title))