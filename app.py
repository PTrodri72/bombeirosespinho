from flask import Flask, render_template_string, request, redirect, session, url_for
import os
import importlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'galia_espinho_super_secret_2026'

# --- BASE DE DADOS INTEGRADA (Para evitar erro de ecrã vazio) ---
class SistemaDados:
    def __init__(self):
        self.users = {
            "igor.rodrigues@comandobombeiros.galiarp.pt": {
                "nome": "Igor Rodrigues", 
                "senha": "GRPGALAIMELHORSERVIDOR", 
                "patente": "Comandante"
            }
        }
        self.stats = {"incendios": 142, "socorros": 315, "operacionais": 24}
        self.viaturas = [
            {"id": "VUCI-01", "tipo": "Combate Urbano", "estado": "Operacional"},
            {"id": "ABSC-01", "tipo": "Socorro", "estado": "Operacional"},
            {"id": "VCOT-01", "tipo": "Comando", "estado": "Operacional"},
            {"id": "VFGC-02", "tipo": "Combate Florestal", "estado": "Oficina"}
        ]

# Tenta carregar do dados.py, se não existir, usa o padrão acima
try:
    import dados
except:
    dados = SistemaDados()

def salvar():
    try:
        caminho = os.path.join(os.path.dirname(__file__), 'dados.py')
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(f"users = {repr(dados.users)}\n")
            f.write(f"stats = {repr(dados.stats)}\n")
            f.write(f"viaturas = {repr(getattr(dados, 'viaturas', []))}\n")
        importlib.reload(dados)
    except: pass

# --- INTERFACE VISUAL (CSS & ESTRUTURA) ---
LAYOUT = """
<!DOCTYPE html>
<html lang="pt-pt">
<head>
    <meta charset="UTF-8">
    <title>BV Espinho | Gália RP</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background-color: #050505; color: #e4e4e7; font-family: sans-serif; }
        .glass { background: rgba(20, 20, 20, 0.8); backdrop-filter: blur(10px); border: 1px solid #27272a; }
        .red-glow { box-shadow: 0 0 15px rgba(220, 38, 38, 0.2); }
    </style>
</head>
<body class="flex h-screen overflow-hidden">
    <aside class="w-72 bg-zinc-950 border-r border-zinc-900 flex flex-col p-6">
        <div class="mb-10 flex items-center space-x-3">
            <div class="bg-red-600 p-2 rounded-lg shadow-lg shadow-red-900/40">
                <i class="fas fa-fire-extinguisher text-white"></i>
            </div>
            <div>
                <h1 class="text-lg font-black uppercase italic tracking-tighter leading-none">BV ESPINHO</h1>
                <p class="text-[9px] text-zinc-500 font-bold uppercase tracking-widest">Proteção e Socorro</p>
            </div>
        </div>

        <nav class="flex-1 space-y-1">
            <p class="text-[10px] text-zinc-600 font-black uppercase mb-4 tracking-widest">Principal</p>
            <a href="{{ url_for('home') }}" class="flex items-center p-3 rounded-xl hover:bg-zinc-900 transition text-xs font-bold uppercase tracking-tighter"><i class="fas fa-home w-8 text-red-600"></i> Mural Operacional</a>
            <a href="{{ url_for('fogos') }}" class="flex items-center p-3 rounded-xl hover:bg-zinc-900 transition text-xs font-bold uppercase tracking-tighter"><i class="fas fa-fire w-8 text-orange-500"></i> Ocorrências</a>
            <a href="{{ url_for('equipa') }}" class="flex items-center p-3 rounded-xl hover:bg-zinc-900 transition text-xs font-bold uppercase tracking-tighter"><i class="fas fa-users w-8 text-blue-500"></i> Quadro Humano</a>
            
            <p class="text-[10px] text-zinc-600 font-black uppercase mb-4 mt-8 tracking-widest">Recrutamento</p>
            <a href="{{ url_for('candidatura') }}" class="flex items-center p-3 rounded-xl bg-red-600/10 text-red-500 border border-red-600/20 hover:bg-red-600 hover:text-white transition text-xs font-bold uppercase tracking-tighter"><i class="fas fa-file-signature w-8"></i> Alistar Agora</a>
        </nav>

        <div class="mt-auto pt-6 border-t border-zinc-900">
            {% if session.get('user_email') %}
                <div class="glass p-4 rounded-2xl red-glow">
                    <p class="text-[9px] text-red-500 font-black uppercase mb-1">{{ session['user_patente'] }}</p>
                    <p class="text-xs font-bold truncate text-white mb-3">{{ session['user_nome'] }}</p>
                    <div class="flex gap-2">
                        <a href="{{ url_for('dashboard') }}" class="bg-zinc-800 p-2 rounded-lg flex-1 text-center hover:bg-white hover:text-black transition text-[10px] font-black uppercase">Painel</a>
                        <a href="{{ url_for('logout') }}" class="bg-red-900/30 p-2 rounded-lg flex-1 text-center hover:bg-red-600 transition text-[10px] font-black uppercase text-white">Sair</a>
                    </div>
                </div>
            {% else %}
                <a href="{{ url_for('login_page') }}" class="block w-full bg-red-700 py-4 rounded-2xl text-center text-[10px] font-black text-white uppercase tracking-widest hover:bg-red-600 transition">Acesso Restrito</a>
            {% endif %}
        </div>
    </aside>

    <main class="flex-1 overflow-y-auto p-12 relative">
        <div class="max-w-6xl mx-auto">
            {% block content %}{% endblock %}
        </div>
    </main>
</body>
</html>
"""

