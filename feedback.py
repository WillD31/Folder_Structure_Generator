import falcon
from stats_db import get_stats

class FeedbackResource(object):
    
    def on_get(self, req, resp):
        stats = get_stats()
        
        # Detect language (Accept-Language or param)
        accept_lang = req.headers.get('ACCEPT-LANGUAGE', '')
        lang = req.get_param('lang')
        if not lang:
            lang = 'fr' if 'fr' in accept_lang.lower() else 'en'
            
        translations = {
            'fr': {
                'title': '📈 Statistiques d’utilisation',
                'conn': 'Connexions au site',
                'gen': 'Structures générées',
                'monthly': 'Détail par mois',
                'month': 'Mois',
                'type': 'Type',
                'count': 'Nombre',
                'by_lang': 'Générations par langue',
                'language': 'Langue',
                'back': '← Retour au générateur',
                'conn_label': 'Connexion',
                'gen_label': 'Génération'
            },
            'en': {
                'title': '📈 Usage Statistics',
                'conn': 'Site connections',
                'gen': 'Folders generated',
                'monthly': 'Monthly detail',
                'month': 'Month',
                'type': 'Type',
                'count': 'Count',
                'by_lang': 'Generations by language',
                'language': 'Language',
                'back': '← Back to generator',
                'conn_label': 'Connection',
                'gen_label': 'Generation'
            }
        }
        
        t = translations.get(lang, translations['en'])
        
        totals = stats['totals']
        monthly = stats['monthly']
        languages = stats['languages']
        
        def translate_type(etype):
            if etype == 'connection': return t['conn_label']
            if etype == 'generation': return t['gen_label']
            return etype

        monthly_table = "".join([f"<tr><td>{m[0]}</td><td>{translate_type(m[1])}</td><td>{m[2]}</td></tr>" for m in monthly])
        lang_table = "".join([f"<tr><td>{l.upper()}</td><td>{v}</td></tr>" for l, v in languages.items()])
        
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.text = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{t['title']}</title>
    <style>
        body {{ font-family: sans-serif; background: #f0f2f5; padding: 40px; color: #333; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        h1 {{ color: #667eea; text-align: center; }}
        .lang-switch {{ text-align: right; margin-bottom: 10px; }}
        .lang-switch a {{ text-decoration: none; font-size: 14px; color: #667eea; margin-left: 10px; font-weight: bold; }}
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
        <div class="lang-switch">
            <a href="?lang=fr">🇫🇷 FR</a>
            <a href="?lang=en">🇬🇧 EN</a>
        </div>
        <h1>{t['title']}</h1>
        
        <div class="card-grid">
            <div class="card">
                <h2>{totals.get('connection', 0)}</h2>
                <p>{t['conn']}</p>
            </div>
            <div class="card">
                <h2>{totals.get('generation', 0)}</h2>
                <p>{t['gen']}</p>
            </div>
        </div>

        <h3>{t['monthly']}</h3>
        <table>
            <thead>
                <tr>
                    <th>{t['month']}</th>
                    <th>{t['type']}</th>
                    <th>{t['count']}</th>
                </tr>
            </thead>
            <tbody>
                {monthly_table}
            </tbody>
        </table>

        <h3>{t['by_lang']}</h3>
        <table>
            <thead>
                <tr>
                    <th>{t['language']}</th>
                    <th>{t['count']}</th>
                </tr>
            </thead>
            <tbody>
                {lang_table}
            </tbody>
        </table>

        <a href="/" class="back-link">{t['back']}</a>
    </div>
</body>
</html>'''
