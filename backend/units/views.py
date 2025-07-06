### Dependencies 
from rest_framework import viewsets
from .models import (
    Faction, Unit, UnitStats, UnitType, Keyword,
    UnitKeyword, Ability, Weapon, WeaponKeyword
)
from .serializers import (
    FactionSerializer, UnitSerializer, UnitStatsSerializer, UnitTypeSerializer,
    KeywordSerializer, UnitKeywordSerializer, AbilitySerializer,
    WeaponSerializer, WeaponKeywordSerializer
)

### View Classes
class FactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Faction.objects.all()
    serializer_class = FactionSerializer

class UnitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

class UnitStatsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UnitStats.objects.all()
    serializer_class = UnitStatsSerializer

class UnitTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UnitType.objects.all()
    serializer_class = UnitTypeSerializer

class KeywordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer

class UnitKeywordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UnitKeyword.objects.all()
    serializer_class = UnitKeywordSerializer

class AbilityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ability.objects.all()
    serializer_class = AbilitySerializer

class WeaponViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Weapon.objects.all()
    serializer_class = WeaponSerializer

class WeaponKeywordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WeaponKeyword.objects.all()
    serializer_class = WeaponKeywordSerializer
