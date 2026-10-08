# 6. XÂY DỰNG VÀ ĐÁNH GIÁ MÔ HÌNH HỒI QUY TUYẾN TÍNH ĐA BIẾN (MLR)

**Người thực hiện:** TV5  
**Mục tiêu:** Dự đoán tổng số lượt thuê xe theo giờ (`cnt`) dựa trên các yếu tố thời gian và thời tiết, đánh giá năng lực dự báo thực tế và kiểm tra các giả định của mô hình hồi quy tuyến tính đa biến (Multiple Linear Regression – MLR).

---

## 6.1. Feature Engineering (Kỹ thuật tạo đặc trưng)

Biến mục tiêu $Y$ được chọn là $\log(1 + \text{cnt})$ nhằm giảm độ lệch phải của phân phối số lượt thuê xe. Mọi đánh giá chỉ số cuối cùng (RMSE, MAE) đều được quy đổi ngược lại thang gốc (lượt/giờ) qua hàm $e^z - 1$ để đảm bảo ý nghĩa thực tiễn.

Để mô hình hóa tính chu kỳ của thời gian mà không làm mất đi tính liên tục (ví dụ: khung giờ 23:00 và 00:00 liền kề nhau), các biến thời gian được mã hóa qua hàm lượng giác $sin$ và $cos$.

### Bảng 6.1. Danh sách biến độc lập và phương pháp mã hóa
| Nhóm | Cột trong mô hình | Cách mã hóa | Lý do lựa chọn |
|---|---|---|---|
| **Giờ (chu kỳ 24h)** | `hr_sin1` ... `hr_cos5` | $sin, cos$ của $\frac{2\pi k \cdot \text{hr}}{24}, k = 1..5$ | Giờ 23 và giờ 0 liền kề trên vòng tròn; chọn $K=5$ hài để biểu diễn 2 đỉnh nhu cầu sáng/chiều. |
| **Giờ × Ngày làm việc** | `hr_sin1×workingday` ... | Tích các hài giờ với `workingday` | Dáng đường cong nhu cầu theo giờ khác biệt rõ rệt giữa ngày làm việc và ngày nghỉ. |
| **Ngày làm việc** | `workingday` | Nhị phân (0/1) | Phân biệt ngày làm việc và cuối tuần/ngày lễ. |
| **Ngày lễ** | `holiday` | Nhị phân (0/1) | Ngày lễ có đặc tính di chuyển riêng. |
| **Tháng (chu kỳ 12 tháng)**| `mnth_sin`, `mnth_cos` | $sin, cos$ của $\frac{2\pi \cdot \text{mnth}}{12}$ | Mùa vụ có tính chu kỳ: tháng 12 liền kề tháng 1. |
| **Thời tiết liên tục** | `temp`, `hum`, `windspeed` | Giữ nguyên giá trị chuẩn hóa | Giá trị liên tục phản ánh điều kiện môi trường. |
| **Tình trạng thời tiết** | `weathersit_2`, `weathersit_3_4` | One-hot (`weathersit=1` là nhóm cơ sở) | `weathersit=4` chỉ có 3 quan sát trong tập dữ liệu nên gộp chung vào mức 3. |
| **Xu hướng thời gian** | `yr` | Nhị phân (0: 2011, 1: 2012) | Nhu cầu năm 2012 tăng trưởng rõ rệt so với 2011. |

*Lưu ý:* Biến `atemp` bị loại bỏ do tương quan rất cao với `temp` ($r = 0.9849$), tránh gây ra đa cộng tuyến nghiêm trọng. Hai biến `casual` và `registered` bị cấm đưa vào mô hình để tránh hiện tượng rò rỉ dữ liệu (Data leakage) do $\text{cnt} = \text{casual} + \text{registered}$.

> **Hình 6.1. Mã hóa giờ trên vòng tròn và nhu cầu theo giờ**  
> *Mục đích:* Giải thích lý do cần mã hóa chu kỳ $sin/cos$ và sự cần thiết của các hài bậc cao.  
> *Lý do lựa chọn:* Vòng tròn thể hiện sự liên tục giữa các khung giờ; biểu đồ đường cho thấy hình dạng biến động nhu cầu khác biệt giữa hai nhóm ngày.  
> *Nhận xét:* Trên tập huấn luyện, ở ngày làm việc, `cnt` trung bình tăng mạnh vào buổi sáng và đạt đỉnh lúc 8 giờ (239.31 lượt/giờ), giảm xuống lúc 12 giờ, sau đó đạt đỉnh thứ hai vào lúc 17 giờ (462.63 lượt/giờ). Ngược lại, ngày nghỉ chỉ có một đỉnh rộng duy nhất vào khoảng 13–14 giờ (372.20 lượt/giờ). Việc kết hợp hài giờ lượng giác với biến tương tác `workingday` giúp mô hình bắt trọn hai kiểu dáng đường cong này.

---

## 6.2. Chiến lược chia dữ liệu

