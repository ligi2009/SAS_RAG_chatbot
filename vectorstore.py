import time
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
import load_csv_to_txt as lc

def load_and_split_documents(file_path, chunk_size, chunk_overlap):
    """加載文檔並進行文本分割"""
    loader = TextLoader(file_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(documents)

def initialize_embeddings(model_name="all-MiniLM-L6-v2", device="cpu", normalize_embeddings=False):
    """初始化嵌入模型"""
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={'device': device},
        encode_kwargs={'normalize_embeddings': normalize_embeddings},
        multi_process=True,
        show_progress=True
    )

def save_to_chroma(docs, embeddings, output_path):
    """保存文檔到向量數據庫"""
    try:
        Vector_db = Chroma.from_documents(docs, embeddings, persist_directory=output_path)
        print(f"Vector_db successfully saved to {output_path}")
    except Exception as e:
        print(f"An error occurred while saving data: {e}")

def main():
    chunk_size = int(input("Enter the chunk size: "))
    chunk_overlap = int(input("Enter the chunk overlap: "))
    output_name = input("Enter the output file name(SAS chemical number): ")
    output_path = f'./Vector_db/{output_name}'

    start_time = time.time()

    # 加載和分割文檔
    docs = load_and_split_documents(file_path, chunk_size, chunk_overlap)

    # 初始化嵌入模型
    hf = initialize_embeddings()

    # 保存為向量數據庫
    save_to_chroma(docs, hf, output_path)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Script executed in {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    # file_path = './SAS_txt_file/Benzene.txt'
    file_path = './Benzene_txt/Benzene_summary_gpt.txt'
    # file_path = './Benzene_txt/Benzene_remove_duplicate.txt' # 59_rm_duplicate
    # file_path = './Benzene_txt/Benzene_alternatives_Childrens_Products.txt'
    main()
