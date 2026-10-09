# Handoff thực thi - Phân tích phân phối xác suất (TV2)

## Mục đích và cách dùng

Tài liệu này là brief thực thi cho AI sẽ hoàn thiện Phần 2 của dự án Bike Sharing. Đọc toàn bộ file trước khi sửa code. Mục tiêu là tạo notebook chạy lại được, báo cáo có thể gộp vào báo cáo nhóm và Findings Sheet định lượng cho TV3, TV4, TV5. Không biến phân tích mô tả thành kiểm định giả thuyết hoặc kết luận nhân quả.

## Bối cảnh dự án

- Dự án phân tích Bike Sharing Dataset, tập trung vào `hour.csv` của hệ thống Capital Bikeshare tại Washington D.C. trong năm 2011–2012; mỗi dòng là một giờ có ghi nhận.
- Phần 2 do TV2 phụ trách. Thứ tự phụ thuộc của nhóm là EDA → phân phối → kiểm định/tương quan/mô hình. Phần này bàn giao căn cứ phân phối, không quyết định thay TV3 về test, TV4 về cách phân tích tương quan, hoặc TV5 về target/mô hình cuối.
- Đầu vào phân tích là `EDA/cleaned_data/hour_cleaned.csv`. Không dùng `day.csv` làm dữ liệu chính và không sửa `data/hour.csv`.
- Dùng Python và các thư viện đã khai báo trong `Distribution/requirements.txt`: pandas, numpy, scipy, matplotlib, seaborn và Jupyter. Không thêm dependency nếu các thư viện hiện có đáp ứng được yêu cầu.
- Nội dung notebook và báo cáo viết bằng tiếng Việt. Ở lần đầu dùng thuật ngữ chuyên môn, ghi English + Vietnamese + viết tắt nếu có; giữ tên biến dataset trong code và nội dung.

## Hợp đồng dữ liệu và EDA đã xác nhận

AI thực thi phải dùng các điểm dưới đây làm sanity check. Nếu dữ liệu chạy thực tế khác, dừng việc chép số cũ, điều tra phiên bản/đường dẫn và ghi rõ sai khác trước khi cập nhật kết luận.

| Nội dung | Kết quả đã xác nhận |
| --- | --- |
| Kích thước cleaned data sau khi bỏ cột index kỹ thuật | 17,379 dòng × 17 biến |
| Chất lượng | Không có ô thiếu hoặc dòng trùng trong file cleaned; không trùng khóa (`dteday`, `hr`) |
| Quan hệ biến mục tiêu | `cnt = casual + registered`; không đưa `casual`/`registered` làm biến giải thích cho `cnt` |
| `cnt` | Min = 1; không có dòng `cnt = 0`; mean = 189.46; median = 142.00; SD = 181.39; skewness = 1.2774; kurtosis = 1.4172; max = 977 |
| Over-dispersion | Variance/mean = 173.6563, lớn hơn nhiều so với 1 của Poisson equidispersion |
| Giá trị thấp/cao của `cnt` | 6.22% dòng có `cnt ≤ 5`; 2.91% có `cnt > 642.5`. Các đỉnh cao đã được EDA đánh giá là nhu cầu hợp lệ; giữ ngoại lai, không tự động xóa |
| `temp` | Mean = 0.4970; median = 0.50; skewness = -0.0060; giá trị chuẩn hóa 0–1 |
| `hum` | Mean = 0.6281; median = 0.63; skewness = -0.0828; giá trị chuẩn hóa 0–1 |
| Tiền xử lý EDA | 22 giá trị `hum = 0` được nội suy cùng giờ lân cận; giữ 2,180 giá trị `windspeed = 0`; không chèn 165 giờ thiếu; giữ các ngoại lai; gộp `weathersit = 4` vào nhóm 3 trong dữ liệu EDA |
| Nhịp theo giờ và loại ngày | Ngày làm việc có mean `cnt` cao điểm lúc 8h = 477.01 và 17h = 525.29; ngày nghỉ đạt đỉnh lúc 13h = 372.73. Đây là số liệu mô tả từ EDA, không phải kiểm định |
| Tự tương quan | ACF `cnt`: lag 1 = 0.8431, lag 24 = 0.8151, lag 168 = 0.8164. EDA ước lượng `N_eff ≈ 1,479` (8.51%) theo xấp xỉ AR(1); đây là chỉ báo hạn chế, không phải cỡ mẫu hiệu dụng chính xác cho mọi phép phân tích |
| Biến đổi | `log1p(cnt)` có skewness khoảng -0.8182; `sqrt(cnt)` có skewness khoảng 0.29 theo EDA. TV2 không chốt biến đổi target thay TV5 |

