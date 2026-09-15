"""
    공통 파서 모음
"""
import re
import bs4
from bs4 import BeautifulSoup
from config import BASE
from urllib.parse import urljoin

# 텍스트 추출
def get_text(node, selector, default=""):
    tag = node.select_one(selector)
    return tag.get_text(strip=True) if tag else default

# 속성 추출 (urljoin 옵션 추가 선택지 고려)
def get_attr(node, selector, attr, default="", base_url=None):
    tag = node.select_one(selector)
    if not tag:
        return default
    val = tag.get(attr, default)
    if val and base_url and attr in ("href", "src"):
        return urljoin(base_url, val)
    return val

# 숫자 추출
def get_number(node, selector, default=0):
    text = get_text(node, selector)
    numbers = re.sub(r"[^\d]", "", text)
    return int(numbers) if numbers else default

# 실수 추출 (유니코드 마이너스 ⁻/− 대응 포함)
def parse_rate(text, default=None):
    if not text:
        return default
    cleaned = text.replace(",", "").replace("−", "-").replace("＋", "+")
    m = re.search(r"[-+]?\d*\.?\d+", cleaned)
    try:
        val = float(m.group()) if (m and m.group() not in ("", "-", "+", ".")) else default
        return val
    except ValueError:
        return default

# stock 목록 파서
def parse_stocks(html):
    soup = BeautifulSoup(html, 'html.parser')

    results = []
    for row in soup.select("tr.stock-row"):
        results.append(
            {
                "code": get_text(row, "td.col-code"),
                "name": get_text(row, "td.col-name a") or get_text(row, "td.col-name"),
                "sector": get_text(row, "td.col-sector"),
                "price": get_number(row, "td.col-price"),
                "rate": parse_rate(get_text(row, "td.col-change")),
                "volume": get_number(row, "td.col-volume"),
                "market": get_text(row, "td.col-market span"),
                "link": get_attr(row, "td.col-name a", "href", base_url=BASE),
            }
        )
    return results