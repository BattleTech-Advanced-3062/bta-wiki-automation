<div class="noresize">
{| class="wikitable sortable"
|+ Comparison of Jump Jets
|-
! Beacon !! Weight !! Slots !! Resolve !! CBills !! Range || # of Drops || Additional Effects || Community Content || Mech Availability ||
|-
{%- for airdrop in airdrops.values() %}
| {{ airdrop.name }} || {{airdrop.weight}} || {{airdrop.slots}} || {{airdrop.resolve}} || {{airdrop.cbills}} || {{airdrop.range}} || {{airdrop.drops}} || {{airdrop.effects}} || {{airdrop.com_content}} || <div class="toccolours mw-collapsible mw-collapsed">
<div style="font-weight:bold;line-height:1.6;">'''Availble From: '''</div>
<div class="mw-collapsible-content">
{% raw %}{{{% endraw %}EquipmentMechs|{{airdrop.airdrop_ID}}{% raw %}}}{% endraw %}
</div>
|-
{%- endfor %}
|}