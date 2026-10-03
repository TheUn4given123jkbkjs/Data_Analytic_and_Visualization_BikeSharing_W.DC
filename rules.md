# QUY CHUẨN CHUNG KHI VIẾT BÁO CÁO VÀ PHÂN TÍCH DỮ LIỆU

> Áp dụng cho cả nhóm, đi kèm `outline.md`.
> Dataset: `hour.csv` (Bike Sharing Dataset). Báo cáo gồm 6 phần, **mỗi thành viên tự viết phần của mình** theo cùng một quy chuẩn, sau đó TV3 gộp lại.

---

## 1. Nguyên tắc chung

Mọi phần phân tích đều phải trả lời được 4 câu hỏi:

> **Mục tiêu → Phương pháp → Kết quả → Nhận xét**

* **Mục tiêu:** Phân tích cái gì? Để trả lời câu hỏi nào?
* **Phương pháp:** Dùng phương pháp/biểu đồ/kiểm định nào? Vì sao?
* **Kết quả:** Thu được con số, biểu đồ hoặc kết quả thống kê gì?
* **Nhận xét:** Kết quả đó có ý nghĩa gì đối với dữ liệu?

Không chỉ đưa code hoặc biểu đồ mà không giải thích.

**Cấu trúc bắt buộc của mỗi phần:** mở đầu bằng mục tiêu của phần, trình bày phân tích theo outline, và **kết thúc bằng mục "Kết luận và hạn chế của phần"** (vì báo cáo không có phần Kết luận tổng quát riêng). Mục này gồm:

1. Các kết quả chính của phần (kèm số liệu cụ thể).
2. Hạn chế của chính phương pháp/dữ liệu được dùng trong phần đó.
3. Điều phần sau cần lưu ý (nếu có).

---

## 2. Quy chuẩn số liệu và định dạng

### 2.1. Số thập phân

**Luôn sử dụng dấu `.` làm dấu thập phân.** Ví dụ: `8.34`, `0.05`, `12.57%`.

**Không sử dụng dấu `,` cho số thập phân.** Ví dụ không dùng: `8,34`, `0,05`.

Số lớn dùng dấu `,` ngăn cách hàng nghìn theo kiểu tiếng Anh (ví dụ `17,379` dòng). Cả nhóm dùng thống nhất một kiểu, không trộn.

Làm tròn thống nhất: hệ số tương quan, p-value, R² lấy **4 chữ số thập phân**; các số đo theo đơn vị (RMSE, MAE, mean, std) lấy **2 chữ số thập phân**. p-value rất nhỏ ghi `p < 0.001`.

### 2.2. Đơn vị và biến đã chuẩn hóa

Luôn ghi rõ đơn vị khi có thể. Ví dụ: `RMSE = 42.31 lượt thuê`.

Các biến `temp`, `atemp`, `hum`, `windspeed` trong `hour.csv` là **giá trị đã chuẩn hóa** theo mô tả của dataset. Cả nhóm thực hiện đúng quyết định chung đã chốt ở Phase 0 (giữ giá trị chuẩn hóa hay quy đổi về đơn vị gốc) và **luôn ghi rõ trạng thái của biến** khi nêu số liệu. Ví dụ:

* `windspeed = 0.21` (giá trị chuẩn hóa)
* `Temperature = 25.4 °C` (sau khi quy đổi)

Không được trộn hai cách ghi trong cùng một báo cáo.

### 2.3. Tên biến

Giữ nguyên tên biến của dataset trong code và khi phân tích: `cnt`, `temp`, `atemp`, `hum`, `windspeed`, `workingday`, `season`, `weathersit`, `hr`...

Ở lần xuất hiện đầu tiên trong phần của mình, giải thích tên biến. Ví dụ: Tổng số lượt thuê (`cnt`). Sau đó dùng trực tiếp `cnt`.

### 2.4. Vai trò của biến (cả nhóm tuân thủ)

* **Biến mục tiêu:** `cnt` (hoặc dạng biến đổi của `cnt` nếu nhóm thống nhất, và phải ghi rõ).
* **`casual` và `registered` không được dùng làm biến độc lập khi dự đoán `cnt`** vì `cnt = casual + registered` (rò rỉ dữ liệu – data leakage). Có thể dùng để mô tả hoặc phân tích tương quan nhưng phải ghi chú.

---

## 3. Quy chuẩn thuật ngữ

Lần đầu tiên xuất hiện phải viết **English + Vietnamese + viết tắt** nếu có. Ví dụ:

