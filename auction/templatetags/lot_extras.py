from django import template

register  = template.Library()

@register.inclusion_tag("auction/output.html")
def display_button_to_lot_bidding(user, lot) -> bool:
    """
    Checks if a user has placed a bid
    """
    for bid in lot.bid_set.all():
        if bid.bidder == user:
            return {"has_placed_bid": True, "lot": lot}
    return {"has_placed_bid": False, "lot": lot}