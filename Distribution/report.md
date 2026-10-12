# CHƯƠNG 2. PHÂN TÍCH PHÂN PHỐI XÁC SUẤT

## 2.1. Giới thiệu và Kiểm tra Dữ liệu Đầu vào

### 2.1.1. Bối cảnh và Mục tiêu Nghiên cứu

Nhu cầu thuê xe đạp trong các hệ thống giao thông công cộng đô thị biến động phức tạp theo chu kỳ thời gian (khung giờ trong ngày, ngày làm việc so với ngày nghỉ) và các điều kiện thời tiết vi mô (nhiệt độ, độ ẩm). Trong Chương 1 (EDA), các phân tích sơ bộ đã chỉ ra rằng biến mục tiêu tổng số lượt thuê xe theo giờ (`cnt`) có phân phối lệch phải rõ rệt với đuôi dài hướng về các giá trị cao, trong khi các biến thời tiết như nhiệt độ (`temp`) và độ ẩm (`hum`) có dạng đối xứng tương đối trên thang đo chuẩn hóa $[0, 1]$.

Mục tiêu cốt lõi của Chương 2 là thực hiện phân tích xác suất chuyên sâu nhằm:
1. **Khảo sát phân phối thực nghiệm:** Mô tả chi tiết hình dạng, độ lệch, độ nhọn, mức độ tập trung và các phân vị thực nghiệm của biến mục tiêu `cnt`.
2. **Khớp và đối chiếu các phân phối lý thuyết rời rạc và liên tục:** Đánh giá hiện tượng phân tán vượt mức (over-dispersion) và so sánh định lượng mức độ phù hợp của 4 mô hình phân phối: Poisson, Negative Binomial, Normal (cắt tại 0) và Log-normal thông qua hàm hợp lý cực đại (MLE) cùng các tiêu chí thông tin AIC, BIC.
3. **Kiểm định độ phù hợp (Goodness-of-Fit - GOF) và trực quan hóa Q-Q Plot:** Đánh giá sai số phân vị và khoảng cách Kolmogorov-Smirnov ($D$), làm rõ hiện tượng "phạt cỡ mẫu lớn" của các kiểm định cổ điển khi cỡ mẫu $N = 17,379$.
4. **Giải mã bản chất đa chế độ (Multi-regime):** Khảo sát cấu trúc hỗn hợp thực nghiệm (Empirical Mixture) của `cnt` thông qua nhịp giờ phân tách theo loại ngày (`workingday`), chỉ ra nguyên nhân bản chất khiến các mô hình đơn biến không thể khớp trọn vẹn toàn bộ dải phân phối.
5. **Mô hình hóa biến giải thích liên tục (`temp`) và hiệu ứng mùa vụ:** So sánh mô hình Normal và Beta cho biến `temp` trên miền $[0, 1]$, kiểm tra độ nhạy biên (boundary sensitivity) và bóc tách các đỉnh gợn sóng thông qua phân bố nhiệt độ theo 4 mùa.
6. **Đóng gói hàm ý chuyển giao downstream:** Cung cấp cơ sở khoa học cho TV3 (chọn kiểm định tham số/phi tham số), TV4 (lựa chọn tương quan Pearson/Spearman) và TV5 (chiến lược tạo đặc trưng và lựa chọn hàm liên kết GLM).

---

### 2.1.2. Dữ liệu và Biến Phân tích

Nghiên cứu sử dụng tệp dữ liệu đã qua tiền xử lý chuẩn hóa `EDA/cleaned_data/hour_cleaned.csv` từ TV1, bao gồm $17,379$ dòng quan sát và 17 biến số. Bốn biến trọng tâm được lựa chọn phân tích bao gồm:

| Biến số | Vai trò phân tích | Thang đo / Đơn vị | Lý do lựa chọn và Lưu ý nghiệp vụ |
| :--- | :--- | :--- | :--- |
| **`cnt`** | Biến mục tiêu chính | Lượt thuê/giờ ($\ge 1$) | Biến đếm rời rạc (Count variable), phản ánh toàn bộ quy mô nhu cầu hệ thống. |
| **`temp`** | Biến giải thích liên tục | Chuẩn hóa $[0, 1]$ (tương ứng $[-8, +39] \text{ °C}$) | Biến thời tiết có tương quan mạnh nhất với `cnt`, phân phối bị chặn trên đoạn $[0, 1]$. |
| **`hum`** | Biến giải thích đối chứng | Chuẩn hóa $[0, 1]$ (tương ứng $[0, 100]\%$) | Biến môi trường liên tục bị chặn hai đầu, có quan hệ nghịch biến với nhu cầu. |
| **`workingday`** | Biến phân tầng nhịp sinh hoạt | Nhị phân (0: Nghỉ/Cuối tuần, 1: Ngày làm việc) | Nhân tố chi phối phân hóa hình thái nhu cầu theo giờ (Commuter vs Leisure). |

> **Quy tắc rò rỉ dữ liệu (Data Leakage):** Hai biến `casual` (khách vãng lai) và `registered` (hội viên) chỉ được dùng để kiểm tra tính toàn vẹn đẳng thức $cnt = casual + registered$, tuyệt đối không đưa vào làm biến giải thích độc lập cho `cnt`.

