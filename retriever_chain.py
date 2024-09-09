import asyncio
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from nemoguardrails import RailsConfig
from nemoguardrails.integrations.langchain.runnable_rails import RunnableRails
import vectorstore as vs

def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])

# 建立RAG Chain 選擇llm model, embedding model, vector database
def chain(llm_model='llama3', load_path=None):
    llm = ChatOllama(model=llm_model, temperature=0.3)
    embeddings = vs.initialize_embeddings()
    db_load = Chroma(persist_directory=load_path, embedding_function=embeddings)
    retriever = db_load.as_retriever()
    

    template = """
    你是一個專注在回答化學領域相關問題的專家。
    你的任務是根據上下文的內容來回答使用者提出的問題。
    請注意：

    1. 你只能回答與化學物質相關的問題，對於非化學物質的問題，請回答「此問題無法回答，請詢問化學相關問題」。
    2. 只回答使用者目前的問題，不要重複之前已經回答過的問題。
    3. 如果不知道答案，請明確回答「此問題無法回答，請詢問化學相關問題」，不要生成無關的答案。
    4. 只使用繁體中文回答問題。
    5. 如果使用只想要總結過去問過的答案就必須提供給使用者。
    6. 盡可能使用敘述的方式回答問題。

    上下文內容：{context}
    問題：{question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    config = RailsConfig.from_path("./config")
    
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    guardrails = RunnableRails(config)
    chain_with_guardrails = guardrails | chain
    
    return chain_with_guardrails

if __name__ == "__main__":
    my_chain = chain()
    
