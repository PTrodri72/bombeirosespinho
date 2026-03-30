from flask import Flask, render_template_string, request, redirect, session, url_for
import dados  # Onde as informações são guardadas
import importlib
import os

app = Flask(__name__)
app.secret_key = 'galia_espinho_vidal_por_vida'

def salvar_no_ficheiro():
    """Escreve as alterações no dados.py para não perder nada"""
    caminho = os.path.join(os.path.dirname(__file__), 'dados.py')
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write("# BASE DE DADOS OPERACIONAL - BV ESPINHO\n")
        f.write(f"users = {repr(dados.users)}\n")
        f.write(f"stats = {repr(dados.stats)}\n")
    importlib.reload(dados)

# --- INTERFACE (HTML + CONTEÚDO) ---
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="pt-pt">
<head>
    <meta charset="UTF-8">
    <title>BV Espinho | Portal Oficial Gália RP</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <script>
        // Bloqueio de Ferramentas de Programador
        document.addEventListener('contextmenu', e => e.preventDefault());
        document.onkeydown = function(e) {
            if(event.keyCode == 123 || (e.ctrlKey && e.shiftKey && (e.keyCode == 73 || e.keyCode == 74 || e.keyCode == 67)) || (e.ctrlKey && e.keyCode == 85)) return false;
        }
    </script>
</head>
<body class="bg-zinc-950 text-zinc-100 font-sans flex h-screen overflow-hidden">

    <aside class="w-72 bg-zinc-900 border-r border-zinc-800 flex flex-col shadow-2xl">
        <div class="p-8 border-b border-zinc-800 text-center bg-black/20">
            <div class="bg-red-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg shadow-red-900/40">
                <i class="fas fa-fire-extinguisher text-2xl text-white"></i>
            </div>
            <h1 class="text-xl font-black italic tracking-tighter uppercase">BV <span class="text-red-600">Espinho</span></h1>
            <p class="text-[9px] text-zinc-500 font-bold uppercase tracking-[0.3em]">Quartel n.º 1</p>
        </div>
        
        <nav class="flex-1 p-6 space-y-3 text-[11px] font-black uppercase tracking-widest">
            <a href="/" class="flex items-center p-3 rounded-lg hover:bg-zinc-800 transition group">
                <i class="fas fa-home w-8 text-red-600 group-hover:scale-110 transition"></i> Início
            </a>
            <a href="/fogos" class="flex items-center p-3 rounded-lg hover:bg-zinc-800 transition group">
                <i class="fas fa-flame w-8 text-orange-500 group-hover:scale-110 transition"></i> Ocorrências
            </a>
            <a href="/equipa" class="flex items-center p-3 rounded-lg hover:bg-zinc-800 transition group">
                <i class="fas fa-shield-halved w-8 text-blue-500 group-hover:scale-110 transition"></i> Quadro Ativo
            </a>
            <a href="/candidatura" class="flex items-center p-3 rounded-lg bg-red-700/10 text-red-500 border border-red-700/20 hover:bg-red-700 hover:text-white transition group">
                <i class="fas fa-file-signature w-8"></i> Recrutamento
            </a>
        </nav>

        <div class="p-6 border-t border-zinc-800">
            {% if session.get('user_email') %}
                <div class="bg-black/40 p-4 rounded-xl border border-zinc-800">
                    <p class="text-[10px] text-red-500 font-black uppercase">{{ session['user_patente'] }}</p>
                    <p class="text-xs font-bold truncate">{{ session['user_nome'] }}</p>
                    <div class="flex mt-4 space-x-2">
                        <a href="/dashboard" class="bg-zinc-800 p-2 rounded-lg flex-1 text-center hover:bg-white hover:text-black transition"><i class="fas fa-user-gear"></i></a>
                        <a href="/logout" class="bg-zinc-800 p-2 rounded-lg flex-1 text-center hover:bg-red-600 transition"><i class="fas fa-power-off"></i></a>
                    </div>
                </div>
            {% else %}
                <a href="/login_page" class="block w-full bg-zinc-100 text-black text-center py-3 rounded-lg text-xs font-black hover:bg-red-600 hover:text-white transition uppercase tracking-widest">Acesso Restrito</a>
            {% endif %}
        </div>
    </aside>

    <main class="flex-1 overflow-y-auto p-16">
        {% block content %}{% endblock %}
    </main>

