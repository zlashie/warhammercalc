from django.db import models

class Faction(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name

class Unit(models.Model):
    faction = models.ForeignKey(Faction, on_delete=models.CASCADE)
    name = models.TextField()
    models_pr_unit = models.TextField()

    class Meta:
        unique_together = ('name', 'faction')

class UnitStats(models.Model):
    unit = models.OneToOneField(Unit, on_delete=models.CASCADE, primary_key=True)
    movement = models.IntegerField(null=True)
    toughness = models.IntegerField(null=True)
    save = models.IntegerField(null=True)
    wounds = models.IntegerField(null=True)
    leadership = models.IntegerField(null=True)
    objective_control = models.IntegerField(null=True)
    invulnerable_save = models.IntegerField(null=True)
    feel_no_pain = models.IntegerField(null=True)

class UnitType(models.Model):
    unit = models.OneToOneField(Unit, on_delete=models.CASCADE, primary_key=True)
    character = models.BooleanField(default=False)
    vehicle = models.BooleanField(default=False)
    infantry = models.BooleanField(default=False)
    monster = models.BooleanField(default=False)
    battleline = models.BooleanField(default=False)
    epic_hero = models.BooleanField(default=False)
    fly = models.BooleanField(default=False)

class Keyword(models.Model):
    name = models.TextField(unique=True)

class UnitKeyword(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('unit', 'keyword')

class Ability(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    name = models.TextField()

    class Meta:
        unique_together = ('unit', 'name')

class Weapon(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    name = models.TextField()
    range = models.IntegerField(null=True)
    range_type = models.TextField(choices=[('melee', 'melee'), ('ranged', 'ranged')])
    attacks = models.IntegerField(null=True)
    ballistic_skill = models.IntegerField(null=True)
    weapon_skill = models.IntegerField(null=True)
    strength = models.IntegerField(null=True)
    ap = models.IntegerField(null=True)
    damage = models.TextField()

    class Meta:
        unique_together = ('unit', 'name')

class WeaponKeyword(models.Model):
    weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('weapon', 'keyword')
