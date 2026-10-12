# PHẦN 3. KIỂM ĐỊNH GIẢ THUYẾT (HYPOTHESIS TESTING)

**Thành viên phụ trách:** Thành viên 3 (TV3)  
**Tập dữ liệu đầu vào:** `EDA/cleaned_data/hour_cleaned.csv` ($N = 17,379$ dòng quan sát theo giờ, đã qua tiền xử lý bởi TV1)  
**Tài liệu tham khảo chuyên khảo cốt lõi:** *100 Statistical Tests (3rd Edition, 2006)* — **Gopal K. Kanji**, SAGE Publications.  

---

## 3.1. Đặt vấn đề Nghiệp vụ & Cơ sở Lý thuyết các Phương pháp Kiểm định

### 3.1.1. Động cơ Thực tiễn và Xác lập 2 Câu hỏi Nghiên cứu (RQ1 & RQ2)

Trong quản lý và khai thác hệ thống xe đạp chia sẻ công cộng Capital Bikeshare tại thủ đô Washington D.C., mọi quyết định phân bổ nguồn lực và điều phối phương tiện đều tác động trực tiếp đến chi phí vận hành và chất lượng dịch vụ hành khách. Người quản lý hệ thống không thể đưa ra các chính sách can thiệp chỉ dựa trên trực giác hoặc những con số chênh lệch trung bình mẫu thô, bởi lẽ biến động mẫu có thể chỉ là sự ngẫu nhiên thuần túy.

Hai bài toán vận hành chiến lược đòi hỏi phải có câu trả lời định lượng dựa trên bằng chứng thống kê vững chắc bao gồm:

1. **Bài toán Điều phối Đội xe Hàng ngày (Daily Fleet Scheduling):**
   - *Bối cảnh thực tế:* Nhà vận hành cần quyết định liệu có nên thay đổi tổng quy mô xe đạp cung ứng ra thị trường giữa ngày làm việc hành chính (`workingday = 1`) và ngày nghỉ cuối tuần (`workingday = 0`) hay không? 
   - *Vấn đề cốt lõi:* Liệu tổng nhu cầu thuê xe trung bình mỗi giờ giữa hai loại ngày có thực sự khác biệt có ý nghĩa thống kê, hay tổng quy mô 24 giờ là tương đương và sự khác biệt thực chất chỉ nằm ở sự phân hóa nhịp giờ cao điểm?
2. **Bài toán Bảo dưỡng & Cân bằng Trạm Theo Mùa vụ (Seasonal Rebalancing & Fleet Maintenance):**
   - *Bối cảnh thực tế:* Khí hậu tại Washington D.C. phân hóa rõ nét qua 4 mùa trong năm. Nhu cầu đi lại ngoài trời biến động mạnh mẽ theo chu kỳ thời tiết.
   - *Vấn đề cốt lõi:* Nhu cầu thuê xe thay đổi ra sao qua 4 mùa? Mùa nào sụt giảm sâu nhất để nhà vận hành chủ động thu hồi bớt xe về xưởng đại tu định kỳ, và mùa nào đạt đỉnh để dồn toàn bộ nguồn lực phương tiện và nhân sự tái cân bằng trạm? Giữa 4 mùa, những cặp mùa nào thực sự có sự chênh lệch có ý nghĩa thống kê?

Từ hai bài toán thực tiễn nêu trên, nghiên cứu chính thức xác lập **2 Câu hỏi Nghiên cứu (Research Questions - RQ)** làm kim chỉ nam phương pháp luận:

> * **Câu hỏi Nghiên cứu 1 (RQ1):**  
>   *Có sự khác biệt có ý nghĩa thống kê về số lượng thuê xe trung bình mỗi giờ (`cnt`) giữa ngày làm việc (`workingday = 1`) và ngày nghỉ / cuối tuần (`workingday = 0`) hay không?*
>
> * **Câu hỏi Nghiên cứu 2 (RQ2):**  
>   *Số lượng thuê xe trung bình mỗi giờ (`cnt`) có sự khác biệt có ý nghĩa thống kê giữa 4 mùa trong năm (`season`: Mùa xuân, Mùa hè, Mùa thu, Mùa đông) hay không? Cụ thể những cặp mùa nào tạo ra sự khác biệt có ý nghĩa thống kê?*

---

### 3.1.2. Bản chất của Kiểm định Thống kê & Quy trình 5 bước Chuẩn tắc (Neave-Kanji Framework)

#### 1. Vì sao phải thực hiện kiểm định giả thuyết thống kê?
Khi quan sát dữ liệu thực nghiệm, ta ghi nhận số lượt thuê xe trung bình mỗi giờ vào ngày làm việc là $\overline{x}_1 = 193.21 \text{ lượt/giờ}$, trong khi ngày nghỉ là $\overline{x}_0 = 181.41 \text{ lượt/giờ}$ (chênh lệch $11.80 \text{ lượt/giờ}$). Tương tự, trung bình mùa xuân là $111.11 \text{ lượt/giờ}$, thấp hơn đáng kể so với mùa thu là $236.02 \text{ lượt/giờ}$.

Tuy nhiên, trong thống kê suy diễn, mọi bộ dữ liệu quan sát được đều chỉ là **một mẫu ngẫu nhiên hữu hạn** được rút ra từ tổng thể hành vi người dùng. Sự chênh lệch giữa các số trung bình mẫu luôn tồn tại hai khả năng:
- **Khả năng 1 (Nhiễu ngẫu nhiên):** Chênh lệch quan sát được chỉ là sự ngẫu nhiên phát sinh trong quá trình lấy mẫu (Sampling variation / Random noise), trong khi bản chất hai tổng thể không hề khác biệt.
- **Khả năng 2 (Quy luật thực chất):** Chênh lệch quan sát được phản ánh một sự khác biệt thực chất và có tính quy luật của tổng thể.

Kiểm định giả thuyết thống kê (Hypothesis Testing) là công cụ toán học duy nhất giúp định lượng xác suất xuất hiện của sự chênh lệch do ngẫu nhiên, từ đó cung cấp căn cứ khách quan để đưa ra quyết định nghiệp vụ đáng tin cậy.

#### 2. Triết lý kiểm định nền tảng theo Gopal K. Kanji (2006, tr. 2)
Theo chuyên khảo *100 Statistical Tests* của Gopal K. Kanji (2006), có hai nguyên tắc triết lý căn bản mà người thực hiện kiểm định phải tuân thủ:
- **Kiểm định không nhằm "chứng minh" giả thuyết:** Phép thử thống kê không được thiết kế để chứng minh hay khẳng định bất kỳ một giả thuyết nào là chân lý tuyệt đối. Mục tiêu duy nhất của kiểm định là **chỉ ra rằng một ý niệm (giả thuyết) là không thể đứng vững (untenable) khi nó dẫn tới một xác suất xảy ra quá nhỏ trong thực tế**.
- **Giả thuyết Không ($H_0$ — Null Hypothesis) luôn đại diện cho trạng thái giữ nguyên (Status Quo):** Giả thuyết mà ta tìm bằng chứng để bác bỏ luôn là giả thuyết "không có sự thay đổi / không có sự khác biệt" (ví dụ: $\mu_1 = \mu_2$).
- **Nguyên tắc vàng về kết luận:** **Tuyệt đối không bao giờ kết luận "chấp nhận $H_0$"**. Trong thống kê khoa học, khi dữ liệu chưa đủ bằng chứng, ta chỉ kết luận: *"Chưa đủ bằng chứng thống kê để bác bỏ $H_0$"* (Do not reject $H_0$), tương tự như nguyên tắc suy đoán vô tội trong pháp lý.

#### 3. Quy trình Kiểm định 5 Bước Chuẩn tắc (Neave-Kanji Five-Step Method)
Để đảm bảo tính nhất quán và chặt chẽ, nghiên cứu áp dụng quy trình 5 bước được Gopal K. Kanji (2006, tr. 2–3) hệ thống hóa từ phương pháp luận của H.R. Neave (1976):

1. **Bước 1 — Phát biểu bài toán thành cặp Giả thuyết ($H_0$ và $H_1$):**
   - *Giả thuyết đối ($H_1$ — Alternative / Action Hypothesis):* Đại diện cho tình huống mà nhà nghiên cứu muốn tìm kiếm bằng chứng để đưa ra hành động can thiệp (ví dụ: tồn tại sự khác biệt giữa các nhóm). $H_1$ quyết định bài toán là kiểm định hai phía (Two-tailed) hay một phía (One-tailed).
   - *Giả thuyết không ($H_0$ — Null Hypothesis / Status Quo):* Điểm tựa chuẩn đối chứng, khẳng định không có sự khác biệt giữa các nhóm.