---

### 2.1.3. Kiểm tra Tính Toàn vẹn Dữ liệu Đầu vào (Sanity Checks)

Để đảm bảo tính nhất quán tuyệt đối theo "hợp đồng dữ liệu" nhóm, toàn bộ các phép kiểm tra chất lượng dữ liệu được tái lập trực tiếp bằng code trên bộ dữ liệu đang phân tích trước khi khớp mô hình.

**Bảng 2.1. Kết quả kiểm tra dữ liệu đầu vào đối chiếu với baseline EDA**

| Nội dung kiểm tra | Kết quả tính toán thực tế | Mốc đối chiếu Baseline EDA | Trạng thái đối chiếu |
| :--- | :---: | :---: | :---: |
| Quy mô dòng ($N$) | 17,379 | 17,379 | Khớp tuyệt đối |
| Số lượng biến sau chuẩn hóa | 17 | 17 | Khớp tuyệt đối |
| Tổng số ô khuyết thiếu (Missing values) | 0 | 0 | Khớp tuyệt đối |
| Số dòng trùng lặp hoàn toàn | 0 | 0 | Khớp tuyệt đối |
| Trùng lặp khóa định danh (`dteday`, `hr`) | 0 | 0 | Khớp tuyệt đối |
| Dòng vi phạm $cnt = casual + registered$ | 0 | 0 | Khớp tuyệt đối |
| Số lượng dòng có $cnt = 0$ | 0 | 0 | Khớp tuyệt đối |
| Giá trị $cnt$ nhỏ nhất (Min) | 1.0 | 1.0 | Khớp tuyệt đối |
| Giá trị $cnt$ lớn nhất (Max) | 977.0 | 977.0 | Khớp tuyệt đối |
| Số lượng dòng có $hum = 0$ (sau xử lý) | 0 | 0 | Khớp tuyệt đối |

*Nhận xét:* Dữ liệu đầu vào hoàn toàn sạch, không có bản ghi khuyết thiếu và thỏa mãn 100% các ràng buộc cấu trúc logic. Biến mục tiêu $cnt \ge 1$ (Zero-truncated), do đó các phân phối lý thuyết biến đếm cần được xem xét trên miền số nguyên dương.

---

## 2.2. Thống kê Mô tả Tổng thể

Thống kê mô tả được thiết lập nhằm tóm tắt mức độ tập trung, độ phân tán và hình dạng phân phối của các biến nghiên cứu chính. Đối với biến đếm `cnt`, tỷ số $\text{Variance}/\text{Mean}$ được tính toán bổ sung để đánh giá giả định đẳng phân tán (equidispersion) của phân phối Poisson.

**Bảng 2.2. Thống kê mô tả của các biến nghiên cứu chính ($N = 17,379$)**

| Biến | Mean | Median | Std | Min | Q1 | Q3 | Max | IQR | Skewness | Kurtosis | Variance/Mean |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`cnt`** | 189.46 | 142.00 | 181.39 | 1.00 | 40.00 | 281.00 | 977.00 | 241.00 | +1.2774 | +1.4172 | **173.6563** |
| **`temp`** | 0.4970 | 0.5000 | 0.1926 | 0.0200 | 0.3400 | 0.6600 | 1.0000 | 0.3200 | -0.0060 | -0.9419 | 0.0746 |
| **`hum`** | 0.6281 | 0.6300 | 0.1918 | 0.0800 | 0.4800 | 0.7800 | 1.0000 | 0.3000 | -0.0828 | -0.9119 | 0.0585 |

*Ghi chú: Đơn vị của `cnt` là lượt thuê/giờ; `temp` và `hum` ở thang đo chuẩn hóa $[0, 1]$. Kurtosis là Excess Kurtosis (độ nhọn chuẩn tắc bằng 0).*

### Nhận xét Thống kê Mô tả:
1. **Biến mục tiêu `cnt`:**
   - Giá trị trung bình ($\text{Mean} = 189.46$) cao hơn rõ rệt so với trung vị ($\text{Median} = 142.00$), kết hợp cùng hệ số bất đối xứng $\text{Skewness} = +1.2774 > 0$, xác nhận phân phối thực nghiệm của lượt thuê xe bị kéo lệch phải mạnh bởi một nhóm nhỏ các khung giờ có nhu cầu đột biến.
   - Độ nhọn $\text{Kurtosis} = +1.4172 > 0$ biểu thị phân phối nhọn hơn phân phối chuẩn (Leptokurtic), với mật độ dồn cục bộ tại vùng giá trị thấp và xuất hiện đuôi dày ở vùng giá trị cao.
   - **Tỷ số $\text{Variance}/\text{Mean} = 173.6563 \gg 1$:** Phương sai thực nghiệm ($\sigma^2 \approx 32,902.3$) gấp hơn 173 lần giá trị kỳ vọng trung bình. Đây là bằng chứng định lượng không thể bác bỏ về hiện tượng **Phân tán vượt mức cực đoan (Severe Over-dispersion)**, vi phạm hoàn toàn giả định nền tảng $\text{Var}(X) = E(X)$ của phân phối Poisson cổ điển.
