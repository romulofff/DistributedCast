import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamo = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamo.Table('DAD-ATV-04')

response = table.scan()
# print(response["Items"][1]["EpisodeID"])

for item in response["Items"]:
    item["EpisodeID"] = int(item["EpisodeID"])

itemsList = response["Items"]

items = { "Episode: {}".format(itemsList[i]["EpisodeID"]) : itemsList[i] for i in range(0, len(itemsList))}
print(items)