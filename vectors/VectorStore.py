import dataclasses
from typing import List, ClassVar
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_core.vectorstores import VectorStoreRetriever
from pydantic import BaseModel

class VectorStore(BaseModel):

    COLLECTION_NAME:ClassVar[str] = 'temp_collection'
    # Define attributes without initializing them in __init__
    _client: chromadb.Client = None
    _gpt4all_embd: GPT4AllEmbeddings = None
    _text_splitter: RecursiveCharacterTextSplitter = None
    _vectorstore: Chroma = None

    def __init__(self, **data):
        super().__init__(**data)
        # Initialize Chroma DB client
        self._client = chromadb.Client()
        self._gpt4all_embd = GPT4AllEmbeddings()
        self._text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=1000, chunk_overlap=0
        )
        self._vectorstore = None


    def load_data(self, docs: List) -> VectorStoreRetriever:
        splits = self._text_splitter.split_documents(docs)
        self._vectorstore = Chroma.from_documents(splits,
                                                  self._gpt4all_embd,
                                                  collection_name=VectorStore.COLLECTION_NAME)
        return self._vectorstore.as_retriever()

    # Similarity Search
    def similarity_search(self, search_str: str):
        searched_docs = self._vectorstore.similarity_search(search_str)
        most_relevant_doc = "\r\n````\r\n".join([doc.page_content for doc in searched_docs])
        return most_relevant_doc