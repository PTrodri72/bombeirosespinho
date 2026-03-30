from flask import Flask, render_template_string, request, redirect, session, url_for
import dados  # Importa o teu ficheiro de persistência
import importlib
import os

app = Flask(__name__)
app.secret_key = 'galia_bombeiros_espinho_2026'

def atualizar_ficheiro_dados():
    """Reescreve o ficheiro dados.py com as informações mais recentes"""
    caminho = os.path.join(os.path.dirname(__file__), 'dados.py')
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write("# Ficheiro de Armazenamento Automático - BV ESPINHO\n")
        f.write(f"users = {repr(dados.users)}\n")
        f.write(f"stats = {repr(dados.stats)}\n")
    importlib.reload(dados)

# --- INTERFACE VISUAL (HTML/CSS) ---
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="pt-pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BV Espinho | Portal Operacional</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <script>
        // SEGURANÇA ANT-INSPEÇÃO
        document.addEventListener('contextmenu', e => e.preventDefault());
        document.onkeydown = function(e) {
            if(event.keyCode == 123 || (e.ctrlKey && e.shiftKey && (e.keyCode == 73 || e.keyCode == 74 || e.keyCode == 67)) || (e.ctrlKey && e.keyCode == 85)) return false;
        }
    </script>
    <style>
        .sidebar-active { border-left: 4px solid #ef4444; background: rgba(239, 68, 68, 0.1); }
        body { -webkit-user-select: none; -moz-user-select: none; -ms-user-select: none; user-select: none; }
    </style>
</head>
<body class="bg-zinc-950 text-zinc-100 font-sans flex h-screen overflow-hidden">

    <aside class="w-64 bg-zinc-900 border-r border-zinc-800 flex flex-col">
        <div class="p-6 border-b border-zinc-800 text-center">
            <i class="fas fa-fire-extinguisher text-3xl text-red-600 mb-2"></i>
            <h1 class="text-xl font-black tracking-tighter uppercase italic">BV <span class="text-red-600">Espinho</span></h1>
            <p class="text-[9px] text-zinc-500 font-bold uppercase tracking-widest">Gália Roleplay</p>
        </div>
        
        <nav class="flex-1 p-4 space-y-2 mt-4 text-[11px] font-black uppercase tracking-widest">
            <a href="/" class="flex items-center p-3 rounded hover:bg-zinc-800 transition"><i class="fas fa-bullhorn w-6 text-red-600"></i> Comunicados</a>
            <a href="/fogos" class="flex items-center p-3 rounded hover:bg-zinc-800 transition"><i class="fas fa-fire w-6 text-red-600"></i> Fogos</a>
            <a href="/equipa" class="flex items-center p-3 rounded hover:bg-zinc-800 transition"><i class="fas fa-users w-6 text-red-600"></i> Equipa</a>
            <a href="/candidatura" class="flex items-center p-3 rounded hover:bg-zinc-800 transition text-yellow-500"><i class="fas fa-file-signature w-6"></i> Candidatura</a>
        </nav>

        <div class="p-4 border-t border-zinc-800 bg-black/20">
            {% if session.get('user_email') %}
                <p class="text-[9px] text-zinc-500 uppercase font-bold">Operacional:</p>
                <p class="text-xs font-black truncate">{{ session['user_nome'] }}</p>
                <div class="flex mt-3 space-x-2">
                    <a href="/dashboard" class="bg-zinc-800 p-2 rounded flex-1 text-center hover:bg-red-700 transition"><i class="fas fa-cog text-[10px]"></i></a>
                    <a href="/logout" class="bg-zinc-800 p-2 rounded flex-1 text-center hover:bg-zinc-700 transition"><i class="fas fa-power-off text-[10px]"></i></a>
                </div>
            {% else %}
                <a href="/login_page" class="block w-full bg-red-700 text-center py-2 rounded text-[10px] font-black hover:bg-red-800 transition uppercase">Login Bombeiros</a>
            {% endif %}
        </div>
    </aside>

    <main class="flex-1 overflow-y-auto p-12 bg-gradient-to-br from-zinc-950 to-black">
        {% block content %}{% endblock %}
    </main>

</body>
</html>
"""

# --- ROTAS ---

@app.route('/')
def home():
    content = """
    <div class="max-w-4xl">
        <h1 class="text-6xl font-black italic uppercase mb-8 leading-none">Últimos<br><span class="text-red-600 text-7xl">Comunicados</span></h1>
        <div class="bg-zinc-900/50 p-8 rounded-xl border border-zinc-800 shadow-2xl relative overflow-hidden">
            <div class="absolute top-0 right-0 p-4 opacity-5"><i class="fas fa-shield-alt text-9xl"></i></div>
            <span class="text-red-500 text-xs font-black uppercase tracking-widest">Comando AHBV Espinho</span>
            <h3 class="text-2xl font-bold mt-2">Sistema de Gestão 2026</h3>
            <p class="text-zinc-400 mt-4 leading-relaxed font-light">Este portal é o centro de operações digital dos Bombeiros Voluntários de Espinho. Aqui, os civis podem acompanhar o nosso esforço no terreno e os operacionais gerir as suas carreiras.</p>
        </div>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=content)

