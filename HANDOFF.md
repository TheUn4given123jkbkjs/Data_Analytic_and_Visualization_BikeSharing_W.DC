# HANDOFF.md — Nhật ký bàn giao của nhóm

> File làm việc nội bộ, **không đưa vào báo cáo, không nộp cho giảng viên**.
> Mỗi người chỉ **thêm dòng mới ở cuối mục "Nhật ký"**, không sửa hoặc xóa dòng của người khác.
> Muốn hỏi hoặc phản hồi: thêm dòng mới, không sửa dòng cũ.

---

## 1. Nhãn trạng thái

| Nhãn     | Ý nghĩa                         | Người downstream được làm gì                               |
| -------- | ------------------------------- | ---------------------------------------------------------- |
| `DRAFT`  | Kết quả tạm, có thể còn đổi     | Dùng làm giả định tạm, **chưa** được viết kết luận dựa vào |
| `FINAL`  | Kết quả đã đóng băng            | Validate xong và viết kết luận                             |
| `CHANGE` | Kết quả đã giao trước đó bị đổi | **Phải kiểm tra lại và chạy lại phần của mình**            |

---

## 2. Mẫu một dòng (copy dòng này, thay nội dung)

```text
[YYYY-MM-DD HH:mm] [TVx] [DRAFT|FINAL|CHANGE] [Phần x.x] — <nội dung ngắn gọn, có số liệu nếu có> — ảnh hưởng: <TVy, TVz> (V-xx)
```

**Ví dụ (chỉ minh họa cách viết, không phải kết quả thật):**

```text
[2026-10-05 20:30] [TV1] [DRAFT] [Phần 1.3] — Đã quyết định giữ/loại ngoại lai: <giữ hay loại>, tiêu chí <IQR / Z-score>, số dòng bị ảnh hưởng <n> — ảnh hưởng: TV2, TV4, TV5 (V-02, V-04, V-11)
[2026-10-07 14:10] [TV2] [FINAL] [Phần 2.4] — `cnt` có phân phối <mô tả>, độ lệch <giá trị>; đề xuất <biến đổi hay không> — ảnh hưởng: TV3, TV4, TV5 (V-05, V-06, V-07)
[2026-10-08 09:45] [TV5] [DRAFT] [Phần 6.4] — Kiểm tra giả định thấy <vấn đề>, đề nghị <bỏ/đổi biến> — ảnh hưởng: TV4 (V-10)
[2026-10-09 18:00] [TV1] [CHANGE] [Phần 1.1.2] — Thay đổi so với bản trước: <nêu rõ thay đổi gì> — ảnh hưởng: tất cả (V-01)
```

**Ghi chú khi viết dòng:**

- Một dòng = một thay đổi. Có nhiều thay đổi thì ghi nhiều dòng.
- Luôn ghi **ai bị ảnh hưởng** và **thẻ V** tương ứng (tra ở Mục 8 trong `outline_v3_parallel.md`).
- Nêu rõ **cái gì đã thay đổi** (với `CHANGE`), không chỉ ghi "đã cập nhật".
- Số liệu ghi theo `rules.md`: dấu `.` thập phân, ghi đơn vị, nói rõ biến đang chuẩn hóa hay đã quy đổi.

---

## 3. Mẫu Findings Sheet (1 trang, dán dưới dòng nhật ký hoặc đính kèm file)

Dành cho **TV1 (EDA Findings), TV2 (Distribution Findings), TV4 (Correlation Findings và Feature Candidate)**.

```markdown
### [Tên sheet] — TVx — v<số> — [DRAFT|FINAL] — YYYY-MM-DD

1. **Dữ liệu/biến đã dùng:** <file và phiên bản, ví dụ bike_clean.csv; biến nào>
2. **Phương pháp:** <ngắn gọn>
3. **Kết quả chính (có số liệu và đơn vị):**
   - ...
   - ...
4. **Quyết định đã đưa ra và lý do:** <ví dụ giữ/loại ngoại lai, biến đổi hay không>
5. **Downstream cần lưu ý (V-xx):**
   - TVy: ...
   - TVz: ...
6. **File liên quan:** <tên file code, hình, bảng>
```

