# Kế hoạch thực hiện: Phần 3 - Kiểm định giả thuyết (Hypothesis Testing) — TV3

## 1. Mục tiêu
Thực hiện toàn diện **Phần 3: Kiểm định giả thuyết** cho đồ án Bike Sharing Dataset (`hour_cleaned.csv` từ EDA), tuân thủ chặt chẽ `outline.md` và `rules.md`. Đồng thời chuẩn bị sẵn cấu trúc tài liệu, code và kết quả để tích hợp vào báo cáo chung.

---

## 2. Các yêu cầu & Tiêu chí tuân thủ (theo `rules.md` và `outline.md`)
1. **Logic phân tích:** Mục tiêu → Phương pháp → Kết quả → Nhận xét (Quan sát → Bằng chứng → Ý nghĩa).
2. **Quy chuẩn số liệu:** Dấu `.` cho số thập phân; p-value, hệ số lấy 4 chữ số thập phân (`p < 0.001` nếu rất nhỏ); mean, std, statistic lấy 2 chữ số thập phân; luôn ghi kèm đơn vị (lượt thuê).
3. **Quy chuẩn kiểm định:**
   - Không chọn test trước rồi gán câu hỏi; chọn câu hỏi nghiên cứu thực tế với Bike Sharing.
   - Bắt buộc kiểm tra các giả định thống kê (Normality: Shapiro-Wilk / D'Agostino / Q-Q plot; Homoscedasticity: Levene's test).
   - Với mẫu lớn ($N = 17,379$) và dữ liệu `cnt` lệch phải (over-dispersion theo kết quả TV2), thực hiện **song song kiểm định tham số và phi tham số tương ứng** (ví dụ Welch's t-test vs Mann-Whitney U; ANOVA vs Kruskal-Wallis).
   - **Bắt buộc báo cáo Effect Size** (Cohen's d, Rank-Biserial Correlation, Eta-squared $\eta^2$, Epsilon-squared $\epsilon^2$, Cramér's V) và phân tích ý nghĩa thực tiễn.
   - Diễn giải kết quả chuẩn: "Có bằng chứng thống kê..." hoặc "Chưa đủ bằng chứng thống kê để bác bỏ giả thuyết không", tuyệt đối **không** viết "Chấp nhận $H_0$".
   - Bàn giao và phân tích rõ các hạn chế: Tự tương quan chuỗi thời gian ($r_1 \approx 0.8431$), các quan sát không hoàn toàn IID, ảnh hưởng của cỡ mẫu lớn lên p-value.
4. **Đối chiếu VALIDATE:**
   - **V-03 (EDA):** `weathersit = 4` chỉ có 3 dòng (đã xử lý/gộp hoặc lưu ý mẫu nhỏ), `hum = 0` 22 dòng đã sửa, 17,379 dòng.
   - **V-05 (Distribution):** `cnt` lệch phải (skewness 1.28), vi phạm giả định chuẩn nghiêm trọng -> bắt buộc kiểm định phi tham số hỗ trợ.
   - **V-08 (Correlation/TV4):** Không chọn câu hỏi trùng lặp trực tiếp với các cặp biến hồi quy/tương quan trọng tâm của TV4.

---

## 3. Lựa chọn 2 Câu hỏi nghiên cứu (Research Questions)

### 📌 Research Question 1 (RQ1) — So sánh 2 nhóm độc lập:
* **Câu hỏi:** *Có sự khác biệt có ý nghĩa thống kê về số lượng thuê xe trung bình mỗi giờ (`cnt`) giữa ngày làm việc (`workingday = 1`) và ngày nghỉ/cuối tuần/lễ (`workingday = 0`) hay không?*
* **Biến số:** Biến phụ thuộc `cnt` (định lượng), Biến độc lập `workingday` (nhị phân: 0 vs 1).
* **Giả thuyết:**
  - $H_0: \mu_{\text{workingday}} = \mu_{\text{non-workingday}}$ (Không có sự khác biệt về số lượng thuê xe trung bình mỗi giờ).
  - $H_1: \mu_{\text{workingday}} \neq \mu_{\text{non-workingday}}$.
* **Kiểm định thực hiện:**
  - Kiểm tra giả định: Levene test (phương sai), Q-Q plot / Skewness.
  - Kiểm định tham số: Independent Samples t-test (Welch's t-test do phương sai không đồng nhất).
  - Kiểm định phi tham số: Mann-Whitney U test (so sánh phân bố/trung vị do `cnt` lệch phải).
  - Effect Size: Cohen's d và Rank-Biserial Correlation ($r$).
  - Phân tích thêm góc nhìn phân tầng theo giờ (đỉnh 8h/17h ở ngày làm việc vs đỉnh 12h-16h ở ngày nghỉ) để giải thích bản chất thực tiễn.

### 📌 Research Question 2 (RQ2) — So sánh nhiều nhóm độc lập:
* **Câu hỏi:** *Số lượng thuê xe trung bình mỗi giờ (`cnt`) có khác biệt có ý nghĩa thống kê giữa các mùa trong năm (`season`: Xuân, Hạ, Thu, Đông) hay không?*
* **Biến số:** Biến phụ thuộc `cnt` (định lượng), Biến độc lập `season` (4 nhóm).
* **Giả thuyết:**
  - $H_0: \mu_1 = \mu_2 = \mu_3 = \mu_4$ (Lượng thuê xe trung bình mỗi giờ giữa 4 mùa là như nhau).
  - $H_1:$ Tồn tại ít nhất một cặp mùa có lượng thuê xe trung bình khác nhau.
* **Kiểm định thực hiện:**
  - Kiểm tra giả định: Levene test, đánh giá phương sai giữa các nhóm mùa.
  - Kiểm định tham số: One-Way ANOVA (và Welch's ANOVA).
  - Kiểm định phi tham số: Kruskal-Wallis H-test.
  - Post-hoc Analysis: Tukey's HSD test & Dunn's test with Bonferroni correction (đối chiếu từng cặp mùa).
  - Effect Size: Eta-squared ($\eta^2$), Omega-squared ($\omega^2$), Epsilon-squared ($\epsilon^2$).

*(Lưu ý: Bổ sung thêm phân tích Chi-square test độc lập giữa `weathersit` và `season` ở phần mở rộng để hoàn thiện đầy đủ lý thuyết 3 phương pháp t-test, ANOVA, Chi-square theo Outline 3.1).*

---

## 4. Cấu trúc thư mục & File đầu ra dự kiến trong `Hypothesis_Test/`
```text
Hypothesis_Test/
├── PLAN.md                     # Kế hoạch chi tiết của TV3 (file này)
├── README.md                   # Hướng dẫn chạy code, môi trường, tóm tắt nội dung
├── requirements.txt            # Thư viện sử dụng
├── 03_hypothesis_testing.ipynb # Jupyter Notebook thực thi toàn bộ tính toán, biểu đồ, bảng biểu
├── hypothesis_findings.md      # Findings Sheet bàn giao theo quy chuẩn HANDOFF.md
├── report.md                   # Toàn bộ nội dung báo cáo Phần 3 hoàn chỉnh (sẵn sàng để gộp)
└── assets/                     # Lưu trữ toàn bộ hình ảnh biểu đồ định dạng PNG (Hình 3.x)
    ├── fig_3_1_workingday_assumptions.png
    ├── fig_3_2_workingday_cnt_distribution.png
    ├── fig_3_3_workingday_hourly_pattern.png
    ├── fig_3_4_season_cnt_distributions.png
    ├── fig_3_5_season_posthoc_diffs.png
    └── fig_3_6_weather_season_contingency.png
```

---

## 5. Lộ trình thực hiện từng bước
1. **Khởi tạo thư mục và cấu trúc dự án:** Tạo thư mục `Hypothesis_Test/assets/`, `requirements.txt`, `README.md`.
2. **Viết Code thực thi (`03_hypothesis_testing.ipynb` & script Python kiểm tra):**
   - Đọc dữ liệu từ `EDA/cleaned_data/hour_cleaned.csv`.
   - Viết các hàm tính toán thống kê chi tiết: Descriptives, Levene, Welch t-test, Mann-Whitney U, Cohen's d, Welch ANOVA, Kruskal-Wallis, Tukey HSD, Dunn test, Chi-square test, Cramér's V.
   - Xuất các biểu đồ đạt chuẩn (`dpi=300`, nhãn, chú thích, rõ ràng).
3. **Soạn thảo tài liệu báo cáo `report.md`:**
   - 3.1. Lý thuyết các phương pháp kiểm định (t-test, ANOVA, Chi-square; tham số vs phi tham số, p-value, mức ý nghĩa, effect size, giả định).
   - 3.2. Xây dựng và thực hiện 2 câu hỏi nghiên cứu (RQ1, RQ2 và mở rộng Chi-square).
   - 3.3. Kết luận và hạn chế của phần 3 (tự tương quan chuỗi thời gian, vi phạm giả định chuẩn, cỡ mẫu lớn).
4. **Tạo `hypothesis_findings.md` và cập nhật `HANDOFF.md`** để thông báo trạng thái bàn giao cho toàn nhóm.
