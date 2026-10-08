# Outline báo cáo cuối kỳ — Bike Sharing Dataset (làm song song, mỗi người tự viết phần của mình)

> **Dataset:** `hour.csv` (Bike Sharing Dataset, Kaggle). Cả nhóm dùng duy nhất file này.
> **Nguyên tắc nhóm:** EDA trước → phát hiện từ dữ liệu → đặt câu hỏi → chọn phương pháp → phân tích → kết luận.
> **Phạm vi báo cáo:** gồm 6 phần (1–6). Không có phần Giới thiệu/Abstract, không có phần Kết luận tổng quát, không làm slide/video.

---

## A. Cách đọc tài liệu này

Để 5 người làm cùng lúc mà không ai phải chờ ai, outline áp dụng 3 cơ chế:

1. **Phase 0 (làm chung, ~1 buổi):** chốt "hợp đồng dữ liệu" để mọi người xuất phát từ cùng một điểm.
2. **Giả định tạm:** ở mỗi chỗ phụ thuộc phần khác, có sẵn một giả định tạm để người làm bắt đầu ngay.
3. **Thẻ VALIDATE:** mọi chỗ dùng thông tin từ "tầng trên" đều có thẻ bên dưới. **Khi làm tới đoạn có thẻ này, người phụ trách bắt buộc phải đối chiếu lại với kết quả chính thức của người upstream, không được dùng giả định tạm làm kết luận cuối.**

> ⚠️ **[V-xx] VALIDATE** — nhận từ **TVa**, dùng bởi **TVb**
> - **Cần gì:** thông tin cần lấy.
> - **Giả định tạm:** làm tạm theo giả định này.
> - **Phải kiểm tra lại:** điều cần đối chiếu.
> - **Nếu khác:** việc phải làm.

Danh sách đầy đủ các thẻ nằm ở **Mục 8 (Sổ theo dõi phụ thuộc)**.

### Phân công

| Thành viên | Phần phụ trách (tự viết tài liệu, code, hình, bảng, nhận xét, nguồn tham khảo của phần mình) |
|---|---|
| **TV1** | Phần 1: EDA |
| **TV2** | Phần 2: Phân phối xác suất |
| **TV3** | Phần 3: Kiểm định giả thuyết. **Thêm:** gộp báo cáo (Word/PDF), mục lục, danh mục tài liệu tham khảo, bảng đóng góp |
| **TV4** | Phần 4 + 5: Tương quan, lý thuyết và bài toán hồi quy |
| **TV5** | Phần 6: Xây dựng và đánh giá mô hình |

### Mỗi người nộp cho TV3 (đúng 5 thành phần theo rules mục 13)

1. File tài liệu phần của mình (Word hoặc Markdown, theo rules).
2. Code (`0x_*.py`), chạy lại được.
3. Hình và bảng đã đánh số theo phần.
4. Nguồn tham khảo đã ghi ngay khi dùng.
5. Dòng khai đóng góp: phần đã làm, tỷ lệ, mức độ hoàn thành.

> Vì không có phần kết luận tổng quát, **mỗi phần phải kết thúc bằng mục "Kết luận và hạn chế của phần"** (xem 1.5, 2.5, 3.3, 4.5, 5.3, 6.6). Đây là nơi người viết tự nêu kết luận và hạn chế của chính phương pháp mình dùng.

---

## B. Phase 0 — Hợp đồng dữ liệu (cả nhóm làm chung, trước khi chia nhau đi)

**B.1. File và cách đọc dữ liệu**

- Dùng `hour.csv` gốc, **không sửa trực tiếp**. Mọi người đọc qua hàm chung `load_data()` trong `common.py` (đọc file, chuyển `dteday` sang datetime, gán nhãn các biến). Khi TV1 xuất `bike_clean.csv`, chỉ cần đổi đường dẫn trong `common.py`.
- `SEED = 42` đặt trong `common.py`. Cùng phiên bản Python và thư viện (`requirements.txt`).
- Quy ước đánh số hình/bảng theo phần để không trùng khi gộp: **Hình/Bảng 1.x** (TV1), **2.x** (TV2), **3.x** (TV3), **4.x và 5.x** (TV4), **6.x** (TV5).

