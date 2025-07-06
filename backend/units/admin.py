from django.contrib import admin
from .models import (
    Faction, Unit, UnitStats, UnitType,
    Keyword, UnitKeyword, Ability,
    Weapon, WeaponKeyword
)

admin.site.register(Faction)
admin.site.register(Unit)
admin.site.register(UnitStats)
admin.site.register(UnitType)
admin.site.register(Keyword)
admin.site.register(UnitKeyword)
admin.site.register(Ability)
admin.site.register(Weapon)
admin.site.register(WeaponKeyword)