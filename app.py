from flask import Flask, render_template_string, request, redirect, session, url_for, flash
import os
import importlib
from datetime import datetime

# --- CONFIGURAÇÃO DE PERSISTÊNCIA ---
try:
    import dados
except ImportError:
    # Caso o dados.py não exista, cria a estrutura inicial
    class Mock:
        users = {
            "igor.rodrigues@comandobombeiros.galiarp.pt": {
                "nome": "Igor Rodrigues", 
                "senha": "GRPGALAIMELHORSERVIDOR", 
                "patente": "Comandante",
                "data_adesao": "01/01/2026"
            }
        }
        stats = {"incendios": 124, "socorros": 450, "limpeza_via": 89}
        viaturas = [
            {"id": "VUCI-01", "tipo": "Combate", "estado": "Operacional"},
            {"id": "ABSC-05", "tipo": "Ambulância", "estado": "Operacional"},
            {"id": "VCOT-01", "tipo": "Comando", "estado": "Oficina"}
        ]
    dados = Mock()

app = Flask(__name__)
app.secret_key = 'galia_premium_secret_key_2026'

def salvar_dados():
    """Função de Escrita no Ficheiro dados.py"""
    try:
        caminho = os.path.join(os.path.dirname(__file__), 'dados.py')
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write("# BASE DE DADOS AUTOMÁTICA BV ESPINHO\n")
            f.write(f"users = {repr(dados.users)}\n")
            f.write(f"stats = {repr(dados.stats)}\n")
            f.write(f"viaturas = {repr(getattr(dados, 'viaturas', []))}\n")
        importlib.reload(dados)
        return True
    except:
        return False

