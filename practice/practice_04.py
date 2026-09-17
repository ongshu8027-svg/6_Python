"""
    Numpy 연습문제
"""

# =========== 이곳에 필요한 모듈 import 한 후 실행 ===========
import numpy as np
from load_utils import load_one_stock, load_dates, load_matrix

"""
    1. 다음 리스트 [1, 2, 3, 4, 5]를 ndarray로 변환하고, 배열의 차원(ndim)과 형태(shape)을 출력하시오.
"""
arr1 = np.array([1, 2, 3, 4, 5])
print(arr1.ndim)
print(arr1.shape)


"""
    2. np.arange()를 이용해 0부터 20까지의 짝수로 이루어진 배열을 생성하시오.
"""
arr2 = np.arange(0, 21, 2)
print(arr2)


"""
    3. 다음 제시된 배열에서, 3 이상인 값만 추출하는 불리언 인덱싱 코드를 작성하시오.
"""
arr3 = np.array([1, 3, 5, 2, 4])
result3 = arr3[arr3 >= 3]
print(result3)


"""
    4. 다음 제시된 리스트를 배열로 변환한 후, 두 번째 행만 슬라이싱하여 출력하시오.
"""
list4 = [[10, 20, 30], [40, 50, 60], [70, 80, 90]]
arr4 = np.array(list4)
print(arr4[1])


"""
    5. 다음 제시된 리스트를 배열로 변환한 후, 모든 홀수에만 10을 더하는 벡터화 연산을 수행하시오.
"""
list5 = [1, 2, 3, 4, 5]
arr5 = np.array(list5)
arr5[arr5 % 2 == 1] += 10
print(arr5)


"""
    6. 다음 제시된 실수 리스트를 배열로 변환한 후, 반올림한 정수형 배열로 변환하시오.
        주의 : astype 만 쓰면 소수점 아래가 버려져서 값이 새어나간다.

        [출력 예시]
            np.array([52000.9, -3.7]) -> [52001, -4]

        [힌트] 반올림을 먼저 하고 타입을 바꾼다. 순서가 중요하다.
"""
list6 = [52000.9, 51999.2, -3.7, 52000.5]
arr6 = np.array(list6)
result6 = np.round(arr6).astype(int)
print(result6)


# =========== 아래 문제들은 실습용 데이터(prices.csv, load_utils.py)를 활용하여 풀이해보세요. ===========
"""
    7. 첫 종목의 종가 데이터를 기준으로 최저가, 최고가와 그에 해당하는 날짜를 각각 출력하시오. 
       (실습용 데이터의 prices 와 dates 는 길이와 순서가 같다.)

        [출력 예시]
            (25899, numpy.datetime64('2023-10-16'), 8885, numpy.datetime64('2026-05-21'))

        [힌트] max 는 '값', argmax 는 '그 값이 있는 위치' 다.
              위치를 얻으면 길이가 같은 다른 배열에서 같은 자리를 꺼낼 수 있다.
"""
first_stock = load_one_stock(0)   # 첫 종목 종가 (750,)
dates = load_dates()              # 날짜 (750,)

min_idx = np.argmin(first_stock)
max_idx = np.argmax(first_stock)

print(first_stock[min_idx], dates[min_idx], first_stock[max_idx], dates[max_idx])


"""
    8. 종가 데이터를 기준으로 각 종목별 평균가와, 날짜별 평균가를 구하시오. 
       또한, 각 종목에서 자기 평균을 뺀 배열을 구하시오.
       
       [힌트]
       - 종목별 평균가 : (종목 수,) 배열 
       
       - 날짜별 평균가 : (날짜 수,) 배열
       
       - 각 종목에서 자기 평균을 뺀 배열 : (종목 수, 날짜 수) 배열 
         결과의 종목별 평균은 0 이 되어야 한다.
"""
prices = load_matrix()            # (120, 750) - 행: 종목, 열: 날짜

stock_mean = prices.mean(axis=1)  # 종목별 평균 -> (120,)
date_mean = prices.mean(axis=0)   # 날짜별 평균 -> (750,)
centered = prices - stock_mean.reshape(-1, 1)

print(stock_mean)
print(date_mean)
print(centered.mean(axis=1))      