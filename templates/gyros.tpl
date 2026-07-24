All gyros are subject to the following rules:

'''Critical Effects:'''

* HIT 1: The gyro was critically hit, reducing unsteady threshold by 50%
* DESTROYED: The gyro was destroyed, setting unsteady threshold to 0

'''Weight:'''

There are two classes of gyro weight: 

* Flat Weight: This is a static weight per gyro
* Chassis Weight: This is a variable number, rounded to the nearest half-ton, that is a percentage chassis weight. Discrepancies between the data here and in-game can be down to inconsistencies in that rounding and do not need to be reported.

<div class="noresize">
{| class="wikitable sortable"
|+ Comparison of Gyros
|-
! Engine !! Weighting Type !! Weight !! Slots !! Salvageable? || Additional Effects || Community Content || Mech Availability ||
|-
{%- for gyro in gyros.values() %}
| {{ gyro.name }} || {{gyro.weight_type}} || {{gyro.weight_value}} || {{gyro.slots}} || {{gyro.salvageable}}  || {{gyro.effects}} || {{gyro.com_content}} || <div class="toccolours mw-collapsible mw-collapsed">
<div style="font-weight:bold;line-height:1.6;">'''Available From: '''</div>
<div class="mw-collapsible-content">
{% raw %}{{{% endraw %}EquipmentMechs|{{gyro.gyro_ID}}{% raw %}}}{% endraw %}
</div>
|-
{%- endfor %}
|}