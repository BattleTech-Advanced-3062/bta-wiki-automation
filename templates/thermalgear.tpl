== Thermal Gear ==

Various activatable pods that affect weapon cooling and performance.

<div class="noresize">
{| class="wikitable sortable"
|+ Comparison of Thermal Gear
|-
! Thermal gear !! Weight !! Slots !! Explosion !! Effects || Mech Availability ||
|-
{%- for gear in thermalgear.values() %}
| {{ gear.name }} || {{gear.weight}} || {{gear.slots}}  || {{gear.explosion}} || {{gear.effects}} || <div class="toccolours mw-collapsible mw-collapsed">
<div style="font-weight:bold;line-height:1.6;">'''Available From: '''</div>
<div class="mw-collapsible-content">
{% raw %}{{{% endraw %}EquipmentMechs|{{gear.ID}}{% raw %}}}{% endraw %}
</div>
|-
{%- endfor %}
|}