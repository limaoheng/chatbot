import langchain_core.load
import requests
from bs4 import BeautifulSoup
import markdownify
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document
from pydantic import BaseModel


class Scraper(BaseModel):
    url: str
    html_content: str = None
    article_html: str = None
    markdown_content: str = None

    def fetch_article(self):
        """
        Fetch the HTML content of the article.
        Uses a User-Agent header to mimic a browser request.
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(self.url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch the URL: {self.url} with status code {response.status_code}")
        self.html_content = response.text

    def parse_article(self):
        """
        Parse the HTML content to find the article content.
        Raises an exception if the article content is not found.
        """
        if not self.html_content:
            raise Exception("HTML content is not fetched")

        soup = BeautifulSoup(self.html_content, 'html.parser')
        article = soup.find('article')
        if not article:
            raise Exception("Article content not found")
        self.article_html = str(article)

    def convert_to_markdown(self):
        """
        Convert the parsed HTML content to Markdown format.
        Raises an exception if the article HTML content is not parsed.
        """
        if not self.article_html:
            raise Exception("Article HTML content is not parsed")

        self.markdown_content = markdownify.markdownify(self.article_html, heading_style="ATX")

    def get_markdown_as_loader(self):
        self.fetch_article()
        self.parse_article()
        self.convert_to_markdown()

        class InMemoryDocumentLoader(BaseLoader):
            def __init__(self, content, url):
                self.url = url
                self.content = content

            def load(self):
                """
                Load the document content.
                Returns a list with a single Document object containing the markdown content.
                """
                return [Document(page_content=self.content, metadata={"source": self.url})]

        return InMemoryDocumentLoader(self.markdown_content, self.url)


    def save_to_file(self, filename):
        """
        Save the Markdown content to a specified file.
        Raises an exception if the Markdown content is not generated.
        """
        if not self.markdown_content:
            raise Exception("Markdown content is not generated")

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(self.markdown_content)


if __name__ == "__main__":
    try:
        # URL of the Medium article to be scraped
        url = "https://medium.com/@jeongiitae/from-rag-to-graphrag-what-is-the-graphrag-and-why-i-use-it-f75a7852c10c"

        # Create an instance of MediumArticleScraper
        scraper = Scraper(url=url)
        print("Markdown content saved to article.md")

        # Get the Markdown content as a LangChain DocumentLoader
        loader = scraper.get_markdown_as_loader()
        print(loader.load())  # This will print the in-memory Markdown content
    except Exception as e:
        print(f"An error occurred: {e}")