# Generated by Django 4.2.4 on 2023-08-13 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ttrpg_store_app', '0002_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='static'),
        ),
    ]