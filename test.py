import tensorflow.keras
import flask
import urllib.request
#import cv2
from keras.preprocessing.image import ImageDataGenerator
from PIL import Image, ImageOps
import numpy as np

test = flask.Flask(__name__)
model = None
binModel = None

'''
def cropping_bgd(img):
    height, width = img.shape[0:2]
    rect = (0, 0, width-1, height-1)
    print(rect)
    mask = np.zeros(img.shape[:2], np.uint8)
    cv2.grabCut(img, mask, rect, None, None, 5, cv2.GC_INIT_WITH_RECT)
    mask_2 = np.where((mask==2) | (mask==0), 0, 1).astype('uint8')
    fix_img = img * mask_2[:, :, np.newaxis]
    return fix_img
'''

#model load
def load_model():
    global model, binModel
    model = tensorflow.keras.models.load_model('./DataflowModel.h5')
    binModel = tensorflow.keras.models.load_model('./BinaryModel.h5')

#http://ip:port/api/predict -> skill
@test.route("/api/predict", methods=["POST"])
def api_predict():
    # 이미지 증강(size = 10)
    img_generator = ImageDataGenerator(
            rotation_range = 10,
            #zoom_range=0.10,
            shear_range = 0.5,
            width_shift_range = 0.10,
            height_shift_range = 0.10,
            horizontal_flip = True,
            vertical_flip = False)
    # UserRequest 중 발화를 req에 parsing.
    req = flask.request.get_json()
    req = req['action']['params']['secureimage']
    req = req[req.find("http://"):req.find('"expire"') - 3]
    
	# 이미지 전처리 - 발화가 jpg, png 확장자일 때만 실행
    if 'jpg' in req or 'png' in req:
        np.set_printoptions(suppress=True)	#소수점 제거
        urllib.request.urlretrieve(req, 'img')	#img load
        image = Image.open('img').convert('RGB')
        size = (150, 150)
        image = ImageOps.fit(image, size, Image.ANTIALIAS) #방향값 제거, 안티앨리어싱
        #배경제거
        #img = cv2.imread('./img')
        #img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #img_cropping = cropping_bgd(img_RGB)
        #image = cv2.resize(img_cropping, (150,150)) 
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 255.0)	#normalizing
        data = np.ndarray(shape=(1, 150, 150, 3), dtype=np.float32)	#reshape
        data[0] = normalized_image_array
        prediction = binModel.predict(data)		#binary model, 정수리 사진인지 확인
        print(prediction[0])
        if(prediction[0] < 0.5):
            augment_size = 4
            x_augmented=img_generator.flow(np.tile(data[0].reshape(150*150*3),augment_size).reshape(-1,150,150,3),np.zeros(augment_size),batch_size=augment_size,shuffle=False).next()[0]
            print(x_augmented.shape)
            prediction = model.predict(x_augmented)
            pred = np.argmax(prediction, axis=-1)
            output = np.mean(pred)
            print(output)
            msg = str(output)
            msg = msg + "단계입니다"      
        else:
            msg = "올바른 이미지를 업로드해주세요."
        print(msg)
        
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
    test.run(host='0.0.0.0')