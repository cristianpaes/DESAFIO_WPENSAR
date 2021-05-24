from django import forms
from estoque.models import Produto, Compra_Produto

class ProdutosForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome_produto']
        labels = {'nome_produto': 'Produto'}


class ComprasForm(forms.ModelForm):
    class Meta:
        model = Compra_Produto
        fields = ['produto', 'quantidade', 'valor_produto']
        labels = {'produto': 'Produto', 'quantidade': 'Quantidade', 'valor_produto': 'Valor'}
