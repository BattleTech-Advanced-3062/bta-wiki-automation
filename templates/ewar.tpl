<div id="" class="" style="clear: right; margin: -1em 0 0 10px; float: right; padding: 10px; background: transparent; width: 220px; ">__TOC__</div>

== ECM ==

=== Universal Auras ===

The below units all¹ benefit from the following Auras:

<div class="noresize">
{| class="wikitable "
|+ Aura Descriptions
|-
! Aura !! Range !! Effects 
|-
| C3 Scrambling || 120 || Jams Alpha, Beta, Delta, Gamma and Epsilon C3s, preventing C3 networks from functioning within range
|-
| VRPP Scrambling || 120 || Imposes massive accuracy debuff to VRPP systems
|-
| DroneOS Scrambling || 120 || Imposes massive accuracy debuff to Inner Sphere DroneOS² systems, impedes walk and run speeds
|}

¹ <small>excepting the Experimental EWAR Suite</small>
² <small>note that this ''only'' indicates IS DroneOS systems, currrently only on the Celerity mech

=== Units ===
<div class="noresize">
{| class="wikitable sortable"
|+ Comparison of ECMs
|-
! ECM !! Weight !! Slots !! Salvageable? || Effects || Community Content || Mech Availability 
|-
{%- for ecm in ecms.values() %}
| {{ ecm.name }} || {{ ecm.weight }} || {{ ecm.slots }} || {{ ecm.salvageable }} || {{ecm.effects}} || {{ecm.com_content}} || <div class="toccolours mw-collapsible mw-collapsed">
<div style="font-weight:bold;line-height:1.6;">'''Available From: '''</div>
<div class="mw-collapsible-content">
{% raw %}{{{% endraw %}EquipmentMechs|{{ecm.ecm_ID}}{% raw %}}}{% endraw %}
</div>
|-
{%- endfor %}
|}

== Probes ==

<div class="noresize">
{| class="wikitable sortable"
|+ Comparison of Probes
|-
! Probe !! Weight !! Slots !! Salvageable? || Sensor Range || Sight Range || Probe Heat || Probe Bubble || Effects || Community Content || Mech Availability 
|-
{%- for probe in probes.values() %}
| {{ probe.name }} || {{ probe.weight }} || {{ probe.slots }} || {{ probe.salvageable }} || {{probe.sensor_range}} || {{probe.sight_range}} || {{probe.probe_heat}} || {{probe.probe_bubble}} || {{probe.effects}} || {{probe.com_content}} || <div class="toccolours mw-collapsible mw-collapsed">
<div style="font-weight:bold;line-height:1.6;">'''Available From: '''</div>
<div class="mw-collapsible-content">
{% raw %}{{{% endraw %}EquipmentMechs|{{probe.probe_ID}}{% raw %}}}{% endraw %}
</div>
|-
{%- endfor %}
|}