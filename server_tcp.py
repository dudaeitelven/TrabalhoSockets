import sys
import socket
import json

def mainServer() :
	ip = 'localhost'
	porta = int(sys.argv[1])

	soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	soquete.bind((ip,porta))
	soquete.listen(10)

	while True:
		soquete2, end = soquete.accept()
		mensagemRecebida = soquete2.recv(1024)

		jsonRecebido = json.loads(mensagemRecebida.decode())

		if (jsonRecebido["metodo"] == "Criar"):
			mensagemEnviar = CriarLivro(jsonRecebido["livro"])
		elif (jsonRecebido["metodo"] == "ConsultarAutor"):
			mensagemEnviar = ConsultarLivroAutor(jsonRecebido["livro"])
		elif (jsonRecebido["metodo"] == "ConsultarTitulo"):
			mensagemEnviar = ConsultarLivroTitulo(jsonRecebido["livro"])
		elif (jsonRecebido["metodo"] == "ConsultarAnoEdicao"):
			mensagemEnviar = ConsultarLivroPorAnoEdicao(jsonRecebido["livro"])
		elif (jsonRecebido["metodo"] == "Remover"):
			mensagemEnviar = RemoverLivro(jsonRecebido["livro"])
		elif (jsonRecebido["metodo"] == "Alterar"):
			mensagemEnviar = AlterarLivro(jsonRecebido["livro"])

		soquete2.send(mensagemEnviar.encode())
		soquete2.close()

	soquete.close()

def ConsultarBaseLivros():
	try:
		with open("bancoDados.json", "r") as json_file:
			dados = json.load(json_file)
	except:
		dados = json.loads('[]')
	return dados

def PersistirBaseLivros(baseLivros):
	with open("bancoDados.json", "w") as json_file:
		json.dump(baseLivros, json_file, indent=4)

def CriarLivro(jsonRecebido):
	livro_novo = jsonRecebido
	livro = jsonRecebido
	baseLivros = ConsultarBaseLivros()

	ultimoCodigo = 0
	
	for livro in baseLivros:
		if (livro["codigo"] > ultimoCodigo):
			ultimoCodigo = livro["codigo"]

	livro_novo["codigo"] = ultimoCodigo + 1

	baseLivros.append(livro_novo)
	PersistirBaseLivros(baseLivros)

	mensagemEnviar = ("Livro inserido!")
	return mensagemEnviar

def ConsultarLivroAutor(jsonRecebido):
	livro_consulta = jsonRecebido
	baseLivros = ConsultarBaseLivros()
	livrosRetorno = json.loads('[]')

	for livro in baseLivros:
		if (livro["autor"] == livro_consulta["autor"]):
			livrosRetorno.append(livro)

	return (json.dumps(livrosRetorno))

def ConsultarLivroTitulo(jsonRecebido):
	livro_consulta = jsonRecebido
	baseLivros = ConsultarBaseLivros()
	livrosRetorno = json.loads('[]')

	for livro in baseLivros:
		if (livro["titulo"] == livro_consulta["titulo"]):
			livrosRetorno.append(livro)

	return (json.dumps(livrosRetorno))

def ConsultarLivroPorAnoEdicao(jsonRecebido):
	livro_consulta = jsonRecebido
	baseLivros = ConsultarBaseLivros()
	livrosRetorno = json.loads('[]')

	for livro in baseLivros:
		if (livro["edicao"] == livro_consulta["edicao"] and livro["anoPublicacao"] == livro_consulta["anoPublicacao"]):
			livrosRetorno.append(livro)

	return (json.dumps(livrosRetorno))

def RemoverLivro(jsonRecebido):
	livro_exclusao = jsonRecebido
	baseLivros = ConsultarBaseLivros()

	for livro in baseLivros:
		if (livro["titulo"] == livro_exclusao["titulo"]):
			baseLivros.remove(livro)

	PersistirBaseLivros(baseLivros)

	mensagemEnviar = ("Livro removido!")
	return mensagemEnviar

def AlterarLivro(jsonRecebido):
	livro_alteracao = jsonRecebido
	baseLivros = ConsultarBaseLivros()

	for livro in baseLivros:
		if (livro["codigo"] == livro_alteracao["codigo"]):
			baseLivros.remove(livro)
			baseLivros.append(livro_alteracao)

	PersistirBaseLivros(baseLivros)
	
	mensagemEnviar = ("Livro alterado!")
	return mensagemEnviar

mainServer()