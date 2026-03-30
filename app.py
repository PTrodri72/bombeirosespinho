from flask import Flask, render_template_string, request, redirect, session, url_for
from functools import wraps
import dados

app = Flask(__name__)
app.secret_key = 'espinhovidal_galiarp_2026'

LAYOUT = """
<!DOCTYPE html>
<html lang="pt-pt">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BV Espinho | MDT</title>
<script src="https://cdn.tailwindcss.com"></script>
<style>
body { background-color: #09090b; color: #d4d4d8; font-family: 'Inter', sans-serif; }
.glass { background: rgba(18,18,18,0.9); border: 1px solid #27272a; backdrop-filter: blur(10px); }
.sidebar-link:hover { border-left: 4px solid #dc2626; background: rgba(220,38,38,0.1); }
</style>
</head>
<body class="flex h-screen overflow-hidden">
<aside class="w-72 bg-black border-r border-zinc-800 flex flex-col p-6 shadow-2xl">
<div class="mb-10 flex items-center space-x-3">
<h1 class="text-lg font-black uppercase italic tracking-tighter text-white">BV ESPINHO</h1>
</div>
<nav class="flex-1 space-y-2">
<a href="/" class="sidebar-link block p-3 rounded-lg text-xs font-bold uppercase tracking-tighter">Comunicados</a>
<a href="/ocorrencias" class="sidebar-link block p-3 rounded-lg text-xs font-bold uppercase tracking-tighter">Fogos</a>
<a href="/dashboard" class="sidebar-link block p-3 rounded-lg text-xs font-bold uppercase tracking-tighter">Bombeiros</a>
<a href="/equipa" class="sidebar-link block p-3 rounded-lg text-xs font-bold uppercase tracking-tighter">Equipa</a>
</nav>
<div class="mt-auto pt-6 border-t border-zinc-900">
{% if session.get('user_email') %}
<div class="glass p-4 rounded-2xl">
<p class="text-[9px] text-red-500 font-black uppercase tracking-widest">{{ session['user_role'] }}</p>
<p class="text-xs font-bold text-white truncate">{{ session['user_nome'] }}</p>
<div class="flex gap-2 mt-3">
<a href="/dashboard" class="bg-zinc-800 p-2 rounded-lg flex-1 text-center hover:bg-white hover:text-black text-[9px] font-black uppercase">Painel</a>
<a href="/logout" class="bg-red-900/40 p-2 rounded-lg flex-1 text-center hover:bg-red-600 text-[9px] font-black uppercase text-white">Sair</a>
</div>
</div>
{% else %}
<a href="/login_page" class="block w-full bg-red-700 py-4 rounded-2xl text-center text-[10px] font-black text-white uppercase tracking-widest hover:bg-red-600">Acesso Restrito</a>
{% endif %}
</div>
</aside>
<main class="flex-1 overflow-y-auto p-12 bg-[#0c0c0e]">
<div class="max-w-5xl mx-auto">
{% block content %}{% endblock %}
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

def role_required(role):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if session.get('user_role') != role:
                return 'Acesso negado'
            return f(*args, **kwargs)
        return decorated
    return wrapper

@app.route('/')
def home():
    content = "<h1 class='text-4xl font-black text-white mb-6'>Comunicados do Comando</h1>"
    return render_template_string(LAYOUT, content=content)

@app.route('/login_page')
def login_page():
    content = """
<h2 class='text-2xl font-black text-white mb-4'>Login</h2>
<form method='POST' action='/login'>
<input name='email' type='email' placeholder='Email' required class='p-2 mb-2 w-full rounded bg-black/50 text-white'>
<input name='senha' type='password' placeholder='Senha' required class='p-2 mb-2 w-full rounded bg-black/50 text-white'>
<button class='w-full bg-red-700 py-2 rounded text-white'>Entrar</button>
</form>
<h2 class='text-2xl font-black text-white mt-6 mb-4'>Registar</h2>
<form method='POST' action='/register'>
<input name='nome' placeholder='Nome' required class='p-2 mb-2 w-full rounded bg-black/50 text-white'>
<input name='email' type='email' placeholder='Email' required class='p-2 mb-2 w-full rounded bg-black/50 text-white'>
<input name='senha' type='password' placeholder='Senha' required class='p-2 mb-2 w-full rounded bg-black/50 text-white'>
<button class='w-full bg-red-700 py-2 rounded text-white'>Registar</button>
</form>
"""
    return render_template_string(LAYOUT, content=content)

@app.route('/register', methods=['POST'])
def register():
    nome = request.form.get('nome','').strip()
    email = request.form.get('email','').strip().lower()
    senha = request.form.get('senha','')
    if email in dados.DB['users']:
        return redirect(url_for('login_page'))
    dados.DB['users'][email] = {'nome': nome, 'senha': dados.hash_password(senha), 'role': 'Recruta'}
    return redirect(url_for('login_page'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email','').strip().lower()
    senha = request.form.get('senha','')
    user = dados.DB['users'].get(email)
    if not user or not dados.check_password(user['senha'], senha):
        return redirect(url_for('login_page'))
    session.clear()
    session['user_email'] = email
    session['user_nome'] = user['nome']
    session['user_role'] = user['role']
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    content = f"<h1 class='text-3xl font-black text-white mb-4'>Painel MDT</h1><p class='text-white mb-2'>Bem-vindo {session['user_nome']} ({session['user_role']})</p>"
    if session['user_role'] == 'Comandante':
        content += "<p class='text-red-500'>Pode criar novas ocorrências e gerir utilizadores.</p>"
    return render_template_string(LAYOUT, content=content)

@app.route('/criar_ocorrencia', methods=['POST'])
@login_required
@role_required('Comandante')
def criar_ocorrencia():
    descricao = request.form.get('descricao','').strip()
    if descricao:
        dados.DB['ocorrencias'].append({'descricao': descricao, 'autor': session['user_nome']})
    return redirect(url_for('ver_ocorrencias'))

@app.route('/ocorrencias')
@login_required
def ver_ocorrencias():
    html = "<h1 class='text-2xl font-black text-white mb-4'>Ocorrências</h1>"
    for o in dados.DB['ocorrencias']:
        html += f"<p class='text-white'>{o['descricao']} - {o['autor']}</p>"
    if session['user_role'] == 'Comandante':
        html += '''<form method='POST' action='/criar_ocorrencia'><input name='descricao' placeholder='Nova ocorrência' required class='p-2 mb-2 w-full rounded bg-black/50 text-white'><button class='w-full bg-red-700 py-2 rounded text-white'>Criar</button></form>'''
    return render_template_string(LAYOUT, content=html)

@app.route('/equipa')
@login_required
def equipa():
    rows = "".join([f"<tr><td class='p-2 text-white'>{u['nome']}</td><td class='p-2 text-red-500'>{u['role']}</td></tr>" for u in dados.DB['users'].values()])
    html = f"<h1 class='text-2xl font-black text-white mb-4'>Equipa</h1><table>{rows}</table>"
    return render_template_string(LAYOUT, content=html)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

app = app
