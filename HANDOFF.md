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
```

### EDA Findings Sheet — TV1 — v0 — DRAFT — 2026-10-04

1. **Dữ liệu/biến đã dùng:** `hour.csv` gốc (17,379 dòng x 17 biến), trong `EDA.ipynb`. `bike_clean.csv` chưa xuất.
2. **Phương pháp:** kiểm tra chất lượng, thống kê mô tả, Spearman/Pearson, ngoại lai IQR và Z-score, tự tương quan bậc 1.
3. **Kết quả chính** (`temp`, `atemp`, `hum`, `windspeed` ở thang chuẩn hóa; `cnt` là lượt thuê/giờ):
   - Sạch: 0 thiếu, 0 trùng, `cnt = casual + registered` đúng mọi dòng.
   - `hum = 0`: 22 dòng, đã sửa. `windspeed = 0`: 2,180 dòng (12.54%), giữ nguyên.
   - Thiếu 165 giờ (0.94%), 59.39% ở 2–5h sáng; ngày 2012-10-29 chỉ có 1/24 giờ.
   - `cnt` 2012 cao hơn 2011 63.20% (234.67 so với 143.79); thấp nhất tháng 1.
   - Mean `cnt` theo mùa: Winter 111.11, Spring 208.34, Summer 236.02, Fall 198.87.
   - Mean `cnt` theo `weathersit` 1/2/3: 204.87 / 175.17 / 111.58.
   - Spearman với `cnt`: `hr` 0.5109, `temp` 0.4233, `hum` -0.3634, `windspeed` 0.1266.
   - Cặp tương quan: `temp`–`atemp` 0.9877, `hum`–`weathersit` 0.4151, `temp`–`season` 0.3058.
4. **Quyết định và lý do:** giữ mọi ngoại lai (giải thích được bằng giờ cao điểm, mùa, xu hướng); giữ thang chuẩn hóa; không điền giờ thiếu; không biến đổi `cnt` (để TV2/TV5 quyết).
5. **Downstream cần lưu ý:**
   - TV2 (V-02): `cnt`, `temp` dùng được; nên xét `cnt` theo nhóm (`hr`, `workingday`).
   - TV3 (V-03): quan sát không độc lập, cần effect size; loại/gộp `weathersit = 4`.
   - TV4 (V-04): bỏ `atemp`, `casual`, `registered`; nhận xét `hr` quan hệ chu kỳ.
   - TV5 (V-11): chưa loại ngoại lai; chia train/test theo thời gian; thận trọng đặc trưng trễ.
6. **File liên quan:** `EDA.ipynb` (Bảng 1.1–1.12, Hình 1.1–1.11), `report.md`, `report.doc`
