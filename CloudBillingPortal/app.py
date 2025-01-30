import json
import genStatement

def lambda_handler(event, context):
    
    query = event.get('queryStringParameters')
    companyName = query["companyName"]
    cloudName = query["cloudName"]
    exchangeRate = float(query["exchangeRate"])
    invoiceDate = query["invoiceDate"]
    addressOne = query["addressOne"]
    addressTwo = query["addressTwo"]
    addressThree = query["addressThree"]
    attn = query["attn"]
    
    addressAndAttn = [addressOne, addressTwo, addressThree, attn]
    body = genStatement.generate_billing_statement(companyName, cloudName, exchangeRate, invoiceDate, addressAndAttn)
    
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        "body": json.dumps(f"{body}"),
        # 'body': json.dumps(f"{cloudName} invoice for the company {companyName} to {attn} with exchangeRate {exchangeRate} and invoice date {invoiceDate} generated in {bucket_name}")
    }