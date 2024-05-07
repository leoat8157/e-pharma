from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('login_view', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('signup_view', views.signup_view, name='signup_view'),
    path('products/', views.product_page, name='product_page'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('carts', views.carts, name='carts'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('place_order/', views.place_order, name='place_order'),
    #path('shipping-address/', views.shipping_address, name='shipping_address'),
    #path('billing-address/', views.billing_address, name='billing_address'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('accountinfo', views.accountinfo, name='accountinfo'),
    path('productpage', views.productpage, name='productpage'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('fetch-shipping-addresses/',views.fetch_shipping_addresses, name='fetch_shipping_addresses'),
    path('save-shipping-address/', views.save_shipping_address, name='save_shipping_address'),
    path('delete-shipping-address/<int:address_id>/', views.delete_shipping_address, name='delete_shipping_address'),


    #path('place_order/', views.place_order, name='place_order'),
    #path('billing_details/', views.billing_details, name='billing_details'),
    #path('shipping_details/', views.shipping_details, name='shipping_details'),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)