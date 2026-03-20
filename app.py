import falcon
import json
from falcon_cors import CORS
from falcon_swagger_ui import register_swaggerui_app

from home import HomeResource
from alive import AliveResource
from get_folder_structure import GetFolderStructure
from feedback import FeedbackResource

cors = CORS(allow_all_origins=True)
api = falcon.App(middleware=[cors.middleware])

# Enable comma-separated query string parsing for lists
api.req_options.auto_parse_qs_csv = True

class OpenApiSpecResource(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'application/json'
        with open('openapi.json', 'r') as f:
            resp.text = f.read()

SWAGGERUI_URL = '/docs'
SCHEMA_URL = '/openapi.json'

register_swaggerui_app(
    api, SWAGGERUI_URL, SCHEMA_URL,
    page_title='Folder Structure API Docs',
    favicon_url='https://falconframework.org/favicon-32x32.png',
    config={'supportedSubmitMethods': ['get']}
)

api.add_route(SCHEMA_URL, OpenApiSpecResource())

Home = HomeResource()
api.add_route('/', Home)

Alive = AliveResource()
api.add_route('/alive', Alive)

FolderStructure = GetFolderStructure()
api.add_route('/get_folder_structure', FolderStructure)
Feedback = FeedbackResource()
api.add_route('/feedback/', Feedback)
