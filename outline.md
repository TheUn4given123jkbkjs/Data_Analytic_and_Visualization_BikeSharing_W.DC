Được. Nếu bản này để **cả nhóm cùng đọc và cùng thống nhất hướng làm**, anh nghĩ không nên viết quá chi tiết ở mức công thức/test ngay từ đầu. Nên giữ một **outline data-driven**, trong đó những thứ chưa biết sau EDA thì đánh dấu là **sẽ quyết định dựa trên dữ liệu**.

Dưới đây là bản tổng quan có thể dùng làm **khung chung của nhóm**.

# Outline báo cáo cuối kỳ — Bike Sharing Dataset

## 0. Giới thiệu đề tài và Abstract

### 0.1. Giới thiệu đề tài

* Bối cảnh bài toán Bike Sharing.
* Giới thiệu bộ dữ liệu.
* Mục tiêu phân tích.
* Phạm vi phân tích.

### 0.2. Abstract

* Dataset và mục tiêu.
* Phương pháp phân tích.
* Phát hiện chính.
* Kết luận chính.

> Abstract sẽ được hoàn thiện sau khi toàn bộ phân tích kết thúc.

---

# 1. Khám phá dữ liệu — EDA

## 1.1. Tổng quan dữ liệu

* Nguồn dữ liệu.
* Số lượng bản ghi.
* Số lượng biến.
* Kiểu dữ liệu.
* Ý nghĩa các biến.
* Phân loại biến:

  * Numerical
  * Categorical
  * Date/Time

### 1.1.1. Kiểm tra chất lượng dữ liệu

* Missing values.
* Duplicate records.
* Giá trị bất hợp lệ nếu có.

### 1.1.2. Tiền xử lý dữ liệu

* Xử lý missing.
* Xử lý duplicate.
* Chuyển đổi kiểu dữ liệu nếu cần.
* Chuẩn hóa định dạng thời gian nếu cần.

> **Không quyết định phương pháp xử lý trước khi kiểm tra dữ liệu.**

---

## 1.2. Thống kê mô tả

### 1.2.1. Thống kê các biến số

Tính các thống kê phù hợp:

* Mean
* Median
* Standard deviation
* Min / Max
* Q1 / Q3
* IQR

Tập trung vào những biến có ý nghĩa đối với bài toán, đặc biệt là biến mục tiêu và các biến số có khả năng giải thích nó.

### 1.2.2. Trực quan hóa

Sử dụng các biểu đồ phù hợp với **đặc điểm thực tế của dữ liệu**, có thể gồm:

* Histogram
* Boxplot
* Bar chart
* Line chart
* Scatter plot

Mỗi biểu đồ cần trả lời:

> **Biểu đồ này được chọn để tìm hiểu điều gì?**

Sau đó:

> **Dữ liệu thực tế cho thấy điều gì?**

---

## 1.3. Phát hiện và xử lý ngoại lai

### 1.3.1. Phát hiện

Có thể sử dụng:

* IQR.
* Z-score.
* Boxplot.
* Phân tích trực quan.

### 1.3.2. Đánh giá và xử lý

Không mặc định xóa outlier.

Phân biệt:

```text
Statistical outlier
        ≠
Data error
```

Nếu một ngày có lượng thuê cực cao nhưng đó là một quan sát thực tế hợp lệ, có thể **giữ lại**.

Phương pháp cuối cùng sẽ được quyết định dựa trên kết quả kiểm tra dữ liệu.

---

## 1.4. Nhận xét tổng quan EDA

Tổng hợp các phát hiện quan trọng:

* Dữ liệu có đặc điểm gì?
* Biến mục tiêu phân bố như thế nào?
* Có xu hướng theo thời gian không?
* Các yếu tố thời tiết có biểu hiện quan hệ với nhu cầu thuê không?
* `hr`, `workingday`, `season`, `weathersit`... có biểu hiện khác biệt gì?
* Có vấn đề dữ liệu nào cần lưu ý cho các bước tiếp theo?

**Kết quả của EDA sẽ được dùng để định hướng các phân tích ở phần 2–6.**

