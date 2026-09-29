"""
    Matplotlib 으로 차트 생성
"""
import matplotlib

matplotlib.use("Agg")
# Agg (Anti-Grain Geometry)
# : 화면(GUI 창)을 열지 않고, 메모리 내에서만 차트 표시(렌더링)
#   화면에 따로 출력하지 않고 파일로 저장할 때 설정
# * pyplot 임포트 하기전에 설정해야 함!
import matplotlib.pyplot as plt

from chart_config import setup, out
from merged_loader import load_merged

setup()
df = load_merged()

one = df[df["code"] == "G0001"].sort_values("date")

# Figure, Axes
#   - Figure (도화지)  -> Axes (그래프 하나)

# * subplots(행, 열, figsize=(가로,세로))
#   행, 열 생략 시 1 * 1

fig, ax = plt.subplots(figsize=(12,4))
#  figsize => 12*4.   dpi(100) --> 1200 * 400 픽셀.

# ax.plot(x, y)
ax.plot(one['date'], one['close'])

ax.set_title("가온전자 주가 추이")
ax.set_xlabel("날짜")
ax.set_ylabel("종가(원)")
ax.grid(alpha=0.3)

fig.savefig(out('01_basic.png'))
#plt.show()
#=>화면에 띄워서 바로 차트를 확인
#   savefig()와 show() 같이 사용하는 경우, savefig() 호출 후 show() 호출해야함
fig, ax = plt.subplots(figsize=(10, 3))
ax.plot(one["date"].iloc[:60], one['changeRate'].iloc[:60], marker=".")
ax.axhline(0, color="gray", lw=0.8)
ax.set_title("가온전자 일간 등락률")
ax.set_ylabel("등락률(%)")
fig.savefig(out('02_minus.png'), dpi=120)

plt.close(fig)

"""
    * 필수 설정 항목 (최소한 이것들을 설정하자!)

    ax.set_title("그래프제목")
    ax.set_xladel("x축 제목")
    ax.set_yladel("y축 제목")
    ax.grid(alpha=0.3)
    ax.legend()
"""

#그래프 여러게 표시

codes = ["G0001", "G0002", "G0003", "G0004"]
fig, axes = plt.subplots(2, 2, figsize=(13, 6), sharex=True)

for ax, code in zip(axes.flat, codes):
    # 2차원 배열을 1차원으로 펼쳐서 순회
    data = df[df["code"] == code].sort_values("date")

    # lx=1 -> lw=1 (linewidth)로 수정
    ax.plot(data["date"], data["close"], lw=1)
    ax.set_title(f"{data['name'].iloc[0]}({code})", fontsize=10)
    ax.grid(alpha=0.3)

fig.suptitle("종목별 주가 추이")
fig.tight_layout()

fig.savefig(out("03_subplots.png"), dpi=120)
plt.close(fig)

