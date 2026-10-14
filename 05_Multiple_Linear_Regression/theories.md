# CHƯƠNG 5. Hồi quy tuyến tính đa biến (MLR)

## 5.1. Khung lý thuyết Hồi quy tuyến tính Đa biến (MLR)

### 5.1.1. Khái niệm bài toán hồi quy tuyến tính đa biến
Hồi quy tuyến tính đa biến (Multiple Linear Regression – MLR) là một phương pháp thống kê tham số dùng để mô hình hóa mối quan hệ phụ thuộc tuyến tính giữa một biến phụ thuộc (biến mục tiêu $Y$) và hai hay nhiều biến độc lập (các biến giải thích $X_1, X_2, \dots, X_k$).

**Mục đích chính:**
1. **Đánh giá tác động biên (Marginal Effects):** Xác định chiều hướng và lượng hóa mức độ ảnh hưởng của từng biến độc lập $X_j$ lên biến mục tiêu $Y$ trong điều kiện giữ nguyên giá trị của tất cả các biến độc lập khác (*ceteris paribus*).
2. **Dự báo (Prediction):** Ước lượng giá trị kỳ vọng của biến mục tiêu $\hat{Y}$ khi biết trước một tập hợp giá trị đầu vào của các biến giải thích.
3. **Kiểm định giả thuyết nhân quả và cấu trúc:** Đánh giá mức độ đóng góp của từng biến số và kiểm tra sự phù hợp tổng thể của mô hình toán học đối với dữ liệu thực nghiệm.

---

### 5.1.2. Các thành phần của mô hình hồi quy tuyến tính đa biến
Một bài toán hồi quy tuyến tính đa biến bao gồm 5 thành phần toán học cốt lõi:
1. **Biến phụ thuộc (Dependent / Target Variable – $Y$):** Biến số định lượng đại diện cho đại lượng cần được giải thích hoặc dự báo.
2. **Các biến độc lập (Independent / Explanatory Variables – $X_1, X_2, \dots, X_k$):** Tập hợp $k$ yếu tố đo lường được sử dụng để giải thích sự biến thiên của $Y$.
3. **Các hệ số hồi quy (Regression Coefficients – $\beta_0, \beta_1, \dots, \beta_k$):** Các tham số tổng thể chưa biết cần được ước lượng từ dữ liệu mẫu:
   - $\beta_0$: Hệ số chặn (Intercept), đại diện cho giá trị kỳ vọng của $Y$ khi tất cả các biến độc lập đều nhận giá trị bằng 0.
   - $\beta_j$ ($j = 1, \dots, k$): Hệ số hồi quy riêng phần (Partial Regression Coefficients), đo lường mức thay đổi trung bình của $Y$ khi $X_j$ tăng thêm 1 đơn vị và các biến giải thích khác được giữ cố định.
4. **Sai số ngẫu nhiên (Random Error Term – $\varepsilon$):** Thành phần bất định trong tổng thể, đại diện cho sai số đo lường, các yếu tố ngoại sinh bị bỏ sót, hoặc bản chất ngẫu nhiên của hành vi thực tế mà mô hình không thể nắm bắt.
5. **Phần dư (Residual – $e_i$):** Đại lượng đo lường trên mẫu quan sát, biểu thị chênh lệch giữa giá trị quan sát thực tế $Y_i$ và giá trị dự đoán từ mô hình $\hat{Y}_i$:
   $$e_i = Y_i - \hat{Y}_i$$

---

### 5.1.3. Phương trình mô hình và Phương pháp Bình phương Tối thiểu (OLS)

#### 1. Hàm hồi quy tổng thể (Population Regression Function – PRF)
Trong tổng thể, mối quan hệ giữa biến phụ thuộc và các biến độc lập được biểu diễn dưới dạng:
$$Y = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \dots + \beta_k X_k + \varepsilon$$
Hoặc dưới dạng kỳ vọng toán có điều kiện:
$$E(Y \mid X_1, X_2, \dots, X_k) = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \dots + \beta_k X_k$$

