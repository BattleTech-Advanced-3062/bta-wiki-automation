{%- for mode in modes %}
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
{%- for weapon in mode.weapons %}
|{{weapon.name}}
|{{weapon.ammo}}
|{{weapon.hardpoint}}
|{{weapon.tonnage}}
|{{weapon.slots}}
|{{weapon.damage}}
|{{weapon.heatdamage}}
|{{weapon.instability}}
|{{weapon.shots}}
|{{weapon.projectiles}}
|{{weapon.heat}}
|{{weapon.recoil}}
|{{weapon.accuracy}}
|{{weapon.evasionignored}}
|{{weapon.bonuscritchance}}
|{{weapon.rangemin}}
|{{weapon.rangeshort}}
|{{weapon.rangemedium}}
|{{weapon.rangelong}}
|{{weapon.rangemax}}
|{{weapon.firesinmelee}}
|{{weapon.additionalinfo}}
|-
{%- endfor %}
|} {%- endfor %}