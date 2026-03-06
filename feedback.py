import falcon
from stats_db import get_stats

class FeedbackResource(object):
    
    def on_get(self, req, resp):
        stats = get_stats()
        
        totals = stats['totals']
        monthly = stats['monthly']
        languages = stats['languages']
        
        monthly_table = "".join([f"<tr><td>{m[0]}</td><td>{m[1]}</td><td>{m[2]}</td></tr>" for m in monthly])
        lang_table = "".join([f"<tr><td>{l}</td><td>{v}</td></tr>" for l, v in languages.items()])
        
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.text = f'''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Statistiques d'utilisation</title>
    <style>
        body {{ font-family: sans-serif; background: #f0f2f5; padding: 40px; color: #333; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        h1 {{ color: #667eea; text-align: center; }}
        .card-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 30px 0; }}
        .card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; }}
        .card h2 {{ margin: 0; font-size: 2em; color: #764ba2; }}
        .card p {{ margin: 5px 0 0; color: #666; font-weight: bold; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #eee; }}
        th {{ background-color: #f8f9fa; color: #667eea; }}
        .back-link {{ display: block; text-align: center; margin-top: 30px; color: #667eea; text-decoration: none; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📈 Statistiques d'utilisation</h1>
        
        <div class="card-grid">
            <div class="card">
                <h2>{totals.get('connection', 0)}</h2>
                <p>Connexions au site</p>
            </div>
            <div class="card">
                <h2>{totals.get('generation', 0)}</h2>
                <p>Structures générées</p>
            </div>
        </div>

        <h3>Détail par mois</h3>
        <table>
            <thead>
                <tr>
                    <th>Mois</th>
                    <th>Type</th>
                    <th>Nombre</th>
                </tr>
            </thead>
            <tbody>
                {monthly_table}
            </tbody>
        </table>

        <h3>Générations par langue</h3>
        <table>
            <thead>
                <tr>
                    <th>Langue</th>
                    <th>Nombre</th>
                </tr>
            </thead>
            <tbody>
                {lang_table}
            </tbody>
        </table>

        <a href="/" class="back-link">← Retour au générateur</a>
    </div>
</body>
</html>'''