2. **Bước 2 — Xây dựng Thống kê Kiểm định ($T$):**
   - Thống kê kiểm định $T(X)$ là một hàm toán học thuần túy của dữ liệu mẫu. Một thống kê kiểm định tốt phải thỏa mãn hai tiêu chuẩn vàng:
     + Có hành vi phân phối phân hóa rõ rệt khi $H_0$ đúng so với khi $H_1$ đúng;
     + Có hàm phân phối xác suất lý thuyết tính toán được chính xác dưới giả định $H_0$ đúng (ví dụ: phân phối Student's $t$, Fisher's $F$, Chi-square $\chi^2$, hoặc chuẩn hóa tiệm cận $Z$).
3. **Bước 3 — Xác lập Miền Bác bỏ (Critical Region):**
   - Dựa trên phân phối của $T$ dưới $H_0$, xác định tập hợp các giá trị của $T$ mà nếu rơi vào đó, khả năng $H_0$ xảy ra là cực kỳ hiếm hoi. Nếu giá trị thống kê $T_{\text{cal}}$ tính từ dữ liệu rơi vào miền bác bỏ, ta bác bỏ $H_0$ để ủng hộ $H_1$; nếu nằm ngoài miền bác bỏ, ta chưa đủ cơ sở bác bỏ $H_0$.
4. **Bước 4 — Thiết lập Mức Ý nghĩa $\alpha$ & Kiểm soát Rủi ro Sai lầm:**
   - Khi ra quyết định thống kê, luôn tồn tại hai loại sai lầm cố hữu:
     + **Sai lầm loại 1 (Type I Error — $\alpha$):** Bác bỏ $H_0$ khi thực chất $H_0$ đúng (Báo động giả / False Positive). Nghiên cứu cố định mức ý nghĩa chuẩn tắc $\alpha = 0.05$ ($5\%$).
     + **Sai lầm loại 2 (Type II Error — $\beta$):** Không bác bỏ $H_0$ khi thực chất $H_0$ sai (Bỏ sót / False Negative). Đại lượng $1 - \beta$ được gọi là **Lực lượng phép thử (Power of the Test)**, biểu thị xác suất phát hiện thành công một sự khác biệt thực tế.
5. **Bước 5 — Ra quyết định Thực tế, Lượng hóa Kích thước Hiệu ứng & Đánh giá Độ bền vững (Robustness):**
   - Tính toán giá trị xác suất thực tế ($p\text{-value}$): Xác suất quan sát được một giá trị thống kê cực đoan ít nhất bằng giá trị tính toán được từ mẫu, giả sử $H_0$ đúng. So sánh $p\text{-value}$ với $\alpha$: nếu $p < \alpha$, bác bỏ $H_0$.
   - **Đánh giá Độ bền vững (Robustness):** Theo Kanji (2006, tr. 3–4), một phép thử được gọi là "vững" (robust) nếu kết luận của nó ít bị sai lệch khi các giả định toán học nền tảng (như giả định chuẩn hay phương sai bằng nhau) bị vi phạm.
   - **Lượng hóa Kích thước Hiệu ứng (Effect Size):** Khi cỡ mẫu rất lớn ($N = 17,379$), $p\text{-value}$ gần như luôn đạt ý nghĩa thống kê ($p < 0.001$). Do đó, bắt buộc phải báo cáo thêm Effect Size (Cohen's $d$, Eta-squared $\eta^2$) để đánh giá xem mức độ chênh lệch có đủ lớn để mang lại ý nghĩa thực tiễn hay không.

---

### 3.1.3. Bốn Đặc trưng Định danh Chung để Xác định một Họ Phép thử Thống kê

Theo hệ thống phân loại của Gopal K. Kanji (2006, *Classification of Tests*, tr. 19–20), trong kho tàng hàng trăm phép kiểm định thống kê, việc lựa chọn chính xác phép thử cho Bước 2 trong quy trình 5 bước được quyết định dựa trên **4 đặc trưng định danh chung cốt lõi**:

1. **Bản chất Biến số và Thang đo (Data Types & Measurement Scales):**
   - Biến phụ thuộc là biến định lượng liên tục (Continuous), biến đếm tỷ lệ (Ratio/Count như `cnt`, `temp`) hay biến phân loại định danh/thứ bậc (Nominal/Ordinal như `season`, `workingday`, `weathersit`)?
   - Thang đo quyết định các phép toán số học có ý nghĩa hay không: Biến định lượng cho phép tính trung bình và phương sai; biến định danh chỉ cho phép đếm tần số xuất hiện.
2. **Thiết kế Mẫu và Số lượng Nhóm So sánh (Sample Design & Number of Groups):**
   - Thiết kế nghiên cứu thuộc dạng một mẫu so sánh với giá trị chuẩn lý thuyết ($\mu_0$)?
   - So sánh giữa hai nhóm mẫu độc lập (Two Independent Samples) hay hai nhóm mẫu từng cặp phụ thuộc (Paired/Matched Samples)?
   - Hay bài toán so sánh đồng thời đa nhóm ($K \ge 3$ groups)?
3. **Tham số Mục tiêu cần Kiểm định (Parameter of Interest):**
   - Phép thử nhằm so sánh đặc trưng nào của phân phối tổng thể:
     + Giá trị kỳ vọng trung bình ($\mu$)?
     + Độ phân tán / Phương sai ($\sigma^2$)?
     + Tần số quan sát so với kỳ vọng ($O_{ij}$ vs $E_{ij}$)?
     + Thứ hạng phân bố và Trung vị (Ranks / Median)?
4. **Giả định Phân phối Mẫu (Distributional Assumptions):**
   - Phép thử có tiền giả định tổng thể tuân theo phân phối chuẩn (*Kiểm định Tham số — Parametric Tests*) hay chấp nhận mọi dạng phân phối tự do (*Kiểm định Phi tham số — Non-parametric / Distribution-free Tests*)?
   - Phép thử có bắt buộc phương sai giữa các nhóm phải đồng nhất (Homoscedasticity) hay chấp nhận phương sai dị biệt (Heteroscedasticity)?

---

### 3.1.4. Bản chất của các Họ Phép thử theo 4 Đặc trưng Định danh & Nguyên lý Họ Phi tham số

Dựa trên 4 đặc trưng định danh ở Mục 3.1.3, bản chất lý thuyết của **3 họ kiểm định tham số kinh điển** và **nguyên lý nền tảng của họ Phi tham số** được hệ thống hóa chi tiết theo chuyên khảo Gopal K. Kanji (2006):

#### 1. Họ phép thử $t$-test (So sánh trung bình 2 nhóm định lượng)
- **Định danh qua 4 đặc trưng:** Biến phụ thuộc định lượng liên tục/biến đếm; số nhóm so sánh tối đa 2 nhóm; tham số mục tiêu là Giá trị trung bình $\mu$; thống kê kiểm định tuân theo phân phối Student's $t$ với bậc tự do $\nu$.
- **Phân hóa nội bộ họ theo sách Kanji (2006):**
  - **Student's $t$-test hai mẫu độc lập (Kanji Test 8, tr. 31):**
    + *Mục đích & Khi nào dùng:* So sánh kỳ vọng trung bình của hai tổng thể độc lập ($\mu_1$ vs $\mu_2$) khi phương sai tổng thể chưa biết nhưng được giả định là bằng nhau ($\sigma_1^2 = \sigma_2^2$).
    + *Giả định:* Cả hai tổng thể tuân theo phân phối chuẩn VÀ có phương sai đồng nhất.
    + *Thống kê kiểm định:*
      $$t = \frac{\overline{x}_1 - \overline{x}_2}{s_p \sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}$$
      Trong đó $s_p^2 = \frac{(n_1 - 1)s_1^2 + (n_2 - 1)s_2^2}{n_1 + n_2 - 2}$ là phương sai gộp (Pooled variance), bậc tự do $\nu = n_1 + n_2 - 2$.
  - **Welch's $t$-test (Kanji Test 9, tr. 33 — Two-sample $t$-test with unequal variances):**
    + *Mục đích & Khi nào dùng:* So sánh kỳ vọng trung bình của hai tổng thể độc lập khi **phương sai của hai nhóm không bằng nhau ($\sigma_1^2 \neq \sigma_2^2$)**.
    + *Thống kê kiểm định:* Loại bỏ phương sai gộp, sử dụng trực tiếp sai số chuẩn riêng biệt:
      $$t^* = \frac{\overline{x}_1 - \overline{x}_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}$$
      Bậc tự do được hiệu chỉnh theo công thức xấp xỉ Satterthwaite-Welch:
      $$\nu_{\text{Welch}} = \frac{\left(\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}\right)^2}{\frac{(s_1^2/n_1)^2}{n_1 - 1} + \frac{(s_2^2/n_2)^2}{n_2 - 1}}$$
    + *Ưu thế:* Miễn nhiễm hoàn toàn với sự vi phạm giả định phương sai bằng nhau, là lựa chọn tham số tối ưu khi kiểm định dữ liệu thực tế.

