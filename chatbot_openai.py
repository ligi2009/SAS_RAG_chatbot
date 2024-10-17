import streamlit as st
import retriever_chain_openai as rc
import argparse
from langchain.vectorstores import Chroma
# from langchain_community.vectorstores import Chroma
import vectorstore as vs
from retriever_chain_openai import format_docs

# 設置命令行參數解析
parser = argparse.ArgumentParser(description='Run chatbot with specific vector database.')
parser.add_argument('chemical_number', type=str, help='The SAS chemical number to specify vector database')

args = parser.parse_args()
SAS_chemical_number = args.chemical_number

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

st.title('🧪 SAS GPT')
st.caption("🦙 A SAS GPT powered by ChatGPT-4o & NeMo-Guardrails") #更改使用模型名稱
st.warning('🤖 Chatbot with 🧪  '  + f"{chemical_name}")

with st.sidebar:
    # 清除聊天歷史按鈕
    st.button('🧹 清除查詢記錄', on_click=lambda: st.session_state.update(messages=[{"role": "assistant", "content": "請輸入化學物質相關問題"}]))
    st.markdown("[🔙 回到SAS平台](https://sas.cmdm.tw)")

# 初始化會話狀態中的消息列表，如果還沒有則創建一個默認的消息
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "請輸入化學物質相關問題"}]

# 顯示會話狀態中的所有消息
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Ｔell if it is a summary question 
def is_summary_query(query):
    summary_keywords = ["總結", "概述", "摘要", "回顧", "重點", "要點", "整理", "summary", "summarize", "summarization", "conclude"]
    return any(keyword in query for keyword in summary_keywords)
# or use NLP model to tell?

def get_response(query):
    try:
        if is_summary_query(query):
            load_path = [f'./Vector_db/59_sum']
        else:
            load_path = [
                f'./Vector_db/59_sum', 
                f'./Vector_db/59_rm_duplicate', 
                f'./Vector_db/59_alternatives_industrial', 
                f'./Vector_db/59_alternatives_children_product', 
                f'./Vector_db/59_alternatives_commercial', 
                f'./Vector_db/59_alternatives_consumer', 
                f'./Vector_db/59_alternatives_consumer_or_commercial', 
                f'./Vector_db/59_alternatives_hydraulic_fluid', 
                f'./Vector_db/59_alternatives_polymers'
            ]
            # load_path = [
            #     f'./Vector_db/59_sum', 
            #     f'./Vector_db/59_rm_duplicate', 
            #     f'./Vector_db/59_1', 
            #     f'./Vector_db/59_2', 
            #     f'./Vector_db/59_3', 
            #     f'./Vector_db/59_4', 
            #     f'./Vector_db/59_5', 
            #     f'./Vector_db/59_6', 
            #     f'./Vector_db/59_7'
            # ]
        # 設置RAG Chain 選用llm model, embedding model
        chain = rc.chain(load_path=load_path)
        response = chain.invoke(query)
        if isinstance(response, dict):
            response_text = response.get('output', '')
        else:
            response_text = response

        if response_text.strip() == "I'm sorry, I can't respond to that.":
            response_text = "此問題無法回答，請試著詢問其他化學物質相關問題"

        return response_text, None

    except Exception as e:
        return None, str(e)

# 接收用戶輸入的消息
if prompt := st.chat_input("請輸入化學物質相關問題"):

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
    st.session_state.messages = [{"role": "assistant", "content": "請輸入化學物質相關問題"}]
