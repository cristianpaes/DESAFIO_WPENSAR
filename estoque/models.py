from django.db import models
from django.db import connection
from django.db.models.signals import post_save
from django.dispatch import receiver

class Produto(models.Model):
    nome_produto = models.CharField(max_length=100, unique=True, verbose_name='nome')
    valor_medio = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name='Preço Médio')

    class Meta:
        db_table = 'produto'

    def __str__(self):
        return self.nome_produto

class Compra_Produto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name='Produto')
    quantidade = models.IntegerField(blank=False, null=True, verbose_name='Quantidade')
    valor_produto = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=True, verbose_name='Preço')

    class Meta:
        db_table = 'compra'

    def __str__(self):
        return self.produto

@receiver(post_save, sender=Compra_Produto)
def atualiza_media_valor_produto(instance, **kwargs):
    sql = '''
        SELECT 
            C.PRODUTO_ID, 
            (SUM(C.QUANTIDADE * C.VALOR_PRODUTO) / CAST(SUM(C.QUANTIDADE) AS FLOAT)) AVERAGE
        FROM COMPRA C        
        WHERE C.PRODUTO_ID = %s
    '''

    with connection.cursor() as cursor:
        cursor.execute(sql, [instance.produto.pk])
        rs = cursor.fetchone()

    instance.produto.valor_medio = rs[1]
    instance.produto.save()

