#!/usr/bin/env python
import json
import openravepy
from flask import Flask, Blueprint, make_response, request, flash, redirect, url_for, send_from_directory, send_file
from werkzeug.utils import secure_filename
import pymongo
import os
from pathlib import Path
from .custom_logger import Logger

logger = Logger("server")

CONTAINER_NAME = os.getenv("CONTAINER_NAME")
WORKSPACE_PATH = Path(os.getenv("WORKSPACE"))

ROBOT_ZIP_PATH = WORKSPACE_PATH / "dep" / "collada_robots"
ROBOT_COLLECTION_PATH = WORKSPACE_PATH / "collection"
ROBOT_COLLECTION_BACKUP_PATH = WORKSPACE_PATH / "collection_backup"


def check_all_robot_format_transfered():
    if not ROBOT_ZIP_PATH.exists():
        logger.error("can not find the collada_robots path: %s",
                     {str(ROBOT_ZIP_PATH)})
        return False
    logger.info("found collada_robots path: %s", str(ROBOT_ZIP_PATH))
    zip_robot_files = list(ROBOT_ZIP_PATH.glob("*.zae"))

    if len(zip_robot_files) != len(list(ROBOT_COLLECTION_PATH.glob("*.json"))):
        num_of_files = 0
        logger.info("converting *.zae robot to *.json. ")
        env_ = openravepy.Environment()
        for file in zip_robot_files:
            env_ = openravepy.Environment()
            num_of_files += 1
            logger.info("processing %s" % str(file.stem))
            env_.Load(str(file))
            env_.Save(
                str(ROBOT_COLLECTION_PATH / "{}.json".format(str(file.stem))))
            # bodies = env_.GetBodies()
            # if len(bodies) != 0:
            #     for body in bodies:
            #         name = body.GetName()
            #         env_.RemoveKinBodyByName(name)
            env_.Destroy()

        logger.info("number of files loaded: %s", num_of_files)

    logger.info("all the *zae files are converted to *json. ")
    logger.info("json robot path: %s", str(ROBOT_COLLECTION_PATH))
    return True


# check_all_robot_format_transfered()
# exit(0)

bp = Blueprint("robot-api", CONTAINER_NAME)


def map_robot_to_dict(robot):
    return {
        "id": robot.GetId(),
        "name": robot.GetName(),
        "dof": robot.GetDOF(),
        "dof_values": robot.GetDOFValues(),
    }


@bp.route("/", methods=["GET"])
def get_all_robots():
    if request.method == "GET":
        robot_files = list(ROBOT_COLLECTION_PATH.glob("*.json"))
        payload = {}
        for fn in robot_files:
            logger.warning(str(fn))
            try:
                with open(str(fn), "r") as f:
                    robot_json = json.load(f, "utf-8")
                payload[str(fn.name)] = robot_json
            except ValueError as e:
                logger.error("file is malformatted, please check: %s" %
                             str(fn))
        return make_response({"message": "success", "payload": payload}, 200)


@bp.route("/<path:filename>", methods=["GET"])
def get_robot_by_filename(filename):
    if request.method == "GET":
        fn = (ROBOT_COLLECTION_PATH / filename)
        if not fn.exists():
            logger.warning("%s not found in collection. " % filename)
            return make_response({}, 200)

        try:
            logger.info("reading file: %s" % filename)
            with open(str(fn), "r") as f:
                payload = json.load(f, "utf-8")
            logger.info("successfully obtained file: %s" % filename)
            return make_response({
                "message": "success",
                "payload": payload
            }, 200)
        except ValueError as e:
            logger.error("%s" % e)
            return make_response(
                {
                    "errorCode": 500,
                    "message": "file exist, but failed to parse. "
                }, 500)


@bp.route("/<path:filename>/download", methods=["GET"])
def download_robot_file(filename):
    if request.method == "GET":
        fn = (ROBOT_COLLECTION_PATH / filename)
        if not fn.exists():
            logger.warning("%s not found in collection. " % filename)
            return make_response(
                {
                    "errorCode": 400,
                    "message": "file not found."
                }, 400)

        try:
            return send_from_directory(str(ROBOT_COLLECTION_PATH),
                                       filename=filename,
                                       as_attachment=True)
        except ValueError as e:
            logger.error("%s" % e)
            return make_response(
                {
                    "errorCode": 500,
                    "message": "file exist, but failed to parse. "
                }, 500)


