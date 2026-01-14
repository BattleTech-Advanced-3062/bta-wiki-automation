{%- for category, groups in categories.items() %}

<div class="noresize">
== {{ category }} ==
</div>

{# ============================================================
   NON-MODE WEAPONS (ONE TABLE)
   ============================================================ #}
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
|{{ weapon.name }}
|{{ weapon.ammo }}
|{{ weapon.hardpoint }}
|{{ weapon.tonnage }}
|{{ weapon.slots }}
|{{ weapon.damage }}
|{{ weapon.heatdamage }}
|{{ weapon.instability }}
|{{ weapon.shots }}
|{{ weapon.projectiles }}
|{{ weapon.heat }}
|{{ weapon.recoil }}
|{{ weapon.accuracy }}
|{{ weapon.evasionignored }}
|{{ weapon.bonuscritchance }}
|{{ weapon.rangemin }}
|{{ weapon.rangeshort }}
|{{ weapon.rangemedium }}
|{{ weapon.rangelong }}
|{{ weapon.rangemax }}
|{{ weapon.firesinmelee }}
|{{ weapon.additionalinfo }}
|-
{%- endfor %}
|}
</div>
{%- for weapon in groups["non_modes"].values() %}
<div class="toccolours mw-collapsible">
<div style="font-weight:bold;line-height:1.6;">'''Found On These 'Mechs: (Click Expand For List)'''</div>
<div class="mw-collapsible-content">

<div class="toccolours mw-collapsible mw-collapsed">
<div style="font-weight:bold;line-height:1.6;">{{weapon.name}}</div>
<div class="mw-collapsible-content">
Gear ID: ''{{ weapon.filepath }}''
{% raw %}{{{% endraw %}EquipmentMechs|{{ weapon.filepath }}{% raw %}}}{% endraw %}'
</div></div>
{%- endfor %}
{%- endif %}

{# ============================================================
   MODE WEAPONS (TABS)
   ============================================================ #}
{%- if groups["modes"] %}
<div class="noresize">
<tabs>

{# collect all mode names #}
{%- set mode_names = [] %}
{%- for weapon in groups["modes"].values() %}
  {%- for mode_name in weapon.modes.keys() %}
    {%- if mode_name not in mode_names %}
      {%- set _ = mode_names.append(mode_name) %}
    {%- endif %}
  {%- endfor %}
{%- endfor %}

{%- for mode_name in mode_names %}
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
|-

{%- for weapon in groups["modes"].values() if mode_name in weapon.modes %}
{%- set mode = weapon.modes[mode_name] %}
|{{ weapon.name }}
|{{ weapon.ammo }}
|{{ weapon.hardpoint }}
|{{ weapon.tonnage }}
|{{ weapon.slots }}
|{{ mode.DamagePerShot | default(weapon.damage) }}
|{{ weapon.heatdamage }}
|{{ weapon.instability }}
|{{ mode.ShotsWhenFired | default(weapon.shots) }}
|{{ weapon.projectiles }}
|{{ mode.HeatGenerated | default(weapon.heat) }}
|{{ mode.RefireModifier | default(weapon.recoil) }}
|{{ mode.AccuracyModifier | default(weapon.accuracy) }}
|{{ weapon.evasionignored }}
|{{ mode.CriticalChanceMultiplier | default(weapon.bonuscritchance) }}
|{{ mode.MinRange | default(weapon.rangemin) }}
|{{ mode.ShortRange | default(weapon.rangeshort) }}
|{{ mode.MediumRange | default(weapon.rangemedium) }}
|{{ mode.LongRange | default(weapon.rangelong) }}
|{{ mode.MaxRange | default(weapon.rangemax) }}
|{{ weapon.firesinmelee }}
|{{ weapon.additionalinfo }}
|-
{%- endfor %}
|}
</tab>
{%- endfor %}

</tabs>
</div>
{%- endif %}

{%- endfor %}
