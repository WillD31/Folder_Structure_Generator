import falcon
from falcon_cors import CORS

from .get_excel import Resource
from .alive import AliveResource
from .get_folder_structure import GetFolderStructure

cors = CORS(allow_all_origins=True)
api = falcon.API(middleware=[cors.middleware])

Alive = AliveResource()
api.add_route('/alive', Alive)

FolderStructure = GetFolderStructure()
api.add_route('/get_folder_structure', FolderStructure)