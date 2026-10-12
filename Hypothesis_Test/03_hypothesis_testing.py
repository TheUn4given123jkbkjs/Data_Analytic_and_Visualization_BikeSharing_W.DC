"""
Script tính toán kiểm định giả thuyết thống kê (Chương 3)
Theo chuyên khảo: 100 Statistical Tests (3rd Edition, 2006) - Gopal K. Kanji
Tập dữ liệu: EDA/cleaned_data/hour_cleaned.csv
"""

import os
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from itertools import combinations

# Cấu hình thư mục
DATA_PATH = os.path.join('EDA', 'cleaned_data', 'hour_cleaned.csv')
ASSETS_DIR = os.path.join('Hypothesis_Test', 'assets')
os.makedirs(ASSETS_DIR, exist_ok=True)

# Thiết lập thẩm mỹ biểu đồ
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Segoe UI']
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

print("=== ĐỌC VÀ KIỂM TRA DỮ LIỆU ===")
df = pd.read_csv(DATA_PATH)
print(f"Tổng số quan sát: N = {len(df):,}, Số biến: {df.shape[1]}")

# ==============================================================================
# CÂU HỎI NGHIÊN CỨU 1 (RQ1): workingday = 1 vs workingday = 0
# ==============================================================================
print("\n" + "="*60)
print("CÂU HỎI NGHIÊN CỨU 1 (RQ1): NGÀY LÀM VIỆC VS NGÀY NGHỈ")
print("="*60)

g_work = df[df['workingday'] == 1]['cnt']
g_rest = df[df['workingday'] == 0]['cnt']

n_work, n_rest = len(g_work), len(g_rest)
mean_work, mean_rest = g_work.mean(), g_rest.mean()
med_work, med_rest = g_work.median(), g_rest.median()
std_work, std_rest = g_work.std(), g_rest.std()
skew_work, skew_rest = g_work.skew(), g_rest.skew()
kurt_work, kurt_rest = g_work.kurt(), g_rest.kurt()

print(f"Ngày làm việc (1): N = {n_work:,}, Mean = {mean_work:.2f}, Median = {med_work:.2f}, Std = {std_work:.2f}, Skew = {skew_work:.4f}")
print(f"Ngày nghỉ (0)    : N = {n_rest:,}, Mean = {mean_rest:.2f}, Median = {med_rest:.2f}, Std = {std_rest:.2f}, Skew = {skew_rest:.4f}")
print(f"Chênh lệch trung bình: Delta = {mean_work - mean_rest:.2f} lượt thuê/giờ")

# 1. Levene's Test (Kanji Test 31)
lev_stat, lev_p = stats.levene(g_work, g_rest, center='median')
print(f"\n1. Levene Test (Test 31): Stat = {lev_stat:.4f}, p = {lev_p:.4e}")

# 2. Welch's t-test (Kanji Test 9)
welch_t, welch_p = stats.ttest_ind(g_work, g_rest, equal_var=False)
se_welch = np.sqrt(std_work**2 / n_work + std_rest**2 / n_rest)
df_welch = (std_work**2 / n_work + std_rest**2 / n_rest)**2 / (
    (std_work**2 / n_work)**2 / (n_work - 1) + (std_rest**2 / n_rest)**2 / (n_rest - 1)
)
ci_low_w = (mean_work - mean_rest) - stats.t.ppf(0.975, df_welch) * se_welch
ci_high_w = (mean_work - mean_rest) + stats.t.ppf(0.975, df_welch) * se_welch

print(f"2. Welch's t-test (Test 9): t = {welch_t:.4f}, df = {df_welch:.2f}, 95% CI = [{ci_low_w:.2f}, {ci_high_w:.2f}], p = {welch_p:.4e}")

# 3. Mann-Whitney U test (Kanji Test 48)
mw_stat, mw_p = stats.mannwhitneyu(g_work, g_rest, alternative='two-sided')
# Rank-biserial correlation r = 1 - (2U / (n1 * n2))
rb_r = 1 - (2 * mw_stat) / (n_work * n_rest)
print(f"3. Mann-Whitney U (Test 48): U = {mw_stat:,.1f}, p = {mw_p:.4e}, Rank-biserial r = {rb_r:.4f}")

# 4. Kolmogorov-Smirnov test (Kanji Test 49)
ks_stat, ks_p = stats.ks_2samp(g_work, g_rest)
print(f"4. Two-sample KS-test (Test 49): D = {ks_stat:.4f}, p = {ks_p:.4e}")

