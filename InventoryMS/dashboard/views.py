# Import necessary modules and classes from Django
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

# Import models, forms, and CustomUserChangeForm from the current app
from . import models
from .forms import AddProductForm, SearchForm, CustomUserChangeForm


# Define a view function for the dashboard index
@login_required
def dashboard_index(request):
    # Retrieve user information
    user = request.user
    f_name = request.user.first_name or 'N/A'
    l_name = request.user.last_name or 'N/A'
    email = request.user.email or 'N/A'

    # Print user information for debugging (optional)
    print(user)

    if user.username == 'admin':
        # Render the admin dashboard page
        return render(request, 'dashboard/index.html',
                      {'title': 'Admin Dashboard', 'user_type': 'Admin', 'f_name': f_name, 'l_name': l_name,
                       'email': email})
    else:
        # Render the regular user dashboard page
        return render(request, 'dashboard/index-user.html',
                      {'title': 'User Dashboard', 'user_type': 'User', 'f_name': f_name, 'l_name': l_name,
                       'email': email})


# Define a view function for adding products
@login_required
def add_products(request):
    form = AddProductForm()

    if request.method == 'POST':
        # Handle form submission
        form = AddProductForm(request.POST)

        if form.is_valid():
            # Save the form if it is valid
            form.save()

            # Render the result page with success message
            context = {
                'result': 'New Product Added successfully',
                'title': 'Add Products',
            }
            return render(request, 'dashboard/result.html', context=context)
        else:
            # Render the result page with an error message
            context = {
                'result': 'ERROR',
                'title': 'Add Products',
            }
            return render(request, 'dashboard/result.html', context=context)

    # Render the form for adding products
    context = {
        'form': form,
        'title': 'Add Products',
    }
    return render(request, 'dashboard/add_product.html', context=context)


# Define a view function for searching available products
@login_required
def search_available_products(request):
    form = SearchForm()

    if request.method == 'POST':
        # Handle form submission
        form = SearchForm(request.POST)

        if form.is_valid():
            # Retrieve search_product from the form
            search_product = form.cleaned_data['search_product']

            # Query the database for products with matching names
            all_products = models.Available_product_table.objects.filter(product_name=search_product).values()

            # Render the result page with the list of matching products
            context = {
                'all_products': all_products,
                'title': 'Search Result',
            }
            return render(request, 'dashboard/view_available_products.html', context=context)

    # Render the form for searching available products
    context = {
        'form': form,
        'title': 'Search Products',
    }
    return render(request, 'dashboard/search_product.html', context=context)


# Define a view function for viewing all available products
@login_required
def view_available_products(request):
    # Query the database for all available products
    all_products = models.Available_product_table.objects.all()

    # Render the page with the list of all available products
    context = {
        'all_products': all_products,
        'title': 'All Products',
    }
    return render(request, 'dashboard/view_available_products.html', context=context)


# Define a view function for selling available products
@login_required
def sell_available_products(request):
    if request.method == 'POST':
        # Handle form submission
        sell_product_id = request.POST['product_id']
        sell_qty = int(request.POST['sellqty'])

        # Query the database for the selected product
        sell_product = models.Available_product_table.objects.filter(id=sell_product_id).values()
        sell_product = sell_product[0]

        if sell_qty <= sell_product['product_quantity']:
            # Create a Sold_product_table entry for the sold product
            product = models.Sold_product_table(
                product_id=sell_product['id'],
                product_name=sell_product['product_name'],
                product_price=sell_product['product_price'],
                product_quantity=sell_qty,
            )
            product.save()

            # Update the Available_product_table with the remaining quantity
            remaning_qty = sell_product['product_quantity'] - sell_qty
            update_product = models.Available_product_table.objects.get(id=sell_product_id)
            update_product.product_quantity = remaning_qty
            update_product.save()

            # Render the result page with success message
            context = {
                'result': 'Product sold successfully!',
                'title': 'Buy Products',
            }
            return render(request, 'dashboard/result.html', context=context)
        else:
            # Render the result page with an error message
            context = {
                'result': 'Enter Quantity is less than available stock or Product is Out of Stock!',
                'title': 'Buy Products',
            }
            return render(request, 'dashboard/result.html', context=context)

    # Query the database for all available products
    all_products = models.Available_product_table.objects.all()

    # Render the form for selling available products
    context = {
        'all_products': all_products,
        'title': 'Buy Products',
    }
    return render(request, 'dashboard/buy_products.html', context=context)