---

## 4. Thuật ngữ bổ sung (nếu cần thêm thuật ngữ mới, ghi vào đây và báo cả nhóm trước khi dùng)

| English | Tiếng Việt | Viết tắt | Người đề xuất |
| ------- | ---------- | -------- | ------------- |
|         |            |          |               |

---

## 5. Nhật ký (thêm dòng mới ở cuối)

```text
<dán dòng của bạn ở dưới đây, theo thứ tự thời gian>

[2026-10-04] [TV1] [DRAFT] [Phần 1.1.2] — Tiền xử lý: `dteday` sang datetime; sửa 22 dòng `hum = 0` (2011-03-10) bằng TB cùng giờ ngày trước/sau; không xóa dòng nào (17,379 dòng); giữ thang chuẩn hóa 0-1 cho `temp`, `atemp`, `hum`, `windspeed`. `bike_clean.csv` CHƯA xuất — ảnh hưởng: tất cả (V-01)
[2026-10-04] [TV1] [DRAFT] [Phần 1.3] — Giữ toàn bộ ngoại lai, loại 0 dòng. IQR toàn cục: 505 dòng `cnt` (2.91%, hàng rào trên 642.5), 80.99% ở giờ 8/17/18 = đỉnh đi làm hợp lệ; Z-score: 244 dòng — ảnh hưởng: TV2, TV3, TV4, TV5 (V-02, V-03, V-04, V-11)
[2026-10-04] [TV1] [DRAFT] [Phần 1.2] — `cnt` lệch phải: mean 189.46, median 142, skew 1.28, phương sai/TB = 173.66; `log1p` đảo lệch (skew -0.82), không về chuẩn. Chưa quyết định biến đổi — ảnh hưởng: TV2, TV3, TV5 (V-05, V-07)
[2026-10-04] [TV1] [DRAFT] [Phần 1.2.2] — Nhịp giờ khác theo `workingday`: ngày làm việc đỉnh 8h (477.01) và 17h (525.29 lượt); ngày nghỉ đỉnh 13h (372.73). Spearman với `cnt`: `hr` 0.51, `temp` 0.42, `hum` -0.36. Nên xét tương tác `hr` x `workingday` — ảnh hưởng: TV3, TV4, TV5 (V-04, V-09)
[2026-10-04] [TV1] [DRAFT] [Phần 1.1.1] — `temp`–`atemp` Pearson 0.9877 (giữ một biến); `weathersit = 4` chỉ 3 dòng (loại/gộp nhóm 3); thiếu 165 giờ (0.94%), không chèn dòng giả; tự tương quan bậc 1 của `cnt` = 0.8431 (quan sát không độc lập) — ảnh hưởng: TV3, TV4, TV5 (V-03, V-09, V-11)
[2026-10-04] [TV1] [FINAL] [Phần 1] — Hoàn thành toàn bộ phần 1
[2026-10-08] [TV1] [CHANGE] [Phần 1] — Cập nhật toàn diện: (1) Xuất `EDA/cleaned_data/hour_cleaned.csv`; (2) Bỏ hoàn toàn ma trận tương quan Spearman/Pearson khỏi EDA để tránh trùng lặp, chuyển giao toàn quyền phân tích tương quan cho TV4 (V-04); (3) Bổ sung kiểm tra độ nhạy cho 165 giờ thiếu và 22 dòng `hum = 0`; (4) Định lượng cỡ mẫu hiệu dụng $N_{\text{eff}} \approx 1,479$ (~8.51%) cho TV3; (5) Đồng bộ 100% tiếng Việt có dấu cho toàn bộ biểu đồ Hình 1.1–1.10 trong notebook và assets — ảnh hưởng: TV2, TV3, TV4, TV5 (V-02, V-03, V-04, V-11)
```

