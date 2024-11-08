import os
import requests
import pandas as pd
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
'''
因為下載 CSV 檔案時 跳過了 SSL 驗證 (verify=False)
所以會有InsecureRequestWarning警告 這邊設定不要警告 如果你們組別在執行py檔案時出錯 
試著註解調第6行 也順便註解第4行呼叫 urllib3 函式庫
'''

URL = 'https://od.cdc.gov.tw/eic/NHI_EnteroviralInfection.csv'
FILENAME = 'NHI_EnteroviralInfection.csv'
current_dir = os.getcwd()
target_folder = os.path.join(current_dir, '3')

if not os.path.exists(target_folder):
    #儲存在根目錄下資料夾名稱為'3'底下，這邊可以根據你們要下載的路徑去修改
    os.makedirs(target_folder)  

output_file = os.path.join(target_folder, FILENAME)

try:
    response = requests.get(URL, verify=False)
    response.raise_for_status()
    with open(output_file, 'wb') as file:
        file.write(response.content)
    print(f'檔案已成功下載並儲存至：{output_file}')
except requests.exceptions.RequestException as e:
    print(f'下載失敗: {e}')
    exit()

'''
#因為我實在看不懂你們教授的pdf檔在供沙小 所以我只留總人次 如果要原封不動
#直接註解第'39'行到'41行'
'''

df = pd.read_csv(output_file)
filtered_df = df[['健保就診總人次']]
filtered_df.to_csv(output_file, index=False)

print(f'篩選後的檔案已儲存至：{output_file}')