#### 2. Hàm hồi quy mẫu (Sample Regression Function – SRF)
Dựa trên mẫu quan sát gồm $n$ quan sát $(Y_i, X_{1i}, \dots, X_{ki})$, phương trình hồi quy mẫu ước lượng được biểu diễn là:
$$\hat{Y}_i = b_0 + b_1 X_{1i} + b_2 X_{2i} + \dots + b_k X_{ki}$$
Trong đó $b_0, b_1, \dots, b_k$ lần lượt là các ước lượng điểm mẫu của các tham số tổng thể $\beta_0, \beta_1, \dots, \beta_k$.

#### 3. Bản chất của phương pháp Bình phương Tối thiểu Thông thường (OLS)
Phương pháp OLS tìm kiếm tập hợp các hệ số ước lượng $(b_0, b_1, \dots, b_k)$ sao cho tổng bình phương các phần dư (Residual Sum of Squares – $SS_{\text{res}}$) đạt giá trị nhỏ nhất:
$$\min \sum_{i=1}^n e_i^2 = \min \sum_{i=1}^n \left( Y_i - (b_0 + b_1 X_{1i} + \dots + b_k X_{ki}) \right)^2$$
Bằng cách lấy đạo hàm riêng theo từng tham số $b_j$ và cho bằng 0, hệ phương trình chuẩn (Normal Equations) được giải để thu được nghiệm tối ưu duy nhất dưới dạng ma trận:
$$\mathbf{b} = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{Y}$$
Điều kiện để ma trận $\mathbf{X}^T \mathbf{X}$ khả nghịch là ma trận thiết kế $\mathbf{X}$ phải có hạng đầy đủ theo cột ($\text{rank}(\mathbf{X}) = k + 1$), nghĩa là không có hiện tượng đa cộng tuyến hoàn hảo giữa các biến giải thích.

---

### 5.1.4. Ý nghĩa của hệ số hồi quy riêng lẻ $\beta_j$
Trong mô hình hồi quy đa biến, hệ số $\beta_j$ được gọi là **hệ số hồi quy riêng phần (Partial Regression Coefficient)**. 

Khác với hồi quy đơn biến (chỉ đo tương quan thô giữa một biến $X$ và $Y$), $\beta_j$ đo lường tác động thuần túy của $X_j$ lên $Y$ sau khi đã kiểm soát và loại trừ ảnh hưởng của tất cả các biến độc lập khác trong mô hình:
- $\beta_j > 0$: $X_j$ có tác động cùng chiều lên $Y$. Khi $X_j$ tăng 1 đơn vị, $Y$ tăng trung bình $\beta_j$ đơn vị (*ceteris paribus*).
- $\beta_j < 0$: $X_j$ có tác động ngược chiều lên $Y$. Khi $X_j$ tăng 1 đơn vị, $Y$ giảm trung bình $|\beta_j|$ đơn vị (*ceteris paribus*).
- $\beta_j \approx 0$: Biến $X_j$ không có tác động tuyến tính đáng kể lên $Y$ khi đã kiểm soát các yếu tố còn lại.

---

### 5.1.5. Hệ số xác định $R^2$
Hệ số xác định $R^2$ (Coefficient of Determination) đo lường tỷ lệ biến thiên của biến phụ thuộc $Y$ được giải thích bởi tập hợp các biến độc lập trong mô hình:
$$R^2 = 1 - \frac{SS_{\text{res}}}{SS_{\text{tot}}} = \frac{SS_{\text{reg}}}{SS_{\text{tot}}}$$
Trong đó:
- $SS_{\text{tot}} = \sum_{i=1}^n (Y_i - \bar{Y})^2$: Tổng bình phương toàn phần (biến thiên tổng thể của $Y$).
- $SS_{\text{reg}} = \sum_{i=1}^n (\hat{Y}_i - \bar{Y})^2$: Tổng bình phương hồi quy (phần biến thiên được mô hình giải thích).
- $SS_{\text{res}} = \sum_{i=1}^n (Y_i - \hat{Y}_i)^2$: Tổng bình phương phần dư (phần biến thiên chưa giải thích được).

Khoảng giá trị của $R^2$ nằm trong đoạn $[0, 1]$. $R^2$ càng gần 1, mô hình giải thích được càng nhiều biến thiên của dữ liệu. 

**Hạn chế của $R^2$:** $R^2$ là một hàm đơn điệu không giảm theo số lượng biến độc lập. Cứ thêm bất kỳ một biến mới nào vào mô hình (kể cả biến hoàn toàn vô nghĩa), $R^2$ sẽ luôn tăng hoặc giữ nguyên, không bao giờ giảm. Do đó, $R^2$ không phải là tiêu chuẩn tối ưu để so sánh các mô hình có số lượng biến giải thích khác nhau.

