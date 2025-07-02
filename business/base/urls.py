
from django.urls import path,include
from .views import authView,home,verify_email




urlpatterns = [
    path("", home, name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("signup/", authView, name="authView"),
    path("verify-email/<uidb64>/<token>/", verify_email, name="verify_email"),
]
