from django.http import JsonResponse
from .models import Campaign, Subscriber

from django.template.loader import render_to_string
import datetime
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings

from rest_framework import generics
from rest_framework.response import Response
from .serializers import SubscriberSerializer
from django.contrib.sites.shortcuts import get_current_site

from concurrent.futures import ThreadPoolExecutor

# Create your views here.


# Handle subscription
class SubscribeView(generics.CreateAPIView):
    queryset = Subscriber.objects.all()  # Get all subscribers from the database
    serializer_class = SubscriberSerializer  # Use the SubscriberSerializer to serialize/deserialize data

    def post(self, request):
        email = request.POST.get("email", None)  # Get the email from the request
        first_name = request.POST.get("first_name", None)  # Get the first name from the request

        if email and first_name:  # Check if both email and first name are provided
            subscriber, created = self.queryset.get_or_create(email=email)  # Get the subscriber with the given email or create a new one
            if created or subscriber.first_name == first_name:  # Check if the subscriber is new or not active
                subscriber.first_name = first_name  # Update the first name of the subscriber
                subscriber.is_active = True  # Activate the subscriber
                subscriber.save()  # Save the changes to the database
                return Response(
                    {
                        "status": "success",
                        "message": "your subscription is activated",
                    }
                )
            else:
                return Response(
                    {
                        "status": "error",
                        "message": "email already in use.",
                    }
                )
        else:
            return Response(
                {
                    "status": "error",
                    "message": "email and first_name parameters are required",
                }
            )



# Handle Unsubscription
class UnsubscribeView(generics.GenericAPIView):
    queryset = Subscriber.objects.all()  # Get all subscribers from the database
    serializer_class = SubscriberSerializer  # Use the SubscriberSerializer to serialize/deserialize data
    lookup_field = ["email", "first_name"]  # Use email and first name as the lookup fields

    # Unsubscribe
    def unsubscribe(self, email, first_name):
        try:
            subscriber = self.queryset.get(email=email, first_name=first_name)  # Get the subscriber with the given email and first name
            subscriber.is_active = False  # Deactivate the subscriber
            subscriber.save()  # Save the changes to the database
            return Response(
                {"status": "success", "message": "Unsubscribed successfully!"}
            )
        except Subscriber.DoesNotExist:
            return Response({"status": "error", "message": "subscriber not found"})

    # Get Method- unsubscribe/?email=email@gmail.com&first_name=moti
    def get(self, request):
        email = request.query_params.get("email", None)  # Get the email from the request
        first_name = request.query_params.get("first_name", None)  # Get the first name from the request

        if email and first_name:  # Check if both email and first name are provided
            return self.unsubscribe(email, first_name)  # Unsubscribe the subscriber
        else:
            return Response(
                {"message": "email and first_name are required"},
            )

    # Post Method
    # For enabling uncomment this
    # def post(self, request):
    #     email = request.POST.get("email", None) # Get the email from the request
    #     first_name = request.POST.get("first_name", None) # Get the first name from the request

    #     if email and first_name:   # Check if both email and first name are provided
    #         return self.unsubscribe(email, first_name)  # Unsubscribe the subscriber
    #     else:
    #         return Response(
    #             {"message": "Email and first_name are required"},
    #         )


# Handle send campaigns

def send_email(campaign, subscriber, current_site):
    email_subject = campaign.subject
    email_from = settings.EMAIL_HOST_USER  # Email of sender

    to_email = subscriber.email  # Email of receiver

    # Render HTML content from a template
    html_content = render_to_string(
        "campaign_template.html",
        {
            "campaign": campaign,
            "domain": current_site,
            "subscriber": subscriber,
            "user_email": subscriber.email,
            "user_name": subscriber.first_name,
        },
    )

    # Create the plaintext version of the email
    text_content = strip_tags(html_content)

    # Create the email object
    email = EmailMultiAlternatives(
        email_subject,
        text_content,
        email_from,
        to=[to_email],
    )

    # Attach the HTML content to the email
    email.attach_alternative(html_content, "text/html")
    # Send email
    email.send()


def send_campaigns(request):
    try:
        campaigns = Campaign.objects.filter(published_date__date=datetime.date.today())  # Get all campaigns published today
        subscribers = Subscriber.objects.filter(is_active=True)  # Get all active subscribers
        current_site = get_current_site(request)  # Get the site url

        with ThreadPoolExecutor() as executor:
            for campaign in campaigns:
                for subscriber in subscribers:
                    executor.submit(send_email, campaign, subscriber, current_site)  # Send email to each subscriber for each campaign using a thread

        # Success message
        return JsonResponse(
            {"status": "success", "message": "emails sent successfully!"}
        )

    # Handle exceptions
    except:
        return JsonResponse({"status": "error", "message": "some error occurred"})
