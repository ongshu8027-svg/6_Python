"""
    실습용 사이트에서
        종목 메뉴 페이지(SSR)의 섹터를 "IT 서비스"로 검색한 결과 데이터를 추출

    - 요청 주소: https://kh-lab.rockua.ai.kr/stocks?sector=S08
    TODO: 오늘(09/15) 18시까지 이메일로 제출
"""
import csv
import json
import requests
from config import BASE, HEADERS, TIMEOUT
from parsers import parse_stocks

# 1. 요청
url = f"{BASE}/stocks"
params = {"sector": "S08"}

resp = requests.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)
resp.raise_for_status()

# 2. 파싱 (SSR 응답 HTML 파싱)
all_stocks = parse_stocks(resp.text)

print(f"수집된 IT서비스 종목 수: {len(all_stocks)}개")
for s in all_stocks:
    print(f"[{s['code']}] {s['name']} | 섹터: {s['sector']} | 현재가: {s['price']}")

# 2-1. 검증:IT서비스 섹터인지 확인
wrong = [s for s in all_stocks if s['sector'] != 'IT서비스']
if wrong:
    print(f"경고: 섹터 불일치 {len(wrong)}건 발견")
    for w in wrong:
        print(f"  -> [{w['code']}] {w['name']} : {w['sector']}")

# 3. 파일 저장
output_json = "stocks_it_service.json"
output_csv = "stocks_it_service.csv"

with open(output_json, "w", encoding="utf-8") as f:
    json.dump(all_stocks, f, ensure_ascii=False, indent=2)

if all_stocks:
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_stocks[0].keys())
        writer.writeheader()
        writer.writerows(all_stocks)

print(f"저장 완료: {output_json}, {output_csv} (총 {len(all_stocks)}개)")