2. **Biến nhiệt độ (`temp`) và độ ẩm (`hum`):**
   - Cả hai biến đều có giá trị trung bình xấp xỉ trung vị ($\text{Mean} \approx \text{Median} \approx 0.50$ cho `temp`; $0.63$ cho `hum`) và hệ số Skewness gần như bằng 0 ($-0.0060$ và $-0.0828$), cho thấy hình thái phân phối có tính đối xứng rất cao.
   - Tuy nhiên, hệ số Kurtosis âm ($\approx -0.94$ và $-0.91$) thể hiện dạng phân phối đỉnh bẹt (Platykurtic), phân tán đều và thiếu vắng các đỉnh nhọn cực đoan.

---

## 2.3. Phân phối Thực nghiệm của Biến Mục tiêu (`cnt`)

### 2.3.1. Trực quan hóa Đa góc nhìn

Để quan sát toàn diện hình thái dữ liệu, Hình 2.1 kết hợp 3 bảng biểu trực quan hóa chuẩn tắc: Biểu đồ phân bố tần suất (Histogram & KDE), Hàm phân phối tích lũy thực nghiệm (ECDF) và Biểu đồ hộp (Boxplot).

![Hình 2.1. Phân phối thực nghiệm của tổng lượt thuê theo giờ](assets/fig_2_1_cnt_empirical.png)

**Hình 2.1. Phân phối thực nghiệm, tỷ lệ tích lũy ECDF và độ phân tán của tổng lượt thuê theo giờ (`cnt`).**  
*(Panel trái: Histogram kèm đường mật độ KDE thể hiện độ lệch phải; Panel giữa: Đường tích lũy ECDF đánh dấu các mốc phân vị then chốt; Panel phải: Boxplot thể hiện vùng IQR và các quan sát phân tán ở đuôi cao).*

### 2.3.2. Nhận xét Chi tiết Phân phối Thực nghiệm
- **Vùng tập trung mật độ cao:** Dữ liệu tập trung dày đặc nhất ở vùng số đếm thấp: $50\%$ số quan sát ($P_{50}$) có nhu cầu không vượt quá 142 lượt/giờ; $75\%$ số quan sát ($P_{75}$) có nhu cầu dưới 281 lượt/giờ. Đặc biệt, có tới $6.22\%$ tổng số dòng dữ liệu (1,081 giờ) ghi nhận mức nhu cầu cực thấp ($cnt \le 5$ lượt/giờ), phần lớn rơi vào các khung giờ đêm muộn (01:00 – 04:00).
- **Phần đuôi dài và giá trị cao điểm hợp lệ:** Đuôi phải kéo dài liên tục từ mốc 281 đến giá trị cực đại 977 lượt/giờ. Có $2.91\%$ số quan sát (505 giờ) nằm vượt ngưỡng rào trên của boxplot ($cnt > Q3 + 1.5 \times \text{IQR} = 642.5$). Theo kết quả kiểm tra độ nhạy ở EDA, các giá trị này phản ánh đúng nhu cầu đỉnh giờ tan tầm vào những ngày thời tiết lý tưởng, hoàn toàn là các quan sát thực tế hợp lệ chứ không phải sai số đo đạc.

### 2.3.3. Đánh giá Phép Biến đổi Target (`log1p` và `sqrt`)

Trong nỗ lực khắc phục tính lệch phải của `cnt` phục vụ các mô hình hồi quy tuyến tính cổ điển, hai phép biến đổi phổ biến đã được kiểm tra:
1. **Biến đổi $\log(1 + cnt)$:** Hệ số Skewness sau biến đổi giảm mạnh xuống **$-0.8182$**. Như vậy, phép biến đổi logarit đã "uốn cong quá mức" (over-correction), làm đảo ngược phân phối từ lệch phải mạnh thành lệch trái rõ rệt do kéo dãn khoảng cách giữa các số đếm nhỏ gần 1.
2. **Biến đổi căn bậc hai $\sqrt{cnt}$:** Hệ số Skewness đạt **$+0.2914$**, đưa phân phối về trạng thái đối xứng tương đối gần chuẩn nhất.

> **Kết luận:** Biến đổi $\log(1 + cnt)$ không đưa `cnt` về phân phối Chuẩn hoàn hảo như kỳ vọng lý thuyết. Tuy nhiên, trong mô hình hóa hồi quy (Chương 5 và 6), hàm logarit vẫn có giá trị đặc biệt trong việc ổn định phương sai và cho phép diễn giải hệ số dưới dạng tỷ lệ phần trăm co giãn.

---

## 2.4. Khớp và So sánh các Mô hình Phân phối Lý thuyết cho `cnt`

### 2.4.1. Cơ sở Lý thuyết Lựa chọn Mô hình

Do $cnt$ là biến đếm không âm với đặc tính phân tán vượt mức, bốn mô hình phân phối lý thuyết được lựa chọn để khớp tham số bằng phương pháp Hợp lý cực đại (Maximum Likelihood Estimation - MLE):
1. **Phân phối Poisson (Biến đếm một tham số):**
   - Hàm khối xác suất: $P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}, \quad k \in \{0, 1, 2, \dots\}$.
   - Ràng buộc: $E(X) = \text{Var}(X) = \lambda$. Đây là mô hình chuẩn mực cho quá trình đếm ngẫu nhiên độc lập nhưng không cho phép phương sai vượt quá kỳ vọng.
