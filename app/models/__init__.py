from .models import User, Product, Sales, Admin   # Import the Seller model



__all__ = ['Admin', 'Product', 'User', 'Sales']  # Include any other models that should be exported

def __init__(self, **kwargs):
    super().__init__(**kwargs)
    if not self.profile_image:
        self.profile_image = 'default_profile.jpg'