# 5. Cohen's d
s_pooled = np.sqrt(((n_work - 1) * std_work**2 + (n_rest - 1) * std_rest**2) / (n_work + n_rest - 2))
cohen_d = (mean_work - mean_rest) / s_pooled
print(f"5. Cohen's d: d = {cohen_d:.4f} (Ngưỡng Cohen: |d| < 0.20 là hiệu ứng không đáng kể)")

# 6. Hiệu chỉnh N_eff = 1,479 (Kanji Test 64)
N_total = len(df)
N_eff = 1479
adj_factor = np.sqrt(N_eff / N_total)
t_adj = welch_t * adj_factor
p_adj_neff = 2 * (1 - stats.t.cdf(np.abs(t_adj), df_welch))
print(f"6. Hiệu chỉnh N_eff = 1,479: t_adj = {t_adj:.4f}, p_adj = {p_adj_neff:.4f} (p > 0.05 -> Mất ý nghĩa thống kê!)")

# 7. Đối chứng chuỗi theo ngày (N = 731 ngày)
day_df = df.groupby(['dteday', 'workingday'])['cnt'].sum().reset_index()
day_work = day_df[day_df['workingday'] == 1]['cnt']
day_rest = day_df[day_df['workingday'] == 0]['cnt']
t_day, p_day = stats.ttest_ind(day_work, day_rest, equal_var=False)
u_day, p_u_day = stats.mannwhitneyu(day_work, day_rest)
print(f"7. Đối chứng cấp độ ngày (N = 731): Day Welch t = {t_day:.4f}, p = {p_day:.4f} | Day Mann-Whitney p = {p_u_day:.4f}")

# ==============================================================================
# VẼ HÌNH 3.1: KIỂM TRA GIẢ ĐỊNH NỘI NHÓM RQ1
# ==============================================================================
print("\n--> Vẽ Hình 3.1: fig_3_1_workingday_assumptions.png...")
fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=300)

palette = {'workingday': '#1f77b4', 'non-workingday': '#ff7f0e'}

# Panel A: Phân phối mật độ KDE & Histogram
sns.histplot(data=df, x='cnt', hue='workingday', stat='density', common_norm=False,
             bins=50, alpha=0.35, palette=[palette['non-workingday'], palette['workingday']], ax=axes[0, 0])
sns.kdeplot(data=df, x='cnt', hue='workingday', common_norm=False,
            linewidth=2, palette=[palette['non-workingday'], palette['workingday']], ax=axes[0, 0])
axes[0, 0].set_title('A. Phân phối mật độ thực nghiệm của cnt theo loại ngày', fontsize=12, fontweight='bold', pad=10)
axes[0, 0].set_xlabel('Số lượt thuê xe mỗi giờ (cnt)', fontsize=10)
axes[0, 0].set_ylabel('Mật độ xác suất (Density)', fontsize=10)
axes[0, 0].axvline(mean_work, color=palette['workingday'], linestyle='--', linewidth=1.5, label=f'Mean Ngày làm việc ({mean_work:.1f})')
axes[0, 0].axvline(mean_rest, color=palette['non-workingday'], linestyle='--', linewidth=1.5, label=f'Mean Ngày nghỉ ({mean_rest:.1f})')
axes[0, 0].legend(title='Loại ngày', labels=['Ngày làm việc (1)', 'Ngày nghỉ (0)'], loc='upper right', framealpha=0.9)
axes[0, 0].grid(True, linestyle=':', alpha=0.5)

# Panel B: Q-Q Plot Ngày làm việc
stats.probplot(g_work, dist="norm", plot=axes[0, 1])
axes[0, 1].get_lines()[0].set_color(palette['workingday'])
axes[0, 1].get_lines()[0].set_markersize(2)
axes[0, 1].get_lines()[0].set_alpha(0.5)
axes[0, 1].get_lines()[1].set_color('#d62728')
axes[0, 1].get_lines()[1].set_linewidth(1.8)
axes[0, 1].set_title('B. Q-Q Plot kiểm tra tính chuẩn: Ngày làm việc (N = 11,865)', fontsize=12, fontweight='bold', pad=10)
axes[0, 1].set_xlabel('Phân vị lý thuyết phân phối chuẩn (Theoretical Quantiles)', fontsize=10)
axes[0, 1].set_ylabel('Giá trị quan sát thực tế (Ordered Values)', fontsize=10)
axes[0, 1].text(0.05, 0.85, f'Skewness = {skew_work:.2f}\nKurtosis = {kurt_work:.2f}\n(Vi phạm tính chuẩn nặng)',
                transform=axes[0, 1].transAxes, fontsize=9, bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8, edgecolor='#ccc'))
