from wisenations import SheetManager

sm = SheetManager()
sm.new_sheet("s1")
my_sheet = sm.get_sheet("s1")

my_stats = {
    # Primary Attributes (Base stats)
    "strength": "280",               # Physical power and carrying capacity
    "agility": "450",                # Speed, reflexes, and precision
    "intelligence": "210",           # Magical prowess and mental acuity
    "vitality": "320",               # Endurance and health
    "wisdom": "190",                 # Intuition, mana efficiency, and perception
    "luck": "160",                   # Chance-based effects and loot quality

    # Secondary Attributes (Derived from primaries)
    "endurance": "vitality * 0.8 + strength * 0.4",       # Stamina for sustained actions
    "dexterity": "agility * 0.7 + luck * 0.2",           # Fine motor skills and crit synergy
    "focus": "intelligence * 0.6 + wisdom * 0.5",         # Spell accuracy and mental resilience
    "resilience": "vitality * 0.5 + wisdom * 0.3",        # Resistance to debuffs and crowd control

    # Combat Stats
    "physical_damage": "strength * 2.0 + dexterity * 0.5 + agility * 0.2",  # Melee/ranged damage
    "magic_damage": "intelligence * 2.5 + focus * 0.8 + wisdom * 0.3",      # Spell damage
    "attack_speed": "agility * 0.006 + dexterity * 0.002 + 0.8",            # Attacks per second
    "critical_chance": "dexterity * 0.06 + luck * 0.03 + agility * 0.01",   # % crit chance
    "critical_damage": "2.0 + luck * 0.008 + intelligence * 0.002",         # Crit multiplier
    "armor_penetration": "strength * 0.3 + dexterity * 0.2",                # % armor ignored
    "spell_penetration": "intelligence * 0.4 + focus * 0.15",               # % magic resist ignored

    # Defensive Stats
    "max_health": "vitality * 18 + strength * 6 + endurance * 2",           # Total HP
    "health_regen": "vitality * 0.25 + resilience * 0.15 + 8",              # HP per second
    "max_mana": "intelligence * 10 + wisdom * 5 + focus * 2",              # Total mana
    "mana_regen": "wisdom * 0.2 + intelligence * 0.1 + focus * 0.05 + 4",   # Mana per second
    "armor": "strength * 1.2 + vitality * 0.6 + endurance * 0.3",           # Physical damage reduction
    "magic_resist": "intelligence * 0.8 + wisdom * 0.5 + resilience * 0.2", # Magic damage reduction
    "dodge_chance": "agility * 0.04 + dexterity * 0.02 + luck * 0.01",      # % chance to dodge
    "block_chance": "strength * 0.03 + endurance * 0.02 + vitality * 0.01", # % chance to block
    "block_amount": "armor * 0.4 + strength * 0.5",                         # Damage reduced on block

    # Utility and Exploration Stats
    "movement_speed": "120 + agility * 0.5 + dexterity * 0.1",              # Base speed + bonuses
    "stamina": "endurance * 10 + vitality * 3 + strength * 1",             # Sprinting/action resource
    "stamina_regen": "endurance * 0.3 + agility * 0.1 + 5",                # Stamina per second
    "perception": "wisdom * 0.9 + luck * 0.3 + intelligence * 0.2",        # Detect traps/hidden items
    "stealth": "agility * 0.7 + dexterity * 0.4 + luck * 0.1",             # Reduced enemy detection
    "loot_quality": "luck * 0.05 + wisdom * 0.02 + perception * 0.01",     # % bonus to loot drops
    "cooldown_reduction": "intelligence * 0.03 + wisdom * 0.02 + focus * 0.01",  # % reduction in ability CDs

    # Conditional Modifiers (Complex formulas with caps or diminishing returns)
    "melee_bonus": "strength * 0.5 + physical_damage * 0.2",     # Bonus melee damage, capped at 200
    "spell_efficiency": "1.0 - wisdom * 0.002 + focus * 0.001", # % reduction in mana costs
    "lifesteal": "critical_chance * 0.3 + luck * 0.02",           # % HP gained on hit, capped at 15%
    "mana_surge": "intelligence * 0.1 + focus * 0.05",            # Bonus mana on ability use
    "debuff_resistance": "resilience * 0.4 + vitality * 0.1 + wisdom * 0.05", # % reduced debuff duration
}

my_sheet.add_stats(my_stats)
print(f"{my_sheet.solve_expressions()=}")