# Projeto
Projeto desenvolvido com o intuito de criar um servidor 
flask para armazenar informações de estudantes em um banco 
de dados relacional.

## Como Funciona?

O servidor possui duas rotas:

1. */estudante* com os seguintes métodos: 
	- GET: Lista todos os estudantes presentes no banco; 
	- POST: Insere um novo estudante no banco; 
	- PUT: Atualiza as informações de um estudante; 
	- DELETE: Deleta um estudante; 

2. */estudante/filtro* com os seguintes métodos: 
	- POST: Retorna os estudantes que se encaixam no filtro;


## Rodando o projeto

Assim que realizar o download ou clonar o projeto, 
basta instalar os requirements através do comando:

```bash
$ python -m pip install -r requirements.txt
```

Após a instalação, o servidor pode ser inicializado com o comando:

```bash
$ python app.py
```
Você também pode rodar este servidor utilizando o docker realizando os
seguintes comandos:

```bash
$ docker build -t servidor_flask .
$ docker run -d -p 5000:5000 servidor_flask
```

Desta maneira, o servidor estará rodando em uma imagem do Docker e se comunicando com 
sua máquina através da porta 5000.

**P.S.**: Dentro do diretório *exemplos* estão alguns arquivos json estruturados 
de acordo com o que cada rota espera
