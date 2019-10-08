from flask import Flask
import ffmpy
from wit import Wit
import os
import requests
from urllib.request import urlopen


app = Flask(__name__)


@app.route('/')
def myfunc():
    ### считали строку
    cid=""

    data = urlopen("https://drive.google.com/uc?export=download&id=1Eker9jD9iC4QPEfBbV0SZ1hSDq1ZsdXq")
	##В файле 2 строки разделенных '\n' url и chatid

    i=0
    for line in data:
        if i==0:
            inf=line.decode("utf-8").rstrip()
        if i==1:
            cid=line.decode("utf-8").rstrip()

        i=i+1

    ## конвертируем
    ff = ffmpy.FFmpeg(
        inputs={inf: None},
        outputs={'file_super.wav': None}
    )

    ff.run()

    ### речь в звук
    access_token="XXXXXX"
    client = Wit(access_token)
    resp = None
    with open('file_super.wav', 'rb') as f:
        resp = client.speech(f, None, {'Content-Type': 'audio/wav'})

    url_= 'https://api.telegram.org/botID/sendMessage?chat_id='+cid+'&text='+str(resp['_text'])
    requests.post(url_)
    os.remove("file_super.wav")
    return url_



if __name__ == '__main__':
    app.run()




