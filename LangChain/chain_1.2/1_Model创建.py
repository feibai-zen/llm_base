from langchain.chat_models import init_chat_model

model = init_chat_model(
   model="Qwen/Qwen3-8B",
   model_provider="openai",
   base_url = "https://api.siliconflow.cn/v1",
   api_key="sk-tkzelvayjnjhxtnjninzltxzspuiukahorrrhwnokcodbtdl"
)  

print(type(model))

print(model.invoke("hi"))