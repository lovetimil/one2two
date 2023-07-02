
import akshare as ak


class UpTools(object):

    def __init__(self,date_input='20230630'):
        self.date = date_input
        self.stock_zt_pool_previous_em_df = None
        self.stock_zt_pool_em_df = None
        self.get_up_code()
        self.get_up_previous_code()
        pass

    def get_up_previous_code(self,date_input=None): #%Y%m%d
        if date_input is None: date_input = self.date
        df = ak.stock_zt_pool_previous_em(date=date_input)
        df.drop(df[(df['名称'].str.contains(pat="st",regex=False)==True) | (df['名称'].str.contains(pat="退",regex=False)==True)].index,inplace=True)

        self.stock_zt_pool_previous_em_df = df

        # print(stock_zt_pool_previous_em_df)
        return  df

    def get_up_code(self,date_input=None): #%Y%m%d
        if date_input is None: date_input = self.date

        df = ak.stock_zt_pool_em(date=date_input)
        df.drop(df[(df['名称'].str.contains(pat="st",regex=False)==True) | (df['名称'].str.contains(pat="退",regex=False)==True)].index,inplace=True)

        self.stock_zt_pool_em_df = df
        # print(stock_zt_pool_previous_em_df)
        return  df



    def get_one2two_can(self):
        if self.stock_zt_pool_previous_em_df is None :
            self.get_up_previous_code()

        df = self.stock_zt_pool_previous_em_df
        # df = df.drop(df[(df['名称'].str.contains(pat="st",regex=False)==True) | (df['名称'].str.contains(pat="退",regex=False)==True)].index,inplace=False)

        # df.drop(df[df['名称'].str.contains(pat="退",regex=False)==True].index,inplace=True)

        #
        df= df.drop(df[df['昨日连板数']>1].index)
        self.one2two_df =df
        return df

    def get_above2_can(self):
        if self.stock_zt_pool_previous_em_df is None :
            self.get_up_previous_code()
        df = self.stock_zt_pool_previous_em_df

        df= df.drop(df[df['昨日连板数']==1].index)

        return  df


if __name__ == '__main__':
    code="603042.SH"
    a = UpTools(date_input='20230630')
    a.get_one2two_can()
    pass
