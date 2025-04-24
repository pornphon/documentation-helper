import os

from dotenv import load_dotenv

load_dotenv()

from langchain.text_splitter import RecursiveCharacterTextSplitter
#from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from consts import INDEX_NAME

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


def ingest_docs():
   #loader = ReadTheDocsLoader("langchain-docs/api.python.langchain.com/en/latest")

    loader = DirectoryLoader(
        "langchain-docs/api.python.langchain.com/en/latest",
        glob="**/*.html",  # เปลี่ยนเป็น *.txt หรือ *.rst ตามประเภทไฟล์ของคุณ
        loader_cls=lambda path: TextLoader(path, encoding="utf-8")
    )


    raw_documents = loader.load()
    print(f"loaded {len(raw_documents)} documents")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    documents = text_splitter.split_documents(raw_documents)
    for doc in documents:
        new_url = doc.metadata["source"]
        new_url = new_url.replace("langchain-docs", "https:/")
        doc.metadata.update({"source": new_url})
        


    print(f"Going to add {len(documents)} to Pinecone")
    

   

    #PineconeVectorStore.from_documents(documents, embeddings, index_name=INDEX_NAME,batch_size=5)


    batch_size = 10
    delay_secs = 1  # ปรับ delay ตามต้องการ

    for i in range(0, len(documents), batch_size):
        batch_docs = documents[i:i + batch_size]
        PineconeVectorStore.from_documents(batch_docs, embeddings, index_name=INDEX_NAME)


        ##texts = [doc.page_content for doc in batch_docs]
        ##metadatas = [doc.metadata for doc in batch_docs]

        # สร้าง embedding แล้ว upsert ทีละ batch
        ##vectors = embeddings.embed_documents(texts)

        # PineconeVectorStore.from_texts(
        #     texts,
        #     embeddings=embeddings,
        #     metadatas=metadatas,
        #     index_name=INDEX_NAME
        # )

        print(f"✅ Uploaded batch {i // batch_size + 1}")
        ##time.sleep(delay_secs)  # 👈 Sleep เพื่อไม่ให้โดน RateLimit








    print("****Loading to vectorstore done ***")


def ingest_docs2() -> None:
    from langchain_community.document_loaders.firecrawl import FireCrawlLoader

    langchain_documents_base_urls = [
        "https://python.langchain.com/docs/integrations/chat//",
        "https://python.langchain.com/docs/integrations/llms/",
        "https://python.langchain.com/docs/integrations/text_embedding/",
        "https://python.langchain.com/docs/integrations/document_loaders/",
        "https://python.langchain.com/docs/integrations/document_transformers/",
        "https://python.langchain.com/docs/integrations/vectorstores/",
        "https://python.langchain.com/docs/integrations/retrievers/",
        "https://python.langchain.com/docs/integrations/tools/",
        "https://python.langchain.com/docs/integrations/stores/",
        "https://python.langchain.com/docs/integrations/llm_caching/",
        "https://python.langchain.com/docs/integrations/graphs/",
        "https://python.langchain.com/docs/integrations/memory/",
        "https://python.langchain.com/docs/integrations/callbacks/",
        "https://python.langchain.com/docs/integrations/chat_loaders/",
        "https://python.langchain.com/docs/concepts/",
    ]

    langchain_documents_base_urls2 = [
        "https://python.langchain.com/docs/integrations/chat/"
    ]
    for url in langchain_documents_base_urls:
        print(f"FireCrawling {url=}")
        loader = FireCrawlLoader(
            url=url,
            mode="scrape",
        )
        docs = loader.load()

        print(f"Going to add {len(docs)} documents to Pinecone")
        PineconeVectorStore.from_documents(
            docs, embeddings, index_name="897-museumsiam-onlinegallery25"
        )
        print(f"****Loading {url}* to vectorstore done ***")


if __name__ == "__main__":
    ingest_docs()
