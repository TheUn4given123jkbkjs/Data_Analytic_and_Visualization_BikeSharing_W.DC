# Module Kiểm định giả thuyết (Hypothesis Testing) — Thành viên 3 (TV3)

Thư mục này chứa toàn bộ mã nguồn, dữ liệu thực nghiệm, biểu đồ và báo cáo chi tiết cho **Phần 3: Kiểm định giả thuyết** trong đề tài phân tích dữ liệu Bike Sharing Dataset.

---

## 1. Cấu trúc thư mục
* `PLAN.md`: Bản kế hoạch chi tiết, tiêu chuẩn thực hiện và các bước triển khai.
* `03_hypothesis_testing.ipynb`: Jupyter Notebook hoàn chỉnh từ nạp dữ liệu, kiểm tra giả định, thực thi kiểm định tham số và phi tham số, tính effect size và trực quan hóa.
* `report.md`: Báo cáo chi tiết Phần 3 (sẵn sàng tích hợp vào báo cáo tổng thể).
* `hypothesis_findings.md`: Findings Sheet bàn giao thông tin cho các thành viên khác theo mẫu `HANDOFF.md`.
* `requirements.txt`: Danh sách các thư viện cần thiết.
* `assets/`: Thư mục chứa các biểu đồ xuất bản chất lượng cao (PNG 300 DPI).

---

## 2. Hướng dẫn chạy
1. Đảm bảo dữ liệu đã được làm sạch tại `../EDA/cleaned_data/hour_cleaned.csv` (17,379 dòng).
2. Cài đặt các thư viện cần thiết (nếu chưa có):
   ```bash
   pip install -r requirements.txt
   ```
3. Mở và chạy toàn bộ các ô trong `03_hypothesis_testing.ipynb`.

---

## 3. Quy chuẩn tuân thủ
* Tuân thủ các nguyên tắc tại `../rules.md` và `../outline.md`.
* Luôn kiểm tra giả định phân phối, phương sai trước khi chạy kiểm định.
* Kết hợp kiểm định tham số (t-test, ANOVA) và phi tham số (Mann-Whitney U, Kruskal-Wallis) do `cnt` lệch phải và có over-dispersion.
* Luôn tính toán và báo cáo độ lớn hiệu ứng (Effect Size) cùng các khoảng tin cậy.
* Luôn nêu rõ các hạn chế về tự tương quan thời gian ($r_1 \approx 0.8431$) và cỡ mẫu lớn $N = 17,379$.
