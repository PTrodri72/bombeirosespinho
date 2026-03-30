from flask import Flask, request, redirect, session, url_for
from functools import wraps
import os
import hashlib

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key")


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def check_password(stored_password, provided_password):
    return stored_password == hashlib.sha256(provided_password.encode()).hexdigest()


DB = {
    "users": {
        "igor.rodrigues@comandobombeiros.galiarp.pt": {
            "nome": "Igor Rodrigues",
            "senha": hash_password("GRPGALAIMELHORSERVIDOR"),
            "patente": "Comandante",
            "role": "admin"
        }
    },
    "ocorrencias": [],
    "viaturas": [
        {"id": "VUCI-01", "tipo": "Combate Urbano", "estado": "Operacional"},
        {"id": "ABSC-01", "tipo": "INEM", "estado": "Operacional"},
        {"id": "VCOT-01", "tipo": "Comando", "estado": "Operacional"}
    ]
}


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_email" not in session:
            return redirect(url_for("login_page"))
        return f(*args, **kwargs)
    return decorated


@app.route('/')
def home():
    return "BV Espinho RP ONLINE"


@app.route('/login_page')
def login_page():
    return '''
    <form method="POST" action="/login">
        <input name="email" type="email" placeholder="Email" required>
        <input name="senha" type="password" placeholder="Senha" required>
        <button type="submit">Login</button>
    </form>
    '''


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get("email", "").strip().lower()
    senha = request.form.get("senha", "")

    if not email or not senha:
        return redirect(url_for("login_page"))

    user = DB["users"].get(email)

    if user is None:
        return redirect(url_for("login_page"))

    if not check_password(user["senha"], senha):
        return redirect(url_for("login_page"))

    session.clear()
    session["user_email"] = email
    session["user_nome"] = user.get("nome")
    session["user_role"] = user.get("role")

    return redirect(url_for("dashboard"))


@app.route('/dashboard')
@login_required
def dashboard():
    nome = session.get("user_nome", "Utilizador")
    return f"Bem-vindo {nome}"


@app.route('/criar_ocorrencia', methods=['POST'])
@login_required
def criar_ocorrencia():
    descricao = request.form.get("descricao", "").strip()

    if not descricao:
        return redirect(url_for("ver_ocorrencias"))

    DB["ocorrencias"].append({
        "descricao": descricao,
        "autor": session.get("user_nome")
    })

    return redirect(url_for("ver_ocorrencias"))


@app.route('/ocorrencias')
@login_required
def ver_ocorrencias():
    html = "<h1>Ocorrências</h1>"

    for o in DB["ocorrencias"]:
        descricao = o.get("descricao", "")
        autor = o.get("autor", "")
        html += f"<p>{descricao} - {autor}</p>"

    html += '''
    <form method="POST" action="/criar_ocorrencia">
        <input name="descricao" placeholder="Nova ocorrência" required>
        <button type="submit">Criar</button>
    </form>
    '''

    return html


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


app = app