`temp`, `atemp`, `hum`, `windspeed` là giá trị chuẩn hóa. Riêng phần này chủ yếu diễn giải `temp` và `hum` trên thang 0–1; không đổi sang đơn vị vật lý hoặc trộn hai thang đo trong cùng kết quả.

## Phạm vi phân tích

1. Kiểm tra dữ liệu đầu vào và mô tả `cnt`, `temp`, `hum`.
2. Mô tả phân phối thực nghiệm của `cnt`; fit Poisson, Negative Binomial, Normal và Log-normal để đối chiếu có giới hạn.
3. Fit Normal và Beta riêng cho `temp` và `hum`.
4. Mô tả `cnt` theo `workingday`, gồm phân phối gộp theo nhóm và mean theo giờ tách nhóm.
5. Kiểm tra `temp` theo `season` để xem cấu trúc theo mùa có thể giải thích một phần hình dạng tổng thể hay không. Chỉ gắn tên mùa sau khi xác minh mã với data dictionary chính thức của UCI; nếu không xác minh được, dùng mã `season` 1–4, không tự suy diễn.
6. Viết kết luận, hạn chế và Findings Sheet chuyển giao.

Không làm kiểm định giả thuyết của TV3, tương quan của TV4, MLR, dự báo hoặc lựa chọn mô hình cuối của TV5. Không tuyên bố nhân quả.

## Yêu cầu phân tích và trình bày

### 1. Kiểm tra đầu vào và thống kê mô tả

- Đọc đúng `EDA/cleaned_data/hour_cleaned.csv`; xử lý cột `Unnamed`/index kỹ thuật nếu có và chuyển `dteday` sang datetime nếu cần. Không thay đổi dataframe nguồn trên đĩa.
- Kiểm tra shape, cột, thiếu/trùng, khóa (`dteday`, `hr`), `cnt = casual + registered`, số dòng `cnt = 0`, min/max và số `hum = 0` sau EDA.
- Bảng mô tả tối thiểu có n, mean, median, SD, min, Q1, Q3, max, IQR, skewness, kurtosis; thêm variance/mean cho `cnt`.
- Dùng kết quả EDA trong bảng trên làm sanity check, không chèn cố định những số đó thay cho tính toán notebook.

### 2. Hình 2.1 - Phân phối thực nghiệm của `cnt`

- Giữ ba panel: histogram + KDE, ECDF, boxplot.
- KDE phải tương phản rõ với histogram; chú giải phải chỉ ra mỗi lớp biểu diễn gì để không nhầm KDE với panel kế bên.
- ECDF dùng trục dọc 0%, 25%, 50%, 75%, 100%; đánh dấu median = 142 tại P50 và Q3 = 281 tại P75 bằng đường ngang/dọc dễ đọc. Tính các mốc từ dữ liệu đang chạy và chỉ dùng giá trị nêu trên làm sanity check.
- Trục ghi `cnt` (lượt thuê/giờ), tiêu đề và chú giải tiếng Việt. Nêu `cnt` lệch phải và boxplot không phân biệt được lỗi dữ liệu với cực trị hợp lệ.

