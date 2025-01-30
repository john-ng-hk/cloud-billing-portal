from fpdf import FPDF
import myBillAcc
import boto3
import os

S3_BUCKET_NAME = os.environ["FRONTEND_BUCKET_NAME"]
class statement(FPDF):
    def header(self):
        # Add an image (e.g., company logo)
        imageLink = "https://s3."+os.environ["REGION"]+".amazonaws.com/"+S3_BUCKET_NAME + "/company_logo.png"
        self.image(imageLink, 10, 11, 10)  # Adjust the path and size as needed
        self.set_font('Arial', 'B', 12)
        self.cell(0, 7, '', 0, 1, 'C')
        self.ln()

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', '', 10)
        self.cell(0, 3, title, 0, 1, 'L')
        self.ln()

    def statement_address(self, addressDetails):
        self.set_font('Arial', '', 10)
        for i in addressDetails:
            if i == addressDetails[-1]:
                self.cell(11, 3, "ATTN: ", 0, 0)
                my_bucket = S3_BUCKET_NAME
                fontName = "fireflysung"
                filename = fontName+".ttf"
                local_font_path = "/tmp/" + filename
                
                s3 = boto3.client('s3')
                s3.download_file(my_bucket, filename, local_font_path)
                self.add_font(fontName, '', local_font_path, uni=True)
                self.set_font(fontName, '', 10)
            self.cell(0, 3, i, 0, 1)
            
            self.ln()

    def statement_invoice_date(self, date):
        self.set_font('Arial', '', 11)
        self.cell(0, 6, "Invoice Date: "+date, 0, 1, 'R')
        self.ln()

    def statement_table_header(self, companyName, cloudName):
        self.set_font('Arial', '', 9)
        self.cell(40, 10, 'Date / Period', "TB")
        self.cell(100, 10, 'Description', "TB")
        self.cell(0, 10, 'Amount (HKD)', "TB",0,"R")
        self.ln()
        self.set_font('Arial', 'B', 9)
        self.cell(40, 10, '')
        self.cell(100, 10, companyName+" "+cloudName+" Services Fee",0,1)

    def statement_table_summary_row(self, xlsx_file, cloudName , exchangeRate):
        billingAccount = myBillAcc.Billing_Account(xlsx_file, cloudName, exchangeRate)
        self.set_font('Arial', '', 9)
        self.cell(40, 5, billingAccount.get_bill_cycle(), 0)
        self.cell(100, 5, cloudName+" Services Fee", 0,0)
        amountHKD = float(billingAccount.gen_bill_sum())*exchangeRate
        self.cell(0, 5, f'{amountHKD:,.2f}', 0,1,"R")
        self.cell(45, 5, '', 0,0)
        self.cell(100, 5, "Account Name: "+billingAccount.accountName, 0,1)
        self.cell(45, 5, '', 0,0)
        self.cell(100, 5, "Exchange Rate: 1 USD="+str(exchangeRate)+" HKD", 0,1)
        self.ln()

        return round(amountHKD,2)
    
    def statement_table_summary_sub_total(self, totalAmountDue):
        #subtotal amount
        self.set_font('Arial', 'B', 9)
        self.cell(100, 5, "",0,0)
        self.cell(40, 5, "Total Amount Due ",'TB',0,'L')
        self.cell(0, 5, f'{totalAmountDue:,.2f}','TB',1,"R")
        self.ln()

    def statement_table_summary_total(self, totalAmountDue):
        #total amount

        self.set_font('Arial', 'B', 12)
        self.cell(40,6,"Total Amount Due","LB",0,"L")
        self.cell(0,6,f'{totalAmountDue:,.2f}',"B",1,"R")

