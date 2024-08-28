# pip install asknews
# https://colab.research.google.com/drive/1tc383HraMZOiyfKFF1EXAtlTYbsuv3Q5?usp=sharing

from config import config
from asknews_sdk import AskNewsSDK
import json, datetime
from IFP import IFP

def save_news(ifp, news):
    fn = f'asknews_for_question/{ifp.id}.json'
    with open(fn, 'w') as f:
        json.dump(news, f)
        print('saved', fn)

class AskNews():

    def __init__(self):
        ASKNEWS_CLIENT_ID = config.ASKNEWS_CLIENT_ID
        ASKNEWS_SECRET = config.ASKNEWS_SECRET
        
        self.ask = AskNewsSDK(
              client_id=config.ASKNEWS_CLIENT_ID,
              client_secret=config.ASKNEWS_SECRET,
              scopes=["news"])

        self.cache = {}
        
    def query(self, 
              q, 
              method,    # use "nl" for natural language for your search, or "kw" for keyword, or 'both'
              strategy,
              end_timestamp,
              return_type="dicts"): # strategy="latest news" enforces looking at the latest news only
                         # strategy="news knowledge" looks for relevant news within the past 60 days
        if end_timestamp is not None:
            return self.ask.news.search_news(
                    query=q, # your keyword query
                    n_articles=10, # control the number of articles to include in the context
                    return_type=return_type,  # you can also ask for "dicts" if you want more information
                    method=method, 
                    end_timestamp = end_timestamp,
                    strategy=strategy).as_dicts # strategy="latest news" enforces looking at the latest news only,
        else:
            return self.ask.news.search_news(
                    query=q, # your keyword query
                    n_articles=10, # control the number of articles to include in the context
                    return_type=return_type,  # you can also ask for "dicts" if you want more information
                    method=method, 
                    strategy=strategy).as_dicts # strategy="latest news" enforces looking at the latest news only,   

    def multi_strategy(self, q, end_timestamp, return_type="dicts"):
        all = []
        R = {}
        for strategy in ['latest news', 'news knowledge']:
            R[strategy] = []
            for x in self.query(q, 'both', strategy, end_timestamp):
                all.append(x.summary if return_type=="dicts" else x)
                x = x.dict()
                x['article_url'] = x['article_url'].unicode_string()
                for y in ['article_id', 'pub_date']:
                    x[y] = str(x[y])
                R[strategy].append(x)
        print("ALL")
        print(all[0])
        all = list(set(all))
        return '\n\n'.join(all), R

    def research(self, group, end_timestamp = None, return_type="dicts"):
        if end_timestamp is None:
            now = datetime.datetime.now().timestamp()
            end_timestamp=int(now)       
        q = '\n'.join(ifp.title.strip() for ifp in group)
        print("Researching", q)
        try:
            return self.cache[q]
        except:
            news, self.R = self.multi_strategy(q,end_timestamp,return_type)
            for ifp in group:
                save_news(ifp, self.R)
            self.cache[q] = news
        return news

if __name__=="__main__":
    ask = AskNews()
    group = [IFP(id) for id in [26771, 26772, 26773, 26774]]
    news = ask.research(group)
    print(news)