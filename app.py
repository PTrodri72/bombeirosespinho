from flask import Flask, render_template_string, request, redirect, session, url_for
import os
import importlib

# Tentar importar os dados, se não existir, cria o dicionário básico para o site não travar
try:
    import dados
except ImportError:
    class MockDados:
        users = {"igor.rodrigues@comandobombeiros.galiarp.pt": {"nome": "Igor Rodrigues", "senha": "GRPGALAIMELHORSERVIDOR", "patente": "Comandante"}}
        stats = {"incendios": 124}
    dados = MockDados()

app = Flask(__name__)
app.secret_key = 'galia_espinho_v2_2026'

def salvar_permanente():
    """Tenta escrever no ficheiro dados.py se o servidor permitir escrita"""
    try:
        caminho = os.path.join(os.path.dirname(__file__), 'dados.py')
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(f"users = {repr(dados.users)}\n")
            f.write(f"stats = {repr(dados.stats)}\n")
        importlib.reload(dados)
    except Exception as e:
        print(f"Erro ao salvar: {e}")

# --- DESIGN DO SITE ---
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="pt-pt">
<head>
    <meta charset="UTF-8">
    <title>BV Espinho | Gália RP</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <script>
        document.addEventListener('contextmenu', e => e.preventDefault());
        document.onkeydown = function(e) {
            if(event.keyCode == 123 || (e.ctrlKey && e.shiftKey && (e.keyCode == 73 || e.keyCode == 74 || e.keyCode == 67)) || (e.ctrlKey && e.keyCode == 85)) return false;
        }
    </script>
</head>
<body class="bg-zinc-950 text-zinc-100 font-sans flex h-screen overflow-hidden">

    <aside class="w-64 bg-zinc-900 border-r border-zinc-800 flex flex-col">
        <div class="p-6 border-b border-zinc-800 text-center">
            <h1 class="text-xl font-black italic uppercase">BV <span class="text-red-600">Espinho</span></h1>
        </div>
        
        <nav class="flex-1 p-4 space-y-2 mt-4 text-[11px] font-black uppercase tracking-widest">
            <a href="{{ url_for('home') }}" class="block p-3 rounded hover:bg-red-700 transition">Comunicados</a>
            <a href="{{ url_for('fogos') }}" class="block p-3 rounded hover:bg-red-700 transition">Fogos</a>
            <a href="{{ url_for('equipa') }}" class="block p-3 rounded hover:bg-red-700 transition">Equipa</a>
            <a href="{{ url_for('candidatura') }}" class="block p-3 rounded bg-zinc-800 text-yellow-500 hover:bg-yellow-500 hover:text-black transition">Candidatura</a>
        </nav>

        <div class="p-4 border-t border-zinc-800">
            {% if session.get('user_email') %}
                <div class="text-[10px] mb-2"><b>{{ session['user_nome'] }}</b></div>
                <div class="flex gap-2">
                    <a href="{{ url_for('dashboard') }}" class="bg-zinc-800 p-2 rounded flex-1 text-center hover:bg-white hover:text-black transition"><i class="fas fa-cog"></i></a>
                    <a href="{{ url_for('logout') }}" class="bg-zinc-800 p-2 rounded flex-1 text-center hover:bg-red-600"><i class="fas fa-power-off"></i></a>
                </div>
            {% else %}
                <a href="{{ url_for('login_page') }}" class="block w-full bg-red-700 text-center py-2 rounded text-[10px] font-black uppercase">Login</a>
            {% endif %}
        </div>
    </aside>

    <main class="flex-1 overflow-y-auto p-12">
        {% block content %}{% endblock %}
    </main>

</body>
</html>
"""

@app.route('/')
def home():
    content = """
    <h1 class="text-6xl font-black italic uppercase mb-6">Portal de <span class="text-red-600">Notícias</span></h1>
    <div class="bg-zinc-900 p-8 rounded-lg border-l-8 border-red-600">
        <h3 class="text-2xl font-bold">Quartel de Espinho</h3>
        <p class="text-zinc-400 mt-4 leading-relaxed">Bem-vindo ao novo sistema operacional. Todas as abas estão agora ligadas corretamente.</p>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=content)

