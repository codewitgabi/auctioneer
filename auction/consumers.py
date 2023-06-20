import json
from django.contrib.auth import get_user_model
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from auction.models import Lot, Bid

# user object
User = get_user_model()


class BidConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # accept connection
        await self.accept()
        self.user = self.scope["user"]
        self.lot_id = self.scope["url_route"]["kwargs"].get("lot_id")
        self.lot = await self.get_lot()

        # create bid group
        self.bid_group = self.lot_id

        await self.channel_layer.group_add(
            self.bid_group, self.channel_name
        )

        # broadcast bids
        await self.channel_layer.group_send(
            self.bid_group, {"type": "broadcast_bids"}
        )

    async def disconnect(self, close_code):
        """ Disconnect handler """
        await self.channel_layer.group_discard(
            self.bid_group, self.channel_name
        )

    async def receive(self, text_data):
        bid = json.loads(text_data)["bid"]

        await self.update_bid(bid)

        # broadcast bids
        await self.channel_layer.group_send(
            self.bid_group, {"type": "broadcast_bids"}
        )

    @database_sync_to_async
    def update_bid(self, new_bid):
        bid = Bid.objects.filter(lot=self.lot).order_by("-bid").first()

        bid_bid = bid.bid if bid.bid else self.lot.price

        if bid_bid < new_bid:
            new_bidding = Bid.objects.get_or_create(
                bidder=self.user, lot=self.lot)[0]

            new_bidding.bid = new_bid
            self.lot.price = new_bid

            # save objects
            self.lot.save()
            new_bidding.save()

    @database_sync_to_async
    def get_lot(self):
        return Lot.objects.get(id=self.lot_id)

    @database_sync_to_async
    def get_lot_related_bids(self):
        bids = list(self.lot.bid_set.values(
            "bidder", "bid").order_by("-bid").filter(bid__gte=0))

        for bid in bids:
            bid["bidder"] = User.objects.get(id=bid["bidder"]).username
            bid["bid"] = float(bid["bid"])

        return bids

    async def broadcast_bids(self, event):
        await self.send(json.dumps({
            "type": "bids",
            "bids": await self.get_lot_related_bids(),
        }))
