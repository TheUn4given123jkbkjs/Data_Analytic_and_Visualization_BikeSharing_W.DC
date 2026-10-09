# CHƯƠNG 5. Hồi quy tuyến tính đa biến (MLR)

## 5.1. Lý thuyết

### 5.1.1. Khái niệm bài toán hồi quy tuyến tính đa biến


**Khái niệm:**

Hồi quy tuyến tính đa biến (Multiple Linear Regression - MLR) là một phương pháp thống kê dùng để mô hình hóa mối quan hệ tuyến tính giữa một biến phụ thuộc (biến mục tiêu) và hai hay nhiều biến độc lập (biến giải thích), với giả định rằng mối quan hệ giữa biến phụ thuộc và các biến độc lập có thể được biểu diễn bằng một hàm tuyến tính.

**Mục đích:**

- Đánh giá mức độ và chiều hướng tác động của từng biến độc lập lên biến mục tiêu (khi giữ nguyên giá trị của các biến độc lập khác).
- Ước tính giá trị của biến mục tiêu dựa trên giá trị của các biến độc lập đầu vào.
- Đánh giá mức độ phù hợp của mô hình với dữ liệu.

### 5.1.2. Khái niệm các thành phần của bài toán hồi quy tuyến tính đa biến

1. Biến phụ thuộc (Dependent Variable - $Y$): Là biến mục tiêu cần giải thích hoặc dự đoán.

2. Các biến độc lập (Independent Variables - $X_1, X_2, \dots, X_k$): Là các yếu tố dùng để giải thích sự thay đổi của $Y$.

3. Hệ số hồi quy (Regression Coefficients - $\beta_0, \beta_1, \dots, \beta_k$): Các tham số thể hiện mức độ tác động của từng biến độc lập lên $Y$.

4. Sai số ngẫu nhiên (Error - $\varepsilon$): Thành phần ngẫu nhiên trong mô hình, đại diện cho những yếu tố ảnh hưởng đến biến phụ thuộc nhưng không được mô hình giải thích.

5. Phần dư (Residual - $e_i$): Chênh lệch giữa giá trị quan sát thực tế và giá trị dự đoán từ mô hình, được tính bằng $e_i=Y_i-\hat Y_i$.

### 5.1.3. Phương trình mô hình

1. Phương trình tổng thể (Population Regression Function):

$$Y = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \dots + \beta_k X_k + \varepsilon$$

Trong đó:
- $Y$: biến phụ thuộc.
- $X_1, X_2, ..., X_k$: các biến độc lập.
- $\beta_0$: hệ số chặn (intercept).
- $\beta_1, \beta_2, ..., \beta_k$: các hệ số hồi quy.
- $\varepsilon$: sai số ngẫu nhiên (error term).


2. Phương trình ước lượng (Sample Regression Function):

$$\hat{Y} = b_0 + b_1 X_1 + b_2 X_2 + \dots + b_k X_k$$

Trong đó:
- $\hat{Y}$ (Y-hat): Giá trị dự đoán của biến phụ thuộc $Y$.
- $b_0$: Hệ số chặn (Intercept) — giá trị dự đoán của $Y$ khi tất cả các biến độc lập $X_i = 0$.
- $b_i$ ($i = 1, \dots, k$): Hệ số hồi quy riêng lẻ (Partial Regression Coefficients) — lượng thay đổi trung bình của $Y$ khi $X_i$ tăng thêm 1 đơn vị, với điều kiện giữ nguyên các biến độc lập khác (ceteris paribus).








### 5.1.4. Hệ số hồi quy

Hệ số $b_i$ cho biết mức thay đổi trung bình của biến phụ thuộc $Y$ khi biến độc lập $X_i$ tăng một đơn vị, trong khi các biến độc lập khác được giữ cố định.

Dấu của hệ số:
- $b_i>0$: quan hệ cùng chiều.
- $b_i<0$: quan hệ ngược chiều.
- $b_i\approx0$: ảnh hưởng tuyến tính của $X_i$ lên $Y$ tương đối nhỏ, khi giữ các biến khác cố định.

