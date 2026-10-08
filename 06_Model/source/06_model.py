"""
06_model.py — Phần 6: Xây dựng và đánh giá mô hình hồi quy tuyến tính đa biến (MLR)
Người viết: TV5
Mục đích: dự đoán tổng số lượt thuê xe theo giờ (cnt) từ thời tiết và thời gian,
          mã hóa giờ/tháng dạng sin-cos, chia train/valid/test theo thời gian.
Đầu vào: hour.csv (qua common.load_data)
Đầu ra: giao diện Streamlit; nút "Xuất hình và bảng" ghi 06_Model/figures/fig_6_*.png và 06_Model/tables/bang_6_*.csv
Chạy: streamlit run 06_model.py
"""
import itertools
import textwrap
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
import streamlit as st
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from common import SEED, load_data

HERE = Path(__file__).parent
C_TR, C_TE, C_PR, C_VA = "#1f77b4", "#ff7f0e", "#2ca02c", "#9467bd"
plt.rcParams.update({"font.size": 12, "axes.labelsize": 12, "xtick.labelsize": 11, "ytick.labelsize": 11, "legend.fontsize": 11,
                     "axes.grid": True, "grid.alpha": 0.3, "figure.dpi": 110})


# ---------------------------------------------------------------- định dạng (rules mục 2.1)
def f4(x):
    return f"{x:.4f}"


def f2(x):
    return f"{x:,.2f}"


def fp(p):
    return "p < 0.001" if p < 0.001 else f"p = {p:.4f}"


# ---------------------------------------------------------------- 6.1 Feature Engineering
def build_features(d, cfg, t0):
    """Trả về (X, groups). groups = [(nhóm, [cột], cách mã hóa, lý do)] để lập Bảng 6.2."""
    X, groups = pd.DataFrame(index=d.index), []

    def add(name, cols, how, why):
        groups.append((name, list(cols), how, why))

    for k in range(1, cfg["K"] + 1):
        ang = 2 * np.pi * k * d["hr"] / 24
        X[f"hr_sin{k}"], X[f"hr_cos{k}"] = np.sin(ang), np.cos(ang)
    add("Giờ (chu kỳ 24h)", [c for c in X.columns if c.startswith("hr_")],
        f"sin, cos của 2πk·hr/24, k = 1..{cfg['K']}",
        "Giờ 23 và giờ 0 liền kề nhau trên vòng tròn; nhiều hài (k) để biểu diễn hai đỉnh sáng/chiều")
    if cfg["inter"]:
        base = [c for c in X.columns if c.startswith("hr_")]
        for c in base:
            X[f"{c}×workingday"] = X[c] * d["workingday"]
        add("Giờ × ngày làm việc", [f"{c}×workingday" for c in base], "tích hài giờ với workingday",
            "Dáng đường cong theo giờ khác nhau giữa ngày làm việc và ngày nghỉ")
    X["workingday"] = d["workingday"]
    add("Ngày làm việc", ["workingday"], "nhị phân 0/1", "Phân biệt ngày làm việc và ngày nghỉ")
    if cfg["holiday"]:
        X["holiday"] = d["holiday"]
        add("Ngày lễ", ["holiday"], "nhị phân 0/1", "Ngày lễ có thể khác ngày thường")
    if cfg["month"] == "cyc":
        X["mnth_sin"], X["mnth_cos"] = np.sin(2 * np.pi * d["mnth"] / 12), np.cos(2 * np.pi * d["mnth"] / 12)
        add("Tháng (chu kỳ 12 tháng)", ["mnth_sin", "mnth_cos"], "sin, cos của 2π·mnth/12",
            "Mùa vụ là chu kỳ: tháng 12 liền kề tháng 1")
    elif cfg["month"] == "season":
        for s in (2, 3, 4):
            X[f"season_{s}"] = (d["season"] == s).astype(int)
        add("Mùa", ["season_2", "season_3", "season_4"], "one-hot, mùa 1 là nhóm cơ sở", "Mã hóa mùa dạng rời rạc")
    for col, name in [("temp", "Nhiệt độ"), ("atemp", "Nhiệt độ cảm nhận"), ("hum", "Độ ẩm"), ("windspeed", "Tốc độ gió")]:
        if cfg[col]:
            X[col] = d[col]
            add(name, [col], "giữ nguyên giá trị chuẩn hóa", "Biến thời tiết liên tục")
    if cfg["weather"]:
        X["weathersit_2"] = (d["weathersit"] == 2).astype(int)
        X["weathersit_3_4"] = (d["weathersit"] >= 3).astype(int)
        add("Tình trạng thời tiết", ["weathersit_2", "weathersit_3_4"],
            "one-hot, nhóm cơ sở là weathersit = 1; gộp mức 3 và 4",
            "weathersit = 4 chỉ có 3 quan sát nên gộp với mức 3")
    if cfg["trend"] == "yr":
        X["yr"] = d["yr"]
        add("Xu hướng", ["yr"], "nhị phân: 0 = 2011, 1 = 2012", "Nhu cầu năm 2012 cao hơn 2011; cần có 2012 trong tập huấn luyện")
    elif cfg["trend"] == "t":
        X["t_year"] = (d["dteday"] - t0).dt.days / 365
        add("Xu hướng", ["t_year"], "số năm kể từ 2011-01-01 (tuyến tính)", "Xu hướng tăng liên tục theo thời gian")
    return X, groups


def target(y, cfg):
    return np.log1p(y) if cfg["target"] == "log" else np.asarray(y, float)


def inverse(z, cfg):
    return np.clip(np.expm1(z) if cfg["target"] == "log" else z, 0, None)


def flag_outliers(tr):
    g = tr.groupby(["yr", "hr", "workingday"])["cnt"]
    q1, q3 = g.transform(lambda s: s.quantile(0.25)), g.transform(lambda s: s.quantile(0.75))
    iqr = q3 - q1
    return (tr["cnt"] < q1 - 1.5 * iqr) | (tr["cnt"] > q3 + 1.5 * iqr)


# ---------------------------------------------------------------- 6.3 Huấn luyện (OLS tự cài đặt)
def fit_ols(X, y):
    A = np.column_stack([np.ones(len(X)), X.to_numpy(float)])
    y = np.asarray(y, float)
    beta = np.linalg.lstsq(A, y, rcond=None)[0]
    resid = y - A @ beta
    n, p = A.shape
    sigma2 = resid @ resid / (n - p)
    se = np.sqrt(np.diag(sigma2 * np.linalg.pinv(A.T @ A)))
    t = beta / se
    tc = stats.t.ppf(0.975, n - p)
    r2 = 1 - resid @ resid / ((y - y.mean()) ** 2).sum()
    return dict(cols=list(X.columns), beta=beta, se=se, t=t, p=2 * stats.t.sf(np.abs(t), n - p),
                lo=beta - tc * se, hi=beta + tc * se, resid=resid, fitted=y - resid, n=n, k=p - 1,
                r2=r2, adj=1 - (1 - r2) * (n - 1) / (n - p))


def predict(m, X):
    return np.column_stack([np.ones(len(X)), X[m["cols"]].to_numpy(float)]) @ m["beta"]


def metrics(y, yhat, k):
    e = np.asarray(y, float) - yhat
    n = len(e)
    r2 = 1 - (e ** 2).sum() / ((y - np.mean(y)) ** 2).sum()
    return dict(n=n, r2=r2, adj=1 - (1 - r2) * (n - 1) / (n - k - 1), mae=np.abs(e).mean(),
                rmse=np.sqrt((e ** 2).mean()), bias=e.mean())


def run(tr, te, cfg, t0):
    """Huấn luyện trên tr, đánh giá trên tr và te. Mọi chỉ số tính trên thang gốc (lượt thuê)."""
    mask = flag_outliers(tr) if cfg["drop_out"] else pd.Series(False, index=tr.index)
    fit_df = tr[~mask]
    Xf, groups = build_features(fit_df, cfg, t0)
    keep = Xf.columns[Xf.std() > 0]
    Xf = Xf[keep]
    m = fit_ols(Xf, target(fit_df["cnt"], cfg))
    Xtr, Xte = build_features(tr, cfg, t0)[0][keep], build_features(te, cfg, t0)[0][keep]
    ptr, pte = inverse(predict(m, Xtr), cfg), inverse(predict(m, Xte), cfg)
    base = np.full(len(te), tr["cnt"].mean())
    return dict(model=m, X=Xf, groups=groups, dropped=[c for c in Xf.columns if False], n_out=int(mask.sum()),
                dropped_cols=[c for c in build_features(fit_df, cfg, t0)[0].columns if c not in keep],
                ptr=ptr, pte=pte, m_tr=metrics(tr["cnt"].to_numpy(), ptr, m["k"]),
                m_te=metrics(te["cnt"].to_numpy(), pte, m["k"]), m_base=metrics(te["cnt"].to_numpy(), base, 0))


