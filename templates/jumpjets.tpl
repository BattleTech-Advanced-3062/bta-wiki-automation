<div class="noresize">
{| class="wikitable sortable"
|+ Comparison of Jump Jets
|-
! Jump Jet !! Weight !! Slots !! JJ per Hex !! Jump Capacity !! Heat || Min. Tons || Max. Tons || Additional Effects || Community Content || Mech Availability ||
|-
{%- for jumpjet in jumpjets.values() %}
| {{ jumpjet.name }} || {{jumpjet.weight}} || {{jumpjet.slots}} || {{jumpjet.jjph}} || {{jumpjet.capacity}} || {{jumpjet.heat}} || {{jumpjet.min_tons}} || {{jumpjet.max_tons}} || {{jumpjet.effects}} || {{jumpjet.com_content}} || <div class="toccolours mw-collapsible mw-collapsed">
<div style="font-weight:bold;line-height:1.6;">'''Availble From: '''</div>
<div class="mw-collapsible-content">
{% raw %}{{{% endraw %}EquipmentMechs|{{jumpjet.jumpjet_ID}}{% raw %}}}{% endraw %}
</div>
|-
{%- endfor %}
|}