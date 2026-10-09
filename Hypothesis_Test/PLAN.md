# KẾ HOẠCH CHI TIẾT: PHẦN 3 — KIỂM ĐỊNH GIẢ THUYẾT (HYPOTHESIS TESTING)
**Thành viên phụ trách:** Thành viên 3 (TV3)  
**Bộ dữ liệu:** Bike Sharing Dataset (`EDA/cleaned_data/hour_cleaned.csv` — 17,379 dòng)  
**Quy chuẩn áp dụng:** `outline.md`, `rules.md`, `HANDOFF.md`

---

## 1. Mục tiêu và Phạm vi công việc của TV3

1. **Thực hiện độc lập và toàn diện Phần 3 (Kiểm định giả thuyết):**
   - Thiết lập nền tảng lý thuyết vững chắc về các phương pháp kiểm định thống kê (tham số, phi tham số, bảng chéo).
   - Xây dựng **3 Câu hỏi nghiên cứu (Research Questions)** gắn liền với bối cảnh nghiệp vụ thực tế của hệ thống chia sẻ xe đạp Capital Bikeshare.
   - Kiểm tra nghiêm ngặt các giả định phân phối; chạy song song kiểm định tham số và phi tham số tương ứng; bắt buộc lượng hóa **Kích thước hiệu ứng (Effect Size)** để đánh giá ý nghĩa thực tiễn (*Practical Significance*), tránh bẫy kết luận hình thức từ cỡ mẫu lớn.
   - Đánh giá rủi ro phương pháp luận: hiện tượng tự tương quan chuỗi thời gian ($r_1 = 0.8431$), cỡ mẫu hiệu dụng ($N_{\text{eff}} \approx 1,479$), nguy cơ Sai lầm loại 1 (Type I Error) và giải pháp kiểm soát.
2. **Chuẩn bị đầu ra chuẩn mực để sẵn sàng gộp báo cáo chung:**
   - Notebook Jupyter (`03_hypothesis_testing.ipynb`) và script Python (`03_hypothesis_testing.py`) chạy độc lập, tái lập 100% kết quả.
   - Hệ thống 6 biểu đồ trực quan hóa chuyên sâu (`fig_3_1` đến `fig_3_6`) xuất ra thư mục `assets/` ở độ phân giải 300 DPI.
   - Tài liệu báo cáo hoàn chỉnh (`report.md`) tuân thủ tuyệt đối quy chuẩn văn phong, công thức, bảng biểu và trích dẫn khoa học.
   - Bảng tổng hợp bàn giao (`hypothesis_findings.md`) theo chuẩn `HANDOFF.md`.

---

## 2. Đối chiếu phụ thuộc và Thẻ VALIDATE

| Thẻ VALIDATE | Nhận từ | Nội dung đối chiếu | Trạng thái tiếp nhận & Hành động của TV3 |
| :--- | :--- | :--- | :--- |
| **V-01 & V-03** | **TV1 (EDA)** | - Dữ liệu sạch `hour_cleaned.csv` (17,379 dòng).<br>- Sự cố `hum = 0` (22 dòng) đã nội suy.<br>- Giữ nguyên `weathersit = 4` (3 dòng) trong file CSV.<br>- Tự tương quan chuỗi $r_1 = 0.8431$, $N_{\text{eff}} \approx 1,479$. | **ĐÃ XÁC NHẬN:** Sử dụng đúng file `EDA/cleaned_data/hour_cleaned.csv`. Chủ động **gộp `weathersit = 4` vào nhóm 3** khi lập bảng chéo/ANOVA để bảo đảm điều kiện tần số kỳ vọng $\ge 5$. |
| **V-05** | **TV2 (Distribution)** | - `cnt` lệch phải mạnh ($\text{Skewness} = 1.28$, $\text{Kurtosis} = 1.42$).<br>- Phân tán vượt mức ($\text{Var}/\text{Mean} = 173.66 \gg 1$).<br>- Vi phạm giả định phân phối chuẩn. | **ĐÃ XÁC NHẬN:** Bắt buộc thiết kế **song song kiểm định tham số và phi tham số** (Welch's t-test vs Mann-Whitney U; Welch's ANOVA vs Kruskal-Wallis); ưu tiên kết luận dựa trên phép thử phi tham số và Effect Size. |
| **V-08** | **TV4 (Correlation)** | Tránh trùng lặp các cặp biến trọng tâm phân tích hồi quy/tương quan tuyến tính của TV4. | **ĐÃ XÁC NHẬN:** TV3 tập trung vào so sánh biến mục tiêu `cnt` theo các biến phân loại (`workingday`, `season`) và kiểm định tính độc lập giữa 2 biến phân loại (`weathersit` × `season`), không trùng lặp phân tích tương quan biến liên tục của TV4. |

