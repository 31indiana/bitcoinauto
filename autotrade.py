import time
import pyupbit
import datetime

access = "myaccessmycodemyaccessmycodemyaccessmycode"
secret = "mysecretmycodemysecretmycodemysecretmycode"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
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

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()     #현재시간
        start_time = get_start_time("KRW-BTC")    #시작시간(오전9시로 설정)
        end_time = start_time + datetime.timedelta(days=1)   #끝나는 시간  오전9시 + 1일 = 다음날 오전 9시

        # 09:00:00 am < 현재 < 다음날 8:59:50 am
        if start_time < now < end_time - datetime.timedelta(seconds=10):  
            target_price = get_target_price("KRW-DOT", 0.5)   #새로운 전략의 경우 target_price를 구하는 코드를 수정하라.
            current_price = get_current_price("KRW-DOT")
            if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 5000:  #최소주문금액 5000원 기준
                    upbit.buy_market_order("KRW-DOT", krw*0.9995)    #수수료 0.05% 
        
        #당일종가에 코인을 전량매도하는 명령
        #다음날 8:59:50 am ~ 9:00:00 am : 10초 동안 코인 전량 매도
        else:
            btc = get_balance("DOT")     #현재 보유중인 btc잔고 가져옴
            if btc > 0.00008:    #현재 잔고가 5000원 이상이면 (0.00008 BTC=5000원이라는 것은 유동적임)
                upbit.sell_market_order("KRW-DOT", btc*0.9995)  #수수료 0.05% 고려한 99.5%만 매도하라는 명령)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
