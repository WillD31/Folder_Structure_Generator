import falcon

class HomeResource(object):
    
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.text = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Folder Structure Generator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 700px;
            margin: 0 auto;
            background-color: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.2em;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
            line-height: 1.6;
        }
        
        .language-switch {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .language-switch button {
            background-color: #f0f0f0;
            border: 2px solid #ddd;
            padding: 8px 20px;
            margin: 0 5px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s;
        }
        
        .language-switch button.active {
            background-color: #667eea;
            color: white;
            border-color: #667eea;
        }
        
        .language-switch button:hover {
            transform: translateY(-2px);
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
            font-size: 15px;
        }
        
        input[type="text"] {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 15px;
            transition: border-color 0.3s;
        }
        
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .checkbox-group {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .checkbox-item {
            margin: 10px 0;
            display: flex;
            align-items: center;
        }
        
        input[type="checkbox"] {
            width: 20px;
            height: 20px;
            margin-right: 10px;
            cursor: pointer;
        }
        
        .checkbox-item label {
            margin-bottom: 0;
            cursor: pointer;
            font-weight: normal;
        }
        
        .download-btn {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 18px;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            transition: transform 0.3s, box-shadow 0.3s;
            margin-top: 20px;
        }
        
        .download-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        
        .download-btn:active {
            transform: translateY(0);
        }
        
        .tips {
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin-top: 30px;
            border-radius: 4px;
        }
        
        .tips h3 {
            color: #856404;
            margin-bottom: 10px;
            font-size: 16px;
        }
        
        .tips ul {
            margin-left: 20px;
            color: #856404;
        }
        
        .tips li {
            margin: 8px 0;
            line-height: 1.5;
        }
        
        .footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
            color: #666;
        }
        
        .footer a {
            color: #667eea;
            text-decoration: none;
        }
        
        .footer a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📁 Folder Structure Generator</h1>
        <p class="subtitle">Générateur de structure de répertoires pour projets de recherche</p>
        
        <div class="language-switch">
            <button class="active" onclick="switchLanguage('fr')">🇫🇷 Français</button>
            <button onclick="switchLanguage('en')">🇬🇧 English</button>
        </div>
        
        <form id="folderForm">
            <div class="form-group">
                <label for="projectName">Nom du projet :</label>
                <input type="text" id="projectName" name="project_name" 
                       placeholder="mon_projet_recherche" required>
            </div>
            
            <div class="form-group">
                <label>
                    <input type="checkbox" id="fullStructure" name="full_structure" checked>
                    <span id="fullStructureText">Inclure tous les dossiers (administrative, explorative, paper) ?</span>
                </label>
            </div>
            
            <div class="form-group">
                <label>
                    <input type="checkbox" id="gitignore" name="include_git_ignore" checked>
                    <span id="gitignoreText">Inclure un fichier .gitignore ?</span>
                </label>
            </div>
            
            <div class="form-group">
                <label id="templatesLabel">Modèles de fichiers à inclure :</label>
                <div class="checkbox-group">
                    <div class="checkbox-item">
                        <input type="checkbox" id="python_file" value="python_file" checked>
                        <label for="python_file">🐍 Python (.py)</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="python_notebook" value="python_notebook" checked>
                        <label for="python_notebook">📓 Jupyter Notebook (.ipynb)</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="r_file" value="r_file">
                        <label for="r_file">📊 R Script (.R)</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="stata_file" value="stata_file">
                        <label for="stata_file">📈 Stata (.do)</label>
                    </div>
                </div>
            </div>
            
            <button type="submit" class="download-btn">⬇️ Télécharger la structure</button>
        </form>
        
        <div class="tips">
            <h3>💡 Quelques conseils :</h3>
            <ul>
                <li>Utilisez des underscores (_) ou camelCase dans le nom du projet</li>
                <li>Pour les templates Stata/R, pensez à modifier manuellement la variable PROJECT_DIR</li>
                <li>"Inclure tous les dossiers" ajoute les dossiers administrative, explorative et paper</li>
            </ul>
        </div>
        
        <div class="footer">
            <p>API : <a href="/alive">/alive</a> | <a href="/get_folder_structure?project_name=demo&full_structure=1&include_git_ignore=1&templates=python_file">Exemple API</a></p>
            <p style="margin-top: 15px; font-size: 13px; color: #888;">
                Projet initial de <a href="https://www.tiesdekok.com/" target="_blank">Ties de Kok</a> - 
                Modifié par Virgile Jarrige (<a href="mailto:virgile.jarrige@unistra.fr">virgile.jarrige@unistra.fr</a>) - 
                <a href="https://github.com/WillD31/Folder_Structure_Generator" target="_blank">Dépôt GitHub</a>
            </p>
        </div>
    </div>
    
    <script>
        const translations = {
            fr: {
                title: '📁 Folder Structure Generator',
                subtitle: 'Générateur de structure de répertoires pour projets de recherche',
                projectName: 'Nom du projet :',
                projectPlaceholder: 'mon_projet_recherche',
                fullStructure: 'Inclure tous les dossiers (administrative, explorative, paper) ?',
                gitignore: 'Inclure un fichier .gitignore ?',
                templates: 'Modèles de fichiers à inclure :',
                download: '⬇️ Télécharger la structure',
                tips: '💡 Quelques conseils :',
                tip1: 'Utilisez des underscores (_) ou camelCase dans le nom du projet',
                tip2: 'Pour les templates Stata/R, pensez à modifier manuellement la variable PROJECT_DIR',
                tip3: '"Inclure tous les dossiers" ajoute les dossiers administrative, explorative et paper'
            },
            en: {
                title: '📁 Folder Structure Generator',
                subtitle: 'Research project folder structure generator',
                projectName: 'Project name:',
                projectPlaceholder: 'my_research_project',
                fullStructure: 'Include all folders (administrative, explorative, paper)?',
                gitignore: 'Include a .gitignore file?',
                templates: 'File templates to include:',
                download: '⬇️ Download Structure',
                tips: '💡 Some tips:',
                tip1: 'Use underscores (_) or camelCase in the project name',
                tip2: 'For Stata/R templates, remember to manually change the PROJECT_DIR variable',
                tip3: '"Include all folders" adds administrative, explorative, and paper folders'
            }
        };
        
        function switchLanguage(lang) {
            document.querySelectorAll('.language-switch button').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
            
            const t = translations[lang];
            
            // Apply all translations
            document.querySelector('h1').textContent = t.title;
            document.querySelector('.subtitle').textContent = t.subtitle;
            document.querySelector('label[for="projectName"]').textContent = t.projectName;
            document.getElementById('projectName').placeholder = t.projectPlaceholder;
            
            // Update checkbox labels text
            document.getElementById('fullStructureText').textContent = t.fullStructure;
            document.getElementById('gitignoreText').textContent = t.gitignore;
            
            // Update templates label
            document.getElementById('templatesLabel').textContent = t.templates;
            
            document.querySelector('.download-btn').textContent = t.download;
            document.querySelector('.tips h3').textContent = t.tips;
            
            const tipsList = document.querySelectorAll('.tips li');
            tipsList[0].textContent = t.tip1;
            tipsList[1].textContent = t.tip2;
            tipsList[2].textContent = t.tip3;
        }
        
        document.getElementById('folderForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const projectName = document.getElementById('projectName').value;
            const fullStructure = document.getElementById('fullStructure').checked ? '1' : '0';
            const gitignore = document.getElementById('gitignore').checked ? '1' : '0';
            
            const templates = [];
            document.querySelectorAll('.checkbox-group input[type="checkbox"]:checked').forEach(cb => {
                templates.push(cb.value);
            });
            
            let url = `/get_folder_structure?project_name=${encodeURIComponent(projectName)}&full_structure=${fullStructure}&include_git_ignore=${gitignore}`;
            
            if (templates.length > 0) {
                url += `&templates=${templates.join(',')}`;
            }
            
            window.location.href = url;
        });
    </script>
</body>
</html>
'''
