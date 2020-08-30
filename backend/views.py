from django.contrib.auth.models import User
from django.shortcuts import render


def index(request):
    user = request.user
    if user.is_anonymous:
        # here
        context = {}
    else:
        # there
        user_count = User.objects.all().count()
        context = {"count": user_count}
    return render(request, "index.html", context)