---

## 3. Thiết kế 3 Câu hỏi nghiên cứu (Research Questions)

### 📌 Research Question 1 (RQ1) — So sánh 2 nhóm độc lập (Two-Sample Comparison)
* **Câu hỏi nghiên cứu:** *Có sự khác biệt có ý nghĩa thống kê về số lượng thuê xe trung bình mỗi giờ (`cnt`) giữa ngày làm việc (`workingday = 1`) và ngày nghỉ / cuối tuần (`workingday = 0`) hay không?*
* **Bản chất biến số:** Biến phụ thuộc định lượng `cnt` vs Biến độc lập nhị phân `workingday` ($N_1 = 11,865$, $N_0 = 5,514$).
* **Cặp giả thuyết:**
  - $H_0: \mu_{\text{workingday}} = \mu_{\text{non-workingday}}$ (Lượng thuê xe trung bình mỗi giờ giữa 2 loại ngày là như nhau).
  - $H_1: \mu_{\text{workingday}} \neq \mu_{\text{non-workingday}}$ (Có sự khác biệt về lượng thuê xe trung bình mỗi giờ giữa 2 loại ngày).
* **Quy trình kiểm định:**
  1. *Kiểm tra giả định:* Kiểm định tính chuẩn (Q-Q plot, Skewness), kiểm định tính đồng nhất phương sai Levene test ($p < 0.05 \rightarrow$ phương sai không bằng nhau).
  2. *Kiểm định tham số:* Welch's $t$-test (không phụ thuộc giả định đồng nhất phương sai).
  3. *Kiểm định phi tham số:* Mann-Whitney U test (so sánh phân bố vị trí / trung vị trên dữ liệu lệch).
  4. *Lượng hóa Effect Size:* Cohen's $d$ và Rank-biserial correlation ($r$).
  5. *Phân tích chuyên sâu nghiệp vụ:* Mặc dù chênh lệch trung bình tổng thể nhỏ ($193.21$ vs $181.41 \text{ lượt/h}$), phân tích phân tầng theo khung giờ (`hr`) cho thấy sự đảo chiều nhịp sinh hoạt cực mạnh (2 đỉnh 8h & 17h ngày làm việc vs đỉnh vòm 12h–16h ngày nghỉ).

---

### 📌 Research Question 2 (RQ2) — So sánh nhiều nhóm độc lập (Multi-Group Comparison)
* **Câu hỏi nghiên cứu:** *Số lượng thuê xe trung bình mỗi giờ (`cnt`) có sự khác biệt có ý nghĩa thống kê giữa 4 mùa trong năm (`season`: Mùa xuân, Mùa hè, Mùa thu, Mùa đông) hay không?*
* **Bản chất biến số:** Biến phụ thuộc định lượng `cnt` vs Biến độc lập định danh 4 nhóm `season` ($N_{\text{Xuân}} = 4,242$, $N_{\text{Hạ}} = 4,409$, $N_{\text{Thu}} = 4,496$, $N_{\text{Đông}} = 4,232$).
* **Cặp giả thuyết:**
  - $H_0: \mu_1 = \mu_2 = \mu_3 = \mu_4$ (Lượng thuê xe trung bình giữa 4 mùa là đồng nhất).
  - $H_1:$ Tồn tại ít nhất một cặp mùa có lượng thuê xe trung bình khác nhau.