### 3. Mô hình phân phối `cnt`, PMF/PDF và AIC/BIC

- Fit Poisson và Negative Binomial như mô hình rời rạc cho biến đếm. Fit Normal và Log-normal chỉ như baseline liên tục để minh họa giới hạn; không trình bày chúng như phân phối đếm.
- Dùng MLE cho mọi log-likelihood được dùng để tính AIC/BIC. Poisson có MLE `lambda = mean(cnt)`. Negative Binomial cần tối ưu log-likelihood trên tham số hợp lệ (size > 0, probability trong (0,1)); kiểm tra optimizer thành công, hữu hạn, và ghi phương pháp/điều kiện fit. Normal và Log-normal cũng phải fit và tính likelihood nhất quán. Không gọi AIC/BIC từ tham số Negative Binomial method-of-moments là AIC/BIC MLE.
- Notebook hiện hành có NB method-of-moments và output đã lưu không theo thứ tự chạy; các tham số, AIC/BIC, hình hoặc số liệu cũ chỉ là tham khảo, không được coi là kết quả mới. Tính lại toàn bộ trong lần chạy sạch.
- Tách Hình 2.2 thành hai panel/axes không dùng chung trục tung:
	- Poisson/NB và histogram thực nghiệm rời rạc: trục y là xác suất khối `P(X=k)`. Chuẩn hóa histogram theo xác suất để tổng khối xấp xỉ 1.
	- Normal/Log-normal và histogram liên tục: histogram dùng mật độ (`density=True`), trục y là mật độ `f(x)`.
- Ghi chú ngay trong hình/chú thích rằng `P(X=k)` và `f(x)` khác đơn vị; không so độ cao đường PMF với PDF như cùng một đại lượng.
- Giải thích công thức: `AIC = -2 log(L) + 2k`; `BIC = -2 log(L) + k log(n)`. `L` là likelihood của dữ liệu dưới mô hình, `k` là số tham số ước lượng, `n` là số quan sát. Giá trị thấp hơn ưu tiên hơn khi so mô hình trên cùng dữ liệu và cùng cơ sở likelihood; AIC/BIC không có ngưỡng “bình thường” độc lập với bài toán.
- Với `n = 17,379`, nêu `log(n) ≈ 9.76`: BIC phạt mỗi tham số khoảng 9.76, cao hơn mức 2 của AIC. Chỉ nêu thứ hạng/chênh lệch AIC/BIC sau khi fit MLE lại; không bê ΔAIC cũ (Poisson–NB khoảng 2.78 triệu) vào nếu nó chưa được tái tạo bằng fit hợp lệ. Nếu AIC và BIC cùng thứ hạng, đó là bằng chứng nhất quán giữa hai tiêu chí, không phải xác suất mô hình đúng.
- So sánh Poisson với NB bằng AIC/BIC trong nhóm phân phối rời rạc. Không xếp hạng NB/Poisson với Normal/Log-normal bằng AIC/BIC vì likelihood khối rời rạc và likelihood mật độ liên tục không cùng cơ sở so sánh trực tiếp trong mục tiêu này.
- Poisson yêu cầu mean gần variance; giải thích variance/mean đã biết là 173.66 nên Poisson equidispersion khó mô tả độ phân tán. Không gọi NB là phân phối sinh dữ liệu thật hoặc mô hình dự báo cuối.

### 4. Q-Q plot và goodness-of-fit

