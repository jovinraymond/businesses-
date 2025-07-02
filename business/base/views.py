from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .models import CustomUser

@login_required
def home(request):
    return render(request, "home.html", {})

def authView(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Send verification email
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_url = request.build_absolute_uri(
                reverse("verify_email", kwargs={"uidb64": uid, "token": token})
            )
            subject = "Verify Your Email Address"
            message = f"Hi {user.username},\n\nPlease click the link below to verify your email:\n{verification_url}\n\nThank you!"
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER or "noreply@yourdomain.com",
                [user.email],
                fail_silently=False,
            )
            return render(request, "registration/verification_sent.html")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_email_verified = True
        user.save()
        login(request, user)
        return redirect("home")
    else:
        return render(request, "registration/verification_failed.html")