### EDA Findings Sheet — TV1 — v1 — FINAL — 2026-10-08

1. **Dữ liệu/biến đã dùng:** `EDA/cleaned_data/hour_cleaned.csv` (17,379 dòng × 17 biến). Dữ liệu sạch, không ô trống, không trùng lặp.
2. **Phương pháp:** Kiểm tra chất lượng dữ liệu, thống kê mô tả mở rộng (Skewness, Kurtosis), kiểm tra độ nhạy (sensitivity analysis), trực quan hóa phân tán và nhịp giờ, phân tích tự tương quan (ACF) và định lượng cỡ mẫu hiệu dụng $N_{\text{eff}}$.
3. **Kết quả chính** (`temp`, `atemp`, `hum`, `windspeed` ở thang chuẩn hóa [0, 1]; `cnt` là lượt thuê/giờ):
   - Đã sửa 22 dòng `hum = 0` ngày 2011-03-10 bằng nội suy cùng giờ lân cận; giữ nguyên 2,180 dòng `windspeed = 0` (ngưỡng đo máy đo gió).
   - 165 giờ thiếu: 98 giờ đêm (2–5h sáng, zero-truncated) + 72 giờ dồn vào 5 ngày bão (Sandy, bão tuyết, mưa băng). Độ nhạy mean lệch $< 0.94\%$.
   - `cnt`: Mean 189.46, Median 142.00, Skewness 1.28, Kurtosis 1.42; $\text{Var}/\text{Mean} = 173.66 \gg 1$ (over-dispersion). Biến đổi $\sqrt{cnt}$ có Skewness 0.29 (gần chuẩn nhất).
   - Tăng trưởng: 2012 cao hơn 2011 là 63.20% (234.67 so với 143.79 lượt/h).
   - Nhịp giờ × Loại ngày: Ngày làm việc có 2 đỉnh nhọn (8h: 477.01 và 17h: 525.29 lượt/h); Ngày nghỉ có 1 đỉnh vòm (13h: 372.73 lượt/h).
   - Tự tương quan: $r_1 = 0.8431$, $r_{24} = 0.8151$, $r_{168} = 0.8164$. Cỡ mẫu hiệu dụng $N_{\text{eff}} \approx 1,479$ quan sát.
   - Ngoại lai: 505 dòng toàn cục ($cnt > 642.5$) là đỉnh giờ cao điểm hợp lệ; 130 dòng cục bộ theo (`hr`, `workingday`) do thời tiết tốt và sự kiện. Giữ lại 100%.
4. **Quyết định đã đưa ra và lý do:**
   - Giữ nguyên thang chuẩn hóa; không chèn dòng giả cho 165 giờ thiếu; gộp `weathersit = 4` vào nhóm 3; không xóa ngoại lai nào; chuyển giao toàn bộ phân tích ma trận tương quan cho TV4.
5. **Downstream cần lưu ý:**
   - **TV2 (V-02):** `cnt` phân tán vượt mức và Zero-truncated $\rightarrow$ kiểm tra Negative Binomial và Zero-truncated models.
   - **TV3 (V-03):** Vi phạm giả định độc lập do tự tương quan ($N_{\text{eff}} \approx 1,479$) $\rightarrow$ chạy song song kiểm định phi tham số (Mann-Whitney U, Kruskal-Wallis) và bắt buộc báo cáo Effect Size; gộp `weathersit = 4` vào nhóm 3.
   - **TV4 (V-04):** Bỏ `atemp` để chống đa cộng tuyến ($r = 0.9877$); cấm dùng `casual`/`registered` làm biến độc lập; thực hiện ma trận tương quan Pearson vs Spearman toàn diện.
   - **TV5 (V-11):** Chia tập Train/Test theo thời gian; cẩn trọng tạo Lag features tại các điểm gãy; thử nghiệm biến đổi $\sqrt{cnt}$ hoặc hồi quy đếm GLM.
