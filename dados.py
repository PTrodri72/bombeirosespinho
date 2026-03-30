DB = {
'users': {
'[igor.rodrigues@comandobombeiros.galiarp.pt](mailto:igor.rodrigues@comandobombeiros.galiarp.pt)': {
'nome': 'Igor Rodrigues',
'senha': 'ef797c8118f02dfb649b5d7f8d0b83ff3cf3e5b0e4c3f1c8f6dbf08d31e7fef5',
'role': 'Comandante'
},
'[joao.silva@comandobombeiros.galiarp.pt](mailto:joao.silva@comandobombeiros.galiarp.pt)': {
'nome': 'João Silva',
'senha': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
'role': 'Bombeiro'
}
},
'ocorrencias': [
{'descricao': 'Incêndio Florestal na Serra', 'autor': 'Igor Rodrigues'},
{'descricao': 'Socorro INEM Rua Central', 'autor': 'João Silva'}
],
'viaturas': [
{'id': 'VUCI-01', 'tipo': 'Combate Urbano', 'estado': 'Operacional'},
{'id': 'ABSC-01', 'tipo': 'INEM', 'estado': 'Operacional'},
{'id': 'VCOT-01', 'tipo': 'Comando', 'estado': 'Operacional'}
]
}

import hashlib

def hash_password(password):
return hashlib.sha256(password.encode()).hexdigest()

def check_password(stored_password, provided_password):
return stored_password == hashlib.sha256(provided_password.encode()).hexdigest()

def gerar_dashboard_html():
html = '<h1 class="text-3xl text-red-600 mb-4">Dashboard MDT</h1>'
html += '<div class="grid md:grid-cols-2 gap-6">'
html += '<div class="glass p-6 rounded-xl border border-zinc-800">'
html += '<h2 class="text-xl font-bold text-white mb-2">Ocorrências Ativas</h2>'
for o in DB['ocorrencias']:
html += f'<p class="text-white">{o["descricao"]} - {o["autor"]}</p>'
html += '</div>'
html += '<div class="glass p-6 rounded-xl border border-zinc-800">'
html += '<h2 class="text-xl font-bold text-white mb-2">Viaturas</h2>'
for v in DB['viaturas']:
status_color = 'green' if v['estado'] == 'Operacional' else 'orange'
html += f'<p class="text-white">{v["id"]} - {v["tipo"]} - <span class="text-{status_color}-500">{v["estado"]}</span></p>'
html += '</div></div>'
return html
