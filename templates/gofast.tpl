<div id="" class="" style="clear: right; margin: -1em 0 0 10px; float: right; padding: 10px; background: transparent; width: 220px; ">__TOC__</div>

= Myomers = 
<div class="noresize">
{| class="wikitable"
|+ Comparison of Myomers
|-
! Name !! UIName !! Dynamic Slots !! Additional Effects || Community Content || Mech Availability ||
|-
{%- for myomer in myomers.values() %}
| {{ myomer.name }} || {{myomer.UIname}} || {{myomer.slots}} || {{myomer.effects}}  || {{myomer.com_content}} || <div class="toccolours mw-collapsible mw-collapsed">
<div style="font-weight:bold;line-height:1.6;">'''Availble From: '''</div>
<div class="mw-collapsible-content">
{% raw %}{{{% endraw %}EquipmentMechs|{{myomer.myomer_ID}}{% raw %}}}{% endraw %}
</div>
|-
{%- endfor %}
|}

= Superchargers =

<div class="noresize">
{| class="wikitable"
|+ Comparison of Superchargers
|-
! Name !! Dynamic Slots !! Allowed Locations !! Slot Locations !! Explosions !! Additional Effects || Community Content || Mech Availability ||
|-
{%- for supercharger in superchargers.values() %}
| {{ supercharger.name }} || {{supercharger.slots}} || {{supercharger.locations}} || {{supercharger.slot_locations}} || {{supercharger.explosions}} || {{supercharger.effects}}  || {{supercharger.com_content}} || <div class="toccolours mw-collapsible mw-collapsed">
<div style="font-weight:bold;line-height:1.6;">'''Availble From: '''</div>
<div class="mw-collapsible-content">
{% raw %}{{{% endraw %}EquipmentMechs|{{supercharger.supercharger_ID}}{% raw %}}}{% endraw %}
</div>
|-
{%- endfor %}
|}
