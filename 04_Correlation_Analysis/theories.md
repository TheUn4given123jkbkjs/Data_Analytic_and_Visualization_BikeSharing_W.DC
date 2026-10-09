# CHƯƠNG 4. Phân tích tương quan giữa các biến

## 4.1. Lý thuyết 

### 4.1.1. Phân tích tương quan Pearson ($r$) - Quan hệ tuyến tính

**Định nghĩa:**

Hệ số tương quan Pearson được dùng để đo lường mức độ và chiều hướng của mối quan hệ **tương quan tuyến tính** (linear relationship) giữa hai biến định lượng.
Hệ số Pearson được tính bằng cách chia **hiệp phương sai** (covariance) của hai biến định lượng cho tích **độ lệch chuẩn** (standard deviation) của từng biến.

**Ý nghĩa:**

Hệ số tương quan Pearson nằm trong khoảng: $$-1 \leq r \leq 1$$

Với:

- $r < 0$: quan hệ tương quan tuyến tính **âm**
- $r > 0$: quan hệ tương quan tuyến tính **dương**
- $r \approx 0$: **Không có hoặc rất ít** tương quan tuyến tính
- $|r|$ càng **gần 1** -> Mối quan hệ càng **mạnh**
- $|r|$ càng **gần 0** -> Mối quan hệ càng **yếu**

**Công thức tính:**
$$r = \frac{\sum(x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum(x_i - \bar{x})^2 \sum(y_i - \bar{y})^2}}$$

Với:

- $x_i, y_i$ là giá trị quan sát thứ i của X và Y.
- $\bar{x}, \bar{y}$ lần lượt là giá trị trung bình của biến X và biến Y.

**Điều kiện áp dụng:**
- Biến định lượng: Pearson phù hợp để đánh giá mối quan hệ giữa hai biến định lượng.
- Quan hệ tuyến tính: Pearson đo lường mối quan hệ tuyến tính, do đó nên kiểm tra scatter plot trước khi sử dụng.
- Không có outlier nghiêm trọng: Pearson khá nhạy cảm với các giá trị ngoại lệ (outliers), vì vậy outlier có thể làm thay đổi đáng kể hệ số $r$.
- Phân phối dữ liệu: Phân phối chuẩn không phải điều kiện bắt buộc để tính $r$, nhưng thường được xem xét khi thực hiện các kiểm định suy luận dựa trên Pearson.

### 4.1.2. Phân tích tương quan Spearman ($\rho$ hoặc $r_s$) - Quan hệ đơn điệu & thứ bậc

**Định nghĩa:**
Hệ số tương quan Spearman ($\rho$ hoặc $r_s$) là một phương pháp tương quan phi tham số (non-parametric), dùng để đo lường mức độ và chiều hướng của mối quan hệ đơn điệu (monotonic relationship) giữa hai biến.

Thay vì sử dụng giá trị thực tế của dữ liệu như Pearson, Spearman chuyển đổi các giá trị quan sát thành thứ hạng (rank), sau đó đánh giá mức độ và chiều hướng tương quan giữa các thứ hạng.

**Ý nghĩa:**

Giống như Pearson, hệ số tương quan Spearman cũng nằm trong khoảng: $$-1 \leq \rho \leq 1$$

Với:
- $\rho < 0$: quan hệ tương quan đơn điệu **âm**
- $\rho > 0$: quan hệ tương quan đơn điệu **dương**
- $\rho \approx 0$: **Không có hoặc rất ít** tương quan đơn điệu
- $|\rho|$ càng **gần 1** -> Mối quan hệ càng **mạnh**
- $|\rho|$ càng **gần 0** -> Mối quan hệ càng **yếu**

**Công thức tính:**

Khi không có tied ranks, có thể sử dụng công thức dựa trên sự chênh lệch thứ hạng $d_i$.

$$\rho = 1 - \frac{6\sum{d_i^2}}{n(n^2 - 1)}$$

Với:
- $d_i = \text{rg}(x_i) - \text{rg}(y_i)$ là sự chênh lệch giữa thứ hạng của $x_i$ và $y_i$
- $n$ là tổng số lượng quan sát.

Khi dữ liệu có tied ranks, hệ số Spearman có thể được tính bằng cách áp dụng công thức tương quan Pearson trên các thứ hạng của dữ liệu.

$$\rho = \frac{\sum_{i=1}^{n} (R(x_i) - \bar{R}_x)(R(y_i) - \bar{R}_y)}{\sqrt{\sum_{i=1}^{n} (R(x_i) - \bar{R}_x)^2 \sum_{i=1}^{n} (R(y_i) - \bar{R}_y)^2}}$$

Với:
- $R(x_i), R(y_i)$ là thứ hạng (rank) của các quan sát $x_i$ và $y_i$.
- $\bar{R}_x, \bar{R}_y$ là thứ hạng trung bình của tập $X$ và $Y$.

**Điều kiện áp dụng:**
- Loại dữ liệu linh hoạt: Thích hợp cho cả biến định lượng liên tục và biến thứ bậc (ordinal variables)
- Mối quan hệ đơn điệu: Mối quan hệ giữa hai biến không bắt buộc phải là đường thẳng, chỉ cần tăng hoặc giảm đồng điệu.
- Không yêu cầu phân phối chuẩn: Phù hợp với dữ liệu bị lệch (skewed) hoặc không tuân theo phân phối chuẩn.
- Ít bị ảnh hưởng bởi ngoại lai (Outliers): Nhờ cơ chế chuyển sang thứ hạng (rank), Spearman thường ít nhạy cảm với ngoại lai hơn Pearson.

### 4.1.3. So sánh Pearson và Spearman

| Đặc điểm | Pearson | Spearman |
| --- | --- | --- |
| Đo lường | Tuyến tính | Đơn điệu |
| Dữ liệu sử dụng | Giá trị gốc | Thứ hạng |
| Nhạy với ngoại lai | Cao hơn | Thường thấp hơn |
| Bắt quan hệ phi tuyến đơn điệu | Không tốt | Tốt hơn |
| Phù hợp khi | Quan hệ gần tuyến tính | Quan hệ đơn điệu nhưng có thể phi tuyến |

### 4.1.4. Trường hợp mà kết quả Pearson và Spearman khác nhau:
1. **Ngoại lai:** Một vài điểm cực đoan có thể kéo Pearson lên/xuống mạnh hơn Spearman.

2. **Quan hệ phi tuyến nhưng đơn điệu:** Spearman vẫn có thể cao trong khi Pearson không nhất thiết cao tương ứng. VD: 
$$Y = X^2, X > 0$$

3. **Quan hệ không đơn điệu:** Ở đây cả Pearson và Spearman đều có thể không phản ánh tốt cấu trúc quan hệ. VD: 
$$Y=X^2,\quad X\in[-1,1]$$

---

# THE REST IS IN THE IPYNB FILE

## 4.2. Áp dụng tính hệ số tương quan Pearson và Spearman giữa các biến số trong bộ dữ liệu đã chọn.

## 4.3. Sử dụng biểu đồ phù hợp để trực quan hóa mối quan hệ giữa các biến.

## 4.4. Đưa ra nhận xét về ý nghĩa thực tiễn của các mối tương quan.