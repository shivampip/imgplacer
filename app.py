from flask import Flask, json, request, jsonify, send_file
from iengine import resize, paste_logo
from PIL import Image
from inputs import docs
import os 

app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    return jsonify({"message": "Hello World"})


@app.route("/resize", methods=["POST"])
def resize_img():
    mwidth = int(request.form["mwidth"])
    mheight = int(request.form["mheight"])
    logo = request.files["logo"]

    resized_img = resize(logo, mwidth, mheight)

    resized_img.save("out/resized_{}".format(logo.filename))

    # return jsonify({"message": "success"})
    return send_file("out/resized_{}".format(logo.filename))


@app.route("/test", methods=["POST"])
def test():
    logo = request.files["logo"]

    count = 0
    for doc in docs:
        name= os.path.splitext(doc["path"])[0]
        mwidth = doc["width"]
        mheight = doc["height"]
        print("Resizing logo==================")
        resized_img = resize(logo, mwidth, mheight,
                             doc["halign"], doc["valign"])
        resized_img.save("out/for_{}.png".format(name))
        print("Putting Logo on Doc============")
        paste_logo(doc, resized_img, count)

        count += 1

    return jsonify({"message": "success"})


if(__name__ == "__main__"):
    app.run(host="0.0.0.0", port=2001)
# https://www.image-map.net/
# 18001200
