### app.py

from flask import Flask, render_template_string, request, redirect, session, url_for
from functools import wraps
import os
from dados import DB, hash_password, check_password, gerar_dashboard_html

app = Flask(**name**)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key")

LAYOUT = """

<!DOCTYPE html>

<html lang='pt-pt'>
<head>
<meta charset='UTF-8'>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<title>BV Espinho RP</title>
<script src='https://cdn.tailwindcss.com'></script>
<script>
window.addEventListener('keydown', function(e) {
    if (e.key === 'F12' || (e.ctrlKey && e.shiftKey && e.key === 'I')) {
        e.preventDefault();
        alert('Inspeção desativada');
    }
});
</script>
<style>
body { background-color: #09090b; color: #d4d4d8; font-family: 'Inter', sans-serif; }
.glass { background: rgba(18,18,18,0.85); border: 1px solid #27272a; backdrop-filter: blur(10px); }
.sidebar-link:hover { border-left: 4px solid #dc2626; background: rgba(220,38,38,0.1); }
</style>
</head>
<body class='flex h-screen overflow-hidden'>
<aside class='w-72 bg-black border-r border-zinc-800 flex flex-col p-6 shadow-2xl'>
<div class='mb-10 flex items-center space-x-3'>
<div class='bg-red-600 p-2 rounded-xl shadow-lg shadow-red-900/40'>
<i class='fas fa-shield-halved text-white text-xl'></i>
</div>
<div>
<h1 class='text-lg font-black uppercase italic tracking-tighter text-white'>BV ESPINHO</h1>
<p class='text-[9px] text-zinc-500 font-bold uppercase tracking-widest'>Gália Roleplay</p>
</div>
</div>
<nav class='flex-1 space-y-2'>
<p class='text-[10px] text-zinc-600 font-black uppercase mb-4 tracking-[0.2em]'>Menu Principal</p>
<a href='/' class='sidebar-link block p-3 rounded-lg transition text-xs font-bold uppercase tracking-tighter'>Comunicados</a>
<a href='/ocorrencias' class='sidebar-link block p-3 rounded-lg transition text-xs font-bold uppercase tracking-tighter'>Fogos</a>
<a href='/equipa' class='sidebar-link block p-3 rounded-lg transition text-xs font-bold uppercase tracking-tighter'>Bombeiros</a>
<a href='/dashboard' class='sidebar-link block p-3 rounded-lg transition text-xs font-bold uppercase tracking-tighter'>Equipa</a>
</nav>
<div class='mt-auto pt-6 border-t border-zinc-900'>
{% if session.get('user_email') %}
<div class='glass p-4 rounded-2xl'>
<p class='text-[9px] text-red-500 font-black uppercase tracking-widest'>{{ session['user_role'] }}</p>
<p class='text-xs font-bold text-white truncate'>{{ session['user_nome'] }}</p>
<div class='flex gap-2 mt-3'>
<a href='/dashboard' class='bg-zinc-800 p-2 rounded-lg flex-1 text-center hover:bg-white hover:text-black transition text-[9px] font-black uppercase'>Painel</a>
<a href='/logout' class='bg-red-900/40 p-2 rounded-lg flex-1 text-center hover:bg-red-600 transition text-[9px] font-black uppercase text-white'>Sair</a>
</div>
</div>
{% else %}
<a href='/login_page' class='block w-full bg-red-700 py-4 rounded-2xl text-center text-[10px] font-black text-white uppercase tracking-widest hover:bg-red-600 transition shadow-lg shadow-red-950/20'>Login</a>
{% endif %}
</div>
</aside>
<main class='flex-1 overflow-y-auto p-12 bg-[#0c0c0e]'>
<div class='max-w-5xl mx-auto'>
{{ content|safe }}
</div>
</main>
</body>
</html>
"""

def login_required(f):
@wraps(f)
def decorated(*args, **kwargs):
if 'user_email' not in session:
return redirect(url_for('login_page'))
return f(*args, **kwargs)
return decorated

@app.route('/')
def home():
return redirect('[https://bombeiros.galia.pt/](https://bombeiros.galia.pt/)')

@app.route('/login_page')
def login_page():
content = """ <form method='POST' action='/login' class='glass p-8 rounded-xl max-w-md mx-auto'> <input name='email' type='email' placeholder='Email' class='w-full p-2 mb-4 rounded' required> <input name='senha' type='password' placeholder='Senha' class='w-full p-2 mb-4 rounded' required> <button type='submit' class='w-full p-2 bg-red-600 text-white rounded'>Login</button> </form>
"""
return render_template_string(LAYOUT, content=content)

@app.route('/login', methods=['POST'])
def login():
email = request.form.get('email', '').strip().lower()
senha = request.form.get('senha', '')

```
if email not in DB['users'] or not check_password(DB['users'][email]['senha'], senha):
    return redirect(url_for('login_page'))

user = DB['users'][email]
session.clear()
session['user_email'] = email
session['user_nome'] = user['nome']
session['user_role'] = user['role']

return redirect(url_for('dashboard'))
```

@app.route('/dashboard')
@login_required
def dashboard():
content = gerar_dashboard_html()
return render_template_string(LAYOUT, content=content)

@app.route('/ocorrencias')
@login_required
def ocorrencias():
content = "<h1 class='text-3xl text-red-600 mb-4'>Ocorrências Ativas</h1>"
for o in DB['ocorrencias']:
content += f"<p class='text-white'>{o['descricao']} - {o['autor']}</p>"
return render_template_string(LAYOUT, content=content)

@app.route('/equipa')
@login_required
def equipa():
content = "<h1 class='text-3xl text-red-600 mb-4'>Quadro de Bombeiros</h1>"
for u_email, u in DB['users'].items():
content += f"<p class='text-white'>{u['nome']} - {u['role']}</p>"
return render_template_string(LAYOUT, content=content)

@app.route('/logout')
def logout():
session.clear()
return redirect(url_for('home'))

if **name** == '**main**':
app.run(debug=True)