---

### 5.1.6. Hệ số xác định hiệu chỉnh (Adjusted $R^2$)
Để khắc phục nhược điểm của $R^2$, hệ số xác định hiệu chỉnh (Adjusted $R^2$, ký hiệu là $\bar{R}^2$) đưa vào một hình phạt (penalty) đối với số lượng biến giải thích được đưa vào mô hình dựa trên số bậc tự do:
$$\bar{R}^2 = 1 - (1 - R^2) \frac{n - 1}{n - k - 1} = 1 - \frac{SS_{\text{res}} / (n - k - 1)}{SS_{\text{tot}} / (n - 1)}$$
Trong đó:
- $n$: Số lượng quan sát mẫu.
- $k$: Số lượng biến độc lập (không tính hệ số chặn).
- $n - k - 1$: Số bậc tự do của phần dư.

**Ý nghĩa:** Khác với $R^2$, Adjusted $R^2$ chỉ tăng lên khi biến độc lập mới được thêm vào giúp giảm phương sai phần dư ($SS_{\text{res}} / (n - k - 1)$) đủ lớn để bù đắp cho sự mất mát 1 bậc tự do. Nếu biến mới đưa vào không có ý nghĩa thống kê, Adjusted $R^2$ sẽ sụt giảm. Do đó, Adjusted $R^2$ là thước đo khách quan để lựa chọn và so sánh các mô hình cạnh tranh.

---

### 5.1.7. Các chỉ số đo lường sai số dự báo thực tế
Khi đánh giá năng lực dự báo trên tập dữ liệu kiểm tra độc lập, hai chỉ số sai số chuẩn mực được áp dụng:
1. **Sai số tuyệt đối trung bình (Mean Absolute Error – MAE):**
   $$\text{MAE} = \frac{1}{n} \sum_{i=1}^n |Y_i - \hat{Y}_i|$$
   MAE đo lường độ lớn trung bình của các sai số dự báo trên cùng đơn vị đo của biến mục tiêu, có ưu điểm trực quan, dễ diễn giải và ít bị chi phối quá mức bởi các giá trị ngoại lai.
2. **Căn bậc hai sai số bình phương trung bình (Root Mean Squared Error – RMSE):**
   $$\text{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^n (Y_i - \hat{Y}_i)^2}$$
   Do có bình phương sai số trước khi lấy căn, RMSE phạt nặng hơn các sai số dự báo có độ lệch lớn, rất phù hợp trong các bài toán vận hành logistics khi việc dự báo thiếu/thừa nghiêm trọng gây ra chi phí rủi ro cao.

---

### 5.1.8. Năm giả định Gauss-Markov cổ điển của mô hình OLS
Theo Định lý Gauss-Markov, nếu mô hình hồi quy thỏa mãn 5 giả định cổ điển sau đây, ước lượng OLS sẽ là ước lượng tuyến tính không chệch tốt nhất (Best Linear Unbiased Estimator – BLUE):
1. **Tính tuyến tính theo tham số (Linearity in parameters):** Mô hình phải có dạng tuyến tính đối với các hệ số $\beta_j$, mặc dù các biến độc lập $X_j$ có thể trải qua các phép biến đổi phi tuyến (như $\log$, bậc hai, hàm lượng giác).
2. **Tính độc lập của sai số (Independence of errors / No autocorrelation):** Các sai số ngẫu nhiên giữa các quan sát khác nhau không có tương quan với nhau: $\text{Cov}(\varepsilon_i, \varepsilon_j) = 0$ với mọi $i \neq j$.
3. **Phương sai sai số đồng nhất (Homoscedasticity):** Phương sai của sai số ngẫu nhiên là hằng số cố định tại mọi mức giá trị của các biến độc lập: $\text{Var}(\varepsilon_i \mid \mathbf{X}) = \sigma^2$ với mọi $i$.
4. **Phân phối chuẩn của sai số (Normality of residuals):** Sai số ngẫu nhiên có phân phối chuẩn với kỳ vọng bằng 0: $\varepsilon_i \sim \mathcal{N}(0, \sigma^2)$. Giả định này là điều kiện cần để các kiểm định suy luận thống kê ($t\text{-test}$, $F\text{-test}$) và khoảng tin cậy của hệ số hồi quy có giá trị chính xác trên mẫu hữu hạn.
5. **Không có hiện tượng đa cộng tuyến hoàn hảo hoặc nghiêm trọng (No multicollinearity):** Không có mối quan hệ tuyến tính hoàn hảo giữa bất kỳ hai hay nhiều biến độc lập nào ($\text{rank}(\mathbf{X}) = k + 1$).

