# Chatbot with webpage scraping ability

This application is a CMD-based application, and you can query the underlying LLM about certain webpage knowledge. 

Furthermore, you can also ask it to crawl the entire website for a certain domain knowledge. 

This can also be used as a base project for a RAG QA system. 

## Installation

Please adding a .env file to put the necessary API keys in. 

For example, I am using GROQ with FireCrawl to do the job - It's cheaper than constantly sending tokens to OpenAI. 

```python
GROQ_API_KEY=groq-api-key
FIREWALL_API_KEY=fc-api-key
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
