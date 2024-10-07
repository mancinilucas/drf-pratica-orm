from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

urlpatterns = [
    path('livros/', views.LivroList.as_view(), name='livro-list'),
    path('livros/<int:pk>/', views.LivroDetail.as_view(), name='livro-detail'),
    path('autores/', views.AutorList.as_view(), name='autor-list'),
    path('autores/<int:pk>', views.AutorDetail.as_view(), name='autor-detail'),
    path('categorias/', views.CategoriaList.as_view(), name='categoria-list'),
    path('categorias/<int:pk>', views.CategoriaDetail.as_view(),
         name='categoria-detail'),
    path("", include(router.urls)),
    path("", views.ApiRoot.as_view(), name=views.ApiRoot.name),
]
