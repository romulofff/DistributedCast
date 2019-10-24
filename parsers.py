import werkzeug
from flask_restplus import reqparse, fields

file_upload = reqparse.RequestParser()

file_upload.add_argument('EpisodeID', type=int, required=True, help='Podcast ID')
file_upload.add_argument('Author', required=True, help='Podcast Author')
file_upload.add_argument('Title', required=True, help='Episode Title')
file_upload.add_argument('mp3_file',  
                         type=werkzeug.datastructures.FileStorage, 
                         location='files', 
                         required=True, 
                         help='MP3 file')