import sys

from auction.models import Lot


def ensure_lot_winner():
    """
    Ensures that a lot is assigned a winner even though there is an error in the server
    """
    
    while True:
        lots = Lot.objects.filter(sold=False) # get lots that are not sold yet
        for lot in lots:
            if lot.has_ended:
                lot.buyer = lot.bid_set.order_by("-bid").first().bidder
                lot.sold = True
                lot.save()
                
                sys.stdout.write(f"[INFO] Assigned buyer ({lot.buyer}) to {lot.id}")