# --- ESTRUTURA VISUAL MASTER (UI/UX) ---
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="pt-pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BV Espinho | Gestão Operacional</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');
        body { font-family: 'Inter', sans-serif; }
        .bg-fire { background: linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%); }
        .glass { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.05); }
        .red-gradient { background: linear-gradient(90deg, #dc2626 0%, #991b1b 100%); }
        .sidebar-item:hover { background: rgba(220, 38, 38, 0.1); border-left: 4px solid #dc2626; }
        .active-link { background: rgba(220, 38, 38, 0.15); border-left: 4px solid #dc2626; color: white; }
    </style>
    <script>
        // SEGURANÇA MÁXIMA
        document.addEventListener('contextmenu', e => e.preventDefault());
        document.onkeydown = function(e) {
            if(event.keyCode == 123 || (e.ctrlKey && e.shiftKey && (e.keyCode == 73 || e.keyCode == 74 || e.keyCode == 67)) || (e.ctrlKey && e.keyCode == 85)) return false;
        }
    </script>
</head>
<body class="bg-fire text-zinc-300 min-h-screen flex overflow-hidden">

    <aside class="w-80 bg-black/40 border-r border-zinc-800 flex flex-col z-50">
        <div class="p-8">
            <div class="flex items-center space-x-4 mb-8">
                <div class="p-3 red-gradient rounded-2xl shadow-lg shadow-red-900/40">
                    <i class="fas fa-biohazard text-2xl text-white"></i>
                </div>
                <div>
                    <h2 class="text-xl font-black text-white tracking-tighter italic leading-none uppercase">BV Espinho</h2>
                    <p class="text-[9px] text-zinc-500 font-bold uppercase tracking-widest mt-1">Proteção e Socorro</p>
                </div>
            </div>

            <nav class="space-y-2 uppercase font-black text-[10px] tracking-[0.15em]">
                <p class="text-zinc-600 mb-4 ml-2">Principal</p>
                <a href="{{ url_for('home') }}" class="sidebar-item flex items-center p-4 rounded-xl transition group">
                    <i class="fas fa-th-large w-8 text-red-600 group-hover:scale-125 transition"></i> Mural Operacional
                </a>
                <a href="{{ url_for('fogos') }}" class="sidebar-item flex items-center p-4 rounded-xl transition group">
                    <i class="fas fa-fire-extinguisher w-8 text-orange-500"></i> Ocorrências
                </a>
                <a href="{{ url_for('equipa') }}" class="sidebar-item flex items-center p-4 rounded-xl transition group">
                    <i class="fas fa-address-book w-8 text-blue-500"></i> Quadro Humano
                </a>
                <a href="{{ url_for('viaturas') }}" class="sidebar-item flex items-center p-4 rounded-xl transition group">
                    <i class="fas fa-truck-pickup w-8 text-zinc-500"></i> Parque Auto
                </a>
                
                <p class="text-zinc-600 mb-4 mt-8 ml-2">Recrutamento</p>
                <a href="{{ url_for('candidatura') }}" class="sidebar-item flex items-center p-4 rounded-xl transition bg-red-600/5 text-red-500 border border-red-900/20">
                    <i class="fas fa-file-contract w-8"></i> Alistar Agora
                </a>
            </nav>
        </div>

        <div class="mt-auto p-6 border-t border-zinc-800/50 bg-black/20">
            {% if session.get('user_email') %}
                <div class="glass p-4 rounded-2xl">
                    <div class="flex items-center space-x-3 mb-4">
                        <div class="w-10 h-10 rounded-full bg-red-600 flex items-center justify-center font-bold text-white shadow-inner">
                            {{ session['user_nome'][0] }}
                        </div>
                        <div class="overflow-hidden">
                            <p class="text-[10px] text-red-500 font-bold uppercase">{{ session['user_patente'] }}</p>
                            <p class="text-xs font-black text-white truncate">{{ session['user_nome'] }}</p>
                        </div>
                    </div>
                    <div class="grid grid-cols-2 gap-2">
                        <a href="{{ url_for('dashboard') }}" class="bg-zinc-800 p-2 rounded-lg text-center hover:bg-white hover:text-black transition text-[10px] font-bold uppercase">Painel</a>
                        <a href="{{ url_for('logout') }}" class="bg-red-950/50 p-2 rounded-lg text-center hover:bg-red-600 text-white transition text-[10px] font-bold uppercase">Sair</a>
                    </div>
                </div>
            {% else %}
                <a href="{{ url_for('login_page') }}" class="block w-full red-gradient py-4 rounded-2xl text-center text-xs font-black text-white uppercase tracking-widest shadow-lg shadow-red-900/20">Acesso Restrito</a>
            {% endif %}
        </div>
    </aside>

    <main class="flex-1 overflow-y-auto relative">
        <div class="absolute top-0 right-0 p-12 opacity-5 pointer-events-none">
            <i class="fas fa-shield-halved text-[400px]"></i>
        </div>
        <div class="p-12 max-w-7xl mx-auto">
            {% block content %}{% endblock %}
        </div>
    </main>

</body>
</html>
"""

# --- ROTAS PÚBLICAS ---

@app.route('/')
def home():
    content = """
    <div class="animate-in fade-in duration-700">
        <header class="mb-12">
            <h1 class="text-8xl font-black text-white uppercase italic leading-none tracking-tighter">Corpo de<br><span class="text-red-600">Bombeiros</span></h1>
            <p class="text-zinc-500 font-bold uppercase tracking-[0.5em] mt-4 ml-2 italic">Associação Humanitária de Espinho</p>
        </header>

        <div class="grid lg:grid-cols-3 gap-8">
            <div class="lg:col-span-2 glass p-10 rounded-[2.5rem] relative overflow-hidden group">
                <div class="absolute top-0 right-0 p-8 text-red-600/10 text-8xl group-hover:rotate-12 transition duration-700">
                    <i class="fas fa-newspaper"></i>
                </div>
                <span class="bg-red-600 text-white text-[10px] px-3 py-1 rounded-full font-black uppercase tracking-widest">Comunicado Interno</span>
                <h3 class="text-3xl font-black text-white mt-6 italic">Atualização do Protocolo de Atuação</h3>
                <p class="text-zinc-400 mt-6 leading-relaxed font-light text-lg">
                    A partir de hoje, todas as viaturas de socorro (ABSC) devem reportar a saída e chegada ao quartel via terminal digital. 
                    O Comandante Igor Rodrigues reforça a importância da pontualidade nos turnos de 24h.
                </p>
                <div class="mt-10 flex space-x-4">
                    <div class="bg-zinc-800/50 p-4 rounded-2xl border border-zinc-700/50">
                        <p class="text-[10px] font-bold text-zinc-500 uppercase">Data</p>
                        <p class="text-sm font-bold text-white">30 Mar 2026</p>
                    </div>
                    <div class="bg-zinc-800/50 p-4 rounded-2xl border border-zinc-700/50">
                        <p class="text-[10px] font-bold text-zinc-500 uppercase">Autor</p>
                        <p class="text-sm font-bold text-white">Comando</p>
                    </div>
                </div>
            </div>

            <div class="space-y-8">
                <div class="bg-red-600 p-8 rounded-[2rem] shadow-2xl shadow-red-900/30">
                    <h4 class="text-white font-black uppercase text-xs tracking-widest mb-4">Estado do Concelho</h4>
                    <p class="text-4xl font-black text-white italic uppercase">Risco Elevado</p>
                    <div class="w-full bg-black/20 h-2 rounded-full mt-6">
                        <div class="bg-white h-2 rounded-full w-[85%]"></div>
                    </div>
                </div>
                <div class="glass p-8 rounded-[2rem]">
                    <h4 class="text-zinc-500 font-black uppercase text-[10px] tracking-widest mb-6 italic">Linha de Emergência</h4>
                    <p class="text-4xl font-black text-white tracking-tighter leading-none">112 / 22 733 3333</p>
                    <p class="text-xs text-zinc-600 mt-4 font-bold">DISPONÍVEL 24/7 NO GÁLIA RP</p>
                </div>
            </div>
        </div>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=content)

@app.route('/fogos')
def fogos():
    content = f"""
    <div class="text-center max-w-4xl mx-auto">
        <h1 class="text-6xl font-black italic uppercase text-white mb-4 tracking-tighter">Centro de <span class="text-orange-500">Controlo</span></h1>
        <p class="text-zinc-500 font-bold uppercase tracking-[0.3em] mb-16">Monitorização de Ocorrências em Tempo Real</p>
        
        <div class="grid md:grid-cols-2 gap-10">
            <div class="glass p-16 rounded-[3rem] border-t-4 border-orange-600 hover:scale-105 transition duration-500">
                <p class="text-9xl font-black text-orange-500 leading-none mb-4 italic tracking-tighter">{dados.stats['incendios']}</p>
                <p class="text-xs font-black text-zinc-500 uppercase tracking-[0.4em]">Incêndios Florestais/Urbanos</p>
            </div>
            <div class="glass p-16 rounded-[3rem] border-t-4 border-red-600 hover:scale-105 transition duration-500">
                <p class="text-9xl font-black text-red-600 leading-none mb-4 italic tracking-tighter">{dados.stats['socorros']}</p>
                <p class="text-xs font-black text-zinc-500 uppercase tracking-[0.4em]">Emergências Médicas</p>
            </div>
        </div>

        <div class="mt-12 glass p-8 rounded-3xl flex justify-between items-center text-left">
            <div>
                <p class="text-[10px] font-black text-zinc-500 uppercase">Última Atualização</p>
                <p class="text-sm font-bold text-white italic">Servidores Gália RP - {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            </div>
            <i class="fas fa-sync text-zinc-800 animate-spin text-2xl"></i>
        </div>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=content)

@app.route('/equipa')
def equipa():
    rows = ""
    for email, info in dados.users.items():
        rows += f"""
        <tr class="border-b border-zinc-800/30 hover:bg-white/[0.02] transition">
            <td class="p-6">
                <div class="flex items-center space-x-4">
                    <div class="w-10 h-10 rounded-xl bg-zinc-800 flex items-center justify-center font-bold text-white">
                        {info['nome'][0]}
                    </div>
                    <div>
                        <p class="font-black text-white uppercase italic tracking-tighter">{info['nome']}</p>
                        <p class="text-[9px] text-zinc-600 font-bold uppercase">{email}</p>
                    </div>
                </div>
            </td>
            <td class="p-6">
                <span class="bg-red-600/10 text-red-500 border border-red-600/20 px-4 py-1 rounded-full text-[10px] font-black uppercase tracking-widest">
                    {info['patente']}
                </span>
            </td>
            <td class="p-6 text-right">
                <div class="flex items-center justify-end space-x-2">
                    <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                    <span class="text-[10px] font-black text-green-500 uppercase">Disponível</span>
                </div>
            </td>
        </tr>"""

    content = f"""
    <div class="mb-10">
        <h1 class="text-5xl font-black text-white italic uppercase tracking-tighter leading-none">Quadro <span class="text-red-600">Humanitário</span></h1>
        <p class="text-zinc-600 font-bold uppercase text-[10px] tracking-widest mt-2">Profissionais de elite ao serviço da comunidade</p>
    </div>
    
    <div class="glass rounded-[2rem] overflow-hidden shadow-2xl border border-zinc-800/50">
        <table class="w-full text-left">
            <thead class="bg-black/40 text-zinc-500 text-[10px] font-black uppercase tracking-[0.2em] border-b border-zinc-800/50">
                <tr><th class="p-6">Operacional</th><th class="p-6">Posto Graduado</th><th class="p-6 text-right">Estado</th></tr>
            </thead>
            <tbody class="divide-y divide-zinc-800/20">{rows}</tbody>
        </table>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=content)

@app.route('/viaturas')
def viaturas():
    v_cards = ""
    frota = getattr(dados, 'viaturas', [])
    for v in frota:
        cor = "text-green-500" if v['estado'] == "Operacional" else "text-orange-500"
        v_cards += f"""
        <div class="glass p-8 rounded-3xl border border-zinc-800 relative">
            <i class="fas fa-truck-fire absolute top-6 right-6 text-2xl text-zinc-800"></i>
            <h4 class="text-2xl font-black text-white mb-1 uppercase tracking-tighter italic">{v['id']}</h4>
            <p class="text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-6">{v['tipo']}</p>
            <div class="flex items-center space-x-2">
                <div class="w-2 h-2 rounded-full bg-current {cor}"></div>
                <span class="text-[10px] font-black uppercase {cor}">{v['estado']}</span>
            </div>
        </div>"""
    
    content = f"""
    <h1 class="text-5xl font-black uppercase italic text-white mb-12">Frota <span class="text-red-600 italic">Mecanizada</span></h1>
    <div class="grid md:grid-cols-3 gap-8">{v_cards}</div>
    """
    return render_template_string(HTML_LAYOUT, content=content)

@app.route('/candidatura')
def candidatura():
    content = """
    <div class="h-full flex flex-col">
        <div class="mb-10 text-center">
            <h1 class="text-5xl font-black text-white uppercase italic leading-none">Junta-te aos <span class="text-red-600">Melhores</span></h1>
            <p class="text-zinc-600 font-bold uppercase text-[10px] tracking-[0.4em] mt-4 italic">Processo de Recrutamento Permanente - Espinho</p>
        </div>
        <div class="flex-1 bg-white rounded-[3rem] shadow-2xl overflow-hidden border-[12px] border-zinc-900 shadow-red-900/10">
            <iframe src="https://forms.gle/XNtCDyekkgjiJaVE9" class="w-full h-full"></iframe>
        </div>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=content)

# --- SISTEMA DE ACESSO E DASHBOARD ---

@app.route('/login_page')
def login_page():
    content = """
    <div class="flex justify-center items-center h-[80vh]">
        <div class="glass p-12 rounded-[3rem] border border-zinc-800 w-full max-w-md shadow-2xl relative overflow-hidden">
            <div class="absolute -top-10 -left-10 w-40 h-40 bg-red-600/10 rounded-full blur-3xl"></div>
            <div class="text-center mb-12">
                <div class="bg-red-600 w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-6 rotate-12 shadow-xl shadow-red-900/20">
                    <i class="fas fa-lock text-white text-2xl -rotate-12"></i>
                </div>
                <h2 class="text-2xl font-black uppercase tracking-widest text-white italic leading-none">Portal Interno</h2>
                <p class="text-[9px] text-zinc-500 font-bold uppercase mt-3 tracking-widest italic leading-none">Acesso exclusivo para funcionários</p>
            </div>
            
            <form action="/login" method="POST" class="space-y-6">
                <div class="space-y-1">
                    <label class="text-[9px] font-black uppercase text-zinc-500 ml-4">Email Corporativo</label>
                    <input type="email" name="email" class="w-full bg-black/40 p-5 rounded-2xl border border-zinc-800 outline-none text-sm focus:border-red-600 transition text-white" required>
                </div>
                <div class="space-y-1">
                    <label class="text-[9px] font-black uppercase text-zinc-500 ml-4">Chave de Segurança</label>
                    <input type="password" name="senha" class="w-full bg-black/40 p-5 rounded-2xl border border-zinc-800 outline-none text-sm focus:border-red-600 transition text-white" required>
                </div>
                <button type="submit" class="w-full red-gradient py-5 rounded-2xl font-black uppercase tracking-widest text-white hover:opacity-90 transition shadow-lg shadow-red-900/40 mt-4 text-xs">Autenticar</button>
            </form>
        </div>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=content)

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')
    if email in dados.users and dados.users[email]['senha'] == senha:
        session.update({
            'user_email': email,
            'user_nome': dados.users[email]['nome'],
            'user_patente': dados.users[email]['patente']
        })
        return redirect(url_for('dashboard'))
    return redirect(url_for('login_page'))

@app.route('/dashboard')
def dashboard():
    if 'user_email' not in session: return redirect(url_for('login_page'))
    
    content = f"""
    <div class="animate-in slide-in-from-bottom duration-700">
        <h2 class="text-5xl font-black text-white italic uppercase tracking-tighter mb-2">Painel de <span class="text-red-600">Comando</span></h2>
        <p class="text-zinc-600 font-bold uppercase text-[10px] tracking-widest italic mb-12">Consola Administrativa BV Espinho</p>
        
        <div class="grid lg:grid-cols-3 gap-8">
            <div class="glass p-10 rounded-[2.5rem] border-t-8 border-red-700">
                <p class="text-xs font-black uppercase text-red-500 mb-8 italic tracking-widest underline decoration-red-900 underline-offset-8">Minhas Definições</p>
                <form action="/update_pass" method="POST" class="space-y-6">
                    <div>
                        <label class="text-[10px] font-black uppercase text-zinc-500 ml-2 italic">Nova Palavra-Passe</label>
                        <input type="password" name="nova_senha" class="w-full bg-black/50 p-4 rounded-xl border border-zinc-800 text-sm mt-2 focus:border-red-600 outline-none text-white font-bold" required>
                    </div>
                    <button class="w-full bg-red-700 py-4 rounded-xl text-[10px] font-black uppercase hover:bg-red-600 transition shadow-lg shadow-red-950">Gravar em dados.py</button>
                </form>
            </div>

            <div class="lg:col-span-2 glass p-10 rounded-[2.5rem]">
                <p class="text-xs font-black uppercase text-zinc-500 mb-8 italic tracking-widest underline decoration-zinc-800 underline-offset-8">Controlo de Operativos</p>
                <form action="/add_user" method="POST" class="grid md:grid-cols-2 gap-6">
                    <div class="space-y-4">
                        <input type="text" name="nome" placeholder="Nome do Operativo" class="w-full bg-black/50 p-4 rounded-xl border border-zinc-800 text-sm focus:border-red-600 outline-none text-white" required>
                        <input type="email" name="email" placeholder="Email @galiarp.pt" class="w-full bg-black/50 p-4 rounded-xl border border-zinc-800 text-sm focus:border-red-600 outline-none text-white" required>
                    </div>
                    <div class="space-y-4">
                        <select name="patente" class="w-full bg-black/50 p-4 rounded-xl border border-zinc-800 text-sm focus:border-red-600 outline-none text-white uppercase font-bold">
                            <option value="Estagiário">Estagiário</option>
                            <option value="Bombeiro 3ª">Bombeiro 3ª</option>
                            <option value="Bombeiro 2ª">Bombeiro 2ª</option>
                            <option value="Chefe">Chefe</option>
                            <option value="Oficial">Oficial</option>
                        </select>
                        <input type="password" name="senha" placeholder="Senha Temporária" class="w-full bg-black/50 p-4 rounded-xl border border-zinc-800 text-sm focus:border-red-600 outline-none text-white" required>
                    </div>
                    <button class="md:col-span-2 bg-white text-black py-4 rounded-xl text-[10px] font-black uppercase hover:bg-zinc-200 transition">Registar na Base de Dados</button>
                </form>
            </div>
            
            <div class="lg:col-span-3 glass p-10 rounded-[2.5rem] border border-orange-600/20">
                <p class="text-xs font-black uppercase text-orange-500 mb-8 italic tracking-widest underline decoration-orange-950 underline-offset-8">Atualizar Relatórios de Campo</p>
                <form action="/update_stats" method="POST" class="flex flex-wrap gap-8 items-center">
                    <div class="flex items-center space-x-4">
                        <label class="text-[10px] font-black uppercase text-zinc-500 italic">Incêndios</label>
                        <input type="number" name="incendios" value="{dados.stats['incendios']}" class="bg-black/50 p-4 rounded-xl border border-zinc-800 w-24 text-center font-black text-orange-500 outline-none focus:border-orange-600">
                    </div>
                    <div class="flex items-center space-x-4">
                        <label class="text-[10px] font-black uppercase text-zinc-500 italic">Socorros</label>
                        <input type="number" name="socorros" value="{dados.stats['socorros']}" class="bg-black/50 p-4 rounded-xl border border-zinc-800 w-24 text-center font-black text-red-500 outline-none focus:border-red-600">
                    </div>
                    <button class="bg-orange-600 text-white px-12 py-4 rounded-xl text-[10px] font-black uppercase hover:bg-orange-500 transition shadow-lg shadow-orange-950">Enviar Relatório Digital</button>
                </form>
            </div>
        </div>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=content)

# --- OPERAÇÕES DE DADOS (POST) ---

@app.route('/update_pass', methods=['POST'])
def update_pass():
    if 'user_email' in session:
        dados.users[session['user_email']]['senha'] = request.form.get('nova_senha')
        salvar_dados()
    return redirect(url_for('dashboard'))

@app.route('/add_user', methods=['POST'])
def add_user():
    if 'user_email' in session:
        email = request.form.get('email')
        dados.users[email] = {
            "nome": request.form.get('nome'),
            "senha": request.form.get('senha'),
            "patente": request.form.get('patente'),
            "data_adesao": datetime.now().strftime("%d/%m/%Y")
        }
        salvar_dados()
    return redirect(url_for('dashboard'))

@app.route('/update_stats', methods=['POST'])
def update_stats():
    if 'user_email' in session:
        dados.stats['incendios'] = int(request.form.get('incendios'))
        dados.stats['socorros'] = int(request.form.get('socorros'))
        salvar_dados()
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# No final do ficheiro, substitui o app.run por isto:
app = app
