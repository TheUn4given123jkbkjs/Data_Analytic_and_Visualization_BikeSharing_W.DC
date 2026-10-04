# CHƯƠNG 1. KHÁM PHÁ DỮ LIỆU (EDA)

## 1.1. Giới thiệu

### 1.1.1. Bối cảnh và mục tiêu

Hệ thống chia sẻ xe đạp cho phép người dùng thuê xe tại một trạm và trả tại một trạm khác. Nhu cầu thuê biến động theo giờ trong ngày, loại ngày (làm việc hay nghỉ), mùa và điều kiện thời tiết. Việc nhận diện các yếu tố này hỗ trợ nhà vận hành điều phối xe, lập kế hoạch bảo trì và dự báo nhu cầu. Chương này thực hiện bước khám phá dữ liệu (Exploratory Data Analysis – EDA) nhằm nắm rõ đặc điểm của dữ liệu trước khi xây dựng mô hình dự báo, với bốn mục tiêu:

1. Mô tả cấu trúc, kiểu dữ liệu và ý nghĩa của từng biến.
2. Kiểm tra chất lượng dữ liệu (giá trị thiếu, trùng lặp, bất hợp lệ, tính đầy đủ của chuỗi thời gian) và quyết định cách xử lý dựa trên bằng chứng từ kết quả kiểm tra.
3. Mô tả phân phối của biến mục tiêu và các biến giải thích quan trọng.
4. Phát hiện và đánh giá giá trị ngoại lai, phân biệt ngoại lai thống kê với lỗi dữ liệu.

Các câu hỏi cụ thể gồm: (i) biến mục tiêu `cnt` phân bố như thế nào; (ii) nhu cầu có xu hướng và tính mùa vụ theo thời gian hay không; (iii) thời tiết (nhiệt độ, độ ẩm, gió) liên quan thế nào đến nhu cầu; (iv) `hr`, `workingday`, `season`, `weathersit` làm nhu cầu khác nhau ra sao; (v) có ngoại lai hoặc vấn đề dữ liệu nào cần lưu ý cho bước mô hình hóa.

### 1.1.2. Nguồn dữ liệu

Nghiên cứu sử dụng bộ dữ liệu **Bike Sharing Dataset** trên UCI Machine Learning Repository (Fanaee-T & Gama, 2013). Dữ liệu gốc là số liệu vận hành của hệ thống Capital Bikeshare tại Washington D.C. (Hoa Kỳ), được các tác giả ghép thêm thông tin thời tiết và lịch ngày lễ. File sử dụng là `hour.csv`, trong đó mỗi bản ghi tương ứng với một giờ.

| Thuộc tính        | Giá trị                                                 |
| ----------------- | ------------------------------------------------------- |
| Phạm vi thời gian | 2011-01-01 đến 2012-12-31 (731 ngày, tối đa 17.544 giờ) |
| Quy mô            | 17.379 bản ghi × 17 biến                                |
| Kiểu dữ liệu      | 12 cột `int64`, 4 cột `float64`, 1 cột chuỗi (`dteday`) |

### 1.1.3. Biến mục tiêu và phân loại biến

Biến mục tiêu là **`cnt`**, tổng số lượt thuê trong một giờ, gồm lượt thuê của khách vãng lai (`casual`) và của thành viên đăng ký (`registered`), với `cnt = casual + registered`. Do quan hệ này, `casual` và `registered` không được dùng làm biến độc lập khi dự đoán `cnt` vì sẽ gây rò rỉ dữ liệu (data leakage); hai biến chỉ dùng cho mục đích mô tả.

**Bảng 1.1. Mô tả và phân loại các biến của `hour.csv`**

| Nhóm           | Biến         | Ý nghĩa                                                     | Phân loại                    |
| -------------- | ------------ | ----------------------------------------------------------- | ---------------------------- |
| Định danh      | `instant`    | Số thứ tự bản ghi                                           | Identifier                   |
| Thời gian      | `dteday`     | Ngày (YYYY-MM-DD)                                           | Date/Time                    |
|                | `yr`         | Năm (0 = 2011, 1 = 2012)                                    | Categorical (nhị phân)       |
|                | `mnth`       | Tháng 1–12                                                  | Categorical (thứ tự, chu kỳ) |
|                | `hr`         | Giờ trong ngày 0–23                                         | Categorical (thứ tự, chu kỳ) |
|                | `weekday`    | Thứ trong tuần 0–6 (0 = Chủ nhật)                           | Categorical (thứ tự, chu kỳ) |
| Loại ngày      | `holiday`    | Ngày lễ (1) hay không (0)                                   | Categorical (nhị phân)       |
|                | `workingday` | Ngày làm việc (1): không phải cuối tuần, không phải ngày lễ | Categorical (nhị phân)       |
| Mùa, thời tiết | `season`     | 1 = đông, 2 = xuân, 3 = hè, 4 = thu                         | Categorical (định danh)      |
|                | `weathersit` | 1 = quang, 2 = mây/sương, 3 = mưa/tuyết nhẹ, 4 = mưa lớn    | Categorical (thứ tự)         |
|                | `temp`       | Nhiệt độ (chuẩn hóa)                                        | Numerical (liên tục)         |
|                | `atemp`      | Nhiệt độ cảm nhận (chuẩn hóa)                               | Numerical (liên tục)         |
|                | `hum`        | Độ ẩm (chuẩn hóa, chia 100)                                 | Numerical (liên tục)         |
|                | `windspeed`  | Tốc độ gió (chuẩn hóa, chia 67)                             | Numerical (liên tục)         |
| Kết quả        | `casual`     | Lượt thuê của khách vãng lai                                | Numerical (đếm)              |
|                | `registered` | Lượt thuê của thành viên đăng ký                            | Numerical (đếm)              |
|                | `cnt`        | Tổng lượt thuê (**biến mục tiêu**)                          | Numerical (đếm)              |

Một số điểm cần lưu ý về cấu trúc biến:

- **Biến phân loại và tính chu kỳ.** Tám biến phân loại chỉ nhận từ 2 đến 24 giá trị khác nhau. Ba biến `hr`, `mnth`, `weekday` được lưu bằng số nhưng mang tính tuần hoàn (giờ 23 liền kề giờ 0, tháng 12 liền kề tháng 1), do đó không nên xử lý như biến liên tục; khi mô hình hóa cần mã hóa one-hot hoặc sin/cos.
- **Chuẩn hóa biến thời tiết.** Theo tài liệu của bộ dữ liệu, bốn biến thời tiết đã được đưa về thang [0, 1]. Với nhiệt độ, phép chuẩn hóa min-max `x_chuẩn hóa = (x − x_min)/(x_max − x_min)` dùng hai cận cố định (`temp`: −8 và +39 °C; `atemp`: −16 và +50 °C); `hum` được chia cho 100 và `windspeed` chia cho 67. Do là phép biến đổi tuyến tính với cận cố định, phép chuẩn hóa không làm mất thông tin, không thay đổi hình dạng phân phối, thứ hạng hay hệ số tương quan, và không gây rò rỉ thông tin giữa tập huấn luyện và tập kiểm tra. **Toàn bộ chương này giữ giá trị chuẩn hóa**, mọi số liệu của bốn biến này đều ở thang 0–1.
- **Thang đo của `windspeed`.** Biến này chỉ nhận 30 giá trị khác nhau trên 17.379 dòng, tức rời rạc theo từng mức.

---

## 1.2. Chất lượng dữ liệu và tiền xử lý

Nguyên tắc xuyên suốt: kiểm tra trước, quyết định xử lý sau và chỉ dựa trên bằng chứng; dữ liệu gốc được lưu riêng (`df_raw`) để đối chiếu; chỉ can thiệp khi có cơ sở cho rằng giá trị là lỗi, tránh áp đặt giả định chưa được kiểm chứng.

### 1.2.1. Kiểm tra chất lượng dữ liệu

Bốn nhóm kiểm tra được thực hiện: (a) giá trị thiếu và bản ghi trùng lặp; (b) giá trị bất hợp lệ (miền giá trị và ràng buộc logic giữa các biến); (c) giá trị nằm trong miền hợp lệ nhưng đáng ngờ; (d) tính đầy đủ của chuỗi thời gian.

**Bảng 1.2. Tổng hợp kết quả kiểm tra chất lượng dữ liệu**

| Nhóm kiểm tra        | Nội dung kiểm tra                                                                                                     | Kết quả                                   |
| -------------------- | --------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| (a) Thiếu và trùng   | Ô trống; dòng trùng toàn bộ; trùng cặp (`dteday`, `hr`); tính duy nhất và tăng dần của `instant`                      | Không có vấn đề (0 ô thiếu, 0 dòng trùng) |
| (b) Miền giá trị     | Từng biến so với miền hợp lệ (ví dụ `season` ∈ [1, 4], biến thời tiết ∈ [0, 1], biến đếm ≥ 0)                         | Không có vi phạm                          |
| (b) Ràng buộc logic  | `cnt = casual + registered`; `weekday`, `mnth`, `yr` khớp `dteday`; `workingday` nhất quán với `weekday` và `holiday` | Không có vi phạm                          |
| (c) Giá trị đáng ngờ | `hum = 0`                                                                                                             | 22 dòng, cùng thuộc ngày 2011-03-10       |
|                      | `windspeed = 0`                                                                                                       | 2.180 dòng (12,54%)                       |
|                      | `weathersit = 4`                                                                                                      | 3 dòng, thuộc 3 ngày khác nhau            |
|                      | Tương quan `temp`–`atemp`                                                                                             | Pearson 0,9877                            |
| (d) Chuỗi thời gian  | So với 731 × 24 = 17.544 giờ kỳ vọng                                                                                  | Thiếu 165 giờ (0,94%), trải trên 76 ngày  |

**Giá trị trong miền hợp lệ.** Các biến đều nằm trong miền cho phép: `temp` từ 0,02 đến 1,00; `atemp` từ 0,00 đến 1,00; `hum` từ 0,00 đến 1,00; `windspeed` từ 0,00 đến 0,8507; `cnt` từ 1 đến 977; `casual` từ 0 đến 367; `registered` từ 0 đến 886. Không có giờ nào có `cnt = 0`. Kết quả cho thấy các biến lịch được sinh nhất quán nên có thể dùng để nhóm dữ liệu ở các bước sau. Tuy nhiên, phép kiểm tra miền giá trị chỉ phát hiện giá trị **ngoài miền**, không phát hiện giá trị nằm trong miền nhưng vô lý về mặt vật lý hoặc đo đạc, được xem xét tiếp ở phần dưới.

**Các giá trị đáng ngờ.** Hình 1.1 trình bày các giá trị đáng ngờ của `windspeed` và `hum`.

![alt text](assets/hinh1.1.png)

- **`hum = 0`.** 22 dòng này đều thuộc ngày 2011-03-10, và ngày này cũng chỉ có đúng 22 dòng dữ liệu; độ ẩm trung bình cả ngày bằng 0 rồi trở lại bình thường vào ngày kế tiếp. Độ ẩm 0% kéo dài cả ngày là bất khả thi trong khí quyển thực, do đó nhiều khả năng đây là lỗi cảm biến hoặc lỗi ghi nhận (suy luận từ dữ liệu, chưa được nguồn xác nhận).
- **`windspeed = 0`.** Có 2.180 dòng (12,54%). Giá trị dương nhỏ nhất là 0,0896 (tương ứng 6,00 theo thang ×67), tức không có quan sát nào nằm giữa 0 và mức này. Có hai cách hiểu: gió thực sự bằng 0, hoặc gió dưới ngưỡng đo bị ghi thành 0. Dữ liệu hiện có chưa đủ để phân biệt (xem thêm mục 1.5.2).
- **`weathersit = 4`.** Chỉ có 3 dòng, quá ít để thống kê theo nhóm có ý nghĩa.
- **`temp` và `atemp`.** Hệ số tương quan Pearson 0,9877, hai biến gần như trùng thông tin; đưa cả hai vào mô hình tuyến tính sẽ gây đa cộng tuyến mà không bổ sung thông tin.

**Tính đầy đủ của chuỗi thời gian.** Các kiểm tra trên đánh giá những dòng đang có; kiểm tra này đánh giá những dòng đáng lẽ phải có nhưng không có. Hình 1.2 cho thấy phân bố 165 giờ bị thiếu.

![alt text](assets/hinh1.2.png)

Chuỗi thời gian **không đầy đủ**: thiếu 165 giờ trên 17.544 giờ kỳ vọng (0,94%), không có ngày nào vắng mặt hoàn toàn. Phần thiếu không phân bố ngẫu nhiên mà có hai kiểu tập trung:

- _Theo giờ trong ngày:_ 98/165 giờ thiếu (59,39%) nằm trong khung 2–5 giờ sáng, cao nhất ở 3 giờ và 4 giờ (mỗi giờ 34 lần), đúng khung có `cnt` trung bình thấp nhất. Kết hợp với việc không có dòng nào có `cnt = 0`, giả thuyết hợp lý là hệ thống chỉ ghi dòng khi có ít nhất một lượt thuê (suy luận từ hình dạng dữ liệu, tài liệu gốc không xác nhận).
- _Theo ngày:_ một số ít ngày thiếu rất nhiều giờ, gồm 2012-10-29 (23 giờ), 2011-01-27 (16 giờ), 2012-10-30 (13 giờ) và 2011-01-18 (12 giờ); 5 ngày thiếu nhiều nhất chiếm 72 giờ (43,64% tổng số giờ thiếu). Cả ngày không có lượt thuê là điều bất thường, nên kiểu thiếu này khó giải thích bằng "không phát sinh lượt thuê" và nhiều khả năng liên quan đến điều kiện cực đoan hoặc sự cố hệ thống.

Như vậy 165 giờ thiếu có thể do hai cơ chế khác nhau mà dữ liệu không đủ để tách bạch.

### 1.2.2. Tiền xử lý dữ liệu

Các quyết định tiền xử lý được tổng hợp ở Bảng 1.3.

**Bảng 1.3. Các quyết định tiền xử lý dữ liệu**

| Vấn đề phát hiện                      | Quyết định                                                                     | Lý do                                                                                                                                                                |
| ------------------------------------- | ------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Không có ô trống và bản ghi trùng lặp | Không xử lý                                                                    | Không có bằng chứng lỗi                                                                                                                                              |
| `dteday` ở dạng chuỗi                 | Chuyển sang kiểu `datetime` tại chỗ, không tạo thêm cột | Phục vụ phân tích xu hướng và mùa vụ                                                                                                                                 |
| Biến phân loại mã hóa bằng số         | Giữ nguyên mã                                                                  | Bảo toàn giá trị gốc; thêm nhãn khi cần trực quan hóa                                                                                                                |
| Biến thời tiết đã chuẩn hóa           | Giữ thang 0–1                                                                  | Tránh biến đổi không cần thiết                                                                                                                                       |
| `hum = 0` (22 dòng, ngày 2011-03-10)  | Thay bằng trung bình độ ẩm **cùng giờ** của ngày liền trước và ngày liền sau   | Độ ẩm 0% cả ngày là bất hợp lý; dùng cùng giờ để giữ chu kỳ ngày–đêm, dùng hai ngày lân cận để cân bằng thông tin hai phía (tương đương nội suy tuyến tính đơn giản) |
| `windspeed = 0` (2.180 dòng)          | Giữ nguyên                                                                     | Gió bằng 0 có thể là giá trị thực; chưa đủ bằng chứng là lỗi                                                                                                         |
| Thiếu 165 giờ                         | Không chèn dòng giả                                                            | Chưa xác định được nguyên nhân; chèn `cnt = 0` hoặc nội suy có thể làm lệch phân phối của `cnt`                                                                      |

Sau xử lý, cột `hum` không còn giá trị 0 hoặc giá trị thiếu. Dữ liệu sau tiền xử lý gồm 17.379 dòng và 17 cột.

**Giả định và hạn chế.**

- Việc xem `hum = 0` là lỗi ghi nhận dựa trên tính hợp lý vật lý và việc các giá trị này dồn vào một ngày; giá trị thay thế chỉ là ước lượng và có thể sai lệch nếu thời tiết thay đổi đột ngột.
- `windspeed = 0` được giữ nguyên; nếu thực chất là giá trị thiếu được mã hóa thì việc giữ lại có thể ảnh hưởng đến thống kê và mô hình.
- Chuỗi vẫn không liên tục (165 giờ thiếu), nên các phân tích dùng đặc trưng trễ, trung bình trượt hoặc tự tương quan cần xử lý riêng các khoảng đứt, tránh coi hai dòng liền kề trong bảng là hai giờ liên tiếp.

---

## 1.3. Thống kê mô tả

### 1.3.1. Thống kê các biến số

**Bảng 1.4. Thống kê mô tả của biến mục tiêu và các biến số**

| Biến         | Mean   | Median | Std    | Min  | Q1   | Q3   | Max  | IQR  | Skewness |
| ------------ | ------ | ------ | ------ | ---- | ---- | ---- | ---- | ---- | -------- |
| `cnt`        | 189,46 | 142    | 181,39 | 1    | 40   | 281  | 977  | 241  | 1,28     |
| `casual`     | 35,68  | 17     | 49,31  | 0    | 4    | 48   | 367  | 44   | 2,50     |
| `registered` | 153,79 | 115    | 151,36 | 0    | 34   | 220  | 886  | 186  | 1,56     |
| `temp`       | 0,50   | 0,50   | 0,19   | 0,02 | 0,34 | 0,66 | 1,00 | 0,32 | −0,01    |
| `atemp`      | 0,48   | 0,48   | 0,17   | 0,00 | 0,33 | 0,62 | 1,00 | 0,29 | −0,09    |
| `hum`        | 0,63   | 0,63   | 0,19   | 0,08 | 0,48 | 0,78 | 1,00 | 0,30 | −0,08    |
| `windspeed`  | 0,19   | 0,19   | 0,12   | 0,00 | 0,10 | 0,25 | 0,85 | 0,15 | 0,57     |

_Ghi chú: các biến thời tiết ở thang chuẩn hóa 0–1; n = 17.379._

- **Biến mục tiêu `cnt` lệch phải.** Giá trị trung bình (189,46) cao hơn trung vị (142); skewness bằng 1,28; giá trị lớn nhất (977) gấp 3,48 lần Q3 (281). Một số ít giờ có lượng thuê rất cao kéo trung bình lên, nên trung vị và IQR mô tả mức nhu cầu điển hình tốt hơn trung bình.
- **Phân tán vượt mức.** Hệ số biến thiên là 0,96 và tỷ số phương sai trên trung bình là 173,66, trong khi phân phối Poisson cho giá trị xấp xỉ 1; dữ liệu gộp do đó có hiện tượng phân tán vượt mức (over-dispersion). Có 1.081 dòng (6,22%) với `cnt` ≤ 5, trong đó 158 dòng bằng 1.
- **Hai nhóm khách.** `registered` chiếm 81,17% tổng lượt thuê, `casual` chiếm 18,83%. `casual` lệch phải mạnh hơn (skewness 2,50 so với 1,56) và có trung vị (17) thấp hơn nhiều so với trung bình (35,68), tức phần lớn các giờ chỉ có ít lượt thuê của khách vãng lai.
- **Biến thời tiết.** `temp`, `atemp` và `hum` gần đối xứng; `windspeed` lệch phải nhẹ và có 2.180 dòng (12,54%) bằng 0.

**Bảng 1.5. Thống kê `cnt` theo `season`, `weathersit`, `workingday` và `yr`**