**B.2. Vai trò của các biến**

| Nhóm | Biến |
|---|---|
| Định danh/thời gian | `instant`, `dteday`, `yr`, `mnth`, `hr`, `weekday` |
| Categorical | `season`, `holiday`, `workingday`, `weathersit` |
| Numerical (liên tục) | `temp`, `atemp`, `hum`, `windspeed` |
| Biến mục tiêu | `cnt` |
| **Cấm đưa vào mô hình dự đoán `cnt`** (data leakage) | `casual`, `registered` (vì `cnt = casual + registered`) |

**B.3. Các quyết định chung cần chốt trong Phase 0**

- Đơn vị của `temp`, `atemp`, `hum`, `windspeed`: theo mô tả dataset, các biến này đã được chuẩn hóa. **Chốt: giữ giá trị chuẩn hóa hay quy đổi về đơn vị gốc**, ghi rõ trong báo cáo (rules mục 2.2). TV1 đối chiếu hệ số quy đổi với tài liệu mô tả dataset trước khi thực hiện.
- Quy ước số thập phân (dấu `.`), thuật ngữ English + Vietnamese + viết tắt, cách viết kết luận kiểm định (rules mục 2, 3, 6). **Vì mỗi người tự viết nên phải thống nhất thuật ngữ và cách dịch ngay từ đầu**, đặc biệt các thuật ngữ dùng chung: EDA, MLR, Multicollinearity, Outlier, Data leakage.
- Kênh trao đổi và file `HANDOFF.md` (Mục 7).

---

# 1. Khám phá dữ liệu (EDA) — *TV1*

> **TV1 là upstream của cả nhóm.** Ưu tiên giao sớm: (a) `bike_clean.csv` và (b) EDA Findings Sheet (mẫu ở Mục 7). Phần trình bày chi tiết có thể hoàn thiện sau.

## 1.1. Tổng quan dữ liệu

- Nguồn, số bản ghi, số biến, kiểu dữ liệu, ý nghĩa các biến, phân loại biến (Numerical / Categorical / Date-Time). Vì báo cáo không có phần giới thiệu riêng, **phần này đồng thời giới thiệu bối cảnh bài toán Bike Sharing và mục tiêu phân tích chung** (ngắn gọn).

### 1.1.1. Kiểm tra chất lượng dữ liệu
- Missing values, duplicate records, giá trị bất hợp lệ (ví dụ `hr` ngoài 0–23, `hum = 0`).
- Dữ liệu theo giờ có thể **thiếu một số khung giờ** (không có lượt thuê nên không có dòng). Kiểm tra và ghi nhận vì ảnh hưởng đến chuỗi thời gian ở phần 6.

### 1.1.2. Tiền xử lý dữ liệu
- Xử lý missing/duplicate, chuyển kiểu dữ liệu, chuẩn hóa định dạng thời gian, thực hiện quyết định đơn vị ở B.3.
- **Không quyết định phương pháp xử lý trước khi kiểm tra dữ liệu.**
- **Nếu tiền xử lý làm thay đổi số dòng hoặc giá trị biến, báo cả nhóm ngay (CHANGE trong `HANDOFF.md`).**

## 1.2. Thống kê mô tả

### 1.2.1. Thống kê các biến số
- Mean, Median, Std, Min/Max, Q1/Q3, IQR. Tập trung vào `cnt` và các biến số có khả năng giải thích `cnt`.

### 1.2.2. Trực quan hóa (ít nhất 3 loại biểu đồ, có lý do chọn)
- Histogram, Boxplot, Bar chart, Line chart, Scatter plot. Mỗi biểu đồ theo rules mục 4: tên, mục đích, lý do chọn, nhận xét cụ thể.
- Chủ đề nên có: phân bố `cnt`; `cnt` theo `hr` (tách `workingday`); `cnt` theo `season` và `weathersit`; xu hướng theo thời gian; `cnt` theo `temp`.

## 1.3. Phát hiện và xử lý ngoại lai

