import flask
import sys
application = flask.Flask(__name__)

msg=[]

#http://ip:port/api/hello -> skill
@application.route("/api/hello",methods=["POST"])
def api_hello():
    global msg
    req=flask.request.get_json()
    msg=req['userRequest']['utterance']
    #mov=req['action']['clientExtra']['m1']
    print(req)
    #print(msg)
    #print(mov)
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


if __name__ == "__main__":
    application.run(host='0.0.0.0')
