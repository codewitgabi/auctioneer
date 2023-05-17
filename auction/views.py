from django.shortcuts import render


def home(request):
	context = {}
	return render(request, "auction/home.html", context)


