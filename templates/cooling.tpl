<div id="" class="" style="clear: right; margin: -1em 0 0 10px; float: right; padding: 10px; background: transparent; width: 220px; ">__TOC__</div>


== E-Cooling ==

E-Cooling is a piece of equipment that represents additional [[Heat Sinks|heat sinks]] added into the engine. [[Engine Cores|Engine cores]] sized 275 or larger can fit E-Cooling up to their limit (see table below). Any suitably sized fusion core can mount any E-Cooling up to its limit or any E-Cooling that fit in smaller brackets, but can't exceed it's allowed size (e.g. the 300 core can mount an E-Cooling +1 or E-Cooling +2, but can't mount a +3 because the engine lacks the space for the extra heat sink). Anything smaller than a 275 engine core cannot mount E-Cooling.

{|class="wikitable"
! Core Size !! E-Cooling
|-
| >275 || None
|-
| 275-295 || +1
|-
| 300-320 || +2
|-
| 325-345 || +3
|-
| 350-370 || +4
|-
| 375-395 || +5
|- 
| 400 || +6 
|}

<div class="noresize">
{| class="wikitable sortable"
|+ Comparison of E-Cooling
|-
! E-Cooling !! Weight !! Effects || Community Content || Mech Availability ||
|-
{%- for ecooling in ecoolings.values() %}
| {{ ecooling.name }} || {{ecooling.weight}} || {{ecooling.effects}} || {{ecooling.com_content}} || <div class="toccolours mw-collapsible mw-collapsed">
<div style="font-weight:bold;line-height:1.6;">'''Availble From: '''</div>
<div class="mw-collapsible-content">
{% raw %}{{{% endraw %}EquipmentMechs|{{ecooling.ecooling_ID}}{% raw %}}}{% endraw %}
</div>
|-
{%- endfor %}
|}