---

## 5.2. Thiết lập bài toán hồi quy (Regression Problem Formulation)

Phần này đóng vai trò là **Bản thiết kế phương pháp luận** (Feature Candidate Sheet & Formulation Protocol). Toàn bộ các quyết định toán học và kỹ thuật được thiết lập dưới đây xuất phát trực tiếp từ các phát hiện thực nghiệm ở Chương 1 (EDA), Chương 2 (Phân phối xác suất) và Chương 4 (Tương quan), làm cơ sở chuẩn xác cho việc thi công mô hình thực chiến ở Chương 6.

### 5.2.1. Xác định bài toán và lý do lựa chọn mô hình MLR
- **Phát biểu bài toán:** Xây dựng mô hình thống kê định lượng dự báo tổng số lượt thuê xe đạp theo giờ (`cnt`) dựa trên các nhóm yếu tố thời gian, nhịp sinh hoạt xã hội và điều kiện thời tiết tại Washington D.C.
- **Lý do lựa chọn MLR:**
  1. *Tính minh bạch và khả năng diễn giải cao (Interpretability):* Khác với các thuật toán hộp đen (Black-box models), MLR cho phép bóc tách và định lượng chính xác tác động biên của từng yếu tố môi trường (nhiệt độ, độ ẩm, sức gió) lên nhu cầu đi lại trong điều kiện các yếu tố khác không đổi.
  2. *Đóng vai trò mô hình mốc đối chứng (Baseline Benchmark):* Trong khoa học dữ liệu, MLR là chuẩn mực bắt buộc phải được thiết lập trước tiên để đo lường mức độ cải thiện hiệu năng trước khi cân nhắc các mô hình phi tuyến phức tạp hơn.

---

### 5.2.2. Cơ sở lý luận chuyển đổi biến mục tiêu sang Bán Logarit (Log-linear Model)

#### 1. Dẫn chứng thực nghiệm từ Chương 1 và Chương 2
- Ở **Chương 1 (EDA)** và **Chương 2 (Phân phối xác suất)**, các kiểm định thực nghiệm đã chỉ ra:
  + Biến mục tiêu gốc `cnt` có phân phối lệch phải rất mạnh ($\text{Skewness} = 1.277, \text{Kurtosis} = 1.417$).
  + Dữ liệu xuất hiện hiện tượng phân tán vượt mức cực kỳ nghiêm trọng: Phương sai mẫu $\sigma^2 \approx 32,900$ gấp gần $173$ lần giá trị trung bình $\mu \approx 189.46$ ($\sigma^2 \gg \mu$).
  + Dữ liệu bị chặn cứng phía dưới tại 0 ($cnt \ge 0$, không tồn tại số lượt thuê âm).

#### 2. Nguy cơ toán học nếu sử dụng mô hình OLS trực tiếp trên biến $cnt$ thô
Nếu thiết lập bài toán hồi quy tuyến tính cộng tính trực tiếp trên biến thô: $\text{cnt} = \beta_0 + \sum \beta_j X_j + \varepsilon$, mô hình chắc chắn sẽ gặp phải hai sai sót nghiêm trọng:
1. *Dự báo ra số lượng âm vô lý:* Vào các khung giờ đêm muộn (01:00 – 04:00) hoặc những ngày thời tiết cực đoan (mưa tuyết, rét buốt), phương trình tuyến tính cộng tính sẽ trừ liên tiếp các hệ số âm và cho ra kết quả dự báo $\widehat{\text{cnt}} < 0$, hoàn toàn vi phạm bản chất vật lý của dữ liệu đếm.
2. *Vi phạm nghiêm trọng giả định phương sai đồng nhất (Homoscedasticity):* Khi $cnt$ lớn, độ phân tán của phần dư thực tế cũng tăng vọt theo kỳ vọng, dẫn đến hiện tượng phương sai thay đổi (Heteroscedasticity). Hậu quả là sai số chuẩn OLS bị sai lệch, khiến các kiểm định $t$ và khoảng tin cậy không còn đáng tin cậy.

