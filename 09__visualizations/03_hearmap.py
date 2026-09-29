import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from chart_config import setup, out
from merged_loader import load_merged

setup()

df = load_merged()

df["ret"] = df.groupby("code")["close"].transform(lambda s: s.pct_change())

pivot = df.pivot_table(index="date", columns="code", values="ret")

order = df[["code", "sector"]].drop_duplicates().sort_values(["sector", "code"])["code"].tolist()
pivot = pivot[order]

corr = pivot.corr()
print(f"pivot : {pivot.shape} (행=날짜, 열=종목)")
print(f"corr : {corr.shape} (종목*종목, 상관계수)")

# 첫 번째 단독 히트맵
fig, ax = plt.subplots(figsize=(9, 7.5))
sns.heatmap(corr, cmap="coolwarm", center=0, vmin=-1, vmax=1,
            xticklabels=False, yticklabels=False, ax=ax)

ax.set_title("종목간 수익률 상관(섹터순 정렬)")
fig.savefig(out("08_heatmap.png"), dpi=120)
plt.close(fig)


fig, axes = plt.subplots(1, 2, figsize=(13.5, 5))

sns.heatmap(corr, cmap="coolwarm", xticklabels=False, yticklabels=False, ax=axes[0])
axes[0].set_title("center 미지정")

sns.heatmap(corr, cmap="coolwarm", center=0, vmin=-1, vmax=1,
            xticklabels=False, yticklabels=False, ax=axes[1])
axes[1].set_title("center=0, vmin/vmax")  

fig.tight_layout()
fig.savefig(out("09_center.png"), dpi=120)
plt.close(fig)

import numpy as np

# 1. 섹터 매핑 딕셔너리(시리즈) 생성
sector_of = df[["code", "sector"]].drop_duplicates().set_index("code")["sector"]
codes = corr.columns
same, diff = [], []

# 2. 이중 반복문으로 상관계수 분류
for i in range(len(codes)):  # code -> codes 로 수정
    for j in range(i + 1, len(codes)):
        v = corr.iloc[i, j]

        # code[i] -> codes[i] 로 수정
        if sector_of[codes[i]] == sector_of[codes[j]]:
            same.append(v)
        else:
            diff.append(v)

# 3. f-string 문법 오류 수정 및 출력 포맷 정리
print(f"같은 섹터 쌍 : {len(same)}개, 평균 상관계수: {np.mean(same):.4f}")
print(f"다른 섹터 쌍 : {len(diff)}개, 평균 상관계수: {np.mean(diff):.4f}")
