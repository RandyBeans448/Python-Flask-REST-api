from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)



class VideoModal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    views = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {name}, likes = {likes}, views = {views})"




video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of video is required", required=True)
video_put_args.add_argument("likes", type=int, help="Number of likes is required", required=True)
video_put_args.add_argument("views", type=int, help="Amount of views is required", required=True)



video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Update name")
video_update_args.add_argument("likes", type=int, help="Update likes")
video_update_args.add_argument("views", type=int, help="Update views")



resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "likes": fields.Integer,
    "views": fields.Integer
}



class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        try:
            result = VideoModal.query.filter_by(id=video_id).first()
            return result
        except:
            abort(404, message="Error: A video with this id does not exist")    
        



    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        
        try:
            video = VideoModal(id=video_id, name=args["name"], likes=args["likes"], views=args["views"])
            db.session.add(video)
            db.session.commit()
            return video, 201
        except:
            abort(409, message="Error: There is already a video with this id")

 



    @marshal_with(resource_fields)
    def patch(self, video_id):

        args = video_update_args.parse_args()

        try:
            result = VideoModal.query.filter_by(id=video_id).first()

            if args["name"]:
                result.name = args['name']

            if args["likes"]:
                result.likes = args['likes']

            if args["views"]:
                result.likes = args['views']

            db.session.commit()
            
            return result

        except:
            abort(404, message="Error: A video with this id does not exist")





    @marshal_with(resource_fields)
    def delete(self, video_id):
        try:
            video_to_delete = VideoModal.query.filter_by(id=video_id).first()
            db.session.delete(video_to_delete)
            db.session.commit()
            return "", 204
        except:
            abort(404, message="Error: Delete request failed. A video with this id does not exist")    

        


api.add_resource(Video, "/video/<int:video_id>")


if __name__ == "__main__":
    app.run(debug=True)