- Phát hiện: IQR, Z-score, boxplot. **Statistical outlier ≠ data error.** Không mặc định xóa.
- **Quyết định cuối về ngoại lai ảnh hưởng phần 2, 3, 4, 6**, ghi rõ trong Findings Sheet: giữ hay loại, tiêu chí, bao nhiêu dòng.

## 1.4. Nhận xét tổng quan EDA

- Đặc điểm dữ liệu, phân bố `cnt`, xu hướng thời gian, quan hệ thời tiết–nhu cầu, khác biệt theo `hr`/`workingday`/`season`/`weathersit`, vấn đề dữ liệu cần lưu ý (ví dụ nhóm `weathersit = 4` có rất ít quan sát, nếu đúng như vậy).
- **Kết quả phần này là đầu vào cho phần 2–6.**

## 1.5. Kết luận và hạn chế của phần 1
- Tóm tắt phát hiện chính của EDA; hạn chế (một hệ thống, hai năm, giá trị đã chuẩn hóa, giờ bị thiếu...).

---

# 2. Phân tích phân phối xác suất — *TV2*

Mục tiêu: xác định đặc điểm phân phối của ít nhất hai biến số quan trọng và mức độ phù hợp với các phân phối lý thuyết.

## 2.1. Lựa chọn biến phân tích

- **Ứng viên ban đầu:** `cnt` và `temp`. `hr`, `workingday`, `season` quan trọng để giải thích `cnt` nhưng không nhất thiết phù hợp để khớp phân phối liên tục.

> ⚠️ **[V-02] VALIDATE** — nhận từ **TV1** (EDA Findings Sheet)
> - **Cần gì:** biến nào có ý nghĩa với bài toán, quyết định về ngoại lai, đã quy đổi đơn vị chưa.
> - **Giả định tạm:** `cnt` và `temp`, chưa loại ngoại lai, giá trị chuẩn hóa.
> - **Phải kiểm tra lại:** biến chọn còn hợp lý sau EDA; kết quả khớp phân phối thay đổi thế nào nếu ngoại lai bị loại.
> - **Nếu khác:** đổi biến hoặc chạy lại và cập nhật 2.2–2.4.

## 2.2. Phân tích phân phối biến 1 (gợi ý `cnt`)

- Phân phối quan sát được, visualization (histogram + đường phân phối lý thuyết, Q–Q plot), độ lệch, độ nhọn.
- `cnt` là biến đếm nên **xem xét Poisson, Negative Binomial, hoặc dạng liên tục lệch phải**, và đối chiếu variance với mean. Có phù hợp hay không do dữ liệu quyết định.
- Với mẫu ~17,000 dòng, kiểm định mức độ phù hợp (Kolmogorov–Smirnov, chi-square goodness-of-fit...) gần như luôn bác bỏ. **Kết hợp đánh giá bằng đồ thị, độ lệch, độ nhọn, không chỉ dựa vào p-value.**

## 2.3. Phân tích phân phối biến 2 (gợi ý `temp`)
Tương tự 2.2.

## 2.4. Nhận xét
- Hai biến có phân phối gì, lệch không, gần Normal không, ảnh hưởng thế nào đến các bước sau. Có thể xem thêm phân phối theo nhóm (ví dụ `cnt` theo `workingday`) vì phần 3 so sánh giữa các nhóm.
- **Xuất Distribution Findings Sheet (Mục 7)** cho TV3, TV4, TV5.

## 2.5. Kết luận và hạn chế của phần 2

---

# 3. Kiểm định giả thuyết — *TV3*

## 3.1. Lý thuyết các phương pháp kiểm định — *làm ngay, không phụ thuộc ai*

- t-test, Chi-square, ANOVA: mục đích, khi nào dùng, H₀/H₁, thống kê kiểm định, p-value, mức ý nghĩa, cách diễn giải, giả định.

## 3.2. Xây dựng câu hỏi nghiên cứu

Tiêu chí: có ý nghĩa với Bike Sharing; kiểm định được bằng dữ liệu; phù hợp t-test/Chi-square/ANOVA; **không trùng** với phần tương quan/hồi quy; giải thích được rõ ràng.