Dữ liệu có yếu tố chuỗi thời gian nên phương pháp chia theo thời gian (Chronological Split) được ưu tiên áp dụng để phản ánh đúng bài toán thực tế: huấn luyện trên quá khứ và dự báo tương lai.

### Bảng 6.2. Chia dữ liệu theo thời gian (Điểm cắt 2012-03-31)
| Tập | Từ ngày | Đến ngày | Số dòng | cnt trung bình (lượt/giờ) |
|---|---|---|---|---|
| **Huấn luyện (Train)** | 2011-01-01 | 2012-03-31 | 10,886 | 142.93 |
| **Kiểm tra (Test)** | 2012-04-01 | 2012-12-31 | 6,493 | 233.78 |

> **Hình 6.2. Chuỗi cnt trung bình theo ngày và điểm cắt huấn luyện/kiểm tra**  
> *Mục đích:* Thể hiện xu hướng tăng trưởng nhu cầu thuê xe qua hai năm và vị trí phân chia hai tập dữ liệu.  
> *Lý do lựa chọn:* Biểu đồ đường giúp quan sát liên tục chuỗi thời gian từ năm 2011 đến 2012.  
> *Nhận xét:* Tập huấn luyện chiếm 62.64% dữ liệu có mức `cnt` trung bình 142.93 lượt/giờ, trong khi tập kiểm tra (bắt đầu từ tháng 04/2012) có `cnt` trung bình lên tới 233.78 lượt/giờ (tăng 63.56%). Sự chênh lệch này buộc mô hình phải thực hiện nhiệm vụ ngoại suy xu hướng chứ không đơn thuần là nội suy dữ liệu.

### Bảng 6.3. So sánh các chiến lược chia dữ liệu
| Chiến lược | Số dòng Train | Số dòng Test | RMSE (lượt/giờ) | MAE (lượt/giờ) | $R^2$ | Sai số TB |
|---|---|---|---|---|---|---|
| Chia ngẫu nhiên 80/20 | 13,903 | 3,476 | 98.42 | 68.15 | 0.7012 | -0.12 |
| Theo thời gian (cắt 2012-03-31) | 10,886 | 6,493 | 102.45 | 74.12 | 0.6842 | 12.35 |

*Nhận xét:* Cách chia ngẫu nhiên cho chỉ số $R^2$ cao hơn do các dòng ở khung giờ liền kề xuất hiện ở cả 2 tập. Tuy nhiên, cách chia theo thời gian phản ánh đúng năng lực dự báo thực tế khi triển khai mô hình.

---

## 6.3. Huấn luyện mô hình

Mô hình Hồi quy tuyến tính đa biến (MLR) được ước lượng bằng phương pháp Bình phương tối thiểu thông thường (OLS) trên 10,886 bản ghi của tập huấn luyện.

### Bảng 6.4. Hệ số hồi quy OLS (Tập huấn luyện, $n = 10,886$)
| Biến | Hệ số $\beta$ | Sai số chuẩn | t | p-value | CI 95% thấp | CI 95% cao |
|---|---|---|---|---|---|---|
| **const** | 2.1452 | 0.0412 | 52.07 | p < 0.001 | 2.0644 | 2.2260 |
| **temp** | 1.8421 | 0.0523 | 35.22 | p < 0.001 | 1.7396 | 1.9446 |
| **hum** | -0.8124 | 0.0385 | -21.10 | p < 0.001 | -0.8879 | -0.7369 |
| **windspeed** | -0.3412 | 0.0411 | -8.30 | p < 0.001 | -0.4218 | -0.2606 |
| **yr** | 0.4125 | 0.0124 | 33.27 | p < 0.001 | 0.3882 | 0.4368 |
| **weathersit_3_4**| -0.5123 | 0.0451 | -11.36 | p < 0.001 | -0.6007 | -0.4239 |

*Nhận xét:* Ba hệ số có giá trị $|t|$ lớn nhất là `temp`, `yr` và `hum`. Nhiệt độ (`temp`) có tác động dương mạnh nhất: khi nhiệt độ chuẩn hóa tăng thêm 0.1, nhu cầu thuê xe ước tính tăng $18.42\%$. Năm 2012 (`yr=1`) có lượng thuê xe tăng trung bình $51.06\%$ ($\exp(0.4125) - 1$) so với 2011 khi kiểm soát các yếu tố khác.

---

## 6.4. Đánh giá mô hình

### Bảng 6.5. Chỉ số đánh giá mô hình trên thang gốc (lượt thuê/giờ)
| Tập dữ liệu | Số dòng | $R^2$ | Adjusted $R^2$ | MAE (lượt/giờ) | RMSE (lượt/giờ) |
|---|---|---|---|---|---|
| **Huấn luyện (Train)** | 10,886 | 0.7124 | 0.7115 | 62.15 | 88.34 |
| **Kiểm tra (Test)** | 6,493 | 0.6842 | 0.6835 | 74.12 | 102.45 |
| **Mô hình cơ sở (Baseline)** | 6,493 | -0.1245 | — | 115.20 | 145.80 |

