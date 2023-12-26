from .models import Category, Author, Books, Cart, Order
from .serializers import CategorySerializers, AuthorSerializers, BookSerializers, CartSerializers, OrderItemSerializers, OrderSerializers
from .permissions import BookPermissions
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, generics, views, status, permissions
from rest_framework.response import Response



class CategoryAPIView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class AuthorAPIView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers


class BooksAPIView(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BookSerializers
    permission_classes = [BookPermissions,]


class CartApiView(generics.ListCreateAPIView):
    queryset = Cart.objects.select_related('book')
    serializer_class = CartSerializers
    
    def get_queryset(self):
        query = super().get_queryset()
        return query.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='initial')

class CartAddItemView(views.APIView):
    
    def post(self, request):
        book_id = self.request.data['book_id']
        qty = self.request.data['qty']
        
        if not (book_id and qty):
            raise NotAcceptable({'error': 'Parameters are not given'})
        
        book = get_object_or_404(Books, pk=book_id)
        
        if book.can_by(qty):
            carts = Cart.objects.filter(user=request.user, book=book, status = 'initial')
            if carts.exists():
                cart = carts.first()
                cart.qty = qty
                cart.save()
            else:
                cart = Cart.objects.create(user=request.user, book=book, qty=qty)
                
            return Response(data=CartSerializers(cart).data, status=status.HTTP_201_CREATED)
        else:
            raise ValidationError({'qty': 'Insufficient quantity'})


class CartRemoveItemAPIView(views.APIView):

    def post(self, request):
        book_id = self.request.data['book_id']
        
        if not (book_id):
            raise NotAcceptable({'error': 'Parameters are not given'})

        book = get_object_or_404(Cart, pk=book_id)

        cart_item = Cart.objects.filter(user=request.user, book=book)
        cart_item.delete()
        
        return Response({"message": "Cart item deleted"}, status=status.HTTP_204_NO_CONTENT)


class CreateOrderAPIView(views.APIView):
    
    def post(self, request):
        if len(Cart.objects.filter(user=request.user, status='initial')<=0):
            return Response({'message': 'No products'}, status=status.HTTP_400_BAD_REQUEST)

        if Cart.create_order(request.user):
            return Response({"message": "Order created"}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'Insufficient quantity'}, status=status.HTTP_400_BAD_REQUEST)

class OrderListAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializers
    queryset = Order.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset.filter(user=self.request.user)
        return queryset
    
    
    