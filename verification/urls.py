from django.urls import path, include
from .views import PhoneNumberRegistration

urlpatterns = [
    path("<phone>/", PhoneNumberRegistration.as_view(), name="OTP Gen"),
]