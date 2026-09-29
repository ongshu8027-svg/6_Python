import numpy as np
import pandas as pd

# 1. 가상 데이터셋 설정 (약 250행)
np.random.seed(42)
n_rows = 250

dates = pd.date_range(start='2026-01-01', periods=n_rows, freq='D')

# 원작 반영 캐릭터 리스트 (우사기 인기도를 가장 높게 설정)
characters = ['치이카와', '하치와레', '우사기', '모몽가', '카니', '시사', '랏코', '쿠리만쥬']
# 확률 가중치: 우사기(0.30)가 가장 높고, 치이카와/하치와레가 그 뒤를 잇도록 설정
character_probs = [0.25, 0.20, 0.30, 0.05, 0.05, 0.05, 0.05, 0.05]

platforms = ['공식 온라인몰', '팝업스토어', '네이버 스마트스토어', '오프라인 편집숍']

data = {
    'date': np.random.choice(dates, n_rows),
    'character_name': np.random.choice(characters, n_rows, p=character_probs),
    'platform': np.random.choice(platforms, n_rows, p=[0.4, 0.3, 0.2, 0.1]),
    'search_volume': np.random.randint(1000, 50000, n_rows),
    'mention_count': np.random.randint(500, 10000, n_rows),
    'avg_rating': np.round(np.random.uniform(3.5, 5.0, n_rows), 2),
    'sales_amount': np.random.randint(500000, 15000000, n_rows)
}

df = pd.DataFrame(data)

# 2. 결측치(NaN) 및 이상치(Outlier) 주입
nan_idx_1 = np.random.choice(df.index, size=12, replace=False)
nan_idx_2 = np.random.choice(df.index, size=10, replace=False)
df.loc[nan_idx_1, 'search_volume'] = np.nan
df.loc[nan_idx_2, 'avg_rating'] = np.nan

df.loc[15, 'sales_amount'] = 99999999  
df.loc[42, 'search_volume'] = 500000  

# 3. CSV 파일로 저장
df.to_csv('business_data.csv', index=False, encoding='utf-8-sig')
print("성공! 치이카와 캐릭터 라인업이 반영된 'business_data.csv' 파일이 생성되었습니다.")