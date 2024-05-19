from dataclasses import dataclass
from typing import Literal, List
from langchain_community.document_loaders import FireCrawlLoader
import json

from langchain_core.documents import Document


@dataclass
class WebsiteCrawler:

    def __init__(self):
        self.loader = None

    def load_doc(self, url: str, mode: Literal["crawl", "scrape"] = "scrape" ):

        if url is None:
            return None
        self.loader: FireCrawlLoader = FireCrawlLoader(
            mode=mode,
            url=url.strip()
        )
        docs = self.loader.load()
        docs = self.clean_metadata(docs)
        return docs


    # Define the metadata extraction function.
    def clean_metadata(self, docs: List[Document]) -> List[Document]:
        for record in docs:
            cleaned_metadata = {}
            metadata = record.metadata
            for key, value in metadata.items():
                if isinstance(value, list):
                    if not value:
                        continue  # Skip empty arrays
                    else:
                        print(f"Size of the list for key '{key}':", len(value))  # Print size of the list
                if isinstance(value, (list, dict)):
                    cleaned_metadata[key] = json.dumps(value)  # Convert lists and dicts to JSON strings
                else:
                    cleaned_metadata[key] = value  # Keep other types as is

            metadata = cleaned_metadata
            record.metadata = metadata
        return docs