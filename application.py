import flask
import sys
application = flask.Flask(__name__)

val=[]

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

#key:val, value:필요한 값
#value 가져오기
#http://ip:port/api/val -> skill
@application.route("/api/val",methods=["POST"])
def api_val():
    global val
    req=flask.request.get_json()
    print(req)
    val.append(req['action']['clientExtra']['val'])
    print(req['action']['clientExtra']['val'])
    return req

#결과 출력
@application.route("/api/result",methods=["POST"])
def api_result():
    global val
    req=flask.request.get_json()
    msg=''
    for i in val:
        msg+=i+'\n'
    print(msg)
    val=[]
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


if __name__ == "__main__":
    application.run(host='0.0.0.0')
    

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