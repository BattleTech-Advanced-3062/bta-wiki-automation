=== Armor Table ===

Activatable: Effects can be toggled off and on again.

Weight Modifier: The amount by which your armour's total weight is adjusted.

Armor Factor: The amount by which your "IN MISSION" armour value of each location is adjusted.

Reserved Critical Slots: How many Critical Location Slots the armour takes up.

CASE/CASE II/SHIELD: Includes the respective gear in every location, number following it is how much an explosion's damage is reduced to.

KineticProtection: Alters the damage by missiles and autocannons by the indicated amount

EnergyProtection: Alters the damage by lasers by the indicated amount
<div class="noresize">
{| class="wikitable"
|+ Comparison of Armor Types
|-
! Armor Type !! Weight Modifier !! Armor Factor !! Reserved Critical Slots !! Additional Effects || Community Content || Mech Availability ||
|-
{%- for armor in armors.values() %}
| {{ armor.name }} || {{armor.weight_mod}} || {{armor.armor_factor}} || {{armor.crit_slots}} || {{armor.effects}}  || {{armor.com_content}} || <div class="toccolours mw-collapsible mw-collapsed">
<div style="font-weight:bold;line-height:1.6;">'''Availble From: '''</div>
<div class="mw-collapsible-content">
{% raw %}{{{% endraw %}EquipmentMechs|{{armor.armor_ID}}{% raw %}}}{% endraw %}
</div>
|-
{%- endfor %}
|}