---

# 2. Phân tích phân phối xác suất

Mục tiêu:

> Xác định đặc điểm phân phối của một số biến số quan trọng và xem dữ liệu có phù hợp với các phân phối xác suất giả định hay không.

## 2.1. Lựa chọn biến phân tích

Ban đầu có thể xem xét:

* `cnt`
* `temp`

Nhưng việc lựa chọn cuối cùng sẽ dựa trên EDA.

Các biến như:

* `hr`
* `workingday`
* `season`

có thể rất quan trọng đối với việc **giải thích `cnt`**, nhưng không nhất thiết là đối tượng phù hợp nhất để kiểm tra phân phối xác suất liên tục.

## 2.2. Phân tích phân phối biến 1

* Phân phối quan sát được.
* Visualization.
* Đặc điểm.
* Phân phối lý thuyết phù hợp nếu có.
* Nhận xét.

## 2.3. Phân tích phân phối biến 2

Tương tự.

## 2.4. Nhận xét

* Hai biến có đặc điểm phân phối gì?
* Có lệch không?
* Có gần Normal không?
* Phân phối quan sát được ảnh hưởng thế nào đến các bước phân tích tiếp theo?

---

# 3. Kiểm định giả thuyết

## 3.1. Lý thuyết các phương pháp kiểm định

### 3.1.1. t-test

### 3.1.2. Chi-square test

### 3.1.3. ANOVA

Trình bày:

* Mục đích.
* Khi nào sử dụng.
* H₀ / H₁.
* Thống kê kiểm định.
* p-value.
* Mức ý nghĩa.
* Cách diễn giải.

---

## 3.2. Xây dựng câu hỏi nghiên cứu

**Hai câu hỏi sẽ được lựa chọn sau EDA.**

Tiêu chí:

* Có ý nghĩa với bài toán Bike Sharing.
* Có thể kiểm định bằng dữ liệu hiện có.
* Phù hợp với một trong các phương pháp yêu cầu.
* Không trùng với câu hỏi của correlation/regression.
* Có khả năng giải thích rõ ràng trong báo cáo.

### 3.2.1. Research Question 1

```text
Research Question
       ↓
Variables
       ↓
H₀ / H₁
       ↓
Chọn statistical test
       ↓
p-value / CI
       ↓
Kết luận
```

### 3.2.2. Research Question 2

Tương tự.

> **Không chốt test trước rồi mới tìm câu hỏi.**
> Câu hỏi → đặc điểm biến → phương pháp kiểm định phù hợp.

---

# 4. Phân tích tương quan

## 4.1. Lý thuyết

### 4.1.1. Pearson

* Ý nghĩa.
* Đo quan hệ tuyến tính.
* Hệ số tương quan.

### 4.1.2. Spearman

* Ý nghĩa.
* Quan hệ đơn điệu.
* Rank correlation.

### 4.1.3. Pearson vs Spearman

So sánh:

* Khi nào sử dụng.
* Khác biệt trong diễn giải.
* Trường hợp hai phương pháp cho kết quả khác nhau.

---

## 4.2. Phân tích tương quan trên dữ liệu

Không nhất thiết phân tích mọi cặp biến.

Lựa chọn các biến số dựa trên:

* EDA.
* Ý nghĩa thực tế.
* Mối quan hệ với biến mục tiêu.
* Kết quả phân phối.

Áp dụng:

* Pearson.
* Spearman.

---

## 4.3. Trực quan hóa

Có thể sử dụng:

* Correlation heatmap.
* Scatter plot.
* Regression line nếu phù hợp.

Việc chọn biểu đồ sẽ dựa trên câu hỏi cần trả lời.

---

## 4.4. Ý nghĩa thực tiễn

Phân tích:

* Quan hệ dương/âm.
* Mạnh/yếu.
* Tuyến tính/đơn điệu.
* Những mối quan hệ đáng chú ý.

Đồng thời phân biệt:

> **Correlation không chứng minh causation.**

---

# 5. Hồi quy tuyến tính đa biến

## 5.1. Lý thuyết

