from modules.display import create_display_window

import pandas as pd
file_path = 'data/global_cancer_patients_2015_2024.csv'
data = pd.read_csv(file_path)

#Hàm tạo giao diện
create_display_window(data)