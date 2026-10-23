# report_rules.py — the knowledge base. Domain vocabulary lives here and only here.

MATERIALS = {"stone", "ceramic", "metal", "wood", "textile"}
DAMAGE = {"crack", "loose_base", "fading", "rot", "corrosion"}
SEVERITIES = {"none", "minor", "major"}

def rule(conclusion, *premises):
    return (frozenset(premises), conclusion)

CLAUSES = [
    # material classes
    rule("inorganic", "material_stone"),
    rule("inorganic", "material_ceramic"),
    rule("inorganic", "material_metal"),
    rule("organic", "material_wood"),
    rule("organic", "material_textile"),
    # any damage type counts as damage
    *[rule("has_damage", f"damage_{d}") for d in sorted(DAMAGE)],
    # derived concept
    rule("structural_risk", "damage_crack", "damage_loose_base"),
    # integrity constraints: a conclusion starting with "invalid:" is a violation
    rule("invalid:rot_on_inorganic", "damage_rot", "inorganic"),
    rule("invalid:corrosion_on_organic", "damage_corrosion", "organic"),
    rule("invalid:none_but_damaged", "severity_none", "has_damage"),
    rule("invalid:structural_risk_marked_minor", "structural_risk", "severity_minor"),
    #2 additional rules (disabled now)
    #rule("invalid:corrosion_on_ceramic", "material_ceramic", "damage_corrosion"),
    #rule("invalid:wood_rot_crack_marked_minor", "material_wood","damage_rot", "damage_crack", "severity_minor"),
]
