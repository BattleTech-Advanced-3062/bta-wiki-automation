All engines are subject to the following rules:

'''Critical Effects:'''
* HIT 1: Engine damaged, additional 15 heat per turn
* HIT 2: Engine damaged, additional 30 heat per turn
* DESTROYED: Engine destroyed, 'mech is incapacitated
* These hits can occur against any slot in any torso location

'''Minimum Heat Sinks:'''

* All fusion cores require a minimum of 10 [[Heat Sinks|heat sinks]] internally or externally in order for the 'Mech to operate, with extra heat sinks permitted in a 'Mech's potentially in the core itself if it is large enough (see [[E-Cooling]] for more information). 
* The 250 core is the minimum sized core that can mount 10 heat sinks internally. Below this size bracket the core can't fit the minimum number of sinks and requires additional heat sinks to be added to the 'Mech (though these extra sinks don't cost any weight, until you go above 10).
* For more information, see [[Engine Cores]]

<div class="noresize">
{| class="wikitable sortable"
|+ Comparison of Engines
|-
! Engine !! Weight Factor !! CT Slots !! RT Slots !! LT Slots || Fixed? || Additional Effects || Community Content || Mech Availability ||
|-
{%- for engine in engines.values() %}
| {{ engine.name }} || {{engine.weight_factor}} || {{engine.ct_slots}} || {{engine.rt_slots}} || {{engine.lt_slots}}  || {{engine.fixed}}  || {{engine.effects}} || {{engine.com_content}} || <div class="toccolours mw-collapsible mw-collapsed">
<div style="font-weight:bold;line-height:1.6;">'''Availble From: '''</div>
<div class="mw-collapsible-content">
{% raw %}{{{% endraw %}EquipmentMechs|{{engine.engine_ID}}{% raw %}}}{% endraw %}
</div>
|-
{%- endfor %}
|}