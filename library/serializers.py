from rest_framework import serializers
from .models import Category, Author, Books, Order, OrderItem, Cart



class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'title',
            'book_count'
        ]


class AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            'full_name',
            'bio',
            'img',
            'book_count',
            'create_at'
        ]


class BookSerializers(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = [
            'title',
            'category',
            'author',
            'img',
            'price',
            'discount_price',
            'bio',
            'page_count',
            'published',
            'lang',
            'level'
        ]

class CartSerializers(serializers.ModelSerializer):
    book_info = BookSerializers(read_only=True, source='book')
    
    class Meta:
        model = Cart
        fields = "__all__"
        
        
class OrderItemSerializers(serializers.ModelSerializer):
    book = BookSerializers(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ("book", "qty", "price", "is_active")
    
class OrderSerializers(serializers.ModelSerializer):
    order_items = OrderItemSerializers(many=True, read_only=True, source='orderitem_set')
    
    class Meta:
        model = Order
        fields = ('user', 'total_price', 'total_discount', 'status', 'order_items')
    