</body>
</html>
"""

# --- ROTAS (CONTEÚDO DAS ABAS) ---

@app.route('/')
def home():
    content = """
    <div class="max-w-4xl animate-fadeIn">
        <h1 class="text-7xl font-black italic uppercase leading-none mb-10">Portal de<br><span class="text-red-600">Comunicações</span></h1>
        
        <div class="grid gap-8">
            <div class="bg-zinc-900 p-8 rounded-2xl border-l-8 border-red-600 shadow-2xl">
                <span class="bg-red-600 text-white text-[9px] px-2 py-1 rounded font-bold uppercase">Urgente</span>
                <h3 class="text-2xl font-bold mt-4 italic">Alerta de Risco de Incêndio: Nível 4</h3>
                <p class="text-zinc-400 mt-4 leading-relaxed">Informamos a população de Espinho que, devido às condições meteorológicas, o risco de incêndio florestal é elevado. Todas as licenças de queima estão suspensas.</p>
            </div>

            <div class="grid md:grid-cols-2 gap-6">
                <div class="bg-zinc-900/50 p-6 rounded-xl border border-zinc-800">
                    <i class="fas fa-history text-red-600 mb-4 text-xl"></i>
                    <h4 class="font-bold uppercase italic tracking-widest text-sm text-zinc-300">Nossa História</h4>
                    <p class="text-xs text-zinc-500 mt-2 leading-relaxed italic">Fundada em 2026, a corporação de Espinho no Gália RP dedica-se à proteção de bens e pessoas, com foco na excelência e rapidez.</p>
                </div>
                <div class="bg-zinc-900/50 p-6 rounded-xl border border-zinc-800">
                    <i class="fas fa-kit-medical text-red-600 mb-4 text-xl"></i>
                    <h4 class="font-bold uppercase italic tracking-widest text-sm text-zinc-300">Emergência Médica</h4>
                    <p class="text-xs text-zinc-500 mt-2 leading-relaxed italic">Contamos com 2 ambulâncias de socorro equipadas com desfibrilhadores (DAE) e técnicos prontos para atuar.</p>
                </div>
            </div>
        </div>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=content)

@app.route('/fogos')
def fogos():
    content = f"""
    <div class="text-center py-10">
        <h1 class="text-5xl font-black uppercase italic mb-16 tracking-tighter">Centro de <span class="text-orange-600 italic">Estatística</span></h1>
        
        <div class="grid md:grid-cols-3 gap-10 max-w-5xl mx-auto">
            <div class="bg-zinc-900 p-12 rounded-3xl border border-zinc-800 relative overflow-hidden group hover:border-orange-600 transition duration-500">
                <i class="fas fa-fire-flame-curved absolute -top-5 -right-5 text-8xl text-orange-600/10 group-hover:text-orange-600/20 transition"></i>
                <p class="text-7xl font-black text-orange-500">{dados.stats['incendios']}</p>
                <p class="text-xs font-bold uppercase text-zinc-500 mt-4 tracking-widest">Incêndios Dominados</p>
            </div>
            
            <div class="bg-zinc-900 p-12 rounded-3xl border border-zinc-800 group hover:border-red-600 transition duration-500">
                <p class="text-7xl font-black text-red-600">12</p>
                <p class="text-xs font-bold uppercase text-zinc-500 mt-4 tracking-widest">Viaturas Prontas</p>
            </div>

            <div class="bg-zinc-900 p-12 rounded-3xl border border-zinc-800 group hover:border-blue-600 transition duration-500">
                <p class="text-7xl font-black text-blue-600">100%</p>
                <p class="text-xs font-bold uppercase text-zinc-500 mt-4 tracking-widest">Eficiência Operacional</p>
            </div>
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
            <td class="p-6">
                <div class="flex items-center space-x-3">
                    <div class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
                    <span class="font-black uppercase italic tracking-tighter text-lg">{info['nome']}</span>
                </div>
            </td>
            <td class="p-6"><span class="text-red-500 font-mono text-xs font-bold uppercase border border-red-500/30 px-3 py-1 rounded tracking-widest">{info['patente']}</span></td>
            <td class="p-6 text-right font-black italic text-zinc-600 text-xs uppercase">Operacional Gália RP</td>
        </tr>"""
    
    content = f"""
    <h1 class="text-5xl font-black uppercase italic mb-10 leading-none">Quadro de <span class="text-red-600 italic">Honra</span></h1>
    <div class="bg-zinc-900/30 rounded-2xl border border-zinc-800 overflow-hidden shadow-2xl backdrop-blur-xl">
        <table class="w-full text-left">
            <thead class="bg-black/60 text-zinc-500 text-[10px] font-black uppercase tracking-[0.2em]">
                <tr><th class="p-6">Operacional</th><th class="p-6 text-center">Posto Graduado</th><th class="p-6 text-right">Estatuto</th></tr>
            </thead>
            <tbody class="divide-y divide-zinc-800">{rows}</tbody>
        </table>
    </div>"""
    return render_template_string(HTML_LAYOUT, content=content)

