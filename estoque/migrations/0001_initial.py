# Generated by Django 3.2.3 on 2021-05-22 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_produto', models.CharField(max_length=100, unique=True, verbose_name='nome')),
            ],
            options={
                'db_table': 'produto',
            },
        ),
        migrations.CreateModel(
            name='Compra_Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField(null=True, verbose_name='Quantidade')),
                ('valor_produto', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Preço')),
                ('valor_medio', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preço Médio')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estoque.produto', verbose_name='Produto')),
            ],
            options={
                'db_table': 'compra',
            },
        ),
    ]