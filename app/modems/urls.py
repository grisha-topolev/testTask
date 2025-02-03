from django.urls import path, include
from rest_framework.routers import DefaultRouter
from modems.api.v1.views import ModemViewSet, CounterViewSet, SensorViewSet, process_modem_data

router = DefaultRouter()
router.register('modem', ModemViewSet)
router.register('counter', CounterViewSet)
router.register('sensor', SensorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('data/', process_modem_data, name='process-data'),
]