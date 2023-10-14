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
    image = models.ImageField()
    lot = models.ForeignKey("Lot", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Lot Images"
        indexes = [
            models.Index(fields=["image"], name="img_idx")
        ]

    def __str__(self):
        return self.image.url


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
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, editable=False)
    sold = models.BooleanField(default=False)

    # Add the "paid" column
    paid = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Lots"
        db_table = "lot"
        ordering = ["-auction_date", "endtime"]
        indexes = [
            models.Index(fields=["name", "price", "increment"])
        ]

    def get_absolute_url(self):
        return reverse("auction:lot_bid_view", kwargs={
            "lot_id": self.id
        })

    def clean(self):
        """ Make sure buyer is the highest bidder """
        if self.bid_set.all() and self.has_ended:
            winner: User = self.bid_set.order_by("-bid").first().bidder

            if self.buyer != winner:
                raise ValidationError(_(f"The selected buyer is not the winner of the bid, please select {winner.username}."))

            super().check()

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
    bid = models.DecimalField(
        max_digits=50, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = "bidder"
        indexes = [
            models.Index(fields=["bidder", "bid"], name="bid_idx")
        ]
        ordering = ["bid"]

    def clean(self):
        # clean bid: Ensure bid is not less than the lot's price
        if self.bid < self.lot.price:
            raise ValidationError(
                _("Your bid can't be less than the lot's price"))

        # clean bidder: Ensure only an instance of a bidder exists for a lot
        if Bid.objects.filter(bidder=self.bidder).exists():
            raise ValidationError(
                _(f"{self.bidder.username} already has a bid instance"))

    def __str__(self):
        return self.bidder.username
