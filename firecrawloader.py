from langchain_community.document_loaders import FireCrawlLoader
from dotenv import load_dotenv
import os

load_dotenv()

loader = FireCrawlLoader(
    url="https://python.langchain.com/docs/integrations/chat/",
    mode="scrape",  # หรือ "browser" (ใช้ headless browser)
    api_key=os.getenv("FIRECRAWL_API_KEY")
)

docs = loader.load()
print(docs[0].page_content)