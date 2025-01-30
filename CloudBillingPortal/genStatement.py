import warnings
from myPdf import huawei_statement
import boto3
import base64
import os

warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

def generate_billing_statement(companyName, cloudName, exchangeRate, date, addressAndAttn):   
    s3_client = boto3.client("s3")
    S3_BUCKET_NAME = os.environ["BACKEND_BUCKET_NAME"]
    #Create a statement object

    # match cloudName:
    #     case "AWS":
    #         pdf = aws_statement()
    #     case "Huawei Cloud":
    pdf = huawei_statement()
        
    pdf.add_page()
    pdf.statement_address(addressAndAttn)
    
    # Add an statement date

    pdf.statement_invoice_date(date)

    # Add the statement header
    pdf.statement_table_header(companyName, cloudName)
    
    response = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME)
    s3_files = response.get("Contents", [])
    
    # Add the statement summary
    totalAmountDue=0
    for s3_file in s3_files:
        if s3_file["Key"].lower().endswith(".xlsx"):
            file_content = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=s3_file["Key"])["Body"].read()
            totalAmountDue = pdf.statement_table_summary_row(file_content, cloudName, exchangeRate) +totalAmountDue

    pdf.statement_table_summary_sub_total(totalAmountDue)
    pdf.statement_table_summary_total(totalAmountDue)
    
    for s3_file in s3_files:
        if s3_file["Key"].lower().endswith(".xlsx"):
            file_content = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=s3_file["Key"])["Body"].read()
            pdf.gen_billing_details(file_content, cloudName, exchangeRate)
            s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key = s3_file["Key"])

    file = "billing_statement.pdf"
    
    return base64.b64encode(pdf.output(file, 'S').encode('latin-1'))