2. **Phân phối Negative Binomial (Biến đếm hai tham số):**
   - Biểu diễn tổng quát theo kỳ vọng $\mu$ và tham số phân tán $r$ (hoặc $\alpha = 1/r$):
     $$\text{Var}(X) = \mu + \frac{\mu^2}{r} = \mu + \alpha \mu^2$$
   - Do có thêm số hạng phương sai bậc hai $\alpha \mu^2$, phân phối này có khả năng hấp thụ hoàn toàn hiện tượng phân tán vượt mức.
3. **Phân phối Chuẩn (Normal - Baseline liên tục đối xứng):** $X \sim \mathcal{N}(\mu, \sigma^2)$, cắt tại 0 để xử lý miền giá trị dương.
4. **Phân phối Log-normal (Baseline liên tục lệch phải):** $\ln(X) \sim \mathcal{N}(\mu, \sigma^2)$, dùng làm mốc so sánh liên tục có đuôi nặng.

Hai tiêu chuẩn thông tin Akaike Information Criterion ($AIC = 2k - 2\ln(L)$) và Bayesian Information Criterion ($BIC = k\ln(n) - 2\ln(L)$) được sử dụng để đánh giá xếp hạng mô hình (giá trị càng nhỏ càng tối ưu).

---

### 2.4.2. Kết quả Khớp Tham số và Tiêu chí Thông tin

![Hình 2.2. So sánh các phân phối lý thuyết với nhu cầu thuê xe theo giờ](assets/fig_2_2_cnt_fits.png)

**Hình 2.2. So sánh đường cong phân phối lý thuyết (Poisson, Negative Binomial, Log-normal, Normal) với histogram thực nghiệm của `cnt`.**  
*(Đường màu cam Negative Binomial bám sát cấu trúc phân bố thực nghiệm ở cả vùng đỉnh thấp lẫn vùng đuôi dốc).*

**Bảng 2.3. Kết quả ước lượng tham số MLE và tiêu chí thông tin các mô hình phân phối cho `cnt` ($N = 17,379$)**

| Mô hình phân phối | Phân loại | Tham số ước lượng MLE | Số tham số ($k$) | Log-Likelihood | AIC | BIC | Xếp hạng AIC |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Negative Binomial** | Rời rạc (Đếm) | $r = 1.0973$; $p = 0.0058$ (hoặc $\mu = 189.46, \alpha = 0.9113$) | 2 | -108,805.54 | **217,615.08** | **217,630.60** | **Hạng 1** |
| **Log-normal** | Liên tục (Dương) | $\text{shape} (\sigma) = 1.4861$; $\text{scale} = 93.3244$ | 2 | -110,377.02 | **220,758.05** | **220,773.57** | **Hạng 2** |
| **Normal** (cắt tại 0) | Liên tục (Đối xứng) | $\mu = 189.4631$; $\sigma = 181.3824$ | 2 | -115,041.09 | **230,086.18** | **230,101.70** | **Hạng 3** |
| **Poisson** | Rời rạc (Đếm) | $\lambda = 189.4631$ | 1 | -1,501,246.10 | **3,002,494.20** | **3,002,501.97** | **Hạng 4** |

### Nhận xét Đánh giá Mô hình:
1. **Sự sụp đổ hoàn toàn của Phân phối Poisson:**
   - AIC của Poisson bùng nổ lên mức $3,002,494.20$, chênh lệch $\Delta\text{AIC} > 2.78 \times 10^6$ so với các mô hình còn lại.
   - Do bị trói buộc bởi giả định $\text{Var}(X) = \lambda = 189.46$, đồ thị PMF của Poisson bị co cụm cực hẹp quanh giá trị trung bình (trong khoảng $[140, 240]$) và hoàn toàn bất lực trong việc bao phủ dải dữ liệu từ 1 đến 977 của `cnt`. Điều này loại bỏ hoàn toàn khả năng sử dụng Poisson đơn thuần cho bài toán.
2. **Chiến thắng tuyệt đối của Negative Binomial:**
   - Phân phối Negative Binomial đạt chỉ số thông tin thấp nhất toàn diện ($AIC = 217,615.08; BIC = 217,630.60$), vượt trội hơn Log-normal ($\Delta\text{AIC} = 3,142.97$) và Normal ($\Delta\text{AIC} = 12,471.10$).
   - Nhờ tham số phân tán $r = 1.0973$, mô hình giải phóng phương sai lên mức $\approx 32,900$, tái hiện chính xác mật độ cao ở vùng số đếm nhỏ đồng thời kéo dài đuôi xác suất đón nhận các giá trị lớn.

---

## 2.5. Kiểm định Độ phù hợp (Goodness-of-Fit) và Biểu đồ Q-Q Plot

### 2.5.1. Trực quan hóa Biểu đồ Phân vị (Q-Q Plot)

