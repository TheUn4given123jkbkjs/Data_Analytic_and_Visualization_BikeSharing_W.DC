# Distribution Findings Sheet - TV2 - v1 - DRAFT

1. **Dữ liệu/biến đã dùng:** `EDA/cleaned_data/hour_cleaned.csv`; `cnt`, `temp`, `hum`; phân nhóm `cnt` theo `workingday`.
2. **Phương pháp:** thống kê mô tả, histogram/KDE, ECDF, Q-Q plot; fit empirical, Poisson, Negative Binomial, Normal, Log-normal và Beta; so sánh AIC/BIC và goodness-of-fit có cảnh báo mẫu lớn.
3. **Kết quả chính:**
   - `cnt`: n = 17,379; mean = 189.46; median = 142.00; skewness = 1.2774; variance/mean = 173.66. Phân phối lệch phải và over-dispersion mạnh.
   - Fit `cnt`: Negative Binomial có AIC = 217,615.076, thấp hơn Poisson = 3,002,494.202; Log-normal = 220,758.045; Normal = 230,086.178.
   - `temp`: skewness = -0.0060; Beta có AIC = -9,102.191, thấp hơn Normal = -7,936.739.
   - `hum`: skewness = -0.0828; Normal có AIC = -8,096.975, thấp hơn Beta = -7,361.881.
   - Theo `workingday`: ngày nghỉ mean = 181.41, median = 119; ngày làm việc mean = 193.21, median = 151.
4. **Quyết định:** không dùng Poisson đơn giản làm mô hình đại diện cho `cnt`; ưu tiên Negative Binomial khi cần mô tả biến đếm có over-dispersion. Chưa chốt biến đổi `cnt` cho hồi quy/mô hình; `log1p` không đưa `cnt` về Normal theo kết quả EDA.
5. **Downstream cần lưu ý:**
   - TV3 (V-05): phân phối `cnt`, mức lệch và lý do cần cân nhắc test phi tham số.
   - TV4 (V-06): cơ sở lựa chọn Pearson/Spearman.
   - TV5 (V-07): có nên biến đổi `cnt`; nếu biến đổi phải đánh giá lại trên thang gốc.
6. **File liên quan:** `02_distribution.ipynb`, `report.md`, `README.md`.
