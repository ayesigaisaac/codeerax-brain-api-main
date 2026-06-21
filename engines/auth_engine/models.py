import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from datetime import timedelta


# ---------------------------
# Custom User Manager
# ---------------------------
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None, **extra_fields):
        if not email:
            raise ValueError("Email is required.")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        # automatically generate verification token on user creation
        user.generate_email_verification()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, username=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, username, **extra_fields)


# ---------------------------
# Custom User Model
# ---------------------------
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=False)   # requires email verification
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)


    # Email verification fields
    def default_email_verification_expiry():
        return timezone.now() + timedelta(hours=24)
    
    email_verification_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False, 
        null=True, 
        blank=True
    )
    email_verification_expiry = models.DateTimeField(
        default=default_email_verification_expiry, 
        null=True, 
        blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    # ---------------------------
    # Generate new verification token
    # ---------------------------
    def generate_email_verification(self, expiry_hours: int = 24):
        self.email_verification_token = uuid.uuid4()
        self.email_verification_expiry = timezone.now() + timedelta(hours=expiry_hours)
        
class BlacklistedToken(models.Model): 
    token = models.TextField(unique=True)
    blacklisted_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Blacklisted: {self.token[:20]}"