6. **File liên quan:** `EDA/EDA.ipynb` (Hình 1.1–1.10), `EDA/report.md`, `EDA/cleaned_data/hour_cleaned.csv`.

### Correlation Findings Sheet — TV4 — v1 — DRAFT — 2026-10-09

1. **Dữ liệu/biến đã dùng:**
   - `EDA/cleaned_data/hour_cleaned.csv` (17,379 dòng × 17 biến). Dữ liệu sạch, không ô trống, không trùng lặp.
   - Các biến đã dùng:
      - `temp`
      - `hum`
      - `windspeed`
      - `cnt`
   - Biến `atemp` được loại khỏi ma trận tương quan chính do có tương quan rất cao với `temp` (r = 0,9877).
   - Hai biến `casual` và `registered` không được sử dụng làm biến dự báo độc lập cho `cnt`, vì `cnt` được tính bằng tổng của hai biến này.
   - Biến `hr` được xem xét riêng do mối quan hệ giữa giờ trong ngày và số lượt thuê xe có thể mang tính chu kỳ, không thể hiện đầy đủ qua một hệ số tương quan đơn lẻ.

2. **Phương pháp:**
   - **Pearson:** Đánh giá mức độ và chiều hướng của mối quan hệ tuyến tính giữa hai biến.
   - **Spearman:** Đánh giá mức độ và chiều hướng của mối quan hệ đơn điệu dựa trên thứ hạng của dữ liệu.

Việc kết hợp hai phương pháp giúp kiểm tra liệu mối quan hệ quan sát được có tương đối tuyến tính hay có thể tồn tại dạng đơn điệu không tuyến tính. Các kết quả được đối chiếu với biểu đồ trực quan để tránh chỉ dựa vào hệ số tương quan khi diễn giải dữ liệu.

Lưu ý: Pearson và Spearman đều đo lường mối liên hệ thống kê, không chứng minh rằng một biến gây ra sự thay đổi của biến còn lại.

3. **Kết quả tính:**
- `temp – cnt`         0,40   Tương quan thuận mức vừa
- `hum – cnt`         -0,33   Tương quan nghịch, mức yếu đến vừa
- `windspeed – cnt`    0,10   Tương quan thuận rất yếu
- `temp – hum`        -0.06   Tương quan nghịch rất yếu
- `temp – windspeed`  -0.01   Tương quan nghịch rất yếu, gần như không có
- `hum – windspeed`   -0.30   Tương quan nghịch, mức yếu đến vừa

4. **Quyết định đã đưa ra và lý do:**
- Loại `atemp` khỏi nhóm biến phân tích chính: `temp` và `atemp` có tương quan rất cao, cho thấy hai biến cung cấp thông tin rất tương đồng. Việc giữ cả hai có thể gây đa cộng tuyến trong một số mô hình hồi quy.
- Không sử dụng `casual` và `registered` làm biến dự báo độc lập cho `cnt`: vì `cnt` = `casual` + `registered`, sử dụng hai biến này sẽ gây rò rỉ thông tin mục tiêu (target leakage) nếu mục tiêu là dự báo `cnt` từ các thông tin có sẵn trước thời điểm cần dự báo.
- Giữ lại `temp`, `hum` và `windspeed` để xem xét trong mô hình: các biến này có thể phản ánh điều kiện thời tiết liên quan đến nhu cầu thuê xe. Tuy nhiên, việc giữ hay loại biến cuối cùng cần dựa trên mục tiêu mô hình, tính sẵn có của dữ liệu và kết quả đánh giá mô hình.
- Phân tích `hr` riêng: số lượt thuê xe thay đổi theo giờ và có thể có nhiều đỉnh trong ngày. Hệ số tương quan đơn lẻ có thể không phản ánh đầy đủ cấu trúc này.

5. **Downstream cần lưu ý:**
....
6. **File liên quan:** `04_Corelation_Analysis/04_correlation.ipynb` (Hình 4.1–4.5), `04_Corelation_Analysis/theories.md`, `EDA/cleaned_data/hour_cleaned.csv`.
