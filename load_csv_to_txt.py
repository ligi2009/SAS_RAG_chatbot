import os
import csv
import pandas as pd

# input folder 來源資料的資料夾
# output folder 輸出txt檔的資料夾

def load_and_save_txt(input_folder, output_folder):
    # 確保輸出資料夾存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(input_folder, filename)
            df = pd.read_csv(file_path)
            # 讀取第一行第一列的內容
            chemical_name = df.iloc[0, 0]

            # 確保chemical_name中無非法檔案名字符
            valid_chemical_name = "".join([c if c.isalnum() else "_" for c in chemical_name])
            # 動態生成每個化學物的輸出txt檔案名
            output_path = os.path.join(output_folder, f"{valid_chemical_name}.txt")
            
            data = []
            with open(file_path, 'r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    data.append(row)
    
            try:
                with open(output_path, 'w', encoding='utf-8') as txt_file:
                    for item in data:
                        txt_file.write(f"化學物名稱: {item['化學物名稱']}\n")
                        txt_file.write(f"中文名稱: {item['中文名稱']}\n")
                        txt_file.write(f"風險等級: {item['風險等級']}\n")
                        txt_file.write(f"PubChem CID: {item['PubChem CID']}\n")
                        txt_file.write(f"CAS No.: {item['CAS No.']}\n")
                        txt_file.write(f"危害組別: {item['危害組別']}\n")
                        txt_file.write(f"危害名稱: {item['危害名稱']}\n")
                        txt_file.write(f"危害等級: {item['危害等級']}\n")
                        txt_file.write(f"資料來源: {item['資料來源']}\n")
                        txt_file.write(f"可信度: {item['可信度']}\n")
                        txt_file.write(f"危害分類是否清楚: {item['危害分類是否清楚']}\n")
                        txt_file.write(f"適用地區: {item['適用地區']}\n")
                        txt_file.write(f"適用產業: {item['適用產業']}\n")
                        txt_file.write(f"是否具強制性？: {item['是否具強制性？']}\n")
                        txt_file.write(f"清單連結: {item['清單連結']}\n")
                        txt_file.write(f"註解: {item['註解']}\n")
                        txt_file.write(f"額外註解: {item['額外註解']}\n")
                        txt_file.write(f"預測值: {item['預測值']}\n")
                        txt_file.write("\n")
                print(f"TXT file successfully saved as {output_path}")
            except Exception as e:
                print(f"An error occurred while saving data: {e}")



if __name__ == "__main__":

    # 設定資料夾路徑
    input_folder = './SAS_file'
    output_folder = './SAS_txt_file'

    # 執行函式將所有檔案轉為TXT
    load_and_save_txt(input_folder, output_folder)
