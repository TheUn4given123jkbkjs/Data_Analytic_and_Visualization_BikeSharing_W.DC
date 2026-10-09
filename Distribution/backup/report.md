# PHẦN 2. PHÂN TÍCH PHÂN PHỐI XÁC SUẤT

## 2.1. Giới thiệu

### 2.1.1. Bối cảnh và mục tiêu

Nhu cầu thuê xe đạp thay đổi theo giờ trong ngày, loại ngày và điều kiện thời tiết. Phần 1 đã cho thấy tổng lượt thuê theo giờ (`cnt`) có đuôi phải dài, trong khi `temp` và `hum` gần đối xứng hơn. Phần này tiếp tục kiểm tra hình dạng phân phối và mức độ phù hợp của một số phân phối lý thuyết trước khi nhóm lựa chọn phương pháp kiểm định, tương quan và mô hình hóa.

Bốn mục tiêu của phần này là:

1. Mô tả phân phối thực nghiệm của tổng lượt thuê (`cnt`).
2. Kiểm tra over-dispersion và so sánh Poisson, Negative Binomial, Normal và Log-normal cho `cnt`.
3. So sánh Normal và Beta cho `temp` và `hum` ở thang chuẩn hóa 0–1.
4. Mô tả sự khác nhau của phân phối `cnt` giữa ngày làm việc và ngày nghỉ để cung cấp ngữ cảnh cho Phần 3.

Các kết quả trong phần này là thống kê mô tả trên mẫu dữ liệu hiện có. Chúng không được dùng để kết luận quan hệ nhân quả.

### 2.1.2. Dữ liệu và biến phân tích

Phân tích sử dụng `EDA/cleaned_data/hour_cleaned.csv`, phiên bản dữ liệu đã được TV1 xử lý từ `hour.csv`. File gồm 17,379 dòng và 17 biến. Cột index kỹ thuật phát sinh khi xuất CSV được loại bỏ khi đọc; dữ liệu gốc không bị sửa.

| Biến | Vai trò | Đơn vị/thang đo | Lý do chọn |
| --- | --- | --- | --- |
| `cnt` | Tổng lượt thuê theo giờ | Lượt thuê/giờ | Biến mục tiêu, thuộc nhóm biến đếm |
| `temp` | Nhiệt độ | Chuẩn hóa 0–1 | Có liên hệ dương với `cnt`, hình dạng gần đối xứng |
| `hum` | Độ ẩm | Chuẩn hóa 0–1 | Có liên hệ âm với `cnt`, bị giới hạn trong 0–1 |
| `workingday` | Loại ngày | 0/1 | Dùng để so sánh mô tả giữa ngày nghỉ và ngày làm việc |

`casual` và `registered` chỉ được dùng để kiểm tra `cnt = casual + registered`, không được dùng làm biến giải thích độc lập cho `cnt` vì gây rò rỉ dữ liệu (data leakage).

### 2.1.3. Kiểm tra dữ liệu đầu vào

**Bảng 2.1. Kiểm tra nhanh dữ liệu trước phân tích**

| Nội dung | Kết quả |
| --- | ---: |
| Số dòng | 17,379 |
| Số biến sau khi loại index kỹ thuật | 17 |
| Ô thiếu | 0 |
| Dòng trùng hoàn toàn | 0 |
| Cặp (`dteday`, `hr`) trùng | 0 |
| Dòng không thỏa `cnt = casual + registered` | 0 |
| Dòng có `cnt = 0` | 0 |
| Giá trị `hum = 0` sau tiền xử lý | 0 |

Kết quả cho thấy dữ liệu đầu vào phù hợp để tiếp tục phân tích. `hum = 0` đã được xử lý ở Phần 1; 165 giờ bị thiếu trong chuỗi thời gian không được chèn thêm, nên các kết luận dưới đây chỉ áp dụng cho những giờ có bản ghi.

## 2.2. Thống kê mô tả

**Bảng 2.2. Thống kê mô tả của các biến phân tích**

