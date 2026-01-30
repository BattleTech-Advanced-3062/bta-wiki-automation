{%- for category, groups in categories.items() %}
== {{ category }} ==

{#- ---------------- NON-MODE WEAPONS (single table) ---------------- #}
{%- if groups["non_modes"] %}
<div class="noresize">
{| class="wikitable"
!
!
!
! colspan="2" |Tonnage/Size
! colspan="3" |Damage
! colspan="4" |Per salvo
! colspan="3" |Modifiers
! colspan="5" |Range
!
!
|-
!<small>Name</small>
!<small>Ammo</small>
!<small>Hardpoint</small>
!<small>Tonnage</small>
!<small>Slots</small>
!<small>Normal</small>
!<small>Heat</small>
!<small>Stab</small>
!<small>Shots</small>
!<small>Projectiles</small>
!<small>Heat</small>
!<small>Recoil</small>
!<small>Accuracy</small>
!<small>Evasion Ignored</small>
!<small>Bonus Crit Chance</small>
!<small>Min</small>
!<small>Short</small>
!<small>Medium</small>
!<small>Long</small>
!<small>Max</small>
!<small>Fires In Melee</small>
!<small>Additional Info</small>
|-
{%- for weapon in groups["non_modes"].values() %}
| {{ weapon.name }}
| {{ weapon.ammo }}
| {{ weapon.hardpoint }}
| {{ weapon.tonnage }}
| {{ weapon.slots }}
| {{ weapon.damage }}
| {{ weapon.heatdamage }}
| {{ weapon.instability }}
| {{ weapon.shots }}
| {{ weapon.projectiles }}
| {{ weapon.heat }}
| {{ weapon.recoil }}
| {{ weapon.accuracy }}
| {{ weapon.evasionignored }}
| {{ weapon.bonuscritchance }}
| {{ weapon.rangemin }}
| {{ weapon.rangeshort }}
| {{ weapon.rangemedium }}
| {{ weapon.rangelong }}
| {{ weapon.rangemax }}
| {{ weapon.firesinmelee }}
| <div style="max-height: 100px; overflow-y: scroll;">{{ weapon.additionalinfo }}</div>
|-
{%- endfor %}
|}
</div>
{%- endif %}
{#- ---------------- MODE WEAPONS (tabs per mode, rows per weapon) ---------------- #}
{%- if groups["modes"] %}

<tabs>
{%- for mode_name, weapons in groups["modes"].items() %}
<tab name="{{ mode_name }}">

{| class="wikitable"
!
!
!
! colspan="2" |Tonnage/Size
! colspan="3" |Damage
! colspan="4" |Per salvo
! colspan="3" |Modifiers
! colspan="5" |Range
!
!
|-
!<small>Name</small>
!<small>Ammo</small>
!<small>Hardpoint</small>
!<small>Tonnage</small>
!<small>Slots</small>
!<small>Normal</small>
!<small>Heat</small>
!<small>Stab</small>
!<small>Shots</small>
!<small>Projectiles</small>
!<small>Heat</small>
!<small>Recoil</small>
!<small>Accuracy</small>
!<small>Evasion Ignored</small>
!<small>Bonus Crit Chance</small>
!<small>Min</small>
!<small>Short</small>
!<small>Medium</small>
!<small>Long</small>
!<small>Max</small>
!<small>Fires In Melee</small>
!<small>Additional Info</small>

{%- for weapon in weapons.values() %}
{%- set mode = weapon.active_mode %}
|-
| {{ weapon.name }}
| {{ weapon.ammo }}
| {{ weapon.hardpoint }}
| {{ weapon.tonnage }}
| {{ weapon.slots }}
| {{ weapon.damage + (mode.DamagePerShot | default(0)) | int }}
| {{ weapon.heatdamage + (mode.HeatDamage | default(0)) | int }}
| {{ weapon.instability + (mode.Instability | default(0)) | int }}
| {{ weapon.shots + (mode.ShotsWhenFired | default(0)) | int }}
| {{ weapon.projectiles + (mode.ProjectilesPerShot | default(0)) | int }}
| {{ weapon.heat + (mode.HeatGenerated | default(0)) | int }}
| {{ weapon.recoil + (mode.RefireModifier | default(0)) | int }}
| {{ weapon.accuracy + (mode.AccuracyModifier | default(0)) | int }}
| {{ weapon.evasionignored + (mode.EvasivePipsIgnored | default(0)) | int }}
| {{ weapon.bonuscritchance + (mode.CriticalChanceMultiplier | default(0)) | int }}
| {{ weapon.rangemin + (mode.MinRange | default(0)) | int }}
| {{ weapon.rangeshort + (mode.ShortRange | default(0)) | int }}
| {{ weapon.rangemedium + (mode.MediumRange | default(0)) | int }}
| {{ weapon.rangelong + (mode.LongRange | default(0)) | int }}
| {{ weapon.rangemax + (mode.MaxRange | default(0)) | int }}
| {{ weapon.firesinmelee }}
| <div style="max-height: 100px; overflow-y: scroll;">{{ weapon.additionalinfo }}</div>
{%- endfor %}
|}

</tab>
{%- endfor %}
</tabs>

{%- endif %}

<div class="toccolours mw-collapsible">
<div style="font-weight:bold;line-height:1.6;">'''Found On These 'Mechs: (Click Expand For List)'''</div>
<div class="mw-collapsible-content">
{%- for weapon in groups["modes"].values() %}
<div class="toccolours mw-collapsible mw-collapsed">
<div style="font-weight:bold;line-height:1.6;">{{ weapon.name }}</div>
<div class="mw-collapsible-content">
Gear ID: ''{{weapon.filepath}}''
{% raw %}{{{% endraw %}EquipmentMechs|{{weapon.filepath}}{% raw %}}}{% endraw %}
</div></div>
{%- endfor %}
{%- for weapon in groups["non_modes"].values() %}
<div class="toccolours mw-collapsible mw-collapsed">
<div style="font-weight:bold;line-height:1.6;">{{ weapon.name }}</div>
<div class="mw-collapsible-content">
Gear ID: ''{{weapon.filepath}}''
{% raw %}{{{% endraw %}EquipmentMechs|{{weapon.filepath}}{% raw %}}}{% endraw %}
</div></div>
{%- endfor %}
</div></div>
{%- endfor %}
