from rest_framework import serializers

from .models import Subscriber


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        # fields = "__all__"
        fields = ["email", "first_name"]
