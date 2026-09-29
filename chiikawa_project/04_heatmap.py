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

# --- [수정] 이상치 및 결측치 전처리 ---
# 1) 9,999만 원 같은 극단적 이상치 매출 제거
# 2) 필수 분석 컬럼의 결측치 제거
df_clean = df[df['sales_amount'] < 50000000].dropna(subset=['search_volume', 'avg_rating']).copy()

# 5. 피벗 테이블 생성 (캐릭터 x 플랫폼 평균 매출 집계)
pivot_df = df_clean.pivot_table(
    index='character_name', 
    columns='platform', 
    values='sales_amount', 
    aggfunc='mean'
)

# 6. Figure, Axes 객체를 이용한 히트맵 시각화
fig, ax = plt.subplots(figsize=(10, 8))

sns.heatmap(
    pivot_df, 
    annot=True,          # 셀 안에 실제 숫자 값 표시
    fmt=',.0f',          # 천 단위 콤마가 포함된 정수형 포맷
    cmap='YlGnBu',       # 시인성이 좋은 컬러 맵
    linewidths=.5,       # 셀 간격 선 두께
    ax=ax
)

# 필수 서식 설정
ax.set_title('치이카와 캐릭터 및 판매 채널별 평균 매출 히트맵 (이상치 제외)', fontsize=14, fontweight='bold')
ax.set_xlabel('판매 채널', fontsize=12)
ax.set_ylabel('캐릭터 이름', fontsize=12)
ax.tick_params(axis='x', rotation=30)

fig.tight_layout()

# 7. output 폴더에 이미지 파일로 저장
fig.savefig('output/04_heatmap.png', dpi=120)
plt.close(fig)

print("성공! 'output/04_heatmap.png' 파일로 히트맵 차트가 저장되었습니다.")