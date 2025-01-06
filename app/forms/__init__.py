from .auth_forms import LoginForm, RegisterForm  # Correctly import the RegisterForm
from .product_form import ProductForm, CartForm  # Import ProductForm from product_form.py
from .edit_profile_form import EditProfileForm  # Import EditProfileForm from product_form.py



print(LoginForm, RegisterForm)
print(ProductForm, CartForm, EditProfileForm)