@app.route('/fogos')
def fogos():
    content = f"""
    <div class="text-center py-10">
        <h1 class="text-5xl font-black uppercase italic mb-16 italic tracking-tighter">Registo de <span class="text-orange-600">Ocorrências</span></h1>
        <div class="inline-grid grid-cols-1 bg-zinc-900 p-16 rounded-[3rem] border-2 border-orange-600/30 shadow-[0_0_50px_rgba(234,88,12,0.1)]">
            <span class="text-[120px] font-black text-orange-500 leading-none drop-shadow-lg">{dados.stats['incendios']}</span>
            <p class="text-zinc-500 font-black uppercase tracking-[0.5em] text-xs mt-6">Incêndios Totalmente Dominados</p>
        </div>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=content)

@app.route('/equipa')
def equipa():
    rows = ""
    for email, info in dados.users.items():
        rows += f"""
        <tr class="border-b border-zinc-800/50 hover:bg-white/5 transition">
            <td class="p-5 font-black uppercase italic tracking-tighter">{info['nome']}</td>
            <td class="p-5 text-red-500 font-mono text-xs font-bold uppercase tracking-widest">{info['patente']}</td>
            <td class="p-5 text-right"><span class="bg-green-500/10 text-green-500 text-[9px] px-2 py-1 rounded-full font-black border border-green-500/20">QUADRO ATIVO</span></td>
        </tr>"""
    content = f"""
    <h1 class="text-4xl font-black uppercase italic mb-10 leading-none tracking-tighter">Corpo <span class="text-red-600">Operacional</span></h1>
    <div class="bg-zinc-900/50 rounded-xl border border-zinc-800 overflow-hidden shadow-2xl">
        <table class="w-full text-left">
            <thead class="bg-black/40 text-zinc-500 text-[10px] font-black uppercase tracking-widest">
                <tr><th class="p-5">Nome de Guerra</th><th class="p-5 text-center">Patente</th><th class="p-5 text-right">Estado</th></tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
    </div>"""
    return render_template_string(HTML_LAYOUT, content=content)

@app.route('/candidatura')
def candidatura():
    content = """
    <div class="h-full flex flex-col">
        <h1 class="text-4xl font-black uppercase italic mb-6">Escola de <span class="text-red-600">Recrutas</span></h1>
        <div class="flex-1 bg-white rounded-xl shadow-2xl overflow-hidden border-4 border-zinc-900">
            <iframe src="https://forms.gle/XNtCDyekkgjiJaVE9" class="w-full h-full">A carregar formulário...</iframe>
        </div>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=content)

@app.route('/login_page')
def login_page():
    content = """
    <div class="flex justify-center items-center h-full">
        <form action="/login" method="POST" class="bg-zinc-900 p-10 rounded-2xl border border-zinc-800 w-full max-w-sm shadow-2xl">
            <div class="text-center mb-10 italic">
                <h2 class="text-2xl font-black uppercase tracking-widest text-red-600">Comando Interno</h2>
                <p class="text-[9px] text-zinc-500 font-bold uppercase">Acesso Restrito a Operacionais</p>
            </div>
            <div class="space-y-4">
                <input type="email" name="email" placeholder="E-mail Corporativo" class="w-full bg-black/50 p-4 rounded-lg border border-zinc-800 outline-none text-sm focus:border-red-600 transition" required>
                <input type="password" name="senha" placeholder="Palavra-passe" class="w-full bg-black/50 p-4 rounded-lg border border-zinc-800 outline-none text-sm focus:border-red-600 transition" required>
                <button type="submit" class="w-full bg-red-700 py-4 rounded-lg font-black uppercase tracking-widest hover:bg-red-800 transition shadow-lg shadow-red-900/20">Entrar no Terminal</button>
            </div>
        </form>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=content)

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
    <div class="bg-zinc-900 p-10 rounded-2xl border border-zinc-800 shadow-2xl border-t-8 border-red-700">
        <h2 class="text-3xl font-black uppercase italic mb-2 tracking-tighter leading-none">Painel de Controlo</h2>
        <p class="text-xs text-zinc-500 mb-10 font-bold uppercase tracking-widest">Bem-vindo, {session['user_nome']}</p>
        
        <div class="grid md:grid-cols-2 gap-10">
            <form action="/update_pass" method="POST" class="bg-black/30 p-6 rounded-xl border border-zinc-800 space-y-4">
                <p class="text-[10px] font-black uppercase text-red-500 tracking-widest">Segurança: Alterar Senha Permanente</p>
                <input type="password" name="nova_senha" placeholder="Introduzir nova palavra-passe" class="w-full bg-zinc-950 p-3 rounded border border-zinc-800 text-sm outline-none focus:border-red-600">
                <button class="w-full bg-red-700 py-3 rounded text-[10px] font-black uppercase hover:bg-red-800 transition shadow-lg">Atualizar Ficheiro dados.py</button>
            </form>
            
            <div class="bg-black/30 p-6 rounded-xl border border-zinc-800">
                <p class="text-[10px] font-black uppercase text-zinc-500 tracking-widest mb-4">Informações do Sistema</p>
                <p class="text-sm text-zinc-400 italic font-light">Este painel permite-te gerir o teu perfil. Todas as alterações feitas aqui são escritas diretamente no código-fonte dos dados.</p>
            </div>
        </div>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=content)

@app.route('/update_pass', methods=['POST'])
def update_pass():
    if 'user_email' in session:
        nova = request.form.get('nova_senha')
        if nova:
            dados.users[session['user_email']]['senha'] = nova
            atualizar_ficheiro_dados() # Grava as alterações no dados.py
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