#### 3. Thiết lập phương trình Bán Logarit (Semi-log / Log-linear)
Để khắc phục triệt để các hạn chế trên, nghiên cứu quyết định biến đổi biến mục tiêu thông qua hàm logarit tự nhiên:
$$Y = \ln(1 + \text{cnt})$$
*(Sử dụng phép cộng 1 để xử lý các quan sát có $cnt = 0$ nếu có, đảm bảo hàm logarit xác định trên toàn miền).*

Phương trình hồi quy tổng thể chính thức được thiết lập dưới dạng:
$$\ln(1 + \text{cnt}_i) = \beta_0 + \sum_{j=1}^k \beta_j X_{ji} + \varepsilon_i$$

**Quy tắc diễn giải hệ số:**  
Trong mô hình Bán Logarit, hệ số $\beta_j$ mang ý nghĩa phần trăm thay đổi tương đối: Khi biến độc lập $X_j$ tăng thêm 1 đơn vị, giá trị kỳ vọng của số lượt thuê xe sẽ thay đổi một lượng ước tính là:
$$\% \Delta \text{cnt} \approx (\exp(\beta_j) - 1) \times 100\%$$
Khi $\beta_j$ nhỏ ($|\beta_j| < 0.1$), mức thay đổi xấp xỉ bằng $\beta_j \times 100\%$.

**Quy tắc nghịch đảo về thang đo thực tế:**  
Mọi giá trị dự báo $\hat{Y}$ thu được từ mô hình hồi quy đều được nghịch đảo về thang đo số lượt thuê xe thực tế trước khi tính toán các chỉ số kiểm tra sai số (MAE, RMSE) theo công thức:
$$\widehat{\text{cnt}} = \exp(\hat{Y}) - 1$$
Nhờ hàm mũ $\exp(\cdot)$, giá trị dự báo $\widehat{\text{cnt}}$ luôn đảm bảo không âm ($\ge -1$, làm tròn $\ge 0$), triệt tiêu hoàn toàn lỗi dự báo số âm.

---

### 5.2.3. Cơ sở lý luận lựa chọn và xử lý biến giải thích (Feature Candidates Specification)

Dựa trên kết quả khám phá tại Chương 4, nghiên cứu đặc tả quy tắc lựa chọn và tiền xử lý cho từng nhóm biến giải thích:

#### 1. Loại bỏ các biến gây rủi ro mô hình
- **Loại bỏ `atemp` (Nhiệt độ cảm nhận):** Hệ số tương quan giữa `temp` và `atemp` đạt tới $r = 0.9877$ (theo Chương 4). Việc giữ lại cả hai biến sẽ gây ra hiện tượng đa cộng tuyến nghiêm trọng, làm phương sai của các ước lượng hệ số bùng nổ (VIF tăng vọt), đảo lộn dấu và mất ý nghĩa thống kê của hệ số. Do đó, chỉ giữ lại `temp`.
- **Loại bỏ `casual` và `registered`:** Hai biến này cộng lại bằng chính `cnt` ($\text{cnt} = \text{casual} + \text{registered}$). Đưa hai biến này vào mô hình dự báo `cnt` là hành vi rò rỉ dữ liệu (Data Leakage) nghiêm trọng, biến mô hình thành phép cộng đồng nhất thức tầm thường và mất giá trị dự báo thực tế.
- **Loại bỏ `instant` và `dteday`:** Các biến định danh chuỗi và ngày tháng thô được thay thế bằng các đặc trưng chu kỳ có ý nghĩa kinh tế - xã hội.

