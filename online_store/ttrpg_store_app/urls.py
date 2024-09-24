from django.urls import path, reverse_lazy
from ttrpg_store_app import views
from ttrpg_store_app.views import SearchView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


app_name = 'ttrpg_store_app'
urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('contact-us/', views.contact, name='contact'),
    path('all-products/', views.all_products, name='all_products'),
    path('product/<slug:slug>/', views.product_details, name='product_details'),
    path('add-to-cart-<int:prod_id>/', views.add_to_cart, name='add_to_cart'),
    path('my_cart/', views.my_cart, name='my_cart'),
    path('my_cart_management/<int:cart_prod_id>/', views.my_cart_management, name='my_cart_management'),
    path('my_cart_delete/', views.my_cart_delete, name='my_cart_delete'),
    path('checkout/', views.checkout, name='checkout'),
    path('customer_registration/', views.customer_registration, name='customer_registration'),
    path('logout/', views.customer_logout, name='logout'),
    path('login/', views.customer_login, name='login'),
    path('password-reset/', PasswordResetView.as_view(
        template_name='users/password_reset.html', email_template_name='users/reset_email.html',
        success_url=reverse_lazy('ttrpg_store_app:password_reset_done')), name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url=reverse_lazy('ttrpg_store_app:password_reset_complete')), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html',), name='password_reset_complete'),
    path('search/', SearchView.as_view(), name='search'),

]