@app.route('/')
def home():
    content = """
    <div class="animate-fadeIn">
        <h1 class="text-7xl font-black italic uppercase leading-none mb-10 text-white tracking-tighter">Últimos <br><span class="text-red-600">Comunicados</span></h1>
        <div class="grid lg:grid-cols-2 gap-8">
            <div class="glass p-10 rounded-[2.5rem] border-l-8 border-red-600">
                <span class="bg-red-600 text-white text-[9px] px-3 py-1 rounded font-black uppercase tracking-widest">Importante</span>
                <h3 class="text-2xl font-black mt-4 italic text-white leading-none">Novo Sistema Operacional v2.0</h3>
                <p class="text-zinc-500 mt-6 leading-relaxed">Bem-vindos ao novo portal da corporação. A partir de agora, as senhas e ocorrências são salvas no sistema central do Gália RP.</p>
            </div>
            <div class="glass p-10 rounded-[2.5rem] border border-zinc-800">
                <i class="fas fa-triangle-exclamation text-orange-500 text-3xl mb-4"></i>
                <h3 class="text-xl font-bold italic text-white uppercase">Alerta de Incêndio</h3>
                <p class="text-zinc-500 mt-2 text-sm italic">Risco moderado no setor Norte de Espinho. Unidades de prontidão reforçada.</p>
            </div>
        </div>
    </div>
    """
    return render_template_string(LAYOUT, content=content)

@app.route('/fogos')
def fogos():
    content = f"""
    <div class="text-center py-10">
        <h1 class="text-6xl font-black uppercase italic mb-16 tracking-tighter text-white">Estatísticas de <span class="text-orange-600 italic">Campo</span></h1>
        <div class="grid md:grid-cols-3 gap-10">
            <div class="glass p-12 rounded-[3rem] border border-orange-600/20">
                <p class="text-8xl font-black text-orange-500 leading-none">{dados.stats['incendios']}</p>
                <p class="text-[10px] font-black text-zinc-500 uppercase mt-4 tracking-widest">Incêndios Extintos</p>
            </div>
            <div class="glass p-12 rounded-[3rem] border border-red-600/20">
                <p class="text-8xl font-black text-red-600 leading-none">{dados.stats['socorros']}</p>
                <p class="text-[10px] font-black text-zinc-500 uppercase mt-4 tracking-widest">Socorros Médicos</p>
            </div>
            <div class="glass p-12 rounded-[3rem] border border-zinc-800">
                <p class="text-8xl font-black text-white leading-none">{dados.stats['operacionais']}</p>
                <p class="text-[10px] font-black text-zinc-500 uppercase mt-4 tracking-widest">Operativos no Ativo</p>
            </div>
        </div>
    </div>
    """
    return render_template_string(LAYOUT, content=content)

@app.route('/equipa')
def equipa():
    rows = ""
    for email, info in dados.users.items():
        rows += f"""
        <tr class="border-b border-zinc-900 hover:bg-white/[0.02] transition">
            <td class="p-6 font-black uppercase italic text-white">{info['nome']}</td>
            <td class="p-6"><span class="bg-red-600/10 text-red-500 border border-red-600/20 px-3 py-1 rounded text-[10px] font-black uppercase tracking-widest">{info['patente']}</span></td>
            <td class="p-6 text-right"><span class="text-green-500 text-[10px] font-black uppercase flex items-center justify-end gap-2"><div class="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"></div> Disponível</span></td>
        </tr>"""
    content = f"""
    <h1 class="text-5xl font-black uppercase italic mb-10 text-white tracking-tighter">Corpo <span class="text-red-600">Ativo</span></h1>
    <div class="glass rounded-[2rem] overflow-hidden shadow-2xl">
        <table class="w-full text-left">
            <thead class="bg-black/50 text-zinc-500 text-[10px] font-black uppercase tracking-widest border-b border-zinc-800">
                <tr><th class="p-6">Nome Operacional</th><th class="p-6">Patente</th><th class="p-6 text-right">Estado</th></tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
    </div>"""
    return render_template_string(LAYOUT, content=content)

