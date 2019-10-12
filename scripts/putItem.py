import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamo = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamo.Table('DAD-ATV-04')

response = table.put_item(
    Item={
        "EpisodeID": 0,
        "Author":"Nerdcast",
        "Title": "Batalha de Crossovers 2",
        "EpisodeLink": "link"
    }
)

if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
    print("Item added.")