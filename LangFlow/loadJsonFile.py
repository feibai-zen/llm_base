from langflow.load import run_flow_from_json
from dotenv import load_dotenv
import os
import sys

# 加载项目根目录的 .env 文件
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path)
os.environ['OPENAI_API_KEY'] = os.environ['DEEP_SEEK_API_KEY']
print("已设置 OPENAI_API_KEY")


def chat_with_flow(flow_path: str, session_id: str = None):
    """
    与 Langflow 流程进行交互式问答
    
    Args:
        flow_path: Langflow 导出的 JSON 流程文件路径
        session_id: 会话 ID（可选，用于保持对话上下文）
    """
    print("=" * 50)
    print("欢迎使用 Langflow 智能助手！")
    print("输入 'quit' 或 'exit' 退出对话")
    print("=" * 50)

    # 如果没有提供 session_id，创建一个
    if not session_id:
        session_id = "default_session"

    while True:
        # 获取用户输入
        user_input = input("\n你: ").strip()

        # 检查退出条件
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n感谢使用，再见！")
            break

        # 跳过空输入
        if not user_input:
            continue

        try:
            # 运行流程
            print("\n助手: ", end="", flush=True)

            result = run_flow_from_json(
                flow=flow_path,
                input_value=user_input,
                session_id=session_id,
                disable_logs=True,
                input_type="chat",
                output_type="chat"
            )

            # 解析并输出结果
            if result and len(result) > 0:
                # result 是 RunOutputs 对象列表
                response_text = ""

                for run_output in result:
                    # 方式1: 从 messages 属性获取（ChatOutputResponse 对象）
                    if hasattr(run_output, 'messages') and run_output.messages:
                        for msg in run_output.messages:
                            if hasattr(msg, 'message') and msg.message:
                                response_text = msg.message
                                break

                    # 方式2: 从 outputs.artifacts 获取
                    if not response_text and hasattr(run_output, 'outputs'):
                        for out in run_output.outputs:
                            if hasattr(out, 'artifacts') and out.artifacts:
                                artifacts = out.artifacts
                                if isinstance(artifacts, dict) and 'message' in artifacts:
                                    response_text = artifacts['message']
                                    break

                    # 方式3: 从 outputs.results 获取
                    if not response_text and hasattr(run_output, 'outputs'):
                        for out in run_output.outputs:
                            if hasattr(out, 'results') and out.results:
                                results = out.results
                                if isinstance(results, dict) and 'message' in results:
                                    msg_obj = results['message']
                                    if hasattr(msg_obj, 'data'):
                                        data = msg_obj.data
                                        if isinstance(data, dict) and 'text' in data:
                                            response_text = data['text']
                                            break

                    # 打印响应
                    if response_text:
                        print(response_text)
                    else:
                        print("(无响应)")
            else:
                print("(无响应)")

        except Exception as e:
            print(f"\n错误: {str(e)}")
            print("请检查流程配置和环境变量是否正确设置")


if __name__ == "__main__":
    # 流程文件路径
    flow_file = "../resources/flow/first-chat-agent.json"

    # 检查文件是否存在
    if not os.path.exists(flow_file):
        print(f"错误: 找不到流程文件 {flow_file}")
        print("请确保流程文件在当前目录下")
        exit(1)

    # 开始交互式对话
    chat_with_flow(flow_file)
