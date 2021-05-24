from django.contrib import admin
from estoque.models import Produto, Compra_Produto

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['id','nome_produto']

@admin.register(Compra_Produto)
class Compra_ProdutoAdmin(admin.ModelAdmin):
    list_display = ['id','produto','quantidade', 'valor_produto']