# Exercício Prático: Biblioteca Django v3

## Desafio
Desenvolver um sistema de gerenciamento de biblioteca que permite a administração de livros, autores, categorias e coleções. Neste exercício, foi utilizado o Django ORM para realizar operações de CRUD, criação de serializers e class-based views.

## Objetivos
- Reimplementar as views utilizando class-based views.
- Adicionar recursos de paginação de resultados, ordenação e busca de termos.
- Criar um repositório público no GitHub para a submissão do exercício.
- Implementar um modelo de coleção de livros associado a um usuário (colecionador).
- Adicionar autenticação baseada em Token e permissões para garantir que apenas o colecionador
possa gerenciar sua coleção.
- Documentar a API com drf-spectacular.
- Desenvolver testes automatizados para a funcionalidade de coleções.

## Documentação da API

#### Api Root

```http
  GET /
```

#### Documentação Open API

```http
  GET /api/docs/
```

## Instalação

1. Clone o projeto:

```bash
  git clone https://github.com/mancinilucas/drf-pratica-orm.git
```

2. Entre no diretório do projeto clonado:
```
  cd drf-pratica-orm
```

3. Crie um ambiente virtual:

```
  python -m venv venv
```

4. Ative o ambiente virtual:

- Windows:
```
  venv\Scripts\Activate.ps1
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

8. Credenciais para testes:
```
  usuario: user01
  senha: user01password
  token: d883b8c125f2d5389601246618180ee4a79678de
```



## Tecnologias
- Python 3.12.4
- PIP 24.2
- Django 5.1
- Django Rest Framework 3.15.2
- Django Filter 24.3
- Pytest 8.3.3
- DRF Spectacular 0.27.2
- Django CORS Headers 4.6.0