import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from .CRUD import create, delete, edit, search
from .displayGraph import display_graph_window

#Hàm tạo giao diện
def create_display_window(data, rows_per_page=10):
    #Tạo cửa sổ chính
    root = tk.Tk()
    root.title("Dataset Viewer")

    #Tạo treeview
    tree = ttk.Treeview(root, columns=list(data.columns), show='headings')

    #Khai báo độ dài các cột
    column_widths = {
            "Patient_ID": 80,
            "Age": 50,
            "Gender": 60,
            "Country_Region": 120,
            "Year": 50,
            "Genetic_Risk": 100,
            "Air_Pollution": 100,
            "Alcohol_Use": 100,
            "Smoking": 100,
            "Obesity_Level": 100,
            "Treatment_Cost_USD": 120,
            "Survival_Years": 100,
            "Target_Severity_Score": 120,
            "Cancer_Type": 100,
            "Cancer_Stage": 100
        }
    
    # Đặt tiêu đề và độ rộng cho các cột
    for col in data.columns:
            tree.heading(col, text=col)
            tree.column(col, width=column_widths.get(col, 100), anchor=tk.CENTER)
        
    #thêm dữ liệu vào treeview
    for _, row in data.iterrows():
        tree.insert("", tk.END, values=list(row))

    # Đặt Treeview vào cửa sổ
    tree.pack(fill=tk.BOTH, expand=True)

    # -- Phân trang --
    # Biến lưu trạng thái phân trang
    current_page = tk.IntVar(value=1)
    total_pages = (len(data) + rows_per_page - 1) // rows_per_page

    # Hàm load trang
    def load_page(page):
        # Xóa dữ liệu cũ
        tree.delete(*tree.get_children())

        # Tính toán chỉ số bắt đầu và kết thúc
        start_idx = (page - 1) * rows_per_page
        end_idx = min(start_idx + rows_per_page, len(data))

        # Thêm dữ liệu vào Treeview
        for _, row in data.iloc[start_idx:end_idx].iterrows():
            tree.insert("", tk.END, values=list(row))

        # Cập nhật số trang hiện tại
        current_page.set(page)
        page_label.config(text=f"Page {page} of {total_pages}")

    # Nút chuyển trang
    def next_page():
        if current_page.get() < total_pages:
            load_page(current_page.get() + 1)

    def prev_page():
        if current_page.get() > 1:
            load_page(current_page.get() - 1)

    def first_page():
        load_page(1)
    
    def last_page():
        load_page(total_pages)

    # Nút điều khiển phân trang
    control_frame = tk.Frame(root)
    control_frame.pack(fill=tk.X)

    first_button = tk.Button(control_frame, text="First", command=first_page)
    first_button.pack(side=tk.LEFT, padx=5, pady=5)

    prev_button = tk.Button(control_frame, text="Previous", command=prev_page)
    prev_button.pack(side=tk.LEFT, padx=5, pady=5)

    page_label = tk.Label(control_frame, text=f"Page 1 of {total_pages}")
    page_label.pack(side=tk.LEFT, padx=5)

    next_button = tk.Button(control_frame, text="Next", command=next_page)
    next_button.pack(side=tk.LEFT, padx=5, pady=5)

    last_button = tk.Button(control_frame, text="Last", command=last_page)
    last_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Tải trang đầu tiên
    load_page(1)
    # --Kết phúc phân trang--

    # -- Tạo container chứa CRUD và tìm kiếm --
    form_container = tk.Frame(root)
    form_container.pack(fill=tk.BOTH, expand=True)
    # -- Kết thúc container --  

    # -- Tạo Label và Entry cho CRUD --
    # Label và text box cho CRUD
    label_frame = tk.Frame(form_container)
    label_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Danh sách các trường cần nhập
    fields = [
    "Patient_ID", "Age", "Gender", "Country_Region", "Year", "Genetic_Risk",
    "Air_Pollution", "Alcohol_Use", "Smoking", "Obesity_Level", "Cancer_Type",
    "Cancer_Stage", "Treatment_Cost_USD", "Survival_Years", "Target_Severity_Score"
    ]

    entries = {}

    # Tạo các Label và Entry
    for field in fields:
        row_frame = tk.Frame(label_frame)
        row_frame.pack(fill=tk.X, pady=5)

        label = tk.Label(row_frame, text=field, width=20, anchor="w")
        label.pack(side=tk.LEFT, padx=5)

        entry = tk.Entry(row_frame, width=30)
        entry.pack(side=tk.LEFT, padx=5)

        # Lưu Entry vào dictionary
        entries[field] = entry
    # -- Kết thúc Label và Entry cho CRUD --

    # -- Tìm kiếm --
    # Tạo Frame chứa Treeview cho tìm kiếm
    search_frame = tk.Frame(form_container)
    search_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)

    # Tạo Treeview trong search_frame
    search_tree = ttk.Treeview(search_frame, columns=list(data.columns), show='headings')

    # Đặt tiêu đề và độ rộng cho các cột trong Treeview tìm kiếm
    for col in data.columns:
        search_tree.heading(col, text=col)
        search_tree.column(col, width=100, anchor=tk.CENTER)

    # Đặt Treeview vào search_frame
    search_tree.pack(fill=tk.BOTH, expand=True)
    # -- Kết thúc Treeview tìm kiếm --

    # -- Các hàm xử lý --
    # Ham xử lý khi nhấn nút Create
    def handle_create():
        nonlocal data

        # Lấy giá trị từ các Entry
        new_entry = {field: entry.get() for field, entry in entries.items()}

        data = create(data, new_entry, 'data/global_cancer_patients_2015_2024.csv')

        load_page(current_page.get())

    # Hàm xử lý khi nhấn nút Delete
    def handle_delete():
        nonlocal data

        # Lấy giá trị từ ô Patient_ID
        patient_id = entries["Patient_ID"].get()

        # Kiểm tra nếu Patient_ID không được nhập
        if not patient_id:
            messagebox.showerror("Cảnh báo", "Chưa chọn đối tượng để xóa")
            return

        # Gọi hàm delete để xóa dữ liệu
        data = delete(data, patient_id, 'data/global_cancer_patients_2015_2024.csv')

        # Cập nhật Treeview để hiển thị dữ liệu mới
        load_page(current_page.get())

    def handle_edit():
        nonlocal data

        # Lấy giá trị từ ô Patient_ID
        patient_id = entries["Patient_ID"].get()

        # Kiểm tra nếu Patient_ID không được nhập
        if not patient_id:
            messagebox.showerror("Cảnh báo", "Chưa chọn đối tượng để chỉnh sửa")
            return

        # Lấy giá trị từ các Entry
        updated_values = {field: entry.get() for field, entry in entries.items()}

        # Gọi hàm edit để cập nhật dữ liệu
        data = edit(data, patient_id, updated_values, 'data/global_cancer_patients_2015_2024.csv')

        # Cập nhật Treeview để hiển thị dữ liệu mới
        load_page(current_page.get())

    def handle_search():
        # Lấy giá trị từ Combobox và Entry
        search_field = search_combobox.get()
        search_value = search_entry.get()

        # Kiểm tra nếu chưa chọn trường hoặc chưa nhập giá trị
        if search_field == "Chọn trường" or not search_value:
            messagebox.showerror("Lỗi", "Vui lòng chọn trường và nhập giá trị tìm kiếm.")
            return

        # Gọi hàm search để tìm kiếm dữ liệu
        try:
            search_results = search(data, search_field, search_value)

            # Xóa dữ liệu cũ trong Treeview tìm kiếm
            search_tree.delete(*search_tree.get_children())

            # Thêm kết quả tìm kiếm vào Treeview
            for _, row in search_results.iterrows():
                search_tree.insert("", tk.END, values=list(row))
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))

    # Thao tác CRUD và search
    # Tạo Frame chứa các nút CRUD
    crud_search_frame = tk.Frame(root)
    crud_search_frame.pack(fill=tk.X)

    # Tạo các nút CRUD
    create_button = tk.Button(crud_search_frame, text="Create", command=handle_create)
    create_button.pack(side=tk.LEFT, padx=5, pady=5)

    edit_button = tk.Button(crud_search_frame, text="Edit", command=handle_edit)
    edit_button.pack(side=tk.LEFT, padx=5, pady=5)

    delete_button = tk.Button(crud_search_frame, text="Delete", command=handle_delete)
    delete_button.pack(side=tk.LEFT, padx=5, pady=5)
    
    # Tạo nút "Xem biểu đồ"
    graph_button = tk.Button(crud_search_frame, text="Xem biểu đồ", command=lambda: display_graph_window(data))
    graph_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Tạo các nút search
    search_controls_frame = tk.Frame(crud_search_frame)
    search_controls_frame.pack(side=tk.RIGHT, padx=10, pady=10)

    # Label "Tìm kiếm"
    search_label = tk.Label(search_controls_frame, text="Tìm kiếm")
    search_label.pack(side=tk.LEFT, padx=5)

    # Combobox chứa các trường tìm kiếm
    search_fields = [
        "Patient_ID", "Age", "Gender", "Country_Region", "Year", "Genetic_Risk",
        "Air_Pollution", "Alcohol_Use", "Smoking", "Obesity_Level", "Cancer_Type",
        "Cancer_Stage", "Treatment_Cost_USD", "Survival_Years", "Target_Severity_Score"
    ]
    search_combobox = ttk.Combobox(search_controls_frame, values=search_fields, state="readonly", width=20)
    search_combobox.set("Chọn trường")  # Giá trị mặc định
    search_combobox.pack(side=tk.LEFT, padx=5)

    # Entry để nhập giá trị cần tìm kiếm
    search_entry = tk.Entry(search_controls_frame, width=30)
    search_entry.pack(side=tk.LEFT, padx=5)

    # Nút "Tìm kiếm"
    search_button = tk.Button(search_controls_frame, text="Tìm kiếm", command=handle_search)
    search_button.pack(side=tk.LEFT, padx=5)

    
    # Hàm xử lý khi double-click vào một item trong Treeview
    def on_treeview_double_click(event):
        # Lấy item được chọn
        selected_item = tree.selection()
        if selected_item:
            # Lấy giá trị của item được chọn
            item_values = tree.item(selected_item, 'values')

            # Gán giá trị vào các Entry
            for i, field in enumerate(fields):
                entries[field].delete(0, tk.END)  # Xóa nội dung cũ
                entries[field].insert(0, item_values[i])  # Gán giá trị mới

    # Kết nối sự kiện double-click với Treeview
    tree.bind("<Double-1>", on_treeview_double_click)

    
    # Chạy vòng lặp chính của tkinter
    root.mainloop()
    

    
