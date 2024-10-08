# Exercício Prático: Biblioteca Django v2

## Desafio
Desenvolver um sistema de gerenciamento de biblioteca que permite a administração de livros, autores e categorias. Neste exercício, foi utilizado o Django ORM para realizar operações de CRUD, criação de serializers e class-based views.

## Objetivos
- Reimplementar as views utilizando class-based views.
- Adicionar recursos de paginação de resultados, ordenação e busca de termos.
- Criar um repositório público no GitHub para a submissão do exercício.

## Documentação da API

#### Api Root

```http
  GET /
```

#### Retorna todos os livros cadastrados

```http
  GET /livros
```

#### Retorna um livro

```http
  GET /livros/${id}
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id`      | `int` | **Obrigatório**. O ID do item que você deseja |


#### Retorna todos os autores cadastrados

```http
  GET /autores
```

#### Retorna um autor

```http
  GET /livros/${id}
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id`      | `int` | **Obrigatório**. O ID do item que você deseja |


#### Retorna todas categorias cadastradas

```http
  GET /categorias
```

#### Retorna uma categoria

```http
  GET /categorias/${id}
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id`      | `int` | **Obrigatório**. O ID do item que você deseja |

## Instalação

1. Clone o projeto:

```bash
  git clone https://github.com/mancinilucas/drf-pratica-orm.git
```

2. Entre no diretório do projeto clonado:
```
  drf-pratica-orm
```

3. Crie um ambiente virtual:

```
  python -m venv venv
```

4. Ative o ambiente virtual:

- Windows:
```
  venv\Scripts\activate
```

- Linux:
```
  source venv/bin/activate
```

5. Instale as dependências listadas no arquivo requirements.txt:
```
  pip install -r requirements.txt
```

6. Se necessário aplique as migrations:
```
  python manage.py migrate
```

7. Para iniciar o servidor local, use o comando:
```
  python manage.py runserver
```


## Tecnologias
- Python 3.12.4
- PIP 24.2
- Django 5.1
- Django Rest Framework 3.15.2
- Django Filter 24.3