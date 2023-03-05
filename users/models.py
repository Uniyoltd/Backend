from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for ndambaplay_backend.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """
    email = models.EmailField(unique=True)
    phone_number = models.CharField(null=True, max_length=30)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='users/images', null=True)
    address = models.CharField(max_length=255, default="")

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def get_user(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone_number': self.phone_number,
            'is_verified': self.is_verified,
            'address': self.address,
            'profile_picture': str(self.profile_picture)
        }