| Biến         | Nhóm              | n      | Mean   | Median | Std    |
| ------------ | ----------------- | ------ | ------ | ------ | ------ |
| `season`     | Winter            | 4.242  | 111,11 | 76     | 119,22 |
|              | Spring            | 4.409  | 208,34 | 165    | 188,36 |
|              | Summer            | 4.496  | 236,02 | 199    | 197,71 |
|              | Fall              | 4.232  | 198,87 | 155,5  | 182,97 |
| `weathersit` | Clear             | 11.413 | 204,87 | 159    | 189,49 |
|              | Mist / Cloudy     | 4.544  | 175,17 | 133    | 165,43 |
|              | Light Rain / Snow | 1.419  | 111,58 | 63     | 133,78 |
|              | Heavy Rain / Snow | 3      | 74,33  | 36     | 77,93  |
| `workingday` | Ngày nghỉ         | 5.514  | 181,41 | 119    | 172,85 |
|              | Ngày làm việc     | 11.865 | 193,21 | 151    | 185,11 |
| `yr`         | 2011              | 8.645  | 143,79 | 109    | 133,80 |
|              | 2012              | 8.734  | 234,67 | 191    | 208,91 |

- **Mùa.** `cnt` trung bình thấp nhất ở Winter (111,11) và cao nhất ở Summer (236,02), gấp 2,12 lần.
- **Thời tiết.** Trung bình giảm khi thời tiết xấu đi: 204,87 (Clear), 175,17 (Mist / Cloudy, thấp hơn 14,50%) và 111,58 (Light Rain / Snow, thấp hơn 45,53%). Nhóm Heavy Rain / Snow chỉ có 3 dòng nên không thể rút ra kết luận.
- **Loại ngày.** Trung bình ngày làm việc cao hơn ngày nghỉ 11,80 lượt/giờ (6,50%), nhưng khác biệt này chưa mô tả được hành vi theo giờ (xem mục 1.4.3).
- **Năm.** Trung bình năm 2012 cao hơn năm 2011 là 63,20%.

Các so sánh trên chỉ mô tả mẫu; chênh lệch giữa các nhóm có thể lẫn với yếu tố khác (ví dụ cơ cấu mùa và năm) nên chưa tách được phần liên hệ riêng của từng biến.

---

## 1.4. Trực quan hóa và phân tích

### 1.4.1. Phân phối của biến mục tiêu

Hình 1.3 khảo sát hình dạng phân phối của `cnt` (mode, độ dài đuôi, vị trí trung bình so với trung vị), kiểm tra phép biến đổi `log1p` (được chọn thay cho `log` vì `casual` và `registered` có giá trị 0) và so sánh hình dạng của `casual` với `registered`. Panel thứ ba dùng cùng dải khoảng và trục tung theo thang log để hai thành phần so sánh được.

![alt text](assets/hinh1.3.png)

Phân phối của `cnt` lệch phải: các cột cao nhất nằm ở vùng giá trị thấp, đuôi kéo dài đến 977 và đường trung bình (189) nằm bên phải đường trung vị (142), phù hợp với skewness 1,28. Khoảng 6,22% số giờ chỉ có từ 1 đến 5 lượt thuê và 2,91% số giờ vượt 642 lượt; một nửa số giờ có không quá 142 lượt. Sau phép biến đổi `log1p`, skewness là −0,82, tức độ lệch bị **đảo sang trái**; histogram có một "bậc" ở khoảng 2–4 và đỉnh chính quanh 5–6, cho thấy `cnt` là sự pha trộn giữa các giờ ít nhu cầu và các giờ nhu cầu cao. Do đó `log1p` không đưa `cnt` về dạng chuẩn, và việc có biến đổi hay không cần được quyết định theo từng mô hình. Cả `casual` và `registered` đều tập trung gần 0, trong đó `casual` có khối lượng ở giá trị thấp lớn hơn.

### 1.4.2. Xu hướng và tính mùa vụ theo thời gian

Hình 1.4 xem xét `cnt` có xu hướng dài hạn và tính mùa vụ hay không: tổng lượt thuê mỗi ngày kèm trung bình trượt 7 ngày (một chu kỳ tuần, để lọc nhiễu theo ngày), và `cnt` trung bình theo tháng của hai năm chồng trên cùng một trục.

![alt text](assets/hinh1.5.png)

Chuỗi có đồng thời hai đặc điểm:

- **Xu hướng tăng.** `cnt` trung bình năm 2012 (234,67) cao hơn năm 2011 (143,79) là 63,20%, và cả 12 tháng của 2012 đều cao hơn tháng tương ứng của 2011 (riêng tháng 1 tăng 2,35 lần).
- **Tính mùa vụ.** Trung bình theo tháng thấp nhất vào tháng 1 ở cả hai năm (55,51 năm 2011; 130,56 năm 2012), tăng qua mùa xuân và đạt đỉnh vào tháng 6/2011 (199,32) và tháng 9/2012 (303,57), rồi giảm về cuối năm.

Đường trung bình trượt biến đổi chậm, cho thấy các ngày liền kề có mức thuê gần nhau (tự tương quan). Điểm sụt sâu nhất, cuối tháng 10/2012, tương ứng ngày 2012-10-29 (22 lượt), ngày chỉ có 1/24 giờ được ghi nhận. Do dữ liệu không chứa thông tin về quy mô hệ thống (số trạm, số xe, số thành viên), nguyên nhân của đà tăng giữa hai năm chỉ có thể là giả thuyết. Vì xu hướng và mùa vụ cùng tồn tại, việc so sánh giữa các nhóm cần tính đến thời điểm quan sát.

### 1.4.3. Chu kỳ theo giờ trong ngày

Đây là câu hỏi trung tâm của phân tích vì `hr` có liên hệ mạnh nhất với `cnt` (mục 1.4.6). Hình 1.5 so sánh nhu cầu trung bình theo giờ giữa ngày làm việc và ngày nghỉ (kèm khoảng tin cậy 95%), tách thêm `registered` và `casual` trên cùng thang trục tung để xác định nhóm khách tạo ra các đỉnh nhu cầu.

![alt text](assets/hinh1.6.png)

**Bảng 1.6. Đặc điểm nhu cầu theo giờ giữa hai loại ngày**

| Tiêu chí            | Ngày làm việc                                                   | Ngày nghỉ                                                        |
| ------------------- | --------------------------------------------------------------- | ---------------------------------------------------------------- |
| Dạng đường theo giờ | Hai đỉnh                                                        | Một đỉnh rộng                                                    |
| Giờ cao điểm        | 8 giờ (477,01 lượt); 17 giờ (525,29 lượt); 18 giờ (492,23 lượt) | 13 giờ (372,73 lượt); nhu cầu tăng dần từ trưa đến khoảng 17 giờ |
| Thành phần chi phối | `registered` chiếm 95,33% (8 giờ) và 89,17% (17 giờ)            | `casual` chiếm 36,60% tại 13 giờ (136,42/372,73)                 |
| Cách diễn giải      | Phù hợp nhịp di chuyển đi làm, đi học                           | Phù hợp các chuyến đi giải trí                                   |

