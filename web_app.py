from flask import Flask, request, session, redirect, url_for
import subprocess, os, random

app = Flask(__name__)
app.secret_key = 'apex_final_secret_2026'
PASSWORD = 'tabarka000@amdouni&'

def ai_generate(target_info):
    words = target_info.split()
    variations = []
    for w in words:
        variations.append(w)
        variations.append(w.capitalize() + "123")
        variations.append(w + "@" + str(random.randint(1990, 2026)))
    return variations[:10]

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        return "Wrong Password"
    return '<body style="background:#0d1117;color:white;text-align:center;padding-top:50px;"><h2 style="color:#00ffcc;">Login</h2><form method="POST"><input type="password" name="password"><br><br><button type="submit">Enter</button></form></body>'

@app.route('/')
def index():
    if not session.get('logged_in'): return redirect(url_for('login'))
    return '''
    <body style="background:#0d1117;color:white;font-family:Arial;padding:20px;">
        <h1 style="color:#00ffcc;text-align:center;">🛡️ APEX CORE (Cloud)</h1>
        <div style="background:#161b22;padding:15px;border-radius:8px;">
            <h3>🧠 AI Core:</h3>
            <form method="POST" action="/ai"><input type="text" name="info" placeholder="Name City Year"><button type="submit">Generate</button></form>
        </div>
        <div style="background:#161b22;padding:15px;border-radius:8px;margin-top:10px;">
            <h3>🛠️ Smart Scan:</h3>
            <a href="/smart_scan" style="color:#00ffcc;">CVE + Ports</a>
        </div>
        <br><a href="/logout" style="color:red;">Logout</a>
    </body>
    '''

@app.route('/ai', methods=['POST'])
def ai_route():
    if not session.get('logged_in'): return redirect(url_for('login'))
    info = request.form['info']
    words = ai_generate(info)
    output = "<br>".join(words)
    return f'<body style="background:#0d1117;color:#00ffcc;padding:20px;font-family:monospace;"><h3>AI Generated:</h3><pre>{output}</pre><a href="/" style="color:white;">Back</a></body>'

@app.route('/smart_scan', methods=['GET', 'POST'])
def smart_scan():
    if not session.get('logged_in'): return redirect(url_for('login'))
    if request.method == 'POST':
        keyword = request.form['keyword']
        cve = subprocess.run(f'python ~/cybersec-toolkit/cve_web.py {keyword}', shell=True, capture_output=True, text=True).stdout
        ports = subprocess.run('python ~/cybersec-toolkit/scan_web.py 127.0.0.1', shell=True, capture_output=True, text=True).stdout
        return f'<body style="background:#0d1117;color:#00ffcc;padding:20px;font-family:monospace;"><pre>=== CVEs ===\n{cve}\n\n=== Ports ===\n{ports}</pre><a href="/">Back</a></body>'
    return '<body style="background:#0d1117;color:white;text-align:center;padding-top:50px;"><h2>Smart Scan</h2><form method="POST"><input type="text" name="keyword" placeholder="Software"><br><br><button type="submit">Analyze</button></form><br><a href="/">Back</a></body>'

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
