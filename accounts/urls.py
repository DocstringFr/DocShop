from django.urls import path
from accounts.views import signup, logout_user, login_user, profile, set_default_shipping_address, delete_address

app_name = 'accounts'

urlpatterns = [
    path('signup/', signup, name="signup"),
    path('delete_address/<int:pk>/', delete_address, name="delete-address"),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name="logout"),
    path('profile/', profile, name="profile"),
    path('profile/set_default_shipping/<int:pk>/', set_default_shipping_address, name="set-default-shipping"),
]