> ⚠️ **[V-03] VALIDATE** — nhận từ **TV1** (EDA Findings Sheet)
> - **Cần gì:** nhóm nào thực sự khác biệt trong EDA, cỡ mẫu từng nhóm, quyết định ngoại lai.
> - **Giả định tạm:** TV3 tự EDA nhẹ trên `hour.csv` để lập **danh sách ứng viên** (gợi ý dưới). Chỉ là ứng viên, chưa chốt.
> - **Phải kiểm tra lại:** câu hỏi chốt khớp với EDA chính thức; cỡ mẫu nhóm đủ cho kiểm định (đặc biệt tần số kỳ vọng của Chi-square).
> - **Nếu khác:** thay câu hỏi, không giữ câu hỏi cũ chỉ để hợp với test đã chọn.

Gợi ý ứng viên (**chọn sau khi xem dữ liệu**):
- `cnt` khác nhau giữa `workingday = 0` và `1`? (t-test hai mẫu)
- `cnt` khác nhau giữa các `season` hoặc `weathersit`? (ANOVA)
- `weathersit` có liên quan đến `season` hoặc `workingday`? (Chi-square độc lập)

> ⚠️ **[V-05] VALIDATE** — nhận từ **TV2** (Distribution Findings Sheet)
> - **Cần gì:** phân phối `cnt`, mức lệch.
> - **Giả định tạm:** `cnt` lệch phải, giả định chuẩn không thỏa; chuẩn bị song song phương án phi tham số (Mann–Whitney U, Kruskal–Wallis) bên cạnh t-test/ANOVA.
> - **Phải kiểm tra lại:** giả định của test đã chọn (chuẩn, đồng nhất phương sai) dựa trên kết quả chính thức của TV2. Nêu rõ lý do dùng test tham số hay phi tham số.
> - **Nếu khác:** đổi test và viết lại phần giải thích lựa chọn.

> ⚠️ **[V-08] VALIDATE** — nhận từ **TV4** (các cặp biến trong phần tương quan)
> - **Phải kiểm tra lại:** hai câu hỏi không trùng cặp biến TV4 phân tích. Trao đổi ngay khi chốt câu hỏi.

### 3.2.1. Research Question 1
```text
Research Question → Variables → H₀/H₁ → α → Test → p-value / CI → Kết luận
```
### 3.2.2. Research Question 2
Tương tự.

- Mẫu rất lớn nên p-value gần như luôn rất nhỏ. **Báo cáo thêm effect size** (Cohen's d, eta-squared, Cramér's V) và nhận xét ý nghĩa thực tiễn.
- Dùng cách viết kết luận theo rules mục 6 (không viết "chấp nhận H₀").
- **Không chốt test trước rồi mới tìm câu hỏi.**

## 3.3. Kết luận và hạn chế của phần 3
- Kết quả hai kiểm định, đủ bằng chứng bác bỏ H₀ hay không. Hạn chế: dữ liệu theo giờ liên tiếp không hoàn toàn độc lập (tự tương quan), giả định của từng test.

---

# 4. Phân tích tương quan — *TV4*

## 4.1. Lý thuyết — *làm ngay, không phụ thuộc ai*
- Pearson (tuyến tính), Spearman (đơn điệu, rank), so sánh hai phương pháp và trường hợp kết quả khác nhau.

## 4.2. Phân tích tương quan trên dữ liệu

Không phân tích mọi cặp biến. Chọn dựa trên EDA, ý nghĩa thực tế, quan hệ với `cnt`, kết quả phân phối.

> ⚠️ **[V-04] VALIDATE** — nhận từ **TV1** (EDA Findings Sheet)
> - **Giả định tạm:** phân tích `temp`, `atemp`, `hum`, `windspeed`, `cnt`.
> - **Phải kiểm tra lại:** danh sách biến, quyết định ngoại lai, đơn vị.

