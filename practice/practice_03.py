"""
    실습용 사이트에서
        종목 메뉴 페이지(SSR)의 섹터를 "IT 서비스"로 검색한 결과 데이터를 추출

    - 요청 주소: ??
    TODO: 오늘(09/15) 18시까지 이메일로 제출
"""
import csv
import json
import requests
from bs4 import BeautifulSoup
from config import BASE, HEADERS, TIMEOUT
from parsers import parse_stocks

# SSR 방식이므로 requests 사용 + S08 섹터 파라미터
url = f"{BASE}/stocks"
params = {"sector": "S08"}

resp = requests.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)
resp.raise_for_status()

# 파싱 (14개 데이터 수집)
stocks = parse_stocks(resp.text)
print(f"수집된 종목수: {len(stocks)}개")

# JSON/CSV 저장
with open("stocks_it_service.json", "w", encoding="utf-8") as f:
  json.dump(stocks, f, ensure_ascii=False, indent=2)

if stocks:
  with open("stocks_it_service.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=stocks[0].keys())
    writer.writeheader()
    writer.writerows(stocks)