import time
import pyupbit
import datetime
import pandas as pd
from pytz import timezone

access = "tUEL0zGCpDf7NgD7x9OuqxtCa2fNISIS9Jg19aQ2"
secret = "Ce8ZwkPqv4Cs0Qti7a6FybxoD42AwEmPxxUqutew"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    df.index = df.index.tz_localize(None) # 엑셀에서 지원하지 않은 tz 제거
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return float(target_price)

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
                return float(b['balance']), float(b['avg_buy_price'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return float(pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"])

# 로그인
upbit = pyupbit.Upbit(access, secret)

# 원하는 코인 티커 입력
tc_name = "KRW-KNC"

# coin = get_balance(tc_name.split("-")[1])[0]
# avg_price = get_balance(tc_name.split("-")[1])[1]
# krw = get_balance(tc_name.split("-")[0])[0]
# print(krw)
# print(coin, avg_price)

# print(get_target_price(tc_name, 0.5), get_start_time(tc_name), get_start_time(tc_name) + datetime.timedelta(minutes=5),
#       get_balance(tc_name), get_current_price(tc_name)*0.98, datetime.datetime.now())
# print("----------------------------------------")
# print(get_balance(tc_name.split("-")[1])['avg_buy_price'] * get_balance(tc_name.split("-")[1])['balance'])
# print(get_balance(tc_name.split("-")[0]))
# print(get_balance(tc_name.split("-")[1]))

print("autotrade start")

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
                krw = get_balance(tc_name.split("-")[0])[0]
                if krw > 5000.0:
                    upbit.buy_market_order(tc_name, krw*0.9995)
                    print("buy now!!!")
                    coin = get_balance(tc_name.split("-")[1])[0]
                    avg_price = get_balance(tc_name.split("-")[1])[1]
                    if avg_price > current_price*1.15:
                        upbit.sell_market_order(tc_name, coin*0.9995)
                        print("gae-e-duck!!!")
                    if avg_price < current_price*0.92:
                        upbit.sell_market_order(tc_name, coin*0.9995)
                        print("dom hwang cha!!!")
        else:
            coin = get_balance(tc_name.split("-")[1])[0]
            avg_price = get_balance(tc_name.split("-")[1])[1]
            if coin*avg_price > 5000.0:
                upbit.sell_market_order(tc_name, coin*0.9995)
                print("time done : sell now!!!")
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)