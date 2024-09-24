from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from .models import *
from django.http import HttpResponseRedirect
from .forms import CheckOutForm, CustomerRegistrationForm, CustomerLoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    # Здесь происходит получение списка продуктов из модели Product,
    # сортировка по количеству просмотров в убывающем порядке и выборка первых 12 продуктов.
    # Полученный список продуктов сохраняется в переменной product_list.
    product_list = Product.objects.all().order_by('-view_count')[:12]
    context = {'product_list': product_list}
    # Возвращается ответ с использованием шаблона 'home.html' и передачей контекста.
    return render(request, 'home.html', context=context)


def all_products(request):
    # Здесь происходит получение значения параметра 'category' из запроса,
    # который был отправлен пользователем.
    category = request.GET.get('category')
    context = {}
    if category == 'all-products':
        # Если значение параметра 'category' равно 'all-products',
        # происходит получение всех категорий из модели Category.
        # Полученный список категорий сохраняется в переменной 'categories'.
        categories = Category.objects.all()
        context = {'categories': categories}
    elif category == 'card-games':
        # Если значение параметра 'category' равно 'card-games',
        # происходит получение категории с идентификатором 1 из модели Category.
        # Полученная категория сохраняется в переменной 'categories'.
        categories = Category.objects.filter(pk=1)
        context = {'categories': categories}
    elif category == 'role-playing-games':
        # Если значение параметра 'category' равно 'role-playing-games',
        # происходит получение категории с идентификатором 2 из модели Category.
        # Полученная категория сохраняется в переменной 'categories'.
        categories = Category.objects.filter(pk=2)
        context = {'categories': categories}
    elif category == 'rulebooks':
        # Если значение параметра 'category' равно 'rulebooks',
        # происходит получение категории с идентификатором 3 из модели Category.
        # Полученная категория сохраняется в переменной 'categories'.
        categories = Category.objects.filter(pk=3)
        context = {'categories': categories}
    # Возвращается ответ с использованием шаблона 'all-products.html' и передачей контекста.
    return render(request, 'all-products.html', context=context)


class SearchView(TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        # Здесь происходит получение данных контекста для отображения страницы поиска.
        # Сначала вызывается метод get_context_data() суперкласса, чтобы получить базовый контекст.
        context = super().get_context_data(**kwargs)
        print(context)
        # Затем получается значение параметра 'keyword' из запроса, который был отправлен пользователем.
        keyword = self.request.GET.get("keyword")
        # Происходит поиск продуктов, у которых заголовок или описание содержат заданное ключевое слово.
        # Результаты поиска сохраняются в переменной 'results'.
        results = Product.objects.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword))
        context["results"] = results
        # Возвращается обновленный контекст.
        return context


def product_details(request, slug):
    # Здесь происходит получение продукта по заданному 'slug' из модели Product.
    # Если продукт не найден, возвращается страница ошибки 404.
    product = get_object_or_404(Product, slug=slug)
    # Увеличивается счетчик просмотров продукта на 1 и сохраняется обновленное значение.
    product.view_count += 1
    product.save()
    # Определяется правильное склонение слова 'просмотр' в зависимости от количества просмотров.
    if product.view_count % 10 == 1 and product.view_count % 100 != 11:
        prosmotr_correct_word = 'просмотр'
    elif 2 <= product.view_count % 10 <= 4 and (product.view_count % 100 < 10 or product.view_count % 100 >= 20):
        prosmotr_correct_word = 'просмотрa'
    else:
        prosmotr_correct_word = 'просмотров'
    # Создается контекст, который содержит информацию о продукте и правильном склонении слова 'просмотр'.
    context = {'product': product, 'prosmotr_correct_word': prosmotr_correct_word}
    # Возвращается ответ с использованием шаблона 'product-details.html' и передачей контекста.
    return render(request, 'product-details.html', context=context)


def add_to_cart(request, prod_id):
    if request.method == 'GET':
        product_id = prod_id
        product_obj = Product.objects.get(id=product_id)
        if request.user.is_authenticated:
            if request.user.id == 1:
                cart_id = request.session.get("cart_id")
            else:
                customer = Customer.objects.get(user=request.user.id)
                cart_id = Cart.objects.filter(customer=customer).order_by('id').last().id
        else:
            cart_id = request.session.get("cart_id")

        # Проверка наличия корзины и добавление товара в нее
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(product=product_obj)

            if this_product_in_cart.exists():
                # Если товар уже присутствует в корзине, увеличиваем его количество и сумму подитога
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
            else:
                # Если товара нет в корзине, создаем новую запись для него
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.selling_price,
                    quantity=1, subtotal=product_obj.selling_price)
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
        else:
            # Если корзина не существует, создаем новую корзину и добавляем товар в нее
            cart_obj = Cart.objects.create(total=0)
            request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(
                cart=cart_obj, product=product_obj, rate=product_obj.selling_price,
                quantity=1, subtotal=product_obj.selling_price)
            cart_obj.total += product_obj.selling_price
            cart_obj.save()

        # Привязка покупателя к корзине (если аутентифицирован) и сохранение изменений
        if request.user.is_authenticated:
            customer = Customer.objects.get(user=request.user.id)
            cart_obj.customer = customer
            cart_obj.save()
        else:
            request.session['cart_id'] = cart_obj.id

    # Передача контекста и рендер страницы
    context = {'prod_id': prod_id}
    return render(request, 'add_to_cart.html', context=context)


