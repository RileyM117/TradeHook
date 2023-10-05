from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models
# Register your models here.

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):

    list_display = ['id','email','username','first_name','last_name','is_staff','is_active']
    list_editable = ['email','username','first_name','last_name','is_staff','is_active']
    list_filter = list_editable
    list_per_page = 10
    search_fields = ['id','email__istartswith','username__istartswith','first_name__istartswith','last_name__istartswith']
    ordering = ['id']

@admin.register(models.CustomerBrokers)
class CustomerBrokersAdmin(admin.ModelAdmin):

    list_display = ['user_id','user_first_name','user_last_name',
                    'broker_name','broker_api_key','broker_secret_key']
    list_editable = list_display[3:]
    list_per_page = 10
    search_fields = ['user__id','user__first_name','user__last_name']
    list_filter = ['broker_name']
    list_select_related = ['user']
    ordering = ['user_id']

    @admin.display()
    def user_first_name(self,customerbrokers):
        return customerbrokers.user.first_name
    
    @admin.display()
    def user_last_name(self,customerbrokers):
        return customerbrokers.user.last_name
    
    @admin.display()
    def user_id(self,customerbrokers):
        return customerbrokers.user.id

@admin.register(models.APIKeys)
class APIKeysAdmin(admin.ModelAdmin):

    list_display = ['user_id','user_first_name','user_last_name',
                    'tradehook_api_key','tradehook_api_key_id']
    list_editable = ['tradehook_api_key']
    list_per_page = 10
    search_fields = ['user__id','user__first_name','user__last_name']
    list_select_related = ['user']
    ordering = ['user_id']

    @admin.display()
    def user_first_name(self,apikeys):
        return apikeys.user.first_name
    
    @admin.display()
    def user_last_name(self,apikeys):
        return apikeys.user.last_name
    
    @admin.display()
    def user_id(self,apikeys):
        return apikeys.user.id
    
    @admin.display()
    def tradehook_api_key_id(self,apikeys):
        return apikeys.id

@admin.register(models.EventLog)
class EventLogAdmin(admin.ModelAdmin):

    list_display = ['user_id','user_first_name','user_last_name',
                    'received_at','webhook_data','broker_response']
    list_per_page = 10
    list_filter = ['received_at']
    search_fields = ['user__id','user__first_name','user__last_name','received_at']
    list_select_related = ['user']
    ordering = ['id']

    @admin.display()
    def user_first_name(self,eventlog):
        return eventlog.user.first_name
    
    @admin.display()
    def user_last_name(self,eventlog):
        return eventlog.user.last_name
    
    @admin.display()
    def user_id(self,eventlog):
        return eventlog.user.id
    
@admin.register(models.Broker)
class BrokerAdmin(admin.ModelAdmin):

    list_display = ['broker_name', 'description']
    list_per_page = 10
    list_filter = ['broker_name']
    search_fields = ['broker_name']
    list_editable = ['description']  # You can make 'description' field editable
    list_display_links = ['broker_name']  # Specify which field to be linked for editing
   