> Phân tích khám phá dữ liệu (Exploratory Data Analysis – EDA)

> Hồi quy tuyến tính đa biến (Multiple Linear Regression – MLR)

Sau đó chỉ dùng: EDA, MLR.

**Bảng thuật ngữ chung (cả nhóm dùng đúng cách dịch này, không tự đổi):**

| English | Tiếng Việt | Viết tắt |
|---|---|---|
| Exploratory Data Analysis | Phân tích khám phá dữ liệu | EDA |
| Multiple Linear Regression | Hồi quy tuyến tính đa biến | MLR |
| Outlier | Giá trị ngoại lai | — |
| Multicollinearity | Đa cộng tuyến | — |
| Variance Inflation Factor | Hệ số phóng đại phương sai | VIF |
| Data leakage | Rò rỉ dữ liệu | — |
| Null hypothesis / Alternative hypothesis | Giả thuyết không / Giả thuyết đối | H0 / H1 |
| Effect size | Độ lớn hiệu ứng | — |
| Autocorrelation | Tự tương quan | — |
| Residual | Phần dư | — |
| Training set / Test set | Tập huấn luyện / Tập kiểm tra | — |
| Mean Absolute Error | Sai số tuyệt đối trung bình | MAE |
| Root Mean Squared Error | Căn sai số bình phương trung bình | RMSE |

Ai cần thêm thuật ngữ mới thì bổ sung vào bảng này (trong `HANDOFF.md`) và báo cả nhóm trước khi dùng.

**Khi mỗi người tự viết:** trong phần của mình, giải thích thuật ngữ ở lần đầu xuất hiện. Khi gộp báo cáo, TV3 giữ phần giải thích ở lần xuất hiện đầu tiên theo **thứ tự trong báo cáo**, và đổi các lần sau thành viết tắt.

---

## 4. Quy chuẩn viết biểu đồ

Mỗi biểu đồ phải có:

### 4.1. Tên biểu đồ

Đánh số theo phần của người viết, ví dụ:

> **Hình 1.3. Phân phối tổng số lượt thuê theo giờ**

Quy ước số phần: **1.x** (EDA), **2.x** (Phân phối), **3.x** (Kiểm định), **4.x** (Tương quan), **5.x** (Lý thuyết và bài toán hồi quy), **6.x** (Mô hình). Không dùng số của phần khác để tránh trùng khi gộp.

### 4.2. Mục đích

Nêu biểu đồ dùng để tìm hiểu điều gì.

### 4.3. Lý do lựa chọn

Giải thích tại sao biểu đồ này phù hợp với loại dữ liệu/câu hỏi đang phân tích.

### 4.4. Nhận xét

Không viết chung chung kiểu "Biểu đồ cho thấy dữ liệu có sự thay đổi." Phải chỉ ra **thay đổi gì, theo hướng nào, ở đâu và đáng chú ý ở điểm nào**. Ví dụ:

> Số lượt thuê tăng rõ rệt vào các khung giờ cao điểm và đạt mức cao hơn vào khoảng 8 giờ và 17–18 giờ. Điều này cho thấy thời điểm trong ngày có mối liên hệ đáng kể với nhu cầu sử dụng xe.

### 4.5. Yêu cầu kỹ thuật

* Có tiêu đề trục và đơn vị.
* Với dữ liệu ~17,000 dòng, scatter plot dễ bị dính điểm: dùng `alpha` thấp, hexbin hoặc lấy mẫu có ghi chú.
* Mỗi hình đủ rõ khi in; font chữ không bị nhỏ.
* Lưu hình trong thư mục chung, tên file theo số hình (ví dụ `fig_1_3_cnt_by_hour.png`).

---

## 5. Quy chuẩn viết bảng

Mỗi bảng cần có:

> **Bảng X.X. [Tên bảng]**

Sau bảng phải có **nhận xét**, không để bảng đứng một mình. Ví dụ:

> Bảng 1.2 cho thấy giá trị trung bình của `cnt` cao hơn đáng kể so với trung vị, cho thấy phân phối lượt thuê có xu hướng lệch phải.

Không cần mô tả lại toàn bộ từng ô; chỉ tập trung vào thông tin đáng chú ý.

---

## 6. Quy chuẩn viết phân tích thống kê

Phải phân biệt:

### Thống kê mô tả

> Trong mẫu dữ liệu, ...

> Giá trị trung bình của `cnt` là ...

### Kiểm định giả thuyết

