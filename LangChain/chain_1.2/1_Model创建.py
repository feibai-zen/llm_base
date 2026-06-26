from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("SILICON_BASE_URL")
API_KEY = os.getenv("SILICON_API_KEY")

model = init_chat_model(
   model="Qwen/Qwen3-8B",
   model_provider="openai",
   base_url = BASE_URL,
   api_key = API_KEY
)  

print(type(model))

print(model.invoke("hi"))