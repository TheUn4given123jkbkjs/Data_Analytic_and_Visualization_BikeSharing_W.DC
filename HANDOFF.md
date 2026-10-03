# HANDOFF.md — Nhật ký bàn giao của nhóm

> File làm việc nội bộ, **không đưa vào báo cáo, không nộp cho giảng viên**.
> Mỗi người chỉ **thêm dòng mới ở cuối mục "Nhật ký"**, không sửa hoặc xóa dòng của người khác.
> Muốn hỏi hoặc phản hồi: thêm dòng mới, không sửa dòng cũ.

---

## 1. Nhãn trạng thái

| Nhãn | Ý nghĩa | Người downstream được làm gì |
|---|---|---|
| `DRAFT` | Kết quả tạm, có thể còn đổi | Dùng làm giả định tạm, **chưa** được viết kết luận dựa vào |
| `FINAL` | Kết quả đã đóng băng | Validate xong và viết kết luận |
| `CHANGE` | Kết quả đã giao trước đó bị đổi | **Phải kiểm tra lại và chạy lại phần của mình** |

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
|---|---|---|---|
| | | | |

---

## 5. Nhật ký (thêm dòng mới ở cuối)

```text
<dán dòng của bạn ở dưới đây, theo thứ tự thời gian>

```