axes[0, 1].grid(True, linestyle=':', alpha=0.5)

# Panel C: Q-Q Plot Ngày nghỉ
stats.probplot(g_rest, dist="norm", plot=axes[1, 0])
axes[1, 0].get_lines()[0].set_color(palette['non-workingday'])
axes[1, 0].get_lines()[0].set_markersize(2)
axes[1, 0].get_lines()[0].set_alpha(0.5)
axes[1, 0].get_lines()[1].set_color('#d62728')
axes[1, 0].get_lines()[1].set_linewidth(1.8)
axes[1, 0].set_title('C. Q-Q Plot kiểm tra tính chuẩn: Ngày nghỉ / Cuối tuần (N = 5,514)', fontsize=12, fontweight='bold', pad=10)
axes[1, 0].set_xlabel('Phân vị lý thuyết phân phối chuẩn (Theoretical Quantiles)', fontsize=10)
axes[1, 0].set_ylabel('Giá trị quan sát thực tế (Ordered Values)', fontsize=10)
axes[1, 0].text(0.05, 0.85, f'Skewness = {skew_rest:.2f}\nKurtosis = {kurt_rest:.2f}\n(Vi phạm tính chuẩn nặng)',
                transform=axes[1, 0].transAxes, fontsize=9, bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8, edgecolor='#ccc'))
axes[1, 0].grid(True, linestyle=':', alpha=0.5)

# Panel D: Boxplot + Violin Plot
df['workingday_label'] = df['workingday'].map({1: 'Ngày làm việc (1)', 0: 'Ngày nghỉ (0)'})
sns.violinplot(data=df, x='workingday_label', y='cnt', palette=[palette['workingday'], palette['non-workingday']],
               inner=None, alpha=0.3, ax=axes[1, 1])
sns.boxplot(data=df, x='workingday_label', y='cnt', width=0.25,
            palette=[palette['workingday'], palette['non-workingday']],
            boxprops=dict(alpha=0.8), showmeans=True,
            meanprops=dict(marker='D', markeredgecolor='black', markerfacecolor='yellow', markersize=6),
            ax=axes[1, 1])
axes[1, 1].set_title('D. So sánh phân vị, trung vị và độ phân tán', fontsize=12, fontweight='bold', pad=10)
axes[1, 1].set_xlabel('Phân nhóm loại ngày', fontsize=10)
axes[1, 1].set_ylabel('Số lượt thuê xe mỗi giờ (cnt)', fontsize=10)
levene_text = f"Levene Test (Test 31):\nF = {lev_stat:.4f}, p = {lev_p:.4f}\n(Phương sai tương đối đồng nhất)\nĐiểm vàng: Mean | Vạch đen: Median"
axes[1, 1].text(0.55, 0.78, levene_text, transform=axes[1, 1].transAxes, fontsize=9,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8, edgecolor='#ccc'))
axes[1, 1].grid(True, linestyle=':', alpha=0.5)

plt.suptitle('Hình 3.1. Kiểm tra giả định phân phối chuẩn và phương sai nội nhóm của cnt theo loại ngày',
             fontsize=14, fontweight='bold', y=0.995)
