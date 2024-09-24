from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text="Введите юзернейм пользователя",
                                verbose_name="Юзернейм пользователя")
    full_name = models.CharField(max_length=200, help_text="Введите полное имя пользователя",
                                 verbose_name="Полное имя пользователя")
    address = models.CharField(max_length=200, null=True, blank=True, help_text="Введите адрес пользователя",
                               verbose_name="Адрес пользователя")
    joined_on = models.DateTimeField(auto_now_add=True, help_text="Введите дату регистрации пользователя",
                                     verbose_name="Дата регистрации пользователя")
    objects = models.Model

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Клиент"  # Название в единственном числе
        verbose_name_plural = "Клиенты"  # Название в единственном числе
        ordering = ["full_name"]  # Сортировка по полю (если с "-" то в обратном порядке)


class Category(models.Model):
    title = models.CharField(max_length=200, help_text="Введите название категории", verbose_name="Название категории")
    slug = models.SlugField(unique=True, help_text="Введите метку URL для категории",
                            verbose_name="Метка URL для категории")
    objects = models.Model

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"  # Название в единственном числе
        verbose_name_plural = "Категории"  # Название в единственном числе
        ordering = ["title"]  # Сортировка по полю (если с "-" то в обратном порядке)


STOCK_STATUS = (
    ("В наличии", "В наличии"),
    ("Нет в наличии", "Нет в наличии"),
    ("Под заказ", "Под заказ"),
)


class Product(models.Model):
    title = models.CharField(max_length=60, help_text="Введите название товара", verbose_name="Название товара")
    slug = models.SlugField(unique=True, help_text="Введите метку URL для товара", verbose_name="Метка URL для товара")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text="Выберите категорию",
                                 verbose_name="Название категории")
    image = models.ImageField(null=True, blank=True, upload_to="static", help_text="Выберите изображение товара",
                              verbose_name="Изображение товара")
    marked_price = models.PositiveIntegerField(null=True, help_text="Введите цену товара без скидки",
                                               verbose_name="Цена товара без скидки")
    selling_price = models.PositiveIntegerField(help_text="Введите цену товара со скидкой",
                                                verbose_name="Цена товара со скидкой")
    description = models.TextField(help_text="Введите описание товара", verbose_name="Описание товара")
    stock = models.CharField(max_length=50, choices=STOCK_STATUS, null=True, blank=True,
                             help_text="Выберите наличие товара", verbose_name="Наличие")
    warranty = models.CharField(max_length=300, null=True, blank=True, help_text="Введите срок гарантии (если есть)",
                                verbose_name="Гарантия")
    return_policy = models.CharField(max_length=300, null=True, blank=True,
                                     help_text="Введите политику возврата товара (если есть)",
                                     verbose_name="Политика возврата")
    view_count = models.PositiveIntegerField(default=0, help_text="", verbose_name="Количество просмотров")
    objects = models.Model

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Товар"  # Название в единственном числе
        verbose_name_plural = "Товары"  # Название в единственном числе
        ordering = ["title"]  # Сортировка по полю (если с "-" то в обратном порядке)


class Cart(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True, help_text="Выберите клиента", verbose_name="Клиент")
    total = models.PositiveIntegerField(default=0, help_text="Введите итоговую сумму", verbose_name="Итоговая сумма")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Введите дату создания корзины",
                                      verbose_name="Дата создания корзины")
    objects = models.Model

    def __str__(self):
        return "Cart: " + str(self.pk)

    class Meta:
        verbose_name = "Корзина"  # Название в единственном числе
        verbose_name_plural = "Корзины"  # Название в единственном числе
        ordering = ["created_at"]  # Сортировка по полю (если с "-" то в обратном порядке)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, help_text="Выберите корзину", verbose_name="Корзина")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, help_text="Выберите товар",
                                verbose_name="Товар в корзине")
    rate = models.PositiveIntegerField(help_text="Введите стоимость товара", verbose_name="Стоимость товара")
    quantity = models.PositiveIntegerField(help_text="Введите количество товаров", verbose_name="Количество товаров")
    subtotal = models.PositiveIntegerField(help_text="Введите итоговую стоимость товаров",
                                           verbose_name="Итоговая стоимость товаров")
    objects = models.Model

    def __str__(self):
        return "Корзина " + str(self.cart.pk) + " --- Товар: " + str(self.product)

    class Meta:
        verbose_name = "Товар в корзине"  # Название в единственном числе
        verbose_name_plural = "Товары в корзине"  # Название в единственном числе
        ordering = ["cart"]  # Сортировка по полю (если с "-" то в обратном порядке)


ORDER_STATUS = (
    ("Заказ принят", "Заказ принят"),
    ("Заказ в обработке", "Заказ в обработке"),
    ("Заказ в пути", "Заказ в пути"),
    ("Заказ выполнен", "Заказ выполнен"),
    ("Заказ отменен", "Заказ отменен"),
)


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, help_text="Выберите корзину", verbose_name="Корзина")
    ordered_by = models.CharField(max_length=200, help_text="Введите имя заказчика", verbose_name="Имя заказчика")
    shipping_address = models.CharField(max_length=200, help_text="Введите адрес доставки",
                                        verbose_name="Адрес доставки")
    mobile = models.CharField(max_length=15, help_text="Введите мобильный телефон", verbose_name="Мобильный телефон")
    email = models.EmailField(null=True, blank=True, help_text="Введите электронную почту",
                              verbose_name="Электронная почта")
    subtotal = models.PositiveIntegerField(help_text="Введите итоговую стоимость", verbose_name="Итоговая стоимость")
    discount = models.PositiveIntegerField(help_text="Введите сумму скидки", verbose_name="Сумма скидки")
    total = models.PositiveIntegerField(help_text="Введите сумму после скидки", verbose_name="Сумма после скидки")
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS, help_text="Выберите статус заказа",
                                    verbose_name="Статус заказа")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Введите дату создания заказа",
                                      verbose_name="Дата заказа")
    objects = models.Model

    def __str__(self):
        return "Order: " + str(self.pk)

    class Meta:
        verbose_name = "Заказ"  # Название в единственном числе
        verbose_name_plural = "Заказы"  # Название в единственном числе
        ordering = ["cart"]  # Сортировка по полю (если с "-" то в обратном порядке)
