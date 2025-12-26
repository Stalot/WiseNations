from wisenations import SheetManager
from pprint import pprint as pp

sm = SheetManager()
sm.new_sheet("s1")
my_sheet = sm.get_sheet("s1")

my_stats = {
    "force": "250",
    "agility": "420",
    "intelligence": "180",
    "vitality": "300",
    "luck": "150",
    "attack_speed": "agility * 0.5",
    "physical_damage": "force * 1.8 + agility * 0.3",
    "critical_chance": "agility * 0.05 + luck * 0.02",
    "critical_damage": "1.5 + luck * 0.005",
    "magic_damage": "intelligence * 2.2",
    "max_health": "vitality * 15 + force * 5",
    "health_regen": "vitality * 0.2 + 5",
    "max_mana": "intelligence * 8 + vitality * 2",
    "mana_regen": "intelligence * 0.15 + 3",
    "dodge_chance": "agility * 0.03 + luck * 0.01",
    "armor": "force * 0.8 + vitality * 0.4",
    "magic_resist": "intelligence * 0.6 + vitality * 0.3",
    "movement_speed": "100 + agility * 0.4",
}

my_stats = {
    "hp": "200",
    "speed": "10",
    "damage": '30',
    "attack_speed": "speed * 2.5"
}
my_sheet.add_stats(my_stats)
pp(my_sheet.get_all_stats())