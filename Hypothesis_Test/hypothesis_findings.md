# Hypothesis Testing Findings Sheet — TV3 — v1 — FINAL — 2026-10-12

### 1. Dữ liệu và Biến số Sử dụng:
- **Tập dữ liệu:** `EDA/cleaned_data/hour_cleaned.csv` ($N = 17,379$ quan sát theo giờ, đã qua tiền xử lý bởi TV1).
- **Biến mục tiêu:** `cnt` (Số lượt thuê xe mỗi giờ, biến đếm).
- **Biến phân nhóm:** 
  - `workingday` (0: Ngày nghỉ / Cuối tuần / Lễ, 1: Ngày làm việc hành chính).
  - `season` (1: Mùa xuân, 2: Mùa hè, 3: Mùa thu, 4: Mùa đông).
- **Cơ sở lý thuyết:** Chuyên khảo *100 Statistical Tests (3rd Edition, 2006)* — Gopal K. Kanji, SAGE Publications.

---

### 2. Phương pháp Thực thi:
- **Quy trình 5 bước Neave-Kanji (2006):** Thiết lập giả thuyết $H_0/H_1$, chọn thống kê kiểm định, xác lập miền bác bỏ, tính toán thống kê kèm $p$-value, ra quyết định kết hợp Effect Size và đánh giá độ bền vững.
- **Kiểm định giả định:** Levene's Test (*Kanji Test 31*, trung vị) kiểm tra tính đồng nhất phương sai; Q-Q plot kiểm tra tính chuẩn.
- **Kiểm định tham số hiệu chỉnh phương sai:** Welch's $t$-test (*Kanji Test 9*), Welch's ANOVA (*Kanji Test 22 adj*), Games-Howell Post-hoc (*Kanji Test 28*).
- **Kiểm định phi tham số đối chứng:** Mann-Whitney $U$ (*Kanji Test 48*), Two-sample Kolmogorov-Smirnov (*Kanji Test 49*), Kruskal-Wallis $H$-test (*Kanji Test 51/54*), Dunn-Bonferroni Post-hoc.
- **Kiểm soát Sai lầm loại 1:** Hiệu chỉnh cỡ mẫu hiệu dụng chuỗi thời gian $N_{\text{eff}} \approx 1,479$ (*Kanji Test 64*) và đối chứng chuỗi tổng hợp cấp ngày ($N = 731$ ngày).

---

### 3. Kết quả Chính (Số liệu và Đơn vị Chuẩn tắc):

#### Câu hỏi Nghiên cứu 1 (RQ1 — Ngày làm việc vs Ngày nghỉ):
- **Thống kê mô tả:**
  - Ngày làm việc ($N_1 = 11,865$): Mean = $193.21$, Median = $151.00$, Std = $185.11$, Skewness = $1.3529$.
  - Ngày nghỉ ($N_0 = 5,514$): Mean = $181.41$, Median = $119.00$, Std = $172.85$, Skewness = $1.0574$.
  - Chênh lệch trung bình: $\Delta = +11.80 \text{ lượt/giờ}$ (Khoảng tin cậy 95% Welch CI: $[6.15, 17.45]$).
- **Kiểm định giả định & Danh nghĩa:**
  - Levene Test (Test 31): $F = 2.7390, p = 0.0979 > 0.05$ (Phương sai tương đối đồng nhất).
  - Welch's $t$-test (Test 9): $t^* = 4.0951, \nu \approx 11,444.68, p = 4.25 \times 10^{-5} < 0.001^{***}$.
  - Mann-Whitney $U$ (Test 48): $U = 33,565,313.0, p = 0.0056^{**}$, Rank-biserial $r = -0.0261$.
  - Two-sample KS-test (Test 49): $D = 0.0748, p = 9.35 \times 10^{-19} < 0.001^{***}$.
- **Kích thước hiệu ứng & Đánh giá độ bền vững:**
  - Cohen's $d = 0.0651 \ll 0.20$ (**Hiệu ứng không đáng kể / Negligible effect**).
  - Hiệu chỉnh cỡ mẫu thực dụng $N_{\text{eff}} \approx 1,479$: $t_{\text{adj}} = 1.1946, p_{\text{adj}} = 0.2323 > 0.05$ (**Mất ý nghĩa thống kê!**).
  - Đối chứng cấp ngày ($N = 731$ ngày): Welch $t = 1.6014, p = 0.1101 > 0.05$; Mann-Whitney $U = 54,699.0, p = 0.1186 > 0.05$ (**Chưa đủ cơ sở bác bỏ $H_0$**).

