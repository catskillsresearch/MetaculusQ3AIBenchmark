from Agent import Agent

class Summarizer (Agent):
    def __init__(self, llm):

        self.system_role = f"""
You a very smart and worldly person reviewing a sequence of rationales given by a team of superforecaster.
Please summarize the rationales in a single statement which is as self-consistent as possible
"""
        super().__init__(self.system_role, llm)

    def summarize(self, prompt):
        return self.chat(prompt)
