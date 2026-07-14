from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def user_statistics(request):

    return render(
        request, 
        "user_statistics/user_statistics.html",
        {
            "page_title": "Statistics",
        },
    )
