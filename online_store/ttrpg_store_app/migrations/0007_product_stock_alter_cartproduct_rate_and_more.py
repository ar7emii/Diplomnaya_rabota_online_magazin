# Generated by Django 4.2.4 on 2023-09-26 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ttrpg_store_app', '0006_alter_product_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.CharField(blank=True, choices=[('В наличии', 'В наличии'), ('Нет в наличии', 'Нет в наличии'), ('Под заказ', 'Под заказ')], help_text='Выберите наличие товара', max_length=50, null=True, verbose_name='Наличие'),
        ),
        migrations.AlterField(
            model_name='cartproduct',
            name='rate',
            field=models.PositiveIntegerField(help_text='Введите стоимость товара', verbose_name='Стоимость товара'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, help_text='Выберите изображение товара', null=True, upload_to='static', verbose_name='Изображение товара'),
        ),
        migrations.AlterField(
            model_name='product',
            name='selling_price',
            field=models.PositiveIntegerField(help_text='Введите цену товара со скидкой', verbose_name='Цена товара со скидкой'),
        ),
    ]
