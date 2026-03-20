import falcon

class HomeResource(object):
    
    def on_get(self, req, resp):
        from stats_db import log_event, get_identifier
        identifier = get_identifier(req)
        log_event('connection', identifier=identifier)
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
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .container {
            width: 95%;
            max-width: 1400px;
            margin: 0 auto;
            background-color: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            display: flex;
            gap: 40px;
            transition: all 0.3s ease;
        }

        .main-content {
            flex: 1;
            min-width: 300px;
        }

        .preview-panel {
            flex: 1;
            background-color: #f8f9fa;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            padding: 25px;
            display: flex;
            flex-direction: column;
        }

        @media (max-width: 1024px) {
            .container {
                flex-direction: column;
                width: 95%;
                padding: 25px;
            }
            .preview-panel {
                display: none;
            }
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
        
        /* Tree Preview Styles */
        .preview-title {
            font-weight: bold;
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.2em;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .tree {
            font-family: 'Courier New', Courier, monospace;
            font-size: 14px;
            color: #444;
            line-height: 1.5;
            overflow-y: auto;
        }

        .tree-item {
            display: flex;
            align-items: center;
            gap: 8px;
            margin: 2px 0;
        }

        .tree-folder { color: #f39c12; font-weight: bold; }
        .tree-file { color: #555; }
        .tree-indent { margin-left: 20px; border-left: 1px dashed #ccc; padding-left: 10px; }

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
        <div class="main-content">
            <h1 id="mainTitle">📁 Folder Structure Generator</h1>
            <p class="subtitle" id="mainSubtitle">Générateur de structure de répertoires pour projets de recherche</p>
            
            <div class="language-switch">
                <button class="active" onclick="switchLanguage('fr')">🇫🇷 Français</button>
                <button onclick="switchLanguage('en')">🇬🇧 English</button>
            </div>
            
            <form id="folderForm">
                <div class="form-group">
                    <label for="projectName" id="labelProjectName">Nom du projet :</label>
                    <input type="text" id="projectName" name="project_name" 
                           placeholder="mon_projet_recherche" required maxlength="100">
                </div>
                
                <div class="form-group">
                    <label>
                        <input type="checkbox" id="fullStructure" name="full_structure" checked>
                        <span id="fullStructureText">Inclure tous les dossiers (01_Administratif, 04_Publication) ?</span>
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
                <h3 id="tipsTitle">💡 Quelques conseils :</h3>
                <ul>
                    <li id="tipItem1">Utilisez des underscores (_) ou notationChameau (mots collés avec majuscules) dans le nom du projet</li>
                </ul>
            </div>
            
            <div class="footer">
                <p>API : <a href="/alive">/alive</a> | <a id="docsLink" href="/docs#/default/">Documentation API (Swagger)</a> | <a id="statsLink" href="/feedback/">Statistiques</a></p>
                <p id="footerText" style="margin-top: 15px; font-size: 13px; color: #888; line-height: 1.5;">
                    <!-- Content injected by JS -->
                </p>
                <p id="privacyText" style="margin-top: 10px; font-size: 12px; color: #aaa; font-style: italic;">
                    <!-- Content injected by JS -->
                </p>
            </div>
        </div>

        <div class="preview-panel">
            <div class="preview-title">
                <span>🔍</span> <span id="previewLabel">Prévisualisation de la structure</span>
            </div>
            <div id="structurePreview" class="tree">
                <!-- Tree will be injected here -->
            </div>
        </div>
    </div>
    
    <script>
        let currentLanguage = 'fr';
        
        const translations = {
            fr: {
                title: '📁 Folder Structure Generator',
                subtitle: 'Générateur de structure de répertoires pour projets de recherche',
                projectName: 'Nom du projet :',
                projectPlaceholder: 'mon_projet_recherche',
                fullStructure: 'Inclure tous les dossiers (01_Administratif, 04_Publication) ?',
                gitignore: 'Inclure un fichier .gitignore ?',
                templates: 'Modèles de fichiers à inclure :',
                download: '⬇️ Télécharger la structure',
                tips: '💡 Quelques conseils :',
                tip1: 'Utilisez des underscores (_) ou notationChameau (mots collés avec majuscules) dans le nom du projet',
                footer: 'Proposé par le groupe de travail "outils applicatifs communs" <br />du réseau des <a href="https://recherche.data.gouv.fr/fr/ateliers-de-la-donnee" target="_blank">ateliers de la donnée</a> <br />avec le soutien de <a href="https://recherche.data.gouv.fr" target="_blank">Recherche Data Gouv</a>.<br/><br/>Projet initial de <a href="https://www.tiesdekok.com/" target="_blank">Ties de Kok</a> <br/> Modifié par Virgile Jarrige (<a href="mailto:virgile.jarrige@unistra.fr">virgile.jarrige@unistra.fr</a>) <br />et William Demet (<a href="mailto:william.demet@ut-capitole.fr">william.demet@ut-capitole.fr</a>) <br/> <br /><a href="https://github.com/WillD31/Folder_Structure_Generator" target="_blank">Dépôt GitHub</a><br/><br/>Hébergé par le <a href="https://eu-eosc-vm.unistra.fr/" target="_blank">noeud EU EOSC - Virtual Machines</a>',
                docs: 'Documentation API (Swagger)',
                stats: 'Statistiques',
                privacy: 'Aucune donnée personnelle n’est conservée sur ce serveur.',
                preview: 'Prévisualisation de la structure'
            },
            en: {
                title: '📁 Folder Structure Generator',
                subtitle: 'Research project folder structure generator',
                projectName: 'Project name:',
                projectPlaceholder: 'my_research_project',
                fullStructure: 'Include all folders (01_Administrative, 04_Publication)?',
                gitignore: 'Include a .gitignore file?',
                templates: 'File templates to include:',
                download: '⬇️ Download Structure',
                tips: '💡 Some tips:',
                tip1: 'Use underscores (_) or camelCase in the project name',
                footer: 'Proposed by the "common application tools" working group <br />of the <a href="https://recherche.data.gouv.fr/en/data-management-cluster" target="_blank">data managment clusters network</a> <br /> with the support of <a href="https://recherche.data.gouv.fr" target="_blank">Recherche Data Gouv</a>.<br/><br/>Original project by <a href="https://www.tiesdekok.com/" target="_blank">Ties de Kok</a> <br/> Modified by Virgile Jarrige (<a href="mailto:virgile.jarrige@unistra.fr">virgile.jarrige@unistra.fr</a>) <br />and William Demet (<a href="mailto:william.demet@ut-capitole.fr">william.demet@ut-capitole.fr</a>) <br/> <br /><a href="https://github.com/WillD31/Folder_Structure_Generator" target="_blank">GitHub Repository</a><br/><br/>Hosted by the <a href="https://eu-eosc-vm.unistra.fr/" target="_blank">EU EOSC - Virtual Machines node</a>',
                docs: 'API Documentation (Swagger)',
                stats: 'Statistics',
                privacy: 'No personal data is stored on this server.',
                preview: 'Folder Structure Preview'
            }
        };
        
        function switchLanguage(lang) {
            currentLanguage = lang;
            
            document.querySelectorAll('.language-switch button').forEach(btn => {
                btn.classList.remove('active');
            });
            
            document.querySelectorAll('.language-switch button').forEach(btn => {
                if (btn.textContent.includes(lang === 'fr' ? 'Français' : 'English')) {
                    btn.classList.add('active');
                }
            });
            
            const t = translations[lang];
            
            document.getElementById('mainTitle').textContent = t.title;
            document.getElementById('mainSubtitle').textContent = t.subtitle;
            document.getElementById('labelProjectName').textContent = t.projectName;
            document.getElementById('projectName').placeholder = t.projectPlaceholder;
            document.getElementById('fullStructureText').textContent = t.fullStructure;
            document.getElementById('gitignoreText').textContent = t.gitignore;
            document.getElementById('templatesLabel').textContent = t.templates;
            document.querySelector('.download-btn').textContent = t.download;
            document.getElementById('tipsTitle').textContent = t.tips;
            document.getElementById('tipItem1').textContent = t.tip1;
            document.getElementById('footerText').innerHTML = t.footer;
            document.getElementById('docsLink').textContent = t.docs;
            document.getElementById('statsLink').textContent = t.stats;
            document.getElementById('statsLink').href = `/feedback/?lang=${lang}`;
            document.getElementById('privacyText').textContent = t.privacy;
            document.getElementById('previewLabel').textContent = t.preview;
            
            updatePreview();
        }

        function updatePreview() {
            const projectName = document.getElementById('projectName').value || '{project_name}';
            const isFull = document.getElementById('fullStructure').checked;
            const hasGitignore = document.getElementById('gitignore').checked;
            
            const templates = [];
            document.querySelectorAll('.checkbox-group input[type="checkbox"]:checked').forEach(cb => {
                templates.push(cb.value);
            });

            const previewDiv = document.getElementById('structurePreview');
            previewDiv.innerHTML = '';

            // Helper to add item
            const addItem = (name, type, level) => {
                const item = document.createElement('div');
                item.className = 'tree-item';
                item.style.marginLeft = (level * 20) + 'px';
                
                const icon = type === 'folder' ? '📁' : '📄';
                const spanClass = type === 'folder' ? 'tree-folder' : 'tree-file';
                
                item.innerHTML = `<span>${icon}</span><span class="${spanClass}">${name}</span>`;
                previewDiv.appendChild(item);
            };

            // Root
            addItem(projectName + '/', 'folder', 0);

            // 01 Admin
            if (isFull) {
                const adminName = currentLanguage === 'fr' ? '01_Administratif' : '01_Administrative';
                addItem(adminName + '/', 'folder', 1);
                addItem((currentLanguage === 'fr' ? '01_RH' : '01_HR') + '/', 'folder', 2);
                addItem('02_Budget/', 'folder', 2);
                addItem((currentLanguage === 'fr' ? '03_PGD' : '03_DMP') + '/', 'folder', 2);
            }

            // 02 Raw Data
            const rawName = currentLanguage === 'fr' ? '02_Donnees_brutes' : '02_Raw_Data';
            addItem(rawName + '/', 'folder', 1);

            // 03 Processing
            const procName = currentLanguage === 'fr' ? '03_Traitement_donnees' : '03_Data_processing';
            addItem(procName + '/', 'folder', 1);
            
            // 03 sub folder Code
            addItem('01_Code/', 'folder', 2);
            addItem('01_Templates/', 'folder', 3);
            
            const templateFiles = {
                'python_notebook': 'template_jupyter.ipynb',
                'python_file': 'template_python.py',
                'r_file': 'template_R.R',
                'stata_file': 'template_stata.do'
            };

            templates.forEach(t => {
                if (templateFiles[t]) {
                    addItem(templateFiles[t], 'file', 4);
                }
            });

            // 03 sub folder Data
            addItem((currentLanguage === 'fr' ? '02_Donnees_traitees' : '02_Processed_data') + '/', 'folder', 2);

            // 04 Publication
            if (isFull) {
                const pubName = currentLanguage === 'fr' ? '04_Publications' : '04_Publication';
                addItem(pubName + '/', 'folder', 1);
                addItem((currentLanguage === 'fr' ? '01_Bibliographie' : '01_Bibliography') + '/', 'folder', 2);
                addItem((currentLanguage === 'fr' ? '02_Texte_publication' : '02_Publication_text') + '/', 'folder', 2);
            }

            // Other root files
            if (hasGitignore) addItem('.gitignore', 'file', 1);
            addItem('README.txt', 'file', 1);
        }

        // Event listeners for real-time update
        document.getElementById('projectName').addEventListener('input', updatePreview);
        document.getElementById('fullStructure').addEventListener('change', updatePreview);
        document.getElementById('gitignore').addEventListener('change', updatePreview);
        document.querySelectorAll('.checkbox-group input').forEach(el => {
            el.addEventListener('change', updatePreview);
        });

        // Detect browser language and initialize
        const userLang = navigator.language || navigator.userLanguage; 
        const initialLang = userLang.startsWith('fr') ? 'fr' : 'en';
        switchLanguage(initialLang);
        
        document.getElementById('folderForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const projectName = document.getElementById('projectName').value;
            const fullStructure = document.getElementById('fullStructure').checked ? '1' : '0';
            const gitignore = document.getElementById('gitignore').checked ? '1' : '0';
            const templates = [];
            document.querySelectorAll('.checkbox-group input[type="checkbox"]:checked').forEach(cb => {
                templates.push(cb.value);
            });
            let url = `/get_folder_structure?project_name=${encodeURIComponent(projectName)}&full_structure=${fullStructure}&include_git_ignore=${gitignore}&language=${currentLanguage}`;
            if (templates.length > 0) {
                url += `&templates=${templates.join(',')}`;
            }
            window.location.href = url;
        });
    </script>
</body>
</html>
'''
