import pandas as pd
import tkinter as tk
from tkinter import messagebox

#Hàm thêm dữ liệu vào file csv
def create(data, entries, file_path):

    # Thêm dữ liệu mới vào DataFrame
    data = data._append(entries, ignore_index=True)
    data.to_csv(file_path, index=False)
    # Trả về DataFrame đã cập nhật
    return data

# Hàm xóa dữ liệu trong file csv
def delete(data, patient_id, file_path):
    # Kiểm tra nếu Patient_ID tồn tại trong DataFrame
    if patient_id in data['Patient_ID'].values:
        # Xóa hàng có Patient_ID tương ứng
        data = data[data['Patient_ID'] != patient_id]
        # Ghi lại DataFrame vào file CSV
        data.to_csv(file_path, index=False)
    else:
        messagebox.showerror("Lỗi", "ID không tồn tại trong dữ liệu.")
    
    # Trả về DataFrame đã cập nhật
    return data

# Hàm cập nhật dữ liệu trong file csv
def edit (data, patient_id, updated_values, file_path):
    # Kiểm tra nếu Patient_ID tồn tại trong DataFrame
    if patient_id in data['Patient_ID'].values:
        # Tìm chỉ số của hàng cần chỉnh sửa
        index = data[data['Patient_ID'] == patient_id].index[0]

        # Cập nhật giá trị cho hàng tương ứng
        for field, value in updated_values.items():
            # Kiểm tra kiểu dữ liệu của cột
            if pd.api.types.is_numeric_dtype(data[field]):
                # Chuyển giá trị sang kiểu số (float64)
                data.at[index, field] = pd.to_numeric(value, errors='coerce')
            else:
                # Gán giá trị trực tiếp nếu không phải kiểu số
                data.at[index, field] = value

        # Ghi lại DataFrame vào file CSV
        data.to_csv(file_path, index=False)
    else:
        messagebox.showerror("Lỗi", "ID không tồn tại trong dữ liệu.")
    
    # Trả về DataFrame đã cập nhật
    return data

# Hàm tìm kiếm dữ liệu trong file csv
def search(data, field, value):
    # Kiểm tra nếu trường tìm kiếm tồn tại trong DataFrame
    if field not in data.columns:
        messagebox.showerror("Lỗi", "Trường không tồn tại trong dữ liệu.")

    # Lọc dữ liệu dựa trên giá trị tìm kiếm
    filtered_data = data[data[field].astype(str).str.contains(value, case=False, na=False)]

    return filtered_data

# Hàm sắp xếp dữ liệu trong file csv
def sort_data(data, field, ascending=True):
    if field not in data.columns:
        raise ValueError("Trường không tồn tại trong dữ liệu.")
    return data.sort_values(by=field, ascending=ascending)

# Hàm lọc dữ liệu theo điều kiện logic (>, <, =, >=, <=)
def filter_data(data, field, operator, value):
    if field not in data.columns:
        raise ValueError("Trường không tồn tại trong dữ liệu.")

    # Nếu là cột chuỗi (kiểu object), thực hiện so sánh chuỗi
    if pd.api.types.is_object_dtype(data[field]):
        if operator == "=":
            return data[data[field] == value]
        else:
            raise ValueError("Chỉ hỗ trợ '=' với dữ liệu dạng chuỗi.")
    else:
        try:
            # Chuyển kiểu số nếu có thể
            col_data = pd.to_numeric(data[field], errors='coerce')
            value = float(value)

            if operator == "=":
                return data[col_data == value]
            elif operator == ">":
                return data[col_data > value]
            elif operator == "<":
                return data[col_data < value]
            elif operator == ">=":
                return data[col_data >= value]
            elif operator == "<=":
                return data[col_data <= value]
            else:
                raise ValueError("Toán tử không hợp lệ.")
        except Exception as e:
            raise ValueError(f"Lỗi khi lọc: {e}")