# ---------------------------------------------------------------- 6.4 Kiểm tra giả định
def acf(e, nlags=48):
    e = e - e.mean()
    return np.array([e[:-k] @ e[k:] / (e @ e) for k in range(1, nlags + 1)])


def diagnostics(m, X):
    e, n = m["resid"], len(m["resid"])
    A, e2 = np.column_stack([np.ones(n), X.to_numpy(float)]), m["resid"] ** 2
    aux = A @ np.linalg.lstsq(A, e2, rcond=None)[0]
    lm = n * (1 - ((e2 - aux) ** 2).sum() / ((e2 - e2.mean()) ** 2).sum())
    return dict(dw=np.sum(np.diff(e) ** 2) / np.sum(e ** 2), lm=lm, bp_p=stats.chi2.sf(lm, X.shape[1]),
                skew=stats.skew(e), kurt=stats.kurtosis(e), r1=acf(e, 1)[0])


def vif(X):
    if X.shape[1] < 2:
        return pd.Series(1.0, index=X.columns)
    R = np.corrcoef(((X - X.mean()) / X.std()).to_numpy().T)
    return pd.Series(np.diag(np.linalg.pinv(R)), index=X.columns)


# ---------------------------------------------------------------- hình và bảng (rules mục 4, 5)
EXPORT = False

FIGURES_DIR = Path("06_Model") / "figures"
TABLES_DIR = Path("06_Model") / "tables"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
TABLES_DIR.mkdir(parents=True, exist_ok=True)

def show_fig(num, title, fig, slug, purpose, reason):
    st.markdown(f"**Hình {num}. {title}**")
    st.caption(f"Mục đích: {purpose}  \nLý do chọn: {reason}")
    w, h = fig.get_size_inches()
    if w > 9:
        fig.set_size_inches(9, max(4.4, h * 9 / w))
    fig.suptitle(textwrap.fill(f"Hình {num}. {title}", 70), fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    st.pyplot(fig)
    if EXPORT:
        clean_num = str(num).replace(".", "_")
        filename = f"fig_{clean_num}_{slug}.png"

        if FIGURES_DIR.exists():
            fig.savefig(FIGURES_DIR / filename, dpi=200, bbox_inches="tight")
        else:
            st.error(
                f"Không tìm thấy thư mục {FIGURES_DIR}. Vui lòng kiểm tra lại!"
            )

    plt.close(fig)


def show_table(num, title, df, slug, index=False):
    st.markdown(f"**Bảng {num}. {title}**")
    st.dataframe(df, hide_index=not index)

    if EXPORT:
        clean_num = str(num).replace(".", "_")
        filename = f"bang_{clean_num}_{slug}.csv"

        if TABLES_DIR.exists():
            df.to_csv(TABLES_DIR / filename, index=index, encoding="utf-8-sig")
        else:
            st.error(
                f"Không tìm thấy thư mục {TABLES_DIR}. Vui lòng kiểm tra lại!"
            )
        

MODES = ["Liên tiếp theo thời gian", "Trộn theo ngày", "Trộn theo từng dòng"]


def split_post(d, cut, mode, frac):
    post = d[d.dteday > cut]
    if mode == MODES[0]:
        c2 = post.dteday.iloc[int(frac * len(post))]
        return post[post.dteday <= c2].copy(), post[post.dteday > c2].copy()
    rng = np.random.default_rng(SEED)
    if mode == MODES[1]:
        days = post.dteday.drop_duplicates().to_numpy()
        in_va = post.dteday.isin(rng.permutation(days)[: int(frac * len(days))]).to_numpy()
    else:
        in_va = rng.permutation(len(post)) < int(frac * len(post))
    return post[in_va].copy(), post[~in_va].copy()


@st.cache_data
def select_config(cut, mode, frac):
    d = load_data()
    t0 = d["dteday"].min()
    a = d[d.dteday <= cut]
    b, c_ = split_post(d, cut, mode, frac)
    base = dict(holiday=True, temp=True, hum=True, windspeed=True, atemp=False, weather=True, drop_out=False, inter=True)
    rows = []
    for K, tg, trd, mo in itertools.product((3, 5, 8), ("log", "cnt"), ("yr", "t"), ("cyc", "season", "none")):
        cf = dict(base, K=K, target=tg, trend=trd, month=mo)
        x, y = run(a, b, cf, t0)["m_te"], run(a, c_, cf, t0)["m_te"]
        rows.append((K, tg, trd, mo, x["rmse"], x["mae"], x["r2"], x["bias"], y["rmse"]))
    return pd.DataFrame(rows, columns=["K", "target", "trend", "month", "rmse", "mae", "r2", "bias", "rmse_te"]).sort_values("rmse").reset_index(drop=True)


def nx(text):
    st.info("*Nhận xét.* " + text) 


def fig_split(df, cut, va, te):
    daily = df.groupby("dteday")["cnt"].mean()
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.plot(daily[daily.index <= cut], color=C_TR, lw=1, label="Tập huấn luyện")
    ax.plot(daily[daily.index > cut], color="lightgray", lw=0.8, zorder=1)
    for part, col, lab in ((va, C_VA, "Tập kiểm định"), (te, C_TE, "Tập kiểm tra")):
        dd = part.groupby("dteday")["cnt"].mean()
        ax.scatter(dd.index, dd.values, s=9, color=col, label=lab, zorder=3)
    ax.axvline(cut, color="gray", ls="--")
    for yr in (2011, 2012):
        s = daily[daily.index.year == yr]
        mu = df.loc[df.dteday.dt.year == yr, "cnt"].mean()
        ax.hlines(mu, s.index.min(), s.index.max(), colors="k", ls=":", lw=1.5)
        ax.text(s.index.min(), mu + 8, f"Trung bình {yr}: {mu:.2f}", fontsize=11, bbox=dict(facecolor="white", alpha=0.85, edgecolor="none"))
    ax.set(xlabel="Ngày", ylabel="cnt trung bình theo ngày (lượt thuê/giờ)")
    ax.legend(loc="upper left")
    return fig


def fig_hour_encoding(tr):
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 4))
    h = np.arange(24)
    a.add_patch(plt.Circle((0, 0), 1, fill=False, color="gray"))
    a.scatter(np.cos(2 * np.pi * h / 24), np.sin(2 * np.pi * h / 24), c=h, cmap="twilight")
    for i in h[::3]:
        a.annotate(f"{i}h", (np.cos(2 * np.pi * i / 24) * 1.15, np.sin(2 * np.pi * i / 24) * 1.15), ha="center", va="center")
    a.set(xlabel="hr_cos1", ylabel="hr_sin1", xlim=(-1.4, 1.4), ylim=(-1.4, 1.4), aspect="equal")
    for w, lab in [(1, "Ngày làm việc"), (0, "Ngày nghỉ")]:
        b.plot(tr[tr.workingday == w].groupby("hr")["cnt"].mean(), marker="o", ms=4, label=lab)
    b.set(xlabel="Giờ trong ngày", ylabel="cnt trung bình (lượt thuê/giờ)", xticks=range(0, 24, 3))
    b.legend()
    return fig


def fig_time_pred(tr, va, te, ptr, pva, pte, cut):
    act = pd.concat([tr, va, te]).groupby("dteday")["cnt"].mean()
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.plot(act, color="k", lw=1, label="Thực tế")
    ax.plot(tr.assign(p=ptr).groupby("dteday")["p"].mean(), color=C_TR, lw=1, label="Dự đoán (tập huấn luyện)")
    for part, p_, col, lab in ((va, pva, C_VA, "Dự đoán (tập kiểm định)"), (te, pte, C_TE, "Dự đoán (tập kiểm tra)")):
        dd = part.assign(p=p_).groupby("dteday")["p"].mean()
        ax.scatter(dd.index, dd.values, s=9, color=col, label=lab, zorder=3)
    ax.axvline(cut, color="gray", ls="--")
    ax.set(xlabel="Ngày", ylabel="cnt trung bình theo ngày (lượt thuê/giờ)")
    ax.legend(loc="upper left")
    return fig


