from Agent import Agent

class QuestionRelator(Agent):
    def __init__(self, llm):
        self.system_role = f"""
You are prompted with list of forecasting questions, each with an id and a title.
Label each question with an underlying event.
If the questions are for the same event, use the same name for the underlying event.
Please return as separate lines formatted as |event|id|title|, do not add any other formatting.
"""
        super().__init__(self.system_role, llm)

    def relate(self, ifps):
        prompt = '\n'.join([f"{ifp.id}: {ifp.title}" for ifp in ifps.values()])
        KL = self.chat(prompt)
        print(KL)
        K1 = [x.split('|') for x in KL.split('\n')]
        self.topic_map = [(int(id),event) for _,event,id,_,_ in K1]
        self.topics = set([event for id,event in self.topic_map])
        self.topic_groups = {topic: [ifps[x] for x,y in self.topic_map if y == topic] for topic in self.topics}
        for id,event in self.topic_map :
            ifps[id].event = event
        return self.topic_groups

if __name__=="__main__":
    from MetaAI import MetaAI
    
    try:
        ifps
    except:
        test_day = '01AUG24'
        ifps = {id: IFP(id) for id in history[test_day]}
    qr = QuestionRelator(MetaAI)
    print(qr.relate(ifps))