| Biến | Mean | Median | Std | Min | Q1 | Q3 | Max | IQR | Skewness | Kurtosis | Variance/Mean |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cnt` | 189.46 | 142.00 | 181.39 | 1.00 | 40.00 | 281.00 | 977.00 | 241.00 | 1.2774 | 1.4172 | 173.6563 |
| `temp` | 0.50 | 0.50 | 0.19 | 0.02 | 0.34 | 0.66 | 1.00 | 0.32 | -0.0060 | -0.9418 | 0.0746 |
| `hum` | 0.63 | 0.63 | 0.19 | 0.08 | 0.48 | 0.78 | 1.00 | 0.30 | -0.0828 | -0.9119 | 0.0585 |

`cnt` có mean lớn hơn median và skewness dương, cho thấy một số giờ có nhu cầu rất cao kéo mean lên. Tỷ số variance/mean bằng 173.6563, lớn hơn rất nhiều so với mức xấp xỉ 1 của Poisson; đây là dấu hiệu over-dispersion mạnh. Ngược lại, `temp` và `hum` có skewness gần 0, nên hình dạng của hai biến này gần đối xứng hơn.

## 2.3. Phân phối thực nghiệm của `cnt`

### 2.3.1. Mục đích và phương pháp

Hình 2.1 được dùng để quan sát trực tiếp vùng tập trung, đuôi phải, tỷ lệ tích lũy và các giá trị cực trị của `cnt`.

- Histogram kết hợp KDE cho biết hình dạng tổng thể và vùng tập trung của phân phối.
- Mean và median được đánh dấu để nhận diện độ lệch phải.
- ECDF cho biết tỷ lệ số giờ có nhu cầu không vượt quá một mức `cnt` cụ thể.
- Boxplot tóm tắt median, IQR và các quan sát nằm xa phần trung tâm.

![Hình 2.1. Phân phối, tỷ lệ tích lũy và độ phân tán của tổng lượt thuê theo giờ](assets/fig_2_1_cnt_empirical.png)

**Hình 2.1. Phân phối thực nghiệm của tổng lượt thuê theo giờ**

### 2.3.2. Nhận xét

Phân phối của `cnt` tập trung nhiều ở vùng nhu cầu thấp và kéo dài về phía phải đến 977 lượt/giờ. Mean bằng 189.46 cao hơn median 142.00, phù hợp với skewness 1.2774. ECDF cho thấy khoảng một nửa số giờ có không quá 142 lượt thuê, trong khi một tỷ lệ nhỏ các giờ cao điểm tạo ra phần đuôi dài.

Boxplot cho thấy nhiều giá trị cao vượt khỏi phần trung tâm. Tuy nhiên, các giá trị này không được tự động xem là lỗi: EDA cho thấy chúng tập trung ở các khung giờ cao điểm và có thể phản ánh nhu cầu thực tế. Có 6.22% số dòng có `cnt ≤ 5` và 2.91% có `cnt > 642.5`.

Phân phối gộp của `cnt` chịu ảnh hưởng đồng thời của giờ trong ngày, loại ngày, năm, mùa và thời tiết. Vì vậy, một phân phối lý thuyết fit trên toàn bộ dữ liệu chỉ là mô hình tổng quát, không đại diện hoàn hảo cho từng nhóm giờ hoặc từng loại ngày.

### 2.3.3. Kiểm tra biến đổi `log1p`

Phép biến đổi `log1p(cnt)` được kiểm tra vì thường được dùng để giảm ảnh hưởng của đuôi phải và xử lý biến đếm có độ phân tán lớn. Skewness của `cnt` là 1.2774, trong khi skewness của `log1p(cnt)` là -0.8182. Như vậy phép biến đổi đã đảo độ lệch sang trái thay vì đưa dữ liệu về dạng chuẩn. `log1p` chỉ được xem là một phương án cần đánh giá theo từng mô hình, chưa được chốt làm biến đổi cuối cùng.

## 2.4. So sánh các phân phối lý thuyết cho `cnt`

### 2.4.1. Cơ sở lựa chọn

- **Poisson:** phù hợp với biến đếm không âm khi mean và variance xấp xỉ nhau. Tham số duy nhất là $\lambda = E[cnt]$.
- **Negative Binomial:** mở rộng Poisson bằng cách cho phép variance lớn hơn mean, phù hợp để kiểm tra dữ liệu có over-dispersion.
- **Normal:** baseline đối xứng, dùng để cho thấy mức độ không phù hợp của giả định chuẩn với `cnt`.
- **Log-normal:** baseline liên tục dương và lệch phải, dùng để đối chiếu với các phân phối cho biến đếm.

AIC và BIC được dùng để cân bằng độ phù hợp và số tham số; giá trị thấp hơn là tốt hơn khi các mô hình được fit trên cùng dữ liệu. Hai tiêu chí này phải được đọc cùng histogram, Q–Q plot và bản chất rời rạc của `cnt`.

### 2.4.2. Kết quả fit

![Hình 2.2. So sánh các phân phối lý thuyết với nhu cầu thuê xe theo giờ](assets/fig_2_2_cnt_distribution_fits.png)

**Hình 2.2. So sánh phân phối rời rạc và baseline liên tục cho `cnt`**

**Bảng 2.3. Kết quả fit các phân phối cho `cnt`**

| Phân phối | Tham số chính | AIC | BIC |
| --- | --- | ---: | ---: |
| Poisson | `mu = 189.4631` | 3,002,494.202 | 3,002,501.965 |
| Negative Binomial | `size = 1.0973`; `p = 0.0058` | 217,615.076 | 217,630.602 |
| Normal | `loc = 189.4631`; `scale = 181.3824` | 230,086.178 | 230,101.704 |
| Log-normal | `shape = 1.4861`; `scale = 93.3244` | 220,758.045 | 220,773.571 |

Negative Binomial có AIC và BIC thấp hơn rất nhiều so với Poisson. Kết quả này phù hợp với tỷ số variance/mean bằng 173.6563, cho thấy Poisson đơn giản không thể phản ánh độ phân tán của dữ liệu. Log-normal có AIC/BIC tốt hơn Normal trong nhóm baseline liên tục, nhưng vẫn không xử lý được bản chất rời rạc và sự pha trộn nhiều nhóm của `cnt`.

### 2.4.3. Q–Q plot và goodness-of-fit

Q–Q plot so sánh quantile thực nghiệm với quantile lý thuyết. Các điểm lệch khỏi đường chéo cho thấy phân phối lý thuyết không mô tả tốt vùng tương ứng. Với Poisson và Negative Binomial, việc đánh giá dựa chủ yếu trên histogram, xác suất theo khoảng và AIC/BIC vì đây là các phân phối rời rạc.

![Hình 2.3. Mức độ phù hợp của các phân phối lý thuyết với nhu cầu thuê xe](assets/fig_2_3_cnt_goodness_of_fit.png)

**Hình 2.3. Q–Q plot và kiểm tra goodness-of-fit cho `cnt`**

Normal lệch rõ khỏi đường chéo vì không thể đồng thời mô tả vùng `cnt` thấp, vùng trung tâm và đuôi phải. Log-normal bám đuôi phải tốt hơn Normal nhưng vẫn không tái hiện hoàn toàn cấu trúc rời rạc của dữ liệu. Chi-square theo các khoảng và KS cho p-value rất nhỏ; tuy nhiên, với 17,379 quan sát, các kiểm định này có thể bác bỏ cả sai lệch nhỏ. Vì vậy không dùng p-value làm tiêu chí duy nhất.

**Kết luận mục 2.4:** Negative Binomial là lựa chọn hợp lý hơn Poisson để mô tả `cnt` trong dữ liệu hiện tại vì vừa là phân phối đếm vừa cho phép over-dispersion. Đây là kết luận về mức độ phù hợp mô tả, không phải khẳng định dữ liệu được sinh ra chính xác từ Negative Binomial.

## 2.5. Phân phối của `temp` và `hum`

### 2.5.1. Phương pháp

Normal được dùng để kiểm tra mức độ gần đối xứng. Beta được dùng vì hai biến được chuẩn hóa trong khoảng 0–1; tuy nhiên, Beta không nhận trực tiếp các giá trị đúng tại biên trong mật độ thông thường. Notebook dùng clipping rất nhỏ chỉ trong bước fit và không thay đổi dataframe gốc.

![Hình 2.4. Phân phối và mức độ phù hợp của các mô hình cho nhiệt độ và độ ẩm](assets/fig_2_4_weather_distributions.png)

**Hình 2.4. Phân phối thực nghiệm, Q–Q plot và ECDF của `temp` và `hum`**

### 2.5.2. Kết quả và nhận xét

`temp` có mean 0.4970, median 0.50 và skewness -0.0060, tức gần đối xứng. Beta có AIC -9,102.191, thấp hơn Normal -7,936.739. Kết quả này cho thấy Beta mô tả tốt hơn trong lần so sánh cụ thể này, một phần vì nó tôn trọng miền giá trị 0–1. Tuy nhiên, histogram có nhiều đỉnh nhỏ do giá trị thời tiết được ghi theo các mức rời rạc, nên không nên xem Beta là mô hình sinh dữ liệu hoàn hảo.

`hum` có mean 0.6281, median 0.63 và skewness -0.0828, cũng gần đối xứng. Normal có AIC -8,096.975, thấp hơn Beta -7,361.881. Q–Q plot cho thấy Normal mô tả phần trung tâm khá tốt, trong khi các điểm gần biên 1 tạo sai lệch ở phần đuôi.

AIC/BIC chỉ được so sánh giữa các phân phối trên cùng một biến và cùng số quan sát. Không so sánh trực tiếp AIC của `temp` với AIC của `hum` để kết luận biến nào “phù hợp hơn”.

## 2.6. `cnt` theo `workingday`

### 2.6.1. Mục đích và phương pháp

Phân tích này mô tả xem ngày làm việc và ngày nghỉ có mức trung tâm, độ phân tán và hình dạng đuôi khác nhau hay không. Histogram dạng step giúp so sánh hình dạng và mức chồng lấn. Boxplot giúp so sánh median, IQR và các giá trị cực trị trên cùng thang đo.

![Hình 2.5. Phân phối nhu cầu thuê theo loại ngày](assets/fig_2_5_workingday_comparison.png)

**Hình 2.5. Phân phối và độ phân tán của `cnt` theo `workingday`**

**Bảng 2.4. Thống kê `cnt` theo `workingday`**

| `workingday` | Nhóm | n | Mean | Median | Std | Q1 | Q3 | IQR | Skewness |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | Ngày nghỉ | 5,514 | 181.41 | 119.00 | 172.85 | 40.00 | 292.00 | 252.00 | 1.06 |
| 1 | Ngày làm việc | 11,865 | 193.21 | 151.00 | 185.11 | 40.00 | 277.00 | 237.00 | 1.35 |

### 2.6.2. Nhận xét

Hai nhóm đều có phân phối lệch phải và chồng lấn đáng kể. Ngày làm việc có mean 193.21 và median 151, cao hơn ngày nghỉ tương ứng là 181.41 và 119. Ngày làm việc có skewness 1.35, còn ngày nghỉ có skewness 1.06; cả hai đều chịu ảnh hưởng của các giờ có nhu cầu cao.

Chênh lệch giữa hai nhóm chưa thể được diễn giải là tác động riêng của `workingday`, vì cơ cấu `hr`, mùa, năm và thời tiết trong hai nhóm không giống nhau. Đây chỉ là thống kê mô tả và không thay thế kiểm định giả thuyết của TV3.

## 2.7. Kết luận và hạn chế

### 2.7.1. Kết luận chính

1. `cnt` là biến đếm lệch phải: mean 189.46 lớn hơn median 142.00, skewness bằng 1.2774 và variance/mean bằng 173.6563.
2. Negative Binomial phù hợp hơn Poisson trong việc mô tả `cnt` vì cho phép over-dispersion; kết luận được hỗ trợ bởi AIC/BIC, đồ thị và tỷ số variance/mean.
3. `log1p(cnt)` làm skewness đảo sang trái nên chưa được chốt làm biến đổi cuối cùng cho mô hình.
4. `temp` gần đối xứng và Beta có AIC thấp hơn Normal; `hum` gần đối xứng và Normal có AIC thấp hơn Beta.
5. Ngày làm việc có mức `cnt` trung tâm cao hơn ngày nghỉ, nhưng hai phân phối chồng lấn nhiều và chưa thể suy ra quan hệ nhân quả.

### 2.7.2. Hạn chế

- Goodness-of-fit nhạy với cỡ mẫu lớn; p-value rất nhỏ không đồng nghĩa sai khác có ý nghĩa thực tiễn lớn.
- Các quan sát theo giờ không độc lập hoàn toàn do tự tương quan, nên độ chắc chắn của các kiểm định có thể bị đánh giá quá cao.
- Phân phối `cnt` gộp nhiều cấu trúc theo giờ, workingday, năm và thời tiết; fit phân phối gộp không đại diện hoàn hảo cho từng nhóm.
- `temp` và `hum` ở thang chuẩn hóa 0–1; Beta được fit sau clipping kỹ thuật rất nhỏ tại biên.
- Dữ liệu có 165 giờ thiếu và chỉ đại diện cho một hệ thống tại Washington D.C. trong hai năm, nên khả năng khái quát hóa bị giới hạn.

### 2.7.3. Hàm ý cho các phần sau

- **TV3 / V-05:** `cnt` lệch phải và over-dispersion; khi chọn kiểm định cần kiểm tra giả định, cân nhắc test phi tham số và báo cáo effect size.
- **TV4 / V-06:** Pearson phù hợp để mô tả quan hệ tuyến tính; Spearman phù hợp hơn khi quan hệ đơn điệu và dữ liệu lệch hoặc có ngoại lai. Lựa chọn cuối cùng cần dựa trên phân phối chính thức.
- **TV5 / V-07:** chưa chốt biến đổi `cnt`; nếu thử log hoặc biến đổi khác, metric cuối phải quy về thang lượt thuê gốc.

## Tài liệu tham khảo

Fanaee-T, H., & Gama, J. (2013). *Event labeling combining ensemble detectors and background knowledge*. Progress in Artificial Intelligence, 2(2–3), 113–127. Bộ dữ liệu *Bike Sharing Dataset*, UCI Machine Learning Repository.

Các kết quả số và hình trong phần này được tạo lại từ `02_distribution.ipynb` bằng dữ liệu `EDA/cleaned_data/hour_cleaned.csv`.
