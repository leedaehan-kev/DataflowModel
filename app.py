import tensorflow.keras
import flask
import urllib.request
from PIL import Image, ImageOps
import numpy as np

app = flask.Flask(__name__)
model = None

#model load
def load_model():
    global model
    model = tensorflow.keras.models.load_model('./DataflowModel.h5')

#http://ip:port/api/predict -> skill
@app.route("/api/predict", methods=["POST"])
def api_predict():

    # UserRequest 중 발화를 req에 parsing.
    req = flask.request.get_json()
    req = req['action']['params']['secureimage']
    print(req)
    req = req[req.find("http://"):req.find('"expire"') - 3]
    print(req)
    
	# 이미지 전처리 - 발화가 jpg, png 확장자일 때만 실행
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
        
        msg = str(output)
        msg = msg + "단계입니다"

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
                                    "label": "사진보기",
                                    "webLinkUrl": req
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


if __name__ == "__main__":
    print("* Loading Keras model and Flask starting server...")
    print("please wait until server has fully started")
    load_model()
    app.run(host='0.0.0.0')