Hình 2.3 trình bày biểu đồ Quantile-Quantile (Q-Q plot) 4 panel so sánh phân vị thực nghiệm của `cnt` với 4 phân phối lý thuyết.

![Hình 2.3. Mức độ phù hợp của các phân phối lý thuyết với nhu cầu thuê xe](assets/fig_2_3_cnt_qq_gof.png)

**Hình 2.3. Biểu đồ Quantile-Quantile (Q-Q Plot) đối chiếu 4 mô hình phân phối với dữ liệu thực nghiệm `cnt`.**  
*(Đường chéo màu đỏ $y = x$ đại diện cho sự ăn khớp hoàn hảo giữa thực nghiệm và lý thuyết).*

### 2.5.2. Kết quả Kiểm định Định lượng (KS-test và Chi-square GOF)

**Bảng 2.5. Đánh giá độ phù hợp Goodness-of-Fit cho phân phối `cnt` ($N = 17,379$)**

| Mô hình lý thuyết | Khoảng cách KS ($D$) | Thống kê Chi-square ($\chi^2$) | Bậc tự do ($df$) | $p$-value Chi-square | Đánh giá sai lệch trực quan trên Q-Q Plot |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Negative Binomial** | **0.0594** | **946.60** | 27 | $< 0.0001$ | Bám sát đường $y = x$ từ mốc 1 đến 500; chỉ lệch nhẹ ở vùng đỉnh cao điểm $> 600$. |
| **Log-normal** | 0.1183 | 2,845.12 | 27 | $< 0.0001$ | Bẻ gập xuống ở đuôi cao: quantile lý thuyết bùng nổ $> 12,000$ trong khi mẫu chỉ tới 977. |
| **Normal** (cắt 0) | 0.0769 | 4,210.85 | 27 | $< 0.0001$ | Uốn lượn hình chữ S rõ rệt; thất bại trong việc mô tả tính bất đối xứng. |
| **Poisson** | 0.5257 | 913,620.55 | 4 | $< 0.0001$ | Đồ thị Q-Q dựng đứng; quantile lý thuyết bị giới hạn trong khoảng hẹp $[140, 240]$. |

### Nhận xét Chuyên sâu về Kiểm định GOF:
1. **Khoảng cách Kolmogorov-Smirnov ($D$):** Negative Binomial đạt khoảng cách cực đại nhỏ nhất $D = 0.0594$, khẳng định sai lệch tích lũy giữa hàm phân phối lý thuyết và thực nghiệm không bao giờ vượt quá $5.94\%$ trên toàn bộ dải giá trị.
2. **Nghịch lý $p$-value trong mẫu lớn ($N = 17,379$):**
   - Mặc dù Negative Binomial mô tả dữ liệu xuất sắc, kiểm định Chi-square vẫn trả về $p < 0.0001$.
   - **Giải thích phương pháp luận:** Khi cỡ mẫu lên tới $17,379$, năng lực kiểm định (Statistical Power) tiệm cận $100\%$, khiến phép thử thống kê trở nên siêu nhạy cảm và bác bỏ $H_0$ trước bất kỳ một sai lệch thực tế nhỏ nào. Vì vậy, trong phân tích dữ liệu lớn, **không được dùng $p$-value làm tiêu chuẩn duy nhất để loại bỏ mô hình**, mà phải dựa trên khoảng cách $D$, AIC/BIC và hình thái Q-Q plot.
3. **Hiện tượng bùng nổ đuôi của Log-normal:** Log-normal có đuôi lý thuyết kéo dài quá mức (quantile lý thuyết dự phóng tới $> 12,000$), hoàn toàn phi thực tế đối với trần năng lực vật lý của hệ thống trạm xe đạp đô thị.

---

## 2.6. Cấu trúc Đa Chế độ (Multi-regime) và Phân tích Nhịp giờ

### 2.6.1. Nguyên lý Phân phối Hỗn hợp Thực nghiệm (Empirical Mixture Concept)

Nguyên nhân căn bản khiến đường Q-Q của Negative Binomial vẫn còn sai lệch nhẹ ở vùng $cnt > 500$ nằm ở chỗ: **`cnt` không phải là một phân phối đơn biến đồng nhất, mà là sự xếp chồng của nhiều chế độ hành vi di chuyển xã hội khác nhau (Multi-regime mixture):**

$$f(cnt) = \sum_{w \in \{0, 1\}} \sum_{h=0}^{23} P(\text{workingday} = w, \text{hr} = h) \cdot f(cnt \mid \text{workingday} = w, \text{hr} = h)$$

Mỗi chế độ mang một cơ chế tạo sinh dữ liệu riêng biệt:
- **Chế độ đêm khuya (Off-peak Night regime, 00h - 05h):** Nhu cầu giao thông tê liệt, tập trung $29.26\%$ các giá trị số đếm cực thấp ($cnt \le 5$).
- **Chế độ đi làm ngày thường (Commuter regime):** Nhóm khách hội viên (`registered`) tạo ra 2 đỉnh cực nhọn lúc 08h sáng và 17h chiều.
- **Chế độ thư giãn ngày nghỉ (Leisure regime):** Khách vãng lai (`casual`) tạo ra một đỉnh vòm thoải duy nhất vào buổi trưa và đầu giờ chiều (11h - 15h).

