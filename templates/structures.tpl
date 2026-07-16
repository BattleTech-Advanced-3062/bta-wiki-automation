Weight Modifier: The amount by which your structure's total weight is adjusted.

Structure Factor: The amount by which your "IN MISSION" structure value of each location is adjusted.

Hybrid Structure Weight: Provides a limited amount of weight savings via fixed Hybrid Structure crits placed around the mech.

<div class="noresize">
{| class="wikitable"
|+ Comparison of Structure Types
|-
! Structure Type !! Weight Modifier !! Structure Factor !! Slots !! Additional Effects || Community Content || Mech Availability ||
|-
{%- for structure in structures.values() %}
| {{ structure.name }} || {{structure.weight_mod}} || {{structure.structure_factor}} || {{structure.slots}} || {{structure.effects}}  || {{structure.com_content}} || <div class="toccolours mw-collapsible mw-collapsed">
<div style="font-weight:bold;line-height:1.6;">'''Available From: '''</div>
<div class="mw-collapsible-content">
{% raw %}{{{% endraw %}EquipmentMechs|{{structure.structure_ID}}{% raw %}}}{% endraw %}
</div>
|-
{%- endfor %}
|}