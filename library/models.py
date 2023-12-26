from django.db import models
from django.contrib.auth.models import User

class Lang(models.Choices):
    uz = 'UZ'
    ru = 'RU'
    en = 'En'


class Level(models.Choices):
    beginner = 'Beginner'
    hart = 'Hart'
    medium = 'Medium'


class Category(models.Model):
    title = models.CharField(max_length=255)

    book_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Author(models.Model):
    full_name = models.CharField(max_length=255)
    bio = models.TextField
    img = models.ImageField(upload_to='library/author')

    book_count = models.IntegerField(default=0)

    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Books(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='book')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='book')

    img = models.ImageField(upload_to='library')
    price = models.IntegerField(default=0)
    discount_price = models.IntegerField(default=0)
    bio = models.TextField()  # RichText

    page_count = models.IntegerField(default=1)
    published = models.DateField()

    lang = models.CharField(max_length=50, choices=Lang.choices)
    level = models.CharField(max_length=50, choices=Level.choices)
    
    is_active = models.BooleanField(default=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
    def active(self):
        if self.active and self.count>0:
            return True
        return False

    def can_buy(self, qty=0):
        holded_books = OrderItem.objects.filter(book=self, is_active=True).aggregate(total_qty=Sum('qty'))['total_qty'] or 0

        return self.count - holded_books >= qty and self.active()


class Order(models.Model):
    STATUS = (
        ('initial', 'Initial'),
        ('payment', "Payment"),
        ('delivery', "Delivery"),
        ('completed', "Completed"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    total_price = models.IntegerField(default=0)
    total_discount = models.IntegerField(default=0)
    
    status = models.CharField(max_length=16, choices=STATUS, default='initial')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    
    is_active = models.BooleanField(default=True)


class Cart(models.Model):
    STATUS_CHOICES = (
        ('initial', 'Initial'),
        ('completed', 'Completed'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, null=True)
    qty = models.IntegerField(default=0)
    status = models.CharField(max_length=64, choices=STATUS_CHOICES, default='initial')
    
    def update_qty(self, qty):
        can_buy = Books.can_buy(book=self.book, qty=qty)
        if can_buy:
            self.qty=qty
            self.save()
            return True
        return False
            
    @classmethod
    def create_order(csl, user):
        carts = Cart.objects.filter(user=user, status='initial')
        all_available = all([Book.can_buy(cart.book, cart.qty) for cart in carts])

        if not all_available:
            return False
        
        order = Order.objects.create(user=user)
        
        total_price = 0
        total_discount = 0

        for cart in carts:
            cart.status = 'completed'
            cart.save()
            
            total_price += cart.book.price * cart.qty
            total_discount += cart.book.discount_price * cart.qty
            
            OrderItem.objects.create(order=order, book=cart.book, price=cart.book.discount_price, qty=cart.qty)

            cart.book.count = cart.book.count - cart.qty
            cart.book.save()
            
        order.total_price = total_price
        order.total_discount = total_discount
        order.save()
        return True