#### 2. Họ phép thử ANOVA (Phân tích phương sai đa nhóm $K \ge 3$)
- **Định danh qua 4 đặc trưng:** Biến phụ thuộc định lượng; biến độc lập phân loại từ 3 nhóm trở lên ($K \ge 3$); tham số mục tiêu là so sánh đồng thời $K$ giá trị trung bình tổng thể: $H_0: \mu_1 = \mu_2 = \dots = \mu_K$; thống kê kiểm định $F$ tuân theo phân phối Fisher-Snedecor.
- **Phân hóa nội bộ họ theo sách Kanji (2006):**
  - **One-way ANOVA tiêu chuẩn (Kanji Test 22, tr. 55):**
    + *Nguyên lý hoạt động:* Phân rã tổng biến thiên toàn phần (Total Sum of Squares - $\text{SS}_{\text{total}}$) thành hai thành phần độc lập: Biến thiên giữa các nhóm (Between-group - $\text{SS}_{\text{between}}$) và Biến thiên nội bộ trong từng nhóm (Within-group / Error - $\text{SS}_{\text{within}}$).
    + *Thống kê kiểm định:*
      $$F = \frac{\text{MS}_{\text{between}}}{\text{MS}_{\text{within}}} = \frac{\text{SS}_{\text{between}} / (K - 1)}{\text{SS}_{\text{within}} / (N - K)} \sim F(K - 1, N - K)$$
    + *Giả định bắt buộc:* Các nhóm phân phối chuẩn và phương sai giữa các nhóm phải đồng nhất.
  - **Welch's ANOVA (Hiệu chỉnh phương sai không đồng nhất):**
    + Khi kiểm định Levene bác bỏ giả định phương sai đồng nhất, One-way ANOVA tiêu chuẩn sẽ làm tăng tỷ lệ sai lầm loại 1. Welch's ANOVA áp dụng trọng số nghịch đảo phương sai từng nhóm ($w_i = n_i / s_i^2$) để hiệu chỉnh thống kê $F$, mang lại kết luận tham số vững chắc.
  - **Kiểm định Hậu định (Post-hoc Comparisons — Kanji Test 28, tr. 65):**
    + *Bản chất Omnibus Test:* Cả ANOVA và Welch's ANOVA chỉ là kiểm định toàn cục (*Omnibus test*). Khi bác bỏ $H_0$, phép thử chỉ khẳng định có ít nhất một cặp nhóm khác nhau, nhưng không cho biết chính xác cặp nào khác nhau.
    + *Rủi ro sai số tích lũy (Family-wise Error Rate - FWER):* Nếu thực hiện nhiều phép thử $t$ riêng lẻ cho $m = \frac{K(K-1)}{2}$ cặp so sánh, xác suất mắc ít nhất một Sai lầm loại 1 sẽ bùng nổ theo công thức $\alpha_{\text{family}} = 1 - (1 - \alpha)^m$ (với 4 mùa, $m = 6$ cặp $\rightarrow \alpha_{\text{family}} \approx 26.5\%$).
    + *Giải pháp:* Kích hoạt các bài kiểm định hậu định chuyên biệt: **Games-Howell post-hoc test** (Kanji Test 28, dành riêng cho trường hợp phương sai không bằng nhau) hoặc **Tukey HSD** để kiểm soát nghiêm ngặt FWER ở mức $0.05$.

#### 3. Họ phép thử Chi-square ($\chi^2$) (Phân tích biến phân loại / Bảng chéo)
- **Định danh qua 4 đặc trưng:** Cả hai biến đều là biến phân loại (Categorical/Nominal); tham số mục tiêu là sự sai khác giữa tần số quan sát thực tế ($O_{ij}$) và tần số kỳ vọng ngẫu nhiên lý thuyết ($E_{ij}$); thống kê kiểm định tuân theo phân phối $\chi^2$.
- **Phân hóa nội bộ họ theo sách Kanji (2006):**
  - **$\chi^2$ Goodness-of-Fit (Kanji Test 37, tr. 79):** Kiểm tra tần số xuất hiện của một biến phân loại có phù hợp với một tỷ lệ lý thuyết định trước hay không.
  - **$\chi^2$ Test of Independence (Kanji Test 44, tr. 91 — Pearson Chi-square Independence):**
    + *Mục đích:* Kiểm tra tính độc lập giữa hai thuộc tính phân loại trong bảng chéo hai chiều (Contingency table $r \times c$).
    + *Thống kê kiểm định:*
      $$\chi^2 = \sum_{i=1}^r \sum_{j=1}^c \frac{(O_{ij} - E_{ij})^2}{E_{ij}} \sim \chi^2(\nu)$$
      Trong đó $E_{ij} = \frac{R_i \times C_j}{N}$ là tần số kỳ vọng dưới giả thuyết độc lập, bậc tự do $\nu = (r - 1)(c - 1)$.
    + *Giới hạn bắt buộc:* Tất cả các ô kỳ vọng phải thỏa điều kiện $E_{ij} \ge 5$. Nếu có ô có tần số kỳ vọng $< 5$, kết luận của $\chi^2$ mất tính chính xác và bắt buộc phải gộp nhóm mẫu hiếm.

#### 4. Nguyên lý Nền tảng của Họ Phi tham số (Distribution-free Tests)
- **Nguyên lý Chuyển đổi Thứ hạng (Rank Transformation):**
  + Thay vì dựa vào giả định dữ liệu phải có dạng hình chuông (chuẩn) và sử dụng giá trị số đo thực (rất dễ bị bóp méo bởi ngoại lai và độ lệch), họ phi tham số **chuyển đổi toàn bộ $N$ giá trị quan sát thành Thứ hạng (Ranks)** từ nhỏ nhất đến lớn nhất ($1, 2, \dots, N$).
  + Phép thử so sánh **Tổng thứ hạng (Rank Sum) hoặc Trung vị (Median)** giữa các nhóm thay vì so sánh kỳ vọng trung bình.
- **Lợi thế phương pháp luận:** Hoàn toàn không phụ thuộc vào phân phối gốc (*Distribution-free*), miễn nhiễm với độ lệch phải và các giá trị cực trị lớn của biến `cnt`.
- **Hệ thống đại diện đối ứng trực tiếp:**
  - **Mann-Whitney $U$ test (Kanji Test 48, tr. 96 — Wilcoxon-Mann-Whitney Rank-sum Test):** Đối ứng phi tham số trực tiếp của Student/Welch $t$-test cho 2 nhóm độc lập. Thống kê $U = \min(U_1, U_2)$ dựa trên tổng thứ hạng $R_1, R_2$.
  - **Two-sample Kolmogorov-Smirnov test (Kanji Test 49, tr. 97):** Đo khoảng cách cực đại $D = \sup_x |F_1(x) - F_0(x)|$ giữa hai hàm phân phối tích lũy thực nghiệm để kiểm tra sự sai khác toàn diện về hình thái phân phối.
  - **Kruskal-Wallis $H$-test (Kanji Test 51 & 54, tr. 99, 104):** Đối ứng phi tham số trực tiếp của One-way ANOVA cho $K \ge 3$ nhóm. Thống kê $H = \frac{12}{N(N+1)} \sum_{i=1}^K \frac{R_i^2}{n_i} - 3(N+1)$ tiệm cận phân phối $\chi^2(K-1)$.
  - **Dunn's Post-hoc Test kết hợp hiệu chỉnh Bonferroni:** Kiểm định so sánh cặp phi tham số, áp dụng ngưỡng ý nghĩa điều chỉnh $\alpha_{\text{adj}} = \alpha / m$ để chống lạm phát Sai lầm loại 1.

---

### 3.1.5. Bảng Tổng hợp: Các Phép kiểm định được dùng trong Bài thuộc 4 Họ kiểm định

Dựa trên sự đối chiếu chặt chẽ giữa giới hạn phương pháp luận trong giáo trình Gopal K. Kanji (2006) và đặc tính thực nghiệm của bộ dữ liệu Bike Sharing, Bảng 3.1 xác lập toàn bộ các phép kiểm định được đưa vào thực thi trong nghiên cứu:

**Bảng 3.1. Tổng hợp các phép kiểm định thống kê sử dụng trong Chương 3**

| Họ kiểm định | Phép kiểm định cụ thể trong bài | Mã sách Kanji (2006) | Tham số / Thống kê mục tiêu | Căn cứ lựa chọn dựa trên Dữ liệu thực tế |
| :--- | :--- | :--- | :--- | :--- |
| **Họ Kiểm tra Giả định** | **Levene's Test** | Kanji Test 31 (tr. 71) | Phương sai giữa các nhóm ($\sigma_i^2 = \sigma_j^2$) | Kiểm tra giả định đồng nhất phương sai trước khi chạy $t$-test và ANOVA. Dùng trung vị thay vì trung bình để kháng độ lệch của `cnt`. |
| **Họ $t$-test (Tham số)** | **Welch's $t$-test** | Kanji Test 9 (tr. 33) | Trung bình 2 nhóm ngày ($\mu_1$ vs $\mu_0$) | Thích ứng khi phương sai giữa ngày làm việc và ngày nghỉ không bằng nhau; cỡ mẫu lớn kích hoạt CLT. |
| **Họ ANOVA (Tham số)** | **Welch's ANOVA** | Kanji Test 22 (adj, tr. 55) | Đồng thời 4 trung bình mùa ($\mu_1 = \dots = \mu_4$) | Thích ứng tối ưu khi phương sai 4 mùa chênh lệch rất lớn ($\text{Std} = 119.22$ ở Mùa xuân vs $197.71$ ở Mùa thu). |
| | **Games-Howell Post-hoc** | Kanji Test 28 (tr. 65) | Chênh lệch cặp mùa ($\mu_i - \mu_j$) | So sánh chi tiết 6 cặp mùa trong điều kiện phương sai không bằng nhau mà vẫn kiểm soát FWER ở mức 0.05. |
| **Họ Phi tham số (Distribution-free)** | **Mann-Whitney $U$ test** | Kanji Test 48 (tr. 96) | Thứ hạng & Trung vị 2 nhóm | Đối chứng phi tham số cho Welch's $t$-test; miễn nhiễm hoàn toàn với độ lệch phải ($\text{Skew} = 1.28$) của `cnt`. |
| | **Two-sample KS-test** | Kanji Test 49 (tr. 97) | Khoảng cách tích lũy $\sup \|F_1(x) - F_0(x)\|$ | So sánh sự khác biệt toàn diện về hình thái phân phối xác suất giữa Ngày làm việc và Ngày nghỉ. |
| | **Kruskal-Wallis $H$-test** | Kanji Test 51/54 (tr. 99, 104) | Thứ hạng trung bình 4 mùa | Đối chứng phi tham số cho ANOVA; đánh giá sự khác biệt giữa 4 mùa không cần giả định chuẩn. |
| | **Dunn-Bonferroni Post-hoc** | Mở rộng Test 51/54 | Chênh lệch thứ hạng cặp | So sánh cặp phi tham số với hiệu chỉnh mức ý nghĩa Bonferroni $\alpha_{\text{adj}} = 0.05 / 6 \approx 0.0083$. |
| **Họ Đánh giá Chuỗi** | **Serial Autocorrelation** | Kanji Test 64 (tr. 120) | Tự tương quan chuỗi bậc 1 ($r_1$) | Lượng hóa mức độ trùng lặp thông tin để tính cỡ mẫu hiệu dụng $N_{\text{eff}} \approx 1,479$, kiểm soát rủi ro Sai lầm loại 1. |

---

### 3.1.6. Căn cứ Thực nghiệm từ EDA & Phân phối: Thách thức Cỡ mẫu lớn và Tự tương quan chuỗi ($N_{\text{eff}}$)

Toàn bộ hệ thống kiểm định ở Bảng 3.1 được thiết kế trực tiếp dựa trên các phát hiện định lượng chuyển giao từ TV1 (EDA) và TV2 (Phân tích phân phối xác suất):

1. **Biến mục tiêu `cnt` vi phạm nghiêm trọng giả định phân phối chuẩn:**
   - TV1 xác nhận: $\text{Mean} = 189.46 > \text{Median} = 142.00$, $\text{Skewness} = 1.28$, $\text{Kurtosis} = 1.42$, tỷ số phân tán $\text{Variance} / \text{Mean} = 173.66 \gg 1$.
   - TV2 chứng minh: Phân phối Chuẩn (Normal) khớp rất kém với dữ liệu (AIC lên tới $230,086$), đường Q-Q plot (đã trình bày tại Hình 2.3 trong Báo cáo Chương 2) bị cong gãy nặng nề ở hai đầu mút; mô hình Negative Binomial mô tả tối ưu hơn nhiều (AIC = $217,615$).
   - *Hàm ý phương pháp luận:* Loại bỏ hoàn toàn Student's $t$-test tiêu chuẩn và One-way ANOVA cổ điển. Bắt buộc phải triển khai song song kiểm định hiệu chỉnh phương sai (Welch) và các kiểm định phi tham số (Mann-Whitney $U$, Kruskal-Wallis).
2. **Phương sai dị biệt (Heteroscedasticity) giữa các phân nhóm:**
   - Độ biến thiên của `cnt` chênh lệch cực lớn giữa các mùa: Mùa xuân có $\text{Std} = 119.22$ trong khi Mùa thu có $\text{Std} = 197.71$. Giữa ngày làm việc và ngày nghỉ cũng có sự chênh lệch ($\text{Std} = 185.11$ vs $172.85$). Do đó, mọi kiểm định tham số bắt buộc phải dùng phiên bản hiệu chỉnh phương sai bất đồng nhất (Welch's $t$, Welch's ANOVA, Games-Howell).
3. **Thách thức Bẫy cỡ mẫu lớn (Large Sample Size Artifact) & Kích thước hiệu ứng:**
   - Với quy mô dữ liệu danh nghĩa rất lớn $N = 17,379$, các phép kiểm định thống kê chuẩn tắc gần như luôn trả về $p\text{-value} < 0.001$ ngay cả khi mức độ khác biệt thực tế giữa hai nhóm là vô cùng nhỏ.
   - Để tránh ngộ nhận giữa "ý nghĩa thống kê" (Statistical significance) và "ý nghĩa thực tiễn" (Practical / Business significance), nghiên cứu bắt buộc phải áp dụng quy chuẩn lượng hóa Kích thước hiệu ứng theo Cohen (1988):
     + Với RQ1 (2 nhóm): Lượng hóa bằng **Cohen's $d$** (tham số) và **Rank-biserial correlation $r$** (phi tham số). Ngưỡng tối thiểu để thừa nhận có hiệu ứng thực tế là $|d| \ge 0.20$.
     + Với RQ2 (4 nhóm): Lượng hóa bằng **Eta-squared ($\eta^2$)**, **Omega-squared ($\omega^2$)** và **Epsilon-squared ($\epsilon^2$)**. Ngưỡng tối thiểu là $\eta^2 \ge 0.01$.
4. **Thách thức Tự tương quan chuỗi thời gian & Cỡ mẫu hiệu dụng ($N_{\text{eff}}$):**
   - TV1 chứng minh dữ liệu chuỗi thời gian theo giờ có hệ số tự tương quan bậc 1 rất cao: $r_1 = 0.8431$. Điều này vi phạm tiền giả định nền tảng của thống kê cổ điển là các quan sát phải độc lập và cùng phân phối (IID - Independent and Identically Distributed).
   - Theo lý thuyết chuỗi thời gian (trích dẫn trong Kanji Test 64), sự phụ thuộc chuỗi khiến lượng thông tin thực tế bị trùng lặp, làm suy giảm **Cỡ mẫu hiệu dụng thực tế xuống chỉ còn $N_{\text{eff}} \approx 1,479$ quan sát** (chiếm $\approx 8.51\%$ tổng số dòng danh nghĩa):
     $$N_{\text{eff}} = N \frac{1 - r_1}{1 + r_1} = 17,379 \times \frac{1 - 0.8431}{1 + 0.8431} \approx 1,479$$
   - Nếu không kiểm soát, các thống kê $t$ và $F$ danh nghĩa sẽ bị phóng đại nhân tạo lên khoảng $\sqrt{N / N_{\text{eff}}} \approx \sqrt{17,379 / 1,479} \approx 3.43 \text{ lần}$, dẫn đến nguy cơ bùng nổ **Sai lầm loại 1 (Type I Error)**. Nghiên cứu sẽ tiến hành kiểm tra độ bền vững bằng cách hiệu chỉnh thống kê theo $N_{\text{eff}}$ và đối chứng trên chuỗi tổng hợp cấp độ ngày ($N_{\text{day}} = 731$).