- Giải thích cách đọc Q-Q: điểm gần đường chéo nghĩa là các quantile tương ứng gần nhau; độ cong/lệch ở hai đầu chỉ ra khác biệt ở đuôi; lệch ở vùng giữa chỉ ra khác biệt phần trung tâm.
- Với `cnt` rời rạc và bị chặn dưới, không xem Q-Q plot liên tục là bằng chứng duy nhất. Đọc cùng histogram/PMF, xác suất theo khoảng và thống kê phân tán.
- Chỉ dùng KS/chi-square nếu cách áp dụng hợp lệ. Nếu dùng chi-square, gộp bins khi expected count quá nhỏ và tính bậc tự do phù hợp với tham số đã ước lượng. KS tiêu chuẩn sau khi fit tham số trên cùng mẫu không cho p-value chuẩn không điều kiện; đánh dấu là tham khảo hoặc hiệu chỉnh thích hợp.
- Với N lớn, p-value goodness-of-fit có thể rất nhỏ với sai khác thực tiễn nhỏ. Không chọn phân phối chỉ từ p-value; báo đồ thị, thống kê mô tả, AIC/BIC hợp lệ và hạn chế độc lập.

### 5. Dữ liệu `cnt` là tập hợp nhiều chế độ

- Giải thích rõ phân phối biên `cnt` trộn giờ đêm có lượng thuê rất thấp, giờ cao điểm ngày làm việc có mức thuê hàng trăm, và các giờ/ngày khác có cấu trúc riêng. EDA ghi nhận ngày làm việc có đỉnh 8h và 17h, ngày nghỉ đạt đỉnh khoảng 13h; đưa các con số này làm bằng chứng có nguồn gốc EDA.
- Dùng Hình 2.6 (mean `cnt` theo `hr` từ 0–23, hai đường `workingday=0/1`) để thể hiện nhịp giờ khác nhau. Ghi lượt thuê/giờ, ticks giờ rõ ràng và chú giải loại ngày. Đây là hình kiểm tra khác biệt theo giờ, không phải kiểm định.
- Việc trộn nhiều nhóm là lý do hợp lý để một phân phối đơn không mô tả mọi chế độ hoàn hảo; không khẳng định một latent mixture cụ thể nếu chưa fit mô hình mixture.
- Nêu rõ min `cnt=1`, không có `cnt=0`, và 6.22% dòng `cnt≤5`. Không dùng thuật ngữ zero-inflated.
- Chỉ fit zero-truncated Poisson/NB như sensitivity analysis nếu kiểm chứng được cơ chế dữ liệu chỉ ghi giờ có lượt thuê. Không kết luận zero-truncation chỉ từ min=1/không có số 0. Nếu cơ chế chưa được xác minh, nêu nghi vấn/giới hạn do các giờ không có bản ghi và không thêm fit truncated. Likelihood truncated (nếu chạy) phải điều kiện hóa trên `X>0`; không so AIC của mô hình truncated với untruncated như cùng likelihood.

### 6. `temp`, `hum`, Beta và `season`

- Fit Normal và Beta riêng cho từng biến và hiển thị histogram/density, Q-Q cho Normal cùng bảng tham số/AIC/BIC. Nêu thang chuẩn hóa 0–1.
- Beta density không xác định hữu hạn ở một số biên tùy tham số. Nếu cần clipping, chỉ áp dụng trên bản sao dùng để fit, không sửa dữ liệu gốc/dataframe phân tích. Dùng `epsilon = 0.5/n`; với `n=17,379`, `epsilon ≈ 0.0000288`. Chạy sensitivity với `epsilon=1e-4`; báo số quan sát bị clip và thay đổi tham số, log-likelihood/AIC. Chỉ viết “không ảnh hưởng đáng kể” nếu số liệu xác nhận.
- Không giải thích nhiều đỉnh của `temp` là do ghi giá trị rời rạc nếu chưa có bằng chứng. Vẽ Hình 2.7 phân phối `temp` theo `season`, rồi mới nhận xét liệu khác biệt theo mùa có thể tạo cấu trúc nhiều cụm trong phân phối tổng thể. Xác minh mapping `season` với UCI data dictionary. Nếu không xác minh được, giữ nhãn mã 1–4 và nói rõ không gán tên mùa.
- Không mặc định Beta luôn đơn đỉnh. Nhận xét giới hạn về hình dạng theo tham số Beta đã fit và so với histogram/đồ thị phân tầng; không nói Beta mô tả chính xác cơ chế sinh dữ liệu.
- Chỉ so AIC/BIC Normal với Beta trong cùng một biến, cùng quan sát và cùng cách xử lý likelihood. Không so AIC của `temp` với AIC của `hum`: đây là hai tập biến/giá trị khác nhau, likelihood có gốc khác nhau nên mức tuyệt đối không so sánh được.

