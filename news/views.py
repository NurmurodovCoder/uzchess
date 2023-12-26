from django.shortcuts import render
from rest_framework import viewsets
from .models import News
from .serializers import NewsSerializers
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .permission import NewsPermission

from rest_framework.decorators import api_view


class CustomBookPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 1000


class NewsAPIView(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializers

    pagination_class = CustomBookPagination
    permission_classes = [NewsPermission]

#     def list(self, request, *args, **kwargs):
#         category = request.query_param.get('category')
#         if category:
#             self.queryset = self.queryset.filter(category=category)
#         return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializers = self.get_serializer(instance)

        similar = News.objects.exclude(id=instance.id)[:3]
        similar_serializers = NewsSerializers(similar, many=True)

        return Response({
            'new': serializers.data,
            'similar_news': similar_serializers.data
        })

    # @action(detail=False, method=['get'])
    # def top_news(self, request):
    #     top_new = News.objects.annotate(avg_rating=models.Avg('relaetd_name__rating')).order_by('-avg_rating')[:2]
    #     serializer = NewsSerializers(top_new, many=True)
    #     return Response(serializer.data)