#### 2. Kỹ thuật điều hòa Fourier và Biến tương tác cho nhịp giờ (`hr`)
- **Vấn đề thực tiễn từ Hình 4.2 (Chương 4):** Quan hệ giữa `hr` và `cnt` là quan hệ phi tuyến chu kỳ mạnh mẽ. Ngày làm việc có **hai đỉnh nhọn** (08:00 và 17:00), trong khi ngày nghỉ chỉ có **một đỉnh vòm** (13:00 – 14:00). Nếu đưa `hr` vào mô hình dưới dạng số tuyến tính bậc 1, hệ số sẽ bị san phẳng và dự báo hoàn toàn sai lệch hình thái nhu cầu.
- **Giải pháp xấp xỉ điều hòa Fourier (Trigonometric Harmonics):**  
  Để bảo toàn giả định quan hệ tuyến tính của OLS trong không gian đặc trưng mới và giữ tính khép kín của vòng tròn thời gian (23:00 liền kề 00:00), biến `hr` được phân tích thành chuỗi điều hòa Fourier bậc $K=5$ gồm 5 cặp hàm lượng giác sin và cos:
  $$\text{hr\_sin}_k = \sin\left(\frac{2\pi k \cdot \text{hr}}{24}\right), \quad \text{hr\_cos}_k = \cos\left(\frac{2\pi k \cdot \text{hr}}{24}\right) \quad (k = 1, \dots, 5)$$
  Việc sử dụng 5 bậc hài lượng giác cho phép hàm tuyến tính tổng hợp tạo ra các điểm uốn phức tạp, mô phỏng chính xác cả hai đỉnh nhọn sáng và chiều.
- **Giải pháp biến tương tác bậc cao (`hr` × `workingday`):**  
  Để mô hình có thể linh hoạt chuyển đổi giữa hai kiểu dáng đường cong (hai đỉnh ngày làm việc vs một đỉnh ngày nghỉ), toàn bộ 5 cặp hài Fourier của giờ được nhân tương tác với biến nhị phân `workingday`:
  $$\text{Interaction}_k = \text{hr\_sin}_k \times \text{workingday}, \quad \text{hr\_cos}_k \times \text{workingday} \quad (k = 1, \dots, 5)$$

#### 3. Các biến thời gian và mùa vụ khác
- **Chu kỳ tháng trong năm:** Biến tháng `mnth` được mã hóa thành 1 cặp sóng chu kỳ 12 tháng: $\sin(2\pi \cdot \text{mnth} / 12)$ và $\cos(2\pi \cdot \text{mnth} / 12)$, bảo đảm tháng 12 liền kề tháng 1 trên chu kỳ thời tiết.
- **Biến loại ngày:** `workingday` (nhị phân 0/1) và `holiday` (nhị phân 0/1) để nắm bắt đặc tính di chuyển ngày lễ.
- **Biến xu hướng tăng trưởng dài hạn:** Biến năm `yr` (0: 2011, 1: 2012) đóng vai trò là biến xu hướng điều chỉnh bước nhảy tăng trưởng nhu cầu của hệ thống xe đạp qua hai năm vận hành.

#### 4. Các biến điều kiện thời tiết
- **Biến liên tục:** `temp`, `hum`, `windspeed` giữ nguyên giá trị chuẩn hóa trên đoạn $[0, 1]$ phản ánh liên tục tác động của môi trường.
- **Biến phân loại điều kiện thời tiết (`weathersit`):** Được mã hóa thành các biến giả (dummy variables) với nhóm cơ sở là `weathersit = 1` (Thời tiết đẹp: trời quang đãng, mây rải rác). Do mức thời tiết cực đoan (`weathersit = 4`: Mưa to, bão tuyết) chỉ xuất hiện 3 lần trong toàn bộ 17,379 quan sát, mức 4 được gộp chung với mức 3 tạo thành biến giả `weathersit_3_4` (Thời tiết xấu) và biến giả `weathersit_2` (Thời tiết sương mù, nhiều mây).

---

### 5.2.4. Cơ sở phương pháp luận phân chia dữ liệu (Chronological & Day-level Split Protocol)

#### 1. Nhược điểm chí tử của phân chia ngẫu nhiên thuần túy (Random Split)
Trong các bài toán dữ liệu bảng thông thường, việc chia ngẫu nhiên thuần túy (Random Train/Test Split) theo tỷ lệ 80/20 là phổ biến. Tuy nhiên, đối với bộ dữ liệu Bike Sharing mang đặc tính chuỗi thời gian (Time-series nature):
- Dữ liệu ghi nhận tuần tự theo từng giờ liên tiếp, có tự tương quan chuỗi rất cao ($r_1 = 0.8431$). Nếu chia ngẫu nhiên từng dòng, các giờ $t-1$ và $t+1$ sẽ nằm ở tập huấn luyện trong khi giờ $t$ nằm ở tập kiểm tra. Mô hình OLS khi đó thực chất chỉ thực hiện phép "nội suy điểm lân cận" (interpolation) thay vì dự báo thực sự.
- Gây ra hiện tượng rò rỉ thông tin tương lai về quá khứ (Look-ahead bias / Temporal data leakage). Chỉ số $R^2$ thu được trên tập test ngẫu nhiên sẽ cao ảo nhưng mô hình sẽ thất bại khi triển khai trong thực tế.

