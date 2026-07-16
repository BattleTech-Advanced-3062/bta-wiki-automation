{| class="wikitable sortable"
|+ Comparison of Actuators
|-
! Actuator !! Location !! Allowed Location !! Slots !! Weight !! Salvageable? !! Additional Bonuses !! Community Content !! Mech Availability 	
|-
{%- for actuator in actuators.values() %}
| {{ actuator.name }} || {{actuator.location}} || {{actuator.allowed}} || {{actuator.slots}} || {{actuator.weight}} || {{actuator.salvageable}} || {{actuator.effects}} || {{actuator.com_content}} || <div class="toccolours mw-collapsible mw-collapsed">
<div style="font-weight:bold;line-height:1.6;">'''Available From: '''</div>
<div class="mw-collapsible-content">
{% raw %}{{{% endraw %}EquipmentMechs|{{actuator.actuator_ID}}{% raw %}}}{% endraw %}
</div>
|-
{%- endfor %}
|}