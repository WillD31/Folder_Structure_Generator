import falcon
from falcon_cors import CORS

from home import HomeResource
from alive import AliveResource
from get_folder_structure import GetFolderStructure

cors = CORS(allow_all_origins=True)
api = falcon.App(middleware=[cors.middleware])

Home = HomeResource()
api.add_route('/', Home)

Alive = AliveResource()
api.add_route('/alive', Alive)

FolderStructure = GetFolderStructure()
api.add_route('/get_folder_structure', FolderStructure)