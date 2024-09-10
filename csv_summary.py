import pandas as pd
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
import os
import time  # 引入 time 模組


# 讀取原始的 CSV 檔案
input_file = './SAS_file/Benzene.csv'
df = pd.read_csv(input_file)

# 初始化 ChatOpenAI 模型
llm = ChatOllama(model='mixtral:8x7b', temperature=0.1)
# llm = ChatOpenAI(model='gpt-4o', temperature=0.1)
# 創建一個新欄位來存放生成的文本
df['Summary'] = ""

# 開始計時
start_time = time.time()

for index, row in df.iterrows():
    # 將整行轉換為一個字串格式，以便於生成敘述
    input_text = ','.join(row.astype(str))  # 將每列轉為字串並以逗號分隔
    prompt = f"""
    依據以下欄位資訊：
    化學物名稱,中文名稱,風險等級,PubChem CID,CAS No.,危害組別,危害名稱,危害等級,資料來源,可信度,
    危害分類是否清楚,適用地區,適用產業,是否具強制性？,清單連結,註解,額外註解,預測值，

    利用以下範本，將CSV檔內容中每一行內容進行敘述性轉換，只使用繁體中文，並且有明顯的段落區隔：

    苯（Benzene），CAS 編號為 71-43-2，風險等級為 1，PubChem CID 為 241。
    該物質屬於慢毒性危害，主要的危害為致癌性，危害等級為高，根據歐洲化學總署公告的 REACH 法規附件 17，可信度相對較高，且危害等級分類明確。
    此危害適用於歐盟地區，主要影響製造業（C 類）。
    該物質在 REACH 法規中的附錄 17 中列出，該清單包含 C（致癌性）、M（致突變性）、R（生殖毒性）物質，且相關 CAS 編號記載於 REACH 法規 EC (No) 1907/2006 的附錄 1-6，並會隨著法規修訂進行更新。
    該法規在歐盟地區具有強制性要求，相關清單可通過以下連結查閱：限制物質清單，REACH 法規，以及 歐盟法律文本。此物質的危害分類屬於第一級或第二級。

    苯（Benzene），CAS 編號為 71-43-2，風險等級為 1，PubChem CID 為 241。
    此物質屬於慢毒性危害，主要危害為致癌性，危害等級為高，根據歐盟 GHS 的資料來源，可信度相對較高，且危害等級分類清楚。
    該危害適用於歐盟地區，主要影響製造業（C 類）。此物質的危害等級被列為第 1A 或 1B 級的致癌性危害，並對應 H350 或 H350i（吸入性）。
    相關的歐盟 GHS 調和分類的最新清單，可通過以下連結查閱：化學物質資訊資料庫，以及 CLP 法規附錄 VI。
    這些清單會定期更新，並提供所有相關 CAS 編號與調和分類的 Excel 清單下載功能。

    苯（Benzene），CAS 編號為 71-43-2，風險等級為 1，PubChem CID 為 241。
    該物質屬於慢毒性危害，主要危害為致癌性，危害等級為高。根據國際癌症研究機構（IARC）清單，該資料來源的可信度相對較高，且危害等級分類清楚。
    此物質的危害適用於全球所有地區與產業。
    根據 IARC 分類，苯被歸類為第 1 類（已知人類致癌物）或第 2A 類（極可能為人體致癌物）。相關清單可通過以下連結查閱：IARC 分類清單，清單中會列出相關 IARC 專題研究的卷冊或補充資料，物質可按 CAS 編號、名稱或作為物質群體列出。此清單不具強制性。

    \n\n{input_text}\n\n"""

    # 呼叫模型進行生成
    response = llm.invoke([("human", prompt)])
    generated_text = response.content
    
    # 將生成的文本存入 DataFrame 的新欄位
    df.at[index, 'Generated_Text'] = generated_text

# 計算總共花費的時間
end_time = time.time()
elapsed_time = end_time - start_time

# 儲存為新的 CSV 檔案
output_file = './SAS_file/Benzene_sum.csv'
df.to_csv(output_file, index=False)

print(f"生成的文字已存為: {output_file}")
print(f"程式執行總共花費了 {elapsed_time:.2f} 秒")
