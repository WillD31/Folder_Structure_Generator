import json
import falcon
import re, os, math, time, sys, datetime
from io import BytesIO
from zipfile import ZipFile

ASSETS_FOLDER = os.path.join('api_server', 'assets', 'folder_structure')

## Logic

def gen_folder_structure(project_name, full_structure = True):
    if full_structure:
        folder_structure = {project_name : 
                                { 
                                'administrative' : None,
                                'empirical' : {'0_data' : {'credentials' : None,
                                                           'external' : None,
                                                           'manual' : None
                                                          }, 
                                               '1_code' : {'templates' : None}, 
                                               '2_pipeline' : None,
                                               '3_output' : {'data' : None,
                                                             'results' : None
                                                            }
                                              },
                                'explorative' : None,
                                'paper' : {'literature' : None, 
                                           'main_text' : None
                                          }
                               }
                           }
    else:
        folder_structure = {project_name : 
                                {'0_data' : 
                                 {
                                    'credentials' : None,
                                   'external' : None,
                                   'manual' : None
                                  }, 
                               '1_code' : {'templates' : None}, 
                               '2_pipeline' : None,
                               '3_output' : {
                                   'data' : None,
                                   'results' : None
                                    }
                               }
                           }
    return folder_structure

def make_dirs_from_dict(d, zipFile, project_dir=''):
    for key, val in d.items():
        zipFile.writestr(os.path.join(project_dir, key).replace('\\', '/') + '/', '')
        if type(val) == dict:
            make_dirs_from_dict(val, zipFile, project_dir = os.path.join(project_dir, key).replace('\\', '/'))

def create_template(project_name, template_type):
    template_dict = {'python_notebook' : 'start_template_jupyter.ipynb', 
                     'python_file' : 'start_template_python.py',
                    'r_file' : 'start_template_R.R', 
                    'stata_file' : 'start_template_stata.do'}
    if template_type in template_dict:
        with open(os.path.join(ASSETS_FOLDER, 'start_templates', template_dict[template_type]), 'r') as file:
            template = file.read()
        template = template.replace('<[{PROJECT}]>', project_name)
        return template, re.sub('^start_', '', template_dict[template_type])
    else:
        return None

def generate_git_ignore(full_structure = True):
    if full_structure:
        filename = 'start_gitignore.txt'
    else:
        filename = 'start_gitignore_slim.txt'
        
    with open(os.path.join(ASSETS_FOLDER, 'start_templates', filename), 'r') as f:
        gitignore_text = f.read()
    
    return gitignore_text

def generate_zip_in_memory(project_name, full_structure = True, save = False, include_git_ignore = True, 
                           templates = ['python_notebook', 'python_file', 'r_file', 'stata_file']):
    ## Generate folder
    folder_structure = gen_folder_structure(project_name, full_structure = full_structure)
    
    ## Create ZIP file with folders
    inMemoryOutputFile = BytesIO()
    zipFile = ZipFile(inMemoryOutputFile, 'w') 
    make_dirs_from_dict(folder_structure, zipFile)
    
    ### Add templates
    if templates:
        for template in templates:
            template_to_add = create_template(project_name, template)
            if template_to_add:
                if full_structure:
                    zipFile.writestr('{}/empirical/1_code/templates/{}'.format(project_name, template_to_add[1]), template_to_add[0])
                else:
                    zipFile.writestr('{}/1_code/templates/{}'.format(project_name, template_to_add[1]), template_to_add[0])
                    
    ### Add gitignore
    if include_git_ignore:
        gitignore = generate_git_ignore(full_structure=full_structure)
        if full_structure:
            zipFile.writestr('{}/.gitignore'.format(project_name), gitignore)
        else:
            zipFile.writestr('.gitignore', gitignore)
                    
    zipFile.close()
    inMemoryOutputFile.seek(0)
    
    ## Save ZIP
    if save:
        with open(project_name + '.zip', 'wb') as out:
            out.write(inMemoryOutputFile.read())
    else:
        return inMemoryOutputFile

## API part

class GetFolderStructure(object):
    
    def on_get(self, req, resp):

        project_name = req.get_param('project_name', required = True)
        full_structure = req.get_param_as_bool('full_structure', required = True)
        include_git_ignore = req.get_param_as_bool('include_git_ignore', required = True)  
        template_files_to_include = req.get_param_as_list('templates', required =  False)  

        #project_name = 'demo_project'
        #full_structure = True
        #include_git_ignore = True
        #template_files_to_include = ['python_notebook', 'python_file', 'r_file', 'stata_file']

        resp.content_type = 'file/zip'
        resp.stream = generate_zip_in_memory(project_name, 
                                            full_structure = full_structure, 
                                            include_git_ignore = include_git_ignore, 
                                            templates = template_files_to_include)

        resp.downloadable_as = 'folder_structure_{}.zip'.format(time.strftime("%d-%m-%Y %H:%M:%S"))
        resp.status  = falcon.HTTP_200