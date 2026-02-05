{{ '{{' }}InfoboxPilot
|callsign = {{callsign}}
|pilotimage = Pilot {{callsign}}.png
|pilotname = {{firstname}} {{lastname}}
|age = {{age}}
|gender = {{gender}}
|faction = {{faction}}
|health = {{health}}
|gunnery = {{gunnery}}
|piloting = {{piloting}}
|guts = {{guts}}
|tactics = {{tactics}}
{% if multitarget is defined%}|{{multitarget}} = yes{% else %}{% endif %}
{% if battlelord is defined%}|{{battlelord}} = yes{% else %}{% endif %}
{% if precisionmaster is defined%}|{{precisionmaster}} = yes{% else %}{% endif %}
{% if ballisticmaster is defined%}|{{ballisticmaster}} = yes{% else %}{% endif %}
{% if energymaster is defined%}|{{energymaster}} = yes{% else %}{% endif %}
{% if missilemaster is defined%}|{{missilemaster}} = yes{% else %}{% endif %}
{% if stonecold is defined%}|{{stonecold}} = yes{% else %}{% endif %}
{% if surefooting is defined%}|{{surefooting}} = yes{% else %}{% endif %}
{% if phantom is defined%}|{{phantom}} = yes{% else %}{% endif %}
{% if acepilot is defined%}|{{acepilot}} = yes{% else %}{% endif %}
{% if invisibletarget is defined%}|{{invisibletarget}} = yes{% else %}{% endif %}
{% if sprinter is defined%}|{{sprinter}} = yes{% else %}{% endif %}
{% if bulwark is defined%}|{{bulwark}} = yes{% else %}{% endif %}
{% if shieldedstance is defined%}|{{shieldedstance}} = yes{% else %}{% endif %}
{% if juggernaut is defined%}|{{juggernaut}} = yes{% else %}{% endif %}
{% if brawler is defined%}|{{brawler}} = yes{% else %}{% endif %}
{% if defensiveformation is defined%}|{{defensiveformation}} = yes{% else %}{% endif %}
{% if sensorlock is defined%}|{{sensorlock}} = yes{% else %}{% endif %}
{% if targetprediction is defined%}|{{targetprediction}} = yes{% else %}{% endif %}
{% if mastertactician is defined%}|{{mastertactician}} = yes{% else %}{% endif %}
{% if knifefighter is defined%}|{{knifefighter}} = yes{% else %}{% endif %}
{% if eagleeye is defined%}|{{eagleeye}} = yes{% else %}{% endif %}
{% if intensifyfirepower is defined%}|{{intensifyfirepower}} = yes{% else %}{% endif %}
{% if perfecttargeting is defined%}|{{perfecttargeting}} = yes{% else %}{% endif %}
{% if overwhelmingaggression is defined%}|{{overwhelmingaggression}} = yes{% else %}{% endif %}
{% if sideslip is defined%}|{{sideslip}} = yes{% else %}{% endif %}
{% if streetracer is defined%}|{{streetracer}} = yes{% else %}{% endif %}
{% if spotter is defined%}|{{spotter}} = yes{% else %}{% endif %}
{% if redundantcomponents is defined%}|{{redundantcomponents}} = yes{% else %}{% endif %}
{% if bruteforce is defined%}|{{bruteforce}} = yes{% else %}{% endif %}
{% if hulldown is defined%}|{{hulldown}} = yes{% else %}{% endif %}
{% if sensorsweep is defined%}|{{sensorsweep}} = yes{% else %}{% endif %}
{% if targetpainting is defined%}|{{targetpainting}} = yes{% else %}{% endif %}
{% if commandandcontrol is defined%}|{{commandandcontrol}} = yes{% else %}{% endif %}
{{pilottags}}
{{ '}}' }}


===Biography:===
{% if biography %}
{{ biography }}
{% else %}
None
{% endif -%}


===Bonuses:===
====Custom Abilities====
{% if custom_ability_name is defined%}
'''Passive Bonus''': {{ custom_ability_name }}

{{custom_ability_details}}

{% else %}
None
{% endif -%}


====Custom Affinties====
{% if custom_affinity_info is defined%}
{% for key, value in custom_affinity_info.items() %}
'''Mech Affinity''': {{ value.chassis_names }} - {{ key }}

(Enabled after {{ value.missions_required }} missions in the mech)

{{ value.description }}

{% endfor %}

{% else %}
None
{% endif -%}


===Availability:===
{% if availability is defined%}
{{ availability }}
{% else %}
Can be found as a random starting pilot or in hiring halls. 
{% endif %}

[[Category:Pilots]]