Tỷ trọng `casual` ở đỉnh ngày nghỉ (36,60%) gần 8 lần tỷ trọng ở đỉnh sáng ngày làm việc (4,67%). Việc diễn giải mục đích chuyến đi chỉ mang tính suy luận vì dữ liệu không ghi nhận mục đích. Nhu cầu thấp nhất ở khoảng 3–5 giờ sáng: `cnt` trung bình lúc 3 giờ là 11,73, chỉ bằng khoảng 1/39 mức lúc 17 giờ (461,45). Như vậy `hr` liên hệ chặt với `cnt` và dạng liên hệ **phụ thuộc vào `workingday`**, nên khi mô hình hóa cần xét tương tác giữa hai biến này.

### 1.4.4. `cnt` theo mùa và điều kiện thời tiết

Hình 1.6 so sánh trung vị, độ phân tán và mức chồng lấn của `cnt` giữa các mùa và các mức thời tiết bằng boxplot (phù hợp vì `cnt` lệch phải nên trung bình đơn thuần bị đuôi kéo lệch); cỡ mẫu được ghi trên nhãn trục do độ tin cậy của một hộp phụ thuộc vào số quan sát.

![alt text](assets/hinh1.7.png)

Trung vị của `cnt` tăng từ Winter (76) lên Spring (165) và Summer (199) rồi giảm ở Fall (155,5); trung vị mùa đông thấp hơn một nửa so với mùa xuân. Tuy nhiên, các hộp của Spring, Summer và Fall chồng lấn nhiều, nên biết mùa chỉ giúp xác định "mức nền" của nhu cầu mà chưa đủ để dự đoán một giờ cụ thể; muốn vậy còn cần biết giờ trong ngày (Hình 1.5). Tương tự, `cnt` giảm khi thời tiết xấu đi, còn nhóm Heavy Rain / Snow (3 dòng) không đủ để so sánh.

### 1.4.5. Quan hệ giữa biến thời tiết liên tục và `cnt`

Hình 1.7 xem xét chiều và dạng quan hệ (dương hay âm, đơn điệu hay không, tuyến tính hay cong) giữa `temp`, `hum`, `windspeed` và `cnt`, đồng thời mức phân tán của `cnt` ở mỗi mức thời tiết.

![alt text](assets/hinh1.8.png)

- **`temp`** có tương quan dương với `cnt` (Spearman ρ = 0,4233). Trung bình `cnt` tăng đều qua các khoảng của `temp`: 65,07 (0–0,2; 1.070 giờ), 123,07, 194,67, 260,70 và 326,28 (0,8–1,0; 709 giờ), tức gấp 5,01 lần giữa khoảng thấp nhất và cao nhất.
- **`hum`** có tương quan âm (ρ = −0,3634). Từ mức 0,4 trở lên, trung bình giảm từ 221,75 (0,4–0,6) xuống 172,41 và 107,17 (0,8–1,0), gần bằng một nửa. Độ ẩm cao thường đi cùng thời tiết u ám hoặc mưa (tương quan giữa `hum` và `weathersit` là 0,4151) nên hai yếu tố này khó tách rời.
- **`windspeed`** có tương quan yếu (ρ = 0,1266) và không đơn điệu.

### 1.4.6. Tương quan giữa các biến

Hình 1.8 trình bày ma trận tương quan Spearman (chọn vì `cnt` lệch phải và nhiều biến là thứ hạng) nhằm phát hiện các cặp biến có tương quan cao (rủi ro đa cộng tuyến và rò rỉ dữ liệu) và các biến liên hệ mạnh với `cnt`; heatmap `cnt` trung bình theo `weekday` × `hr` cho thấy tương tác mà từng biến riêng lẻ không thể hiện được.

![alt text](assets/hinh1.9.png)

**Bảng 1.7. Hệ số tương quan giữa các biến và `cnt`** (sắp xếp theo |Spearman|)

| Biến         | Spearman | Pearson |
| ------------ | -------- | ------- |
| `registered` | 0,9894   | 0,9722  |
| `casual`     | 0,8505   | 0,6946  |
| `hr`         | 0,5109   | 0,3941  |
| `temp`       | 0,4233   | 0,4048  |
| `atemp`      | 0,4233   | 0,4009  |
| `hum`        | −0,3634  | −0,3292 |
| `yr`         | 0,2075   | 0,2505  |
| `season`     | 0,1852   | 0,1781  |
| `windspeed`  | 0,1266   | 0,0932  |
| `weathersit` | −0,1263  | −0,1424 |
| `mnth`       | 0,1259   | 0,1206  |
| `weekday`    | 0,0303   | 0,0269  |
| `holiday`    | −0,0295  | −0,0309 |
| `workingday` | 0,0210   | 0,0303  |

Các nhận xét chính:

- **Biến liên hệ mạnh nhất với `cnt`** (ngoài `casual` và `registered`) là `hr` (0,5109), tiếp theo là `temp` (0,4233) và `hum` (−0,3634). Đây là mối liên hệ đi cùng, không phải bằng chứng nhân quả; các biến thời tiết còn liên hệ với nhau và với mùa (`hum`–`weathersit`: 0,4151; `temp`–`season`: 0,3058) nên liên hệ riêng lẻ với `cnt` chưa tách được khỏi các yếu tố đi kèm.
- **Hệ số thấp không đồng nghĩa không liên quan.** `hr` chỉ đạt 0,5109 dù chênh lệch giữa các giờ rất lớn, vì quan hệ có chu kỳ (tăng – giảm – tăng – giảm) không đơn điệu. Các biến `workingday` (0,0210), `weekday` (0,0303) và `holiday` (−0,0295) gần 0, nhưng hình dạng nhu cầu theo giờ giữa các loại ngày khác nhau rõ rệt (Hình 1.5); hệ số tương quan chỉ đo xu hướng đơn điệu của mức trung bình.
- **Heatmap `weekday` × `hr`.** Từ thứ Hai đến thứ Sáu có hai dải cao lúc 8 giờ và 17–18 giờ; thứ Bảy và Chủ nhật có một dải rộng khoảng 11–16 giờ. Giá trị trung bình cao nhất là thứ Ba lúc 17 giờ (544,28).
- **Đa cộng tuyến.** `temp` và `atemp` có tương quan 0,9877 (Pearson) và 0,9896 (Spearman); chỉ nên giữ một biến trong mô hình tuyến tính.
- **Rò rỉ dữ liệu.** `registered` (0,9894) và `casual` (0,8505) tương quan rất cao với `cnt` do `cnt = casual + registered`; hai biến này không được dùng làm biến độc lập.

