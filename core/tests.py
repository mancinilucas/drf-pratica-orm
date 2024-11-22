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

    def create_user_without_token(self):
        self.user_without_token = User.objects.create_user(
            "user02", "user02@example.com", "user02password")

    def setUp(self):
        self.create_user_and_set_token_credentials()
        self.create_user_without_token()
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

    def test_create_colecao(self):
        url = reverse('colecao-list')
        data = {
            'nome': 'Nova Coleção',
            'descricao': 'Descrição da nova coleção',
            'livros': [self.livro.id],
            'colecionador': self.user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nome'], 'Nova Coleção')

    def test_create_colecao_without_authentication(self):
        self.client.credentials()  # Remove as credenciais
        url = reverse('colecao-list')
        data = {
            'nome': 'Coleção Não Autenticada',
            'descricao': 'Tentando criar sem autenticação',
            'livros': [self.livro.id],
            'colecionador': self.user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_edit_colecao_as_owning_user(self):
        url = reverse('colecao-detail', args=[self.colecao.id])
        data = {'nome': 'Coleção Editada'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'Coleção Editada')

    def test_edit_colecao_as_non_owner(self):
        self.client.force_authenticate(
            user=self.user_without_token)  # Simula outro usuário
        url = reverse('colecao-detail', args=[self.colecao.id])
        data = {'nome': 'Tentando editar outra coleção'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_colecao_as_owning_user(self):
        url = reverse('colecao-detail', args=[self.colecao.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_colecao_as_non_owner(self):
        self.client.force_authenticate(
            user=self.user_without_token)  # Simula outro usuário
        url = reverse('colecao-detail', args=[self.colecao.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_colecao_as_non_authenticated_user(self):
        self.client.credentials()  # Remove as credenciais
        url = reverse('colecao-list')
        data = {
            'nome': 'Coleção não autenticada',
            'descricao': 'Tentativa de criar sem token',
            'livros': [self.livro.id],
            'colecionador': self.user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