@app.route('/candidatura')
def candidatura():
    content = """
    <div class="h-full flex flex-col">
        <div class="mb-8">
            <h1 class="text-4xl font-black uppercase italic italic leading-none">Recrutamento <span class="text-red-600 italic">Aberto</span></h1>
            <p class="text-zinc-500 text-sm mt-2 font-bold uppercase tracking-widest">Escola de Estagiários - Concurso 2026</p>
        </div>
        <div class="flex-1 bg-white rounded-3xl shadow-2xl overflow-hidden border-8 border-zinc-900">
            <iframe src="https://forms.gle/XNtCDyekkgjiJaVE9" class="w-full h-full">A carregar...</iframe>
        </div>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=content)

@app.route('/login_page')
def login_page():
    content = """
    <div class="flex justify-center items-center h-full">
        <form action="/login" method="POST" class="bg-zinc-900 p-12 rounded-[2rem] border border-zinc-800 w-full max-w-md shadow-2xl relative">
            <div class="absolute -top-10 left-1/2 -translate-x-1/2 bg-red-600 w-20 h-20 rounded-3xl flex items-center justify-center rotate-12 shadow-xl">
                <i class="fas fa-lock text-3xl text-white -rotate-12"></i>
            </div>
            <div class="text-center mt-6 mb-10">
                <h2 class="text-2xl font-black uppercase tracking-widest italic text-white leading-none">Terminal de Comando</h2>
                <p class="text-[9px] text-zinc-500 font-bold uppercase mt-2">Área de Acesso Restrito aos B.V. Espinho</p>
            </div>
            <div class="space-y-6">
                <input type="email" name="email" placeholder="E-mail Institucional" class="w-full bg-black/50 p-5 rounded-2xl border border-zinc-800 outline-none text-sm focus:border-red-600 transition" required>
                <input type="password" name="senha" placeholder="Palavra-passe de Comando" class="w-full bg-black/50 p-5 rounded-2xl border border-zinc-800 outline-none text-sm focus:border-red-600 transition" required>
                <button type="submit" class="w-full bg-red-700 py-5 rounded-2xl font-black uppercase tracking-widest hover:bg-red-600 transition shadow-lg shadow-red-900/30">Autenticar Sistema</button>
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
    <div class="bg-zinc-900 p-12 rounded-[3rem] border border-zinc-800 shadow-2xl relative overflow-hidden">
        <div class="absolute top-0 right-0 p-10 opacity-5"><i class="fas fa-user-shield text-[200px]"></i></div>
        <h2 class="text-4xl font-black uppercase italic mb-2 tracking-tighter">Painel Operacional</h2>
        <p class="text-xs text-zinc-500 mb-12 font-bold uppercase tracking-widest italic">Sessão Ativa: {session['user_nome']} ({session['user_patente']})</p>
        
        <div class="grid md:grid-cols-2 gap-10">
            <form action="/update_pass" method="POST" class="bg-black/30 p-8 rounded-3xl border border-zinc-800 space-y-6 relative z-10">
                <p class="text-xs font-black uppercase text-red-500 tracking-widest">Alterar Senha Interna (Permanente)</p>
                <input type="password" name="nova_senha" placeholder="Introduzir nova senha" class="w-full bg-zinc-950 p-4 rounded-xl border border-zinc-800 text-sm outline-none focus:border-red-600">
                <button class="w-full bg-red-700 py-4 rounded-xl text-xs font-black uppercase hover:bg-red-600 transition shadow-lg">Atualizar Ficheiro dados.py</button>
            </form>
            
            <div class="bg-black/30 p-8 rounded-3xl border border-zinc-800 relative z-10">
                <p class="text-xs font-black uppercase text-zinc-500 tracking-widest mb-6 border-b border-zinc-800 pb-2 italic">Ações Rápidas</p>
                <p class="text-xs text-zinc-400 italic font-light mb-4 leading-relaxed">Qualquer alteração feita no teu perfil será gravada no código-fonte do sistema para persistência total.</p>
                <div class="flex gap-4">
                    <div class="bg-zinc-800 p-4 rounded-xl text-center flex-1">
                        <p class="text-lg font-black">{dados.stats['incendios']}</p>
                        <p class="text-[8px] uppercase font-bold text-zinc-500 italic">Meus Fogos</p>
                    </div>
                </div>
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
            salvar_no_ficheiro()
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
