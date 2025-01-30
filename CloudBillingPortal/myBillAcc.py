import datetime
import pandas as pd
import numpy as np
import io
import calendar

class Billing_Account:
    def __init__(self, excel_file, cloud, exchangeRate):
        self.df = pd.read_excel(io.BytesIO(excel_file))
        self.accountName = self.df["Account Name"][0]
        self.billCycle = self.df['Billing Cycle'][0]
        self.exchangeRate = exchangeRate
        self.cloud = cloud
        df=self.df

        discountLimit = 0.10
        markupDiscount = 0.08
        discountCoefficient = (1-markupDiscount)/(1-discountLimit)
        
        df['Settlement Discount']= df['Settlement Discount'].str.replace('%','')
        df['Settlement Discount'] = df['Settlement Discount'].astype(float)
        df['Actual Settlement Discount'] = np.where(df['Settlement Discount']<discountLimit*100,0,markupDiscount*100)
        df['Actual Customer Expenditure(USD) before discount'] = np.where((df['Coupons Used(USD)'] >= df['Payment(USD)']) & (df['Coupons Used(USD)'] <= df['Payment(USD)']), df['Payment(USD)']*discountCoefficient, df['Customer Expenditure(USD)']*(1-df['Actual Settlement Discount']/100))
        df['Actual Coupons Used(USD)'] = df['Coupons Used(USD)']*discountCoefficient
        df['Actual Customer Expenditure(USD)'] = np.where((df['Coupons Used(USD)'] >= df['Payment(USD)']) & (df['Coupons Used(USD)'] <= df['Payment(USD)']), 0, df['Customer Expenditure(USD)']*(1-df['Actual Settlement Discount']/100)-df['Coupons Used(USD)']*discountCoefficient)
        df['Actual Customer Expenditure(HKD)'] = pd.to_numeric(df['Actual Customer Expenditure(USD)'])*float(exchangeRate)

    def get_bill_cycle(self):
        rawBillCycle = datetime.datetime.strptime(self.billCycle, '%Y-%m')
        billCycleMonthYear = rawBillCycle.strftime("%b %y")
        
        billCycleYear = int(rawBillCycle.strftime("%y"))
        billCycleMonth = list(calendar.month_abbr).index(rawBillCycle.strftime("%b"))
        
        temp, lastDay = calendar.monthrange(billCycleYear, billCycleMonth)

        billCycle = "1 "+str(billCycleMonthYear)+" - "+str(lastDay)+" "+str(billCycleMonthYear)

        return billCycle
        
    def gen_bill_sum(self):      
        df= self.df
        accountAmount = df['Actual Customer Expenditure(USD)'].sum()
        
        return accountAmount