from flask import Flask, render_template_string, request, redirect, session, url_for
import os

app = Flask(__name__)
app.secret_key = 'espinhovidal_galiarp_2026'

# --- BASE DE DADOS INTEGRADA (DADOS REAIS DE RP) ---
# Se o dados.py falhar no Vercel, o site usa estes valores automaticamente
DB = {
    "users": {
        "igor.rodrigues@comandobombeiros.galiarp.pt": {
            "nome": "Igor Rodrigues",
            "senha": "GRPGALAIMELHORSERVIDOR",
            "patente": "Comandante"
        }
    },
    "stats": {
        "incendios": 124,
        "socorros": 315,
        "operativos": 24
    },
    "viaturas": [
        {"id": "VUCI-01", "tipo": "Combate Urbano", "estado": "Operacional"},
        {"id": "ABSC-01", "tipo": "Socorro (INEM)", "estado": "Operacional"},
        {"id": "VCOT-01", "tipo": "Comando", "estado": "Operacional"},
        {"id": "VFGC-02", "tipo": "Combate Florestal", "estado": "Oficina"}
    ]
}

# --- TEMPLATE MASTER (DESIGN GÁLIA RP) ---
LAYOUT = """
<!DOCTYPE html>
<html lang="pt-pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BV Espinho | Portal Operacional</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background-color: #09090b; color: #d4d4d8; font-family: 'Inter', sans-serif; }
        .glass { background: rgba(18, 18, 18, 0.9); border: 1px solid #27272a; backdrop-filter: blur(10px); }
        .sidebar-link:hover { border-left: 4px solid #dc2626; background: rgba(220, 38, 38, 0.1); }
    </style>
</head>
<body class="flex h-screen overflow-hidden">
    <aside class="w-72 bg-black border-r border-zinc-800 flex flex-col p-6 shadow-2xl">
        <div class="mb-10 flex items-center space-x-3">
            <div class="bg-red-600 p-2 rounded-xl shadow-lg shadow-red-900/40">
                <i class="fas fa-shield-halved text-white text-xl"></i>
            </div>
            <div>
                <h1 class="text-lg font-black uppercase italic tracking-tighter text-white">BV ESPINHO</h1>
                <p class="text-[9px] text-zinc-500 font-bold uppercase tracking-widest">Gália Roleplay</p>
            </div>
        </div>

        <nav class="flex-1 space-y-2">
            <p class="text-[10px] text-zinc-600 font-black uppercase mb-4 tracking-[0.2em]">Menu Principal</p>
            <a href="/" class="sidebar-link block p-3 rounded-lg transition text-xs font-bold uppercase tracking-tighter"><i class="fas fa-house w-6 text-red-600"></i> Mural</a>
            <a href="/ocorrencias" class="sidebar-link block p-3 rounded-lg transition text-xs font-bold uppercase tracking-tighter"><i class="fas fa-flame w-6 text-orange-500"></i> Ocorrências</a>
            <a href="/equipa" class="sidebar-link block p-3 rounded-lg transition text-xs font-bold uppercase tracking-tighter"><i class="fas fa-users-viewfinder w-6 text-blue-500"></i> Quadro Ativo</a>
            <a href="/viaturas" class="sidebar-link block p-3 rounded-lg transition text-xs font-bold uppercase tracking-tighter"><i class="fas fa-truck-fire w-6 text-zinc-400"></i> Parque Auto</a>
            
            <p class="text-[10px] text-zinc-600 font-black uppercase mb-4 mt-8 tracking-[0.2em]">Recrutamento</p>
            <a href="/candidatura" class="block p-3 rounded-xl bg-red-600/10 text-red-500 border border-red-600/20 hover:bg-red-600 hover:text-white transition text-xs font-black uppercase text-center">Alistar Agora</a>
        </nav>

        <div class="mt-auto pt-6 border-t border-zinc-900">
            {% if session.get('user_email') %}
                <div class="glass p-4 rounded-2xl">
                    <p class="text-[9px] text-red-500 font-black uppercase tracking-widest">{{ session['user_patente'] }}</p>
                    <p class="text-xs font-bold text-white truncate">{{ session['user_nome'] }}</p>
                    <div class="flex gap-2 mt-3">
                        <a href="/dashboard" class="bg-zinc-800 p-2 rounded-lg flex-1 text-center hover:bg-white hover:text-black transition text-[9px] font-black uppercase">Painel</a>
                        <a href="/logout" class="bg-red-900/40 p-2 rounded-lg flex-1 text-center hover:bg-red-600 transition text-[9px] font-black uppercase text-white">Sair</a>
                    </div>
                </div>
            {% else %}
                <a href="/login_page" class="block w-full bg-red-700 py-4 rounded-2xl text-center text-[10px] font-black text-white uppercase tracking-widest hover:bg-red-600 transition shadow-lg shadow-red-950/20">Acesso Restrito</a>
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

# --- ROTAS ---

@app.route('/')
def home():
    content = """
    <div class="animate-in fade-in duration-700">
        <h1 class="text-7xl font-black italic uppercase leading-none mb-10 text-white tracking-tighter">Mural de<br><span class="text-red-600">Comando</span></h1>
        <div class="grid md:grid-cols-2 gap-8">
            <div class="glass p-10 rounded-[2.5rem] border-l-8 border-red-600">
                <span class="bg-red-600 text-white text-[9px] px-3 py-1 rounded font-black uppercase tracking-widest">Alerta de Serviço</span>
                <h3 class="text-2xl font-black mt-4 italic text-white uppercase">Turnos de 24 Horas</h3>
                <p class="text-zinc-500 mt-6 leading-relaxed">Todos os operacionais devem registar a entrada em serviço no terminal do quartel de Espinho. O fardamento n.º 3 é obrigatório para patrulha urbana.</p>
            </div>
            <div class="glass p-10 rounded-[2.5rem] border border-zinc-800 flex flex-col justify-center">
                <h4 class="text-zinc-600 font-black uppercase text-[10px] tracking-widest mb-2 italic">Estado da Corporação</h4>
                <p class="text-4xl font-black text-white italic uppercase tracking-tighter">100% OPERACIONAL</p>
                <div class="w-full bg-zinc-900 h-2 rounded-full mt-4"><div class="bg-green-500 h-2 rounded-full w-full shadow-[0_0_10px_#22c55e]"></div></div>
            </div>
        </div>
    </div>
    """
    return render_template_string(LAYOUT, content=content)

@app.route('/ocorrencias')
def ocorrencias():
    content = f"""
    <h1 class="text-6xl font-black uppercase italic mb-12 text-white tracking-tighter">Dados de <span class="text-orange-600">Campo</span></h1>
    <div class="grid md:grid-cols-3 gap-8 text-center">
        <div class="glass p-12 rounded-[3rem] border border-orange-600/20">
            <p class="text-8xl font-black text-orange-500 leading-none mb-4 italic">{DB['stats']['incendios']}</p>
            <p class="text-[10px] font-black text-zinc-500 uppercase tracking-widest">Incêndios Dominados</p>
        </div>
        <div class="glass p-12 rounded-[3rem] border border-red-600/20">
            <p class="text-8xl font-black text-red-600 leading-none mb-4 italic">{DB['stats']['socorros']}</p>
            <p class="text-[10px] font-black text-zinc-500 uppercase tracking-widest">Socorros Efetuados</p>
        </div>
        <div class="glass p-12 rounded-[3rem] border border-zinc-800">
            <p class="text-8xl font-black text-white leading-none mb-4 italic">{DB['stats']['operativos']}</p>
            <p class="text-[10px] font-black text-zinc-500 uppercase tracking-widest">Bombeiros Ativos</p>
        </div>
    </div>
    """
    return render_template_string(LAYOUT, content=content)

@app.route('/equipa')
def equipa():
    rows = "".join([f"<tr class='border-b border-zinc-900 hover:bg-white/[0.02] transition'><td class='p-6 font-black uppercase italic text-white'>{u['nome']}</td><td class='p-6'><span class='bg-red-600/10 text-red-500 border border-red-600/20 px-3 py-1 rounded text-[10px] font-black uppercase tracking-widest'>{u['patente']}</span></td><td class='p-6 text-right text-green-500 font-black text-[10px] uppercase'>Disponível</td></tr>" for u in DB['users'].values()])
    content = f"""
    <h1 class="text-5xl font-black uppercase italic mb-10 text-white tracking-tighter">Quadro <span class="text-red-600">Honra</span></h1>
    <div class="glass rounded-[2rem] overflow-hidden">
        <table class="w-full text-left">
            <thead class="bg-black/80 text-zinc-600 text-[10px] font-black uppercase tracking-widest border-b border-zinc-800">
                <tr><th class="p-6">Nome</th><th class="p-6">Patente</th><th class="p-6 text-right">Estatuto</th></tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
    """
    return render_template_string(LAYOUT, content=content)

@app.route('/viaturas')
def viaturas():
    cards = "".join([f"<div class='glass p-8 rounded-3xl border border-zinc-800'><h4 class='text-2xl font-black text-white uppercase italic tracking-tighter mb-1'>{v['id']}</h4><p class='text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-6'>{v['tipo']}</p><div class='flex items-center gap-2'><div class='w-2 h-2 rounded-full {'bg-green-500' if v['estado']=='Operacional' else 'bg-orange-500'}'></div><span class='text-[10px] font-black uppercase italic'>{'Operacional' if v['estado']=='Operacional' else 'Em Manutenção'}</span></div></div>" for v in DB['viaturas']])
    content = f"<h1 class='text-5xl font-black uppercase italic mb-12 text-white tracking-tighter'>Parque <span class='text-red-600'>Auto</span></h1><div class='grid md:grid-cols-2 lg:grid-cols-4 gap-6'>{cards}</div>"
    return render_template_string(LAYOUT, content=content)

@app.route('/candidatura')
def candidatura():
    content = """
    <h1 class="text-4xl font-black uppercase italic mb-8 text-white tracking-tighter">Recrutamento <span class="text-red-600">Aberto</span></h1>
    <div class="h-[75vh] bg-white rounded-[2.5rem] overflow-hidden border-8 border-zinc-900 shadow-2xl">
        <iframe src="https://forms.gle/XNtCDyekkgjiJaVE9" class="w-full h-full"></iframe>
    </div>
    """
    return render_template_string(LAYOUT, content=content)

@app.route('/login_page')
def login_page():
    content = """
    <div class="flex justify-center items-center h-[70vh]">
        <form action="/login" method="POST" class="glass p-12 rounded-[3rem] w-full max-w-sm shadow-2xl relative overflow-hidden">
            <div class="text-center mb-10 relative z-10">
                <div class="bg-red-600 w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-xl shadow-red-900/30 rotate-3">
                    <i class="fas fa-key text-white text-2xl -rotate-3"></i>
                </div>
                <h2 class="text-xl font-black uppercase tracking-widest text-white italic">Acesso Restrito</h2>
            </div>
            <div class="space-y-4 relative z-10">
                <input type="email" name="email" placeholder="Email @galiarp.pt" class="w-full bg-black/60 p-4 rounded-xl border border-zinc-800 outline-none text-xs text-white focus:border-red-600 transition" required>
                <input type="password" name="senha" placeholder="Senha Interna" class="w-full bg-black/60 p-4 rounded-xl border border-zinc-800 outline-none text-xs text-white focus:border-red-600 transition" required>
                <button class="w-full bg-red-700 py-4 rounded-xl font-black uppercase tracking-widest text-xs text-white hover:bg-red-600 transition shadow-lg shadow-red-950/20 mt-4">Autenticar</button>
            </div>
        </form>
    </div>
    """
    return render_template_string(LAYOUT, content=content)

@app.route('/login', methods=['POST'])
def login():
    email, senha = request.form.get('email'), request.form.get('senha')
    if email in DB['users'] and DB['users'][email]['senha'] == senha:
        session.update({'user_email': email, 'user_nome': DB['users'][email]['nome'], 'user_patente': DB['users'][email]['patente']})
        return redirect(url_for('home'))
    return redirect(url_for('login_page'))

@app.route('/dashboard')
def dashboard():
    if 'user_email' not in session: return redirect(url_for('login_page'))
    content = f"""
    <div class="glass p-12 rounded-[3rem] border-t-8 border-red-700 animate-in slide-in-from-bottom duration-500">
        <h2 class="text-4xl font-black uppercase italic mb-2 text-white tracking-tighter leading-none">Painel de <span class="text-red-600">Comando</span></h2>
        <p class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest mb-10 italic">Bem-vindo de volta, {session['user_nome']}</p>
        <div class="grid md:grid-cols-2 gap-10">
            <div class="bg-black/50 p-8 rounded-2xl border border-zinc-800">
                <p class="text-[10px] font-black uppercase text-red-500 tracking-widest italic mb-6 border-b border-red-900/20 pb-2">Segurança da Conta</p>
                <input type="password" placeholder="Nova Senha Temporária" class="w-full bg-zinc-900 p-4 rounded-xl border border-zinc-800 text-xs text-white mb-4">
                <button class="w-full bg-zinc-800 py-3 rounded-xl text-[10px] font-black uppercase text-white hover:bg-white hover:text-black transition">Atualizar Dados</button>
            </div>
            <div class="bg-black/50 p-8 rounded-2xl border border-zinc-800 flex flex-col justify-center">
                <p class="text-xs text-zinc-400 italic leading-relaxed text-center font-light">Este painel permite a gestão de turnos e visualização de alertas críticos do Gália RP.</p>
            </div>
        </div>
    </div>
    """
    return render_template_string(LAYOUT, content=content)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# ESSENCIAL PARA O VERCEL RECONHECER A VARIAVEL APP
app = app
