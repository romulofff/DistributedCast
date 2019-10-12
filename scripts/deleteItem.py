import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamo = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamo.Table('DAD-ATV-04')

response = table.delete_item(
    Key={
        "EpisodeID": 0
    }
)
print(response)
if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
    print("Item deleted.")