### 5.1.5. Hệ số xác định $R^2$

$R^2$ (R-squared) là hệ số xác định, dùng để đánh giá mức độ mà các biến độc lập trong mô hình giải thích được sự biến thiên của biến phụ thuộc.


$$R^2 = 1-\frac{SS_{Residual}}{SS_{Total}}$$

Trong đó:
- $SS_{Residual}$: tổng bình phương sai số.
- $SS_{Total}$: tổng bình phương độ lệch của các giá trị quan sát so với giá trị trung bình.
$R^2$ thường nằm trong khoảng:
$$0\leq R^2\leq1$$

Lưu ý: $R^2$ cao không đồng nghĩa với mô hình chắc chắn tốt hoặc có khả năng dự đoán tốt, vì cần xem xét thêm các giả định, ý nghĩa thống kê của mô hình, sai số dự đoán và các chỉ số đánh giá khác.

### 5.1.6. Adjusted $R^2$
Adjusted $R^2$ (R-squared hiệu chỉnh) là phiên bản điều chỉnh của $R^2$, có tính đến số lượng biến độc lập và kích thước mẫu.

Công thức:

$$Adjusted\ R^2 = 1-(1-R^2)\frac{n-1}{n-k-1}$$

Trong đó:
- $n$: số lượng quan sát.
- $k$: số lượng biến độc lập.
- $R^2$: hệ số xác định.

Điểm quan trọng: Khác với $R^2$, Adjusted $R^2$ không tự động tăng khi thêm biến độc lập vào mô hình. Nếu biến mới không cải thiện mô hình đủ đáng kể, Adjusted $R^2$ có thể giảm.

Vì vậy, trong hồi quy đa biến, Adjusted $R^2$ thường hữu ích hơn $R^2$ khi so sánh các mô hình có số lượng biến độc lập khác nhau.

### 5.1.7. Sai số và phần dư

**Sai số (Error)**

Trong mô hình lý thuyết:
$$Y_{i}=\beta _{0}+\beta _{1}X_{1i}+\beta _{2}X_{2i}+...+\beta _{k}X_{ki}+\varepsilon _{i}$$

$\varepsilon_i$ là sai số ngẫu nhiên, đại diện cho những yếu tố ảnh hưởng đến $Y$ nhưng không được đưa vào mô hình.

**Phần dư (Residual)**

Sau khi mô hình được ước lượng, ta không biết chính xác $\varepsilon_i$, mà tính được phần dư:

$$e_i=Y_i-\hat{Y}_i$$

Trong đó:
- $Y_i$: giá trị thực tế.
- $\hat{Y}_i$: giá trị dự đoán.
- $e_i$: phần dư.

### 5.1.8. Các giả định của hồi quy tuyến tính đa biến

Để mô hình hồi quy tuyến tính được ước lượng và diễn giải một cách đáng tin cậy, cần kiểm tra một số giả định quan trọng của mô hình. Năm giả định thường được xem xét gồm:

1. Tính tuyến tính (Linearity): Mối quan hệ giữa các biến độc lập $X$ và biến phụ thuộc $Y$ phải là quan hệ tuyến tính.

2. Tính độc lập của sai số (Independence of Errors): Các phần dư $e_i$ của các quan sát cần độc lập với nhau và không có tự tương quan.

3. Phương sai sai số không đổi (Homoscedasticity): Phương sai của phần dư được giả định là gần như không đổi đối với các mức giá trị dự đoán $\hat Y$.

4. Phân phối chuẩn của phần dư (Normality of Residuals): Phần dư $e_i$ được giả định có phân phối chuẩn với trung bình bằng 0.

5. Không có đa cộng tuyến nghiêm trọng: Các biến độc lập không có mối quan hệ tuyến tính quá mạnh gây ảnh hưởng đáng kể đến việc ước lượng các hệ số hồi quy.
