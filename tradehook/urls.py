from django.urls import path
from django.contrib.auth.views import LogoutView
from rest_framework_nested import routers
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.decorators.csrf import csrf_protect
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

# registering backend endpoints.
router = routers.DefaultRouter()
router.register('users',views.UserViewSet,basename='users')
router.register('api_keys',views.APIKeysViewSet,basename='api_keys')
router.register('event_logs',views.EventLogViewSet,basename='event_logs')
router.register('brokers',views.BrokerViewSet,basename='brokers')
router.register('customer_brokers',views.CustomerBrokersViewSet,basename='customer_brokers')

users_router = routers.NestedDefaultRouter(
    router,'users',lookup='user'
    )
api_keys_router = routers.NestedDefaultRouter(
    router,'api_keys',lookup='api_key'
    )
event_logs_router = routers.NestedDefaultRouter(
    router,'event_logs',lookup='event_log'
    )
brokers_router = routers.NestedDefaultRouter(
    router,'brokers',lookup='broker'
    )
customer_brokers_router = routers.NestedDefaultRouter(
    router,'customer_brokers',lookup='customer_broker'
)


# registering frontend endpoints
urlpatterns = [path('webhook/', views.webhook_receiver, name='webhook-receiver'),
               
               path('home/', views.home_page,name='home-page'),
               
               path('me/',csrf_protect(login_required(views.MeView.as_view())),name='me'),
               path('brokers/', views.brokers_list, name='brokers-list'),
               path('api-keys/', csrf_protect(login_required(views.APIKeyView.as_view())), name='api-keys'),
               path('event-logs/', csrf_protect(login_required(views.EventLogView.as_view())), name='event-logs'),
               path('account/', csrf_protect(login_required(views.account)),name='account'),
               path('alert-guide/',csrf_protect(views.alert_guide),name='alert-guide'),
               path('register/', views.register, name='register'),
               #path('login/', LoginView.as_view(), name='login'),
               path('logout/', LogoutView.as_view(), name='logout'),
] 
urlpatterns += router.urls + api_keys_router.urls + event_logs_router.urls + brokers_router.urls + customer_brokers_router.urls + users_router.urls 
urlpatterns += staticfiles_urlpatterns()


