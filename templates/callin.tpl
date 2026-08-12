<div id="" class="" style="clear: right; margin: -1em 0 0 10px; float: right; padding: 10px; background: transparent; width: 220px; ">__TOC__</div>
A full explanation of how Beacons and Strafing Runs are used can be found [[https://www.bta3062.com/index.php?title=Beacons_and_Strafing_Runs|here]].

= Beacons =
<div class="noresize">
{| class="wikitable sortable"
|+ Comparison of Beacons
|-
! Beacon !! Weight !! Slots !! Resolve !! Call-in Cost !! Range || # of Call-Ins || Additional Effects || Community Content 
|-
{%- for airdrop in airdrops.values() %}
| {{ airdrop.name }} || {{airdrop.weight}} || {{airdrop.slots}} || {{airdrop.resolve}} || {{airdrop.cbills}} || {{airdrop.range}} || {{airdrop.drops}} || {{airdrop.effects}} || {{airdrop.com_content}} 
|-
{%- endfor %}
|}

= Contracts = 
<div class="noresize">
{| class="wikitable sortable"
|+ Comparison of Contracts
|-
! Contract !! Type !! Single-Use? !! Community Content 
|-
{%- for contract in contracts.values() %}
| {{ contract.name }} || {{contract.type}} || {{contract.single_use}} || {{contract.com_content}} 
|-
{%- endfor %}
|}

= BA-specific Beacons =

<div class="noresize">
{| class="wikitable sortable"
|+ Comparison of BA-specific Beacons
|-
! Beacon !! Weight !! Slots !! Resolve !! Call-in Cost !! Range || # of Drops || Additional Effects || Community Content 
|-
{%- for battlearmor in battlearmors.values() %}
| {{ battlearmor.name }} || {{battlearmor.weight}} || {{battlearmor.slots}} || {{battlearmor.resolve}} || {{battlearmor.cbills}} || {{battlearmor.range}} || {{battlearmor.drops}} || {{battlearmor.effects}} || {{battlearmor.com_content}} 
|-
{%- endfor %}
|}