import pyupbit

# api 입력
access = "nF2JmnhmkfXRtRUcrAn01Vbor5wA92bwz5OdeM0Y"          # 본인 값으로 변경
secret = "zXSwglcGbxSu70ZH1tuFJxj9lxf0NaqxN856cgDG"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

# 잔고 조회 
print(upbit.get_balance("KRW-MATIC"))     # KRW-XRP 조회
print(upbit.get_balance("KRW-KNC"))         # 보유 현금 조회