# @bp.route("/", methods=["POST"])
# def upload():
#     if request.method == "POST":
#         return redirect(url_for('robot-api.upload'))


@bp.route("/", methods=["POST"])
def upload_robot_file():
    if request.method == "POST":
        logger.info("checking form data")

        if "file" not in request.files:
            redirect('/')
            return make_response(
                {
                    "error_code": 400,
                    "message": "file not exist"
                }, 400)
            # return redirect(request.url)

        logger.info("extracting file")
        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.

        if file.filename == "":
            logger.error("file name is empty")
            redirect('/')
            return make_response(
                {
                    "error_code": 400,
                    "message": "empty file name"
                }, 400)

        if file and str(Path(file.filename).suffix).lower() == ".json":
            # filename = secure_filename(file.filename)
            logger.info("saving ... ")
            filename = file.filename
            file.save(os.path.join(str(ROBOT_COLLECTION_PATH), filename))
            redirect('/')
            return make_response({"message": "success"}, 200)

        redirect('/')
        return make_response(
            {
                "error_code":
                422,
                "message":
                "empty file or file type is not allowed. use .json instead. "
            }, 422)


@bp.route("/<path:filename>", methods=["PUT"])
def update_robot_by_filename(filename):
    if request.method == "PUT":
        fn = (ROBOT_COLLECTION_PATH / filename)
        if not fn.exists():
            logger.error("%s not found in collection. " % filename)
            return make_response(
                {
                    "error_code": 400,
                    "message": "file not found in collection. "
                }, 400)
        try:
            logger.info("loading file: %s" % filename)
            with open(str(fn), "r") as f:
                robot = json.load(f, "utf-8")

            logger.info("updating file: %s" % filename)
            for key, val in request.json.items():
                robot[key] = val

            logger.info("saving file: %s" % filename)
            with open(str(fn), "w") as f:
                json.dump(robot, f, "utf-8")

            return make_response({
                "message": "success",
            }, 200)
        except ValueError as e:
            logger.error("%s" % e)
            return make_response(
                {
                    "errorCode": 500,
                    "message": "fail to update robot. "
                }, 500)


@bp.route("/<path:filename>", methods=["DELETE"])
def delete_robot_by_filename(filename):
    if request.method == "DELETE":
        fn = (ROBOT_COLLECTION_PATH / filename)
        if not fn.exists():
            logger.error("%s not found in collection. " % filename)
            return make_response({"message": "deleted"}, 200)
        try:
            fn.rename(ROBOT_COLLECTION_BACKUP_PATH / filename)
            return make_response({"message": "deleted"}, 200)
        except ValueError as e:
            logger.error("%s" % e)
            return make_response(
                {
                    "errorCode": 500,
                    "message": "fail to delete robot. "
                }, 500)


bp1 = Blueprint("upload-page", CONTAINER_NAME)


@bp1.route("/", methods=["GET"])
def upload_page():
    return """
<html>
   <body>
      <form action = "http://localhost:5000/api/robot" method = "POST" 
         enctype = "multipart/form-data">
         <input type = "file" name = "file" />
         <input type = "submit"/>
      </form>   
   </body>
</html>
    """


def create_app():
    app = Flask(__name__)

    app.config["UPLOAD_FOLDER"] = str(ROBOT_COLLECTION_PATH)
    app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024
    app.register_blueprint(bp, url_prefix="/api/robot")
    app.register_blueprint(bp1, url_prefix="")

    logger.info("Setting up server. ")
    return app


if __name__ == "__main__":
    create_app()

# env = openravepy.Environment()
# env.Load(str(ROBOT_ZIP_PATH / "barrett-hand.zae"))
# # env.SetViewer("qtcoin")
# # viewer = env.GetViewer()
# env.Save(str(ROBOT_JSON_PATH / "barrett-hand.json"))
# robot = env.GetRobots()[0]
# print(env.GetRobots())
# print(robot.GetDOF())
# print(robot.GetDof())

# import IPython
# IPython.embed()