### 7. `cnt` theo `workingday`

- Giữ thống kê theo nhóm (n, mean, median, SD, Q1, Q3, IQR, skewness) và biểu đồ ECDF hai nhóm; ECDF thay histogram step chồng lấn vì đường histogram cũ khó đọc ở vùng giao nhau. Có thể giữ boxplot nếu bố cục rõ và bổ sung thông tin.
- Mean EDA: ngày nghỉ 181.41 lượt/giờ; ngày làm việc 193.21 lượt/giờ (chênh khoảng 11.80). Cùng nêu median (119 so với 151) và SD (172.85 so với 185.11), không chỉ dựa vào mean.
- Đặt trọng tâm nhận xét vào hình dạng/nhịp giờ: hai nhóm có phân phối gộp chồng lấn, nhưng profile theo giờ khác nhau; tham chiếu Hình 2.6 và EDA. Chỉ kết luận mô tả. Viết rõ chưa thể cô lập ảnh hưởng riêng của `workingday` vì cơ cấu giờ, thời tiết, mùa và năm khác nhau; mọi khác biệt cần TV3 kiểm định nếu phù hợp.

## Báo cáo và bàn giao downstream

- Mỗi phần báo cáo tuân thủ logic **Mục tiêu → Phương pháp → Kết quả → Nhận xét**, và kết thúc bằng **Kết luận và hạn chế của phần**.
- Đánh số bảng/hình trong phần TV2 là `Bảng 2.x`/`Hình 2.x`. Mọi hình có tên, mục đích/lý do chọn, nhãn trục và đơn vị; sau mỗi bảng/hình có nhận xét dựa trên số liệu. Dùng dấu chấm thập phân; mean/SD/RMSE/MAE làm tròn 2 chữ số khi phù hợp, skewness, p-value, R² làm tròn 4 chữ số; p rất nhỏ ghi `p < 0.001`.
- Đồng bộ con số giữa notebook, `report.md` và `distribution_findings.md`; notebook là nguồn tính toán, report/Findings không tự nhập số khác. Không đánh dấu Findings `FINAL` nếu quy trình nhóm chưa xác nhận.
- **TV3 / V-05:** báo `cnt` lệch phải (skewness≈1.2774), over-dispersed (variance/mean≈173.66), phân phối hai nhóm `workingday`, SD nhóm 172.85 và 185.11, cùng caveat tự tương quan. Gợi ý TV3 kiểm tra giả định phương sai (cân nhắc Welch nếu dùng t-test), lệch/phân phối và effect size; không chọn test thay TV3, không dựa riêng vào p-value.
- **TV4 / V-06:** cung cấp kết quả phân phối chính thức của TV2: phân phối/skewness, ngoại lai được giữ, kết quả Normal/Beta của `temp`/`hum` và hạn chế do tự tương quan. Không ghi “đợi phân phối chính thức” sau khi TV2 hoàn tất; TV4 tự chọn Pearson/Spearman phù hợp câu hỏi và cặp biến.
- **TV5 / V-07:** không chốt target hoặc phép biến đổi thay TV5. Nêu `log1p(cnt)` skewness≈-0.8182 và `sqrt(cnt)` skewness≈0.29 như kết quả tham khảo từ EDA; nếu thử biến đổi target thì đánh giá metric cuối trên thang gốc lượt thuê/giờ.
- Findings Sheet tối thiểu có: phiên bản/file dữ liệu và biến; phương pháp; kết quả có số liệu/đơn vị; quyết định và lý do; hạn chế; lưu ý V-05/V-06/V-07; file code/hình/bảng; trạng thái và ngày.

