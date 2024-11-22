from django.utils.http import urlencode
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.test import TestCase
from .models import Colecao, Livro, Autor, Categoria
from .serializers import LivroSerializer, ColecaoSerializer, CategoriaSerializer, AutorSerializer
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


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "user01", "user01@example.com", "user01password")
        self.categoria = Categoria.objects.create(nome="Ficção")
        self.autor = Autor.objects.create(nome="Autor Teste")
        self.livro = Livro.objects.create(
            titulo="Livro de Teste",
            autor=self.autor,
            categoria=self.categoria,
            publicado_em="2023-11-22"
        )
        self.colecao = Colecao.objects.create(
            nome="Coleção de Teste",
            descricao="Descrição da Coleção",
            colecionador=self.user
        )
        self.colecao.livros.set([self.livro])

    def test_categoria_str(self):
        self.assertEqual(str(self.categoria), "Ficção")

    def test_autor_str(self):
        self.assertEqual(str(self.autor), "Autor Teste")

    def test_livro_str(self):
        self.assertEqual(str(self.livro), "Livro de Teste")

    def test_colecao_str(self):
        self.assertEqual(str(self.colecao), "Coleção de Teste - user01")

    def test_criar_colecao_com_livros(self):
        colecao = Colecao.objects.create(
            nome="Nova Coleção",
            descricao="Uma nova coleção de livros",
            colecionador=self.user
        )
        colecao.livros.set([self.livro])
        self.assertEqual(colecao.livros.count(), 1)

    def test_relacionamento_livro_autor_categoria(self):
        livro = Livro.objects.get(titulo="Livro de Teste")
        self.assertEqual(livro.autor, self.autor)
        self.assertEqual(livro.categoria, self.categoria)


class SerializerTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "user01", "user01@example.com", "user01password")
        self.categoria = Categoria.objects.create(nome="Ficção")
        self.autor = Autor.objects.create(nome="Autor Teste")
        self.livro = Livro.objects.create(
            titulo="Livro de Teste",
            autor=self.autor,
            categoria=self.categoria,
            publicado_em="2023-11-22"
        )
        self.colecao = Colecao.objects.create(
            nome="Coleção de Teste",
            descricao="Descrição da Coleção",
            colecionador=self.user
        )
        self.colecao.livros.set([self.livro])

    def test_categoria_serializer_create(self):
        data = {"nome": "Ficção Científica"}
        serializer = CategoriaSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        categoria = serializer.save()
        self.assertEqual(categoria.nome, "Ficção Científica")

    def test_categoria_serializer_update(self):
        categoria = Categoria.objects.create(nome="Aventura")
        data = {"nome": "Aventura Atualizada"}
        serializer = CategoriaSerializer(categoria, data=data)
        self.assertTrue(serializer.is_valid())
        updated_categoria = serializer.save()
        self.assertEqual(updated_categoria.nome, "Aventura Atualizada")

    def test_autor_serializer_create(self):
        data = {"nome": "Autor Teste 2"}
        serializer = AutorSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        autor = serializer.save()
        self.assertEqual(autor.nome, "Autor Teste 2")

    def test_livro_serializer_create(self):
        data = {
            "titulo": "Novo Livro",
            "autor": self.autor.id,
            "categoria": self.categoria.id,
            "publicado_em": "2023-11-22"
        }
        serializer = LivroSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        livro = serializer.save()
        self.assertEqual(livro.titulo, "Novo Livro")
        self.assertEqual(livro.autor, self.autor)
        self.assertEqual(livro.categoria, self.categoria)

    def test_colecao_serializer_create(self):
        data = {
            "nome": "Coleção Nova",
            "descricao": "Descrição da nova coleção",
            "livros": [self.livro.id],
            "colecionador": self.user.id
        }
        serializer = ColecaoSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        colecao = serializer.save()
        self.assertEqual(colecao.nome, "Coleção Nova")
        self.assertEqual(colecao.livros.count(), 1)
        self.assertEqual(colecao.colecionador, self.user)

    def test_colecao_serializer_update(self):
        colecao = Colecao.objects.create(
            nome="Coleção Antiga",
            descricao="Descrição da coleção antiga",
            colecionador=self.user
        )
        colecao.livros.set([self.livro])
        data = {
            "nome": "Coleção Atualizada",
            "descricao": "Descrição atualizada",
            "livros": [self.livro.id]
        }
        serializer = ColecaoSerializer(colecao, data=data)
        self.assertTrue(serializer.is_valid())
        updated_colecao = serializer.save()
        self.assertEqual(updated_colecao.nome, "Coleção Atualizada")
        self.assertEqual(updated_colecao.livros.count(), 1)

    def test_colecao_serializer_invalid_data(self):
        data = {
            "descricao": "Coleção sem nome",
            "livros": [self.livro.id]
        }
        serializer = ColecaoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("nome", serializer.errors)

    def test_livro_serializer_invalid_data(self):
        data = {
            "titulo": "Livro Inválido",
            "autor": 999,
            "categoria": self.categoria.id,
            "publicado_em": "2023-11-22"
        }
        serializer = LivroSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("autor", serializer.errors)

    def test_colecao_serializer_livros_detalhes(self):
        data = {
            "nome": "Coleção com Detalhes",
            "livros": [self.livro.id],
            "colecionador": self.user.id
        }
        serializer = ColecaoSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        colecao = serializer.save()
        self.assertIn("livros_detalhes", serializer.data)
        self.assertEqual(len(serializer.data["livros_detalhes"]), 1)
        self.assertEqual(
            serializer.data["livros_detalhes"][0]["titulo"], self.livro.titulo)
