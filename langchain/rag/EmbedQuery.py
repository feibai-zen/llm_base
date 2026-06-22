from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()
loader = PyPDFLoader("../../resources/Corporate_Action.pdf")
pages = loader.load_and_split()

# 文档切分
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=100,
    length_function=len,
    add_start_index=True
)

# 文档切割
paragraphs = []
for page in pages:
    paragraphs.extend(text_splitter.create_documents([page.page_content]))

# 文档向量化
db = Chroma.from_documents(paragraphs, OpenAIEmbeddings())

# 向量化查询
query = "llama2有多少参数？"
docs = db.similarity_search(query)
for doc in docs:
    print(f"{doc.page_content}\n-------\n")

# 使用检索器进行查询
retriever = db.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"score_threshold": 0.5, "k": 1}
)
docs = retriever.invoke("llama2有多少参数？")
print(docs)
