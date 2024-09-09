import streamlit as st
import retriever_chain as rc
import argparse

# 設置命令行參數解析
parser = argparse.ArgumentParser(description='Run chatbot with specific vector database.')
parser.add_argument('chemical_number', type=str, help='The SAS chemical number to specify vector database')

args = parser.parse_args()
SAS_chemical_number = args.chemical_number
load_path = f'./Vector_db/{SAS_chemical_number}'

# 讀取化學物質對應的名稱
def get_chemical_name(chemical_number, mapping_file='./chemical_mapping.txt'):
    with open(mapping_file, 'r') as file:
        for line in file:
            number, name = line.strip().split(':')
            if number == chemical_number:
                return name
    return "Unknown Chemical"  

# 根據用戶輸入的化學品號碼獲取對應的名稱
chemical_name = get_chemical_name(SAS_chemical_number)

# 設置RAG Chain 選用llm model, embedding model
chain = rc.chain(load_path=load_path)

st.title('🧪 SAS GPT')
st.caption("🦙 A SAS GPT powered by Llama3 & NeMo-Guardrails")
st.warning('🤖 Chatbot with 🧪  '  + f"{chemical_name}")

with st.sidebar:
    # 清除聊天歷史按鈕
    st.button('🧹 清除查詢記錄', on_click=lambda: st.session_state.update(messages=[{"role": "assistant", "content": "請輸入想查詢化學物質"}]))
    st.markdown("[🔙 回到SAS平台](https://sas.cmdm.tw)")

# 初始化會話狀態中的消息列表，如果還沒有則創建一個默認的消息
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "請輸入想查詢化學物質"}]

# 顯示會話狀態中的所有消息
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
    
def get_response(query):
    try:
        # 使用 retriever chain 來處理查詢
        response = chain.invoke(query)
        
        # 假設 response 是字典，提取 'output' 或其他關鍵字
        if isinstance(response, dict):
            response_text = response.get('output', '')  # 假設 'output' 是你需要的字段
        else:
            response_text = response  # 如果不是字典，直接使用 response

        # 檢查提取的文本，替換特定的英文訊息為中文
        if response_text.strip() == "I'm sorry, I can't respond to that.":
            response_text = "此問題無法回答，請詢問化學相關問題"

        return response_text, None
    except Exception as e:
        return None, str(e)



# 接收用戶輸入的消息
if prompt := st.chat_input("請輸入想查詢化學物質"):

    # 將用戶消息添加到會話狀態中
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # 構建一個查詢，只包含目前使用者輸入的問題
    query = prompt  # 只使用最新的使用者輸入作為查詢

    with st.spinner("Thinking..."):
        response, error = get_response(query)
        
        if error:
            st.error(f"Error: {error}")
        else:
            # 將模型生成的回應添加到會話狀態中並顯示
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.chat_message("assistant").write(response)

# 清除聊天歷史功能和按鈕
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "請輸入想查詢化學物質"}]
