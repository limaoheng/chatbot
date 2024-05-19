
from ChatAgent import ChatAgent
from vectors.VectorStore import VectorStore
from vectors.WebsiteCrawler import WebsiteCrawler
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

print("Please input the URL you would like to ask about.")
url: str = input()

crawler: WebsiteCrawler = WebsiteCrawler()
docs = crawler.load_doc(url=url.strip(), mode="scrape")

store: VectorStore = VectorStore()

retriever = store.load_data(docs)

print("Insert your text. Each line would start the chat. Enter 'q' or press Ctrl-D (or Ctrl-Z on Windows) to end.")
chatbot = ChatAgent()
while True:
    try:
        line = input()
    except EOFError:
        break
    if line == "q":
        break
    related_docs_str = store.similarity_search(line)
    response = chatbot.get_completion_from_messages(user_message=line, context=related_docs_str)
    print(response)
