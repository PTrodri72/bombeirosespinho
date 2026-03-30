from flask import Flask, render_template_string, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'galia_esp_2026_oficial'

# --- BANCO DE DADOS EM MEMÓRIA ---
stats = {"incendios": 124}
HIERARQUIA = ["Comandante", "2º Comandante", "Adjunto do Comando", "Oficial Bombeiro", "Chefe", "Sub Chefe", "Bombeiro de 1ª", "Bombeiro de 2ª", "Bombeiro de 3ª", "Estagiario"]

users = {
    "igor.rodrigues@comandobombeiros.galiarp.pt": {
        "nome": "Igor Rodrigues",
        "senha": "GRPGALAIMELHORSERVIDOR",
        "patente": "Comandante"
    }
}

# --- ESTRUTURA VISUAL COM BLOQUEIO DE INSPEÇÃO ---
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="pt-pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bombeiros de Espinho | Gália RP</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    
    <script>
        // BLOQUEIO DE F12 E INSPEÇÃO
        document.addEventListener('contextmenu', event => event.preventDefault()); // Bloqueia Botão Direito
        
        document.onkeydown = function(e) {
            if(event.keyCode == 123) { return false; } // Bloqueia F12
            if(e.ctrlKey && e.shiftKey && e.keyCode == 'I'.charCodeAt(0)) { return false; } // Bloqueia Ctrl+Shift+I
            if(e.ctrlKey && e.shiftKey && e.keyCode == 'C'.charCodeAt(0)) { return false; } // Bloqueia Ctrl+Shift+C
            if(e.ctrlKey && e.shiftKey && e.keyCode == 'J'.charCodeAt(0)) { return false; } // Bloqueia Ctrl+Shift+J
            if(e.ctrlKey && e.keyCode == 'U'.charCodeAt(0)) { return false; } // Bloqueia Ctrl+U (Ver Código Fonte)
        }
    </script>
</head>
<body class="bg-zinc-900 text-zinc-100 font-sans min-h-screen select-none">

    <nav class="bg-red-800 p-4 shadow-2xl sticky top-0 z-50 border-b-4 border-red-900">
        <div class="container mx-auto flex justify-between items-center">
            <div class="flex items-center space-x-3">
                <i class="fas fa-fire-extinguisher text-2xl text-white"></i>
                <span class="font-black uppercase tracking-tighter text-xl">BV ESPINHO</span>
            </div>
            
            <div class="hidden md:flex items-center space-x-8 text-[11px] font-bold uppercase tracking-widest">
                <a href="/" class="hover:text-yellow-400 transition">Comunicados</a>
                <a href="/fogos" class="hover:text-yellow-400 transition">Fogos</a>
                <a href="/equipa" class="hover:text-yellow-400 transition">Equipa Bombeiros</a>
                <a href="/candidatura" class="bg-white text-red-800 px-3 py-1 rounded hover:bg-zinc-200 transition font-black">Candidatura</a>
            </div>

            <div class="border-l border-red-700 pl-6">
                {% if session.get('user_email') %}
                    <div class="flex items-center space-x-4">
                        <div class="text-right">
                            <p class="text-[9px] leading-none text-yellow-400 font-bold uppercase">{{ session['user_patente'] }}</p>
                            <p class="text-xs font-black">{{ session['user_nome'] }}</p>
                        </div>
                        <a href="/dashboard" class="bg-zinc-950 p-2 rounded hover:bg-white hover:text-black transition"><i class="fas fa-user-cog"></i></a>
                        <a href="/logout" class="text-white opacity-60 hover:opacity-100 transition"><i class="fas fa-power-off"></i></a>
                    </div>
                {% else %}
                    <a href="/login_page" class="bg-zinc-950 text-white px-5 py-2 rounded-sm border border-zinc-700 hover:bg-white hover:text-black transition text-xs font-bold uppercase tracking-widest">
                        <i class="fas fa-lock mr-2"></i> Login
                    </a>
                {% endif %}
            </div>
        </div>
    </nav>

    <main class="container mx-auto p-6 md:p-12">
        {% block content %}{% endblock %}
    </main>

</body>
</html>
"""

# --- ROTAS PÚBLICAS ---

@app.route('/')
def home():
    content = """
    <div class="max-w-4xl">
        <h1 class="text-6xl font-black italic uppercase mb-8 leading-none">Comunicados<br><span class="text-red-600">Oficiais</span></h1>
        <div class="bg-zinc-800 p-8 rounded-lg border-l-8 border-red-600 shadow-2xl">
            <p class="text-red-500 text-xs font-black mb-2 uppercase tracking-widest italic">Quartel de Espinho</p>
            <h3 class="text-2xl font-bold italic">Bem-vindo, Comandante Igor Rodrigues.</h3>
            <p class="text-zinc-400 mt-4 leading-relaxed font-light">Este portal é de acesso público para consulta de fogos e equipa, mas restrito para alteração de dados de comando. Mantenha as suas credenciais seguras.</p>
        </div>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=content)

