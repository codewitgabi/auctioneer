from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone


class User(AbstractUser):
	id = models.UUIDField(
		primary_key=True,
		default=uuid.uuid4,
		editable=False)
	username = models.CharField(max_length=30)
	email = models.EmailField(unique=True)
	phone = models.CharField(max_length=14, blank=True, null=True)
	avatar = models.ImageField(default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-uPy9lZuIjzqW0aACiqVpVRFQqP3mpf54Fw&s")
	
	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ["username"]
	
	@property
	def get_cart_price(self):
	    count: int = 0
	    return [count + float(lot.price) for lot in self.lot_set.all()][0]
	
	def __str__(self):
	    return self.username