---

## 1.5. Phát hiện và đánh giá giá trị ngoại lai

Mục tiêu là xác định các quan sát nằm xa phần lớn dữ liệu, sau đó phân biệt **ngoại lai thống kê** (statistical outlier) với **lỗi dữ liệu** (data error) để quyết định giữ hay xử lý; ngoại lai không bị loại bỏ mặc định.

### 1.5.1. Phát hiện

Hai quy tắc được áp dụng: (1) IQR, đánh dấu giá trị nhỏ hơn Q1 − 1,5×IQR hoặc lớn hơn Q3 + 1,5×IQR; (2) Z-score, đánh dấu |z| > 3. Do `cnt` phụ thuộc mạnh vào `hr`, ngưỡng tính trên toàn bộ dữ liệu có thể coi các đỉnh giờ cao điểm là bất thường; vì vậy bổ sung ngưỡng IQR tính riêng theo `hr`, theo cặp (`hr`, `workingday`) và theo tổng lượt thuê mỗi ngày.

**Bảng 1.8. Kết quả phát hiện giá trị ngoại lai bằng IQR và Z-score**

| Biến         | Hàng rào dưới | Hàng rào trên | Ngoại lai IQR | % IQR | Ngoại lai \|z\| > 3 | % Z  |
| ------------ | ------------- | ------------- | ------------- | ----- | ------------------- | ---- |
| `cnt`        | −321,5        | 642,5         | 505           | 2,91  | 244                 | 1,40 |
| `casual`     | −62,0         | 114,0         | 1.192         | 6,86  | 467                 | 2,69 |
| `registered` | −245,0        | 499,0         | 680           | 3,91  | 371                 | 2,13 |
| `temp`       | −0,14         | 1,14          | 0             | 0,00  | 0                   | 0,00 |
| `hum`        | 0,03          | 1,23          | 0             | 0,00  | 0                   | 0,00 |
| `windspeed`  | −0,119        | 0,477         | 342           | 1,97  | 107                 | 0,62 |

Hàng rào dưới của `cnt` âm nên chỉ có ngoại lai phía trên (505 dòng, 2,91%). Z-score đánh dấu ít hơn (244 dòng) vì trung bình và độ lệch chuẩn đều bị đuôi phải kéo lên và phương pháp này giả định phân phối gần chuẩn, điều kiện mà `cnt` không thỏa. `casual` và `registered` bị đánh dấu nhiều hơn `cnt` do phân phối lệch mạnh hơn. Trong các biến thời tiết, `temp` và `hum` không có ngoại lai; `windspeed` có 342 dòng (1,97%) vượt hàng rào trên 0,477 (giá trị lớn nhất 0,85). Giá trị ngoại lai do đó tập trung ở các biến đếm và `windspeed`, phù hợp với các phân phối lệch phải ở mục 1.3.

![alt text](assets/hinh1.10.png)

Hình 1.9 cho thấy hạn chế của ngưỡng toàn cục. Median và hộp tăng ở 7–9 giờ và 16–19 giờ, trong khi gần như mọi giờ khác đều có điểm vượt râu trên; quy tắc "quá 642 lượt/giờ là bất thường" sẽ báo động đúng vào giờ tan tầm, lúc hệ thống bận nhất. Cụ thể:

- Trong 505 dòng vượt ngưỡng toàn cục (giá trị lớn nhất 977, trung bình 749,24), **80,99%** rơi vào các giờ 8, 17, 18 và **81,98%** thuộc ngày làm việc. Đây chính là hai đỉnh giờ đi làm đã nêu ở mục 1.4.3, và `cnt = casual + registered` đúng ở mọi dòng, nên không có dấu hiệu lỗi.
- Khi tính ngưỡng riêng theo `hr`, 533 dòng (3,07%) bị đánh dấu, nằm ở các giờ 0–5 (53,85%), 10–16 và 21–23, và **không có dòng nào ở các giờ cao điểm 8, 17, 18**. Mức đông ở giờ cao điểm là bình thường của khung giờ đó. Với ngưỡng theo (`hr`, `workingday`), còn 130 dòng (0,75%).
- **Ở cấp ngày**, không có ngày nào vượt hàng rào IQR [−1.054; 10.162] hoặc có |z| > 3. Ngày thấp nhất là 2012-10-29 (22 lượt, z = −2,32) nhưng chỉ có 1/24 giờ được ghi nhận; ngày cao nhất là 2012-09-15 (8.714 lượt, đủ 24 giờ). Phần lớn đuôi thấp là các ngày thiếu giờ nên tổng lượt thuê theo ngày của chúng không so sánh được với ngày đủ 24 giờ.

### 1.5.2. Đánh giá và xử lý

Hai nhóm cần bằng chứng bổ sung trước khi quyết định: `windspeed = 0` và 130 giá trị `cnt` cao theo (`hr`, `workingday`).

**`windspeed = 0`.** Nếu các số 0 là lỗi cảm biến kéo dài thì chúng phải dồn vào một khoảng thời gian ngắn; nếu đến từ ngưỡng đo hoặc gió lặng thật thì tỷ lệ phải ổn định theo năm và tháng.

- Tỷ lệ gần như không đổi giữa hai năm (12,81% năm 2011; 12,29% năm 2012) và theo tháng chỉ dao động từ 5,34% đến 19,03%; không tháng nào có giá trị 0 chiếm đa số. Các số 0 vì vậy không giống một sự cố cảm biến kéo dài.
- Tỷ lệ thay đổi theo giờ: 17,24% số dòng ở giờ 0–5 so với 11,01% ở giờ 6–23, cao nhất 19,30% lúc 2 giờ và thấp nhất 5,63% lúc 18 giờ. Quy luật này phù hợp cả với giả thuyết đêm lặng gió hơn ban ngày lẫn giả thuyết thiết bị chỉ ghi nhận gió trên một ngưỡng; dữ liệu chưa đủ để phân biệt.
- `cnt` trung bình của nhóm `windspeed = 0` (160,64) thấp hơn nhóm còn lại (193,60) 32,96 lượt/giờ, nhưng khi so sánh **trong cùng khung giờ** chênh lệch giảm đáng kể: 24,50 so với 24,99 ở giờ 0–5 (thấp hơn 1,96%) và 230,18 so với 244,77 ở giờ 6–23 (thấp hơn 5,96%). Khoảng cách ban đầu chủ yếu do các số 0 tập trung ở những giờ đêm vốn ít nhu cầu.

