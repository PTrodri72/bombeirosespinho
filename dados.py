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
    'ocorrencias': [],
    'viaturas': [
        {'id': 'VUCI-01', 'tipo': 'Combate Urbano', 'estado': 'Operacional'},
        {'id': 'ABSC-01', 'tipo': 'Socorro (INEM)', 'estado': 'Operacional'},
        {'id': 'VCOT-01', 'tipo': 'Comando', 'estado': 'Operacional'},
        {'id': 'VFGC-02', 'tipo': 'Combate Florestal', 'estado': 'Oficina'}
    ]
}
