# render_tempalte serve para chamar um arquivo html
from flask import Flask, render_template, request, redirect, session, flash, url_for


# criando classe
class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = str(nome)
        self.categoria = categoria
        self.console = console


# instanciando a classe Jogo e passando o nome, categoria e console
jogo1 = Jogo('Tetris', 'Puzzle', 'Aari')
jogo2 = Jogo('God of War', 'Rack in Slash', 'PS2')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'PS2')

# colocando os jogs em uma lista
listaJogos = [jogo1, jogo2, jogo3]


class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha


usuario1 = Usuario("Thulio", "Abufir", "alohomora")
usuario2 = Usuario("Camila Ferreira", "Mila", "paozinho")
usuario3 = Usuario("Guilherme Louro", "Cake", "python_eh_vida")

usuarios = {usuario1.nickname: usuario1,
            usuario2.nickname: usuario2,
            usuario3.nickname: usuario3}

usuarios_nome = {usuario1.nome: usuario1,
                 usuario2.nome: usuario2,
                 usuario3.nome: usuario3}

# name faz referencia ao proprio arquivo e garante que vai rodar a aplicação
app = Flask(__name__)
# adicionando camada de criptografia no site
app.secret_key = 'alura'


# rota padrão responsável por retornar a lista de jogos já cadastrados
@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=listaJogos)


# rota responsável por chamar o formulário para cadastrar novos jogos
# se não tiver nenhum usuario logado na sessão, redireciona para a pagina de login para ser efetuar o login,
# e assim que o login for realizado, redireciona para a pagina com o formulario para cadastrar o novo jogo
@app.route('/novo')
def novo():
    # se não tiver nenhum usuário logado na sessão, ou se não tiver um usuario logado, redireciona para a rota login
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        # passando dentro do url_for a função que instancia a rota login, redirecionando para a pagina de /novo
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')


# rota responsável por puxar as informações do novo.html e cadastrar um novo jogo
# capturando o nome, categoria e console da pessoa que digitou no formulário, adicionando na lista de jogos
# e redireciona para pagina index para listar os jogos.
@app.route('/criar', methods=['POST', ])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogo(nome, categoria, console)
    listaJogos.append(jogo)

    return redirect(url_for('index'))


# Rota de login que retorna o formulário para digitar as credenciais e fazer o login
@app.route('/login')
def login():
    # capturando a informação da queryString
    proxima = request.args.get('proxima')
    if proxima == None:
        proxima = "/"
    # enviando as informações da proxima pagina pro html
    return render_template('login.html', proxima=proxima)


# session é um atributo flask que guarda as informações do usuário nos coockies do navegador
# rota responsável por realizar a autenticação do login
# Se o usuário que a pessoa digitou estiver na lista de usuarios cadastrada no sistema,
# verifica se a senha que a pessoa digitou é a mesma senha do usuário cadastrado no sistema,
# cria uma sessão, imprime na tela o sucesso da operação e redireciona para proxima pagina.
@app.route('/autenticar', methods=['POST'], )
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form["senha"] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    elif request.form['usuario'] in usuarios_nome:
        usuario = usuarios_nome[request.form['usuario']]
        if request.form["senha"] == usuario.senha:
            session['usuario_logado'] = usuario.nome
            flash(usuario.nome + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado.')
        # passando dentro do url_for a função que instancia a rota login, que é o /login
        return redirect(url_for('login'))


# Rota responsável por finalizar a sessão do usuário
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    # passando dentro do url_for a função que instancia a rota index, que é o barra /
    return redirect(url_for('index'))


# faz rodar a aplicação
app.run(debug=True)
