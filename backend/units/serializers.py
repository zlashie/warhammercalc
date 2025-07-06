### Dependencies
from rest_framework import serializers
from .models import (
    Faction, Unit, UnitStats, UnitType, Keyword,
    UnitKeyword, Ability, Weapon, WeaponKeyword
)

### Serializer Classes
class FactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faction
        fields = '__all__'

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'

class UnitStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitStats
        fields = '__all__'

class UnitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitType
        fields = '__all__'

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = '__all__'

class UnitKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitKeyword
        fields = '__all__'

class AbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ability
        fields = '__all__'

class WeaponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weapon
        fields = '__all__'

class WeaponKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeaponKeyword
        fields = '__all__'