---

### 2.6.2. Phân tách Định lượng theo Khung giờ và Loại ngày

Hình 2.6 và Bảng 2.6 thể hiện sự phân hóa sâu sắc của các chế độ nhu cầu trên toàn bộ 24 khung giờ giữa ngày làm việc và ngày nghỉ.

![Hình 2.6. Số lượt thuê xe trung bình theo giờ trong ngày phân tách theo loại ngày](assets/fig_2_6_cnt_by_hour_workingday.png)

**Hình 2.6. Số lượt thuê xe trung bình theo giờ trong ngày phân tách theo loại ngày (`workingday`).**  
*(Đường màu xanh thể hiện Ngày làm việc với 2 đỉnh nhọn commuter; đường màu cam thể hiện Ngày nghỉ với 1 đỉnh vòm thư giãn; vùng bóng mờ biểu thị dải sai số chuẩn $\pm 1 \text{ SEM}$).*

**Bảng 2.6. Thống kê mô tả các chế độ nhu cầu thuê xe theo khung giờ và loại ngày**

| Loại ngày | Khung giờ chức năng | Số giờ ($n$) | Mean | SD | Median | Q1 | Q3 | Tỷ lệ $cnt \le 5$ |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Ngày nghỉ / Cuối tuần**<br>(`workingday = 0`) | 1. Đêm (00h - 05h) | 1,364 | 43.00 | 42.00 | 27.0 | 10.0 | 69.0 | 12.54% |
| | 2. Cao điểm sáng (08h - 09h) | 462 | 138.64 | 90.10 | 122.0 | 70.0 | 189.8 | 0.22% |
| | 3. Buổi trưa (11h - 14h) | 924 | 354.74 | 171.60 | 354.0 | 225.8 | 472.2 | 0.00% |
| | 4. Cao điểm chiều (17h - 18h) | 461 | 302.35 | 166.42 | 297.0 | 159.0 | 419.0 | 0.00% |
| | 5. Khung giờ khác | 2,303 | 178.21 | 157.56 | 132.0 | 48.0 | 272.5 | 2.43% |
| **Ngày làm việc**<br>(`workingday = 1`) | 1. Đêm (00h - 05h) | 2,912 | 16.44 | 17.17 | 10.0 | 5.0 | 24.0 | **29.26%** |
| | 2. Cao điểm sáng (08h - 09h) | 992 | 359.26 | 186.70 | 327.5 | 210.0 | 462.5 | 0.00% |
| | 3. Buổi trưa (11h - 14h) | 1,989 | 185.28 | 85.60 | 182.0 | 124.0 | 242.0 | 0.05% |
| | 4. Cao điểm chiều (17h - 18h) | 997 | **508.78** | 225.05 | **522.0** | 333.0 | 672.0 | 0.00% |
| | 5. Khung giờ khác | 4,975 | 203.49 | 132.88 | 172.0 | 102.0 | 282.0 | 0.00% |

*Nhận xét:*
- Vào ngày làm việc, lúc 17h–18h chiều, nhu cầu đạt đỉnh trung bình $508.78$ lượt/giờ với $Q3 = 672.0$ lượt/giờ; trong khi ban đêm trung bình chỉ $16.44$ lượt/giờ.
- Việc gộp hai chế độ có kỳ vọng chênh lệch hơn 30 lần vào một biến đơn biến duy nhất tất yếu tạo ra độ phân tán vượt mức giả tạo (spurious over-dispersion). Đây là căn cứ quyết định để TV5 phải sử dụng biến tương tác `workingday × hr` trong mô hình hồi quy.

---

## 2.7. Phân tích Biến Giải thích: Nhiệt độ (`temp`) và Hiệu ứng Mùa vụ

### 2.7.1. Mô hình Phân phối Normal so với Beta cho `temp`

Biến nhiệt độ `temp` được chuẩn hóa trên đoạn $[0, 1]$. Hai mô hình lý thuyết được xem xét:
1. **Phân phối Chuẩn (Normal):** Giả định đối xứng không bị chặn, $\mu = 0.4970, \sigma = 0.1926$.
2. **Phân phối Beta:** Hàm mật độ trên đoạn $[0, 1]$ xác định bởi hai tham số hình dạng $(\alpha, \beta)$:
   $$f(x; \alpha, \beta) = \frac{1}{B(\alpha, \beta)} x^{\alpha - 1} (1 - x)^{\beta - 1}, \quad x \in [0, 1]$$

![Hình 2.4. Phân phối và mức độ phù hợp của các mô hình cho nhiệt độ và độ ẩm](assets/fig_2_4_weather_fits.png)

**Hình 2.4. Phân phối thực nghiệm, Q-Q Plot và hàm phân phối tích lũy ECDF của `temp` và `hum`.**

**Bảng 2.7. So sánh kết quả ước lượng phân phối cho biến nhiệt độ (`temp`) ($N = 17,379$)**

