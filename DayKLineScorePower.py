from xtquant import xtdata
from  datetime import datetime,timedelta
from BaseScore import BaseScore
from CodeInfos import Codeinfos


class DayKlineScorePower(BaseScore):

    def __init__(self):
        super(BaseScore,self).__init__()
        self.type = '1m'
        self.day = None
        self.codes = None
        self.codes_info =None
        self.code2codeinfos = None
        pass

    def get_codes(self,codes_info):
        self.codes =  []
        self.code2codeinfos = dict()
        for code_info in codes_infos:
            cde = code_info.code
            self.codes.append(cde)
            self.code2codeinfos[cde] = code_info

        return self.codes
    def get_1m_data(self,params_dict):
        day = self.day
        codes = self.codes
        typ =  self.type
        # day_dt = datetime.strptime(day,"%Y%m%d")
        # dayP1_dt = day_dt+timedelta(days=1)
        # dayP1=dayP1_dt.strftime("%Y%m%d")

        data = xtdata.get_market_data(field_list=[], stock_list=codes, period=typ, start_time=day,end_time=day,count=-1)

        if  data['time'].empty:
            xtdata.download_history_data2(codes, period=typ, start_time=day, end_time=day)

            data = xtdata.get_market_data(field_list=[], stock_list=codes, period=typ, start_time=day, end_time=day,
                                          count=-1)

        return data

    def scores_all(self,params_dict):
        self.codes_info = params_dict.get("codes_infos")
        self.day = params_dict.get("day")
        self.get_codes(self.codes_info)
        data = self.get_1m_data(params_dict)
        mean_df = (data['open'] +data['close'])/2
        for code in self.codes:
            mean_code_1m_s = mean_df.loc[code]
            up_price = self.code2codeinfos[code].UpStopPrice
            delta_10 =  self.code2codeinfos[code].UpStopPrice - self.code2codeinfos[code].DownStopPrice
            delta = mean_code_1m_s - up_price
            delta_p = delta*20/delta_10
            pass

        pass

    def score(self,delta_p_series):
        pass


if __name__ == '__main__':
    code="000001.SZ"

    day_kline_score = DayKlineScorePower()


    codes_infos = [Codeinfos("000002.SZ"),Codeinfos("000004.SZ")]
    params={'day':"20230630",
            "codes_infos":codes_infos
            }
    day_kline_score.score(params)

    pass