> ⚠️ **[V-06] VALIDATE** — nhận từ **TV2** (Distribution Findings Sheet)
> - **Giả định tạm:** tính **cả Pearson và Spearman** cho mọi cặp đã chọn (đề bài yêu cầu cả hai).
> - **Phải kiểm tra lại:** lý do ưu tiên Pearson hay Spearman trong nhận xét phải dựa trên phân phối chính thức (lệch, ngoại lai, phi tuyến).

- `hr` có quan hệ chu kỳ với `cnt` (hai đỉnh sáng/chiều ngày làm việc), nên hệ số tương quan tuyến tính giữa `hr` và `cnt` có thể thấp dù mối liên hệ mạnh. Nếu đưa `hr` vào, **nhận xét rõ điều này**.
- `casual`, `registered` có thể đưa vào để mô tả nhưng **đánh dấu rõ là không dùng làm biến độc lập cho `cnt`** (B.2).

## 4.3. Trực quan hóa
- Correlation heatmap, scatter plot, đường hồi quy nếu phù hợp. Với ~17,000 điểm, dùng `alpha` thấp hoặc hexbin.

## 4.4. Ý nghĩa thực tiễn
- Chiều, độ mạnh, tuyến tính/đơn điệu, mối quan hệ đáng chú ý. **Correlation không chứng minh causation.**
- **Bàn giao TV5: Correlation Findings Sheet** (cặp tương quan cao với nhau như `temp`–`atemp`, biến nào tương quan với `cnt`).

## 4.5. Kết luận và hạn chế của phần 4

---

# 5. Hồi quy tuyến tính đa biến (MLR) — *TV4*

## 5.1. Lý thuyết — *làm ngay, không phụ thuộc ai*
- Khái niệm MLR, biến phụ thuộc/độc lập, phương trình mô hình, hệ số hồi quy, R²/Adjusted R², sai số, các giả định (tuyến tính, độc lập, phương sai không đổi, residual phân phối chuẩn, không đa cộng tuyến).

## 5.2. Xây dựng bài toán hồi quy

### 5.2.1. Xác định biến mục tiêu
- Ứng viên: `cnt`.

> ⚠️ **[V-07] VALIDATE** — nhận từ **TV2**
> - **Giả định tạm:** `Y = cnt`.
> - **Phải kiểm tra lại:** nếu `cnt` lệch phải mạnh, cân nhắc biến đổi (ví dụ `log(1 + cnt)`) và **thống nhất với TV5** `Y` cuối cùng.

### 5.2.2. Lựa chọn biến độc lập — **điểm giao giữa TV4 và TV5**

Ứng viên: `temp`, `hum`, `windspeed`, `hr`, `workingday`, `season`, `weathersit`, các biến phù hợp khác. **Không mặc định đưa tất cả vào model.** `atemp` nhiều khả năng bị loại do tương quan rất cao với `temp` (xác nhận bằng số liệu). `casual`, `registered` bị loại (leakage).

```text
EDA → Domain meaning → Correlation → Multicollinearity (VIF) → Assumptions → Final features
```

> ⚠️ **[V-09] VALIDATE** — **TV4 giao** cho **TV5** (Feature Candidate Sheet)
> - **Nội dung:** danh sách biến ứng viên kèm lý do, cặp biến tương quan cao, VIF sơ bộ, cách mã hóa từng biến.
> - **Hạn giao v0:** theo timeline Mục 9. Sau đó cập nhật v1 khi có phản hồi.

> ⚠️ **[V-10] VALIDATE** — nhận từ **TV5** (phản hồi sau khi huấn luyện, kiểm tra giả định)
> - **Cần gì:** nếu TV5 phải đổi biến (bỏ biến, biến đổi `cnt`, thêm tương tác...), TV4 cập nhật 5.2.2.
> - **Phải kiểm tra lại:** 5.2.2 và phần 6 mô tả **cùng một tập biến cuối cùng**, cùng lý do chọn.

## 5.3. Kết luận và hạn chế của phần 5

---

# 6. Xây dựng và đánh giá mô hình — *TV5*

> **TV5 không đợi TV4.** Bắt đầu từ **baseline** với danh sách ứng viên mặc định (không có `atemp`, `casual`, `registered`), dựng sẵn toàn bộ pipeline. Khi nhận Feature Candidate Sheet thì **thay danh sách biến và chạy lại**, không viết lại pipeline.