* **Quy trình kiểm định:**
  1. *Kiểm tra giả định:* Levene test kiểm tra tính đồng nhất phương sai giữa 4 mùa.
  2. *Kiểm định tham số:* One-Way ANOVA và Welch's ANOVA (hiệu chỉnh phương sai không đồng nhất).
  3. *Kiểm định phi tham số:* Kruskal-Wallis $H$-test.
  4. *Kiểm định hậu định (Post-hoc Tests):* Games-Howell post-hoc test (tham số) và Dunn's test kết hợp hiệu chỉnh Bonferroni (phi tham số) để so sánh từng cặp mùa cụ thể (Xuân-Hạ, Xuân-Thu, Xuân-Đông, Hạ-Thu, Hạ-Đông, Thu-Đông).
  5. *Lượng hóa Effect Size:* Eta-squared ($\eta^2$), Omega-squared ($\omega^2$) và Epsilon-squared ($\epsilon^2$).

---

### 📌 Research Question 3 (RQ3) — Kiểm định tính độc lập bảng chéo (Contingency Chi-Square)
* **Câu hỏi nghiên cứu:** *Có mối liên hệ phụ thuộc có ý nghĩa thống kê giữa Điều kiện thời tiết (`weathersit`) và Mùa trong năm (`season`) hay không?*
* **Bản chất biến số:** 2 biến phân loại `weathersit` (3 mức sau khi gộp) × `season` (4 mùa).
* **Xử lý nhóm mẫu hiếm (Bắt buộc):** Gộp 3 dòng `weathersit = 4` vào nhóm `3` tạo thành nhóm *Thời tiết bất lợi (Mưa/Tuyết/Bão)*, đảm bảo 100% các ô trong bảng chéo $3 \times 4 = 12 \text{ ô}$ đều có tần số kỳ vọng $E_{ij} \gg 5$.
* **Cặp giả thuyết:**
  - $H_0:$ Điều kiện thời tiết và Mùa trong năm là hai biến cố độc lập về mặt thống kê.
  - $H_1:$ Điều kiện thời tiết và Mùa trong năm có mối liên hệ phụ thuộc lẫn nhau.
* **Quy trình kiểm định:**
  1. Lập bảng tần số quan sát ($O_{ij}$) và bảng tần số kỳ vọng ($E_{ij}$).
  2. Kiểm định Chi-square độc lập Pearson ($\chi^2$).
  3. Lượng hóa Effect Size: Hệ số **Cramér's $V$**.
  4. Phân tích phần dư chuẩn hóa hiệu chỉnh (*Adjusted Standardized Residuals - ASR*) để chỉ rõ các cặp mùa–thời tiết xuất hiện vượt trội hoặc suy giảm đáng kể so với kỳ vọng ngẫu nhiên.

---

## 4. Chiến lược Phương pháp luận: Kiểm soát Rủi ro Sai lầm Loại 1

Với mẫu dữ liệu lớn ($N = 17,379$) và tự tương quan thời gian cao ($r_1 = 0.8431$), TV3 thực thi nghiêm ngặt **3 nguyên tắc phương pháp luận**:

1. **Quy tắc bác bỏ $H_0$ kép:** Bác bỏ $H_0$ khi và chỉ khi thỏa mãn đồng thời:
   - Ý nghĩa thống kê: $p\text{-value} < \alpha = 0.05$.
   - Ý nghĩa thực tiễn: $\text{Effect Size}$ vượt qua ngưỡng tối thiểu có ý nghĩa nghiệp vụ (Cohen's $d \ge 0.2$, $\eta^2 \ge 0.01$, Cramér's $V \ge 0.1$).
2. **Phân tích độ bền vững qua Cỡ mẫu hiệu dụng ($N_{\text{eff}}$ Robustness Check):**
   - Tính toán lại giá trị kiểm định điều chỉnh dựa trên cỡ mẫu độc lập thực tế $N_{\text{eff}} \approx 1,479$:
     $$\text{Statistic}_{\text{adj}} = \text{Statistic}_{\text{gốc}} \times \sqrt{\frac{N_{\text{eff}}}{N}} \approx \frac{\text{Statistic}_{\text{gốc}}}{3.43}$$
   - Đối chiếu xem kết luận bác bỏ $H_0$ có bền vững trước sự suy giảm bậc tự do hiệu dụng hay không.
3. **Văn phong kết luận khoa học:**
   - Dùng: *"Có đủ bằng chứng thống kê ở mức ý nghĩa $\alpha = 0.05$ để bác bỏ giả thuyết $H_0$..."* hoặc *"Chưa đủ bằng chứng thống kê để bác bỏ giả thuyết $H_0$..."*.
   - **Tuyệt đối không viết "Chấp nhận $H_0$"**.

