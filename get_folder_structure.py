import json
import falcon
import re, os, math, time, sys, datetime
from io import BytesIO
from zipfile import ZipFile

ASSETS_FOLDER = os.path.join('assets', 'folder_structure')

## Logic

def gen_folder_structure(project_name, full_structure = True, language = 'fr'):
    """
    Generate folder structure based on language and full_structure options.
    
    Args:
        project_name: Name of the project
        full_structure: If True, include optional folders (01_Administratif/Administrative and 04_Publications/Publication)
        language: 'fr' for French or 'en' for English folder names
    """
    
    if language == 'fr':
        # Structure française
        base_structure = {
            '02_Donnees_brutes': None,
            '03_Traitement_donnees': {
                '01_Code': {'01_Templates': None},
                '02_Donnees_traitees': None
            }
        }
        
        if full_structure:
            base_structure = {
                '01_Administratif': {
                    '01_RH': None,
                    '02_Budget': None,
                    '03_PGD': None
                },
                **base_structure,
                '04_Publications': {
                    '01_Bibliographie': None,
                    '02_Texte_publication': None
                }
            }
    else:  # English
        base_structure = {
            '02_Raw_Data': None,
            '03_Data_processing': {
                '01_Code': {'01_Templates': None},
                '02_Processed_data': None
            }
        }
        
        if full_structure:
            base_structure = {
                '01_Administrative': {
                    '01_HR': None,
                    '02_Budget': None,
                    '03_DMP': None
                },
                **base_structure,
                '04_Publication': {
                    '01_Bibliography': None,
                    '02_Publication_text': None
                }
            }
    
    folder_structure = {project_name: base_structure}
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

def generate_git_ignore():
    """Generate a .gitignore file for the new folder structure"""
    gitignore_text = '''# Ignore all files
*
!.gitignore
!README.txt

# Keep code and templates
!03_Traitement_donnees/
03_Traitement_donnees/*
!03_Traitement_donnees/01_Code/
03_Traitement_donnees/01_Code/*
!03_Traitement_donnees/01_Code/01_Templates/
!03_Traitement_donnees/01_Code/01_Templates/*

!03_Data_processing/
03_Data_processing/*
!03_Data_processing/01_Code/
03_Data_processing/01_Code/*
!03_Data_processing/01_Code/01_Templates/
!03_Data_processing/01_Code/01_Templates/*
'''
    return gitignore_text

def generate_readme(language='fr'):
    """Generate a README file based on language"""
    filename = 'readme_fr.txt' if language == 'fr' else 'readme_en.txt'
    readme_path = os.path.join(ASSETS_FOLDER, 'readme_templates', filename)
    
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_text = f.read()
        return readme_text
    else:
        # Fallback si le fichier n'existe pas
        return "README.txt - Please add your project documentation here."

def generate_zip_in_memory(project_name, full_structure = True, save = False, include_git_ignore = True, 
                           templates = ['python_notebook', 'python_file', 'r_file', 'stata_file'], language='fr'):
    ## Generate folder
    folder_structure = gen_folder_structure(project_name, full_structure = full_structure, language=language)
    
    ## Create ZIP file with folders
    inMemoryOutputFile = BytesIO()
    zipFile = ZipFile(inMemoryOutputFile, 'w') 
    make_dirs_from_dict(folder_structure, zipFile)
    
    ### Add templates
    if templates:
        for template in templates:
            template_to_add = create_template(project_name, template)
            if template_to_add:
                # Templates go in 03_Traitement_donnees/01_Code/01_Templates or 03_Data_processing/01_Code/01_Templates
                templates_path = '03_Traitement_donnees/01_Code/01_Templates' if language == 'fr' else '03_Data_processing/01_Code/01_Templates'
                zipFile.writestr('{}/{}/{}'.format(project_name, templates_path, template_to_add[1]), template_to_add[0])
                    
    ### Add gitignore
    if include_git_ignore:
        gitignore = generate_git_ignore()
        zipFile.writestr('{}/.gitignore'.format(project_name), gitignore)
    
    ### Add README
    readme = generate_readme(language=language)
    zipFile.writestr('{}/README.txt'.format(project_name), readme)
                    
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
        language = req.get_param('language', default='fr')  # 'fr' or 'en'

        #project_name = 'demo_project'
        #full_structure = True
        #include_git_ignore = True
        #template_files_to_include = ['python_notebook', 'python_file', 'r_file', 'stata_file']
        #language = 'fr'

        resp.content_type = 'file/zip'
        resp.stream = generate_zip_in_memory(project_name, 
                                            full_structure = full_structure, 
                                            include_git_ignore = include_git_ignore, 
                                            templates = template_files_to_include,
                                            language = language)

        resp.downloadable_as = '{}_{}.zip'.format(project_name, time.strftime("%d-%m-%Y_%H-%M-%S"))
        resp.status  = falcon.HTTP_200