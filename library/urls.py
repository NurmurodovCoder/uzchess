from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryAPIView, AuthorAPIView, BooksAPIView

router = DefaultRouter()
router.register(r'category', CategoryAPIView)
router.register(r'author', AuthorAPIView)
router.register(r'books', BooksAPIView)

urlpatterns = [
    path('', include(router.urls))
]