---

## 5. Cấu trúc Tài liệu Báo cáo Dự kiến (`Hypothesis_Test/report.md`)

```text
# CHƯƠNG 3. KIỂM ĐỊNH GIẢ THUYẾT (HYPOTHESIS TESTING)

## 3.1. Cơ sở lý thuyết các phương pháp kiểm định thống kê
   3.1.1. Bản chất của kiểm định giả thuyết thống kê (H0, H1, mức ý nghĩa, p-value, miền bác bỏ)
   3.1.2. Sai lầm loại 1, Sai lầm loại 2 và Tầm quan trọng của Kích thước hiệu ứng (Effect Size)
   3.1.3. Kiểm định tham số vs Kiểm định phi tham số (t-test vs Mann-Whitney U, ANOVA vs Kruskal-Wallis)
   3.1.4. Kiểm định tính độc lập Chi-square và Phân tích phần dư hiệu chỉnh
   3.1.5. Thách thức phương pháp luận: Cỡ mẫu lớn và Tự tương quan chuỗi thời gian (N_eff)

## 3.2. Xây dựng và Thực thi các Câu hỏi nghiên cứu
   3.2.1. Câu hỏi nghiên cứu 1: So sánh nhu cầu thuê xe giữa Ngày làm việc và Ngày nghỉ (RQ1)
          - Đặt vấn đề và Thiết lập giả thuyết
          - Kiểm tra giả định (Tính chuẩn, Đồng nhất phương sai)
          - Kết quả kiểm định tham số (Welch's t-test) và phi tham số (Mann-Whitney U)
          - Lượng hóa Effect Size (Cohen's d, Rank-biserial r) và Phân tầng theo giờ
          - Kết luận và Ý nghĩa thực tiễn
   3.2.2. Câu hỏi nghiên cứu 2: So sánh nhu cầu thuê xe giữa các Mùa trong năm (RQ2)
          - Đặt vấn đề và Thiết lập giả thuyết
          - Kiểm tra giả định (Levene test)
          - Kết quả kiểm định ANOVA, Welch's ANOVA và Kruskal-Wallis
          - Phân tích hậu định từng cặp mùa (Games-Howell & Dunn-Bonferroni)
          - Lượng hóa Effect Size (Eta-squared, Epsilon-squared) và Kết luận
   3.2.3. Câu hỏi nghiên cứu 3: Kiểm định tính độc lập giữa Mùa và Điều kiện thời tiết (RQ3)
          - Đặt vấn đề và Xử lý nhóm mẫu hiếm (Gộp weathersit = 4 vào nhóm 3)
          - Bảng chéo quan sát và tần số kỳ vọng
          - Kết quả kiểm định Pearson Chi-square và Cramér's V
          - Phân tích phần dư chuẩn hóa hiệu chỉnh (ASR) và Kết luận

## 3.3. Đánh giá độ bền vững và Kiểm soát Sai lầm loại 1
   3.3.1. Đánh giá độ bền vững theo Cỡ mẫu hiệu dụng (N_eff Correction)
   3.3.2. Đối chứng kiểm định trên chuỗi tổng hợp theo Ngày (Day-level Aggregates, N = 731)

## 3.4. Kết luận và Hạn chế của Chương 3
   3.4.1. Tóm tắt các kết luận kiểm định chính
   3.4.2. Hạn chế về phương pháp luận và dữ liệu
   3.4.3. Bảng hàm ý chuyển giao cho TV4 và TV5

## Tài liệu tham khảo
```

---

## 6. Danh mục 6 Biểu đồ Trực quan hóa (`Hypothesis_Test/assets/`)

