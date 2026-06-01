<div id="" class="" style="clear: right; margin: -1em 0 0 10px; float: right; padding: 10px; background: transparent; width: 220px; ">__TOC__</div>

== Heat Sink Kits ==

A 'Mech's cooling system provides heat dissipation for components inside the mech and compatible extension points for additional heat sinks throughout the mech. The equipped kit determines what type of heat sinks you can fit in the 'mech.

<div class="noresize">
{| class="wikitable sortable"
|+ Comparison of Heat Sink Kits
|-
! Kit !! Valid Heat Sinks !! Explosion !! Effects || Community Content || Mech Availability ||
|-
{%- for kit in kits.values() %}
| {{ kit.name }} || {{kit.validity}} || {{kit.explosion}} || {{kit.effects}} || {{kit.com_content}} || <div class="toccolours mw-collapsible mw-collapsed">
<div style="font-weight:bold;line-height:1.6;">'''Availble From: '''</div>
<div class="mw-collapsible-content">
{% raw %}{{{% endraw %}EquipmentMechs|{{kit.ID}}{% raw %}}}{% endraw %}
</div>
|-
{%- endfor %}
|}

== Heat Sinks ==

Heat Sinks actively expel thermal energy generated from firing weaponry or other sources, preventing damage from excessive heat buildup. Their effectiveness can be impacted by the surrounding environment, positively or negatively.

<div class="noresize">
{| class="wikitable sortable"
|+ Comparison of Heat Sinks
|-
! Heat Sink !! Weight !! Slots !! Dissipation !! Explosion !! Effects || Community Content || Mech Availability ||
|-
{%- for heatsink in heatsinks.values() %}
| {{ heatsink.name }} || {{heatsink.weight}} || {{heatsink.slots}} ||{{heatsink.dissipation}} || {{heatsink.explosion}} || {{heatsink.effects}} || {{heatsink.com_content}} || <div class="toccolours mw-collapsible mw-collapsed">
<div style="font-weight:bold;line-height:1.6;">'''Availble From: '''</div>
<div class="mw-collapsible-content">
{% raw %}{{{% endraw %}EquipmentMechs|{{heatsink.ID}}{% raw %}}}{% endraw %}
</div>
|-
{%- endfor %}
|}

== Exchangers ==

Thermal Exchangers reduce the overall heat generated from weapon attacks by a fixed percentage. Unlike Heat Sink components, Thermal Exchangers are not impacted by the surrounding environment.

<div class="noresize">
{| class="wikitable sortable"
|+ Comparison of Exchangers
|-
! Exchanger !! Weight !! Slots || Stackable || Effects ||Community Content ||  Mech Availability ||
|-
{%- for exchanger in exchangers.values() %}
| {{ exchanger.name }} || {{exchanger.weight}} || {{exchanger.slots}} || {{exchanger.stackable}} || {{exchanger.effects}} || {{exchanger.com_content}} || <div class="toccolours mw-collapsible mw-collapsed">
<div style="font-weight:bold;line-height:1.6;">'''Availble From: '''</div>
<div class="mw-collapsible-content">
{% raw %}{{{% endraw %}EquipmentMechs|{{exchanger.ID}}{% raw %}}}{% endraw %}
|-
{%- endfor %}
|}

=== Heat Exchanger Efficiency ===
In a heat neutral biome (Highlands/Lowlands) the equivalent weight of double heat sinks are more efficient cooling per ton than heat exchangers until the amount of heat generated becomes greater than 120 at which point it's more efficient to fit the exchangers (e.g. a 'Mech producing 110 heat in a Highlands biome will get more value out of 2 double heat sinks than it will fitting an exchanger). As the tonnage and effectiveness of exchangers scales linearly this is true regardless of what type of exchanger you have. What this means is, as a rule of thumb if it produces more than 120 heat adding an exchanger will be beneficial in the majority of biomes (6 out of 9).

The table below lists the amount of heat in each biome you need to be generating in a 'Mech in order for exchangers to be more efficient than the equivalent weight of DHS and therefore worth fitting. Depending on how much space you have available, in colder biomes (especially Polar) where heat sinks become even more efficient it might actually be worth removing the exchangers from your 'Mechs in favour of more sinks.

{| class="wikitable"
! Biome !! Heat Effect !! Heat Threshold
|-
| Lunar || +35% || >78
|-
| Martian || +25% || >90
|-
| Badlands  || +15% || >102
|-
| Desert || +15% || >102
|-
| Highlands || 0% || >120
|-
| Lowlands || 0% || >120
|-
| Jungle || -10% || >132
|-
| Tundra || -15% || >138
|-
| Polar || -20% || >144
|}

== Heat Banks ==

Heat Banks are installed to allow for more thermal energy venting. However, where standard heat sinks rely on coolants (which have varied effectiveness in different environments) heat banks do not. They simply collect and expel heat automatically, though only in certain increments. What this means is that, while their effect doesn't get accounted for by a mech's cooling systems, they always vent off their collected heat regardless of environments. This trait makes Heat Banks invaluable in extremely hazardous environments such as Martian or Lunar settings. 

<div class="noresize">
{| class="wikitable sortable"
|+ Comparison of Heat Banks
|-
! Bank !! Weight !! Slots || Stackable || Effects ||Community Content || Mech Availability ||
|-
{%- for bank in banks.values() %}
| {{ bank.name }} || {{bank.weight}} || {{bank.slots}} || {{bank.stackable}} || {{bank.effects}} || {{bank.com_content}} || <div class="toccolours mw-collapsible mw-collapsed">
<div style="font-weight:bold;line-height:1.6;">'''Availble From: '''</div>
<div class="mw-collapsible-content">
{% raw %}{{{% endraw %}EquipmentMechs|{{bank.ID}}{% raw %}}}{% endraw %}
</div>
|-
{%- endfor %}
|}

== E-Cooling ==

<div class="noresize">
{| class="wikitable sortable"
|+ Comparison of E-Cooling
|-
! E-Cooling !! Weight !! Minimum Engine Size !! Effects || Community Content || Mech Availability ||
|-
{%- for ecooling in ecoolings.values() %}
| {{ ecooling.name }} || {{ecooling.weight}} || {{ecooling.engine_size}} || {{ecooling.effects}} || {{ecooling.com_content}} ||<div class="toccolours mw-collapsible mw-collapsed">
<div style="font-weight:bold;line-height:1.6;">'''Availble From: '''</div>
<div class="mw-collapsible-content">
{% raw %}{{{% endraw %}EquipmentMechs|{{ecooling.ID}}{% raw %}}}{% endraw %}
</div>
|-
{%- endfor %}
|}