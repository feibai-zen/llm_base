from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
embeddings_model = OpenAIEmbeddings()

embeddings = embeddings_model.embed_documents(["Hello world", "hi, how are you", "what is your name"])

print(len(embeddings), len(embeddings[0]))
print(embeddings[0][0:5])