| Tên tệp | Tên biểu đồ chính thức | Nội dung biểu thị |
| :--- | :--- | :--- |
| `fig_3_1_workingday_assumptions.png` | **Hình 3.1. Kiểm tra giả định phân phối và phương sai của cnt theo loại ngày** | Q-Q plot và phân phối mật độ KDE của `cnt` trên ngày làm việc vs ngày nghỉ |
| `fig_3_2_workingday_cnt_comparison.png` | **Hình 3.2. So sánh phân phối và giá trị trung bình cnt giữa Ngày làm việc và Ngày nghỉ** | Boxplot kết hợp Violin plot và khoảng tin cậy 95% Mean `cnt` |
| `fig_3_3_workingday_hourly_interaction.png` | **Hình 3.3. Phân tích tương tác nhịp sinh hoạt theo giờ giữa ngày làm việc và ngày nghỉ** | Line chart xu hướng `cnt` theo 24 khung giờ tách biệt giữa 2 loại ngày |
| `fig_3_4_season_cnt_distributions.png` | **Hình 3.4. Phân phối số lượng thuê xe cnt theo 4 mùa trong năm** | Boxplot + Strip plot phân tán thể hiện sự chênh lệch phân phối giữa 4 mùa |
| `fig_3_5_season_posthoc_diffs.png` | **Hình 3.5. Kết quả so sánh hậu định chênh lệch trung bình từng cặp mùa** | Forest plot biểu diễn khoảng tin cậy 95% chênh lệch khác biệt trung bình giữa 6 cặp mùa |
| `fig_3_6_weather_season_contingency.png` | **Hình 3.6. Ma trận bảng chéo và Phần dư chuẩn hóa hiệu chỉnh giữa Thời tiết và Mùa** | Heatmap phần dư chuẩn hóa hiệu chỉnh (ASR) giữa 3 mức thời tiết × 4 mùa |

---

## 7. Cấu trúc Thư mục và File đầu ra của TV3

```text
Hypothesis_Test/
├── PLAN.md                     # Kế hoạch chi tiết của TV3 (file này)
├── README.md                   # Hướng dẫn chạy môi trường, luồng xử lý và tóm tắt kết quả
├── requirements.txt            # Thư viện sử dụng (scipy, statsmodels, pingouin, seaborn, matplotlib)
├── 03_hypothesis_testing.py    # Script Python thực thi tính toán thuần
├── 03_hypothesis_testing.ipynb # Jupyter Notebook trực quan, đầy đủ biểu đồ, bảng biểu và diễn giải
├── hypothesis_findings.md      # Findings Sheet bàn giao theo chuẩn HANDOFF.md
├── report.md                   # Toàn bộ nội dung báo cáo Chương 3 hoàn chỉnh
└── assets/                     # 6 hình ảnh biểu đồ độ phân giải 300 DPI (fig_3_1 đến fig_3_6)
```

---

## 8. Lộ trình Triển khai Chi tiết

1. **Giai đoạn 1: Môi trường và Script tính toán (`03_hypothesis_testing.py`):**
   - Viết toàn bộ hàm thống kê: Levene, Welch t-test, Mann-Whitney U, Cohen's d, Rank-biserial r, Welch ANOVA, Kruskal-Wallis, Games-Howell, Dunn-Bonferroni, Eta-squared, Epsilon-squared, Chi-square, Cramér's V, ASR matrix, $N_{\text{eff}}$ adjustment.
   - Xuất trọn vẹn 6 hình ảnh `fig_3_1` đến `fig_3_6` vào `Hypothesis_Test/assets/`.
2. **Giai đoạn 2: Xây dựng Jupyter Notebook (`03_hypothesis_testing.ipynb`):**
   - Tích hợp code chạy và trình bày kết quả bảng biểu, biểu đồ rõ ràng, có ghi chú tiếng Việt hoàn chỉnh.
3. **Giai đoạn 3: Soạn thảo Báo cáo chuyên sâu (`Hypothesis_Test/report.md`):**
   - Viết báo cáo học thuật đầy đủ từ Mục 3.1 đến Mục 3.4 theo đúng chuẩn `rules.md` (không có lỗi LaTeX, dấu thập phân `.`, công thức rõ ràng, nhận xét theo chuỗi Quan sát $\rightarrow$ Bằng chứng $\rightarrow$ Ý nghĩa).
4. **Giai đoạn 4: Hoàn thiện Bàn giao và Quản lý Repo:**
   - Tạo `hypothesis_findings.md`, `README.md`, `requirements.txt`.
   - Cập nhật dòng thông báo bàn giao chính thức trong `HANDOFF.md`.
   - Commit và push lên GitHub.