**130 ngoại lai theo (`hr`, `workingday`).** 80,00% thuộc năm 2012, 69,23% ở giờ 0–5, 76,92% có `weathersit = 1` (toàn bộ dữ liệu: 65,67%), `temp` trung bình 0,56 (toàn bộ: 0,50) và 98,46% thuộc ba mùa Spring, Summer, Fall; `cnt` của nhóm này từ 11 đến 651. Các đặc điểm này phù hợp với xu hướng tăng theo năm, mùa ấm và thời tiết tốt, không có dấu hiệu lỗi ghi nhận.

**Tính độc lập giữa các giờ liên tiếp.** Nhiều kiểm định và mô hình giả định quan sát độc lập, trong khi dữ liệu là chuỗi theo giờ. Tự tương quan bậc 1 của `cnt`, tính chỉ trên các cặp giờ liên tiếp thực sự (17.303 cặp, bỏ qua chỗ chuỗi đứt do giờ thiếu), là **0,8431**. Sau khi trừ `cnt` trung bình của từng nhóm (`hr`, `workingday`), hệ số của phần dư vẫn cao (**0,8903**). Điều này cho thấy sự phụ thuộc giữa các giờ liên tiếp không chỉ do chu kỳ trong ngày, mà còn do các điều kiện thay đổi chậm (thời tiết trong ngày, mùa, xu hướng giữa hai năm). Hệ quả là việc coi 17.379 dòng như 17.379 quan sát độc lập sẽ đánh giá quá cao mức chắc chắn của kiểm định, và việc chia tập huấn luyện/kiểm tra cần theo thứ tự thời gian.

**Bảng 1.9. Đánh giá và xử lý các nhóm giá trị ngoại lai và giá trị đáng ngờ**

| Nhóm                                                  | Bằng chứng                                                                                  | Kết luận                                                    | Xử lý                                                                                       |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `cnt` cao theo ngưỡng toàn cục (505 dòng)             | 80,99% ở giờ 8, 17, 18; 81,98% ở ngày làm việc; `cnt = casual + registered` đúng ở mọi dòng | Đỉnh giờ đi làm hợp lệ; ngưỡng toàn cục không tính đến `hr` | Giữ lại                                                                                     |
| `cnt` cao theo ngưỡng (`hr`, `workingday`) (130 dòng) | 80,00% thuộc 2012; 98,46% ở Spring–Fall; `temp` trung bình 0,56                             | Biến động theo xu hướng, mùa và thời tiết                   | Giữ lại                                                                                     |
| `casual` cao (1.192 dòng theo IQR)                    | Phân phối lệch mạnh (skewness 2,50); thành phần của `cnt` nhất quán                         | Biến động thực tế                                           | Giữ lại                                                                                     |
| `windspeed` cao (342 dòng > 0,477)                    | Giá trị lớn nhất 0,85, nằm trong thang 0–1                                                  | Cực trị thời tiết, không có bằng chứng lỗi                  | Giữ lại                                                                                     |
| Ngày 2012-10-29 (22 lượt, 1/24 giờ)                   | Không vượt ngưỡng theo ngày; tổng thấp do thiếu giờ                                         | Ngày không đầy đủ, không phải lỗi nhập liệu                 | Giữ lại; đánh dấu ngày `n_hours < 24` khi tổng hợp theo ngày                                |
| `hum = 0` (22 dòng, ngày 2011-03-10)                  | Độ ẩm 0% cả ngày là bất khả thi                                                             | **Lỗi dữ liệu**                                             | Đã thay bằng trung bình cùng giờ của ngày liền trước và liền sau; giá trị thay là ước lượng |
| `windspeed = 0` (2.180 dòng)                          | Tỷ lệ ổn định theo năm, tháng; chênh lệch `cnt` chủ yếu do giờ trong ngày                   | Chưa đủ bằng chứng là lỗi; nguyên nhân chưa xác định        | Giữ nguyên; ghi nhận là hạn chế                                                             |

**Kết luận mục 1.5:** không có quan sát nào bị loại bỏ. Các ngoại lai thống kê của `cnt` đều giải thích được bằng giờ cao điểm, mùa và xu hướng; chỉ `hum = 0` đủ bằng chứng để xếp vào lỗi dữ liệu. Khi mô hình hóa, nên ưu tiên các hướng chịu được đuôi dài (biến đổi `log1p`, mô hình cho dữ liệu đếm, mô hình cây) thay vì loại bỏ dữ liệu.

---

## 1.6. Nhận xét tổng quan

### 1.6.1. Trả lời các câu hỏi nghiên cứu

**(i) Phân phối của `cnt`.** `cnt` là biến đếm lệch phải (trung bình 189,46 > trung vị 142; skewness 1,28), phân tán vượt mức (phương sai gấp 173,66 lần trung bình) và là hỗn hợp của các giờ thấp điểm và cao điểm. Phép biến đổi `log1p` đảo độ lệch sang trái (−0,82) chứ không đưa phân phối về dạng chuẩn. Hình dạng của `cnt` chủ yếu do nhóm `registered` (81,17% tổng lượt thuê) quyết định.

**(ii) Xu hướng và mùa vụ.** Nhu cầu năm 2012 cao hơn năm 2011 là 63,20% và tăng ở cả 12 tháng; mùa vụ rõ rệt với mức thấp nhất vào tháng 1 và mức cao từ giữa năm đến đầu thu. Nguyên nhân của đà tăng chỉ có thể là giả thuyết do thiếu thông tin về quy mô hệ thống.

**(iii) Thời tiết.** Nhiệt độ có tương quan dương với `cnt` (Spearman 0,4233), độ ẩm tương quan âm (−0,3634), tốc độ gió yếu và không đơn điệu (0,1266). `cnt` trung bình tăng đơn điệu theo `temp` (gấp 5,01 lần giữa khoảng thấp nhất và cao nhất), giảm theo `hum` từ mức 0,4 trở lên và thấp hơn khi `weathersit` xấu đi (204,87; 175,17; 111,58 ở các mức 1, 2, 3). Tuy nhiên các yếu tố này đan xen với nhau, với mùa và với giờ trong ngày nên chưa tách được tác động riêng của từng yếu tố.

