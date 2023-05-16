# python imports
import uuid

# django imports
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class LotImage(models.Model):
	id = models.UUIDField(
		primary_key=True,
		default=uuid.uuid4,
		editable=False
	)
	image = models.ImageField(upload_to="property")
	image_url = models.URLField(max_length=2048, editable=False)
	lot = models.ForeignKey("Lot", on_delete=models.CASCADE)
	
	class Meta:
		verbose_name_plural = "Property Images"
		indexes = [
			models.Index(fields=["image_url"], name="img_idx")
		]
	
	def save(self, *args, **kwargs):
		self.image_url = self.image.url
		super().save(*args, **kwargs)
		
	def __str__(self):
		return self.image_url
	

class Lot(models.Model):
	id = models.UUIDField(
		primary_key=True,
		default=uuid.uuid4,
		editable=False
	)
	name = models.CharField(max_length=80)
	description = models.TextField(blank=True, null=True)
	price = models.DecimalField(max_digits=30, decimal_places=2)
	increment = models.DecimalField(max_digits=10, decimal_places=2)
	auction_date = models.DateTimeField()
	sold = models.BooleanField(default=False)
	
	class Meta:
		verbose_name_plural = "Properties"
		db_table = "property"
		indexes = [
			models.Index(fields=["name", "price", "increment"])
		]
	
	def __str__(self):
		return self.name
		
	
class Bidder(models.Model):
	id = models.UUIDField(
		primary_key=True,
		default=uuid.uuid4,
		editable=False
	)
	lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	bid = models.DecimalField(max_digits=30, decimal_places=2)
	
	class Meta:
		db_table = "bidder"
		indexes = [
			models.Index(fields=["user", "bid"], name="bid_idx")
		]
		ordering = ["bid"]
	
	def __str__(self):
		return self.user.username

