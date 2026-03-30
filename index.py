from flask import Flask, render_template_string, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'galia_rp_secret_key_2026'

# --- BANCO DE DADOS SIMULADO ---
# Hierarquia Oficial conforme imagem
HIERARQUIA = [
    "Comandante", "2º Comandante", "Adjunto do Comando", "Oficial Bombeiro", 
    "Chefe", "Sub Chefe", "Bombeiro de 1ª", "Bombeiro de 2ª", "Bombeiro de 3ª", "Estagiario"
]

users = {
    "igor.rodrigues@comandobombeiros.galiarp.pt": {
        "nome": "Igor Rodrigues",
        "senha": "GRPGALAIMELHORSERVIDOR",
        "patente": "Comandante",
        "status": "Ativo"
    },
    "bombeiro.teste@galiarp.pt": {
        "nome": "Recruta Exemplo",
        "senha": "123",
        "patente": "Estagiario",
        "status": "Ativo"
    }
}

stats = {"incendios": 124}
avisos = []

# --- TEMPLATE HTML (SISTEMA COMPLETO) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-pt">
<head>
    <meta charset="UTF-8">
    <title>BV Espinho - Portal Operacional</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        .sidebar-item:hover { background: rgba(220, 38, 38, 0.1); }
        .active-tab { border-left: 4px solid #dc2626; background: rgba(220, 38, 38, 0.05); }
    </style>
</head>
<body class="bg-zinc-900 text-zinc-100 font-sans flex h-screen overflow-hidden">

    {% if not session.get('user_email') %}
    <div class="fixed inset-0 bg-black flex items-center justify-center p-6 z-[100]">
        <div class="bg-zinc-900 border border-zinc-800 p-8 rounded-xl w-full max-w-md shadow-2xl">
            <div class="text-center mb-8">
                <i class="fas fa-fire-extinguisher text-red-600 text-5xl mb-4"></i>
                <h1 class="text-2xl font-black uppercase italic tracking-widest">Portal de Comando</h1>
                <p class="text-zinc-500 text-xs mt-2 uppercase">BV Espinho - Gália Roleplay</p>
            </div>
            <form action="/login" method="POST" class="space-y-4">
                <input type="email" name="email" placeholder="E-mail Institucional" class="w-full p-4 bg-zinc-950 border border-zinc-800 rounded focus:border-red-600 outline-none transition" required>
                <input type="password" name="senha" placeholder="Palavra-passe" class="w-full p-4 bg-zinc-950 border border-zinc-800 rounded focus:border-red-600 outline-none transition" required>
                <button type="submit" class="w-full bg-red-700 hover:bg-red-800 py-4 rounded font-bold uppercase tracking-widest transition shadow-lg shadow-red-900/20">Aceder ao Terminal</button>
            </form>
            {% with messages = get_flashed_messages() %}{% if messages %}
                <p class="text-red-500 text-center mt-4 text-xs font-bold uppercase">{{ messages[0] }}</p>
            {% endif %}{% endwith %}
        </div>
    </div>
    {% else %}

    <aside class="w-72 bg-zinc-950 border-r border-zinc-800 flex flex-col">
        <div class="p-8 border-b border-zinc-900">
            <h2 class="font-black uppercase text-xl italic tracking-tighter">BV <span class="text-red-600">Espinho</span></h2>
        </div>
        <nav class="flex-1 p-4 space-y-2 mt-4">
            <a href="/" class="sidebar-item flex items-center p-3 rounded text-sm font-bold uppercase tracking-wider transition"><i class="fas fa-home w-8 text-red-600"></i> Comunicados</a>
            <a href="/equipa" class="sidebar-item flex items-center p-3 rounded text-sm font-bold uppercase tracking-wider transition"><i class="fas fa-users w-8 text-red-600"></i> Quadro Ativo</a>
            <a href="/recrutamento" class="sidebar-item flex items-center p-3 rounded text-sm font-bold uppercase tracking-wider transition"><i class="fas fa-file-contract w-8 text-red-600"></i> Recrutamento</a>
        </nav>
        
        <div class="p-6 bg-zinc-900/50 border-t border-zinc-800">
            <p class="text-[10px] text-zinc-500 uppercase font-black mb-1">Operacional Conectado</p>
            <p class="text-sm font-bold text-white">{{ session['user_nome'] }}</p>
            <p class="text-[10px] text-red-500 uppercase font-bold mb-4">{{ session['user_patente'] }}</p>
            
            <form action="/update_pass" method="POST" class="space-y-2">
                <input type="password" name="nova_senha" placeholder="Mudar Senha" class="w-full p-2 bg-zinc-950 border border-zinc-800 text-[10px] rounded focus:border-red-600 outline-none">
                <button class="w-full bg-zinc-800 text-[10px] py-1 rounded font-bold hover:bg-red-700 transition uppercase">Atualizar Senha</button>
            </form>
            <a href="/logout" class="block text-center text-[10px] text-zinc-600 hover:text-white mt-4 uppercase font-bold tracking-widest">Sair do Sistema</a>
        </div>
    </aside>

    <main class="flex-1 overflow-y-auto p-12 bg-zinc-900">
        
        {% if page == 'home' %}
        <div class="max-w-4xl">
            <div class="flex justify-between items-end mb-10">
                <h1 class="text-5xl font-black uppercase italic tracking-tighter">Comunicados <span class="text-red-700">Oficiais</span></h1>
                <div class="text-right">
                    <p class="text-4xl font-black text-white">{{ stats['incendios'] }}</p>
                    <p class="text-[10px] text-zinc-500 font-black uppercase tracking-widest">Fogos Dominados</p>
                </div>
            </div>

            {% if session['user_patente'] in ['Comandante', '2º Comandante', 'Adjunto do Comando'] %}
            <div class="bg-red-950/20 border border-red-900/40 p-6 rounded mb-8">
                <h3 class="text-xs font-black uppercase mb-4 text-red-500">Gestão de Comandante</h3>
                <div class="grid grid-cols-2 gap-4">
                    <form action="/update_stats" method="POST" class="flex space-x-2">
                        <input type="number" name="count" class="bg-black p-2 rounded text-xs w-24 border border-zinc-700" placeholder="Incêndios">
                        <button class="bg-red-700 px-4 py-2 rounded text-xs font-bold uppercase">Atualizar</button>
                    </form>
                </div>
            </div>
            {% endif %}

            <div class="space-y-4">
                <div class="bg-zinc-800 p-8 rounded-lg border-l-8 border-red-700 relative overflow-hidden shadow-xl">
                    <i class="fas fa-bullhorn absolute -right-4 -bottom-4 text-8xl text-white/5 rotate-12"></i>
                    <span class="text-red-500 text-[10px] font-black uppercase tracking-widest">Comando BV Espinho - Gália RP</span>
                    <h3 class="text-xl font-bold mt-2">Bem-vindo ao Portal Operacional Igor Rodrigues.</h3>
                    <p class="text-zinc-400 mt-4 font-light leading-relaxed">Mantenha a sua senha protegida. O uso de terminais de comando para fins não autorizados resultará em expulsão imediata do quadro ativo.</p>
                </div>
            </div>
        </div>

        {% elif page == 'equipa' %}
        <div class="max-w-6xl">
            <h1 class="text-5xl font-black uppercase italic tracking-tighter mb-10">Quadro <span class="text-red-700">Ativo</span></h1>
            
            <div class="bg-zinc-950 rounded-lg shadow-2xl overflow-hidden border border-zinc-800">
                <table class="w-full text-left">
                    <thead class="bg-zinc-900 text-zinc-500 text-[10px] font-black uppercase tracking-widest">
                        <tr>
                            <th class="p-5">Agente</th>
                            <th class="p-5">Patente</th>
                            <th class="p-5">Status</th>
                            {% if session['user_patente'] in ['Comandante', '2º Comandante', 'Adjunto do Comando'] %}
                            <th class="p-5">Ações de Comando</th>
                            {% endif %}
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-zinc-900 text-sm">
                        {% for email, data in users.items() %}
                        <tr class="hover:bg-zinc-900/50 transition">
                            <td class="p-5 font-bold">{{ data['nome'] }}<br><span class="text-[10px] text-zinc-600 font-normal">{{ email }}</span></td>
                            <td class="p-5 font-mono text-red-500 uppercase text-xs">{{ data['patente'] }}</td>
                            <td class="p-5"><span class="bg-green-900/30 text-green-500 text-[10px] px-2 py-1 rounded font-bold uppercase">{{ data['status'] }}</span></td>
                            {% if session['user_patente'] in ['Comandante', '2º Comandante', 'Adjunto do Comando'] %}
                            <td class="p-5 flex space-x-2">
                                {% if email != session['user_email'] %}
                                <a href="/admin/promover/{{ email }}" class="text-green-500 hover:scale-110 transition"><i class="fas fa-chevron-up"></i></a>
                                <a href="/admin/rebaixar/{{ email }}" class="text-orange-500 hover:scale-110 transition"><i class="fas fa-chevron-down"></i></a>
                                <a href="/admin/eliminar/{{ email }}" class="text-red-500 hover:scale-110 transition"><i class="fas fa-trash"></i></a>
                                {% else %}
                                <span class="text-zinc-700 italic text-[10px]">Autogestão bloqueada</span>
                                {% endif %}
                            </td>
                            {% endif %}
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>

            <div class="mt-12 bg-red-950/10 p-6 rounded border border-red-900/20">
                <h3 class="text-red-600 font-black uppercase italic text-lg mb-4"><i class="fas fa-gavel mr-2"></i> Advertências e Sanções</h3>
                <div class="text-sm text-zinc-400">Nenhum processo disciplinar ativo no sistema.</div>
            </div>
        </div>

        {% elif page == 'recrutamento' %}
        <div class="h-full flex flex-col">
            <h1 class="text-4xl font-black uppercase italic mb-6">Processo de <span class="text-red-700">Recrutamento</span></h1>
            <div class="flex-1 bg-white rounded shadow-2xl overflow-hidden">
                <iframe src="https://forms.gle/XNtCDyekkgjiJaVE9" class="w-full h-full border-none"></iframe>
            </div>
        </div>
        {% endif %}

    </main>
    {% endif %}

</body>
</html>
"""

# --- ROTAS DO SERVIDOR ---

@app.route('/')
def index():
    if 'user_email' not in session:
        return render_template_string(HTML_TEMPLATE)
    return render_template_string(HTML_TEMPLATE, page='home', stats=stats, users=users)

@app.route('/equipa')
def equipa():
    if 'user_email' not in session: return redirect('/')
    return render_template_string(HTML_TEMPLATE, page='equipa', users=users)

@app.route('/recrutamento')
def recrutamento():
    if 'user_email' not in session: return redirect('/')
    return render_template_string(HTML_TEMPLATE, page='recrutamento')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')
    
    if email in users and users[email]['senha'] == senha:
        session['user_email'] = email
        session['user_nome'] = users[email]['nome']
        session['user_patente'] = users[email]['patente']
        return redirect('/')
    
    flash('Credenciais Inválidas')
    return redirect('/')

@app.route('/update_pass', methods=['POST'])
def update_pass():
    nova = request.form.get('nova_senha')
    if nova and 'user_email' in session:
        users[session['user_email']]['senha'] = nova
        flash('Senha atualizada!')
    return redirect('/')

@app.route('/update_stats', methods=['POST'])
def update_stats():
    if session.get('user_patente') in ['Comandante', '2º Comandante', 'Adjunto do Comando']:
        stats['incendios'] = request.form.get('count')
    return redirect('/')

@app.route('/admin/promover/<email>')
def promover(email):
    if session.get('user_patente') in ['Comandante', '2º Comandante', 'Adjunto do Comando'] and email != session['user_email']:
        p_atual = users[email]['patente']
        idx = HIERARQUIA.index(p_atual)
        if idx > 0:
            users[email]['patente'] = HIERARQUIA[idx-1]
    return redirect('/equipa')

@app.route('/admin/rebaixar/<email>')
def rebaixar(email):
    if session.get('user_patente') in ['Comandante', '2º Comandante', 'Adjunto do Comando'] and email != session['user_email']:
        p_atual = users[email]['patente']
        idx = HIERARQUIA.index(p_atual)
        if idx < len(HIERARQUIA) - 1:
            users[email]['patente'] = HIERARQUIA[idx+1]
    return redirect('/equipa')

@app.route('/admin/eliminar/<email>')
def eliminar(email):
    if session.get('user_patente') in ['Comandante', '2º Comandante', 'Adjunto do Comando'] and email != session['user_email']:
        del users[email]
    return redirect('/equipa')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)