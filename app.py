from flask import Flask, render_template_string, request, redirect, session, url_for
import os

app = Flask(__name__)
app.secret_key = 'galia_espinho_2026_safe'

# --- DADOS DE SEGURANÇA (Caso o dados.py falhe, o site usa estes) ---
users_db = {
    "igor.rodrigues@comandobombeiros.galiarp.pt": {
        "nome": "Igor Rodrigues",
        "senha": "GRPGALAIMELHORSERVIDOR",
        "patente": "Comandante"
    }
}
stats_db = {"incendios": 124, "socorros": 315, "operacionais": 24}
viaturas_db = [
    {"id": "VUCI-01", "tipo": "Combate Urbano", "estado": "Operacional"},
    {"id": "ABSC-01", "tipo": "Socorro", "estado": "Operacional"},
    {"id": "VCOT-01", "tipo": "Comando", "estado": "Operacional"}
]

# Tentar carregar do ficheiro externo, se falhar, mantém os de cima
try:
    import dados
    users_db = dados.users
    stats_db = dados.stats
    viaturas_db = getattr(dados, 'viaturas', viaturas_db)
except Exception:
    pass

# --- LAYOUT HTML COMPLETO ---
LAYOUT = """
<!DOCTYPE html>
<html lang="pt-pt">
<head>
    <meta charset="UTF-8">
    <title>BV Espinho | Gália RP</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-zinc-950 text-zinc-300 flex h-screen overflow-hidden">
    <aside class="w-64 bg-zinc-900 border-r border-zinc-800 flex flex-col p-6">
        <h1 class="text-xl font-black text-white italic mb-10 text-center">BV <span class="text-red-600">ESPINHO</span></h1>
        <nav class="flex-1 space-y-2 uppercase text-[10px] font-black tracking-widest">
            <a href="/" class="block p-3 rounded hover:bg-red-600 transition">Início</a>
            <a href="/ocorrencias" class="block p-3 rounded hover:bg-red-600 transition">Ocorrências</a>
            <a href="/equipa" class="block p-3 rounded hover:bg-red-600 transition">Equipa</a>
            <a href="/candidatura" class="block p-3 rounded bg-zinc-800 text-yellow-500">Recrutamento</a>
        </nav>
        <div class="mt-auto border-t border-zinc-800 pt-4">
            {% if session.get('user_email') %}
                <p class="text-xs font-bold text-white mb-2">{{ session['user_nome'] }}</p>
                <a href="/logout" class="text-[10px] text-red-500 uppercase font-black">Sair</a>
            {% else %}
                <a href="/login_page" class="block bg-red-700 text-center py-2 rounded text-[10px] font-black uppercase">Login</a>
            {% endif %}
        </div>
    </aside>
    <main class="flex-1 overflow-y-auto p-10">{% block content %}{% endblock %}</main>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(LAYOUT + "{% block content %}<h1 class='text-5xl font-black italic uppercase mb-6'>Mural <span class='text-red-600'>Operacional</span></h1><div class='bg-zinc-900 p-8 rounded-xl border-l-8 border-red-600'><h3 class='text-xl font-bold'>Bem-vindo, Comandante!</h3><p class='mt-4 text-zinc-500'>O sistema está online e pronto para o RP em Espinho.</p></div>{% endblock %}")

@app.route('/ocorrencias')
def ocorrencias():
    return render_template_string(LAYOUT + f"""{{% block content %}}
    <h1 class="text-5xl font-black italic uppercase mb-10">Registo de <span class="text-orange-600">Ocorrências</span></h1>
    <div class="grid grid-cols-2 gap-6">
        <div class="bg-zinc-900 p-10 rounded-2xl text-center border border-orange-600/20">
            <p class="text-7xl font-black text-orange-500">{stats_db['incendios']}</p>
            <p class="text-xs font-bold uppercase text-zinc-500 mt-2">Incêndios Extintos</p>
        </div>
        <div class="bg-zinc-900 p-10 rounded-2xl text-center border border-red-600/20">
            <p class="text-7xl font-black text-red-600">{stats_db['socorros']}</p>
            <p class="text-xs font-bold uppercase text-zinc-500 mt-2">Socorros Efetuados</p>
        </div>
    </div>
    {{% endblock %}}""")

@app.route('/equipa')
def equipa():
    rows = "".join([f"<tr class='border-b border-zinc-800'><td class='p-4 font-bold'>{u['nome']}</td><td class='p-4 text-red-500'>{u['patente']}</td></tr>" for u in users_db.values()])
    return render_template_string(LAYOUT + f"{{% block content %}}<h1 class='text-5xl font-black italic uppercase mb-8'>Quadro <span class='text-red-600'>Ativo</span></h1><table class='w-full bg-zinc-900 rounded-xl overflow-hidden'><thead class='bg-black text-[10px] uppercase font-black text-zinc-500'><tr><th class='p-4 text-left'>Nome</th><th class='p-4 text-left'>Patente</th></tr></thead><tbody>{rows}</tbody></table>{{% endblock %}}")

@app.route('/candidatura')
def candidatura():
    return render_template_string(LAYOUT + "{% block content %}<h1 class='text-5xl font-black italic uppercase mb-8 text-white'>Escola de <span class='text-red-600'>Recrutas</span></h1><div class='h-[70vh] bg-white rounded-2xl overflow-hidden'><iframe src='https://forms.gle/XNtCDyekkgjiJaVE9' class='w-full h-full'></iframe></div>{% endblock %}")

@app.route('/login_page')
def login_page():
    return render_template_string(LAYOUT + "{% block content %}<div class='flex justify-center pt-20'><form action='/login' method='POST' class='bg-zinc-900 p-10 rounded-2xl border border-zinc-800 w-full max-w-sm'><h2 class='text-center text-xl font-black uppercase mb-8'>Login Operacional</h2><input type='email' name='email' placeholder='Email' class='w-full bg-black p-4 mb-4 rounded border border-zinc-800 outline-none text-white' required><input type='password' name='senha' placeholder='Senha' class='w-full bg-black p-4 mb-6 rounded border border-zinc-800 outline-none text-white' required><button class='w-full bg-red-700 py-4 rounded font-black uppercase'>Entrar</button></form></div>{% endblock %}")

@app.route('/login', methods=['POST'])
def login():
    email, senha = request.form.get('email'), request.form.get('senha')
    if email in users_db and users_db[email]['senha'] == senha:
        session.update({'user_email': email, 'user_nome': users_db[email]['nome'], 'user_patente': users_db[email]['patente']})
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# IMPORTANTE: Para o Vercel reconhecer a aplicação
app = app