## 6.1. Feature Engineering

- Mã hóa categorical (`season`, `weathersit`, `hr`...), xử lý date/time, tạo biến mới nếu có cơ sở, kiểm tra multicollinearity, chọn biến, biến đổi nếu cần.

> ⚠️ **[V-09] VALIDATE** — nhận từ **TV4**
> - **Giả định tạm:** baseline gồm `temp`, `hum`, `windspeed`, `hr`, `workingday`, `season`, `weathersit`.
> - **Phải kiểm tra lại:** tập biến cuối, cách mã hóa, biến bị loại và lý do khớp Feature Candidate Sheet v1.

> ⚠️ **[V-11] VALIDATE** — nhận từ **TV1** (quyết định ngoại lai)
> - **Phải kiểm tra lại:** train/test được tạo từ dữ liệu đã áp dụng đúng quyết định ngoại lai chính thức.

> ⚠️ **[V-07] VALIDATE** — nhận từ **TV2**
> - **Phải kiểm tra lại:** có biến đổi `cnt` hay không theo phân phối chính thức. Nếu biến đổi, **đánh giá cuối quy về thang gốc** (lượt thuê) để RMSE/MAE có đơn vị rõ ràng.

## 6.2. Chiến lược chia dữ liệu
- Training/test. Dữ liệu có yếu tố thời gian nên cân nhắc **random split hay chronological split**, quyết định theo mục tiêu mô hình. Ghi rõ lý do và `SEED`.
- Random split trên dữ liệu theo giờ liên tiếp có thể làm chỉ số test lạc quan. Cần nhận xét điểm này.

## 6.3. Huấn luyện mô hình
- Fit MLR, ước lượng hệ số, ý nghĩa thống kê của hệ số nếu phù hợp.

## 6.4. Đánh giá mô hình
- R², Adjusted R², MAE, RMSE (ghi đơn vị: lượt thuê).
- Kiểm tra giả định: linearity, independence (Durbin–Watson do dữ liệu theo thời gian), homoscedasticity, residuals, multicollinearity (VIF).

## 6.5. Nhận xét kết quả
- Biến đáng chú ý, mức độ giải thích, **gửi phản hồi cho TV4 (V-10)**.

## 6.6. Kết luận và hạn chế của phần 6
- Hạn chế của mô hình tuyến tính với dữ liệu này, giả định bị vi phạm, hạn chế do chia dữ liệu.

---

# 7. Quy trình bàn giao (để làm song song không bị lệch)

**`HANDOFF.md` dùng chung.** Mỗi lần giao hoặc thay đổi kết quả, người upstream thêm một dòng:

```text
[Ngày giờ] [TVx] [FINAL | DRAFT | CHANGE] [Phần] — nội dung — ai bị ảnh hưởng (V-xx)
```

- **DRAFT:** dùng được làm giả định tạm, chưa được kết luận dựa vào.
- **FINAL:** đã đóng băng, downstream được phép validate xong.
- **CHANGE:** kết quả đã giao bị đổi. Người downstream có thẻ V liên quan **phải kiểm tra và chạy lại phần của mình**.

**Findings Sheet (mỗi upstream giao 1 trang):** (1) dữ liệu/biến đã dùng, kèm phiên bản file; (2) phương pháp; (3) kết quả chính, có số liệu và đơn vị; (4) quyết định và lý do; (5) điều downstream cần lưu ý; (6) tên file code, hình, bảng.

Có 4 sheet: **EDA Findings** (TV1), **Distribution Findings** (TV2), **Correlation Findings** và **Feature Candidate** (TV4). TV3 và TV5 là downstream cuối, chỉ cần ghi `HANDOFF.md` khi có CHANGE ảnh hưởng người khác.

---

# 8. Sổ theo dõi phụ thuộc (V-tags)

