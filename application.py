import flask
import sys

application = flask.Flask(__name__)

users = {}

#nosql -> user의 정보를 json
#JSON Tree
#{Users:
#	{User_ID:
#		[value1, value2]
#	}
#}
#Users -> {'User_ID1', 'User_ID2', ...}
#Users['User_ID'] -> [value1, value2, ...]
#update -> {} 추가, pop -> {} 제거, append -> [] 추가
#Hello Block에서 호출
@application.route("/api/user",methods=["POST"])
def api_user():
    global users
    req=flask.request.get_json()
    user_id = req['userRequest']['user']['id']
    json = {}
    json[user_id] = []
    users.update(json)
    print(users)
    return req

#key:val, value:필요한 값
#value 가져오기
#http://ip:port/api/val -> skill
@application.route("/api/val",methods=["POST"])
def api_val():
    global users
    req=flask.request.get_json()
    user_id = req['userRequest']['user']['id']
    users[user_id].append(req['action']['clientExtra']['val'])
    print(users)
    return req

#결과 출력
@application.route("/api/result",methods=["POST"])
def api_result():
    global users
    req=flask.request.get_json()
    user_id = req['userRequest']['user']['id']
    msg=''
    for i in users[user_id]:
        msg+=i+'\n'
    print(msg)
    print(users)
    users.pop(user_id)
    res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": msg
                        }
                    }
                ]
            }
        }
    return flask.jsonify(res)


#http://ip:port/api/hello -> skill
@application.route("/api/hello",methods=["POST"])
def api_hello():
    req=flask.request.get_json()
    msg=req['userRequest']['utterance']
    print(req)
    res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": msg+"TEST"
                        }
                    }
                ]
            }
        }
    return flask.jsonify(res)

if __name__ == "__main__":
    application.run(host='0.0.0.0')
    
''' #json 추출
@application.route("/api/user",methods=["POST"])
def api_user():
    global val, user_count
    req=flask.request.get_json()
    json = {}
    user_id = req['userRequest']['user']['id']
    json[user_id] = []
    json[user_id].append("test")
    json[user_id].append("test2")
    user_count += 1
    print(json)
    for i in json[user_id]:
        print(i)
    val.update(json)
    print(val)
    print(val[user_id])
    val.pop(user_id)
    print(val)
    return req
'''
    

'''
#http://ip:port/api/move1 -> skill
@application.route("/api/move1",methods=["POST"])
def api_move1():
    global msg
    req=flask.request.get_json()
    #msg=req['userRequest']['utterance']
    mov=req['action']['clientExtra']['m1']
    conval=req['contexts'][0]['params']['hello_var']['resolvedValue']
    con=req['contexts']
    print(conval)
    print(con)
    #print(msg)
    #print(mov)
    res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": msg+"TEST\n"+mov
                        }
                    }
                ]
            }
        }
    return flask.jsonify(res)
'''