@app.route('/fogos')
def fogos():
    content = f"""
    <div class="text-center py-16">
        <h1 class="text-5xl font-black uppercase italic mb-12 tracking-tighter">Estado de <span class="text-orange-500">Ocorrências</span></h1>
        <div class="inline-grid grid-cols-1 bg-zinc-800 p-12 rounded-3xl border border-zinc-700 shadow-2xl">
            <span class="text-9xl font-black text-orange-500">{stats['incendios']}</span>
            <p class="text-zinc-400 font-black uppercase tracking-[0.4em] text-sm mt-4">Incêndios Dominados</p>
        </div>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=content)

@app.route('/equipa')
def equipa():
    rows = ""
    for email, data in users.items():
        rows += f"<tr class='border-b border-zinc-800'><td class='p-5 font-black uppercase italic'>{data['nome']}</td><td class='p-5'><span class='text-red-500 font-mono text-xs font-bold uppercase'>{data['patente']}</span></td><td class='p-5 text-right text-green-500 font-black text-[10px] uppercase tracking-widest'>Ativo</td></tr>"
    content = f"""
    <h1 class="text-4xl font-black uppercase italic mb-10">Quadro de <span class="text-red-600">Pessoal</span></h1>
    <div class="bg-zinc-950 rounded shadow-2xl border border-zinc-800 overflow-hidden">
        <table class="w-full text-left">
            <thead class="bg-zinc-900 text-zinc-500 text-[10px] font-black uppercase tracking-widest"><tr><th class="p-5">Nome</th><th class="p-5">Patente</th><th class="p-5 text-right">Status</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=content)

@app.route('/candidatura')
def candidatura():
    content = """
    <div class="h-[80vh] flex flex-col">
        <h1 class="text-4xl font-black uppercase italic mb-6">Escola de <span class="text-red-600">Estagiários</span></h1>
        <iframe src="https://forms.gle/XNtCDyekkgjiJaVE9" class="flex-1 bg-white rounded-lg border-none"></iframe>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=content)

@app.route('/login_page')
def login_page():
    content = """
    <div class="flex justify-center py-10">
        <form action="/login" method="POST" class="bg-zinc-950 p-10 rounded border border-zinc-800 w-full max-w-sm shadow-2xl">
            <h2 class="text-xl font-black uppercase italic mb-6 text-center text-red-500">Autenticação</h2>
            <div class="space-y-4">
                <input type="email" name="email" placeholder="E-mail" class="w-full bg-zinc-900 p-4 rounded border border-zinc-800 outline-none focus:border-red-600 text-sm" required>
                <input type="password" name="senha" placeholder="Senha" class="w-full bg-zinc-900 p-4 rounded border border-zinc-800 outline-none focus:border-red-600 text-sm" required>
                <button type="submit" class="w-full bg-red-700 py-4 rounded font-bold uppercase tracking-widest hover:bg-red-800 transition">Entrar</button>
            </div>
        </form>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=content)

@app.route('/login', methods=['POST'])
def login():
    email, senha = request.form.get('email'), request.form.get('senha')
    if email in users and users[email]['senha'] == senha:
        session.update({'user_email': email, 'user_nome': users[email]['nome'], 'user_patente': users[email]['patente']})
        return redirect(url_for('dashboard'))
    return redirect(url_for('login_page'))

@app.route('/dashboard')
def dashboard():
    if 'user_email' not in session: return redirect(url_for('login_page'))
    content = f"""
    <div class="bg-zinc-950 p-10 rounded-lg border-t-8 border-red-700 shadow-2xl">
        <h2 class="text-2xl font-black uppercase italic mb-6">Painel de Controlo: {session['user_nome']}</h2>
        <form action="/update_pass" method="POST" class="max-w-xs space-y-4">
            <p class="text-xs font-black uppercase text-red-500">Mudar Palavra-passe</p>
            <input type="password" name="nova_senha" placeholder="Nova Senha" class="w-full bg-zinc-900 p-3 rounded border border-zinc-800 text-sm">
            <button class="bg-zinc-800 px-6 py-2 rounded text-xs font-bold uppercase hover:bg-white hover:text-black transition">Guardar</button>
        </form>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=content)

@app.route('/update_pass', methods=['POST'])
def update_pass():
    if 'user_email' in session: users[session['user_email']]['senha'] = request.form.get('nova_senha')
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

app = app
