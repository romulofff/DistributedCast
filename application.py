import boto3
from boto3.dynamodb.conditions import Attr, Key
from flask import Flask, request
from flask_restplus import Api, Resource, fields

application = Flask(__name__)
app = Api(app=application,
          version="0.1",
          title="Dynamo Worker",
          description="This API accesses a DynamoDB table and can manage its Data.\n \
                        Click on \'dynamo\' to use the methods GET and POST and work with the \
                        Database items. Each method section contains information on how to use it.")

ns = app.namespace('dynamo', description="Main API")


model = app.model('Podcast',
                  {
                      "EpisodeID": fields.Integer(required=True),
                      "Author": fields.String(required=True),
                      "Title": fields.String(required=True),
                      "EpisodeLink": fields.String()
                  }
                  )


@ns.route("/retrieve/<int:epID>")
@ns.doc(description="Use this to Retrieve Data from the Database.\
                        \n Use the episode ID to retrieve it \
                        \n The database comes with three IDs inserted, 0, 1 and 2.")
class RetrieveClass(Resource):

    @app.doc(responses={200: 'OK', 400: 'Invalid Data'},
             params={"epID": "Podcast episode ID"})
    def get(self, epID):
        dynamo = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamo.Table('DAD-ATV-04')

        try:
            response = table.get_item(
                Key={
                    "EpisodeID": epID
                }
            )
            response["Item"]["EpisodeID"] = int(response["Item"]["EpisodeID"])
            return {
                "status": "Podcast retrieved.",
                "data": response["Item"]
            }

        except Exception as e:
            print(e)
            ns.abort(
                400, e.__doc__, status="Episode not found.", statusCode="400")


@ns.route("/delete/<int:epID>")
@ns.doc(description="Use this to Delete Data from the Database.\
                        \n Use the episode ID to delete it \
                        \n The database comes with three IDs inserted, 0, 1 and 2.")
class DeleteClass(Resource):

    @app.doc(responses={200: 'OK', 400: 'Invalid Data'},
             params={"epID": "Podcast episode ID"})
    def get(self, epID):
        dynamo = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamo.Table('DAD-ATV-04')

        try:
            table.delete_item(
                Key={
                    "EpisodeID": epID
                }
            )
            return {
                "status": "Podcast deleted."
            }

        except Exception as e:
            print(e)
            ns.abort(
                400, e.__doc__, status="Episode not found.", statusCode="400")


@ns.route("/add")
@ns.doc(description="Use this to Insert or Update Data in the Database.\
                        \n To update, just use an EpisodeID that already exists \
                        \n To insert use the model with a completely new EpisodeID")
class AddClass(Resource):

    @app.doc(responses={200: 'OK', 400: 'Invalid Data'})
    @app.expect(model)
    def post(self):
        dynamo = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamo.Table('DAD-ATV-04')

        try:
            response = table.put_item(
                Item=request.json
            )
            if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                return {
                    "status": "Podcast Added"
                }
        except Exception as e:
            ns.abort(
                400, e.__doc__, statusCode="400")


@ns.route("/listItems")
@ns.doc(description="Use this to retrieve all items from the table.")
class ListClass(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Data'})
    def get(self):
        dynamo = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamo.Table('DAD-ATV-04')

        response = table.scan()

        for item in response["Items"]:
            item["EpisodeID"] = int(item["EpisodeID"])

        itemsList = response["Items"]

        items = {"Episode: {}".format(
            itemsList[i]["EpisodeID"]): itemsList[i] for i in range(0, len(itemsList))}

        return items