---

## 3.2. Thực thi Kiểm định cho 2 Câu hỏi Nghiên cứu

Sau khi xác lập cơ sở phương pháp luận và bảng phân loại kiểm định ở Mục 3.1, phần này tiến hành triển khai chi tiết quy trình 5 bước Neave-Kanji cho hai câu hỏi nghiên cứu cốt lõi trên tập dữ liệu sạch `EDA/cleaned_data/hour_cleaned.csv` ($N = 17,379$).

---

### 3.2.1. Nghiên cứu RQ1: So sánh 2 Nhóm Độc lập — Ngày làm việc (`workingday = 1`) và Ngày nghỉ (`workingday = 0`)

#### 1. Bước 1: Phát biểu Cặp Giả thuyết Thống kê
Nhằm trả lời bài toán điều phối đội xe hàng ngày (Daily Fleet Scheduling), nghiên cứu kiểm tra xem liệu nhu cầu thuê xe trung bình mỗi giờ giữa ngày làm việc hành chính và ngày nghỉ/cuối tuần có sự khác biệt thực chất hay không:
- **Giả thuyết Không ($H_0$):** Không có sự khác biệt về số lượng thuê xe trung bình mỗi giờ giữa ngày làm việc và ngày nghỉ.
  $$H_0: \mu_{\text{workingday}} = \mu_{\text{non-workingday}} \quad (\text{hoặc } \mu_1 - \mu_0 = 0)$$
- **Giả thuyết Đối ($H_1$):** Có sự khác biệt có ý nghĩa thống kê về số lượng thuê xe trung bình mỗi giờ giữa hai loại ngày.
  $$H_1: \mu_{\text{workingday}} \neq \mu_{\text{non-workingday}} \quad (\text{hoặc } \mu_1 - \mu_0 \neq 0)$$
- **Mức ý nghĩa kiểm định:** $\alpha = 0.05$ (Kiểm định hai phía — Two-tailed test).

#### 2. Bước 2 & 3: Thống kê Mô tả và Kiểm tra Giả định Phân phối, Phương sai Nội nhóm
Để chọn đại lượng kiểm định thích hợp, trước hết ta tổng hợp các chỉ số thống kê mô tả thực nghiệm trên hai phân nhóm dữ liệu tại Bảng 3.2:

**Bảng 3.2. Thống kê mô tả số lượng thuê xe mỗi giờ (`cnt`) theo loại ngày**

| Chỉ số Thống kê | Ngày làm việc (`workingday = 1`) | Ngày nghỉ / Cuối tuần (`workingday = 0`) | Chênh lệch ($\Delta = \text{Nhóm 1} - \text{Nhóm 0}$) |
| :--- | :---: | :---: | :---: |
| **Cỡ mẫu quan sát ($N$)** | $11,865$ ($68.27\%$) | $5,514$ ($31.73\%$) | $N_{\text{total}} = 17,379$ |
| **Trung bình ($\overline{x}$, Mean)** | $193.21$ lượt/giờ | $181.41$ lượt/giờ | $+11.80$ lượt/giờ |
| **Trung vị ($\text{Med}$, Median)** | $151.00$ lượt/giờ | $119.00$ lượt/giờ | $+32.00$ lượt/giờ |
| **Độ lệch chuẩn ($s$, Std)** | $185.11$ | $172.85$ | $+12.26$ |
| **Phương sai ($s^2$, Variance)** | $34,265.71$ | $29,877.12$ | $+4,388.59$ |
| **Hệ số bất đối xứng ($\text{Skewness}$)** | $1.3529$ | $1.0574$ | Lệch phải mạnh ở cả 2 nhóm |
| **Hệ số nhọn ($\text{Kurtosis}$)** | $1.6378$ | $0.6587$ | Đuôi dài hơn phân phối chuẩn |

Việc kiểm tra hai giả định nền tảng (Tính chuẩn và Đồng nhất phương sai) được trực quan hóa toàn diện trên **Hình 3.1**:

![Hình 3.1. Kiểm tra giả định phân phối chuẩn và phương sai nội nhóm của cnt theo loại ngày](assets/fig_3_1_workingday_assumptions.png)

Từ kết quả trực quan hóa trên Hình 3.1 và kiểm định thống kê:
- **Kiểm tra tính chuẩn (Normality Check — Panel B & C):** Đồ thị Q-Q plot của cả hai phân nhóm đều bị uốn cong chữ S gãy khúc dữ dội khỏi đường thẳng tham chiếu màu đỏ ($y = x$), đặc biệt kéo dài ở vùng phân vị cao. Hệ số Skewness đều $> 1.0$ ($\text{Skew}_1 = 1.35$, $\text{Skew}_0 = 1.06$), khẳng định biến `cnt` **vi phạm nghiêm trọng giả định phân phối chuẩn trong từng phân nhóm**.
- **Kiểm tra tính đồng nhất phương sai (Homoscedasticity Check — Panel D):** Thực thi **Levene's Test (*Kanji Test 31*, trung vị)**:
  $$F_{\text{Levene}} = 2.7390, \quad p = 0.0979 > 0.05$$
  Do $p > 0.05$, ta chưa đủ bằng chứng bác bỏ giả định phương sai đồng nhất. Tuy nhiên, do hai nhóm có cỡ mẫu chênh lệch lớn ($N_1 / N_0 \approx 2.15$) kết hợp với việc vi phạm nặng tính chuẩn, Student's $t$-test cổ điển tiềm ẩn rủi ro sai lệch. Phép thử **Welch's $t$-test (*Kanji Test 9*)** được lựa chọn làm phép kiểm định tham số chủ đạo nhờ đặc tính vững (robustness), song song với các phép thử phi tham số **Mann-Whitney $U$ (*Kanji Test 48*)** và **Kolmogorov-Smirnov (*Kanji Test 49*)**.

#### 3. Bước 4: Thực thi Tính toán Thống kê và $p$-value
Kết quả thực thi các phép kiểm định thống kê cho RQ1 được tổng hợp chi tiết trong Bảng 3.3:

**Bảng 3.3. Bảng tổng hợp kết quả các phép kiểm định thống kê cho RQ1**

| Phép kiểm định | Mã sách Kanji (2006) | Thống kê Kiểm định | Bậc tự do / Tham số | $p$-value Thực nghiệm | Ngưỡng $\alpha$ | Kết luận Thống kê |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Levene's Test** | Test 31 (tr. 71) | $F = 2.7390$ | $k = 2$ | $0.0979$ | $0.05$ | Chưa đủ bằng chứng bác bỏ $H_0$ phương sai bằng nhau |
| **Welch's $t$-test** | Test 9 (tr. 33) | $t^* = 4.0951$ | $\nu = 11,444.68$ | $4.25 \times 10^{-5}$ | $0.05$ | **Bác bỏ $H_0$** ($p < 0.001^{***}$) |
| **Mann-Whitney $U$** | Test 48 (tr. 96) | $U = 33,565,313.0$ | $r_{\text{rb}} = -0.0261$ | $0.0056$ | $0.05$ | **Bác bỏ $H_0$** ($p = 0.0056^{**}$) |
| **Two-sample KS-test** | Test 49 (tr. 97) | $D = 0.0748$ | $N_1, N_0$ | $9.35 \times 10^{-19}$ | $0.05$ | **Bác bỏ $H_0$** ($p < 0.001^{***}$) |
| **Cohen's $d$ (Effect Size)** | Cohen (1988) | $d = 0.0651$ | $s_p = 181.33$ | — | $|d| \ge 0.20$ | **Hiệu ứng không đáng kể (Negligible Effect)** |

*Chi tiết các đại lượng thống kê:*
- **Welch's $t$-test (Kanji Test 9):**
  - Sai số chuẩn chênh lệch trung bình:
    $$\text{SE} = \sqrt{\frac{s_1^2}{n_1} + \frac{s_0^2}{n_0}} = \sqrt{\frac{34,265.71}{11,865} + \frac{29,877.12}{5,514}} \approx 2.8814$$
  - Thống kê kiểm định:
    $$t^* = \frac{193.21 - 181.41}{2.8814} = 4.0951$$
  - Bậc tự do hiệu chỉnh Welch-Satterthwaite: $\nu \approx 11,444.68$.
  - Khoảng tin cậy $95\%$ của chênh lệch trung bình:
    $$\text{CI}_{95\%} = (\overline{x}_1 - \overline{x}_0) \pm t_{0.975, \nu} \times \text{SE} = 11.80 \pm 1.960 \times 2.8814 = [6.15, 17.45] \text{ lượt/giờ}$$
  - Do $p = 4.25 \times 10^{-5} < 0.001$, trên phương diện ý nghĩa thống kê danh nghĩa, ta có đủ bằng chứng để bác bỏ giả thuyết $H_0$.