**(iv) `hr`, `workingday`, `season`, `weathersit`.** `hr` là biến có liên hệ mạnh nhất với `cnt` (0,5109), theo dạng chu kỳ chứ không đơn điệu. Hình dạng theo giờ phụ thuộc vào `workingday`: ngày làm việc có hai đỉnh (8 giờ và 17–18 giờ, chủ yếu do `registered`), ngày nghỉ có một đỉnh rộng cao nhất lúc 13 giờ (`casual` chiếm 36,60%). Vì vậy trung bình mỗi giờ giữa hai loại ngày chênh lệch nhỏ (193,21 và 181,41) và hệ số tương quan của `workingday` gần 0 (0,0210) dù nhịp theo giờ khác hẳn nhau; tương quan đơn biến đánh giá thấp vai trò của biến này. `season` và `weathersit` xác định mức nền khác nhau của nhu cầu nhưng các nhóm chồng lấn nhiều, chưa giải thích được giá trị của một giờ cụ thể.

**(v) Ngoại lai và vấn đề dữ liệu.** Dữ liệu sạch về cấu trúc. Các vấn đề còn lại mang tính ngữ nghĩa: 22 giá trị `hum = 0` (đã xử lý), 2.180 giá trị `windspeed = 0` (giữ nguyên), 165 giờ thiếu (không điền) và nhóm `weathersit = 4` chỉ có 3 dòng. Ba mối liên hệ cấu trúc cần chú ý là `temp`–`atemp` (0,9877), `cnt`–`casual`/`registered` (0,8505 và 0,9894) và tự tương quan giữa các giờ liên tiếp (0,8431).

### 1.6.2. Hạn chế

**Về phương pháp.**

- Chương này chỉ sử dụng thống kê mô tả và biểu đồ, chưa có kiểm định giả thuyết. Chênh lệch giữa các nhóm chỉ mô tả mẫu và có thể bị trộn lẫn bởi các yếu tố đi kèm (mùa, năm, giờ), do đó không dùng để kết luận quan hệ nhân quả.
- Hệ số Spearman chỉ đo xu hướng đơn điệu nên đánh giá thấp liên hệ có tính chu kỳ (`hr`) hoặc liên hệ qua hình dạng phân phối (`workingday`).
- Ngưỡng IQR (hệ số 1,5) và Z-score (|z| > 3) là quy ước; Z-score giả định phân phối gần chuẩn nên đánh dấu ít hơn IQR (244 so với 505 dòng).

**Về dữ liệu.**

- 22 giá trị `hum` thay thế chỉ là ước lượng; số liệu độ ẩm của ngày 2011-03-10 chỉ nên diễn giải ở mức xấp xỉ.
- Bản chất của 2.180 giá trị `windspeed = 0` (gió lặng thật hay dưới ngưỡng đo) chưa xác định được.
- 165 giờ thiếu không được điền, nên tổng lượt thuê theo ngày của các ngày thiếu giờ không so sánh được với ngày đủ 24 giờ; nhóm `weathersit = 4` (3 dòng) không đủ để thống kê.
- Dữ liệu chỉ gồm hai năm của một hệ thống ở một thành phố: tính mùa vụ được ước lượng từ hai chu kỳ và khả năng khái quát hóa sang thời điểm hoặc hệ thống khác bị hạn chế. Dữ liệu cũng không có thông tin về quy mô hệ thống hay các sự kiện đặc biệt.

**Về cấu trúc dữ liệu.**

- Các quan sát theo giờ không độc lập (tự tương quan bậc 1 là 0,8431, và 0,8903 sau khi trừ trung bình theo nhóm).
- Biến thời tiết ở thang chuẩn hóa; diễn giải theo đơn vị gốc cần quy đổi theo công thức ở mục 1.1.3.

### 1.6.3. Hàm ý cho các bước tiếp theo

| Nội dung                   | Hàm ý                                                                                                                                                                                                                                                                            |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Phân phối của `cnt`        | Xét các họ phân phối cho dữ liệu đếm (Poisson, Negative Binomial) hoặc mô hình cây; xét phân phối theo nhóm (`hr`, `workingday`) vì phân phối gộp là hỗn hợp; quyết định biến đổi `log1p` theo từng mô hình cụ thể                                                               |
| Kiểm định thống kê         | Do các quan sát không độc lập, p-value đánh giá quá cao mức chắc chắn; với cỡ mẫu lớn, khác biệt rất nhỏ cũng có thể có ý nghĩa thống kê nên cần báo cáo độ lớn hiệu ứng (effect size) và so sánh trong cùng khung giờ hoặc loại ngày; loại hoặc gộp `weathersit = 4` vào nhóm 3 |
| Tương quan và biến độc lập | Kiểm tra đa cộng tuyến (ví dụ bằng VIF) cho các cặp `temp`–`atemp`, `hum`–`weathersit`, `temp`–`season`; không dùng `casual` và `registered` làm biến độc lập                                                                                                                    |
| Chia dữ liệu               | Chia tập huấn luyện/kiểm tra theo thứ tự thời gian vì nhu cầu năm 2012 cao hơn 2011; xáo trộn ngẫu nhiên sẽ làm rò rỉ thông tin tương lai                                                                                                                                        |
| Xây dựng đặc trưng         | Mã hóa `hr`, `mnth`, `weekday` theo dạng chu kỳ hoặc one-hot; xét tương tác `hr` × `workingday`; thận trọng khi tạo đặc trưng trễ vì chuỗi có 165 giờ thiếu                                                                                                                      |
| Đánh giá mô hình           | Nếu biến đổi `cnt`, đánh giá cuối cùng cần quy về thang gốc; đánh dấu ngày 2012-10-29 khi phân tích sai số                                                                                                                                                                       |

---

## Tài liệu tham khảo

Fanaee-T, H., & Gama, J. (2013). Event labeling combining ensemble detectors and background knowledge. _Progress in Artificial Intelligence_, 2(2–3), 113–127. Bộ dữ liệu _Bike Sharing Dataset_, UCI Machine Learning Repository.

---

<!-- GHI CHÚ CHO NGƯỜI SOẠN (có thể xóa): đối chiếu số hiệu hình/bảng với notebook gốc
Hình 1.1 = 1.1 | Hình 1.2 = 1.2 | Hình 1.3 = 1.3 | Hình 1.4 = 1.5 | Hình 1.5 = 1.6 | Hình 1.6 = 1.7 | Hình 1.7 = 1.8 | Hình 1.8 = 1.9 | Hình 1.9 = 1.10
Các hình lược bỏ: 1.4 (phân phối 4 biến thời tiết), 1.11 (phân bố ngoại lai theo giờ và loại ngày).
Bảng 1.4 (mới) = Bảng 1.3 | Bảng 1.5 = 1.4–1.7 | Bảng 1.6 = tóm tắt từ Bảng 1.8 + Hình 1.6 | Bảng 1.7 = 1.9 | Bảng 1.8 = 1.10 | Bảng 1.9 = 1.12 -->