#### 2. Chiến lược phân chia hai tầng: Điểm cắt thời gian kết hợp Trộn ngẫu nhiên theo ngày (Day-level Post-split)
Để giải quyết hài hòa giữa yêu cầu ngoại suy tương lai và nhu cầu tinh chỉnh mô hình độc lập, nghiên cứu thiết lập chiến lược phân chia hai tầng:

1. **Tầng 1 — Phân chia theo mốc thời gian cố định (Chronological Cutoff at 31/03/2012):**
   - **Tập huấn luyện (Train Set):** Toàn bộ dữ liệu từ ngày **01/01/2011 đến ngày 31/03/2012** (Gồm $10,821$ dòng, chiếm $62.26\%$ dữ liệu; mức `cnt` trung bình đạt $148.59$ lượt/giờ). Mốc này bảo đảm mô hình học được toàn bộ chu kỳ 4 mùa của năm 2011 và một quý đầu năm 2012 để nhận diện bước nhảy tăng trưởng của biến xu hướng `yr`.

2. **Tầng 2 — Phân bổ ngẫu nhiên theo cấp độ Ngày cho giai đoạn tương lai (Day-level Shuffled Split, `SEED = 42`):**
   Giai đoạn sau điểm cắt (từ ngày 01/04/2012 đến 31/12/2012, gồm $6,558$ dòng) là dữ liệu hoàn toàn thuộc tương lai so với tập huấn luyện, có mức nhu cầu trung bình tăng vọt lên trên $256$ lượt/giờ (tăng hơn $72\%$). Để phục vụ vừa chọn cấu hình mô hình vừa đánh giá khách quan, phần dữ liệu này được phân bổ ngẫu nhiên theo **từng ngày nguyên vẹn (Day-level)** thành 2 tập (tỷ lệ xấp xỉ 50/50):
   - **Tập kiểm định (Validation Set — điểm màu tím trên Hình 6.2):** Gồm $3,286$ dòng ($18.91\%$ dữ liệu; `cnt` trung bình $= 256.46$ lượt/giờ), được dùng để dò tìm siêu tham số tối ưu (chọn số bậc hài Fourier $K$, hình thức biến đổi target, cách thức mô hình hóa mùa vụ).
   - **Tập kiểm tra (Test Set — điểm màu cam trên Hình 6.2):** Gồm $3,272$ dòng ($18.83\%$ dữ liệu; `cnt` trung bình $= 257.36$ lượt/giờ), hoàn toàn được giữ kín trong quá trình thử nghiệm và chỉ dùng đúng một lần để báo cáo năng lực dự báo thực chiến cuối cùng.

**Ý nghĩa khoa học của cơ chế trộn theo ngày (Day-level Split):**
- **Tránh rò rỉ tương quan giờ:** Bằng cách gộp trọn vẹn cả 24 giờ của một ngày vào cùng một tập, phương pháp loại trừ hoàn toàn hiện tượng rò rỉ thông tin giữa các giờ liền kề.
- **Cân bằng mùa vụ:** Cả tập Kiểm định và Kiểm tra đều có các ngày trải đều từ tháng 4 đến tháng 12 năm 2012 (mùa hè, mùa thu, mùa đông), bảo đảm đánh giá công bằng cấu hình mô hình mà không bị thiên lệch mùa.
- **Bảo toàn năng lực ngoại suy:** Cả hai tập đều nằm 100% ở tương lai sau thời điểm huấn luyện, buộc mô hình phải ngoại suy xu hướng tăng trưởng của năm 2012.

---

### 5.2.5. Khung phương pháp luận kiểm định giả định mô hình (Assumptions Verification Roadmap)

Để đảm bảo kết quả hồi quy OLS đáng tin cậy và không vi phạm Định lý Gauss-Markov, Chương 6 bắt buộc phải triển khai một quy trình kiểm định chẩn đoán nghiêm ngặt gồm 4 bước:

1. **Kiểm định tính độc lập của sai số (Tự tương quan chuỗi):**
   - *Công cụ:* Thống kê Durbin–Watson ($DW$).
   - *Tiêu chuẩn:* Giá trị $DW \approx 2.0$ thể hiện không có tự tương quan bậc nhất. Nếu $DW < 1.5$, phần dư có tự tương quan dương chuỗi thời gian, đòi hỏi phải thảo luận về ảnh hưởng làm thu hẹp nhân tạo sai số chuẩn OLS.
2. **Kiểm định phương sai sai số đồng nhất (Homoscedasticity):**
   - *Công cụ:* Kiểm định Breusch–Pagan (LM test).
   - *Giả thuyết:* $H_0$: Phương sai sai số ngẫu nhiên là hằng số không đổi ($\sigma_i^2 = \sigma^2$). Bác bỏ $H_0$ nếu $p\text{-value} < 0.05$.
3. **Kiểm định phân phối chuẩn của phần dư:**
   - *Công cụ:* Đo lường hệ số bất đối xứng (Skewness) và hệ số độ nhọn (Kurtosis) của phần dư chuẩn hóa.
   - *Tiêu chuẩn:* Phân phối chuẩn lý tưởng có $\text{Skewness} = 0$ và $\text{Kurtosis} = 3$ (hoặc Excess Kurtosis $= 0$).
4. **Kiểm tra hiện tượng đa cộng tuyến (Multicollinearity):**
   - *Công cụ:* Hệ số phóng đại phương sai (Variance Inflation Factor – VIF):
     $$\text{VIF}_j = \frac{1}{1 - R_j^2}$$
     với $R_j^2$ là hệ số xác định khi hồi quy biến $X_j$ theo tất cả các biến độc lập còn lại.
   - *Tiêu chuẩn:* Ngưỡng an toàn thực nghiệm là $\text{VIF} < 5$ hoặc $\text{VIF} < 10$. Các biến có $\text{VIF} > 10$ được coi là có đa cộng tuyến nghiêm trọng.

---

## 5.3. Kết luận và hạn chế lý thuyết của Phần 5

### 5.3.1. Kết luận chương 5
1. Chương 5 đã thiết lập hoàn chỉnh khung lý thuyết Hồi quy tuyến tính Đa biến (MLR) chuẩn mực, làm rõ ý nghĩa các hệ số OLS, các thước đo độ phù hợp ($R^2, \bar{R}^2, \text{MAE}, \text{RMSE}$) và 5 giả định cổ điển Gauss-Markov.
2. Dựa trên các phát hiện thực nghiệm từ các chương trước, bài toán hồi quy được thiết lập một cách khoa học: chuyển đổi biến mục tiêu sang dạng Bán Logarit $\ln(1 + \text{cnt})$ để bảo đảm tính không âm và ổn định phương sai; loại trừ triệt để biến đa cộng tuyến `atemp` và biến rò rỉ dữ liệu `casual/registered`; đề xuất giải pháp chuỗi điều hòa Fourier và biến tương tác `hr * workingday` để bắt trọn tính phi tuyến hai đỉnh; và xác lập chiến lược chia dữ liệu theo thời gian cắt mốc 31/03/2012.

### 5.3.2. Hạn chế lý thuyết
1. **Giả định tuyến tính trong không gian đặc trưng biến đổi:** Dù các kỹ thuật lượng giác hóa và logarit hóa đã giúp tuyến tính hóa cấu trúc bài toán, bản chất mô hình OLS vẫn là sự kết hợp cộng tính của các tham số. Mô hình có thể gặp khó khăn khi phản ánh những hiệu ứng phi tuyến bậc cao đột biến tại các giá trị cực biên (như các đợt bão tuyết hoặc các sự kiện lễ hội quy mô lớn ngoài dự kiến).
2. **Thách thức của hiện tượng tự tương quan chuỗi thời gian:** Do bản chất dữ liệu theo giờ có sự phụ thuộc chuỗi liên tục, mô hình OLS cơ bản chắc chắn sẽ đối mặt với nguy cơ vi phạm giả định sai số độc lập ($DW < 1.5$), đòi hỏi Chương 6 phải tiến hành chẩn đoán phần dư thực nghiệm chi tiết và đưa ra các khuyến nghị hiệu chỉnh thận trọng.
