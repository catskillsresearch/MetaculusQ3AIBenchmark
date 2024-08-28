from Agent import Agent

class Critic (Agent):
    def __init__(self, llm):

        self.system_role = f"""
You a very smart and worldly person reviewing a superforecaster's assignment of probabilities to events.
You will receive an event with probabilities given as |event|id|question|zz|rationale|.
zz is an integer probability from 1 to 99 and rationale is the student's logic for assigning probability of zz.
You will reply with a line |id|feedback| where feedback is "I concur" if you see no problem with the rationale and zz otherwise presents possible problems with the rationale and zz.
"""
        super().__init__(self.system_role, llm)

    def feedback(self, ifp):
        self.fb = 'I prasldfkbeddy.'
        prompt = f"|{ifp.event}|{ifp.id}|{ifp.title}|{ifp.forecast}|{ifp.rationale}|"
        self.fb = self.chat(prompt)
        if '|' in self.fb: # LLM obeyed system role
            self.fb1 = self.fb.split('|')[2:]
            self.fb = ''.join([x.strip() for x in self.fb1 if x])
        ifp.feedback = self.fb 
        print(ifp.id, ifp.feedback)

if __name__=="__main__":
    from MetaAI import MetaAI
    critic = Critic(MetaAI)
    critic.feedback(ifp) 
