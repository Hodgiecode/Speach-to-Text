from flask import Flask
import ffmpy
from wit import Wit
import os
import requests
from urllib.request import urlopen
from flask import request


app = Flask(__name__)


@app.route('/myfunc',methods=['GET', 'POST'])
def myfunc():
    ### считали строку
    arg1= request.args.get('url', default = '1', type = str)
    arg2 = request.args.get('id',default = '*', type = str)

    data = urlopen(arg1).read()

    with open('file_in.oga', 'wb') as f:
        f.write(data)

    ## конвертируем
    ff = ffmpy.FFmpeg(
        inputs={'file_in.oga': None},
        outputs={'file_out.wav': None}
    )

    ff.run()

    ## речь в звук
    access_token="WNUZ5JT2LMFVIQB4QXMWCX4LH6XUU34Z"
    client = Wit(access_token)
    resp = None
    with open('file_out.wav', 'rb') as f:
        resp = client.speech(f, None, {'Content-Type': 'audio/wav'})

    url_= 'https://api.telegram.org/bot1053711456:AAG4r3cVeVrTm1DYY_KIz950dLXLjhyy5d0/sendMessage?chat_id='+arg2+'&text='+str(resp['text'])
    requests.post(url_)
    os.remove("file_in.oga")
    os.remove("file_out.wav")
    return url_

if __name__ == '__main__':
    app.run()

