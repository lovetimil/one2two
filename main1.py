# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from xtquant import xtdata
import  pandas as pd
import akshare as ak
from datetime import  datetime,timedelta

from CodeInfos import Codeinfos


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    a="000001.SZ"
    print(dir(xtdata))
    typ = "tick"
    codes=["603042.SH"]

    codes = [Codeinfos("603042.SH")]
    cs = codes[0]
    code = cs.code

    xtdata.download_history_data2([code],period=typ,start_time='20230630',end_time='20230630')
    data = xtdata.get_market_data(field_list=[],stock_list=[code],period=typ,count=-1)

    code_data = data[code]
    up_price = cs.UpStopPrice
    for ele in code_data:
        tims = ele[0] // 1000
        dt = datetime.fromtimestamp(tims)
        open_price = ele[2]
        # new_price = max(ask_price[0],bid_price[0])
        new_price = ele[1]
        ask_prices = ele[12]
        bid_prices = ele[13]
        ask_vol = ele[14]
        bid_vol = ele[15]
        print("now",datetime.fromtimestamp(tims),"new_price:", new_price, "up_price:", up_price,
               'ask_price',ask_prices,  'bid_price',bid_prices,"ask_vol",ask_vol,"bid_vol",bid_vol)

    # print("data",data)
    #df = pd.DataFrame(data)
