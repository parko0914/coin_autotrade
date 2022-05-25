import time
import pyupbit
import datetime

access = "nF2JmnhmkfXRtRUcrAn01Vbor5wA92bwz5OdeM0Y"
secret = "zXSwglcGbxSu70ZH1tuFJxj9lxf0NaqxN856cgDG"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    df.index = df.index.tz_localize(None) # 엑셀에서 지원하지 않은 tz 제거
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    df.index = df.index.tz_localize(None) # 엑셀에서 지원하지 않은 tz 제거
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

tc_name = "KRW-KNC"
# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time(tc_name)
        end_time = start_time + datetime.timedelta(days=1)
        # 9:00 < 현재 < 8:59:50 
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price(tc_name, 0.5)
            current_price = get_current_price(tc_name)
            if target_price < current_price:
                krw = get_balance(tc_name)
                if krw > 5000:
                    upbit.buy_market_order(tc_name, krw*0.9995)
        else:
            btc = get_balance(tc_name)
            if btc > 0.00008:
                upbit.sell_market_order(tc_name, btc*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)