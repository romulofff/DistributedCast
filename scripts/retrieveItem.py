import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamo = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamo.Table('DAD-ATV-04')

response = table.get_item(
    Key={
        "EpisodeID": 2
    }
)
print(response["Item"])