def my_cart(request):
    product_list = Product.objects.all()
    if request.user.is_authenticated:
        if request.user.id == 1:
            cart_id = request.session.get("cart_id")
            if cart_id:
                cart = Cart.objects.get(id=cart_id)
            else:
                cart = None
            context = {'view_my_cart': cart, 'product_list': product_list}
        else:
            # Получение корзины для аутентифицированного покупателя
            customer = Customer.objects.get(user=request.user.id)
            try:
                cart = Cart.objects.filter(customer=customer).order_by('id').last()
                context = {'view_my_cart': cart, 'product_list': product_list}
            except ObjectDoesNotExist:
                cart = None
                context = {'view_my_cart': cart, 'product_list': product_list}
    else:
        # Получение корзины из сессии для неаутентифицированного пользователя
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context = {'view_my_cart': cart, 'product_list': product_list}

    # Передача контекста и рендер страницы
    return render(request, 'my_cart.html', context=context)


def my_cart_management(request, cart_prod_id):
    if request.method == 'GET':
        action = request.GET.get("action")
        cart_prod_obj = CartProduct.objects.get(id=cart_prod_id)
        cart = cart_prod_obj.cart
        cart_id = request.session.get('cart_id')

        # Увеличение количества товара в корзине
        if action == 'inc':
            cart_prod_obj.quantity += 1
            cart_prod_obj.subtotal += cart_prod_obj.rate
            cart_prod_obj.save()
            cart.total += cart_prod_obj.rate
            cart.save()

        # Уменьшение количества товара в корзине
        elif action == 'dcr':
            cart_prod_obj.quantity -= 1
            cart_prod_obj.subtotal -= cart_prod_obj.rate
            cart_prod_obj.save()
            cart.total -= cart_prod_obj.rate
            cart.save()
            # Если количество товара становится равным 0, удаляем его из корзины
            if cart_prod_obj.quantity == 0:
                cart_prod_obj.delete()

        # Удаление товара из корзины
        elif action == 'rmv':
            cart.total -= cart_prod_obj.subtotal
            cart.save()
            cart_prod_obj.delete()

        else:
            pass

    # Перенаправление на страницу "my_cart/"
    return HttpResponseRedirect("/my_cart/")