- **Mann-Whitney $U$ test (Kanji Test 48):**
  - Tổng thứ hạng kiểm tra trung vị cho giá trị $U = 33,565,313.0$, trả về $p = 0.0056 < 0.01$, củng cố kết luận bác bỏ $H_0$ trên thang đo thứ hạng.
  - Hệ số tương quan Rank-biserial: $r_{\text{rb}} = 1 - \frac{2U}{n_1 n_0} = -0.0261$.
- **Kolmogorov-Smirnov test (Kanji Test 49):**
  - Khoảng cách thẳng đứng cực đại giữa hai hàm phân phối tích lũy là $D = 0.0748$, $p = 9.35 \times 10^{-19} < 0.001$, chứng minh hình thái phân phối xác suất tổng thể giữa hai loại ngày có sự phân hóa nhất định.

#### 4. Bước 5: Đánh giá Kích thước Hiệu ứng & Bóc tách Nghịch lý Thực tiễn qua Nhịp giờ

##### a. Lượng hóa Kích thước Hiệu ứng (Effect Size)
Mặc dù cả ba phép thử danh nghĩa đều trả về $p < 0.01$ (đạt ý nghĩa thống kê), việc đánh giá kích thước hiệu ứng chuẩn hóa mang lại một bức tranh hoàn toàn khác:
- Độ lệch chuẩn gộp: $s_p = \sqrt{\frac{(11,865-1)(185.11)^2 + (5,514-1)(172.85)^2}{11,865 + 5,514 - 2}} \approx 181.33$.
- Kích thước hiệu ứng Cohen's $d$:
  $$d = \frac{\overline{x}_1 - \overline{x}_0}{s_p} = \frac{11.80}{181.33} \approx 0.0651$$
Theo quy chuẩn thẩm định của Cohen (1988), một hiệu ứng chỉ được xem là có ý nghĩa thực tiễn ở mức nhỏ (Small) khi $|d| \ge 0.20$, trung bình (Medium) khi $|d| \ge 0.50$, và lớn (Large) khi $|d| \ge 0.80$. Giá trị $d = 0.0651$ rơi sâu vào vùng **"Không đáng kể" (Negligible effect / Trivial)**. Tương tự, hệ số Rank-biserial $|r_{\text{rb}}| = 0.0261 \ll 0.10$. 

Điều này khẳng định: **Việc bác bỏ $H_0$ ở cấp độ danh nghĩa chủ yếu là hệ quả của cỡ mẫu cực lớn ($N = 17,379$), khiến phép thử phát hiện cả những sai biệt vô cùng nhỏ nhặt ($11.80$ lượt/giờ trên nền độ lệch chuẩn $> 180$) vốn không mang lại ý nghĩa kinh tế thực chất.**

##### b. Bóc tách Nghịch lý Triệt tiêu qua Phân tầng Nhịp giờ (Stratified Hourly Pattern)
Để trả lời trọn vẹn câu hỏi tại sao chênh lệch trung bình 24 giờ lại nhỏ ($11.80$ lượt/giờ), nghiên cứu tái sử dụng và dẫn chiếu trực tiếp **Hình 1.6** từ Báo cáo Khám phá Dữ liệu (TV1):

![Hình 1.6. So sánh nhu cầu thuê xe theo giờ giữa ngày làm việc và ngày nghỉ (Trích xuất từ Chương 1 - TV1)](../EDA/assets/hinh1.6.png)

Phân tích Hình 1.6 làm sáng tỏ hiện tượng **Triệt tiêu lẫn nhau (Cancellation Effect)** khi tính trung bình gộp 24 giờ:
1. **Cấu trúc nhu cầu Ngày làm việc (`workingday = 1`):** Phản ánh đặc trưng sinh hoạt của nhóm hành khách đi làm định kỳ (Commuters). Biểu đồ xuất hiện **hai đỉnh nhọn cực đại (Bimodal distribution)** trùng khớp hoàn toàn với khung giờ cao điểm công sở:
   - Đỉnh sáng: Lúc $8\text{h}$ sáng ($\overline{x} \approx 360 \text{ lượt/giờ}$).
   - Đỉnh chiều: Lúc $17\text{h} - 18\text{h}$ chiều ($\overline{x} \approx 430 - 460 \text{ lượt/giờ}$).
   - Ngược lại, vào giữa trưa ($10\text{h} - 15\text{h}$), nhu cầu sụt giảm xuống mức trung bình thấp ($\approx 180 - 200 \text{ lượt/giờ}$).
2. **Cấu trúc nhu cầu Ngày nghỉ (`workingday = 0`):** Phản ánh hành vi giải trí, du lịch và dạo phố (Leisure / Casual users). Biểu đồ có dạng **hình chuông đơn thoải (Unimodal distribution)**:
   - Hoàn toàn vắng bóng đỉnh sáng lúc $8\text{h}$ ($\overline{x} < 100 \text{ lượt/giờ}$).
   - Tăng dần đều từ $10\text{h}$ sáng và đạt đỉnh thoải duy nhất vào buổi trưa và đầu giờ chiều ($12\text{h} - 15\text{h}$, đạt $\approx 370 - 380 \text{ lượt/giờ}$).
3. **Cơ chế triệt tiêu:** Khoảng thặng dư khổng lồ của ngày nghỉ vào buổi trưa ($+180 \text{ lượt/giờ}$) đã bù trừ trực tiếp cho khoảng thiếu hụt vào hai khung giờ cao điểm sáng và chiều của ngày làm việc. Khi tích phân tổng lượt thuê trên toàn bộ chu kỳ 24 giờ, tổng diện tích dưới đường cong của hai loại ngày là **xấp xỉ tương đương nhau** ($\approx 4,637$ lượt/ngày làm việc so với $\approx 4,354$ lượt/ngày nghỉ).

##### c. Kết luận và Hàm ý Nghiệp vụ cho Daily Fleet Scheduling
- **Kết luận Thống kê:** Mặc dù kiểm định danh nghĩa bác bỏ $H_0$ do cỡ mẫu lớn, kích thước hiệu ứng $d = 0.0651$ chứng minh tổng nhu cầu trung bình 24 giờ giữa ngày làm việc và ngày nghỉ là tương đương trên thực tế.
- **Hàm ý Vận hành Đội xe:**
  - *Tổng quy mô phương tiện (Fleet Size):* Nhà vận hành **không cần thiết phải cắt giảm hay tăng thêm tổng số lượng xe đạp hoạt động trên toàn thành phố** giữa ngày làm việc và ngày nghỉ, vì tổng nhu cầu trong ngày không chênh lệch đáng kể.
  - *Biểu đồ Điều phối theo Giờ (Dynamic Hourly Rebalancing):* Bắt buộc phải áp dụng **hai chiến lược điều phối trạm đối lập nhau**:
    + Vào ngày làm việc: Tập trung xe tại các trạm đầu mối giao thông công cộng, trạm tàu điện ngầm (Metro) và khu dân cư trước $7\text{h}30$ sáng; tăng cường rút bớt xe giải phóng trạm tại khu trung tâm tài chính và công sở trước $16\text{h}30$ chiều.
    + Vào ngày nghỉ: Chuyển dịch trọng tâm phân bổ xe ra các tuyến đường ven sông, công viên, khu di tích lịch sử và trung tâm thương mại từ $10\text{h}$ sáng đến $16\text{h}$ chiều.

---

### 3.2.2. Nghiên cứu RQ2: So sánh 4 Nhóm Độc lập — Sự Khác biệt Nhu cầu Giữa 4 Mùa trong Năm (`season`)

#### 1. Bước 1: Phát biểu Cặp Giả thuyết Thống kê Đa nhóm
Nhằm giải quyết bài toán bảo dưỡng đại tu và tái cân bằng trạm theo mùa (Seasonal Rebalancing & Fleet Maintenance), nghiên cứu kiểm định sự khác biệt về số lượng thuê xe trung bình mỗi giờ giữa 4 mùa trong năm (Mùa xuân: `season = 1`, Mùa hè: `season = 2`, Mùa thu: `season = 3`, Mùa đông: `season = 4`):
- **Giả thuyết Không ($H_0$):** Lượng thuê xe trung bình mỗi giờ là như nhau ở cả 4 mùa trong năm.
  $$H_0: \mu_{\text{Spring}} = \mu_{\text{Summer}} = \mu_{\text{Fall}} = \mu_{\text{Winter}} \quad (\text{hoặc } \mu_1 = \mu_2 = \mu_3 = \mu_4)$$
