from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.db import IntegrityError,transaction
from django.contrib.auth import get_user_model
from .models import Product,Cart,ShippingAddress#,Address,Order,OrderItem
from django.views.generic import DetailView
#from .forms import AddressForm



@require_POST
def delete_shipping_address(request, address_id):
    try:
        # Retrieve the shipping address from the database
        shipping_address = ShippingAddress.objects.get(id=address_id)
        # Delete the shipping address
        shipping_address.delete()
        # Return success response
        return JsonResponse({'success': True})
    except ShippingAddress.DoesNotExist:
        # Return error response if shipping address not found
        return JsonResponse({'success': False, 'error': 'Shipping address not found'})

def save_shipping_address(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')

        # Save shipping address to the database
        shipping_address = ShippingAddress.objects.create(
            name=name,
            contact=contact,
            address=address,
            address2=address2,
            city=city,
            pincode=pincode,
            state=state
        )

        # Return success response
        return JsonResponse({'success': True})

    # Return error response if the request method is not POST
    return JsonResponse({'success': False})

def fetch_shipping_addresses(request):
    addresses = ShippingAddress.objects.all().values()
    return JsonResponse(list(addresses), safe=False)


'''
@login_required
def shipping_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.is_shipping_address = True
            address.save()
            return redirect('billing_address')
    else:
        form = AddressForm()
    return render(request, 'shipping_address.html', {'form': form})

@login_required
def billing_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.is_billing_address = True
            address.save()
            return redirect('place_order')
    else:
        form = AddressForm()
    return render(request, 'billing_address.html', {'form': form})
'''

from django.contrib.auth.decorators import login_required

@login_required
def place_order(request):
    return render(request, 'place_order.html')

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = Cart.objects.get(pk=cart_item_id)
    cart_item.delete()
    return redirect('carts')

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'


@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(pk=product_id)
        price = product.price
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'price': price}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.price = cart_item.product.price * cart_item.quantity
            cart_item.save()
        return JsonResponse({'message': 'Product added to cart'})
    else:
        return JsonResponse({'error': 'Invalid request method'})



def product_page(request):
    products = Product.objects.all()
    return render(request, 'product_page.html', {'products': products})


@login_required
def carts(request):
    cart_items = Cart.objects.all()
    total_amount = sum(item.price for item in cart_items)
    return render(request, 'carts.html', {'cart_items': cart_items, 'total_amount': total_amount})


User = get_user_model()

def signup_view(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = fullname.split()[0] 
            user.last_name = ' '.join(fullname.split()[1:])  
            user.save()

            print("Registration successful")

            return redirect('/')
        
        except IntegrityError:
            return render(request, 'registration.html', {'error_message': 'Username or email already exists. Please choose a different username or email.'})
    else:
        return render(request, 'registration.html')



def signup(request):
    return render(request, 'signup.html')


def login(request):
    return render(request, 'login.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user) 
            
            return redirect('/dashboard')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

    
def register(request):
    return render(request, 'registration.html')
    

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def productpage(request):
    return render(request, 'product_page.html')



@login_required
def logout_view(request):
    logout(request)
    
    return redirect('/')




@login_required
def accountinfo(request):
    user = request.user
    
    fullname = user.get_full_name()
    
    return render(request, 'Account-info.html', {'fullname': fullname})

def update_profile(request):
    if request.method == 'POST':
        user = request.user
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')

        if name:
            user.first_name = name.split()[0]
            user.last_name = ' '.join(name.split()[1:])

        if email:
            user.email = email

        if username:
            user.username = username

        user.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})