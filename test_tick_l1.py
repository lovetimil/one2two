# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from xtquant import xtdata
import  pandas as pd
import akshare as ak
from datetime import  datetime,timedelta

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    a="000001.SZ"
    print(dir(xtdata))
    typ = "1m"
    codes=["603042.SZ","000002.SZ"]

    now= datetime.now()

    month = (now.month - 1) - (now.month - 1) % 3 + 1

    this_quarter_start = datetime(now.year, month, 1)

    this_quarter_end = datetime(now.year, month + 3, 1) - timedelta(days=1)

    pass
    # stock_gdfx_free_top_10_em_df = ak.stock_gdfx_free_top_10_em(symbol="sz000002", date="20230331")
    # # stock_gdfx_free_top_10_em_df = ak.stock_gdfx_free_top_10_em()
    # print(stock_gdfx_free_top_10_em_df)
    #
    #
    # stock_individual_info_em_df = ak.stock_individual_info_em(symbol="000002")
    # print(stock_individual_info_em_df)
    # negotiable_value = stock_individual_info_em_df.iloc[1,1]
    # negotiable_volume=stock_individual_info_em_df.iloc[7,1]



    xtdata.download_history_data2(codes,period=typ,start_time='20230530',end_time='20230530')
    data = xtdata.get_market_data(field_list=[],stock_list=codes,period=typ,count=-1)
    xtdata.get_financial_data
    print("data",data)
    #df = pd.DataFrame(data)
    print(df.iloc[-1])