- **Giả thuyết Đối ($H_1$):** Tồn tại ít nhất một cặp mùa có lượng thuê xe trung bình khác nhau.
  $$H_1: \exists (i, j) \text{ sao cho } \mu_i \neq \mu_j \quad (1 \le i < j \le 4)$$
- **Mức ý nghĩa kiểm định:** $\alpha = 0.05$.

#### 2. Bước 2 & 3: Thống kê Mô tả và Kiểm tra Giả định Phương sai Giữa 4 Mùa
Số liệu thống kê mô tả chi tiết của 4 mùa được tổng hợp tại Bảng 3.4:

**Bảng 3.4. Thống kê mô tả số lượng thuê xe mỗi giờ (`cnt`) phân theo 4 mùa**

| Mùa vụ (`season`) | Tên Mùa | Cỡ mẫu ($N$) | Tỷ lệ | Trung bình ($\overline{x}$) | Trung vị ($\text{Med}$) | Độ lệch chuẩn ($s$) | Phương sai ($s^2$) | Hệ số lệch ($\text{Skew}$) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$1$** | Mùa xuân (Spring) | $4,242$ | $24.41\%$ | $111.11$ | $76.00$ | $119.22$ | $14,213.62$ | $1.9119$ |
| **$2$** | Mùa hè (Summer) | $4,409$ | $25.37\%$ | $208.34$ | $165.00$ | $188.36$ | $35,478.43$ | $1.0401$ |
| **$3$** | Mùa thu (Fall) | $4,496$ | $25.87\%$ | $236.02$ | $199.00$ | $197.71$ | $39,088.08$ | $0.9865$ |
| **$4$** | Mùa đông (Winter) | $4,232$ | $24.35\%$ | $198.87$ | $155.50$ | $182.97$ | $33,476.99$ | $1.2422$ |
| **Toàn bộ** | **Tổng thể** | $17,379$ | $100\%$ | $189.46$ | $142.00$ | $181.39$ | $32,901.87$ | $1.2774$ |

Để kiểm tra trực quan hình thái phân tán và phương sai giữa các mùa, nghiên cứu tái sử dụng **Hình 1.7** từ Chương 1:

![Hình 1.7. Phân phối cnt theo các mùa trong năm và điều kiện thời tiết (Trích xuất từ Chương 1 - TV1)](../EDA/assets/hinh1.7.png)

- **Kiểm định tính đồng nhất phương sai đa nhóm (Levene Test — *Kanji Test 31*):**
  Thực hiện kiểm định Levene đa nhóm dựa trên trung vị cho 4 mùa:
  $$F_{\text{Levene}} = 324.50, \quad p = 5.03 \times 10^{-205} \ll 0.001$$
  Giá trị $p$-value cực nhỏ bác bỏ dứt khoát giả định phương sai đồng nhất. Độ lệch chuẩn giữa các nhóm dao động từ $119.22$ (Mùa xuân) lên tới $197.71$ (Mùa thu) — phương sai mùa thu cao gấp gần $2.75$ lần mùa xuân.
- **Lựa chọn phương pháp:** Hiện tượng phương sai dị biệt cực đoan (Severe Heteroscedasticity) làm vô hiệu hóa One-way ANOVA truyền thống (*Kanji Test 22*). Nghiên cứu xác lập **Welch's ANOVA** làm kiểm định tham số chủ đạo, phối hợp đối chứng phi tham số **Kruskal-Wallis $H$-test (*Kanji Test 51/54*)** và thủ tục so sánh cặp **Games-Howell Post-hoc (*Kanji Test 28*)**.

#### 3. Bước 4: Thực thi Kiểm định Tổng thể Đa nhóm (Omnibus Tests) & Kích thước Hiệu ứng
Kết quả các phép kiểm định tổng quát đa nhóm được trình bày tại Bảng 3.5:

**Bảng 3.5. Kết quả các phép kiểm định tổng quát (Omnibus Tests) cho RQ2**

| Phép kiểm định Tổng quát | Mã sách Kanji (2006) | Thống kê Kiểm định | Bậc tự do ($\nu$) | $p$-value Thực nghiệm | Kích thước Hiệu ứng | Kết luận Thống kê |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Levene's Test 4 mùa** | Test 31 (tr. 71) | $F = 324.50$ | $k = 4$ | $5.03 \times 10^{-205}$ | — | **Bác bỏ giả định đồng nhất phương sai** |
| **Welch's ANOVA** | Kanji Test 22 adj | $F_{\text{Welch}} = 606.73$ | $\nu_1 = 3, \nu_2 = 9,462.11$ | $< 10^{-300}$ | $\eta^2 = 0.0660$ | **Bác bỏ $H_0$** ($p < 0.001^{***}$) |
| **One-way ANOVA cổ điển**| Test 22 (tr. 55) | $F = 409.18$ | $\nu_1 = 3, \nu_2 = 17,375$ | $7.40 \times 10^{-257}$ | $\omega^2 = 0.0658$ | **Bác bỏ $H_0$** ($p < 0.001^{***}$) |
| **Kruskal-Wallis $H$-test**| Test 51/54 (tr. 99) | $H = 1,190.27$ | $\nu = 3$ | $9.47 \times 10^{-258}$ | $\epsilon^2 = 0.0683$ | **Bác bỏ $H_0$** ($p < 0.001^{***}$) |

*Lượng hóa Kích thước Hiệu ứng Toàn cục:*
- Tổng bình phương giữa các nhóm: $\text{SS}_{\text{between}} = \sum_{j=1}^4 n_j (\overline{x}_j - \overline{x})^2 = 38,799,017$.
- Tổng bình phương toàn phần: $\text{SS}_{\text{total}} = 588,095,496$.
- Tỷ số Eta-squared:
  $$\eta^2 = \frac{\text{SS}_{\text{between}}}{\text{SS}_{\text{total}}} = \frac{38,799,017}{588,095,496} \approx 0.0660 \quad (6.60\%)$$
- Hệ số phi tham số Epsilon-squared:
  $$\epsilon^2 = \frac{H - k + 1}{N - k} = \frac{1,190.27 - 4 + 1}{17,379 - 4} \approx 0.0683 \quad (6.83\%)$$
Theo phân loại của Cohen (1988), $\eta^2 \ge 0.06$ đại diện cho một **Hiệu ứng ở mức độ Trung bình (Medium Effect Size)**. Yếu tố mùa vụ giải thích trực tiếp khoảng $6.6\%$ tổng độ biến thiên của nhu cầu thuê xe toàn hệ thống. Đây là một tác động thực chất rất lớn, vượt trội hoàn toàn so với biến loại ngày ở RQ1.

#### 4. Bước 5: Phân tích Hậu định Từng Cặp Mùa (Games-Howell Post-hoc Test) & Cơ chế Khí hậu

##### a. Kết quả Kiểm định Hậu định Games-Howell (*Kanji Test 28*)
Do kiểm định tổng quát bác bỏ $H_0$, bước tiếp theo là xác định chính xác những cặp mùa nào có sự sai biệt thực chất. Vì phương sai không đồng nhất, thủ tục **Games-Howell (*Kanji Test 28*)** được áp dụng cho toàn bộ $m = C_4^2 = 6$ cặp so sánh, kiểm soát nghiêm ngặt sai lầm loại 1 toàn họ (FWER) ở mức $0.05$. 

Kết quả chi tiết được tổng hợp tại Bảng 3.6 và trực quan hóa trên **Hình 3.2**:

**Bảng 3.6. Kết quả kiểm định so sánh hậu định Games-Howell (Kanji Test 28) cho 6 cặp mùa**

| STT | Cặp So sánh Mùa vụ | Chênh lệch ($\Delta$, lượt/h) | Sai số chuẩn ($\text{SE}$) | Bậc tự do ($\nu$) | Khoảng tin cậy $95\%$ CI | $p$-value điều chỉnh | Mức ý nghĩa |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | **Mùa xuân vs Mùa hè** | $-97.23$ | $3.38$ | $7,508.8$ | $[-105.90, -88.55]$ | $< 0.0001$ | $p < 0.001^{***}$ |
| 2 | **Mùa xuân vs Mùa thu** | $-124.90$ | $3.47$ | $7,587.2$ | $[-133.82, -115.98]$ | $< 0.0001$ | $p < 0.001^{***}$ |
| 3 | **Mùa xuân vs Mùa đông** | $-87.75$ | $3.36$ | $7,249.4$ | $[-96.38, -79.13]$ | $< 0.0001$ | $p < 0.001^{***}$ |
| 4 | **Mùa hè vs Mùa thu** | $-27.67$ | $4.09$ | $8,898.3$ | $[-38.19, -17.16]$ | $9.10 \times 10^{-11}$| $p < 0.001^{***}$ |
| 5 | **Mùa hè vs Mùa đông** | $\mathbf{+9.48}$ | $\mathbf{3.99}$ | $\mathbf{8,609.9}$ | $\mathbf{[-0.79, +19.74]}$ | $\mathbf{0.0826}$ | **Không có ý nghĩa (ns)** |
| 6 | **Mùa thu vs Mùa đông** | $+37.15$ | $4.07$ | $8,674.8$ | $[+26.68, +47.62]$ | $< 0.0001$ | $p < 0.001^{***}$ |

