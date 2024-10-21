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

            # 更改副檔名為.txt
            txt_filename = filename.replace('.csv', '.txt')
            output_path = os.path.join(output_folder, txt_filename)
            
            data = []
            with open(file_path, 'r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    data.append(row)
    
            try:
                with open(output_path, 'w', encoding='utf-8') as txt_file:
                    for item in data:
                        txt_file.write(f"名稱: {item['名稱']}\n")
                        txt_file.write(f"CAS no.: {item['CAS no.']}\n")
                        txt_file.write(f"工業用途: {item['工業用途']}\n")
                        txt_file.write(f"安全性: {item['安全性']}\n")
                        txt_file.write(f"註解: {item['註解']}\n")
                        txt_file.write("\n")
                print(f"TXT file successfully saved as {output_path}")
            except Exception as e:
                print(f"An error occurred while saving data: {e}")

if __name__ == "__main__":
    # 設定資料夾路徑
    input_folder = './SAS_file/Benzene_alternatives'
    output_folder = './Benzene_txt'

    # 執行函式將所有檔案轉為TXT
    load_and_save_txt(input_folder, output_folder)
