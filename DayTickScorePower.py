import math

import numpy as np
from xtquant import xtdata
from  datetime import datetime,timedelta
from BaseScore import BaseScore
from CodeInfos import Codeinfos
from UpTools import UpTools


class DayTickScorePower(BaseScore):

    def __init__(self):
        super(BaseScore,self).__init__()
        self.type = 'tick'
        self.day = None
        self.codes = None
        self.codes_info =None
        self.code2codeinfos = None
        self.time_930=datetime.now().replace(hour=9,minute=30).timestamp()*1000
        self.time_1500 = datetime.now().replace(hour=15).timestamp()*1000
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

        data = xtdata.get_market_data(field_list=[], stock_list=codes, period=typ, start_time=day,end_time=day,count=-1)


        if  data[codes[0]].size == 0:
            xtdata.download_history_data2(codes, period=typ, start_time=day, end_time=day)

            data = xtdata.get_market_data(field_list=[], stock_list=codes, period=typ, start_time=day, end_time=day,
                                          count=-1)

        return data

    def scores_all(self,params_dict):
        self.codes_info = params_dict.get("codes_infos")
        self.day = params_dict.get("day")
        self.get_codes(self.codes_info)
        data = self.get_1m_data(params_dict)
        # mean_df = (data['open'] +data['close'])/2
        for code in self.codes:
            # print("==123",code)
            one_code_ndarray = data[code]
            # mean_code_1m_s = mean_df.loc[code]
            # up_price = self.code2codeinfos[code].UpStopPrice
            # delta_10 =  self.code2codeinfos[code].UpStopPrice - self.code2codeinfos[code].DownStopPrice
            # delta = mean_code_1m_s - up_price
            # delta_p = delta*20/delta_10
            code_infos = self.code2codeinfos[code]
            self.score(one_code_ndarray,code_infos)
            #self.score_v2(one_code_ndarray,code_infos)
            # print(code_infos.InstrumentName,code_infos.score_dict)
            pass


        pass

    def score_v2(self, one_code_ndarray, codeinfos):
        count_all = 0;


        up_price = codeinfos.UpStopPrice
        delta_10 = codeinfos.UpStopPrice - codeinfos.DownStopPrice
        DownStopPrice = codeinfos.DownStopPrice
        close_price = 0
        open_price = 0

        area = 0
        for ele in one_code_ndarray:
            tims = ele[0] // 1000
            dt = datetime.fromtimestamp(tims)
            if not ((dt.hour < 15 and dt.hour > 10) or (dt.hour == 9 and dt.minute > 29)): continue
            open_price = ele[2]
            # new_price = max(ask_price[0],bid_price[0])
            new_price = ele[1]
            delta_p = (new_price - DownStopPrice) * 20 / delta_10
            area +=delta_p*3
            close_price = new_price

            count_all += 1

        area_all = count_all*3*20


        open_p = (open_price - up_price) * 20 / delta_10
        open_sore = 0
        if open_p <-0.001 and open_p > -5: open_sore = -0.4
        if open_p < -5 and open_p > -10 :open_sore =-0.5
        if open_p < -10 and open_p > -15: open_sore=-0.7
        if open_p < -15 and open_p > -20.001 :open_sore = -0.8


        close_p = (close_price - up_price) * 20 /delta_10
        close_score = 0
        if close_p <-0.001 and close_p > -5: close_score = -5
        if close_p < -5 and close_p > -10 :close_score = -10
        if close_p < -10 and close_p > -15 :close_score = -12
        if close_p < -15 and close_p > -20.001 :close_score = -15

        area_score = int(area * 100 / area_all)
        score = max(area_score+open_sore+close_score,0)

        print("score_v2",codeinfos.InstrumentName,codeinfos.code,score,area_score,open_sore,close_score)


        codeinfos.set_score(dt.strftime("%Y%m%d"), score)
        pass

    def score(self,one_code_ndarray,codeinfos):
        up_price = codeinfos.UpStopPrice
        delta_10 =  codeinfos.UpStopPrice - codeinfos.DownStopPrice

        count_all = 0;ct_hit_up = 0
        pre_hit_up = True;last_hole_time = 0;last_price = up_price;now_hit_up=False;count_hole=0

        last_tims = 0

        open_price=0
        new_price = 0
        hole_area = 0 ;flag_count=0

        # for ele in one_code_ndarray:
        size =  one_code_ndarray.size
        T_flag = False
        i = 0
        while i < size:
            ele = one_code_ndarray[i]
            tims = ele[0]//1000
            dt = datetime.fromtimestamp(tims)
            # print("orgin dt",dt)
            if not ((dt.hour <16 and dt.hour > 9 ) or (dt.hour ==9 and dt.minute> 29)):
                i+=1
                continue
            ask_price = ele[12]
            bid_price = ele[13]
            open_price = ele[2]
            # new_price = max(ask_price[0],bid_price[0])
            new_price = ele[1]
            delta_p = (new_price - up_price)*20/delta_10
            delta_price = abs(( new_price -last_price)*20/delta_10)
            if(delta_price > 3) :delta_price = 3
            if delta_p >-0.0001:
                ct_hit_up +=1;
                now_hit_up = True
                flag_count = 0
            else:
                now_hit_up = False
                hole_area += delta_price*3
                flag_count +=1
                T_flag = True


            if now_hit_up is False and pre_hit_up is True and flag_count ==1 :hole_area = 0
            print("ct_hit_up",ct_hit_up,"count_all",count_all,"new_price:",new_price,"up_price:",up_price,"hole area",hole_area,'flag_count',flag_count,'now_hit_up',now_hit_up,'pre_hit_up',pre_hit_up,"now",datetime.fromtimestamp(tims))
            # delta_time = tims - last_hit_time
            if now_hit_up is  True and  pre_hit_up is  False and True and hole_area > 7 and tims - last_hole_time > 1*20*3+3  :
            #if now_hit_up != pre_hit_up and delta_time_hit > 60 and delta_price > 1:

                print("code name:",codeinfos.InstrumentName,"new_price:",new_price,"up_price:",up_price,"last_price:",last_price,"now_hit_up:",now_hit_up,"pre_hit_up:",pre_hit_up,"hole_area:",hole_area,"now time:",datetime.fromtimestamp(tims),"last hit time:",datetime.fromtimestamp(last_hole_time))
                hole_area = 0
                count_hole +=1
                # pre_hit_up = now_hit_up
                last_hole_time =tims
                last_price = new_price
                flag_count = 0

            pre_hit_up = now_hit_up
            count_all +=1

            #补充数据
            if (tims - last_tims) >3 and last_tims !=0 and not (dt.hour==13 and dt.minute == 0) : #13:00 那一分钟不补
                last_tims+=3
            else:
                last_tims = tims
                i+=1


        #last for hole
        delta_price = abs((up_price-new_price)*20/delta_10)
        #if now_hit_up  != True and delta_time_hit > 57 and delta_price >0.3:
        if now_hit_up != True and True and delta_price > 0.3:
            # print("code name:", codeinfos.InstrumentName, "new_price:", new_price, "up_price:", up_price, "last_price:",
            #       last_price, "now_hit_up:", now_hit_up, "pre_hit_up:", pre_hit_up, "delta price:", delta_price,
            #       "now time:", datetime.fromtimestamp(tims), "last hit time:", datetime.fromtimestamp(last_hit_time))


            count_hole += 1


        ratio = ct_hit_up*1.0/count_all
        count_hole = count_hole

        hole_score = min(count_hole*5,50)
        below_score =  (1-ratio)*100

        open_sore = 0
        open_p = (open_price - up_price) * 20 / delta_10
        if open_p <-0.001 and open_p > -5: open_sore = 5
        if open_p < -5 and open_p > -10 :open_sore = 8
        if open_p < -10 and open_p > -15 :open_sore = 13
        if open_p < -15 and open_p > -20.001 :open_sore = 10



        score = max(100 - max( below_score ,hole_score),0)

        if score > 95:  score -=open_sore
        if score == 100: score -= 2


        print("score","name:",codeinfos.InstrumentName,"code:",codeinfos.code,'score:',score,'below_score:',below_score,'hole_score:',hole_score,'open_score:',open_sore)

        codeinfos.set_score(dt.strftime("%Y%m%d"),score)
        pass


if __name__ == '__main__':
    code="000001.SZ"

    day_Tick_score = DayTickScorePower()


    # codes_infos = [Codeinfos("603042.SH"),Codeinfos("603118.SH")]
    codes_infos = [Codeinfos("603042.SH")]
    params={'day':"20230630",
            "codes_infos":codes_infos
            }
    day_Tick_score.scores_all(params)
    # print(codes_infos[0].score_dict,codes_infos[1].score_dict)
    print(codes_infos[0].score_dict)


    #
    # ut = UpTools()
    # df = ut.get_up_code()
    # test_codes = []
    # for code in df['代码']:
    #     test_codes.append(Codeinfos(Codeinfos.convert2_st_code(code)))
    #     pass
    #
    # codes_infos = [Codeinfos("603042.SH"),Codeinfos("603767.SH")]
    # params={'day':"20230630",
    #         "codes_infos":test_codes
    #         }
    # day_Tick_score.scores_all(params)
    #
    # for code in test_codes:
    #     print(code.InstrumentName,code.score_dict)
    # pass
    # # 600714.
    # SH
    #
    # 002647.
    # SZ
    #
    # 002356.
    # SZ
    #
    # 001209.
    # SZ
    #
    # 002731.
    # SZ
    pass