# Define a view function for viewing sold products
@login_required
def view_sold_products(request):
    # Query the database for all sold products
    all_sold_products = models.Sold_product_table.objects.all()

    # Render the page with the list of all sold products
    context = {
        'all_sold_products': all_sold_products,
        'title': 'Sold Products',
    }
    return render(request, 'dashboard/view_sold_products.html', context=context)


# Define a view function for managing users
@login_required
def users(request):
    # Create a UserCreationForm instance
    form = UserCreationForm

    if request.method == 'POST':
        # Handle form submission
        form = UserCreationForm(request.POST)

        if form.is_valid():
            # Save the form if it is valid
            form.save()

            # Render the result page with success message
            context = {
                'result': 'User Added successfully',
                'title': 'Add User',
            }
            return render(request, 'dashboard/result.html', context=context)
        else:
            # Render the result page with an error message
            context = {
                'result': 'ERROR - Does not meet the requirements!',
                'title': 'Add User',
            }
            return render(request, 'dashboard/result.html', context=context)

    # Render the form for adding users
    context = {
        'form': form,
        'title': 'Add User',
    }
    return render(request, 'dashboard/user.html', context=context)


# Define a view function for removing users
@login_required
def remove_user(request):
    # Query the database for all users
    users = User.objects.all()

    # Render the page for removing users
    return render(request, 'dashboard/remove_user.html', {'users': users, 'title': 'Remove User'})


# Define a view function for deleting a user
@login_required
def delete_user(request, user_id):
    # Retrieve the user by ID
    u_id = User.objects.get(pk=user_id)

    # Check if the request is a POST request (i.e., form submission)
    if request.method == 'POST':
        # Perform user removal
        if u_id.is_superuser:
            # You may want to handle this case differently, e.g., display an error message
            return render(request, 'dashboard/result.html',
                          {'title': 'Remove User', 'result': 'Cannot delete the admin user.'})
        u_id.delete()

    # Redirect to the dashboard index page after user deletion
    return render(request, 'dashboard/index.html')


# Define a view function for listing available products
@login_required
def product_list(request):
    # Query the database for available products with quantity greater than 0
    products = models.Available_product_table.objects.filter(product_quantity__gt=0)

    # Render the page with the list of available products
    return render(request, 'dashboard/product_list.html', {'title': 'Product List', 'products': products})


# Define a view function for updating a product
@login_required
def update_product(request, product_id):
    # Retrieve the product by ID
    product = models.Available_product_table.objects.get(pk=product_id)

    if request.method == 'POST':
        # Update the product fields directly
        product.product_name = request.POST['product_name']
        product.product_price = request.POST['product_price']
        product.product_quantity = request.POST['product_quantity']
        product.save()

        # Redirect to the product list page after product update
        return redirect('dashboard:product_list')

    # Render the form for updating a product
    return render(request, 'dashboard/update_product.html', {'title': 'Update Product', 'product': product})


# Define a view function for deleting a product
@login_required
def delete_product(request, product_id):
    # Retrieve the product by ID
    product = models.Available_product_table.objects.get(pk=product_id)

    if request.method == 'POST':
        # Perform product deletion
        product.delete()

        # Redirect to the product list page after product deletion
        return redirect('dashboard:product_list')

    # Render the confirmation page for deleting a product
    return render(request, 'dashboard/delete_product.html', {'title': 'Delete List', 'product': product})


# Define a view function for shopping available products
def shop_products(request):
    # Query the database for available products with quantity greater than 0
    products = models.Available_product_table.objects.filter(product_quantity__gt=0)

    # Render the page with the list of available products for shopping
    return render(request, 'dashboard/shop_products.html', {'title': 'Shop Products', 'products': products})


# Define a view function for user profile
def user_profile(request):
    # Your view logic here

    # Render the user profile page
    return render(request, 'dashboard/user_profile.html')


# Define a class-based view for user profile with LoginRequiredMixin
class UserProfileView(LoginRequiredMixin, View):
    template_name = 'dashboard/user_profile.html'

    def get(self, request, *args, **kwargs):
        # Retrieve the user profile form with the user's current information
        form = CustomUserChangeForm(instance=request.user)

        # Render the user profile page with the form
        return render(request, 'dashboard/user_profile.html', {'form': form, 'title': 'User Profile'})

    def post(self, request, *args, **kwargs):
        # Handle form submission for updating user profile
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

            # Redirect to the dashboard index page after user profile update
            return redirect('dashboard:dashboard_index')  # Use the correct name here

        # Render the user profile page with the form and validation errors
        return render(request, 'dashboard/user_profile.html', {'form': form, 'title': 'User Profile'})