Dùng:

> Có bằng chứng thống kê cho thấy ...

hoặc:

> Chưa đủ bằng chứng thống kê để bác bỏ giả thuyết không.

Không viết "Chấp nhận H0."

Nếu sử dụng mức ý nghĩa `α = 0.05`:

* `p-value < 0.05` → **bác bỏ H0**
* `p-value ≥ 0.05` → **chưa đủ bằng chứng bác bỏ H0**

Không gọi `p-value` là "confidence level".

### Lưu ý với mẫu lớn (`hour.csv` có hơn 17,000 dòng)

* Với mẫu rất lớn, kiểm định gần như luôn cho p-value rất nhỏ ngay cả khi chênh lệch rất nhỏ. **Vì vậy ngoài p-value, phải báo cáo độ lớn hiệu ứng (effect size)** (Cohen's d, eta-squared, Cramér's V...) và nhận xét ý nghĩa thực tiễn.
* Các kiểm định kiểm tra tính chuẩn (Shapiro–Wilk, Kolmogorov–Smirnov...) với mẫu lớn dễ bác bỏ chuẩn dù độ lệch nhỏ. **Kết hợp đánh giá bằng biểu đồ (histogram, Q–Q plot), độ lệch, độ nhọn**, không chỉ dựa vào p-value.
* Dữ liệu theo giờ liên tiếp **không hoàn toàn độc lập** (có tự tương quan theo thời gian). Phần nào dùng giả định độc lập phải nêu điều này trong "Kết luận và hạn chế của phần".

---

## 7. Không nhầm tương quan với quan hệ nhân quả

Khi phân tích tương quan, viết:

> `X` và `Y` có tương quan ...

Không tự kết luận `X` gây ra `Y` chỉ dựa trên correlation. Ví dụ:

> `temp` có tương quan dương với `cnt`.

Không viết "Nhiệt độ làm tăng số lượt thuê" trừ khi có thiết kế nghiên cứu đủ để chứng minh quan hệ nhân quả.

Lưu ý: `hr` có quan hệ chu kỳ với `cnt` nên hệ số tương quan tuyến tính có thể thấp dù mối liên hệ mạnh. Khi diễn giải phải nói rõ, không kết luận "không liên quan" chỉ vì hệ số thấp.

---

## 8. Quy chuẩn nhận xét

Mỗi nhận xét nên theo logic:

> **Quan sát → Bằng chứng → Ý nghĩa**

Ví dụ:

> `cnt` có phân phối lệch phải, thể hiện qua việc giá trị trung bình cao hơn trung vị. Điều này cho thấy một số thời điểm có lượng thuê rất cao và kéo giá trị trung bình lên.

Tránh các nhận xét không có căn cứ như:

* "Có vẻ như..."
* "Có thể thấy khá rõ..."
* "Dữ liệu rất tốt..."
* "Biểu đồ rất đẹp..."
* "Biến này ảnh hưởng mạnh..." nếu chưa có phân tích chứng minh.

---

## 9. Quy chuẩn viết công thức

1. Nói công thức dùng để làm gì.
2. Đưa công thức.
3. Giải thích các ký hiệu cần thiết.
4. Nếu cần, đưa kết quả áp dụng vào dataset.

Không cần giải thích toán học quá sâu nếu nội dung đó không phục vụ trực tiếp cho bài phân tích. Ký hiệu thống nhất giữa các phần (ví dụ biến mục tiêu `Y`, biến độc lập `X`, hệ số hồi quy `β`).

---

## 10. Liên kết giữa các phần và quy tắc VALIDATE

Các phần **không được làm hoàn toàn độc lập**. Kết quả của phần trước là cơ sở cho phần sau. Ví dụ:

> EDA phát hiện `temp` có mối quan hệ đáng chú ý với `cnt` → kiểm tra phân phối → đặt câu hỏi nghiên cứu → kiểm định / tương quan → đưa biến vào MLR nếu phù hợp.

Để 5 người làm song song, cả nhóm dùng **thẻ VALIDATE** (định nghĩa trong `outline_v3_parallel.md`):