*Ghi chú:* Kiểm định phi tham số Dunn-Bonferroni đối chứng cho cặp Mùa hè vs Mùa đông cũng trả về $p_{\text{adj}} = 0.4339 > 0.05$ (đồng thuận kết luận).

![Hình 3.2. Khoảng tin cậy 95% chênh lệch trung bình từng cặp mùa từ kiểm định Games-Howell (Kanji Test 28)](assets/fig_3_2_season_posthoc_forest.png)

##### b. Phát hiện Thực nghiệm Phản trực giác: Sự Tương đồng Nhu cầu Giữa Mùa hè và Mùa đông
Quan sát Forest plot trên Hình 3.2 làm nổi bật hai quy luật cốt lõi:
1. **5/6 cặp mùa có sự khác biệt cực kỳ ý nghĩa thống kê ($p < 0.001^{***}$):**
   - Mùa xuân có nhu cầu sụt giảm sâu sắc nhất so với tất cả các mùa còn lại (thấp hơn Mùa hè $97.23$ lượt/h, thấp hơn Mùa thu $124.90$ lượt/h, và thấp hơn Mùa đông $87.75$ lượt/h).
   - Mùa thu là mùa đạt đỉnh cao nhất trong năm, vượt trội hơn Mùa hè $+27.67$ lượt/h và vượt hơn Mùa đông $+37.15$ lượt/h.
2. **Ngoại lệ Phản trực giác (Counter-intuitive Finding): Cặp Mùa hè vs Mùa đông:**
   - Chênh lệch trung bình giữa Mùa hè ($\overline{x} = 208.34$) và Mùa đông ($\overline{x} = 198.87$) chỉ vỏn vẹn là $\Delta = +9.48 \text{ lượt/giờ}$.
   - Khoảng tin cậy $95\%$ của Games-Howell là $[-0.79, +19.74]$ **bao trùm giá trị 0**.
   - Giá trị $p$-value hiệu chỉnh là $p = 0.0826 > 0.05$.
   - **Kết luận:** **Chưa đủ bằng chứng thống kê ở mức ý nghĩa $\alpha = 0.05$ để khẳng định có sự khác biệt về nhu cầu thuê xe giữa Mùa hè và Mùa đông.**

##### c. Thảo luận Cơ chế Khí hậu Mùa vụ (Dẫn chiếu Hình 2.7 từ Chương 2 - TV2)
Để lý giải về mặt khoa học tại sao Mùa hè (thời tiết ấm áp) lại có nhu cầu thuê xe tương đương Mùa đông (thời tiết lạnh giá), nghiên cứu đối chiếu với phân tích phân bố nhiệt độ mùa vụ của TV2 (**Hình 2.7**):

![Hình 2.7. Phân bố nhiệt độ temp theo 4 mùa (Trích xuất từ Chương 2 - TV2)](../Distribution/assets/fig_2_7_temp_by_season.png)

Cơ chế vi khí hậu tại thủ đô Washington D.C. giải thích trọn vẹn hiện tượng này:
- **Tác động ức chế của Khí hậu Mùa hè (Extreme Heat & Humidity):** Washington D.C. vào mùa hè có đặc trưng nhiệt độ rất cao (giá trị chuẩn hóa `temp` thường xuyên $> 0.75$, tương đương $> 32^\circ\text{C} - 38^\circ\text{C}$) kết hợp độ ẩm cao (`hum` cao). Điều kiện nắng gắt và chỉ số khó chịu nhiệt độ (Heat Index) cao làm ức chế mạnh mẽ hoạt động đạp xe ngoài trời của người dân vào ban ngày.
- **Tính Bền vững của Hành vi Di chuyển Mùa đông (Commuter Resilience):** Mặc dù nhiệt độ mùa đông tại D.C. xuống thấp (`temp` $\approx 0.20 - 0.35$, khoảng $5^\circ\text{C} - 12^\circ\text{C}$), mùa đông tại khu vực này tương đối khô ráo. Lực lượng khách hàng thường xuyên (Registered commuters) vẫn duy trì thói quen đạp xe đi làm hàng ngày để tránh ùn tắc giao thông đô thị và giữ ấm qua vận động thể chất.
- **Sự sụt giảm của Mùa xuân:** Mùa xuân tại D.C. (tháng 1 đến tháng 3 trong dataset) thực chất là giai đoạn tuyết tan, mưa phùn dầm dề và thời tiết chuyển mùa ẩm ướt khó lường, kết hợp với các đợt rét muộn, khiến nhu cầu chạm đáy sâu nhất trong năm.

##### d. Kết luận và Hàm ý Nghiệp vụ cho Seasonal Maintenance & Fleet Rebalancing
- **Chiến lược Đại tu & Bảo dưỡng Định kỳ Đội xe (Fleet Overhaul):**
  - Mùa xuân là "cửa sổ vàng" để thu hồi xe về xưởng bảo dưỡng lớn. Do nhu cầu trung bình chỉ đạt $111.11$ lượt/h (giảm hơn $50\%$ so với mùa thu), việc rút bớt $20\% - 30\%$ lượng xe đạp về xưởng đại tu hệ thống phanh, xích líp và thay lốp sẽ **không gây ra tình trạng thiếu hụt xe tại các trạm hay ảnh hưởng đến trải nghiệm khách hàng**.
- **Chiến lược Tái cân bằng Trạm Đỉnh cao (Peak Rebalancing):**
  - Mùa thu là giai đoạn bùng nổ nhu cầu lớn nhất ($236.02$ lượt/h). Doanh nghiệp cần huy động $100\%$ lượng phương tiện ra thị trường, đồng thời tăng tần suất các chuyến xe tải tái cân bằng trạm (Rebalancing vans) tại các khu vực trường đại học và cơ quan chính phủ để ngăn ngừa tình trạng trạm rỗng (empty station) hoặc trạm đầy nghẽn (full station).
- **Chiến lược Đồng nhất Mùa hè và Mùa đông:**
  - Nhà quản trị **không cần phải thiết lập hai định mức cung ứng xe khác nhau giữa Mùa hè và Mùa đông**. Quy mô xe đạp và nhân sự phục vụ có thể giữ nguyên ở mức cơ bản tương đương nhau ($\approx 200$ lượt/h) cho cả hai mùa này.

---

## Tài liệu Tham khảo

1. **Cohen, J. (1988).** *Statistical Power Analysis for the Behavioral Sciences* (2nd ed.). Lawrence Erlbaum Associates.
2. **Dunn, O. J. (1964).** Multiple comparisons using rank sums. *Technometrics*, 6(3), 241–252.
3. **Fanaee-T, H., & Gama, J. (2014).** Event labeling combining ensemble detectors and background knowledge. *Progress in Artificial Intelligence*, 2(2–3), 113–127.
4. **Games, P. A., & Howell, J. F. (1976).** Pairwise multiple comparison procedures with unequal N's and/or variances: a Monte Carlo study. *Journal of Educational Statistics*, 1(2), 113–125.
5. **Kanji, G. K. (2006).** *100 Statistical Tests* (3rd ed.). SAGE Publications.
6. **Kruskal, W. H., & Wallis, W. A. (1952).** Use of ranks in one-criterion variance analysis. *Journal of the American Statistical Association*, 47(260), 583–621.
7. **Mann, H. B., & Whitney, D. R. (1947).** On a test of whether one of two random variables is stochastically larger than the other. *Annals of Mathematical Statistics*, 18(1), 50–60.
8. **Neave, H. R. (1976).** *Statistical Tables for Students*. Allen & Unwin.
9. **Satterthwaite, F. E. (1946).** An approximate distribution of estimates of variance components. *Biometrics Bulletin*, 2(6), 110–114.
10. **Welch, B. L. (1947).** The generalization of 'Student's' problem when several different population variances are involved. *Biometrika*, 34(1/2), 28–35.
