# Plan - Phân tích phân phối xác suất (TV2)

## Mục tiêu

Xác định đặc điểm phân phối của `cnt`, `temp` và `hum`, sau đó so sánh với các phân phối lý thuyết phù hợp. Kết quả được trình bày bằng notebook và bàn giao cho TV3, TV4, TV5.

## Phạm vi đã chốt

- Dữ liệu chính: `../EDA/cleaned_data/hour_cleaned.csv`.
- Không sửa `../data/hour.csv`.
- Biến chính: `cnt`, `temp`, `hum`.
- Thêm so sánh phân phối `cnt` theo `workingday`.
- `cnt`: empirical, Poisson, Negative Binomial, Normal và Log-normal.
- `temp`, `hum`: Normal và Beta.
- Đánh giá bằng histogram/KDE, ECDF, Q-Q plot, thống kê mô tả, AIC/BIC và KS/chi-square khi phù hợp.
- Viết bằng tiếng Việt, giữ thuật ngữ English trong ngoặc.
- Không diễn giải tên `season` nếu không cần, do tài liệu đang có mâu thuẫn mã.

## Cấu trúc đầu ra

- `02_distribution.ipynb`: notebook chạy độc lập, Markdown -> code -> output -> nhận xét.
- `report.md`: nội dung Phần 2 để TV3 tham khảo khi gộp báo cáo.
- `distribution_findings.md`: Findings Sheet theo mẫu `HANDOFF.md`.
- `README.md`: cách chạy, dependency và phạm vi.

## Các bước thực hiện

1. Đọc dữ liệu, loại cột index dư thừa, chuyển `dteday` sang datetime và kiểm tra chất lượng.
2. Tạo bảng thống kê mô tả cho ba biến.
3. Phân tích empirical distribution của `cnt` bằng histogram/KDE, ECDF và boxplot.
4. Fit và so sánh Poisson, Negative Binomial, Normal và Log-normal cho `cnt`.
5. Fit và so sánh Normal và Beta cho `temp`, `hum`.
6. So sánh `cnt` giữa hai nhóm `workingday` bằng thống kê và biểu đồ mô tả.
7. Viết nhận xét theo logic Quan sát -> Bằng chứng -> Ý nghĩa.
8. Viết kết luận và hạn chế của Phần 2.
9. Tạo Findings Sheet với kết quả số liệu và lưu ý downstream.
10. Chạy notebook từ đầu đến cuối trong kernel mới.

## Tiêu chí kiểm tra

- Sau khi đọc dữ liệu có 17,379 dòng và các biến phân tích đúng.
- Kết quả gần với EDA: `cnt` mean khoảng 189.46, median khoảng 142, skewness khoảng 1.28, variance/mean khoảng 173.66.
- Tất cả tham số fit hợp lệ; AIC/BIC không tính trên giá trị lỗi.
- Biểu đồ có tiêu đề, nhãn trục, đơn vị và đánh số `Hình 2.x`; bảng đánh số `Bảng 2.x`.
- Không kết luận phân phối chỉ dựa trên p-value; phải ghi rõ ảnh hưởng của cỡ mẫu lớn và tự tương quan theo giờ.
- Findings Sheet có dữ liệu, phương pháp, kết quả, quyết định và lưu ý cho V-05, V-06, V-07.

## Phạm vi không làm

- Không làm hypothesis testing của TV3.
- Không làm correlation, MLR hoặc mô hình dự báo.
- Không sửa dataset gốc, EDA report hay HANDOFF của thành viên khác.
- Không dùng `day.csv` cho phân tích chính.
