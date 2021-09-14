from rest_framework import serializers
from .models import Character, Quote


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = "__all__"


class CharacterSerializer(serializers.ModelSerializer):
    quotes = QuoteSerializer(many=True, read_only=True)

    class Meta:
        model = Character
        fields = [
            "id",
            "name",
            "race",
            "gender",
            "spouse",
            "wiki_url",
            "user",
            "is_favorite",
            "quotes",
        ]
