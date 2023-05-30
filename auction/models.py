# python imports
import uuid

# django imports
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.timesince import timeuntil

User = get_user_model()


class LotImage(models.Model):
	id = models.UUIDField(
		primary_key=True,
		default=uuid.uuid4,
		editable=False
	)
	image = models.ImageField(upload_to="property")
	image_url = models.URLField(max_length=2048, editable=False, blank=True)
	lot = models.ForeignKey("Lot", on_delete=models.CASCADE)
	
	class Meta:
		verbose_name_plural = "Lot Images"
		indexes = [
			models.Index(fields=["image_url"], name="img_idx")
		]
	
	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
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
	price = models.DecimalField(max_digits=50, decimal_places=2)
	increment = models.DecimalField(max_digits=10, decimal_places=2)
	auction_date = models.DateTimeField()
	endtime = models.DateTimeField()
	sold = models.BooleanField(default=False)
	
	class Meta:
		verbose_name_plural = "Lots"
		db_table = "lot"
		indexes = [
			models.Index(fields=["name", "price", "increment"])
		]
		
	
	def get_absolute_url(self):
		return reverse("auction:lot_bid_view", kwargs={
			"lot_id": self.id
		})
	
	@property
	def is_ready(self):
		t, mins = timeuntil(self.auction_date).split(",")[0].split()
		return t == "0" and mins == "minutes"
	
	@property
	def has_ended(self):
		t, mins = timeuntil(self.endtime).split(",")[0].split()
		return t == "0" and mins == "minutes"
	
	def __str__(self):
		return self.name
		
	
class Bid(models.Model):
	id = models.UUIDField(
		primary_key=True,
		default=uuid.uuid4,
		editable=False
	)
	lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
	bidder = models.ForeignKey(User, on_delete=models.CASCADE)
	bid = models.DecimalField(max_digits=50, decimal_places=2, blank=True, null=True)
	
	
	class Meta:
		db_table = "bidder"
		indexes = [
			models.Index(fields=["bidder", "bid"], name="bid_idx")
		]
		ordering = ["bid"]
	
	
	def clean(self):
		# clean bid: Ensure bid is not less than the lot's price
		if self.bid < self.lot.price:
			raise ValidationError(_("Your bid can't be less than the lot's price"))
		
		# clean bidder: Ensure only an instance of a bidder exists for a lot
		if Bid.objects.filter(bidder=self.bidder).exists():
			raise ValidationError(_(f"{self.bidder.username} already has a bid instance"))
	
	def __str__(self):
		return self.bidder.username