| Mô hình phân phối | Miền hỗ trợ lý thuyết | Tham số ước lượng MLE | $k$ | Log-Likelihood | AIC | BIC | Đánh giá tính hợp lệ miền giá trị |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **Normal** | $(-\infty, +\infty)$ | $\mu = 0.4970$; $\sigma = 0.1926$ | 2 | 3,970.37 | -7,936.74 | -7,921.21 | Vi phạm: Gán xác suất $0.94\%$ ra ngoài đoạn $[0, 1]$. |
| **Beta** (cơ sở) | $[0, 1]$ | $\alpha = 2.9362$; $\beta = 2.9728$ | 2 | 4,553.10 | **-9,102.19** | **-9,086.66** | **Tôn trọng hoàn toàn miền giá trị bị chặn $[0, 1]$.** |

**Bảng 2.7b. Phân tích độ nhạy biên (Boundary Clipping Sensitivity) của mô hình Beta**

| Kịch bản xử lý biên | Ngưỡng clip ($\epsilon$) | Số điểm bị clip | $\alpha$ | $\beta$ | Log-Likelihood | AIC |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Cơ sở (Baseline)** | $\epsilon = 0.5/n \approx 2.88 \times 10^{-5}$ | 1 | 2.936196 | 2.972787 | 4,553.10 | -9,102.19 |
| **Độ nhạy (Sensitivity)** | $\epsilon = 1.0 \times 10^{-4}$ | 1 | 2.937181 | 2.973967 | 4,555.55 | -9,107.11 |
| **Chênh lệch tuyệt đối** | — | 0 | 0.000986 | 0.001180 | 2.46 | 4.92 |

*Nhận xét:*
- Mô hình Beta vượt trội hoàn toàn so với Normal với mức chênh lệch $\Delta\text{AIC} = 1,165.45$.
- Phân phối Chuẩn gán $0.94\%$ xác suất ra ngoài miền $[0, 1]$ (nhiệt độ âm bất khả thi hoặc vượt ngưỡng tối đa), trong khi Beta tôn trọng tuyệt đối miền giá trị thực tế. Kiểm tra độ nhạy khẳng định ước lượng tham số Beta cực kỳ bền vững trước kỹ thuật xử lý biên.

---

### 2.7.2. Hiệu ứng Chu kỳ 4 Mùa Giải mã Dạng Đa Đỉnh (Multimodal) của `temp`

Trên đồ thị Histogram của `temp` (Hình 2.4), mật độ không có một đỉnh trơn nhẵn mà xuất hiện các gợn sóng đa đỉnh. Hình 2.7 và Bảng 2.8 chứng minh đây là hệ quả của sự phân tầng nhiệt độ theo 4 mùa trong năm tại Washington D.C.

![Hình 2.7. Phân bố nhiệt độ theo 4 mùa](assets/fig_2_7_temp_by_season.png)

**Hình 2.7. Phân bố nhiệt độ chuẩn hóa (`temp`) bóc tách theo 4 mùa trong năm.**  
*(Đường màu xanh: Mùa xuân; màu cam: Mùa hè; màu xanh lá: Mùa thu; màu đỏ: Mùa đông).*

**Bảng 2.8. Thống kê mô tả nhiệt độ chuẩn hóa (`temp`) phân tầng theo 4 mùa**

| Mùa vụ (Theo từ điển UCI) | Số giờ ($n$) | Mean | SD | Median | Min | Max | Skewness | Excess Kurtosis |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. Mùa xuân (Spring)** | 4,242 | 0.2991 | 0.1187 | 0.28 | 0.02 | 0.72 | +0.5893 | +0.3374 |
| **2. Mùa hạ (Summer)** | 4,409 | 0.5447 | 0.1392 | 0.56 | 0.16 | 0.94 | -0.1464 | -0.3770 |
| **3. Mùa thu (Fall)** | 4,496 | 0.7064 | 0.0939 | 0.70 | 0.38 | 1.00 | -0.0066 | +0.1057 |
| **4. Mùa đông (Winter)** | 4,232 | 0.4231 | 0.1222 | 0.42 | 0.14 | 0.76 | +0.2546 | -0.6964 |

*Nhận xét:*
- Nhiệt độ trung bình dịch chuyển rõ rệt qua 4 mùa: Mùa xuân thấp nhất ($0.2991 \approx 6.0\text{ °C}$), Mùa đông trung bình thấp ($0.4231 \approx 11.9\text{ °C}$), Mùa hè ấm áp ($0.5447 \approx 17.6\text{ °C}$) và Mùa thu nóng nhất ($0.7064 \approx 25.2\text{ °C}$).
- Sự pha trộn giữa 4 phân phối con theo mùa chính là cơ chế tạo ra dạng đỉnh bẹt và các gợn sóng đa đỉnh của biến `temp`.

---

## 2.8. Kết luận và Hàm ý Chuyển giao Downstream