#### Câu hỏi Nghiên cứu 2 (RQ2 — 4 Mùa trong năm):
- **Thống kê mô tả 4 mùa:**
  - Mùa xuân ($N=4,242$): Mean = $111.11$, Median = $76.00$, Std = $119.22$, Skew = $1.9119$.
  - Mùa hè ($N=4,409$): Mean = $208.34$, Median = $165.00$, Std = $188.36$, Skew = $1.0401$.
  - Mùa thu ($N=4,496$): Mean = $236.02$, Median = $199.00$, Std = $197.71$, Skew = $0.9865$.
  - Mùa đông ($N=4,232$): Mean = $198.87$, Median = $155.50$, Std = $182.97$, Skew = $1.2422$.
- **Kiểm định giả định & Tổng thể (Omnibus):**
  - Levene Test 4 mùa (Test 31): $F = 324.50, p = 5.03 \times 10^{-205} \ll 0.001$ (Phương sai dị biệt cực kỳ nghiêm trọng).
  - Welch's ANOVA (Chính): $F_{\text{Welch}} = 606.73, \nu_1 = 3, \nu_2 = 9,462.11, p < 10^{-300} < 0.001^{***}$.
  - Kruskal-Wallis $H$-test (Test 51/54): $H = 1,190.27, \nu = 3, p < 10^{-250} < 0.001^{***}$.
  - Kích thước hiệu ứng: Eta-squared $\eta^2 = 0.0660$ ($6.60\%$ biến thiên), Epsilon-squared $\epsilon^2 = 0.0683$ (**Hiệu ứng mức độ Trung bình / Medium effect size**). Hiệu chỉnh $N_{\text{eff}}$: $F_{\text{adj}} \approx 51.64, p < 10^{-25}$ (Bền vững tuyệt đối).
- **Kiểm định Hậu nghiệm Song hành (Games-Howell Test 28 & Dunn-Bonferroni):**
  - 5/6 cặp mùa khác biệt cực kỳ mạnh mẽ ($p < 0.001^{***}$).
  - **Ngoại lệ phản trực giác:** Cặp **Mùa hè vs Mùa đông** có $\Delta = +9.48 \text{ lượt/h}$, $95\% \text{ CI} = [-0.79, +19.74]$ chứa 0, $p_{\text{Games-Howell}} = 0.0826 > 0.05$ (ns); Dunn-Bonferroni $p_{\text{adj}} = 0.4339 > 0.05$. **Chưa đủ bằng chứng thống kê để khẳng định có sự khác biệt nhu cầu giữa Mùa hè và Mùa đông!**

---

### 4. Quyết định Đã Đưa Ra và Lý do:
1. **Bác bỏ kết luận vội vã dựa trên $p$-value danh nghĩa ở RQ1:** Sự chênh lệch $11.80$ lượt/h đạt ý nghĩa thống kê danh nghĩa thuần túy do cỡ mẫu lớn. Khi kiểm soát tự tương quan và kích thước hiệu ứng, tổng nhu cầu 24h là tương đương. Nghịch lý nằm ở cấu trúc nhịp giờ: Ngày làm việc 2 đỉnh nhọn (8h, 17h) bù trừ cho đỉnh chuông đơn giữa trưa (12h-15h) của ngày nghỉ.
2. **Loại bỏ One-way ANOVA và Tukey HSD cổ điển ở RQ2:** Do phương sai dị biệt cực đoan ($F_{\text{Levene}} = 324.50$), bắt buộc phải sử dụng Welch's ANOVA và Games-Howell Post-hoc để bảo vệ tính chính xác của mức ý nghĩa $\alpha = 0.05$.
3. **Xác nhận hiện tượng tương đương nhu cầu giữa Mùa hè và Mùa đông:** Do nhiệt độ mùa hè D.C. quá nóng ẩm gây ức chế đạp xe, trong khi mùa đông duy trì ổn định nhóm khách đi làm định kỳ.