class aws_statement(statement):
    def gen_billing_details(self, xlsx_file, cloudName, exchangeRate):
        billingAccount = myBillAcc.Billing_Account(xlsx_file, cloudName, exchangeRate)
        df=billingAccount.df
        accountName = billingAccount.accountName
        exchangeRate = billingAccount.exchangeRate

        self.add_page()
        self.set_font('Arial', '', 9)
        self.cell(100, 5, accountName+":" ,0,1)

        # Add the table header
        self.set_font('Arial', '', 4)
        tableHeight = 3
        self.set_fill_color(192,192,192)

        # pdf.cell(11, tableHeight, 'Billing Cycle',1,0,fill = True)
        self.cell(15, tableHeight, 'Billing Mode',1,0,fill = True)
        self.cell(35, tableHeight, 'Product Type', 1,0,fill = True)
        self.cell(60, tableHeight, 'Product Name', 1,0,fill = True)
        self.cell(15, tableHeight, 'Usage', 1,0,fill = True)
        self.cell(15, tableHeight, 'Usage Unit', 1,0,fill = True)
        self.cell(15, tableHeight, 'Payment(USD)', 1,0,fill = True)
        self.cell(15, tableHeight, 'Exchange Rate', 1,0,fill = True)
        self.cell(20, tableHeight, 'Payment(HKD)', 1,1,fill = True)

        for index, row in df.iterrows():
            # pdf.cell(11, tableHeight, row['Billing Cycle'], 1)
            self.cell(15, tableHeight, row['Billing Mode'], 1)
            self.cell(35, tableHeight, row['Product Type'], 1)
            self.cell(60, tableHeight, row['Product Name'], 1)
            tempUsage = ""
            if str(row['Usage'])!='nan':
                tempUsage = str(row['Usage'])
            self.cell(15, tableHeight, tempUsage, 1)

            tempUsageUnit=""
            if str(row['Usage Unit'])!='nan':
                tempUsageUnit = str(row['Usage Unit'])
            self.cell(15, tableHeight, tempUsageUnit, 1)
            self.cell(15, tableHeight, str(row['Actual Customer Expenditure(USD)']), 1,0,'R')
            self.cell(15, tableHeight, str(exchangeRate), 1)
            self.cell(20, tableHeight, str(row['Actual Customer Expenditure(HKD)']), 1,1,'R')

class huawei_statement(statement):
    def gen_billing_details(self, xlsx_file, cloudName, exchangeRate):
        billingAccount = myBillAcc.Billing_Account(xlsx_file, cloudName, exchangeRate)
        df=billingAccount.df
        accountName = billingAccount.accountName
        exchangeRate = billingAccount.exchangeRate

        self.add_page()
        self.set_font('Arial', '', 9)
        self.cell(100, 5, accountName+":" ,0,1)

        # Add the table header
        self.set_font('Arial', '', 4)
        tableHeight = 3
        self.set_fill_color(192,192,192)

        self.cell(15, tableHeight, 'Billing Mode',1,0,fill = True)
        self.cell(35, tableHeight, 'Product Type', 1,0,fill = True)
        self.cell(60, tableHeight, 'Product Name', 1,0,fill = True)
        self.cell(15, tableHeight, 'Usage', 1,0,fill = True)
        self.cell(10, tableHeight, 'Usage Unit', 1,0,fill = True)
        self.cell(15, tableHeight, 'Payment(USD)', 1,0,fill = True)
        self.cell(15, tableHeight, 'Coupons Used(USD)', 1,0,fill = True)
        self.cell(15, tableHeight, 'Exchange Rate', 1,0,fill = True)
        self.cell(15, tableHeight, 'Payment(HKD)', 1,1,fill = True)

        for index, row in df.iterrows():
            self.cell(15, tableHeight, row['Billing Mode'], 1)
            self.cell(35, tableHeight, row['Product Type'], 1)
            self.cell(60, tableHeight, row['Product Name'], 1)
            tempUsage = ""
            if str(row['Usage'])!='nan':
                tempUsage = str(row['Usage'])
            self.cell(15, tableHeight, tempUsage, 1)

            tempUsageUnit=""
            if str(row['Usage Unit'])!='nan':
                tempUsageUnit = str(row['Usage Unit'])
            self.cell(10, tableHeight, tempUsageUnit, 1)
            actualUSD=row['Actual Customer Expenditure(USD) before discount']
            actualCouponUsed=row['Actual Coupons Used(USD)']
            self.cell(15, tableHeight, f'{actualUSD:,.4f}', 1,0,'R')
            self.cell(15, tableHeight, f'{actualCouponUsed:,.4f}', 1,0,'R')
            self.cell(15, tableHeight, str(exchangeRate), 1)
            actualHKD=row['Actual Customer Expenditure(HKD)']
            self.cell(15, tableHeight, f'{actualHKD:,.4f}', 1,1,'R')