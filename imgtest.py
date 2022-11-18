import tensorflow.keras
import flask
from flask import render_template
import urllib.request
from PIL import Image, ImageOps
import numpy as np

app = flask.Flask(__name__)
model = None

users = {}

#model load
def load_model():
    global model
    model = tensorflow.keras.models.load_model('./DataflowModel.h5')

@app.route("/api/img", methods=["POST"])
def api_img():
    global users
    req = flask.request.get_json()
    user_id = req['userRequest']['user']['id']
    json = {}
    json[user_id]={}
    json[user_id].update({"image":[]})
    users.update(json)
    
    req = req['userRequest']['utterance']
    if 'jpg' in req or 'png' in req:
        np.set_printoptions(suppress=True)	#소수점 제거
        urllib.request.urlretrieve(req, 'img')	#img load
        image = Image.open('img').convert('RGB')
        size = (150, 150)
        image = ImageOps.fit(image, size, Image.ANTIALIAS) #방향값 제거, 안티앨리어싱
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 255.0)	#normalizing
        data = np.ndarray(shape=(1, 150, 150, 3), dtype=np.float32)	#reshape
        data[0] = normalized_image_array
        prediction = model.predict(data)	#예측
        output = np.argmax(prediction, axis=-1)	#가장 높은 예측값
        
        for i in prediction[0]:
            users[user_id]["image"].append(str(int(i*100))+"%")
        users[user_id]["image"].append(str(output[0]*20+10)+"%")
        users[user_id]["image"].append(output[0])
        users[user_id]["image"].append(req)
        print(users)
        msg = str(output[0])
        msg = msg + "단계입니다"
        imgURL="https://dataflowtest-notice6143.run.goorm.io/image-result/" + user_id
		# basic card format
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "basicCard": {
                            "title": msg,
                            "description": "",
                            "thumbnail": {
                                "imageUrl": req
                            },
                            "buttons": [
                                {
                                    "action":  "webLink",
                                    "label": "상세정보",
                                    "webLinkUrl": imgURL
                                }
                            ]
                        }
                    }
                ]
            }
        }        
    else:
    	# simple text format
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "사진을 보내주세요"
                        }
                    }
                ]
            }
        }
    print(res)
    return flask.jsonify(res)


@app.route('/input/<int:num>')
def input(num):
    name = ''
    if num == 1:
        name = '1'
    elif num == 2:
        name = '2'
    elif num == 3:
        name = '3'
    return "hello {}".format(name)

@app.route('/image-result/<string:id>')
def print_url(id):
    global users
    print(id)
    return render_template("img.html",img_output=users[id]["image"])
  
if __name__ == "__main__":
    print("* Loading Keras model and Flask starting server...")
    print("please wait until server has fully started")
    load_model()
    app.run(host='0.0.0.0')