def my_cart_delete(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            if request.user.id == 1:
                cart_id = request.session.get('cart_id')
                cart = Cart.objects.get(id=cart_id)
                cart.cartproduct_set.all().delete()
                cart.total = 0
                cart.save()
            else:
                # Удаление всех товаров из корзины для аутентифицированного покупателя
                customer = Customer.objects.get(user=request.user.id)
                cart_obj = Cart.objects.filter(customer=customer).order_by('id').last()
                cart_obj.cartproduct_set.all().delete()
                cart_obj.total = 0
                cart_obj.save()
        else:
            # Удаление всех товаров из корзины для неаутентифицированного пользователя
            cart_id = request.session.get('cart_id')
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()

    # Перенаправление на страницу "my_cart/"
    return HttpResponseRedirect("/my_cart/")


def checkout(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            # Если пользователь аутентифицирован, получаем информацию о нем
            customer = Customer.objects.get(user=request.user.id)
            cart_id = Cart.objects.filter(customer=customer).order_by('id').last().id
        else:
            # Если пользователь не аутентифицирован, получаем информацию о корзине из сессии
            cart_id = request.session.get("cart_id")

        if cart_id:
            # Если есть идентификатор корзины, получаем информацию о корзине
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None

        # Создаем форму оформления заказа и передаем ее в контекст
        obj_checkout_form = CheckOutForm()
        context = {'view_my_cart': cart, 'checkout_form': obj_checkout_form}
        return render(request, 'checkout.html', context=context)

    elif request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.id == 1:
                cart_id = request.session.get("cart_id")
            else:
                customer = Customer.objects.get(user=request.user.id)
                cart_id = Cart.objects.filter(customer=customer).order_by('id').last().id
        else:
            cart_id = request.session.get("cart_id")

        if cart_id:
            # Если есть идентификатор корзины, получаем информацию о корзине
            cart = Cart.objects.get(id=cart_id)
            obj_checkout_form = CheckOutForm(request.POST)

            if obj_checkout_form.is_valid():
                # Если форма оформления заказа действительна, получаем данные из формы
                ordered_by = obj_checkout_form.cleaned_data.get("ordered_by")
                shipping_address = obj_checkout_form.cleaned_data.get("shipping_address")
                mobile = obj_checkout_form.cleaned_data.get("mobile")
                email = obj_checkout_form.cleaned_data.get("email")

                # Создаем объект заказа и заполняем его данными из формы и корзины
                order = obj_checkout_form.save(commit=False)
                order.ordered_by = ordered_by
                order.shipping_address = shipping_address
                order.mobile = mobile
                order.email = email
                order.cart = cart
                order.subtotal = cart.total
                order.discount = 0
                order.total = cart.total
                order.order_status = "Заказ принят"
                order.save()

                if request.user.is_authenticated:
                    if request.user.id == 1:
                        del request.session['cart_id']
                    else:
                        # Если пользователь аутентифицирован, но его идентификатор не равен 1, создаем новую корзину
                        # для пользователя
                        customer = Customer.objects.get(user=request.user.id)
                        new_cart = Cart.objects.create(customer=customer)
                        new_cart.total = 0
                        new_cart.save()
                else:
                    # Если пользователь не аутентифицирован, удаляем идентификатор корзины из сессии
                    del request.session['cart_id']

                context = {}
                return render(request, 'checkout_success.html', context=context)
            else:
                print('1 else')
                context = {'cart': cart, 'checkout_form': obj_checkout_form}
                return render(request, 'home.html', context=context)
        else:
            print('2 else')
            return HttpResponseRedirect("/")


def customer_registration(request):
    if request.method == 'POST':
        customer_registration_form = CustomerRegistrationForm(request.POST)
        if customer_registration_form.is_valid():
            # Если форма регистрации клиента действительна, получаем данные из формы
            username = customer_registration_form.cleaned_data.get("username")
            password = customer_registration_form.cleaned_data.get("password")
            email = customer_registration_form.cleaned_data.get("email")

            if User.objects.filter(username=username).exists():
                # Проверяем, существует ли пользователь с таким именем пользователя
                customer_registration_form.add_error('username', "Такое имя пользователя уже существует.")
            else:
                # Если пользователь с таким именем пользователя не существует, создаем нового пользователя,
                # связываем его с объектом клиента и сохраняем данные клиента
                user = User.objects.create_user(username, email, password)
                customer = customer_registration_form.save(commit=False)
                customer.user = user
                customer.save()

                # Аутентифицируем пользователя и создаем новую корзину для нового пользователя
                login(request, user)
                new_cart_for_new_user = Cart.objects.create(customer=customer)
                new_cart_for_new_user.total = 0
                new_cart_for_new_user.save()

                return redirect("ttrpg_store_app:home")
    else:
        customer_registration_form = CustomerRegistrationForm()

    # Создаем контекст с формой регистрации клиента и передаем его в шаблон
    context = {'customer_registration_form': customer_registration_form}
    return render(request, 'customer_registration.html', context=context)


def customer_logout(request):
    # Выход пользователя из системы
    logout(request)
    return redirect("ttrpg_store_app:home")


def customer_login(request):
    if request.method == 'POST':
        customer_login_form = CustomerLoginForm(request.POST)
        if customer_login_form.is_valid():
            # Если метод запроса POST и форма входа пользователя действительна, получаем данные из формы
            username = customer_login_form.cleaned_data.get("username")
            password = customer_login_form.cleaned_data.get("password")

            # Аутентификация пользователя
            user = authenticate(username=username, password=password)

            if user is not None and user.customer:
                # Если пользователь существует и является клиентом, аутентифицируем пользователя и перенаправляем на
                # домашнюю страницу
                login(request, user)
                return redirect("ttrpg_store_app:home")
            else:
                # Если пользователь не существует или не является клиентом, отображаем ошибку входа
                context = {'customer_login_form': CustomerLoginForm, 'error': 'Данные введены неверно'}
                return render(request, 'customer_login.html', context)
    else:
        customer_login_form = CustomerLoginForm()

    # Создаем контекст с формой входа пользователя и передаем его в шаблон
    context = {'customer_login_form': customer_login_form}
    return render(request, 'customer_login.html', context=context)


def about(request):
    # Отображение страницы "О нас"
    context = {}
    return render(request, 'about.html', context=context)


def contact(request):
    # Отображение страницы "Контакты"
    context = {}
    return render(request, 'contact-us.html', context=context)
