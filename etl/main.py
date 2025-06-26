from helper_functions.get_unit_stats import get_unit_stats
from helper_functions.get_weapons_for_unit import get_weapons_for_unit

url = "https://raw.githubusercontent.com/BSData/wh40k-10e/main/Imperium%20-%20Space%20Marines.cat"
unit_name = "Assault Intercessors with Jump Packs"

unit_stats = get_unit_stats(url, unit_name)
weapon_profiles = get_weapons_for_unit(url, unit_name)

# Display
if unit_stats:
    print(f"📊 Unit Stats for '{unit_stats.name}':\n")
    print(f"🔹 M: {unit_stats.movement}")
    print(f"🔹 T: {unit_stats.toughness}")
    print(f"🔹 SV: {unit_stats.save}")
    print(f"🔹 W: {unit_stats.wounds}")
    print(f"🔹 LD: {unit_stats.leadership}")
    print(f"🔹 OC: {unit_stats.oc}")
else:
    print("❌ Unit stats not found.")

print("\n🔫 Weapons:")
if weapon_profiles:
    for wp in weapon_profiles:
        print(f"\n🔸 {wp.name}")
        if wp.range: print(f"   Range: {wp.range}")
        if wp.attacks: print(f"   A: {wp.attacks}")
        if wp.ws: print(f"   WS: {wp.ws}")
        if wp.bs: print(f"   BS: {wp.bs}")
        if wp.strength: print(f"   S: {wp.strength}")
        if wp.ap: print(f"   AP: {wp.ap}")
        if wp.damage: print(f"   D: {wp.damage}")
        if wp.keywords: print(f"   Keywords: {wp.keywords}")
else:
    print("❌ No weapons found.")