## Phạm vi file của AI thực thi

AI thực thi sau này được phép sửa hoặc tạo chỉ các đầu ra thuộc `Distribution`:

- `Distribution/02_distribution.ipynb` - notebook tính toán, phân tích và hình.
- `Distribution/report.md` - nội dung Phần 2.
- `Distribution/distribution_findings.md` - Findings Sheet TV2.
- `Distribution/assets/` - hình được notebook sinh ra.

Không sửa `Distribution/PLAN.md` khi đang thực thi các đầu ra trên; không sửa `Distribution/README.md`, `Distribution/requirements.txt`, file dữ liệu, EDA, `HANDOFF.md`, `rules.md`, `outline.md` hoặc phần TV3–TV5. Nếu phát hiện cần mở rộng phạm vi, dừng và hỏi chủ dự án.

Quy ước tên ảnh mới: dùng tên mô tả ASCII ổn định như `fig_2_1_cnt_empirical.png`, `fig_2_2_cnt_fits.png`, `fig_2_3_cnt_qq_gof.png`, `fig_2_4_weather_fits.png`, `fig_2_5_workingday_ecdf.png`, `fig_2_6_cnt_by_hour_workingday.png`, `fig_2_7_temp_by_season.png`. Đồng bộ đường dẫn trong notebook và `report.md`; không xóa asset cũ nếu không cần thiết.

## Trình tự thực hiện

1. Xác minh input, path khi chạy từ thư mục `Distribution`, phiên bản dữ liệu, mapping `season` và cơ chế ghi nhận giờ không có lượt thuê nếu định dùng mô hình zero-truncated. Không giả định điều chưa kiểm chứng.
2. Viết lại notebook thành quy trình từ đầu đến cuối; không dựa output cache hoặc biến tồn tại trong kernel.
3. Tạo bảng mô tả, đồ thị, fit và kiểm tra tính hợp lệ/convergence; ghi lại số liệu thực tế mới.
4. Hoàn thiện diễn giải đúng phạm vi TV2, kết luận/hạn chế, và Findings Sheet V-05/V-06/V-07.
5. Đồng bộ `report.md`, Findings Sheet và assets với lần chạy sạch; kiểm tra mọi liên kết ảnh.
6. Chạy Restart Kernel → Run All trong Jupyter/VS Code và xử lý mọi lỗi trước khi bàn giao.

## Tiêu chí nghiệm thu

- [ ] Chạy từ kernel mới, toàn bộ code cell hoàn tất không lỗi; không phụ thuộc biến do chạy cell lẻ hoặc output cũ.
- [ ] Input sau khi bỏ index kỹ thuật có 17,379 × 17; chất lượng và ràng buộc khớp dữ liệu EDA; các sanity checks `cnt` gần số đã nêu ở trên.
- [ ] NB MLE optimizer báo thành công, tham số hợp lệ; log-likelihood hữu hạn; AIC/BIC tái tạo từ đúng log-likelihood và số tham số. Poisson/NB thứ hạng được tính lại, không dùng số cũ nếu chưa tái xác minh.
- [ ] Không xếp hạng AIC/BIC giữa likelihood rời rạc và liên tục hoặc giữa hai biến khác nhau; giải thích công thức, penalty và giới hạn diễn giải.
- [ ] Hình 2.1 KDE dễ phân biệt; ECDF có ticks 0–100%, đánh dấu P50/P75 chính xác.
- [ ] Hình 2.2 tách PMF/PDF, histogram liên tục có `density=True`, mỗi trục y ghi đúng đại lượng và đơn vị.
- [ ] Hình Q-Q được giải thích đúng; GOF không diễn giải chỉ bằng p-value và không bỏ qua vấn đề tham số fit/bin expected count.
- [ ] Hình 2.5 dùng ECDF nhóm dễ đọc; Hình 2.6 có hai đường mean theo `hr` và `workingday`; Hình 2.7 dùng mã `season` đã xác minh hoặc chỉ ghi mã.
- [ ] Beta epsilon và sensitivity được báo bằng kết quả thực đo; không tuyên bố “không ảnh hưởng” nếu không có bằng chứng.
- [ ] Report/Findings/Notebook khớp nhau về số liệu, tên hình, đánh số, đơn vị và kết luận; mọi ảnh được tham chiếu đều tồn tại.
- [ ] Nêu rõ tự tương quan (`r1=0.8431`, `N_eff≈1,479` theo xấp xỉ AR(1)) và hậu quả lên suy luận độc lập; không coi `N_eff` là hiệu chỉnh tự động cho AIC/BIC.
- [ ] Findings Sheet không vượt quá trạng thái xác nhận của nhóm và bàn giao đủ thông tin cho V-05, V-06, V-07.