@app.route('/fogos')
def fogos():
    content = f"""
    <div class="text-center py-10">
        <h1 class="text-5xl font-black uppercase mb-12 italic">Fogo <span class="text-orange-500">Controlado</span></h1>
        <div class="inline-block bg-zinc-900 p-16 rounded-full border-4 border-orange-600 shadow-2xl">
            <span class="text-8xl font-black text-orange-500">{dados.stats['incendios']}</span>
        </div>
        <p class="mt-6 text-zinc-500 font-bold uppercase tracking-widest">Ocorrências Finalizadas</p>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=content)

@app.route('/equipa')
def equipa():
    rows = ""
    for email, info in dados.users.items():
        rows += f"<tr class='border-b border-zinc-800'><td class='p-4 font-black uppercase'>{info['nome']}</td><td class='p-4 text-red-500 font-mono text-xs'>{info['patente']}</td><td class='p-4 text-right text-green-500 font-black text-[10px]'>ATIVO</td></tr>"
    content = f"""
    <h1 class="text-4xl font-black uppercase italic mb-8">Quadro <span class="text-red-600">Operacional</span></h1>
    <div class="bg-zinc-900 rounded-lg overflow-hidden border border-zinc-800">
        <table class="w-full text-left">
            <thead class="bg-black text-zinc-500 text-[10px] uppercase font-bold"><tr><th class="p-4">Nome</th><th class="p-4">Patente</th><th class="p-4 text-right">Status</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=content)

@app.route('/candidatura')
def candidatura():
    content = """
    <h1 class="text-4xl font-black uppercase italic mb-6">Recrutamento <span class="text-red-600">2026</span></h1>
    <div class="h-[70vh] bg-white rounded-lg overflow-hidden">
        <iframe src="https://forms.gle/XNtCDyekkgjiJaVE9" class="w-full h-full border-none"></iframe>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=content)

@app.route('/login_page')
def login_page():
    content = """
    <div class="flex justify-center items-center py-20">
        <form action="/login" method="POST" class="bg-zinc-900 p-10 rounded border border-zinc-800 w-full max-w-sm">
            <h2 class="text-xl font-black uppercase text-center text-red-500 mb-8 border-b border-red-700 pb-2 italic">Acesso Restrito</h2>
            <input type="email" name="email" placeholder="E-mail" class="w-full bg-black p-4 mb-4 rounded border border-zinc-800 outline-none text-sm focus:border-red-600 transition" required>
            <input type="password" name="senha" placeholder="Senha" class="w-full bg-black p-4 mb-6 rounded border border-zinc-800 outline-none text-sm focus:border-red-600 transition" required>
            <button class="w-full bg-red-700 py-4 rounded font-black uppercase hover:bg-red-800 transition">Entrar</button>
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
    <div class="bg-zinc-900 p-10 rounded-lg border-t-8 border-red-700">
        <h2 class="text-2xl font-black uppercase mb-8 italic">Painel Interno: {session['user_nome']}</h2>
        <form action="/update_pass" method="POST" class="max-w-xs space-y-4">
            <p class="text-[10px] font-black uppercase text-red-500">Mudar Senha (Grava no ficheiro)</p>
            <input type="password" name="nova_senha" placeholder="Nova Senha" class="w-full bg-black p-4 rounded border border-zinc-800 text-sm">
            <button class="bg-red-700 px-8 py-3 rounded text-xs font-black uppercase hover:bg-red-800 transition">Salvar Alterações</button>
        </form>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=content)

@app.route('/update_pass', methods=['POST'])
def update_pass():
    if 'user_email' in session:
        dados.users[session['user_email']]['senha'] = request.form.get('nova_senha')
        salvar_permanente()
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
