import matplotlib
# 1. 화면 창을 띄우지 않고 파일로 저장하기 위한 Agg 백엔드 설정 (pyplot 임포트 전 필수)
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import platform
import os

# 2. 출력 디렉토리 생성 (이미지 저장용)
os.makedirs("output", exist_ok=True)

# 3. 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':
    plt.rc('font', family='AppleGothic')
else:
    plt.rc('font', family='NanumGothic')

plt.rcParams['axes.unicode_minus'] = False

# 4. 데이터 로드 (business_data.csv 읽기)
df = pd.read_csv('business_data.csv')

# --- [수정] 이상치 필터링 추가 ---
# 시각화의 가독성을 해치는 극단적인 이상치(매출 5천만 원 초과 또는 검색량 10만 초과)를 제거합니다.
df_clean = df[(df['search_volume'] < 100000) & (df['sales_amount'] < 50000000)].copy()

# 5. Figure, Axes 객체를 이용한 산점도 시각화 (df_clean 사용)
fig, ax = plt.subplots(figsize=(12, 7))

sns.scatterplot(
    data=df_clean, 
    x='search_volume', 
    y='sales_amount', 
    hue='platform',        # 판매 채널별 색상 구분
    style='platform',      # 마커 모양도 함께 구분
    s=90,                    # 마커 크기
    alpha=0.8,               # 투명도 조절
    ax=ax
)

# 필수 서식 설정
ax.set_title('치이카와 검색량 vs 매출액 상관관계 및 이상치 탐색 (이상치 제외)', fontsize=14, fontweight='bold')
ax.set_xlabel('일간 검색량 ', fontsize=12)
ax.set_ylabel('매출액 ', fontsize=12)
ax.grid(True, linestyle='--', alpha=0.5)

# 범례 위치 조정
plt.legend(title='판매 채널', bbox_to_anchor=(1.05, 1), loc='upper left')

fig.tight_layout()

# 6. output 폴더에 이미지 파일로 저장
fig.savefig('output/02_scatter_plot.png', dpi=120)
plt.close(fig)

print("성공! 'output/02_scatter_plot.png' 파일로 산점도 차트가 저장되었습니다.")