<div class="noresize">
{| class="wikitable sortable"
|+ Comparison of Cockpits
|-
! Cockpit !! Weight !! Slots !! Location !! Fixed? || Init Bonus || Injuries Resisted || Additional Effects || Community Content || Mech Availability ||
|-
{%- for cockpit in cockpits.values() %}
| {{ cockpit.name }} || {{cockpit.weight}} || {{cockpit.slots}} || {{cockpit.location}} || {{cockpit.fixed}}  || {{cockpit.init}} || {{cockpit.injuries}} || {{cockpit.effects}} || {{cockpit.com_content}} || <div class="toccolours mw-collapsible mw-collapsed">
<div style="font-weight:bold;line-height:1.6;">'''Availble From: '''</div>
<div class="mw-collapsible-content">
{% raw %}{{{% endraw %}EquipmentMechs|{{cockpit.cockpit_ID}}{% raw %}}}{% endraw %}
</div>
|-
{%- endfor %}
|}