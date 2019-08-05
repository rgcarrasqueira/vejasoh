# vejasoh
Projeto Desafio Infoglobo

## Escopo Inicial

O projeto tem como objetivo construir uma aplicação que fizesse leitura de feeds das revistas do grupo Globo, onde foi colocado como exemplo a Revista AutoEsporte http://revistaautoesporte.globo.com/rss/ultimas/feed.xml

## Descrição Técnica da Aplicação

Foi desenvolvida uma aplicação baseado no Framerwork Django 2.2, rodando sobre o Python 3.7, juntamento com o banco de dados padrão de desenvolvimento (SQLLite3)
A aplicação construída permite cadastrar vários feeds a partir de uma interace administrativa, no objeto Stream, onde poderá ser cadastrados várias publicação da Editora Globo para fazer a leitura do JSON a partir dos feeds em XML
Foi implantado o TastyPie 0.14 dentro da aplicação para que esta pudesse também dar acesso via webservice através de requisições REST para fazer o download do arquivo JSON com os dados do Feed.
Foi necessário fazer uma trabalho de limpeza do Feed, pois ao importar e transformá-lo para JSON, ele fica fora do padrão pedido, sendo assim necessário uma séria de rotinas, para serem removidos elementos não necessários conforme o escopo solicitado.
Foi aplicada uma cobertuda de testes unitários no que tange à obtenção do feed e acesso ao Webservice para comprovação do funcionamento, para executar os testes basta baixar a aplicação e executar a seguinte sequência de comandos:

1 - Preparar o seu ambiente virtual com Python3:

```
machine$ virtualenv -p python3 VejaSoh
```

2 - A partir do Diretório com o Virtual Enviromento configurado, baixar o repositório:

```
machine$ git clone https://github.com/rgcarrasqueira/vejasoh.git
```

3 - Instalar os requirements:

```
machine$ pip install -r requirements.txt
```

4 - Execute as migraçao:

```
machine$ python manage.py migrate
```

5 - Para executar os testes:

```
machine$ python manage.py test
```

6 - A aplicação também poderá ser executado em um ambiente Web, chamando pelo browser, mas antes você deverá cadastrar um superusuário para a aplicação

```
machine$ python manage.py createsuperuser
```

7 - Siga os passos pedidos pelo prompt de comando para cadastrar um usuário administrador e na sequência coloque o servidor local para funcionar

```
machine$ python manage.py runserver
```

Para acessar, basta chamar no browser o endereço http://localhost:8000 ou http://127.0.0.1:8000, fazer um cadastro, na sequência efetuar o login e já será levado a um página com todos os feeds e o acesso para o JSON

## WebService

O acesso ao WebService poderá ser utilizado via CURL conforme exemplo abaixo:

```
curl --dump-header -H "Content-Type: application/json" -H "Authorization: Basic user:bla123bla123" http://localhost:8000/api/v1/feeds/stream/1/content/

```
Assumindo que 1 é o ID da Revista em questão e o usuário você criou ao rodar a aplicação pela 1a vez, para ter acesso a todas revistas, utilize:

```
curl --dump-header -H "Content-Type: application/json" -H "Authorization: Basic user:bla123bla123" http://localhost:8000/api/v1/feeds/stream/

```




