### Dependencies
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    FactionViewSet, UnitViewSet, UnitStatsViewSet, UnitTypeViewSet,
    KeywordViewSet, UnitKeywordViewSet, AbilityViewSet,
    WeaponViewSet, WeaponKeywordViewSet
)

### Routers
router = DefaultRouter()
router.register(r'factions', FactionViewSet)
router.register(r'units', UnitViewSet)
router.register(r'unitstats', UnitStatsViewSet)
router.register(r'unitypes', UnitTypeViewSet)
router.register(r'keywords', KeywordViewSet)
router.register(r'unitkeywords', UnitKeywordViewSet)
router.register(r'abilities', AbilityViewSet)
router.register(r'weapons', WeaponViewSet)
router.register(r'weaponkeywords', WeaponKeywordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]