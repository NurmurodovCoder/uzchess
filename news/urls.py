from django.urls import path, include
from .views import NewsAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'news', NewsAPIView)

urlpatterns = [
    path('', include(router.urls))
]