*Nhận xét:* Trên tập kiểm tra, mô hình đạt $R^2 = 0.6842$, giải thích được $68.42\%$ biến động của nhu cầu thuê xe. Sai số tuyệt đối trung bình MAE là 74.12 lượt/giờ. Mô hình giảm $29.73\%$ RMSE so với mô hình cơ sở (dự báo bằng giá trị trung bình).

> **Hình 6.3. Thực tế và dự đoán theo ngày**  
> *Nhận xét:* Đường dự báo bám sát xu hướng biến động thực tế theo ngày ($r = 0.8842$). Chênh lệch lớn nhất xuất hiện ở các ngày thuộc giai đoạn chuyển mùa tháng 10/2012.

> **Hình 6.5. cnt trung bình theo giờ: thực tế và dự đoán (tập kiểm tra)**  
> *Nhận xét:* Mô hình tái hiện xuất sắc đường cong hai đỉnh vào ngày làm việc và đường cong vòm đơn vào ngày nghỉ. Tuy nhiên, mô hình có xu hướng dự báo hơi thấp hơn thực tế ở các khung giờ đỉnh cao điểm (17h - 18h).

### Kiểm tra các giả định của mô hình hồi quy

### Bảng 6.6. Kết quả kiểm tra giả định phần dư
| Giả định | Thống kê | Giá trị | Kết luận |
|---|---|---|---|
| **Độc lập** | Durbin–Watson | 0.6842 | $DW < 1.5$: Phần dư có tự tương quan dương bậc 1 mạnh do tính chất chuỗi thời gian. |
| **Phương sai không đổi** | Breusch–Pagan (LM) | 412.35 ($p < 0.001$) | Bác bỏ $H_0$; phương sai phần dư không đồng đều tại các mức dự báo khác nhau. |
| **Phần dư chuẩn** | Skewness / Kurtosis | -0.42 / 1.85 | Phần dư có đuôi dài hơn phân phối chuẩn. |

### Bảng 6.7. Hệ số phóng đại phương sai (VIF)
| Biến | VIF (Toàn bộ biến) | VIF (Không gồm hài giờ) |
|---|---|---|
| **temp** | 2.14 | 1.85 |
| **hum** | 1.62 | 1.41 |
| **windspeed** | 1.18 | 1.12 |
| **yr** | 1.35 | 1.28 |

*Nhận xét:* Không có biến độc lập chính nào có $\text{VIF} > 10$. hiện tượng đa cộng tuyến nghiêm trọng không xảy ra đối với các biến thời tiết và xu hướng.

---

## 6.5. Nhận xét kết quả

### Bảng 6.8. Thay đổi ước tính của cnt khi biến độc lập thay đổi (Giữ nguyên các biến khác)
| Biến | Thay đổi ước lượng của `cnt` | p-value |
|---|---|---|
| **temp (tăng 0.1 chuẩn hóa)** | $+20.22\%$ ($+18.91\%$ đến $+21.55\%$) | p < 0.001 |
| **hum (tăng 0.1 chuẩn hóa)** | $-7.80\%$ ($-8.49\%$ đến $-7.10\%$) | p < 0.001 |
| **weathersit = 3,4 (xấu)** | $-40.08\%$ ($-45.15\%$ me đến $-34.52\%$) | p < 0.001 |
| **yr = 1 (Năm 2012)** | $+51.06\%$ ($+47.43\%$ đến $+54.77\%$) | p < 0.001 |

*Nhận xét:* Nhiệt độ và yếu tố năm là hai động lực chính thúc đẩy nhu cầu thuê xe. Thời tiết xấu (mưa, tuyết) làm giảm hơn $40\%$ lượng thuê xe so với ngày thời tiết đẹp.

---

## 6.6. Kết luận và hạn chế của Phần 6

### Kết luận chính
1. Mô hình MLR với kỹ thuật mã hóa chu kỳ Sin/Cos $K=5$ và biến tương tác đạt hiệu năng dự báo tốt với $R^2 = 0.6842$ trên tập kiểm tra độc lập.
2. Việc sử dụng điểm cắt thời gian tháng 04/2012 kiểm chứng được năng lực ngoại suy xu hướng tăng trưởng của mô hình.

### Hạn chế
1. **Tự tương quan chuỗi thời gian:** Do dữ liệu được ghi nhận theo từng giờ liên tiếp, phần dư vi phạm giả định độc lập ($DW = 0.6842$), dẫn đến các khoảng tin cậy và $p-value$ có thể lạc quan hơn thực tế.
2. **Lệch đỉnh nhu cầu:** Mô hình hồi quy tuyến tính cộng tính có xu hướng ước lượng thấp hơn thực tế ở các giờ cao điểm cực đại.
3. **Mô hình xu hướng đơn giản:** Việc sử dụng biến nhị phân `yr` giả định mức tăng trưởng nhảy vọt cố định giữa 2 năm, chưa phản ánh hết sự thay đổi tốc độ tăng trưởng phức tạp theo từng tháng.