def fig_scatter(y, p):
    fig, ax = plt.subplots(figsize=(5.5, 5))
    hb = ax.hexbin(p, y, gridsize=45, bins="log", mincnt=1, cmap="viridis")
    lim = max(y.max(), p.max())
    ax.plot([0, lim], [0, lim], "r--", lw=1, label="Dự đoán = thực tế")
    ax.set(xlabel="Dự đoán (lượt thuê/giờ)", ylabel="Thực tế (lượt thuê/giờ)")
    fig.colorbar(hb, label="Số quan sát (thang log)")
    ax.legend()
    return fig


def fig_hour_pred(te, pte):
    fig, axs = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
    d = te.assign(p=pte)
    for ax, w, lab in zip(axs, (1, 0), ("Ngày làm việc", "Ngày nghỉ")):
        g = d[d.workingday == w].groupby("hr")[["cnt", "p"]].mean()
        ax.plot(g["cnt"], "k-o", ms=4, label="Thực tế")
        ax.plot(g["p"], color=C_PR, marker="s", ms=4, label="Dự đoán")
        ax.set(title=lab, xlabel="Giờ trong ngày", xticks=range(0, 24, 3))
    axs[0].set_ylabel("cnt trung bình (lượt thuê/giờ)")
    axs[0].legend()
    return fig


def fig_month_err(te, pte):
    d = te.assign(e=te["cnt"] - pte).assign(m=lambda x: x["dteday"].dt.strftime("%Y-%m"))
    g = d.groupby("m")["e"].agg(bias="mean", rmse=lambda s: np.sqrt((s ** 2).mean()))
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 4))
    a.bar(g.index, g["bias"], color=np.where(g["bias"] >= 0, C_TE, C_TR))
    a.axhline(0, color="k", lw=0.8)
    a.set(ylabel="Sai số TB (lượt thuê/giờ)", xlabel="Tháng")
    b.bar(g.index, g["rmse"], color="gray")
    b.set(ylabel="RMSE (lượt thuê/giờ)", xlabel="Tháng")
    for ax in (a, b):
        ax.tick_params(axis="x", rotation=45)
    return fig, g


def fig_resid_fitted(m, cfg):
    fig, ax = plt.subplots(figsize=(6, 4.5))
    hb = ax.hexbin(m["fitted"], m["resid"], gridsize=50, bins="log", mincnt=1, cmap="viridis")
    ax.axhline(0, color="r", ls="--", lw=1)
    unit = "log(1 + cnt)" if cfg["target"] == "log" else "lượt thuê/giờ"
    ax.set(xlabel=f"Giá trị khớp ({unit})", ylabel=f"Phần dư ({unit})")
    fig.colorbar(hb, label="Số quan sát (thang log)")
    return fig


def fig_resid_dist(m):
    e = m["resid"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 4))
    a.hist(e, bins=60, density=True, color=C_TR, alpha=0.7)
    x = np.linspace(e.min(), e.max(), 200)
    a.plot(x, stats.norm.pdf(x, e.mean(), e.std()), "r-", label="Phân phối chuẩn")
    a.set(xlabel="Phần dư (thang mô hình)", ylabel="Mật độ")
    a.legend(fontsize=10)
    stats.probplot(e, dist="norm", plot=b)
    b.set(title="", xlabel="Phân vị lý thuyết (chuẩn)", ylabel="Phân vị phần dư")
    return fig


def fig_acf(m):
    a = acf(m["resid"], 48)
    fig, ax = plt.subplots(figsize=(11, 3.5))
    ax.bar(range(1, 49), a, color=C_TR)
    bound = 1.96 / np.sqrt(len(m["resid"]))
    ax.axhline(bound, color="r", ls="--", lw=1)
    ax.axhline(-bound, color="r", ls="--", lw=1, label="Khoảng ±1.96/√n")
    ax.set(xlabel="Độ trễ (số quan sát liên tiếp)", ylabel="Tự tương quan phần dư")
    ax.legend()
    return fig, a


# ---------------------------------------------------------------- giao diện
def sidebar():
    s = st.sidebar
    s.header("Cấu hình mô hình")
    cut = s.date_input("Ngày cuối của tập huấn luyện", value=pd.Timestamp("2012-03-31"),
                       min_value=pd.Timestamp("2011-06-30"), max_value=pd.Timestamp("2012-11-30"))
    cfg = dict(cut=pd.Timestamp(cut))
    cfg["split_mode"] = s.radio("Cách chia phần sau ngày cắt", MODES, index=1)
    cfg["val_frac"] = s.slider("Tỷ lệ tập kiểm định trong phần sau ngày cắt", 0.2, 0.8, 0.5, 0.05)
    cfg["target"] = "log" if s.radio("Biến mục tiêu", ["log(1 + cnt)", "cnt"]) == "log(1 + cnt)" else "cnt"
    cfg["K"] = s.slider("Số hài sin/cos của giờ (K)", 1, 8, 5)
    cfg["inter"] = s.checkbox("Tương tác hài giờ × workingday", True)
    cfg["month"] = {"sin/cos tháng": "cyc", "one-hot mùa (season)": "season", "không dùng": "none"}[
        s.selectbox("Mã hóa tháng/mùa", ["sin/cos tháng", "one-hot mùa (season)", "không dùng"], index=2)]
    cfg["trend"] = {"yr (0/1)": "yr", "số năm tuyến tính": "t", "không dùng": "none"}[
        s.selectbox("Biến xu hướng tăng theo thời gian", ["yr (0/1)", "số năm tuyến tính", "không dùng"])]
    s.markdown("**Biến thời tiết** (giá trị chuẩn hóa)")
    for col in ("temp", "hum", "windspeed"):
        cfg[col] = s.checkbox(col, True)
    cfg["atemp"] = s.checkbox("atemp (dễ gây đa cộng tuyến với temp)", False)
    cfg["weather"] = s.checkbox("weathersit (one-hot)", True)
    cfg["holiday"] = s.checkbox("holiday", True)
    cfg["drop_out"] = s.checkbox("Loại ngoại lai (IQR theo nhóm yr, hr, workingday) khỏi tập huấn luyện", False)
    s.caption("casual và registered không được đưa vào (rò rỉ dữ liệu: cnt = casual + registered).")
    return cfg, s.button("Xuất hình và bảng cho báo cáo")


