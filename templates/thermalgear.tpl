== Thermal Gear ==

Various activatable pods that affect weapon cooling and performance.

<div class="noresize">
{| class="wikitable sortable"
|+ Comparison of Thermal Gear
|-
! gear !! Valid Heat Sinks !! Explosion !! Effects || Community Content || Mech Availability ||
|-
{%- for gear in thermalgear.values() %}
| {{ gear.name }} || {{gear.validity}} || {{gear.explosion}} || {{gear.effects}} || {{gear.com_content}} || <div class="toccolours mw-collapsible mw-collapsed">
<div style="font-weight:bold;line-height:1.6;">'''Available From: '''</div>
<div class="mw-collapsible-content">
{% raw %}{{{% endraw %}EquipmentMechs|{{gear.ID}}{% raw %}}}{% endraw %}
</div>
|-
{%- endfor %}
|}