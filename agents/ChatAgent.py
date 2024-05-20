from typing import Optional

from langchain_groq import ChatGroq

from langchain_core.prompts import ChatPromptTemplate

class ChatAgent:

    DELIMITER = "####"
    SYSTEM_MESSAGE = """\
        You will be provided with customer service queries. \
        Output a friendly reply to the customer based on the context provided \
        If you don't know the answer, say: 

        'Sorry, I don't know the answer to your question'.

        For example:
        Q: What is Google?
        A: Sorry, I don't know the answer to your question.

        The context will writing as markdown langauge and between ####

        Each context will be separated by using ````
        
        Here starts the context:
        
        ####
        {most_relevant_docs}
        ####

        """

    def __init__(self):
        self.LLM = ChatGroq(temperature=0.7, model="llama3-70b-8192")



    def get_input(self) -> str:
        print("Insert your text. Enter 'q' or press Ctrl-D (or Ctrl-Z on Windows) to end.")
        contents = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            if line == "q":
                break
            contents.append(line)
        return "\n".join(contents)

    def get_completion_from_messages(self, user_message: str, context: Optional[str] = None) -> str:
        messages = [
            ("system", self.SYSTEM_MESSAGE),
            ('human', f"{user_message}"),
        ]
        prompt = ChatPromptTemplate.from_messages(messages)

        chain = prompt | self.LLM
        response = chain.invoke({"most_relevant_docs": context})
        return response.content