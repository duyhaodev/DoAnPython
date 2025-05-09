import tkinter as tk
import matplotlib.pyplot as plt
import pandas as pd

def display_graph_window(data):
    # Tạo cửa sổ mới
    graph_window = tk.Toplevel()
    graph_window.title("Cancer Data Visualizations")
    graph_window.geometry("400x300")

    # Hàm hiển thị biểu đồ phân bố độ tuổi
    def plot_age_distribution():
        plt.figure(figsize=(8, 6))
        plt.hist(data['Age'], bins=30, color='skyblue', edgecolor='black')
        plt.title('Age Distribution of Cancer Patients')
        plt.xlabel('Age')
        plt.ylabel('Frequency')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    # Hàm hiển thị biểu đồ phân bố giới tính
    def plot_gender_distribution():
        gender_counts = data['Gender'].value_counts()
        plt.figure(figsize=(8, 6))
        plt.pie(
            gender_counts,
            labels=gender_counts.index,
            autopct='%1.1f%%',
            colors=['lightblue', 'salmon', 'lightgreen'],
            startangle=90
        )
        plt.title('Gender Distribution of Cancer Patients')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    # Hàm hiển thị biểu đồ bệnh nhân theo quốc gia
    def plot_country_distribution():
        country_counts = data['Country_Region'].value_counts()
        plt.figure(figsize=(10, 6))
        country_counts.plot(kind='bar', color='lightcoral')
        plt.title('Cancer Patients by Country/Region')
        plt.xlabel('Country/Region')
        plt.ylabel('Number of Patients')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, axis='y', alpha=0.3)
        plt.tight_layout()
        plt.show()

    # Hàm hiển thị biểu đồ phân bố loại ung thư
    def plot_cancer_type_distribution():
        cancer_type_counts = data['Cancer_Type'].value_counts()
        plt.figure(figsize=(8, 6))
        cancer_type_counts.plot(kind='bar', color='lightyellow')
        plt.title('Distribution of Cancer Types')
        plt.xlabel('Cancer Type')
        plt.ylabel('Number of Patients')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, axis='y', alpha=0.3)
        plt.tight_layout()
        plt.show()

    # Hàm hiển thị biểu đồ phân bố giai đoạn ung thư
    def plot_cancer_stage_distribution():
        stage_counts = data['Cancer_Stage'].value_counts()
        plt.figure(figsize=(8, 6))
        stage_counts.plot(kind='bar', color='lavender')
        plt.title('Distribution of Cancer Stages')
        plt.xlabel('Cancer Stage')
        plt.ylabel('Number of Patients')
        plt.grid(True, axis='y', alpha=0.3)
        plt.tight_layout()
        plt.show()

    # Tạo các nút với màu sắc khác nhau
    btn_age = tk.Button(
        graph_window,
        text="Age Distribution",
        command=plot_age_distribution,
        width=30,
        bg='lightblue',
        activebackground='skyblue'
    )
    btn_age.pack(pady=10)

    btn_gender = tk.Button(
        graph_window,
        text="Gender Distribution",
        command=plot_gender_distribution,
        width=30,
        bg='lightgreen',
        activebackground='limegreen'
    )
    btn_gender.pack(pady=10)

    btn_country = tk.Button(
        graph_window,
        text="Patients by Country",
        command=plot_country_distribution,
        width=30,
        bg='lightcoral',
        activebackground='coral'
    )
    btn_country.pack(pady=10)

    btn_cancer_type = tk.Button(
        graph_window,
        text="Cancer Type Distribution",
        command=plot_cancer_type_distribution,
        width=30,
        bg='lightyellow',
        activebackground='yellow'
    )
    btn_cancer_type.pack(pady=10)

    btn_cancer_stage = tk.Button(
        graph_window,
        text="Cancer Stage Distribution",
        command=plot_cancer_stage_distribution,
        width=30,
        bg='lavender',
        activebackground='plum'
    )
    btn_cancer_stage.pack(pady=10)