
from django.urls import path,include
from .views import authView,home




urlpatterns = [
    path("",home,name="home"), # Home page view
    path('accounts/',include("django.contrib.auth.urls") ),
    path("signup/",authView,name="authView"), # Include the base app's URLs
]
