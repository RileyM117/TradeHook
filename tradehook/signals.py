#from django.db.models.signals import post_save
#from django.dispatch import receiver
#from django.conf import settings  # Import your User model if you've customized it
#from .models import U  # Import your Customer model
#
#@receiver(post_save, sender=settings.AUTH_USER_MODEL)
#def create_customer_profile(sender, instance, created, **kwargs):
#    if created:
#        Customer.objects.create(user=instance,first_name=instance.first_name,last_name=instance.last_name)
#
#def save_customer(sender, instance, **kwargs):
#    instance.customer.save()
