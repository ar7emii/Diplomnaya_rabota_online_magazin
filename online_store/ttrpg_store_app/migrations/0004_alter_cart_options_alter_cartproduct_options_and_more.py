# Generated by Django 4.2.4 on 2023-09-24 11:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ttrpg_store_app', '0003_alter_product_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'ordering': ['created_at'], 'verbose_name': 'Корзина', 'verbose_name_plural': 'Корзины'},
        ),
        migrations.AlterModelOptions(
            name='cartproduct',
            options={'ordering': ['cart'], 'verbose_name': 'Товар в корзине', 'verbose_name_plural': 'Товары в корзине'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['title'], 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['full_name'], 'verbose_name': 'Клиент', 'verbose_name_plural': 'Клиенты'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['cart'], 'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['title'], 'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
        migrations.AlterField(
            model_name='cart',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='Введите дату создания корзины', verbose_name='Дата создания корзины'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='customer',
            field=models.ForeignKey(blank=True, help_text='Выберите клиента', null=True, on_delete=django.db.models.deletion.SET_NULL, to='ttrpg_store_app.customer', verbose_name='Клиент'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='total',
            field=models.PositiveIntegerField(default=0, help_text='Введите итоговую сумму', verbose_name='Итоговая сумма'),
        ),
        migrations.AlterField(
            model_name='cartproduct',
            name='cart',
            field=models.ForeignKey(help_text='Выберите корзину', on_delete=django.db.models.deletion.CASCADE, to='ttrpg_store_app.cart', verbose_name='Корзина'),
        ),
        migrations.AlterField(
            model_name='cartproduct',
            name='product',
            field=models.ForeignKey(help_text='Выберите товар', on_delete=django.db.models.deletion.CASCADE, to='ttrpg_store_app.product', verbose_name='Товар в корзине'),
        ),
        migrations.AlterField(
            model_name='cartproduct',
            name='quantity',
            field=models.PositiveIntegerField(help_text='Введите количество товаров', verbose_name='Количество товаров'),
        ),
        migrations.AlterField(
            model_name='cartproduct',
            name='rate',
            field=models.PositiveIntegerField(help_text='Введите стоимость товара', verbose_name='Стоимость твоара'),
        ),
        migrations.AlterField(
            model_name='cartproduct',
            name='subtotal',
            field=models.PositiveIntegerField(help_text='Введите итоговую стоимость товаров', verbose_name='Итоговая стоимость товаров'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(help_text='Введите метку URL для категории', unique=True, verbose_name='Метка URL для категории'),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(help_text='Введите название категории', max_length=200, verbose_name='Название категории'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(blank=True, help_text='Введите адрес пользователя', max_length=200, null=True, verbose_name='Адрес пользователя'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='full_name',
            field=models.CharField(help_text='Введите полное имя пользователя', max_length=200, verbose_name='Полное имя пользователя'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='joined_on',
            field=models.DateTimeField(auto_now_add=True, help_text='Введите дату регистрации пользователя', verbose_name='Дата регистрации пользователя'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(help_text='Введите юзернейм пользователя', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Юзернейм пользователя'),
        ),
        migrations.AlterField(
            model_name='order',
            name='cart',
            field=models.OneToOneField(help_text='Выберите корзину', on_delete=django.db.models.deletion.CASCADE, to='ttrpg_store_app.cart', verbose_name='Корзина'),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='Введите дату создания заказа', verbose_name='Дата заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='discount',
            field=models.PositiveIntegerField(help_text='Введите сумму скидки', verbose_name='Сумма скидки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(blank=True, help_text='Введите электронную почту', max_length=254, null=True, verbose_name='Электронная почта'),
        ),
        migrations.AlterField(
            model_name='order',
            name='mobile',
            field=models.CharField(help_text='Введите мобильный телефон', max_length=15, verbose_name='Мобильный телефон'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('Заказ принят', 'Заказ принят'), ('Заказ в обработке', 'Заказ в обработке'), ('Заказ в пути', 'Заказ в пути'), ('Заказ выполнен', 'Заказ выполнен'), ('Заказ отменен', 'Заказ отменен')], help_text='Выберите статус заказа', max_length=50, verbose_name='Статус заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='ordered_by',
            field=models.CharField(help_text='Введите имя заказчика', max_length=200, verbose_name='Имя заказчика'),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=models.CharField(help_text='Введите адрес доставки', max_length=200, verbose_name='Адрес доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='subtotal',
            field=models.PositiveIntegerField(help_text='Введите итоговую стоимость', verbose_name='Итоговая стоимость'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.PositiveIntegerField(help_text='Введите сумму после скидки', verbose_name='Сумма после скидки'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(help_text='Выберите категорию', on_delete=django.db.models.deletion.CASCADE, to='ttrpg_store_app.category', verbose_name='Название категории'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(help_text='Введите описание товара', verbose_name='Описание товара'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, help_text='Выберите изображение твоара', null=True, upload_to='static', verbose_name='Изображение товара'),
        ),
        migrations.AlterField(
            model_name='product',
            name='marked_price',
            field=models.PositiveIntegerField(help_text='Введите цену товара без скидки', verbose_name='Цена товара без скидки'),
        ),
        migrations.AlterField(
            model_name='product',
            name='return_policy',
            field=models.CharField(blank=True, help_text='Введите политику возврата товара (если есть)', max_length=300, null=True, verbose_name='Политика возврата'),
        ),
        migrations.AlterField(
            model_name='product',
            name='selling_price',
            field=models.PositiveIntegerField(help_text='Введите цену товара со скидкой', verbose_name='Цена товар асо скидкой'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(help_text='Введите метку URL для товара', unique=True, verbose_name='Метка URL для товара'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(help_text='Введите название товара', max_length=200, verbose_name='Название товара'),
        ),
        migrations.AlterField(
            model_name='product',
            name='view_count',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество просмотров'),
        ),
        migrations.AlterField(
            model_name='product',
            name='warranty',
            field=models.CharField(blank=True, help_text='Введите срок гарантии (если есть)', max_length=300, null=True, verbose_name='Гарантия'),
        ),
    ]
