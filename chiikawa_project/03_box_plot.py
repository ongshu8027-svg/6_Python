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

# 5. Figure, Axes 객체를 이용한 박스 플롯 시각화
fig, ax = plt.subplots(figsize=(11, 6))

# 박스 플롯 그리기
sns.boxplot(
    data=df, 
    x='platform', 
    y='avg_rating', 
    palette='Pastel1',
    ax=ax,
    boxprops=dict(alpha=0.8)
)

# 데이터의 실제 분포를 더 직관적으로 보기 위해 개별 데이터 포인트(stripplot) 겹치기
sns.stripplot(
    data=df, 
    x='platform', 
    y='avg_rating', 
    color='black', 
    alpha=0.4, 
    jitter=0.2, 
    size=5,
    ax=ax
)

# 필수 서식 설정
ax.set_title('판매 채널별 상품 평점 분포 비교', fontsize=14, fontweight='bold')
ax.set_xlabel('판매 채널', fontsize=12)
ax.set_ylabel('평점', fontsize=12)
ax.grid(axis='y', linestyle='--', alpha=0.5)

fig.tight_layout()

# 6. output 폴더에 이미지 파일로 저장
fig.savefig('output/03_box_plot.png', dpi=120)
plt.close(fig)

print("성공! 'output/03_box_plot.png' 파일로 박스 플롯 차트가 저장되었습니다.")