from rest_framework.permissions import BasePermission
from .models import Books


class BookPermissions(BasePermission):
     def has_permission(self, request, *args, **kwargs):
          if request.method == 'GET':
               return True
          return request.user.is_staff
     
     def has_object_permission(self, request,*args, **kwargs):
          if request.method == 'GET':
               return True
          return request.user.is_staff
          
