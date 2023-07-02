from xtquant import xtdata
from  datetime import datetime,timedelta
from BaseScore import BaseScore
from CodeInfos import Codeinfos
from UpTools import UpTools


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
        for code_info in codes_info:
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
        # xtdata.download_history_data2(codes, period=typ, start_time=day, end_time=day)
        xtdata.download_history_data2(codes, period=typ, start_time=day, end_time=day)

        data = xtdata.get_market_data(field_list=[], stock_list=codes, period=typ, start_time=day,end_time=day,count=-1,fill_data=True)

        if  data['time'].empty:
            xtdata.download_history_data2(codes, period=typ, start_time=day, end_time=day)

            data = xtdata.get_market_data(field_list=[], stock_list=codes, period=typ, start_time=day, end_time=day,
                                          count=-1,fill_data=True)

        return data

    def scores_all(self,params_dict):
        self.codes_info = params_dict.get("codes_infos")
        self.day = params_dict.get("day")
        self.get_codes(self.codes_info)
        data = self.get_1m_data(params_dict)
        mean_df = data['close']
        for code in self.codes:
            code_1m_s = mean_df.loc[code]
            # up_price = self.code2codeinfos[code].UpStopPrice
            # delta_10 =  self.code2codeinfos[code].UpStopPrice - self.code2codeinfos[code].DownStopPrice
            # delta = mean_code_1m_s - up_price
            # delta_p = delta*20/delta_10
            self.score(code_1m_s,self.code2codeinfos[code])
            pass

        pass

    def score(self,code_1m_s,code_infos):
        count_all = 0;ct_hit_up = 0
        pre_hit_up = True;count_hole=0
        up_price = code_infos.UpStopPrice
        delta_10 = code_infos.UpStopPrice - code_infos.DownStopPrice
        T_flag = False
        now_hit_up = False
        hole_area = 0
        last_hole_time = 0
        flag_count = 0

        for dt,close_price in code_1m_s.iteritems():
            delta_p = abs(close_price - up_price)*20/delta_10

            if delta_p  < 0.01:
                ct_hit_up += 1;
                now_hit_up = True
                flag_count = 0
            else:
                now_hit_up = False
                hole_area += delta_p*1
                flag_count +=1
                T_flag = True

            if now_hit_up is False and pre_hit_up is True and flag_count == 1: hole_area = 0
            # print("ct_hit_up", ct_hit_up, "count_all", count_all, "new_price:", close_price, "up_price:", up_price,
            #       "hole area", hole_area, 'flag_count', flag_count, 'now_hit_up', now_hit_up, 'pre_hit_up', pre_hit_up,
            #       "now", dt)
            # delta_time = tims - last_hit_time
            if now_hit_up is True and pre_hit_up is False and True and hole_area > 0 :
                # if now_hit_up != pre_hit_up and delta_time_hit > 60 and delta_price > 1:

                # print("code name:", code_infos.InstrumentName, "new_price:", close_price, "up_price:", up_price,
                #       "now_hit_up:", now_hit_up, "pre_hit_up:", pre_hit_up, "hole_area:",
                #       hole_area, "now time:", dt, "last hit time:",
                #       last_hole_time)
                hole_area = 0
                count_hole += 1
                # pre_hit_up = now_hit_up
                last_hole_time = dt
                # last_price = close_price
                flag_count = 0

            pre_hit_up = now_hit_up
            count_all += 1



            # last for hole
        delta_price = abs((up_price - close_price) * 20 / delta_10)
        # if now_hit_up  != True and delta_time_hit > 57 and delta_price >0.3:
        if now_hit_up != True and True and delta_price > 0.3:
            print("code name:", code_infos.InstrumentName, "new_price:", close_price, "up_price:", up_price, "last_price:",
                  "now_hit_up:", now_hit_up, "pre_hit_up:", pre_hit_up, "delta price:", delta_price,
                  "now time:", dt, "last hit time:", last_hole_time)

            count_hole += 1

        ratio = ct_hit_up * 1.0 / count_all
        count_hole = count_hole

        hole_score = min(count_hole * 5, 50)
        below_score = (1 - ratio) * 100

        open_sore = 0
        open_p = (close_price - up_price) * 20 / delta_10
        if open_p < -0.001 and open_p > -5: open_sore = 5
        if open_p < -5 and open_p > -10: open_sore = 8
        if open_p < -10 and open_p > -15: open_sore = 13
        if open_p < -15 and open_p > -20.001: open_sore = 10

        score = max(100 - max(below_score, hole_score), 0)

        if score > 95:  score -= open_sore
        if score == 100 and T_flag : score -= 2

        print("score", "name:", code_infos.InstrumentName, "code:", code_infos.code, 'score:', score, 'below_score:',
              below_score, 'hole_score:', hole_score, 'open_score:', open_sore)
        code_infos.set_score(datetime.strptime(dt,"%Y%m%d%H%M%S").strftime("%Y%m%d"), score)
        pass


if __name__ == '__main__':
    code="000001.SZ"

    day_kline_score = DayKlineScorePower()


    #codes_infos = [Codeinfos("000678.SZ"),Codeinfos("000002.SZ")]
    # codes_infos = [Codeinfos("002286.SZ"),Codeinfos("603042.SH")]
    # params={'day':"20230630",
    #         "codes_infos":codes_infos
    #         }
    # day_kline_score.scores_all(params)

    ut = UpTools()
    df = ut.get_up_code()
    test_codes = []
    for code in df['代码']:
        test_codes.append(Codeinfos(Codeinfos.convert2_st_code(code)))
        pass

    codes_infos = [Codeinfos("603042.SH"),Codeinfos("603767.SH")]
    params={'day':"20230630",
            "codes_infos":test_codes
            }
    day_kline_score.scores_all(params)

    pass