| ID | Từ → Đến | Nội dung | Giả định tạm để làm song song | Thời điểm validate |
|---|---|---|---|---|
| V-01 | TV1 → tất cả | Dữ liệu sạch, thay đổi so với `hour.csv` gốc | Dùng `load_data()` trên file gốc | Khi TV1 đăng FINAL |
| V-02 | TV1 → TV2 | Biến chọn, quyết định ngoại lai | `cnt`, `temp`, chưa loại ngoại lai | Trước khi chốt 2.1 |
| V-03 | TV1 → TV3 | Khác biệt giữa nhóm, cỡ mẫu nhóm | TV3 tự EDA nhẹ để lập ứng viên | Trước khi chốt câu hỏi ở 3.2 |
| V-04 | TV1 → TV4 | Biến đưa vào tương quan, ngoại lai | Các biến số + `cnt` | Trước khi chốt 4.2 |
| V-05 | TV2 → TV3 | Phân phối `cnt` → test tham số hay phi tham số | `cnt` lệch phải, chuẩn bị cả hai phương án | Trước khi viết kết luận ở 3.2 |
| V-06 | TV2 → TV4 | Phân phối → lý giải Pearson/Spearman | Tính cả hai | Trước khi viết nhận xét 4.4 |
| V-07 | TV2 → TV4, TV5 | Có biến đổi `cnt` hay không | `Y = cnt` | Trước khi chốt 5.2.1 và 6.1 |
| V-08 | TV3 ↔ TV4 | Không trùng câu hỏi/cặp biến | Trao đổi sớm | Khi chốt câu hỏi nghiên cứu |
| V-09 | TV4 → TV5 | Feature Candidate Sheet | Baseline mặc định | Trước khi chốt 6.1 |
| V-10 | TV5 → TV4 | Phản hồi đổi biến sau khi kiểm tra giả định | — | Trước khi đóng băng 5.2.2 |
| V-11 | TV1 → TV5 | Quyết định ngoại lai áp dụng vào train/test | Chưa loại ngoại lai | Trước khi chốt 6.2 |
| V-12 | tất cả → TV3 | Gộp: đánh số hình/bảng, thuật ngữ, đơn vị, nhất quán số liệu giữa các phần | — | Khi gộp bản cuối |

---

# 9. Timeline đề xuất (hạn nộp 23h59 ngày 13/10/2026)

| Ngày | Việc | Checkpoint |
|---|---|---|
| 03–04/10 | Phase 0: chốt hợp đồng dữ liệu, `common.py`, repo, `HANDOFF.md`, thuật ngữ. Mỗi người bắt đầu phần "làm ngay" (lý thuyết, pipeline, khung tài liệu) | — |
| 05/10 | TV1 giao `bike_clean.csv` và EDA Findings Sheet (**DRAFT**) | **CP-A:** V-01, V-02, V-03, V-04, V-11 lần 1 |
| 07/10 | TV2 giao Distribution Findings Sheet. TV4 giao Feature Candidate Sheet v0 | **CP-B:** V-05, V-06, V-07, V-09 lần 1 |
| 08/10 | TV3 chốt hai câu hỏi nghiên cứu. TV5 chạy lại với danh sách biến v0, gửi phản hồi | **CP-C:** V-08, V-10 |
| 09/10 | Tất cả sheet chuyển **FINAL**, mỗi người validate lần cuối các thẻ V của mình | **CP-D:** đóng băng kết quả |
| 10/10 | Mỗi người nộp tài liệu phần mình (5 thành phần ở Mục A) cho TV3 | — |
| 11/10 | TV3 gộp bản đầu. Cả nhóm rà soát chéo theo `rules.md` (số liệu, thuật ngữ, đơn vị) | **CP-E:** V-12 |
| 12/10 | Sửa lỗi, xuất Word và PDF, kiểm tra số trang theo quy định của khoa | — |
| 13/10 | Nộp sớm trong ngày. Mỗi người tự nộp, file nén đặt tên theo mã số sinh viên | — |

---

# 10. Phụ lục bắt buộc theo đề bài — *TV3 tổng hợp, mỗi người tự khai phần mình*

- Phần mỗi sinh viên thực hiện, tỷ lệ đóng góp, mức độ hoàn thành.
- Kiểm tra quy định của khoa xem phụ lục này có tính vào số trang hay không.