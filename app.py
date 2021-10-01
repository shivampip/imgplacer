from flask import Flask, json, request, jsonify, send_file
from iengine import resize, paste_logo
from PIL import Image
import os
import json
import time
from datetime import datetime


# ========================================================
# output_dir = "/home/u4-0dm1dehw5e1g/www/businessready.miraeassetmf.co.in/public_html/resized_imgs/output"
# input_json_path = "/home/u4-0dm1dehw5e1g/www/businessready.miraeassetmf.co.in/public_html/resized_imgs/inputs.json"
# docs_path = "/home/u4-0dm1dehw5e1g/www/businessready.miraeassetmf.co.in/public_html/resized_imgs/docs"
output_dir = "./out"
input_json_path = "./inputs.json"

update_fq = 20  # seconds
# ========================================================


app = Flask(__name__)

ts = 0
idocs = {"docs": []}


def get_timename():
    now = datetime.now()
    return now.strftime("%Y_%m_%d___%H_%M_%S")


@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Hello World From Image Resizer"})


@app.route("/resize", methods=["POST"])
def resize_img():
    mwidth = int(request.form["mwidth"])
    mheight = int(request.form["mheight"])
    logo = request.files["logo"]

    resized_img = resize(logo, mwidth, mheight)

    resized_img.save("out/resized_{}".format(logo.filename))

    # return jsonify({"message": "success"})
    return send_file("out/resized_{}".format(logo.filename))


@app.route("/test_disabled", methods=["POST"])
def test():
    global ts
    global idocs
    logo = request.files["logo"]

    cts = time.time()
    if cts - update_fq > ts:
        ts = cts
        print("======================Reading files=====================")

        idocs_file = open(
            "./inputs.json",
        )
        idocs = json.load(idocs_file)

    count = 0
    for doc in idocs["docs"]:
        name = os.path.splitext(doc["path"])[0]
        mwidth = doc["width"]
        mheight = doc["height"]
        print("Resizing logo==================")
        resized_img = resize(logo, mwidth, mheight, doc["halign"], doc["valign"])
        resized_img.save("out/for_{}.png".format(name))
        print("Putting Logo on Doc============")
        paste_logo(doc, resized_img, count)

        count += 1

    return jsonify({"message": "success"})


@app.route("/resize_all", methods=["POST"])
def resize_all():
    global ts
    global idocs

    if "logo" not in request.files:
        return jsonify({"status": "error", "message": "logo file not provided"})

    logo = request.files["logo"]
    # logoname = request.form.get("folder_name")

    # if not logoname:
    #     logoname = os.path.splitext(logo.filename)[0]

    msg = ""

    cts = time.time()
    if cts - update_fq > ts:
        print("======================Reading files=====================")
        try:
            idocs_file = open(
                input_json_path,
            )
            idocs = json.load(idocs_file)
            ts = cts
        except OSError:
            msg = "JSON file not found"
        except ValueError:
            msg = "Incorrect json file format"
        if msg == "":
            msg = "Total docs updated: {}".format(len(idocs["docs"]))

    # out_folder = os.path.join(output_dir, logoname)
    # try:
    #     os.makedirs(out_folder)
    # except OSError as error:
    #     print(error)

    out_paths = {}
    timename = get_timename()
    for doc in idocs["docs"]:
        name = os.path.splitext(doc["path"])[0]
        resized_img = resize(
            logo, doc["width"], doc["height"], doc["halign"], doc["valign"]
        )
        filename = "{}__{}.png".format(timename, name)
        out_path = os.path.join(output_dir, filename)
        resized_img.save(out_path)
        out_paths[doc["path"]] = filename

    return jsonify({"status": "success", "message": msg, "paths": out_paths})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3501)
# https://www.image-map.net/
# 18001200


9425604658