### 2.8.1. Tóm tắt Kết luận Khoa học
1. **Phân phối của `cnt`:** Bị lệch phải nghiêm trọng (Skewness 1.28), có độ nhọn Leptokurtic (Kurtosis 1.42) và phân tán vượt mức cực đoan ($\text{Variance}/\text{Mean} = 173.66$).
2. **Mô hình tối ưu cho `cnt`:** Phân phối Negative Binomial ($AIC = 217,615.08, D = 0.0594$) vượt trội hoàn toàn so với Poisson ($AIC > 3.0 \times 10^6$), giải quyết thành công bài toán phân tán vượt mức.
3. **Mô hình tối ưu cho `temp`:** Phân phối Beta ($AIC = -9,102.19$) vượt trội hơn Normal ($AIC = -7,936.74$) nhờ tôn trọng miền giá trị bị chặn $[0, 1]$.
4. **Cấu trúc đa chế độ:** Sự biến thiên của `cnt` và `temp` chịu sự chi phối có điều kiện của nhịp giờ xã hội (ngày làm việc vs ngày nghỉ) và chu kỳ khí hậu 4 mùa.

---

### 2.8.2. Hạn chế Phương pháp luận
1. **Tự tương quan chuỗi thời gian:** Tự tương quan bậc 1 ($r_1 = 0.8431$) làm suy giảm cỡ mẫu hiệu dụng xuống $N_{\text{eff}} \approx 1,479$, dẫn đến việc thổi phồng giá trị thống kê kiểm định Chi-square và làm các bài kiểm tra GOF bác bỏ $H_0$.
2. **Giới hạn của mô hình tĩnh đơn biến:** Không thể biểu diễn đồng thời cả hai đỉnh cao điểm công sở và trần dung lượng trạm xe nếu không đưa thêm các biến điều kiện phụ trợ.

---

### 2.8.3. Bảng Chuyển giao Khuyến nghị Kỹ thuật cho TV3, TV4, TV5

**Bảng 2.9. Bảng chuyển giao khuyến nghị phương pháp luận từ Chương 2 cho các thành viên tiếp theo**

| Thành viên tiếp nhận / Nhiệm vụ | Phát hiện từ Chương 2 | Hành động kỹ thuật bắt buộc (Downstream Guidance) | Rủi ro cần phòng tránh |
| :--- | :--- | :--- | :--- |
| **TV3: Kiểm định Giả thuyết**<br>*(V-05: Lựa chọn phép kiểm định)* | `cnt` vi phạm nghiêm trọng tính chuẩn ($D_{\text{Normal}} = 0.0769$); phương sai giữa các nhóm biến động rất lớn. | **Bắt buộc dùng kiểm định vững phương sai (Welch's t, Welch's ANOVA)** kết hợp kiểm định phi tham số đối chứng (Mann-Whitney U, Kruskal-Wallis); luôn báo cáo kích thước hiệu ứng (Cohen's d, $\eta^2$). | Tránh dùng Student's t-test hoặc ANOVA cổ điển vì nguy cơ lạm phát Sai lầm loại 1 nghiêm trọng. |
| **TV4: Phân tích Tương quan & Lý thuyết MLR**<br>*(V-06, V-07: Lập bài toán)* | Quan hệ phân vị giữa `cnt` và các biến thời tiết phi tuyến; `cnt` có đuôi dài làm méo mó các mối quan hệ tuyến tính. | **1. Ưu tiên tương quan hạng Spearman** thay vì chỉ phụ thuộc vào Pearson.<br>**2. Định hướng biến đổi target:** Cân nhắc $\log(1 + cnt)$ để ổn định phương sai cho OLS. | Tránh ngộ nhận về mối liên hệ tuyến tính yếu khi thực tế tồn tại quan hệ phi tuyến mạnh mẽ. |
| **TV5: Xây dựng Mô hình Hồi quy**<br>*(V-09, V-11: Feature Engineering & Đánh giá)* | Cấu trúc đa chế độ thể hiện 2 đỉnh nhọn ngày làm việc (08h, 17h) và 1 đỉnh vòm ngày nghỉ (13h); `temp` phân tầng theo mùa. | **1. Bắt buộc tạo biến tương tác giữa giờ và loại ngày:** Kết hợp các hài Fourier $(\sin, \cos)$ của giờ với `workingday`.<br>**2. Quy đổi về thang gốc:** Mọi chỉ số đánh giá (MAE, RMSE) sau khi fit trên $\log(1+cnt)$ phải quy đổi ngược qua $e^z - 1$. | Nếu chỉ đưa `workingday` như một biến độc lập đơn lẻ, hệ số sẽ bị triệt tiêu và mất hoàn toàn khả năng dự báo theo giờ. |

---

## Tài liệu Tham khảo

1. **Akaike, H. (1974).** A new look at the statistical model identification. *IEEE Transactions on Automatic Control*, 19(6), 716–723.
2. **Cameron, A. C., & Trivedi, P. K. (2013).** *Regression Analysis of Count Data* (2nd ed.). Cambridge University Press.
3. **Fanaee-T, H., & Gama, J. (2014).** Event labeling combining ensemble detectors and background knowledge. *Progress in Artificial Intelligence*, 2(2–3), 113–127.
4. **Johnson, N. L., Kemp, A. W., & Kotz, S. (2005).** *Univariate Discrete Distributions* (3rd ed.). John Wiley & Sons.
5. **Schwarz, G. (1978).** Estimating the dimension of a model. *The Annals of Statistics*, 6(2), 461–464.