def main():
    global EXPORT
    st.set_page_config(page_title="Phần 6 - Mô hình MLR Bike Sharing", layout="wide")
    st.title("Phần 6. Xây dựng và đánh giá mô hình hồi quy tuyến tính đa biến (MLR)")
    cfg, EXPORT = sidebar()
    df = st.cache_data(load_data)()
    t0, cut = df["dteday"].min(), cfg["cut"]
    post = df[df.dteday > cut]
    va, te = split_post(df, cut, cfg["split_mode"], cfg["val_frac"])
    tr = df[df.dteday <= cut].copy()
    if len(va) < 100 or len(te) < 100 or len(tr) < 500:
        st.error("Điểm cắt làm một trong ba tập quá nhỏ. Hãy chọn ngày khác.")
        return
    r = run(tr, te, cfg, t0)
    rv = run(tr, va, cfg, t0)
    m, mt, me, mb = r["model"], r["m_tr"], r["m_te"], r["m_base"]
    if cfg["trend"] != "none" and r["dropped_cols"]:
        st.warning(f"Các biến {r['dropped_cols']} không đổi giá trị trong tập huấn luyện nên bị bỏ. "
                   "Với điểm cắt này tập huấn luyện không chứa năm 2012, mô hình không học được xu hướng tăng.")
    c = st.columns(4)
    c[0].metric("RMSE tập kiểm tra", f"{me['rmse']:.2f} lượt thuê/giờ")
    c[1].metric("MAE tập kiểm tra", f"{me['mae']:.2f} lượt thuê/giờ")
    c[2].metric("R² tập kiểm tra", f4(me["r2"]))
    c[3].metric("Số biến độc lập", m["k"])

    t61, t62, t63, t64, t65, t66 = st.tabs(["6.1 Feature Engineering", "6.2 Chia dữ liệu", "6.3 Huấn luyện",
                                            "6.4 Đánh giá", "6.5 Nhận xét", "6.6 Kết luận và hạn chế"])

    # ---- 6.1
    with t61:
        st.markdown("Biến mục tiêu `Y` là " + ("`log(1 + cnt)`; đánh giá cuối quy về thang gốc (lượt thuê)." if cfg["target"] == "log"
                                              else "`cnt` (tổng số lượt thuê mỗi giờ)."))
        rows = [(g, ", ".join(c for c in cols if c in m["cols"]), how, why) for g, cols, how, why in r["groups"]
                if any(c in m["cols"] for c in cols)]
        show_table("6.1", "Các biến độc lập và cách mã hóa", pd.DataFrame(rows, columns=["Nhóm", "Cột trong mô hình", "Cách mã hóa", "Lý do"]), "features")
        hr_cols = [c for c in m["cols"] if c.startswith("hr_")]
        wx_cols = [c for c in m["cols"] if c in ("temp", "hum", "windspeed", "weathersit_2", "weathersit_3_4")]
        nx(f"Mô hình có {m['k']} biến độc lập, trong đó {len(hr_cols)} cột ({100 * len(hr_cols) / m['k']:.2f}%) mô tả giờ trong ngày (gồm cả tích với `workingday`) và {len(wx_cols)} cột mô tả thời tiết. "  + "Phần lớn tham số được dành cho dáng đường cong theo giờ vì `cnt` thay đổi rất khác nhau giữa các giờ (Hình 6.1). " + (f"`atemp` không đưa vào vì tương quan với `temp` là {f4(df.temp.corr(df.atemp))}, gần như trùng thông tin." if not cfg["atemp"] else "`atemp` được đưa vào cùng `temp` nên có nguy cơ đa cộng tuyến.") + " `casual` và `registered` bị loại để tránh rò rỉ dữ liệu.")

        show_fig("6.1", "Mã hóa giờ trên vòng tròn và nhu cầu theo giờ", fig_hour_encoding(tr), "hour_encoding",
                 "cho thấy vì sao giờ cần mã hóa chu kỳ và vì sao cần nhiều hài",
                 "vòng tròn thể hiện sự liền kề của giờ 23 và 0; đường trung bình theo giờ cho thấy hình dạng nhu cầu")
        w1 = tr[tr.workingday == 1].groupby("hr")["cnt"].mean()
        w0 = tr[tr.workingday == 0].groupby("hr")["cnt"].mean()
        a1, p1, p0 = w1[w1.index < 12].idxmax(), w1[w1.index >= 12].idxmax(), w0.idxmax()
        mid = w1.loc[a1:p1].idxmin()

        nx(f"Trên tập huấn luyện, ở ngày làm việc, `cnt` trung bình tăng mạnh vào buổi sáng và đạt đỉnh lúc {a1} giờ ({f2(w1[a1])} lượt thuê/giờ), giảm xuống thấp nhất lúc {mid} giờ ({f2(w1[mid])} lượt thuê/giờ), "
        + f"rồi đạt đỉnh {'cao' if w1[p1] > w1[a1] else 'thấp'} hơn lúc {p1} giờ ({f2(w1[p1])} lượt thuê/giờ); mức thấp nhất trong ngày là lúc {w1.idxmin()} giờ ({f2(w1.min())} lượt thuê/giờ). "
        + f"Ở ngày nghỉ chỉ có một đỉnh rộng lúc {p0} giờ ({f2(w0[p0])} lượt thuê/giờ). "
        + "Hai đỉnh ở ngày làm việc khớp với giờ đi làm và tan làm, nên một cặp sin/cos (chỉ tạo một đỉnh mỗi ngày) không đủ, cần nhiều hài và tích với `workingday`. "
        +"Vòng tròn bên trái đặt giờ 23 sát giờ 0, đúng với thực tế hai giờ này liền kề.")

    # ---- 6.2
    with t62:
        g11, g12 = df[df.yr == 0]["cnt"].mean(), df[df.yr == 1]["cnt"].mean()
        sp = pd.DataFrame({"Tập": ["Huấn luyện", "Kiểm định", "Kiểm tra"], "Từ ngày": [x.dteday.min().date() for x in (tr, va, te)],
                           "Đến ngày": [x.dteday.max().date() for x in (tr, va, te)], "Số dòng": [f"{len(x):,}" for x in (tr, va, te)],
                           "cnt trung bình (lượt thuê/giờ)": [f2(x.cnt.mean()) for x in (tr, va, te)]})
        show_table("6.2", "Chia dữ liệu thành ba tập huấn luyện, kiểm định, kiểm tra", sp, "split")
        how = {MODES[0]: "được chia theo thứ tự thời gian thành hai nửa liên tiếp",
               MODES[1]: f"được trộn ngẫu nhiên theo từng ngày (SEED = {SEED}) rồi chia theo số ngày",
               MODES[2]: f"được trộn ngẫu nhiên theo từng dòng (SEED = {SEED}) rồi chia theo số dòng"}[cfg["split_mode"]]
        why = {MODES[0]: "Giữ nguyên thứ tự thời gian nên tập kiểm định và tập kiểm tra thuộc hai giai đoạn khác nhau của năm (xem Hình 6.2); chênh lệch giữa hai tập vì thế phản ánh cả mùa vụ.",
               MODES[1]: "Mô hình chỉ được huấn luyện trên dữ liệu đến hết " + str(cut.date()) + " nên cả hai tập đều là dữ liệu của các tháng sau thời điểm huấn luyện. Trộn theo ngày giúp hai tập cùng trải đều các tháng 4 đến 12 (`cnt` trung bình gần nhau) và giữ mọi giờ của một ngày trong cùng một tập, vì các giờ liền kề có `cnt` rất giống nhau.",
               MODES[2]: "Mô hình chỉ được huấn luyện trên dữ liệu đến hết " + str(cut.date()) + " nên không học từ tập kiểm định. Trộn theo từng dòng khiến các giờ liền kề của cùng một ngày rơi vào hai tập khác nhau, nên hai tập không độc lập hoàn toàn và chỉ số kiểm tra có thể lạc quan hơn."}[cfg["split_mode"]]
        nx(f"Tập huấn luyện có {len(tr):,} dòng ({100 * len(tr) / len(df):.2f}% dữ liệu) với `cnt` trung bình {f2(tr.cnt.mean())} lượt thuê/giờ. "
           f"Phần sau ngày {cut.date()} ({len(post):,} dòng) {how}: tập kiểm định {len(va):,} dòng (`cnt` trung bình {f2(va.cnt.mean())} lượt thuê/giờ) "
           f"và tập kiểm tra {len(te):,} dòng (`cnt` trung bình {f2(te.cnt.mean())} lượt thuê/giờ). Hai tập này cao hơn tập huấn luyện lần lượt {100 * (va.cnt.mean() / tr.cnt.mean() - 1):.2f}% và {100 * (te.cnt.mean() / tr.cnt.mean() - 1):.2f}%, "
           "nên mô hình phải dự đoán ở mức nhu cầu cao hơn mức đã thấy khi huấn luyện, tức là ngoại suy xu hướng chứ không chỉ nội suy. "
           "Tập kiểm định dùng để chọn cấu hình mô hình; tập kiểm tra chỉ dùng để báo cáo kết quả của cấu hình đã chọn. " + why)

        show_fig("6.2", "Chuỗi cnt trung bình theo ngày và cách chia huấn luyện/kiểm định/kiểm tra", fig_split(df, cut, va, te), "figure_split",
                 "thể hiện xu hướng tăng giữa hai năm, ngày cắt huấn luyện và các ngày thuộc tập kiểm định, tập kiểm tra",
                 "đường cho phần huấn luyện (chuỗi thời gian liên tục) và chấm cho từng ngày của tập kiểm định, tập kiểm tra để thấy cách các ngày được phân bổ")
        mm = df.groupby(["yr", "mnth"])["cnt"].mean().unstack(0)
        ratio = mm[1] / mm[0]
        pk0, pk1 = mm[0].idxmax(), mm[1].idxmax()
        nx(f"`cnt` trung bình theo ngày thấp vào mùa đông và cao vào mùa hè–thu ở cả hai năm: tháng cao nhất là tháng {pk0} của 2011 ({f2(mm[0][pk0])} lượt thuê/giờ) và tháng {pk1} của 2012 ({f2(mm[1][pk1])} lượt thuê/giờ). "
        + f"Mỗi tháng của 2012 đều cao hơn cùng tháng của 2011, với tỷ lệ từ {ratio.min():.2f} lần (tháng {ratio.idxmin()}) đến {ratio.max():.2f} lần (tháng {ratio.idxmax()}), trong khi mức tăng trung bình cả năm là {100 * (g12 / g11 - 1):.2f}%. "
        + "Mức tăng không đồng đều giữa các tháng nên một biến xu hướng đơn giản (bước nhảy giữa hai năm hoặc tuyến tính theo thời gian) chỉ xấp xỉ được hiện tượng này (xem Hình 6.6).")

        cs = []
        for lab, a, b in [("Chia ngẫu nhiên 80/20", *(lambda s: (s.iloc[:int(.8 * len(df))], s.iloc[int(.8 * len(df)):]))(df.sample(frac=1, random_state=SEED)))] + \
                [(f"Theo thời gian, cắt {d}", df[df.dteday <= d], df[df.dteday > d]) for d in ("2012-01-31", "2012-03-31", "2012-06-30", "2012-08-31")]:
            rr = run(a, b, cfg, t0)
            cs.append((lab, f"{len(a):,}", f"{len(b):,}", f2(rr["m_te"]["rmse"]), f2(rr["m_te"]["mae"]), f4(rr["m_te"]["r2"]), f2(rr["m_te"]["bias"])))

        show_table("6.3", "So sánh chiến lược chia dữ liệu (cùng cấu hình biến ở thanh bên; tập kiểm tra là toàn bộ phần sau điểm cắt)",
                   pd.DataFrame(cs, columns=["Chiến lược", "Số dòng huấn luyện", "Số dòng kiểm tra", "RMSE (lượt thuê/giờ)", "MAE (lượt thuê/giờ)", "R²", "Sai số TB (thực tế − dự đoán)"]), "compare_split")
        rm = [float(x[3]) for x in cs[1:]]
        bm = [float(x[6]) for x in cs[1:]]
        nx(f"Chia ngẫu nhiên 80/20 cho RMSE {cs[0][3]} lượt thuê/giờ và R² {cs[0][5]}, {'tốt hơn' if float(cs[0][3]) < min(rm) else 'không tốt hơn'} các cách chia theo thời gian (RMSE từ {min(rm):.2f} đến {max(rm):.2f} lượt thuê/giờ). "
        + "Khi chia ngẫu nhiên, các giờ liền kề có `cnt` rất giống nhau nằm ở cả hai tập nên chỉ số lạc quan hơn tình huống dự đoán tương lai. "
        + f"Với cách chia theo thời gian, sai số trung bình (thực tế − dự đoán) đổi từ {min(bm):.2f} đến {max(bm):.2f} lượt thuê/giờ tùy điểm cắt, tức kết quả phụ thuộc vào số tháng của 2012 nằm trong tập huấn luyện.")

    # ---- 6.3
    with t63:
        names = ["const"] + m["cols"]
        coef = pd.DataFrame({"Biến": names, "Hệ số β": m["beta"], "Sai số chuẩn": m["se"], "t": m["t"],
                             "p-value": [fp(p) for p in m["p"]], "CI 95% thấp": m["lo"], "CI 95% cao": m["hi"]})
        for col in ("Hệ số β", "Sai số chuẩn", "t", "CI 95% thấp", "CI 95% cao"):
            coef[col] = coef[col].map(f4)
        show_table("6.4", f"Hệ số hồi quy (OLS, n = {m['n']:,} dòng huấn luyện)", coef, "coefficients")
        ns = [c for c, p in zip(names[1:], m["p"][1:]) if p >= 0.05]
        top3 = sorted(zip(names[1:], m["t"][1:]), key=lambda z: -abs(z[1]))[:3]

        txt = f"Ba hệ số có |t| lớn nhất là " + ", ".join(f"`{c}` (t = {f2(t)})" for c, t in top3) + ". "
        if "temp" in m["cols"]:
            b = m["beta"][m["cols"].index("temp") + 1] * 0.1
            txt += f"Hệ số của `temp` {'dương' if b > 0 else 'âm'}: khi `temp` (chuẩn hóa) tăng 0.1 và các biến khác giữ nguyên, " + (f"`cnt` {'tăng' if b > 0 else 'giảm'} khoảng {abs(100 * (np.exp(b) - 1)):.2f}%. " if cfg["target"] == "log" else f"`cnt` {'tăng' if b > 0 else 'giảm'} khoảng {abs(b):.2f} lượt thuê/giờ. ")
        if "yr" in m["cols"]:
            b = m["beta"][m["cols"].index("yr") + 1]
            txt += f"Hệ số của `yr` cho thấy năm 2012 cao hơn 2011 khoảng " + (f"{100 * (np.exp(b) - 1):.2f}% " if cfg["target"] == "log" else f"{b:.2f} lượt thuê/giờ ") + "khi các biến khác giữ nguyên. "
        if "t_year" in m["cols"]:
            b = m["beta"][m["cols"].index("t_year") + 1]
            txt += "Hệ số của `t_year` cho thấy khi thời gian tăng thêm một năm và các biến khác giữ nguyên, " + (f"`cnt` {'tăng' if b > 0 else 'giảm'} khoảng {abs(100 * (np.exp(b) - 1)):.2f}%. " if cfg["target"] == "log" else f"`cnt` {'tăng' if b > 0 else 'giảm'} khoảng {abs(b):.2f} lượt thuê/giờ. ")
        txt += (f"Các hệ số chưa đủ bằng chứng thống kê để bác bỏ H0 (β = 0) là {', '.join('`' + c + '`' for c in ns)}. " if ns else "")
        nx(txt + "Do phần dư có tự tương quan (xem 6.4), p-value chỉ mang tính tham khảo.")

        st.markdown(f"R² trên tập huấn luyện (thang mô hình) = {f4(m['r2'])}; Adjusted R² = {f4(m['adj'])}.")
        st.markdown(f"{int((m['p'] < 0.05).sum())}/{len(m['p'])} hệ số có p < 0.05. Với n lớn, p-value nhỏ không đồng nghĩa ảnh hưởng lớn; cần xem độ lớn hệ số (Bảng 6.8)."
              + " Sai số chuẩn và p-value giả định phần dư độc lập; dữ liệu theo giờ có tự tương quan (xem 6.4) nên p-value chỉ mang tính tham khảo."
              + " Hệ số của các hài sin/cos không diễn giải riêng lẻ được; hình dạng theo giờ xem ở Hình 6.5.")

    # ---- 6.4
    with t64:
        tbl = pd.DataFrame([("Huấn luyện", mt), ("Kiểm tra", me)], columns=["Tập", "m"])
        out = [(n, f"{x['n']:,}", f4(x["r2"]), f4(x["adj"]), f2(x["mae"]), f2(x["rmse"])) for n, x in [("Huấn luyện", mt), ("Kiểm định", rv["m_te"]), ("Kiểm tra", me)]]
        out.append(("Kiểm tra, mô hình cơ sở (dự đoán bằng trung bình huấn luyện)", f"{mb['n']:,}", f4(mb["r2"]), "—", f2(mb["mae"]), f2(mb["rmse"])))
        show_table("6.5", "Chỉ số đánh giá trên thang gốc (lượt thuê)",
                   pd.DataFrame(out, columns=["Tập", "Số dòng", "R²", "Adjusted R²", "MAE (lượt thuê/giờ)", "RMSE (lượt thuê/giờ)"]), "metrics")
        mv = rv["m_te"]
        nx(f"Trên tập kiểm tra, R² là {f4(me['r2'])} so với {f4(mt['r2'])} ở tập huấn luyện và {f4(mv['r2'])} ở tập kiểm định; RMSE là {f2(me['rmse'])} lượt thuê/giờ ở tập kiểm tra, {f2(mv['rmse'])} ở tập kiểm định và {f2(mt['rmse'])} ở tập huấn luyện. "
           f"MAE ở tập kiểm tra là {f2(me['mae'])} lượt thuê/giờ, bằng {100 * me['mae'] / te.cnt.mean():.2f}% `cnt` trung bình của tập kiểm tra. "
           f"Mô hình giảm RMSE {100 * (1 - me['rmse'] / mb['rmse']):.2f}% so với mô hình cơ sở. "
           + (f"R² của mô hình cơ sở âm vì trung bình huấn luyện ({f2(tr.cnt.mean())}) thấp hơn trung bình kiểm tra ({f2(te.cnt.mean())}), một biểu hiện khác của xu hướng tăng. " if mb["r2"] < 0 else "")
           + f"Sai số trung bình (thực tế − dự đoán) là {f2(mv['bias'])} lượt thuê/giờ ở tập kiểm định và {f2(me['bias'])} lượt thuê/giờ ở tập kiểm tra; "
           + ("chênh lệch giữa hai tập cho thấy hiệu năng thay đổi theo giai đoạn dữ liệu." if abs(mv["r2"] - me["r2"]) > 0.03 else "hai tập cho kết quả gần nhau."))

        c1, c2 = st.columns(2)
        with c1:
            show_fig("6.3", "Thực tế và dự đoán theo ngày (tập huấn luyện, kiểm định, kiểm tra)", fig_time_pred(tr, va, te, r["ptr"], rv["pte"], r["pte"], cut), "time_pred",
                     "kiểm tra mô hình có bám xu hướng tăng và mùa vụ ở tập kiểm định và tập kiểm tra không", "biểu đồ đường theo thời gian")
            dv = va.assign(p=rv["pte"]).groupby("dteday")[["cnt", "p"]].mean()
            dd = te.assign(p=r["pte"]).groupby("dteday")[["cnt", "p"]].mean()
            cv_, cr = dv["cnt"].corr(dv["p"]), dd["cnt"].corr(dd["p"])
            gap = dd["p"] - dd["cnt"]
            wd_ = gap.abs().idxmax()
            nx(f"Hệ số tương quan Pearson giữa `cnt` thực tế và dự đoán theo ngày là {f4(cv_)} ở tập kiểm định và {f4(cr)} ở tập kiểm tra: đường dự đoán {'bám theo' if cr > 0.8 else 'chưa bám tốt'} xu hướng và biến động mùa của đường thực tế ở tập kiểm tra. "
               f"Ở tập kiểm tra, ngày lệch nhiều nhất là {wd_.date()}, dự đoán {'cao' if gap[wd_] > 0 else 'thấp'} hơn thực tế {f2(abs(gap[wd_]))} lượt thuê/giờ. "
               f"Đường dự đoán ở tập kiểm định và tập kiểm tra lệch nhiều hơn ở tập huấn luyện, phù hợp với RMSE tăng từ {f2(mt['rmse'])} lên {f2(mv['rmse'])} và {f2(me['rmse'])} lượt thuê/giờ.")
        with c2:
            show_fig("6.4", "Dự đoán so với thực tế (tập kiểm tra)", fig_scatter(te["cnt"].to_numpy(), r["pte"]), "scatter",
                     "xem mức lệch của từng quan sát so với đường dự đoán = thực tế", "hexbin tránh dính điểm với hơn 6,000 quan sát")
            yy, pp = te["cnt"].to_numpy(), r["pte"]
            ee = pp - yy
            q90 = np.percentile(yy, 90)
            hi = yy > q90
            nx(f"{100 * np.mean(np.abs(ee) <= 50):.2f}% quan sát có sai số tuyệt đối không quá 50 lượt thuê/giờ. "
            + f"Ở nhóm 10% giờ có `cnt` cao nhất (trên {f2(q90)} lượt thuê/giờ), dự đoán trung bình {f2(pp[hi].mean())} lượt thuê/giờ so với thực tế {f2(yy[hi].mean())} lượt thuê/giờ, tức {'thấp' if pp[hi].mean() < yy[hi].mean() else 'cao'} hơn {100 * abs(pp[hi].mean() / yy[hi].mean() - 1):.2f}%. "
            + f"MAE ở nhóm này là {f2(np.abs(ee[hi]).mean())} lượt thuê/giờ, so với {f2(np.abs(ee[~hi]).mean())} lượt thuê/giờ ở phần còn lại: sai số tập trung ở các giờ cao điểm. "
            + ("Độ lệch trung bình nhỏ nhưng MAE lớn, tức sai số ở nhóm này đi theo cả hai hướng và triệt tiêu nhau khi lấy trung bình, nên mô hình dự đoán đỉnh nhu cầu kém ổn định." if abs(pp[hi].mean() - yy[hi].mean()) < 0.25 * np.abs(ee[hi]).mean() else "Mô hình lệch có hệ thống ở các giờ cao điểm."))
        show_fig("6.5", "cnt trung bình theo giờ: thực tế và dự đoán (tập kiểm tra)", fig_hour_pred(te, r["pte"]), "hour_pred",
                 "kiểm tra mô hình tái hiện đường cong theo giờ ở ngày làm việc và ngày nghỉ", "so sánh hai đường theo giờ, tách theo workingday")
        d5 = te.assign(p=r["pte"])
        parts = []
        for w, lab in ((1, "ngày làm việc"), (0, "ngày nghỉ")):
            gh = d5[d5.workingday == w].groupby("hr")[["cnt", "p"]].mean()
            dif = gh["p"] - gh["cnt"]
            h = dif.abs().idxmax()
            parts.append(f"Ở {lab}, đường dự đoán {'tái hiện sát' if gh['cnt'].corr(gh['p']) > 0.9 else 'chưa tái hiện tốt'} hình dạng theo giờ (tương quan {f4(gh['cnt'].corr(gh['p']))}); chênh lệch lớn nhất lúc {h} giờ, dự đoán {'cao' if dif[h] > 0 else 'thấp'} hơn thực tế {f2(abs(dif[h]))} lượt thuê/giờ (thực tế {f2(gh['cnt'][h])} lượt thuê/giờ).")
        nx(" ".join(parts))

        fm, gm = fig_month_err(pd.concat([va, te]), np.r_[rv["pte"], r["pte"]])
        show_fig("6.6", "Sai số theo tháng (tập kiểm định và tập kiểm tra)", fm, "month_error",
                 "phát hiện sai lệch hệ thống theo thời gian (độ lệch xu hướng)", "cột theo tháng cho thấy sai số đổi dấu hay lệch dần")
        mx, mn = gm["bias"].idxmax(), gm["bias"].idxmin()
        chg = int((np.sign(gm["bias"]).diff().abs() > 0).sum())
        nx(f"Sai số trung bình (thực tế − dự đoán) cao nhất ở {mx} ({gm['bias'][mx]:+.2f} lượt thuê/giờ, dự đoán {'thấp' if gm['bias'][mx] > 0 else 'cao'} hơn thực tế) và thấp nhất ở {mn} ({gm['bias'][mn]:+.2f} lượt thuê/giờ, dự đoán {'thấp' if gm['bias'][mn] > 0 else 'cao'} hơn thực tế); dấu đổi {chg} lần trong {len(gm)} tháng. "
        + f"RMSE theo tháng lớn nhất ở {gm['rmse'].idxmax()} ({f2(gm['rmse'].max())} lượt thuê/giờ) và nhỏ nhất ở {gm['rmse'].idxmin()} ({f2(gm['rmse'].min())} lượt thuê/giờ). "
        + ("Sai số kéo dài cùng dấu qua nhiều tháng liên tiếp chứ không dao động ngẫu nhiên quanh 0, phù hợp với nhận xét ở Hình 6.2 rằng tỷ lệ tăng so với cùng kỳ năm trước khác nhau giữa các tháng." if chg <= len(gm) / 3 else "Dấu sai số đổi nhiều lần giữa các tháng nên chưa thấy lệch có hệ thống theo thời gian."))

        st.subheader("Kiểm tra giả định (trên tập huấn luyện)")
        dg = diagnostics(m, r["X"])
        show_table("6.6", "Kết quả kiểm tra giả định",
                   pd.DataFrame([("Độc lập", "Durbin–Watson", f4(dg["dw"]), "gần 2: không tự tương quan bậc 1; gần 0: tự tương quan dương"),
                                 ("Độc lập", "Tự tương quan phần dư độ trễ 1", f4(dg["r1"]), "xem Hình 6.8"),
                                 ("Phương sai không đổi", "Breusch–Pagan (LM)", f"{dg['lm']:,.2f}, {fp(dg['bp_p'])}", "mẫu lớn nên dễ bác bỏ; xem thêm Hình 6.7"),
                                 ("Phần dư chuẩn", "Độ lệch (skewness)", f4(dg["skew"]), "0 nếu đối xứng"),
                                 ("Phần dư chuẩn", "Độ nhọn dư (excess kurtosis)", f4(dg["kurt"]), "0 nếu như phân phối chuẩn")],
                                columns=["Giả định", "Thống kê", "Giá trị", "Cách đọc"]), "assumptions")
        nx(f"Durbin–Watson là {f4(dg['dw'])} và tự tương quan phần dư độ trễ 1 là {f4(dg['r1'])}: "
        + ("phần dư của hai giờ liên tiếp cùng chiều rõ rệt (nếu độc lập, Durbin–Watson gần 2), nên giả định độc lập bị vi phạm; sai số chuẩn bị đánh giá thấp và p-value ở Bảng 6.4 nhỏ hơn thực tế. " if dg["dw"] < 1.5 else "chưa thấy tự tương quan bậc 1 đáng kể. ")
        + f"Breusch–Pagan cho LM = {f2(dg['lm'])}, {fp(dg['bp_p'])}: "
        + ("có bằng chứng thống kê cho thấy phương sai phần dư không đồng đều. " if dg["bp_p"] < 0.05 else "chưa đủ bằng chứng thống kê để bác bỏ giả thuyết phương sai không đổi. ")
        + f"Độ lệch {f4(dg['skew'])} ({'đuôi trái dài hơn, tức có những giờ dự đoán cao hơn thực tế nhiều' if dg['skew'] < -0.3 else 'đuôi phải dài hơn' if dg['skew'] > 0.3 else 'gần đối xứng'}) và độ nhọn dư {f4(dg['kurt'])} ({'đuôi nặng hơn phân phối chuẩn' if dg['kurt'] > 0.5 else 'gần phân phối chuẩn'}).")

        d1, d2 = st.columns(2)
        with d1:
            show_fig("6.7", "Phần dư theo giá trị khớp (tập huấn luyện)", fig_resid_fitted(m, cfg), "resid_fitted",
                     "kiểm tra tính tuyến tính và phương sai không đổi", "phần dư quanh 0 và độ rộng đều theo giá trị khớp là dấu hiệu tốt")
            dec = pd.qcut(m["fitted"], 10, labels=False, duplicates="drop")
            sd = pd.Series(m["resid"]).groupby(dec).std()
            nx(f"Phần dư dao động quanh 0 nhưng độ phân tán đổi theo giá trị khớp: độ lệch chuẩn của phần dư là {f4(sd.iloc[0])} ở nhóm giá trị khớp thấp nhất và {f4(sd.iloc[-1])} ở nhóm cao nhất, "
            + f"tức nhóm thấp nhất {'lớn' if sd.iloc[0] > sd.iloc[-1] else 'nhỏ'} hơn nhóm cao nhất {max(sd.iloc[0], sd.iloc[-1]) / min(sd.iloc[0], sd.iloc[-1]):.2f} lần. "
            + "Phương sai phần dư không đồng đều, phù hợp với kết quả Breusch–Pagan ở Bảng 6.6.")
        with d2:
            fa, acfv = fig_acf(m)
            show_fig("6.8", "Tự tương quan của phần dư theo độ trễ", fa, "acf",
                     "kiểm tra giả định độc lập của phần dư", "dữ liệu theo giờ liên tiếp nên cần kiểm tra tự tương quan")
            bnd = 1.96 / np.sqrt(len(m["resid"]))
            nx(f"Tự tương quan phần dư là {f4(acfv[0])} ở độ trễ 1, {f4(acfv[11])} ở độ trễ 12 và {f4(acfv[23])} ở độ trễ 24; {int((np.abs(acfv) > bnd).sum())}/48 độ trễ vượt khoảng ±{bnd:.4f}. "
            + "Phần dư của các giờ gần nhau liên quan chặt và mối liên quan còn kéo dài nhiều độ trễ, nên các giờ liên tiếp không độc lập; đây là cơ sở của giá trị Durbin–Watson thấp ở Bảng 6.6.")

        show_fig("6.9", "Phân phối và Q–Q plot của phần dư", fig_resid_dist(m), "resid_dist",
                 "kiểm tra giả định phần dư chuẩn", "histogram kèm đường chuẩn và Q–Q plot, không chỉ dựa vào p-value")
        e_ = m["resid"]; s_ = e_.std()
        lo_, hi_ = 100 * np.mean(e_ < e_.mean() - 3 * s_), 100 * np.mean(e_ > e_.mean() + 3 * s_)
        nx(f"Có {lo_:.2f}% phần dư thấp hơn trung bình quá 3 độ lệch chuẩn và {hi_:.2f}% cao hơn quá 3 độ lệch chuẩn (phân phối chuẩn kỳ vọng 0.13% mỗi phía). "
        + f"Độ lệch {f4(dg['skew'])} và độ nhọn dư {f4(dg['kurt'])} cho thấy phần dư không chuẩn, "
        + ("đuôi trái nặng hơn: một số giờ thực tế thấp hơn dự đoán rất nhiều. " if lo_ > hi_ else "đuôi phải nặng hơn: một số giờ thực tế cao hơn dự đoán rất nhiều. ")
        + "Với mẫu lớn, ước lượng hệ số vẫn xấp xỉ chuẩn nhưng khoảng dự đoán cho từng giờ không đáng tin.")

        v = vif(r["X"])
        nh = [c for c in r["X"].columns if not c.startswith("hr_")]
        v2 = vif(r["X"][nh]) if len(nh) > 1 else pd.Series(dtype=float)
        vt = pd.DataFrame({"Biến": v.index, "VIF (toàn bộ biến)": v.map(f2).values,
                           "VIF (không gồm hài giờ)": [f2(v2[c]) if c in v2.index else "—" for c in v.index]})
        show_table("6.7", "Hệ số phóng đại phương sai (VIF)", vt, "vif")
        nx(f"VIF lớn nhất là {v.idxmax()} ({f2(v.max())}); "
        + ("có biến vượt ngưỡng 10 nên cần xem xét đa cộng tuyến. " if v.max() > 10 else "không biến nào vượt ngưỡng 10 nên chưa thấy đa cộng tuyến đáng kể. ")
        + f"Các cột hài giờ có VIF từ {f2(v[[c for c in v.index if c.startswith('hr_')]].min())} đến {f2(v[[c for c in v.index if c.startswith('hr_')]].max())}; mức này chủ yếu đến từ việc mỗi hài giờ đi cùng tích của chính nó với `workingday`, không phải do đa cộng tuyến giữa các biến khác nhau.")
        
    # ---- 6.5
    with t65:
        scale = 0.1
        eff = []
        for col, lab in [("temp", "temp"), ("hum", "hum"), ("windspeed", "windspeed"), ("atemp", "atemp"), ("weathersit_2", "weathersit = 2 (so với 1)"),
                         ("weathersit_3_4", "weathersit = 3 hoặc 4 (so với 1)"), ("holiday", "holiday = 1"), ("yr", "yr = 1 (2012 so với 2011)"), ("t_year", "thời gian tăng thêm 1 năm")]:
            if col in m["cols"]:
                i = m["cols"].index(col) + 1
                s = 1 if col in ("weathersit_2", "weathersit_3_4", "holiday", "yr", "t_year") else scale
                b, lo, hi = m["beta"][i] * s, m["lo"][i] * s, m["hi"][i] * s
                if cfg["target"] == "log":
                    val = f"{100 * (np.exp(b) - 1):+.2f}% ({100 * (np.exp(lo) - 1):+.2f}% đến {100 * (np.exp(hi) - 1):+.2f}%)"
                else:
                    val = f"{b:+.2f} lượt thuê/giờ ({lo:+.2f} đến {hi:+.2f})"
                eff.append((lab + ("" if s == 1 else " tăng 0.1 (chuẩn hóa)"), val, fp(m["p"][i])))
        if eff:
            show_table("6.8", "Thay đổi của cnt khi một biến đổi, giữ nguyên các biến khác (CI 95%)",
                       pd.DataFrame(eff, columns=["Biến", "Thay đổi ước lượng của cnt", "p-value"]), "effects")
        rows_ = {x[0]: x for x in eff}
        ks = [k for k in rows_ if k.startswith("weathersit = 3")] + [k for k in rows_ if k.startswith("yr") or k.startswith("thời gian")] + [k for k in rows_ if k.startswith("temp")]
        nx(" ".join(f"Khi {k}, `cnt` thay đổi {rows_[k][1]} ({rows_[k][2]})." for k in ks)
        + f" Mô hình giải thích {100 * me['r2']:.2f}% phương sai của `cnt` ở tập kiểm tra. Các thay đổi này là mối liên hệ thống kê trong mô hình, không chứng minh quan hệ nhân quả.")

        sel = select_config(cut, cfg["split_mode"], cfg["val_frac"])
        nm_m, nm_t = {"cyc": "sin/cos tháng", "season": "one-hot mùa", "none": "không dùng"}, {"yr": "yr (0/1)", "t": "tuyến tính theo năm"}
        orig = sel[(sel.K == 5) & (sel.target == "log") & (sel.trend == "yr") & (sel.month == "cyc")].index[0]
        show_idx = list(range(6)) + ([orig] if orig >= 6 else [])
        sv = pd.DataFrame({"Hạng": [i + 1 for i in show_idx], "K": sel.K[show_idx].values, "Biến mục tiêu": sel.target[show_idx].map({"log": "log(1 + cnt)", "cnt": "cnt"}).values,
                           "Xu hướng": sel.trend[show_idx].map(nm_t).values, "Mã hóa tháng/mùa": sel.month[show_idx].map(nm_m).values,
                           "RMSE kiểm định (lượt thuê/giờ)": sel.rmse[show_idx].map(f2).values, "MAE kiểm định (lượt thuê/giờ)": sel.mae[show_idx].map(f2).values, "R² kiểm định": sel.r2[show_idx].map(f4).values})
        show_table("6.9", f"Chọn cấu hình trên tập kiểm định ({len(sel)} cấu hình, xếp theo RMSE)", sv, "config_selection")
        best, o = sel.iloc[0], sel.iloc[orig]
        nx(f"Trong {len(sel)} cấu hình, cấu hình tốt nhất theo RMSE kiểm định có K = {best.K}, biến mục tiêu {'log(1 + cnt)' if best.target == 'log' else 'cnt'}, xu hướng {nm_t[best.trend]}, mã hóa tháng {nm_m[best.month]}, với RMSE {f2(best.rmse)} lượt thuê/giờ. "
           f"Cấu hình ban đầu (K = 5, log(1 + cnt), `yr`, sin/cos tháng) xếp hạng {orig + 1} với RMSE {f2(o.rmse)} lượt thuê/giờ, cao hơn {100 * (o.rmse / best.rmse - 1):.2f}%. "
           f"Hai cách đo cho thứ tự khác nhau: nhóm dùng log(1 + cnt) có MAE kiểm định thấp nhất {f2(sel[sel.target == 'log'].mae.min())} lượt thuê/giờ, nhóm dùng cnt là {f2(sel[sel.target == 'cnt'].mae.min())} lượt thuê/giờ, nhưng RMSE thì ngược lại "
           f"({f2(sel[sel.target == 'log'].rmse.min())} so với {f2(sel[sel.target == 'cnt'].rmse.min())} lượt thuê/giờ). "
           "RMSE được chọn làm tiêu chí vì nó phạt nặng sai số ở các giờ cao điểm và là đại lượng OLS giảm thiểu trên thang gốc khi biến mục tiêu là `cnt`.")

    # ---- 6.6
    with t66:
        st.markdown("**Kết quả chính**")
        st.markdown(f"- Chia dữ liệu: huấn luyện {len(tr):,} dòng ({tr.dteday.min().date()} đến {tr.dteday.max().date()}), kiểm định {len(va):,} dòng ({va.dteday.min().date()} đến {va.dteday.max().date()}), kiểm tra {len(te):,} dòng ({te.dteday.min().date()} đến {te.dteday.max().date()}).\n"
                    f"- Cấu hình được chọn trên tập kiểm định: K = {cfg['K']}, biến mục tiêu {'log(1 + cnt)' if cfg['target'] == 'log' else 'cnt'}, xu hướng `{cfg['trend']}`, mã hóa tháng/mùa `{cfg['month']}`, {m['k']} biến độc lập.\n"
                    f"- Trên tập kiểm tra: R² = {f4(me['r2'])}, Adjusted R² = {f4(me['adj'])}, MAE = {f2(me['mae'])} lượt thuê/giờ, RMSE = {f2(me['rmse'])} lượt thuê/giờ; trên tập kiểm định: R² = {f4(rv['m_te']['r2'])}, RMSE = {f2(rv['m_te']['rmse'])} lượt thuê/giờ.\n"
                    f"- Mô hình cơ sở (dự đoán bằng trung bình huấn luyện): RMSE = {f2(mb['rmse'])} lượt thuê/giờ trên tập kiểm tra.")
        st.markdown("**Hạn chế**")
        st.markdown("- Mô hình tuyến tính cộng tính theo các biến; ảnh hưởng của thời tiết được giả định như nhau ở mọi giờ và mọi mùa (chưa có tương tác thời tiết × giờ).\n"
                    "- Biến xu hướng (bước nhảy `yr` hoặc tuyến tính theo thời gian) là dạng đơn giản; tỷ lệ tăng so với cùng kỳ năm trước thay đổi theo tháng nên sai số có thể lệch theo từng giai đoạn (xem Hình 6.6).\n"
                    "- Dữ liệu theo giờ liên tiếp nên phần dư tự tương quan; sai số chuẩn và p-value của hệ số chỉ mang tính tham khảo.\n"
                    "- Chỉ có hai năm dữ liệu từ một hệ thống, nên khó kiểm chứng mùa vụ lặp lại ổn định và xu hướng ngoài phạm vi 2012.\n"
                    "- Dữ liệu thiếu 165 khung giờ (không có lượt thuê nên không có dòng); mô hình không dùng giá trị trễ nên không bị ảnh hưởng trực tiếp.\n"
                    "- Các biến thời tiết là giá trị chuẩn hóa nên hệ số diễn giải theo đơn vị chuẩn hóa, chưa quy về °C hay km/h.\n"
                    f"- Thứ hạng cấu hình {'khá ổn định' if stats.spearmanr(sel.rmse, sel.rmse_te)[0] > 0.5 else 'không ổn định'} giữa tập kiểm định và tập kiểm tra: hệ số tương quan hạng Spearman của RMSE qua {len(sel)} cấu hình là {stats.spearmanr(sel.rmse, sel.rmse_te)[0]:.4f} ({'p < 0.001' if stats.spearmanr(sel.rmse, sel.rmse_te)[1] < 0.001 else 'p = ' + format(stats.spearmanr(sel.rmse, sel.rmse_te)[1], '.4f')}). "
                    f"RMSE trung bình của nhóm log(1 + cnt) là {sel[sel.target == 'log'].rmse.mean():.2f} ở tập kiểm định và {sel[sel.target == 'log'].rmse_te.mean():.2f} ở tập kiểm tra; của nhóm cnt là {sel[sel.target == 'cnt'].rmse.mean():.2f} và {sel[sel.target == 'cnt'].rmse_te.mean():.2f} lượt thuê/giờ. "
                    "Phép so sánh này chỉ dùng để chẩn đoán độ ổn định, không dùng để chọn lại cấu hình.\n"
                    "- Cấu hình được chọn trên tập kiểm định có khoảng 3,000 dòng với phần dư tự tương quan, nên việc chọn từ nhiều cấu hình có thể làm RMSE kiểm định lạc quan; tập kiểm tra là thước đo độc lập hơn. Mô hình chỉ được huấn luyện trên dữ liệu đến hết ngày cắt; nếu huấn luyện lại trên cả tập kiểm định rồi đánh giá trên tập kiểm tra, các ngày kiểm tra nằm xen giữa các ngày huấn luyện và chỉ số sẽ lạc quan.\n"
                    + {MODES[0]: "- Tập kiểm định và tập kiểm tra thuộc hai giai đoạn khác nhau của năm, nên chênh lệch giữa hai tập phản ánh cả mùa vụ lẫn chất lượng mô hình.",
                       MODES[1]: f"- Việc trộn theo ngày dùng SEED = {SEED}; đổi SEED làm đổi các ngày thuộc từng tập nên có thể đổi cấu hình tốt nhất theo RMSE kiểm định.",
                       MODES[2]: f"- Việc trộn theo từng dòng dùng SEED = {SEED}; đổi SEED có thể đổi cấu hình tốt nhất theo RMSE kiểm định, và các giờ liền kề nằm ở cả hai tập nên hai tập không độc lập hoàn toàn."}[cfg["split_mode"]])


main()
