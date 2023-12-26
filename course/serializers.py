from rest_framework import serializers
from .models import Category, Author, Course, Block, Lesson, Comments # , Cart, OrderItem, Order


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        ref_name = 'Category'

        model = Category
        fields = [
            'id',
            'title',
            'course_count',
        ]


class AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        ref_name = 'Author'

        model = Author
        fields = [
            'id',
            'full_name',
            'img',
            'bio',
            'course_count',
        ]


class CourseReadSerializers(serializers.ModelSerializer):
    category = CategorySerializers(read_only=True)
    author = AuthorSerializers(read_only=True)

    class Meta:

        model = Course
        fields = [
            'id',
            'title',
            'category',
            'author',
            'img',
            'lang',
            'block',
            'price',
            'discount_price',
            'level',
            'create_at'
        ]

class CourseCreateSerializers(serializers.ModelSerializer):

    class Meta:

        model = Course
        fields = [
            'title',
            'category',
            'author',
            'img',
            'lang',
            'block',
            'price',
            'discount_price',
            'level',
        ]


class BlockSerializers(serializers.ModelSerializer):
    class Meta:
        ref_name = 'Block'

        model = Block
        fields = [
            'id',
            'title'
        ]


class LessonSerializers(serializers.ModelSerializer):
    block = BlockSerializers()
    course = CourseReadSerializers()

    class Meta:
        ref_name = 'Lesson'

        model = Lesson
        fields = [
            'id',
            'title',
            'bio',
            'url',
            'block',
            'course'
        ]


class CommentSerializers(serializers.ModelSerializer):
    course = CourseReadSerializers()

    # useer = UserSerializers()

    class Meta:
        ref_name = 'Comment'

        model = Comments
        fields = [
            'id',
            'title',
            'user',
            'course',
            'rating',
            'create_at'
        ]


# class CartSerializer(serializers.ModelSerializer):
#     course = CourseSerializers()
    
#     class Meta:
#         model = Cart
#         fields = '__all__'

# class OrderItemSerializers(serializers.ModelSerializer):
#     course = CourseSerializers()
    
#     class Meta:
#         model = OrderItem
#         fields = '__all__'

# class OrderSerializers(serializers.ModelSerializer):
#     order_item = OrderItemSerializers()
    
#     class Meta:
#         model = Order
#         fields = '__all__'
