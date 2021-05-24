
from django.contrib import admin
from django.urls import path
from estoque import views
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/produtos/')),
    path('login/', views.login_user),
    path('login/submit', views.submit_login),
    path('logout/', views.logout_sistema),
    path('produtos/', views.lista_produtos, name='produtos'),
    path('cadastra_produto/', views.cadastra_produto, name='cad_produto'),
    path('deleta/<int:id_produto>', views.deleta_produto),
    path('compras/', views.lista_compras, name='compras'),
    path('delete/<int:id_compra>', views.deleta_compra),
    path('cadastra_compras/', views.compras_produtos, name='compras_produtos'),
    path('relatorio_compras/', views.relatorio_compras, name='relatorio_compras'),
]
