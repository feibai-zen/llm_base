# 环境准备
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from IPython.display import Image, display
import os

load_dotenv()
API_KEY = os.getenv("SILICON_API_KEY")
model = init_chat_model(
    model="Qwen/Qwen3-8B",
    model_provider="openai",
    base_url="https://api.siliconflow.cn/v1",
    api_key=API_KEY,
    temperature=0.0
)

print(model.invoke("你好，我叫Zen"))


def display_graph(app):
    # 使用 Graphviz 渲染（Colab 最稳定的方案）
    try:
        display(Image(app.get_graph(xray=True).draw_png()))
    except Exception as e:
        print(f"Graphviz 渲染失败: {e}")
        print("\n使用 Mermaid 文本方式显示:")
        print(app.get_graph(xray=True).draw_mermaid())
