from django.shortcuts import render, redirect

from .models import Meetup, Participant
from .forms import RegistrationForm


def index(request):

    meetups = Meetup.objects.all()
    return render(
        request, "meetups/index.html", {"show_meetups": True, "meetups": meetups}
    )


def meetup_details(request, meetup_slug):
    try:
        selected_meetup = Meetup.objects.get(slug=meetup_slug)
        if request.method == "GET":
            registration_form = RegistrationForm()

        elif request.method == "POST":
            registration_form = RegistrationForm(request.POST)
            if registration_form.is_valid():
                user_email = registration_form.cleaned_data["email"]
                participant, created_new = Participant.objects.get_or_create(
                    email=user_email
                )
                if created_new:
                    selected_meetup.participant.add(participant)
                    return redirect(
                        "confirm-registration", meetup_slug=meetup_slug, added="new"
                    )
                else:
                    return redirect(
                        "confirm-registration", meetup_slug=meetup_slug, added="created"
                    )

        return render(
            request,
            "meetups/meetup-details.html",
            {
                "meetup_found": True,
                "meetup": selected_meetup,
                "form": registration_form,
            },
        )
    except Exception as e:
        print(e)
        return render(request, "meetups/meetup-details.html", {"meetup_found": False})


def confirm_registration(request, meetup_slug, added):
    meetup = Meetup.objects.get(slug=meetup_slug)
    if added == "new":
        return render(
            request,
            "meetups/registration-success.html",
            {"organizer_email": meetup.organizer_email, "added": True},
        )
    else:
        return render(
            request,
            "meetups/registration-success.html",
            {"organizer_email": meetup.organizer_email, "added": False},
        )
