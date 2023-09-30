from django.template import RequestContext
from django.http import HttpRequest


def has_perm_to_add_lot(request: HttpRequest):
    return {
        "user_has_perm_to_add_lot": request.user.has_perm("auction.add_lot")
    }