@app.route('/candidatura')
def candidatura():
    content = """
    <div class="h-[80vh] flex flex-col">
        <h1 class="text-4xl font-black uppercase italic mb-8 text-white tracking-tighter">Recrutamento <span class="text-red-600">Aberto</span></h1>
        <div class="flex-1 bg-white rounded-[2rem] overflow-hidden border-8 border-zinc-900 shadow-2xl">
            <iframe src="https://forms.gle/XNtCDyekkgjiJaVE9" class="w-full h-full"></iframe>
        </div>
    </div>"""
    return render_template_string(LAYOUT, content=content)

@app.route('/login_page')
def login_page():
    content = """
    <div class="flex justify-center items-center h-[70vh]">
        <form action="/login" method="POST" class="glass p-12 rounded-[2.5rem] w-full max-w-sm shadow-2xl">
            <div class="text-center mb-10">
                <div class="bg-red-600 w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-xl shadow-red-900/30">
                    <i class="fas fa-shield-halved text-white text-2xl"></i>
                </div>
                <h2 class="text-xl font-black uppercase tracking-widest text-white italic">Login Comando</h2>
            </div>
            <div class="space-y-4">
                <input type="email" name="email" placeholder="Email @galiarp.pt" class="w-full bg-black/50 p-4 rounded-xl border border-zinc-800 outline-none text-xs text-white focus:border-red-600 transition" required>
                <input type="password" name="senha" placeholder="Palavra-passe" class="w-full bg-black/50 p-4 rounded-xl border border-zinc-800 outline-none text-xs text-white focus:border-red-600 transition" required>
                <button class="w-full bg-red-700 py-4 rounded-xl font-black uppercase tracking-widest text-xs text-white hover:bg-red-600 transition shadow-lg shadow-red-950">Autenticar</button>
            </div>
        </form>
    </div>"""
    return render_template_string(LAYOUT, content=content)

@app.route('/login', methods=['POST'])
def login():
    email, senha = request.form.get('email'), request.form.get('senha')
    if email in dados.users and dados.users[email]['senha'] == senha:
        session.update({'user_email': email, 'user_nome': dados.users[email]['nome'], 'user_patente': dados.users[email]['patente']})
        return redirect(url_for('dashboard'))
    return redirect(url_for('login_page'))

@app.route('/dashboard')
def dashboard():
    if 'user_email' not in session: return redirect(url_for('login_page'))
    content = f"""
    <div class="glass p-12 rounded-[3rem] border-t-8 border-red-700">
        <h2 class="text-3xl font-black uppercase italic mb-10 text-white tracking-tighter">Painel Interno</h2>
        <div class="grid md:grid-cols-2 gap-10">
            <form action="/update_pass" method="POST" class="bg-black/40 p-8 rounded-2xl border border-zinc-800 space-y-4">
                <p class="text-[10px] font-black uppercase text-red-500 tracking-widest italic">Alterar Senha de Acesso</p>
                <input type="password" name="nova_senha" placeholder="Nova Senha" class="w-full bg-black p-4 rounded-xl border border-zinc-800 text-xs text-white">
                <button class="w-full bg-red-700 py-3 rounded-xl text-[10px] font-black uppercase text-white shadow-lg">Atualizar Ficheiro dados.py</button>
            </form>
            <div class="bg-black/40 p-8 rounded-2xl border border-zinc-800">
                <p class="text-[10px] font-black uppercase text-zinc-500 tracking-widest italic">Info Sistema</p>
                <p class="text-xs text-zinc-400 mt-4 leading-relaxed font-light italic">Toda e qualquer alteração é registada no ficheiro de persistência de dados do servidor para evitar perdas em caso de reinicialização do script.</p>
            </div>
        </div>
    </div>"""
    return render_template_string(LAYOUT, content=content)

@app.route('/update_pass', methods=['POST'])
def update_pass():
    if 'user_email' in session:
        dados.users[session['user_email']]['senha'] = request.form.get('nova_senha')
        salvar()
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# ESSENCIAL PARA O VERCEL
app = app
