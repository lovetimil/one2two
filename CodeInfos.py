
import akshare as ak
from xtquant import xtdata
from datetime import datetime ,timedelta
from dateutil.relativedelta import relativedelta


class Codeinfos(object):

    y = 100000000
    w_hands = 100000000
    def __init__(self,code):
        self.code = code
        self.ak_code = Codeinfos.convert2_ak_code(code)
        self.ExchangeID= None
        self.InstrumentID = None
        self.InstrumentName = None
        self.ProductID = None
        self.CreateDate = None
        self.OpenDate = None
        self.ExpireDate = None
        self.PreClose = None
        self.SettlementPrice = None
        self.UpStopPrice = None
        self.DownStopPrice = None
        self.FloatVolume = None  #流通市值
        self.TotalVolume = None #总股：本用akshare数据
        self.TotalValue = None #总市值：用akshare
        self.LongMarginRatio =None
        self.ShortMarginRatio = None
        self.PriceTick = None
        self.VolumeMultiple = None
        self.MainContract = None
        self.LastVolume = None
        self.InstrumentStatus = None
        self.IsTrading = None
        self.IsRecent = None

        self.FloatVolume = None  #实际流通股  akshare

        self.score_dict  =dict()

        self.stock_gdfx_free_top_10_em_df = None
        self.real_FloatVolume= 0
        self.real_FloatValue = 0

        self.fresh()


    def convert_human_view(self):
        self.TotalValue_hv=self.TotalValue/Codeinfos.y
        self.TotalVolume_hv  =self.TotalVolume/Codeinfos.w_hands
        self.FloatVolume_hv = self.FloatVolume/Codeinfos.w_hands
        self.LastVolume_hv =self.LastVolume/Codeinfos.w_hands
        self.real_FloatValue_hv = self.real_FloatValue/Codeinfos.y
        self.real_FloatVolume_hv = self.real_FloatVolume/Codeinfos.w_hands

    def fresh(self):
        self.get_negotiable()
        self.get_infos()
        # self.get_free_top_10_em()
        # self.get_real_FloatVolumeAndValue()
        self.convert_human_view()

    def get_real_FloatVolumeAndValue(self):
        if self.stock_gdfx_free_top_10_em_df is None:self.get_free_top_10_em()
        df = self.stock_gdfx_free_top_10_em_df
        df_above_5 = df.where(cond=df['占总流通股本持股比例'] > 4.999999).dropna(subset=['占总流通股本持股比例'])

        real_float_ratio = 1- df_above_5['占总流通股本持股比例'].sum()/100
        self.real_FloatVolume = real_float_ratio * self.TotalVolume
        self.real_FloatValue = real_float_ratio * self.TotalValue

        pass



    def set_score(self,day,score):
        self.score_dict[day] = score
        return self
    def get_negotiable(self):
        code_ak = self.ak_code
        stock_individual_info_em_df = ak.stock_individual_info_em(code_ak)
        # print(stock_individual_info_em_df)
        self.TotalVolume = stock_individual_info_em_df.iloc[6,1]
        self.TotalValue = stock_individual_info_em_df.iloc[0,1]
        self.FloatValue = stock_individual_info_em_df.iloc[1, 1] # 用xtdata 数据
        self.FloatVolume = stock_individual_info_em_df.iloc[7, 1]

    def get_infos(self):
        code = self.code
        # {'ExchangeID': 'SZ', 'InstrumentID': '000002', 'InstrumentName': '万 科Ａ', 'ProductID': '', 'ProductName': '',
        #  'CreateDate': '0', 'OpenDate': '19910129', 'ExpireDate': 99999999, 'PreClose': 14.01, 'SettlementPrice': 14.01,
        #  'UpStopPrice': 15.41, 'DownStopPrice': 12.61, 'FloatVolume': 9716667215.0, 'TotalVolume': 9724196533.0,
        #  'LongMarginRatio': 1.7976931348623157e+308, 'ShortMarginRatio': 1.7976931348623157e+308, 'PriceTick': 0.01,
        #  'VolumeMultiple': 1, 'MainContract': 2147483647, 'LastVolume': 2147483647, 'InstrumentStatus': 0,
        #  'IsTrading': False, 'IsRecent': False, 'ProductTradeQuota': None, 'ContractTradeQuota': None,
        #  'ProductOpenInterestQuota': None, 'ContractOpenInterestQuota': None}

        one_stock_dict = xtdata.get_instrument_detail(code)
        self.ExchangeID=one_stock_dict['ExchangeID']
        self.InstrumentID = one_stock_dict['InstrumentID']
        self.InstrumentName = one_stock_dict['InstrumentName']
        self.ProductID = one_stock_dict['ProductID']
        self.CreateDate = one_stock_dict['CreateDate']
        self.OpenDate = one_stock_dict['OpenDate']
        self.ExpireDate = one_stock_dict['ExpireDate']
        self.PreClose = one_stock_dict['PreClose']
        self.SettlementPrice = one_stock_dict['SettlementPrice']
        self.UpStopPrice = one_stock_dict['UpStopPrice']
        self.DownStopPrice = one_stock_dict['DownStopPrice']
        #self.FloatVolume = one_stock_dict['FloatVolume']
        #self.TotalVolume = one_stock_dict['TotalVolume'] #总股本用akshare数据
        self.LongMarginRatio = one_stock_dict['LongMarginRatio']
        self.ShortMarginRatio = one_stock_dict['ShortMarginRatio']
        self.PriceTick = one_stock_dict['PriceTick']
        self.VolumeMultiple = one_stock_dict['VolumeMultiple']
        self.MainContract = one_stock_dict['MainContract']
        self.LastVolume = one_stock_dict['LastVolume']
        self.InstrumentStatus = one_stock_dict['InstrumentStatus']
        self.IsTrading = one_stock_dict['IsTrading']
        self.IsRecent = one_stock_dict['IsRecent']

    def fresh_day_price(self):
        code = self.code
        one_stock_dict = xtdata.get_instrument_detail(code)
        self.PreClose = one_stock_dict['PreClose']
        self.SettlementPrice = one_stock_dict['SettlementPrice']
        self.UpStopPrice = one_stock_dict['UpStopPrice']
        self.DownStopPrice = one_stock_dict['DownStopPrice']

    @staticmethod
    def convert2_df_code(xt_code):
        e_id = xt_code[-2:].lower()
        return e_id+xt_code.lower().strip(".sz").strip(".sh")

    @staticmethod
    def  convert2_ak_code(xt_code):
        return xt_code.lower().strip(".sz").strip(".sh")

    @staticmethod
    def convert2_st_code(ak_code):
        pre = ""
        if ak_code.startswith("60"): pre = ".SH"
        if ak_code.startswith("000"): pre = ".SZ"
        if ak_code.startswith("00"): pre = ".SZ"
        if ak_code.startswith("30"): pre = ".SZ"
        #688
        #N   C  U

        return ak_code+pre

    @staticmethod
    def get_quarter_last_day(now,last_n=0): # now is  datetime
        delta = last_n*3
        now = now - relativedelta(months=+delta)
        month = (now.month - 1) - (now.month - 1) % 3 + 1

        # this_quarter_start = datetime(now.year, month, 1)
        this_quarter_end = datetime(now.year, month + 3, 1) - timedelta(days=1)

        return  this_quarter_end

    def get_free_top_10_em(self,date=None): #"%Y%m%d"
        if date is None:
            dd = datetime.now()
        else:
            dd = datetime.strptime(date, "%Y%m%d")
        for i in range(5):
            try:

                last_quarter = Codeinfos.get_quarter_last_day(dd,i)
                stock_gdfx_free_top_10_em_df = ak.stock_gdfx_free_top_10_em(symbol=Codeinfos.convert2_df_code(self.code), date=last_quarter.strftime("%Y%m%d"))
                if stock_gdfx_free_top_10_em_df is None :continue
                self.stock_gdfx_free_top_10_em_df =stock_gdfx_free_top_10_em_df
                return  stock_gdfx_free_top_10_em_df
            except Exception as e:
                print("warning in get_free_top_10_em",e)
                continue

        return    None

if __name__ == '__main__':
    code="603042.SH"
    a = Codeinfos(code)
    pass