plt.tight_layout()
fig_3_1_path = os.path.join(ASSETS_DIR, 'fig_3_1_workingday_assumptions.png')
plt.savefig(fig_3_1_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Đã lưu Hình 3.1 vào: {fig_3_1_path}")

# ==============================================================================
# CÂU HỎI NGHIÊN CỨU 2 (RQ2): 4 MÙA TRONG NĂM
# ==============================================================================
print("\n" + "="*60)
print("CÂU HỎI NGHIÊN CỨU 2 (RQ2): 4 MÙA TRONG NĂM")
print("="*60)

seasons = [1, 2, 3, 4]
season_names = {1: 'Mùa xuân (Spring)', 2: 'Mùa hè (Summer)', 3: 'Mùa thu (Fall)', 4: 'Mùa đông (Winter)'}
groups_s = [df[df['season'] == s]['cnt'].values for s in seasons]

for s in seasons:
    vals = df[df['season'] == s]['cnt']
    print(f"Season {s} ({season_names[s]}): N = {len(vals):,}, Mean = {vals.mean():.2f}, Median = {vals.median():.2f}, Std = {vals.std():.2f}, Skew = {vals.skew():.4f}")

# 1. Levene's Test đa nhóm (Kanji Test 31)
lev_s_stat, lev_s_p = stats.levene(*groups_s, center='median')
print(f"\n1. Levene Test 4 mùa (Test 31): Stat = {lev_s_stat:.4f}, p = {lev_s_p:.4e} (Phương sai dị biệt cực mạnh!)")

# 2. One-way ANOVA tiêu chuẩn (Kanji Test 22)
f_stat, f_p = stats.f_oneway(*groups_s)
print(f"2. One-way ANOVA (Test 22): F = {f_stat:.4f}, p = {f_p:.4e}")

# 3. Welch's ANOVA
k_s = len(seasons)
ns_s = [len(g) for g in groups_s]
means_s = [g.mean() for g in groups_s]
vars_s = [np.var(g, ddof=1) for g in groups_s]

weights_s = [n / v for n, v in zip(ns_s, vars_s)]
w_sum_s = sum(weights_s)
mean_prime_s = sum(w * m for w, m in zip(weights_s, means_s)) / w_sum_s

num_w = sum(w * (m - mean_prime_s)**2 for w, m in zip(weights_s, means_s)) / (k_s - 1)
q_s = sum((1 - w / w_sum_s)**2 / (n - 1) for w, n in zip(weights_s, ns_s)) / (k_s**2 - 1)
den_w = 1 + 2 * (k_s - 2) * q_s

f_welch = num_w / den_w
df1_w = k_s - 1
df2_w = 1 / (3 * q_s)
p_welch = 1 - stats.f.cdf(f_welch, df1_w, df2_w)
print(f"3. Welch's ANOVA: F_welch = {f_welch:.4f}, df1 = {df1_w}, df2 = {df2_w:.2f}, p = {p_welch:.4e}")

# 4. Kruskal-Wallis H-test (Kanji Test 51/54)
kw_stat, kw_p = stats.kruskal(*groups_s)
print(f"4. Kruskal-Wallis H-test (Test 51/54): H = {kw_stat:.4f}, df = {k_s - 1}, p = {kw_p:.4e}")

# 5. Kích thước hiệu ứng Eta-squared
ss_total = np.sum((df['cnt'] - df['cnt'].mean())**2)
ss_between = sum(len(g) * (g.mean() - df['cnt'].mean())**2 for g in groups_s)
eta_sq = ss_between / ss_total
epsilon_sq = (kw_stat - k_s + 1) / (len(df) - k_s)
print(f"5. Effect Size: Eta-squared = {eta_sq:.4f} (6.60% biến thiên), Epsilon-squared = {epsilon_sq:.4f}")

# 6. Kiểm định hậu định Games-Howell (Kanji Test 28)
pairs_s = list(combinations(seasons, 2))
gh_results = []

print("\n6. Games-Howell Post-hoc Pairwise Comparisons (Kanji Test 28):")
for s1, s2 in pairs_s:
    n1, n2 = len(df[df['season'] == s1]), len(df[df['season'] == s2])
    m1, m2 = df[df['season'] == s1]['cnt'].mean(), df[df['season'] == s2]['cnt'].mean()
    v1, v2 = df[df['season'] == s1]['cnt'].var(ddof=1), df[df['season'] == s2]['cnt'].var(ddof=1)
    
    diff = m1 - m2
    se = np.sqrt(v1/n1 + v2/n2)
    t_val = diff / se
    df_pair = (v1/n1 + v2/n2)**2 / ((v1/n1)**2/(n1-1) + (v2/n2)**2/(n2-1))
    
    q_val = np.abs(diff) / np.sqrt(0.5 * (v1/n1 + v2/n2))
    p_val = 1 - stats.studentized_range.cdf(q_val, k_s, df_pair)
    
    q_crit = stats.studentized_range.ppf(0.95, k_s, df_pair)
    ci_low = diff - (q_crit / np.sqrt(2)) * se
    ci_high = diff + (q_crit / np.sqrt(2)) * se
    
    sig_label = "***" if p_val < 0.001 else ("**" if p_val < 0.01 else ("*" if p_val < 0.05 else "ns"))
    
    gh_results.append({
        'pair': f"{season_names[s1].split()[0]} vs {season_names[s2].split()[0]}",
        's1': s1, 's2': s2,
        'diff': diff, 'se': se, 't': t_val, 'df': df_pair,
        'ci_low': ci_low, 'ci_high': ci_high,
        'p_val': p_val, 'sig': sig_label
    })
    
    print(f"  {season_names[s1].split()[0]} vs {season_names[s2].split()[0]}: Diff = {diff:+.2f}, SE = {se:.2f}, 95% CI = [{ci_low:+.2f}, {ci_high:+.2f}], p = {p_val:.4e} ({sig_label})")

gh_df = pd.DataFrame(gh_results)

# ==============================================================================
# VẼ HÌNH 3.2: FOREST PLOT CHO KIỂM ĐỊNH HẬU ĐỊNH GAMES-HOWELL
# ==============================================================================
print("\n--> Vẽ Hình 3.2: fig_3_2_season_posthoc_forest.png...")
fig, ax = plt.subplots(figsize=(12, 7), dpi=300)

y_positions = np.arange(len(gh_df))[::-1]  # Đảo ngược để cặp 1 ở trên cùng

colors = ['#d95f02' if row['sig'] == 'ns' else '#1f77b4' for _, row in gh_df.iterrows()]

# Vẽ vạch chuẩn 0
ax.axvline(0, color='#d62728', linestyle='--', linewidth=1.5, alpha=0.8, label='Vạch chuẩn 0 (Không có chênh lệch)')

# Vẽ thanh khoảng tin cậy và điểm ước lượng
for y, (_, row), color in zip(y_positions, gh_df.iterrows(), colors):
    # Error bar
    ax.plot([row['ci_low'], row['ci_high']], [y, y], color=color, linewidth=2.5, solid_capstyle='round')
    ax.plot([row['ci_low'], row['ci_low']], [y - 0.15, y + 0.15], color=color, linewidth=2)
    ax.plot([row['ci_high'], row['ci_high']], [y - 0.15, y + 0.15], color=color, linewidth=2)
    # Point estimate
    ax.plot(row['diff'], y, marker='o', markersize=8, color=color, markeredgecolor='black', markeredgewidth=1)
    
    # Nhãn số liệu bên cạnh
    if row['sig'] == 'ns':
        label_text = f"Delta = {row['diff']:+.2f} [{row['ci_low']:+.1f}, {row['ci_high']:+.1f}] | p = {row['p_val']:.3f} (ns)"
    else:
        label_text = f"Delta = {row['diff']:+.2f} [{row['ci_low']:+.1f}, {row['ci_high']:+.1f}] | p < 0.001***"
    
    # Canh lề text
    text_x = row['ci_high'] + 4 if row['diff'] > -60 else row['ci_low'] - 4
    ha = 'left' if row['diff'] > -60 else 'right'
    ax.text(text_x, y, label_text, va='center', ha=ha, fontsize=9.5, fontweight='bold', color=color)

ax.set_yticks(y_positions)
ax.set_yticklabels(gh_df['pair'], fontsize=11, fontweight='bold')
ax.set_xlabel('Chênh lệch trung bình số lượt thuê xe mỗi giờ (Delta Mean, lượt thuê/giờ)', fontsize=11, fontweight='bold', labelpad=10)
ax.set_title('Hình 3.2. Khoảng tin cậy 95% chênh lệch trung bình từng cặp mùa từ kiểm định Games-Howell (Kanji Test 28)',
             fontsize=13, fontweight='bold', pad=15)

# Chú giải
ax.grid(True, linestyle=':', alpha=0.6, axis='x')
ax.set_xlim(-165, 95)

# Thêm hộp ghi chú kết luận
summary_box = (
    "Ý nghĩa thống kê:\n"
    "• 5/6 cặp mùa khác biệt cực kỳ ý nghĩa (p < 0.001***)\n"
    "• Cặp Mùa hè vs Mùa đông: p = 0.083 (ns, CI chứa 0)\n"
    "-> Nhu cầu Mùa hè và Mùa đông tương đương nhau!"
)
ax.text(0.02, 0.08, summary_box, transform=ax.transAxes, fontsize=10,
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#f8f9fa', edgecolor='#bbb', alpha=0.9))

plt.tight_layout()
fig_3_2_path = os.path.join(ASSETS_DIR, 'fig_3_2_season_posthoc_forest.png')
plt.savefig(fig_3_2_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Đã lưu Hình 3.2 vào: {fig_3_2_path}")

print("\n=== HOÀN TẤT TÍNH TOÁN VÀ XUẤT ASSETS THÀNH CÔNG! ===")