* Khái niệm Multiple Linear Regression.
* Biến phụ thuộc.
* Biến độc lập.
* Phương trình mô hình.
* Regression coefficients.
* R² / Adjusted R².
* Sai số.
* Các giả định của mô hình.

---

## 5.2. Xây dựng bài toán hồi quy

### 5.2.1. Xác định biến mục tiêu

Ứng viên trung tâm:

> `cnt`

Nhưng sẽ xác nhận sau khi hoàn thành EDA.

### 5.2.2. Lựa chọn biến độc lập

Các ứng viên có thể gồm:

* `temp`
* `hum`
* `windspeed`
* `hr`
* `workingday`
* `season`
* `weathersit`
* Các biến phù hợp khác.

**Không mặc định đưa tất cả vào model.**

Việc lựa chọn dựa trên:

```text
EDA
 ↓
Domain meaning
 ↓
Correlation
 ↓
Multicollinearity
 ↓
Regression assumptions
 ↓
Final features
```

---

# 6. Xây dựng và đánh giá mô hình

## 6.1. Feature Engineering

Tùy dữ liệu thực tế:

* Encoding categorical variables.
* Xử lý date/time.
* Tạo biến mới nếu có cơ sở.
* Kiểm tra multicollinearity.
* Feature selection.
* Transformation nếu cần.

---

## 6.2. Chiến lược chia dữ liệu

Xác định cách:

* Training set.
* Test set.

Vì Bike Sharing có yếu tố thời gian, cần cân nhắc:

> Random split hay chronological split?

Việc lựa chọn phải dựa trên **mục tiêu của mô hình**, không chọn chỉ vì đó là cách phổ biến.

---

## 6.3. Huấn luyện mô hình

* Fit Multiple Linear Regression.
* Ước lượng coefficients.
* Phân tích statistical significance nếu phù hợp.

---

## 6.4. Đánh giá mô hình

Các chỉ số có thể gồm:

* R².
* Adjusted R².
* MAE.
* RMSE.

### Kiểm tra assumptions

* Linearity.
* Independence.
* Homoscedasticity.
* Residuals.
* Multicollinearity.

---

## 6.5. Nhận xét kết quả

---

# 7. Kết luận tổng quát

Báo cáo cuối cùng cần trả lời được:

### 7.1. EDA

> Dữ liệu Bike Sharing có những đặc điểm nổi bật nào?

### 7.2. Distribution

> Các biến được lựa chọn có phân phối như thế nào?

### 7.3. Hypothesis Testing

> Hai câu hỏi nghiên cứu được kiểm định cho kết quả gì?

> Có đủ bằng chứng thống kê để bác bỏ H₀ hay không?

### 7.4. Correlation

> Các biến số có quan hệ như thế nào với nhau và với `cnt`?

### 7.5. Regression

> Khi xét đồng thời nhiều biến, những biến nào có vai trò đáng chú ý trong việc giải thích/dự đoán `cnt`?

### 7.6. Hạn chế

* Giới hạn của dataset.
* Giới hạn của sampling/data collection nếu có.
* Correlation không chứng minh causation.
* Các giả định của statistical tests.
* Các giả định của linear regression.
* Temporal effects.
* Những biến quan trọng có thể chưa được quan sát.

---

# Logic tổng thể của bài

Điểm quan trọng nhất để cả nhóm thống nhất là **không coi đây là 7 phần độc lập**.

```text
                 BIKE SHARING DATA
                        │
                        ▼
                       EDA
                        │
             "Dữ liệu thực sự có gì?"
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
   Distribution    Research Q.       Correlation
        │               │                │
        │               ▼                │
        │          Hypothesis            │
        │             Tests              │
        │               │                │
        └───────────────┼────────────────┘
                        ▼
                FEATURE SELECTION
                        │
                        ▼
              MULTIPLE REGRESSION
                        │
                        ▼
                   EVALUATION
                        │
                        ▼
                   CONCLUSION
```

### Nguyên tắc của nhóm

**EDA trước → phát hiện từ dữ liệu → đặt câu hỏi → chọn phương pháp → phân tích → kết luận.**
