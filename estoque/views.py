from collections import namedtuple
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from estoque.models import Produto, Compra_Produto
from django.db import connection
from estoque.form import ProdutosForm, ComprasForm
from django.contrib.auth import authenticate,login, logout


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0].lower() for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

# COMEÇA A CRIAÇÃO DA ATENTICAÇÃO
def login_user(reuest):
    return render(reuest,'login.html')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('pass')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuário ou senha inválida")
    return redirect('/login')

def logout_sistema(request):
    logout(request)
    return redirect('/')


# COMEÇA AS VIEWS REALICIONADA A PRODUTOS
@login_required(login_url='/login/')
def lista_produtos(request):
    produto = Produto.objects.all()
    dados_produtos = {'produto': produto}
    return render(request,'produto.html', dados_produtos)


@login_required(login_url='/login/')
def cadastra_produto(request):
    form = ProdutosForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('produtos')
    return render(request, 'cadastra_produto.html', {'form': form})


@login_required(login_url='/login/')
def deleta_produto(request, id_produto):
    Produto.objects.filter(id=id_produto).delete()
    return redirect('/')



# COMEÇA AS VIEWS REALICIONADA A COMPRA DE PRODUTOS
@login_required(login_url='/login/')
def lista_compras(request):
    compras = Compra_Produto.objects.all()
    dados_compra = {'produtos': compras}
    return render(request,'compra.html', dados_compra)


@login_required(login_url='/login/')
def deleta_compra(request, id_compra):
    Compra_Produto.objects.filter(id=id_compra).delete()
    return redirect('/compras')


@login_required(login_url='/login/')
def compras_produtos(request):
    form = ComprasForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('compras')
    return render(request, 'cadastra_compras.html', {'form': form})


@login_required(login_url='/login/')
def relatorio_compras(request):
    sql = '''
            SELECT 
            P.ID,
            P.NOME_PRODUTO,
            COALESCE(TMP.QUANTIDADE, 0) QUANTIDADE,
            COALESCE(TMP.TOTAL, 0) TOTAL,
            COALESCE(TMP.PRECO_MEDIO, 0) PRECO_MEDIO
        FROM PRODUTO P LEFT JOIN (
            SELECT 
                C.PRODUTO_ID,
                SUM(C.QUANTIDADE) QUANTIDADE,
                SUM(C.QUANTIDADE * C.VALOR_PRODUTO) TOTAL,
                (SUM(C.QUANTIDADE * C.VALOR_PRODUTO) / CAST(SUM(C.QUANTIDADE) AS FLOAT)) PRECO_MEDIO
            FROM COMPRA C
            GROUP BY C.PRODUTO_ID
        ) TMP ON P.ID = TMP.PRODUTO_ID;
    '''
    with connection.cursor() as cursor:
        cursor.execute(sql)
        produtos = namedtuplefetchall(cursor)

    print(produtos)

    return render(request, 'relatorio_compras.html', {'produtos': produtos})

