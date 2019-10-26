import os

import boto3
import werkzeug
from boto3.dynamodb.conditions import Attr, Key
from flask import Flask, request, Response
from flask_restplus import Api, Resource, fields

import parsers

application = Flask(__name__)
app = Api(app=application,
          version="1.0",
          title="DistribuCast",
          description="This API accesses a DynamoDB table and can manage its Data.\n \
                        Click on \'dynamo\' to use the methods GET and POST and work with the \
                        Database items. Each method section contains information on how to use it.")

ns = app.namespace('podcast', description="Main API")

model = app.model('Podcast', {
    "EpisodeID": fields.Integer(required=True),
    "Author": fields.String(required=True),
    "Title": fields.String(required=True),
    "EpisodeLink": fields.String()
}
)

model_file = app.model('Podcast', {
    "EpisodeID": fields.Integer(required=True),
    "Author": fields.String(required=True),
    "Title": fields.String(required=True)
}
)

S3_BUCKET = os.environ.get('S3_BUCKET')
S3_LOCATION = os.environ.get('S3_LOCATION')

@ns.route("/<int:epID>")
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


@ns.route("/<int:epID>/download")
@ns.doc(description="Use this to Download Episode from the S3.\
                        \n Use the episode ID to download it it \
                        \n The Bucket comes with three IDs inserted, 0, 1 and 2.")
class DownloadClass(Resource):

    @app.doc(responses={200: 'OK', 400: 'Invalid Data'},
             params={"epID": "Podcast episode ID"})
    def get(self, epID):

        s3 = boto3.client('s3')
        S3_BUCKET = os.environ.get('S3_BUCKET')
        
        dynamo = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamo.Table('DAD-ATV-04')

        try:
            response = table.get_item(
                Key={
                    "EpisodeID": epID
                }
            )
            response["Item"]["EpisodeID"] = int(response["Item"]["EpisodeID"])

            # This downloads the file
            filename = response["Item"]["EpisodeLink"].split('/')[-1]
            podcast_file = s3.get_object(Bucket=S3_BUCKET, Key=filename)
            
            return Response(
                podcast_file['Body'],
                mimetype='audio/mp3',
                status="Podcast Downloaded",
                headers={"Content-Disposition": "attatchment;filename={}".format(filename)},
            )

        except Exception as e:
            print(e)
            ns.abort(
                400, e.__doc__, status="Episode not found.", statusCode="400")


@ns.route("/<int:epID>/delete")
@ns.doc(description="Use this to Delete Data from the Database.\
                        \n Use the episode ID to delete it \
                        \n The database comes with three IDs inserted, 0, 1 and 2.")
class DeleteClass(Resource):

    @app.doc(responses={200: 'OK', 400: 'Invalid Data'},
             params={"epID": "Podcast episode ID"})
    def delete(self, epID):
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


@ns.route("/upload")
@ns.doc(description="Use this to Insert or Update Data in the Database.\
                        \n To update, just use an EpisodeID that already exists \
                        \n To insert use the model with a completely new EpisodeID")
class UploadClass(Resource):

    @app.doc(responses={200: 'OK', 400: 'Invalid Data'})
    @app.expect(parsers.file_upload)
    def post(self):
        dynamo = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamo.Table('DAD-ATV-04')

        s3 = boto3.client('s3')
        S3_BUCKET = os.environ.get('S3_BUCKET')
        S3_LOCATION = os.environ.get('S3_LOCATION')

        args = parsers.file_upload.parse_args()
        episode_file = args['mp3_file']

        try:
            s3.upload_fileobj(
                episode_file,
                S3_BUCKET,
                str(episode_file.filename),
                ExtraArgs={'ACL':'public-read'}

            )
        except Exception as e:
            print(e)
            ns.abort(
                400, e.__doc__, statusCode="400")

        episode_link = S3_LOCATION+episode_file.filename

        json = {
            "EpisodeID": args["EpisodeID"],
            "Author": args["Author"],
            "Title": args["Title"],
            "EpisodeLink": episode_link
        }

        try:
            response = table.put_item(
                Item=json
            )
            if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                return {
                    "status": "Podcast Uploaded"
                }
        except Exception as e:
            print(e)
            ns.abort(
                400, e.__doc__, statusCode="400")


@ns.route("/listEpisodes")
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
