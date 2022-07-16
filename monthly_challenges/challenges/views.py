from ast import arg
from urllib import response
from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.template.loader import render_to_string


monthly_challeng = {
    "january": "Eat no meat for entire month",
    "februrary": "You are in februrary month",
    "march": "You are in march month",
    "april": "You are in april month",
    "may": "You are in May month",
    "june": "You are in june month",
    "july": "You are in july month",
    "august": "You are in august month",
    "september": "You are in september month",
    "october": "You are in october month",
    "november": "You are in november month",
    "december": None

}


def index(request):

    months = list(monthly_challeng.keys())

    return render(request, "challenges/index.html", {
        "months": months
    })


def monthly_challenge_by_number(request, month):

    months = list(monthly_challeng.keys())

    if(month > len(months)):
        return HttpResponseNotFound("Invalid month")

    redirect_month = months[month - 1]

    # it will create a complete path like :  /challenges/january
    redirect_url = reverse("month-challenge", args=[redirect_month])
    return HttpResponseRedirect(redirect_url)


def monthly_challenge(request, m):

    challenge_text = ""
    try:
        challenge_text = monthly_challeng[m]
        return render(request, "challenges/challenge.html", {
            "text": challenge_text,
            "month": m,

        })
    except:
        # It will automatically call 404.html file
        raise Http404()