---

### 5. Khuyến nghị Kỹ thuật Bắt buộc cho Downstream:

#### A. Đối với TV4 (Phần 4: Tương quan & Phần 5: Lý thuyết, Định hướng Mô hình Hồi quy):
- **Phân tích Tương quan (Phần 4):**
  - Nhận xét rõ giới hạn của hệ số tương quan tuyến tính Pearson khi quan hệ giữa giờ (`hr`) và lượt thuê (`cnt`) mang tính chu kỳ hai đỉnh.
  - Ưu tiên sử dụng hệ số tương quan hạng Spearman cho các biến điều kiện thời tiết (`temp`, `hum`, `windspeed`) để phát hiện các mối quan hệ phi tuyến đơn điệu.
- **Lý thuyết & Định hướng Bài toán Hồi quy (Phần 5):**
  - **Biến mục tiêu:** Nêu rõ cơ sở lựa chọn biến đổi $\log(1 + \text{cnt})$ nhằm ổn định phương sai trước sự vi phạm tính chuẩn và phương sai dị biệt nặng nề được chứng minh ở Chương 3.
  - **Lập Feature Candidate Sheet chuyển giao cho TV5:** Đề xuất đưa biến tương tác giữa `workingday` và `hr` vào danh sách ứng viên; chọn Mùa xuân làm nhóm cơ sở (`reference category`) khi mã hóa mùa vụ; lý giải cơ sở loại trừ `atemp` để chống đa cộng tuyến.

#### B. Đối với TV5 (Phần 6: Xây dựng và Đánh giá Mô hình Hồi quy Thực chiến):
- **Kỹ thuật Tạo Đặc trưng (Feature Engineering - Mục 6.1):**
  - **Bắt buộc đưa biến tương tác loại ngày và giờ vào mô hình:** Kết hợp các hàm điều hòa lượng giác Fourier ($sin, cos$) với `workingday` (tích các hài giờ với `workingday`: `hr_sin1×workingday` ... `hr_cos5×workingday` như TV5 đã thực hiện) để mô hình tái hiện trọn vẹn 2 đỉnh giờ đi làm và 1 đỉnh giờ nghỉ.
  - **Mã hóa chu kỳ mùa vụ / tháng:** Sử dụng các hàm điều hòa tháng (`mnth_sin`, `mnth_cos`) hoặc biến giả mùa để nắm bắt đỉnh Mùa thu ($236.02$) và đáy Mùa xuân ($111.11$).
- **Đánh giá và Kiểm tra Giả định Mô hình (Assumptions Check - Mục 6.4):**
  - **Tính độc lập phần dư:** Kết quả kiểm định tự tương quan $r_1 = 0.8431$ ở Chương 3 dự báo trước hiện tượng thống kê Durbin-Watson rơi xuống mức thấp ($DW \approx 0.68 < 1.5$); TV5 cần lưu ý điểm này khi đánh giá giả định phần dư độc lập.
  - **Chiến lược chia dữ liệu (Chronological Split):** Áp dụng điểm cắt theo thời gian (cắt ngày 31/03/2012) thay vì chia ngẫu nhiên để đánh giá năng lực ngoại suy xu hướng thực tế, tránh rò rỉ thông tin chuỗi thời gian giữa các giờ liền kề.

---

### 6. Danh mục Tài liệu và File Liên quan:
- **Tài liệu Báo cáo đầy đủ:** `Hypothesis_Test/report.md` (Chương 3 hoàn chỉnh từ 3.1 đến 3.4).
- **Jupyter Notebook thực thi:** `Hypothesis_Test/03_hypothesis_testing.ipynb` (Chạy sạch, nhúng output tables & figures).
- **Mã nguồn tính toán độc lập:** `Hypothesis_Test/03_hypothesis_testing.py`.
- **Tài sản Biểu đồ ấn phẩm (300 DPI):**
  - `Hypothesis_Test/assets/fig_3_1_workingday_assumptions.png` (Kiểm tra giả định RQ1).
  - `Hypothesis_Test/assets/fig_3_2_season_posthoc_forest.png` (Forest plot kiểm định hậu nghiệm RQ2).
