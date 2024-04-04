import json
import falcon
import os

class AliveResource(object):
    
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200 
        resp.body = ('It is alive! {}'.format(os.getcwd()))
