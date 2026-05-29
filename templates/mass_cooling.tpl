<div id="" class="" style="clear: right; margin: -1em 0 0 10px; float: right; padding: 10px; background: transparent; width: 220px; ">__TOC__</div>


== E-Cooling ==

E-Cooling is a piece of equipment that represents additional [[Heat Sinks|heat sinks]] added into the engine. [[Engine Cores|Engine cores]] sized 275 or larger can fit E-Cooling up to their limit (see table below). Any suitably sized fusion core can mount any E-Cooling up to its limit or any E-Cooling that fit in smaller brackets, but can't exceed it's allowed size (e.g. the 300 core can mount an E-Cooling +1 or E-Cooling +2, but can't mount a +3 because the engine lacks the space for the extra heat sink). Anything smaller than a 275 engine core cannot mount E-Cooling.

<div class="noresize">
{| class="wikitable sortable"
|+ Comparison of E-Cooling
|-
! E-Cooling !! Weight !! Effects || Community Content || 
|-
{%- for ecooling in ecoolings.values() %}
| {{ ecooling.name }} || {{ecooling.weight}} || {{ecooling.effects}} || {{ecooling.com_content}} ||
|-
{%- endfor %}
|}

== Exchangers ==

Thermal Exchangers reduce the overall heat generated from weapon attacks by a fixed percentage. Unlike Heat Sink components, Thermal Exchangers are not impacted by the surrounding environment.

<div class="noresize">
{| class="wikitable sortable"
|+ Comparison of Exchangers
|-
! Exchanger !! Weight !! Effects || Community Content || 
|-
{%- for ecooling in ecoolings.values() %}
| {{ exchanger.name }} || {{exchanger.weight}} || {{exchanger.effects}} || {{exchanger.com_content}} ||
|-
{%- endfor %}
|}