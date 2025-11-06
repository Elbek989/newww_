from rest_framework import serializers
from .models import Card


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'card_number', 'expire_date', 'card_user']
        extra_kwargs = {
            'card_user': {'read_only': True},
        }

    def validate_expire_date(self, value):

        import re, datetime
        if not re.match(r'^(0[1-9]|1[0-2])\/\d{2}$', value):
            raise serializers.ValidationError("Expire date formati noto‘g‘ri. Masalan: 09/28")

        month, year = map(int, value.split('/'))
        current_year = int(str(datetime.date.today().year)[-2:])
        current_month = datetime.date.today().month
        if (year < current_year) or (year == current_year and month < current_month):
            raise serializers.ValidationError("Kartaning muddati o‘tgan.")
        return value
