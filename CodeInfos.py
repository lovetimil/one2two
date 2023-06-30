
import akshare as ak
from xtquant import xtdata


class Codeinfos(object):


    def __init__(self,code):
        self.code = code
        self.ak_code = Codeinfos.convert_ak_code(code)
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

        self.fresh()


    def fresh(self):
        self.get_negotiable()
        self.get_infos()


    def get_negotiable(self):
        code_ak = self.ak_code
        stock_individual_info_em_df = ak.stock_individual_info_em(code_ak)
        # print(stock_individual_info_em_df)
        self.TotalVolume = stock_individual_info_em_df.iloc[6,1]
        self.TotalValue = stock_individual_info_em_df.iloc[0,1]
        # self.FloatValue = stock_individual_info_em_df.iloc[1, 1] # 用xtdata 数据
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
        self.FloatVolume = one_stock_dict['FloatVolume']
        self.TotalVolume = one_stock_dict['TotalVolume'] #总股本用akshare数据
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
    def  convert_ak_code(xt_code):
        return xt_code.lower().strip(".sz").strip(".sh")

    @staticmethod
    def convert_st_code(ak_code):
        pre = ""
        if ak_code.startswith("60"): pre = ".SH"
        if ak_code.startswith("000"): pre = ".SZ"
        if ak_code.startswith("002"): pre = ".SZ"
        if ak_code.startswith("300"): pre = ".SZ"
        #688
        #N   C  U

        return ak_code+pre

if __name__ == '__main__':
    code="000002.SZ"
    a = Codeinfos(code)
    pass