from django.db import models
from django.core.validators import RegexValidator
from course.models import Course
from library.models import Books
from django.contrib.auth.models import User

# phone_numbers = RegexValidator(
#     negex=r'^\+998\d{9}$',
#     message="Xato raqam terildi qayta tekshiring"
# )


# class BookOrder(models.Model):
#     pending = 'Pending'
#     processing = 'Processing'
#     shipped = 'Shipped'
#     delivered = 'Delivered'
#     cancelled = 'Cancelled'

#     STATUS_CHOICES = [
#         (pending, 'Pending'),
#         (processing, 'Processing'),
#         (shipped, 'Shipped'),
#         (delivered, 'delivered'),
#         (cancelled, 'Cancelled'),
#     ]

#     product = models.ForeignKey(Books, on_delete=models.CASCADE, null=True, blank=True)

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=pending)

#     phone_number = models.CharField(max_length=32, validators=[phone_numbers])

#     def is_transition_allowed(self, new_status):
#         allowed_transitions = {
#             self.pending: [self.processing, self.cancelled],
#             self.processing: [self.shipped, self.cancelled],
#             self.shipped: [self.delivered, self.cancelled]
#         }

#         return new_status in allowed_transitions.get(self.status, [])


# class CourseOrder(models.Model):
#     pending = 'Pending'
#     processing = 'Processing'
#     shipped = 'Shipped'
#     delivered = 'Delivered'
#     cancelled = 'Cancelled'
#
#     STATUS_CHOICES = [
#         (pending, 'Pending'),
#         (processing, 'Processing'),
#         (shipped, 'Shipped'),
#         (delivered, 'delivered'),
#         (cancelled, 'Cancelled'),
#     ]
#
#     product = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
#
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=pending)
#
#     phone_number = models.CharField(max_length=32, validators=[phone_numbers])
#
#     def is_transition_allowed(self, new_status):
#         allowed_transitions = {
#             self.pending: [self.processing, self.cancelled],
#             self.processing: [self.shipped, self.cancelled],
#             self.shipped: [self.delivered, self.cancelled]
#         }
#
#         return new_status in allowed_transitions.get(self.status, [])
