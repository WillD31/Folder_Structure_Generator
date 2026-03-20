import json
import falcon
import os

class AliveResource(object):
    
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200 
        resp.content_type = 'text/html'
        resp.text = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>API Status</title>
    <style>
        body {{ font-family: sans-serif; text-align: center; padding: 50px; background-color: #f7f9fc; }}
        .status-box {{ background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); display: inline-block; }}
        h1 {{ color: #4CAF50; }}
        a {{ text-decoration: none; color: #667eea; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="status-box">
        <h1>API is Online and Alive!</h1>
        <p>Working directory: {os.getcwd()}</p>
        <br>
        <a href="/">&larr; Return to Homepage</a>
    </div>
</body>
</html>'''
