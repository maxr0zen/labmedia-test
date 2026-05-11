from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.clients.views import ClientViewSet
from apps.payments.views import PaymentViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