1. **Làm trước bằng giả định tạm** được phép, nhưng giả định tạm **không được xuất hiện thành kết luận cuối** trong báo cáo.
2. **Khi làm tới đoạn có thẻ VALIDATE, bắt buộc đối chiếu lại** với kết quả chính thức (FINAL) của người upstream trước khi viết kết luận. Nếu khác giả định tạm thì chạy lại và cập nhật phần của mình.
3. **Khi kết quả của mình thay đổi sau khi đã giao**, người upstream phải ghi **CHANGE** vào `HANDOFF.md` và báo người bị ảnh hưởng. Người downstream nhận CHANGE phải chạy lại phần của mình.
4. **Phát hiện liên quan đến phần khác phải thông báo cho người phụ trách phần đó.** Ví dụ: `temp` và `atemp` có tương quan rất cao → TV4 và TV5 phải kiểm tra đa cộng tuyến.
5. Mọi thẻ VALIDATE, ghi chú giả định tạm, ghi chú `HANDOFF` **phải được xóa khỏi tài liệu trước khi nộp bản cho TV3 gộp**. Báo cáo cuối không chứa nội dung quy trình nội bộ.

---

## 11. Quy chuẩn riêng cho từng loại phân tích

### EDA (Phần 1)

* Dữ liệu gồm những gì? Bao nhiêu bản ghi/biến? Kiểu dữ liệu?
* Missing/duplicate? Giá trị bất hợp lệ? Giờ bị thiếu trong chuỗi thời gian?
* Thống kê mô tả (mean, median, std, Q1/Q3, IQR)?
* Ít nhất 3 loại biểu đồ, có lý do chọn.
* Outlier: phương pháp phát hiện, phân biệt statistical outlier với data error, quyết định giữ/loại và lý do.
* Vì báo cáo không có phần Giới thiệu riêng, phần 1.1 nêu ngắn gọn bối cảnh Bike Sharing và mục tiêu chung.

### Probability Distribution (Phần 2)

* Biến nào được chọn? Tại sao?
* Phân phối có dạng gì? Có phù hợp với phân phối lý thuyết nào không (kể cả với biến đếm như `cnt`: Poisson, Negative Binomial...)?
* Biểu đồ và thống kê hỗ trợ nhận xét gì?

### Hypothesis Testing (Phần 3)

Mỗi câu hỏi nghiên cứu cần có:

> Research Question → H0/H1 → α → Test → kiểm tra giả định → p-value → effect size → Kết luận

* Không chọn kiểm định trước rồi cố tạo câu hỏi cho phù hợp.
* Giải thích vì sao dùng test tham số hay phi tham số, dựa trên kết quả phân phối.
* Hai câu hỏi không trùng với phần tương quan.

### Correlation (Phần 4)

* Biến nào được phân tích? Pearson hay Spearman? Vì sao?
* Hệ số tương quan, mức độ và chiều, ý nghĩa thực tế.
* Cặp biến tương quan cao với nhau (ví dụ `temp`–`atemp`) phải được ghi lại để bàn giao cho người làm MLR.

### Multiple Linear Regression (Phần 5 và 6)

* Phần 5 (lý thuyết và bài toán): biến mục tiêu `Y`, các biến độc lập `X`, lý do chọn/loại từng biến, mục đích dự đoán.
* Phần 6 (xây dựng và đánh giá): cách xử lý biến, cách chia train/test (random hay chronological, lý do), huấn luyện, metric (R², Adjusted R², MAE, RMSE, ghi đơn vị lượt thuê), kiểm tra giả định (tuyến tính, độc lập, phương sai không đổi, phần dư, đa cộng tuyến), nhận xét.
* **Phần 5.2.2 và phần 6 phải mô tả cùng một tập biến cuối cùng**, cùng lý do chọn.
* Nếu biến đổi `cnt` (ví dụ log), đánh giá cuối phải **quy về thang gốc** để metric có đơn vị rõ ràng.
* Không cần biến phần này thành một bài Machine Learning quá sâu.

---

## 12. Quy chuẩn code

Cả nhóm thống nhất:

* Cùng phiên bản Python và thư viện chính (ghi trong `requirements.txt`).
* Cùng dataset đầu vào `hour.csv`, đọc qua hàm chung `load_data()` trong `common.py`. Khi TV1 xuất `bike_clean.csv`, chỉ đổi đường dẫn trong `common.py`.
* `SEED = 42` đặt trong `common.py`, mọi nơi có yếu tố ngẫu nhiên đều dùng giá trị này.
* Code phải chạy lại được từ đầu đến cuối, không phụ thuộc đường dẫn cá nhân (dùng đường dẫn tương đối).
* **Không sửa dataset gốc trực tiếp.**
* Mỗi file code có phần chú thích đầu file: người viết, mục đích, đầu vào, đầu ra.

Tên file:

```text
common.py
01_eda.py
02_distribution.py
03_hypothesis_testing.py
04_correlation.py
05_regression_setup.py
06_model.py
```

---

## 13. Quy chuẩn bàn giao

### 13.1. Bàn giao giữa các thành viên (upstream → downstream)

Dùng `HANDOFF.md` với nhãn **DRAFT / FINAL / CHANGE**:

```text
[Ngày giờ] [TVx] [FINAL | DRAFT | CHANGE] [Phần] — nội dung — ai bị ảnh hưởng (V-xx)
```

Các upstream giao **Findings Sheet** (1 trang) gồm: dữ liệu/biến đã dùng (kèm phiên bản file); phương pháp; kết quả chính (số liệu có đơn vị); quyết định và lý do; điều downstream cần lưu ý; tên file code, hình, bảng.

* **EDA Findings** (TV1), **Distribution Findings** (TV2), **Correlation Findings** và **Feature Candidate** (TV4).

Không chỉ gửi file code rồi để người khác tự đoán kết quả.

### 13.2. Bàn giao phần của mình cho TV3 gộp

Mỗi người nộp đủ **5 thành phần**:

1. Tài liệu phần của mình (đã bỏ thẻ VALIDATE và ghi chú nội bộ).
2. Code (chạy lại được).
3. Hình và bảng đã đánh số theo phần, kèm nhận xét.
4. Nguồn tham khảo đã ghi.
5. Dòng khai đóng góp: phần đã làm, tỷ lệ, mức độ hoàn thành.

### 13.3. TV3 khi gộp

* Kiểm tra đánh số hình/bảng, thuật ngữ (theo bảng ở mục 3), đơn vị, số thập phân.
* Đối chiếu số liệu giữa các phần (ví dụ số dòng, hệ số tương quan được nhắc lại ở nhiều phần phải khớp nhau).
* Lập mục lục, danh mục tài liệu tham khảo, bảng đóng góp.
* Phát hiện chỗ không nhất quán thì trả về người phụ trách sửa, không tự đổi số liệu.

---

## 14. Quy chuẩn tài liệu tham khảo

Khi sử dụng dataset, giáo trình, paper, documentation, website học thuật, tài liệu thống kê → **ghi lại nguồn ngay khi sử dụng**, không để đến cuối mới nhớ.

Mỗi nguồn ghi tối thiểu: tác giả/tổ chức, tên tài liệu, năm, đường dẫn (nếu có), ngày truy cập (với trang web). Dùng một kiểu trích dẫn thống nhất cả nhóm (ví dụ APA) do TV3 chốt ở Phase 0.

Dataset phải được trích dẫn: Bike Sharing Dataset (Kaggle) và nguồn gốc của nó theo mô tả trên trang dataset.

---

## 15. Quy định nộp bài (theo đề)

* Nộp báo cáo dưới dạng **Word (.doc/.docx) và PDF**, kèm **mã nguồn Python**.
* Tất cả file được nén, **đặt tên file nén theo mã số sinh viên**. Báo cáo ghi tên các thành viên; **mỗi bạn tự nộp bài lên hệ thống**.
* Trong bài phải nói rõ: **phần mỗi sinh viên thực hiện, tỷ lệ đóng góp, mức độ hoàn thành**.
* Bài làm tuân theo quy định của khoa; số trang **không tính trang bìa, danh mục tài liệu tham khảo và mục lục**. Kiểm tra giới hạn số trang trước khi gộp.
* Hạn cuối: **23h59 ngày 13/10/2026**. Nộp sớm trong ngày.
* Bộ dữ liệu phải khác với các bộ đã dùng trong bài giữa kỳ.
* Slide và video: theo quyết định của nhóm, đề tài này không làm. Cần xác nhận với giảng viên để tránh sai sót.

---

## 16. Quy chuẩn quan trọng nhất

Toàn bộ báo cáo phải có **một cách viết thống nhất**, dù được chia cho nhiều người. Mỗi người trước khi nộp phần của mình tự kiểm tra:

> **Tôi đang phân tích cái gì?**
> **Tại sao dùng phương pháp này?**
> **Kết quả cụ thể là gì?**
> **Kết quả đó nói lên điều gì?**
> **Có chỗ nào đang dùng giả định tạm chưa được validate không?**

Nếu một biểu đồ, bảng, phép kiểm định hoặc mô hình **không giúp trả lời một câu hỏi cụ thể**, cần xem xét lại việc đưa nó vào báo cáo.