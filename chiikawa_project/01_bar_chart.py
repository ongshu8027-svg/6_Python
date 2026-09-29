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

# 4. 데이터 로드 (loader.py로 생성한 CSV 읽기)
df = pd.read_csv('business_data.csv')

# 5. 데이터 정합성 확인 (결측치 현황 출력)
print("[결측치 현황]")
print(df.isnull().sum())

# 6. 전처리: 결측치가 포함된 행 일시 제외 후 캐릭터별 총 매출액 집계
df_clean = df.dropna(subset=['search_volume', 'avg_rating']).copy()
char_sales = df_clean.groupby('character_name')['sales_amount'].sum().reset_index()

# 7. Figure, Axes 객체를 이용한 바 차트 시각화
fig, ax = plt.subplots(figsize=(12, 6))

sns.barplot(
    data=char_sales, 
    x='character_name', 
    y='sales_amount', 
    palette='Set2',
    ax=ax
)

# 필수 서식 설정
ax.set_title('치이카와 캐릭터별 총 매출액 현황', fontsize=14, fontweight='bold')
ax.set_xlabel('캐릭터 이름', fontsize=12)
ax.set_ylabel('총 매출액', fontsize=12)
ax.tick_params(axis='x', rotation=30)
ax.grid(axis='y', alpha=0.3)

fig.tight_layout()

# 8. 화면에 띄우는 대신 output 폴더에 이미지 파일로 저장
fig.savefig('output/01_bar_chart.png', dpi=120)
plt.close(fig)

print("성공! 'output/01_bar_chart.png' 파일로 차트가 저장되었습니다.")