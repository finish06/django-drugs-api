from django.urls import path, include
from rest_framework.routers import DefaultRouter

from drugs import views

router = DefaultRouter()
router.register('drugs', views.DrugViewSet)
router.register('routes', views.RouteViewSet)
router.register('moa', views.MoaViewSet)

app_name = "drugs"

urlpatterns = [
    path('', include(router.urls))
] 