from rest_framework import serializers
from polls.models import Color


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('color_id_hex', 'color_name')