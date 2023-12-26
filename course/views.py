from .models import Category, Author, Course, Block, Comments, Lesson # , Order, OrderItem, Cart
from rest_framework import viewsets, views, generics, permissions
from django.shortcuts import get_object_or_404

from .serializers import CategorySerializers, AuthorSerializers, CourseReadSerializers, CourseCreateSerializers, BlockSerializers, \
    CommentSerializers, LessonSerializers # , CartSerializer, OrderItemSerializers, OrderSerializers    x


class CategoryAPIView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class AuthorAPIView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers


class CourseAPIView(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseCreateSerializers


class BlockAPIView(viewsets.ModelViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializers


class LessonAPIView(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializers


class CommentAPIView(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializers


class SubscriptionCreateAPIView(views.APIView):
    
    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        
        if course.subscription_user(request.user):
            return response.Response({'details': "Successfully subscribed"}, status=status.HTTP_201_CREATED)
        return response.Response({'details': "User already subscribed to this course"},
                                 status=status.HTTP_208_ALREADY_REPORTED)
    
class UnsubsicriptionAPIView(views.APIView):
    
    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        
        if course.unsubsicription_user(request.user):
            return response.Response({'details': "Successfully unsubscribed"}, status=status.HTTP_200_OK)
        return response.Response({'details': "User not subscribed to this course"}, status=status.HTTP_204_NO_CONTENT)
