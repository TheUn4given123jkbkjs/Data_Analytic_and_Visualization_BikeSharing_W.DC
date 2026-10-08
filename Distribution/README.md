# Distribution - TV2

Thư mục này chứa Phần 2 - Phân tích phân phối xác suất.

## Chạy notebook

Mở `02_distribution.ipynb` trong VS Code, chọn Python kernel có `pandas`, `numpy`, `scipy`, `matplotlib`, `seaborn` và chạy `Restart Kernel -> Run All`.

Notebook đọc dữ liệu đã xử lý từ `../EDA/cleaned_data/hour_cleaned.csv`. File có cột index dư thừa ở đầu, notebook sẽ tự động loại cột này khi đọc. Dataset gốc `../data/hour.csv` không bị thay đổi.

## Đầu ra

- `02_distribution.ipynb`: phân tích và hình/bảng.
- `report.md`: nội dung Phần 2 dạng Markdown.
- `distribution_findings.md`: bàn giao cho các thành viên downstream.

## Lưu ý

`cnt` là biến đếm lệch phải và có over-dispersion. P-value goodness-of-fit trên mẫu lớn chỉ là một bằng chứng phụ, không được dùng đơn độc để chọn phân phối. Các quan sát theo giờ có tự tương quan, nên kết luận là mô tả trên mẫu dữ liệu hiện có.
