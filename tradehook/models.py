import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone   

# Custom User manager to define required information to create user and superuser
class CustomerAccountManager(BaseUserManager):

    def create_user(self,email,username,first_name,last_name,password,**other_fields):

        email = self.normalize_email(email)
        user = self.model(email=email,username=username,first_name=first_name,last_name=last_name,**other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, first_name, last_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if other_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, username, first_name, last_name, password, **other_fields)

# Custom user class.
class User(AbstractBaseUser, PermissionsMixin):
    
    # Cannot have two accounts with the same email.
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    start_date = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    password = models.CharField(max_length=255)
    objects = CustomerAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    def __str__(self) -> str:
        return self.username

class CustomerBrokers(models.Model):
    # All current and future brokers will be heres
    ALPACA = 'Alpaca'
    ALPACA_PAPER = 'Alpaca - Paper'
    #OANDA = 'Oanda'
    #TRADESTATION = 'Tradestation'

    # Defines available brokers
    MEMBERSHIP_CHOICES = [
        (ALPACA, 'Alpaca'),
        (ALPACA_PAPER, 'Alpaca - Paper'),
        #(OANDA, 'Oanda'),
        #(TRADESTATION, 'Tradestation'),
    ]

    # CustomerBroker objects are attached to users, upon deleting user, customerbroker object is also deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    broker_name = models.CharField(
        max_length=255, choices=MEMBERSHIP_CHOICES)
   
    broker_api_key = models.CharField(max_length=255)

    # Some brokers may only provide one api key so the secret key is optional. 
    broker_secret_key = models.CharField(max_length=255, null=True, blank=True)

    # A user can only have one of each broker.
    class Meta:
        unique_together = ('user', 'broker_name')
    
class APIKeys(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tradehook_api_key = models.UUIDField(default=uuid.uuid4, unique=True)

class EventLog(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    received_at = models.DateTimeField(default=timezone.now)

    # Both webhook_data and broker_response are model fields that will be filled by post requests from other servers.
    webhook_data = models.JSONField()
    broker_response = models.JSONField()

class Broker(models.Model):

    slug = models.SlugField()
    broker_name = models.CharField(max_length=255)
    description = models.TextField(null=True,blank=True)

