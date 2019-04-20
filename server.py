import tornado.ioloop
import tornado.web
import requests
import json
import os
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class VoiceDictationHandler(tornado.web.RequestHandler):
    """
       请求语音服务
    """

    def post(self):
        resp = {}
        resp['code'] = 1
        resp['msg'] = '服务器开小差了'
        try:
            audio = self.get_body_argument('audio')
            url = ''
            data = {"audio": audio}
            response = requests.post(url, data=data)
            result = json.loads(response.text)
            # result = {}
            # result['code'] = 0
            # result['data'] = audio
            if result['code'] == 0:
                resp['code'] = 0
                resp['data'] = result['data']
            else:
                resp['code'] = 1
                resp['msg'] = result['msg']
        except Exception as e:
            logger.warning(e)

        self.write(resp)


app = tornado.web.Application(
    [
        (r"/", IndexHandler),
        (r"/voice_dictation", VoiceDictationHandler)
    ],
    static_path=os.path.join(os.path.dirname(__file__), "static")
)


if __name__ == '__main__':
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
