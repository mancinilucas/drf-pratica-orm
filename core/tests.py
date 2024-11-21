from django.utils.http import urlencode
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Colecao, Livro, Autor, Categoria
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class ColecaoTests(APITestCase):
    def post_colecao(self, nome, descricao, livros, colecionador):
        url = reverse('colecao-list')
        data = {
            'nome': nome,
            'descricao': descricao,
            'livros': livros,
            'colecionador': colecionador
        }
        response = self.client.post(url, data, format='json')
        return response

    def create_user_and_set_token_credentials(self):
        self.user = User.objects.create_user(
            "user01", "user01@example.com", "user01password")
        token = Token.objects.create(user=self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token {0}'.format(token.key))

    def setUp(self):
        self.create_user_and_set_token_credentials()
        self.categoria = Categoria.objects.create(nome='Categoria Teste')
        self.autor = Autor.objects.create(nome='Autor Teste')
        self.livro = Livro.objects.create(
            titulo='Livro de Teste',
            autor=self.autor,
            categoria=self.categoria,
            publicado_em='2023-11-22'
        )
        self.colecao = Colecao.objects.create(
            nome='Coleção de Teste',
            descricao='Descrição da Coleção',
            colecionador=self.user
        )
        self.colecao.livros.set([self.livro])

    def test_get_colecao(self):
        url = reverse('colecao-list')
        authorized_get_response = self.client.get(url, format='json')
        print(authorized_get_response.data)
        self.assertEqual(status.HTTP_200_OK,
                         authorized_get_response.status_code)
        results = authorized_get_response.data.get('results', [])
        if results:
            self.assertEqual(self.colecao.nome, results[0]['nome'])
