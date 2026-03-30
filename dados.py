import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(stored_password, provided_password):
    return stored_password == hashlib.sha256(provided_password.encode()).hexdigest()

DB = {
    'users': {
        'igor.rodrigues@comandobombeiros.galiarp.pt': {
            'nome': 'Igor Rodrigues',
            'senha': hash_password('GRPGALAIMELHORSERVIDOR'),
            'role': 'Comandante'
        }
    },
    'ocorrencias': [
        {'descricao': 'Incêndio Florestal na Serra', 'autor': 'Igor Rodrigues'},
        {'descricao': 'Socorro a ferido em acidente rodoviário', 'autor': 'Igor Rodrigues'}
    ],
    'viaturas': [
        {'id': 'VUCI-01', 'tipo': 'Combate Urbano', 'estado': 'Operacional'},
        {'id': 'ABSC-01', 'tipo': 'Socorro (INEM)', 'estado': 'Operacional'},
        {'id': 'VCOT-01', 'tipo': 'Comando', 'estado': 'Operacional'},
        {'id': 'VFGC-02', 'tipo': 'Combate Florestal', 'estado': 'Oficina'}
    ]
}

def gerar_dashboard_html():
    html = "<h1 class='text-3xl font-black text-white mb-6'>Dashboard MDT</h1>"

    html += "<h2 class='text-2xl text-red-600 mb-2'>Ocorrências Ativas</h2><div class='grid md:grid-cols-2 gap-4 mb-6'>"
    for o in DB['ocorrencias']:
        html += f"<div class='glass p-4 rounded-xl border border-red-600'><p class='text-white font-bold'>{o['descricao']}</p><p class='text-zinc-400 text-sm'>Autor: {o['autor']}</p></div>"
    html += "</div>"

    html += "<h2 class='text-2xl text-red-600 mb-2'>Viaturas</h2><div class='grid md:grid-cols-2 lg:grid-cols-4 gap-4'>"
    for v in DB['viaturas']:
        estado_color = 'bg-green-500' if v['estado'] == 'Operacional' else 'bg-orange-500'
        estado_text = 'Operacional' if v['estado'] == 'Operacional' else 'Em Manutenção'
        html += f"<div class='glass p-4 rounded-xl border border-zinc-800'><h3 class='text-white font-bold'>{v['id']}</h3><p class='text-zinc-400 text-sm'>{v['tipo']}</p><div class='flex items-center gap-2 mt-2'><div class='w-2 h-2 rounded-full {estado_color}'></div><span class='text-white text-sm'>{estado_text}</span></div></div>"
    html += "</div>"

    return html
