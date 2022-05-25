import pyupbit
import numpy as np
import pandas as pd
from pytz import timezone
from datetime import datetime

# OHLCV(open, high, low, close, volume)로 당일 시가, 고가, 저가, 종가, 거래량에 대한 데이터
df = pyupbit.get_ohlcv("KRW-MATIC", count = 7)
df.index = df.index.tz_localize(None) # 엑셀에서 지원하지 않은 tz 제거

# 변동폭 * k 계산, (고가 - 저가) * k값
df['range'] = (df['high'] - df['low']) * 0.5

# target(매수가), range 컬럼을 한 칸씩 밑으로 내림(.shift(1))
df['target'] = df['open'] + df['range'].shift(1)

# ror(수익율), np.where(조건문, 참일 때 값, 거짓일 때 값)
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'],
                     1)

# 누적 곱 계산(cumprod) -> 누적 수익률
df['hpr'] = df['ror'].cumprod()

# draw down 계산 (누적 최대 값과 현재 hpr 차이 / 누적 최대값 * 100)
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

# MDD 계산 
print("MDD(%): ", df['dd'].max())

df.to_excel("dd.xlsx")