## Theo dõi tiến độ hiện tại

| Phần | Trạng thái | Đã hoàn thành | Còn cần làm |
| --- | --- | --- | --- |
| 2.1 Kiểm tra dữ liệu đầu vào | Hoàn thành | Notebook đọc đúng `EDA/cleaned_data/hour_cleaned.csv`, xử lý cột index kỹ thuật, hiển thị schema gồm tên và kiểu dữ liệu của 17 biến, kiểm tra shape, thiếu/trùng, khóa (`dteday`, `hr`), quan hệ `cnt = casual + registered`, `cnt = 0`, min/max `cnt` và `hum = 0`. Output đã lưu khớp baseline 17,379 × 17; Bảng 2.1 trình bày kết quả và đối chiếu baseline. | Không còn thiếu sót nội dung đáng kể. |
| 2.2 Thống kê mô tả | Hoàn thành | Notebook tính và hiển thị `n`, mean, median, SD, min, Q1, Q3, max, IQR, skewness và excess kurtosis cho `cnt`, `temp`, `hum`; tính variance/mean cho `cnt`. Bảng 2.2 đã lưu đủ các chỉ tiêu và phần nhận xét diễn giải độ lệch, độ phân tán, thang đo và giới hạn mô tả. | Không còn thiếu sót phân tích đáng kể. Còn một câu biên tập nhỏ trong phần phương pháp nói bảng theo số liệu báo cáo trước; nên sửa để nhất quán với code tính trực tiếp từ `df`. |
| 2.3 Phân phối thực nghiệm của `cnt` | Hoàn thành | Notebook tính động các thống kê và tỷ lệ trọng tâm (`n`, mean, median, Q1, Q3, IQR, min/max, `cnt ≤ 5`, trên ngưỡng Q3 + 1.5 × IQR); tạo Hình 2.1 gồm histogram + KDE tham khảo, ECDF với mốc P50/P75 và boxplot. Phần giải thích phân biệt KDE với PMF, nêu bước nhảy ECDF do dữ liệu rời rạc và cảnh báo không đồng nhất điểm ngoài râu với lỗi; output đã lưu cho thấy Hình 2.1 được tạo trong `Distribution/assets/fig_2_1_cnt_empirical.png` và các sanity checks khớp baseline. | Không còn thiếu sót phân tích đáng kể. Có thể dọn cảnh báo deprecation của tham số `vert` trong boxplot và một vài lỗi biên tập nhỏ trong Markdown; không ảnh hưởng kết quả hiện tại. |

**Căn cứ trạng thái:** nội dung, bảng và output hiện có của các phần 2.1–2.3 đã được rà soát. Theo yêu cầu, việc chạy lại kernel không được dùng làm điều kiện đánh giá tiến độ ở đây. Trạng thái hoàn thành chỉ áp dụng cho 2.1–2.3, không đồng nghĩa toàn bộ notebook hoặc các phần còn lại đã nghiệm thu.
