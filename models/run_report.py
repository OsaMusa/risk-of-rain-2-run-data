import xml.etree.ElementTree as ET
import os.path as path
from datetime import datetime as dt

class Run_Report:
    """A Risk of Rain 2 run."""

    def __init__(self, file):
        date_created = path.getctime(file)
        run_date = dt.fromtimestamp(date_created).strftime('%Y-%m-%d %H:%M:%S')

        tree = ET.parse(file)
        root = tree.getroot()
        
        player_info = root.find('playerInfos/PlayerInfo')
        self.stat_sheet = root.find('playerInfos/PlayerInfo/statSheet/fields')

        run_ending = root.findtext('gameEnding')
        endings = {'MainEnding':'Victory', 'ObliterationEnding':'Obliterated', 'LimboEnding':'Limbo', 'StandardLoss':'Defeat'}

        # Run Meta Data
        self.run_id = root.findtext('runGuid')
        self.gameMode = root.findtext('gameModeName')
        self.difficulty = root.findtext('ruleBook').split('.')[1].split()[0]
        self.ending = endings.get(run_ending) if endings.get(run_ending) != None else 'Defeat'
        self.date = dt.strptime(run_date, '%Y-%m-%d %H:%M:%S')

        # Player Info
        self.playerName = player_info.findtext('name')
        self.survivor = player_info.findtext('bodyName')
        self.totalTimeAlive = self.get_stat('totalTimeAlive')
        self.totalDistanceTraveled = self.get_stat('totalDistanceTraveled')
        self.died = 'Yes' if player_info.findtext('isDead') == '1' else 'No'
        self.killer = player_info.findtext('killerBodyName')
        self.highestLevel = self.get_stat('highestLevel')
        self.totalDeaths = self.get_stat('totalDeaths')

        # Damage Stats
        self.totalMinionDamageDealt  = self.get_stat('totalMinionDamageDealt')
        self.totalDamageDealt = self.get_stat('totalDamageDealt')
        self.totalDamageTaken = self.get_stat('totalDamageTaken')
        self.totalHealthHealed = self.get_stat('totalHealthHealed')
        self.highestDamageDealt = self.get_stat('highestDamageDealt')
        self.damageDealtToBeetle = self.get_damage_dealt('beetle')
        self.damageDealtToBeetleguard = self.get_damage_dealt('beetleguard')
        self.damageDealtToBison = self.get_damage_dealt('bison')
        self.damageDealtToGolem = self.get_damage_dealt('golem')
        self.damageDealtToWisp = self.get_damage_dealt('wisp')
        self.damageDealtToGreaterwisp = self.get_damage_dealt('greaterwisp')
        self.damageDealtToLemurian = self.get_damage_dealt('lemurian')
        self.damageDealtToLemurianbruiser = self.get_damage_dealt('lemurianbruiser')
        self.damageDealtToImp = self.get_damage_dealt('imp')
        self.damageDealtToJellyfish = self.get_damage_dealt('jellyfish')
        self.damageDealtToHermitcrab = self.get_damage_dealt('hermitcrab')
        self.damageDealtToBell = self.get_damage_dealt('bell')
        self.damageDealtToClaybruiser = self.get_damage_dealt('claybruiser')
        self.damageDealtToVulture = self.get_damage_dealt('vulture')
        self.damageDealtToRoboballmini = self.get_damage_dealt('roboballmini')
        self.damageDealtToNullifier = self.get_damage_dealt('nullifier')
        self.damageDealtToParent = self.get_damage_dealt('parent')
        self.damageDealtToMinimushroom = self.get_damage_dealt('minimushroom')
        self.damageDealtToLunarwisp = self.get_damage_dealt('lunarwisp')
        self.damageDealtToLunargolem = self.get_damage_dealt('lunargolem')
        self.damageDealtToLunarexploder = self.get_damage_dealt('lunarexploder')
        self.damageDealtToBeetlequeen = self.get_damage_dealt('beetlequeen')
        self.damageDealtToClayboss = self.get_damage_dealt('clayboss')
        self.damageDealtToTitan = self.get_damage_dealt('titan')
        self.damageDealtToTitangold = self.get_damage_dealt('titangold')
        self.damageDealtToVagrant = self.get_damage_dealt('vagrant')
        self.damageDealtToMagmaworm = self.get_damage_dealt('magmaworm')
        self.damageDealtToElectricworm = self.get_damage_dealt('electricworm')
        self.damageDealtToImpboss = self.get_damage_dealt('impboss')
        self.damageDealtToGravekeeper = self.get_damage_dealt('gravekeeper')
        self.damageDealtToRoboballboss = self.get_damage_dealt('roboballboss')
        self.damageDealtToSuperroboballboss = self.get_damage_dealt('superroboballboss')
        self.damageDealtToScav = self.get_damage_dealt('scav')
        self.damageDealtToScavlunar1 = self.get_damage_dealt('scavlunar1')
        self.damageDealtToScavlunar2 = self.get_damage_dealt('scavlunar2')
        self.damageDealtToScavlunar3 = self.get_damage_dealt('scavlunar3')
        self.damageDealtToScavlunar4 = self.get_damage_dealt('scavlunar4')
        self.damageDealtToGrandparent = self.get_damage_dealt('grandparent')
        self.damageDealtToArtifactshell = self.get_damage_dealt('artifactshell')
        self.damageDealtToBrother = self.get_damage_dealt('brother')
        self.damageTakenFromBeetle = self.get_damage_taken('beetle')
        self.damageTakenFromBeetleguard = self.get_damage_taken('beetleguard')
        self.damageTakenFromBison = self.get_damage_taken('bison')
        self.damageTakenFromGolem = self.get_damage_taken('golem')
        self.damageTakenFromWisp = self.get_damage_taken('wisp')
        self.damageTakenFromGreaterwisp = self.get_damage_taken('greaterwisp')
        self.damageTakenFromLemurian = self.get_damage_taken('lemurian')
        self.damageTakenFromLemurianbruiser = self.get_damage_taken('lemurianbruiser')
        self.damageTakenFromImp = self.get_damage_taken('imp')
        self.damageTakenFromJellyfish = self.get_damage_taken('jellyfish')
        self.damageTakenFromHermitcrab = self.get_damage_taken('hermitcrab')
        self.damageTakenFromBell = self.get_damage_taken('bell')
        self.damageTakenFromClaybruiser = self.get_damage_taken('claybruiser')
        self.damageTakenFromVulture = self.get_damage_taken('vulture')
        self.damageTakenFromRoboballmini = self.get_damage_taken('roboballmini')
        self.damageTakenFromNullifier = self.get_damage_taken('nullifier')
        self.damageTakenFromParent = self.get_damage_taken('parent')
        self.damageTakenFromMinimushroom = self.get_damage_taken('minimushroom')
        self.damageTakenFromLunarwisp = self.get_damage_taken('lunarwisp')
        self.damageTakenFromLunargolem = self.get_damage_taken('lunargolem')
        self.damageTakenFromLunarexploder = self.get_damage_taken('lunarexploder')
        self.damageTakenFromBeetlequeen = self.get_damage_taken('beetlequeen')
        self.damageTakenFromClayboss = self.get_damage_taken('clayboss')
        self.damageTakenFromTitan = self.get_damage_taken('titan')
        self.damageTakenFromTitangold = self.get_damage_taken('titangold')
        self.damageTakenFromVagrant = self.get_damage_taken('vagrant')
        self.damageTakenFromMagmaworm = self.get_damage_taken('magmaworm')
        self.damageTakenFromElectricworm = self.get_damage_taken('electricworm')
        self.damageTakenFromImpboss = self.get_damage_taken('impboss')
        self.damageTakenFromGravekeeper = self.get_damage_taken('gravekeeper')
        self.damageTakenFromRoboballboss = self.get_damage_taken('roboballboss')
        self.damageTakenFromSuperroboballboss = self.get_damage_taken('superroboballboss')
        self.damageTakenFromScav = self.get_damage_taken('scav')
        self.damageTakenFromScavlunar1 = self.get_damage_taken('scavlunar1')
        self.damageTakenFromScavlunar2 = self.get_damage_taken('scavlunar2')
        self.damageTakenFromScavlunar3 = self.get_damage_taken('scavlunar3')
        self.damageTakenFromScavlunar4 = self.get_damage_taken('scavlunar4')
        self.damageTakenFromGrandparent = self.get_damage_taken('grandparent')
        self.damageTakenFromArtifactshell = self.get_damage_taken('artifactshell')
        self.damageTakenFromBrother = self.get_damage_taken('brother')
        
        # Kill Stats
        self.totalMinionKills = self.get_stat('totalMinionKills')
        self.totalKills = self.get_stat('totalKills')
        self.totalEliteKills = self.get_stat('totalEliteKills')
        self.totalTeleporterBossKills = self.get_stat('totalTeleporterBossKillsWitnessed')
        self.killsAgainstBeetle = self.get_kills('beetle')
        self.killsAgainstBeetleguard = self.get_kills('beetleguard')
        self.killsAgainstBison = self.get_kills('bison')
        self.killsAgainstGolem = self.get_kills('golem')
        self.killsAgainstWisp = self.get_kills('wisp')
        self.killsAgainstGreaterwisp = self.get_kills('greaterwisp')
        self.killsAgainstLemurian = self.get_kills('lemurian')
        self.killsAgainstLemurianbruiser = self.get_kills('lemurianbruiser')
        self.killsAgainstImp = self.get_kills('imp')
        self.killsAgainstJellyfish = self.get_kills('jellyfish')
        self.killsAgainstHermitcrab = self.get_kills('hermitcrab')
        self.killsAgainstBell = self.get_kills('bell')
        self.killsAgainstClaybruiser = self.get_kills('claybruiser')
        self.killsAgainstVulture = self.get_kills('vulture')
        self.killsAgainstRoboballmini = self.get_kills('roboballmini')
        self.killsAgainstNullifier = self.get_kills('nullifier')
        self.killsAgainstParent = self.get_kills('parent')
        self.killsAgainstMinimushroom = self.get_kills('minimushroom')
        self.killsAgainstLunarwisp = self.get_kills('lunarwisp')
        self.killsAgainstLunargolem = self.get_kills('lunargolem')
        self.killsAgainstLunarexploder = self.get_kills('lunarexploder')
        self.killsAgainstBeetlequeen = self.get_kills('beetlequeen')
        self.killsAgainstClayboss = self.get_kills('clayboss')
        self.killsAgainstTitan = self.get_kills('titan')
        self.killsAgainstTitangold = self.get_kills('titangold')
        self.killsAgainstVagrant = self.get_kills('vagrant')
        self.killsAgainstMagmaworm = self.get_kills('magmaworm')
        self.killsAgainstElectricworm = self.get_kills('electricworm')
        self.killsAgainstImpboss = self.get_kills('impboss')
        self.killsAgainstGravekeeper = self.get_kills('gravekeeper')
        self.killsAgainstRoboballboss = self.get_kills('roboballboss')
        self.killsAgainstSuperroboballboss = self.get_kills('superroboballboss')
        self.killsAgainstScav = self.get_kills('scav')
        self.killsAgainstScavlunar1 = self.get_kills('scavlunar1')
        self.killsAgainstScavlunar2 = self.get_kills('scavlunar2')
        self.killsAgainstScavlunar3 = self.get_kills('scavlunar3')
        self.killsAgainstScavlunar4 = self.get_kills('scavlunar4')
        self.killsAgainstGrandparent = self.get_kills('grandparent')
        self.killsAgainstArtifactshell = self.get_kills('artifactshell')
        self.killsAgainstBrother = self.get_kills('brother')
        self.killsAgainstEliteBeetle = self.get_elite_kills('beetle')
        self.killsAgainstEliteBeetleguard = self.get_elite_kills('beetleguard')
        self.killsAgainstEliteBison = self.get_elite_kills('bison')
        self.killsAgainstEliteGolem = self.get_elite_kills('golem')
        self.killsAgainstEliteWisp = self.get_elite_kills('wisp')
        self.killsAgainstEliteGreaterwisp = self.get_elite_kills('greaterwisp')
        self.killsAgainstEliteLemurian = self.get_elite_kills('lemurian')
        self.killsAgainstEliteLemurianbruiser = self.get_elite_kills('lemurianbruiser')
        self.killsAgainstEliteImp = self.get_elite_kills('imp')
        self.killsAgainstEliteJellyfish = self.get_elite_kills('jellyfish')
        self.killsAgainstEliteHermitcrab = self.get_elite_kills('hermitcrab')
        self.killsAgainstEliteBell = self.get_elite_kills('bell')
        self.killsAgainstEliteClaybruiser = self.get_elite_kills('claybruiser')
        self.killsAgainstEliteVulture = self.get_elite_kills('vulture')
        self.killsAgainstEliteRoboballmini = self.get_elite_kills('roboballmini')
        self.killsAgainstEliteNullifier = self.get_elite_kills('nullifier')
        self.killsAgainstEliteParent = self.get_elite_kills('parent')
        self.killsAgainstEliteMinimushroom = self.get_elite_kills('minimushroom')
        self.killsAgainstEliteLunarwisp = self.get_elite_kills('lunarwisp')
        self.killsAgainstEliteLunargolem = self.get_elite_kills('lunargolem')
        self.killsAgainstEliteLunarexploder = self.get_elite_kills('lunarexploder')
        self.killsAgainstEliteBeetlequeen = self.get_elite_kills('beetlequeen')
        self.killsAgainstEliteClayboss = self.get_elite_kills('clayboss')
        self.killsAgainstEliteTitan = self.get_elite_kills('titan')
        self.killsAgainstEliteVagrant = self.get_elite_kills('vagrant')
        self.killsAgainstEliteImpboss = self.get_elite_kills('impboss')
        self.killsAgainstEliteGravekeeper = self.get_elite_kills('gravekeeper')
        self.killsAgainstEliteRoboballboss = self.get_elite_kills('roboballboss')
        self.killsAgainstEliteScav = self.get_elite_kills('scav')
        self.killsAgainstEliteGrandparent = self.get_elite_kills('grandparent')

        # Purchases
        self.totalGoldCollected = self.get_stat('totalGoldCollected')
        self.maxGoldCollected = self.get_stat('maxGoldCollected')
        self.totalPurchases = self.get_stat('totalPurchases')
        self.highestPurchases = self.get_stat('highestPurchases')
        self.totalGoldPurchases = self.get_stat('totalGoldPurchases')
        self.highestGoldPurchases = self.get_stat('highestGoldPurchases')
        self.totalBloodPurchases = self.get_stat('totalBloodPurchases')
        self.highestBloodPurchases = self.get_stat('highestBloodPurchases')
        self.totalLunarPurchases = self.get_stat('totalLunarPurchases')
        self.highestLunarPurchases = self.get_stat('highestLunarPurchases')
        self.totalDronesPurchased = self.get_stat('totalDronesPurchased')
        self.totalTurretsPurchased = self.get_stat('totalTurretsPurchased')

        # Item Info
        self.totalItemsCollected = self.get_stat('totalItemsCollected')
        self.highestItemsCollected = self.get_stat('highestItemsCollected')
        self.totalCollectedClover = self.get_total_items_collected('clover')
        self.totalCollectedSyringe = self.get_total_items_collected('syringe')
        self.totalCollectedBear = self.get_total_items_collected('bear')
        self.totalCollectedBehemoth = self.get_total_items_collected('behemoth')
        self.totalCollectedMissile = self.get_total_items_collected('missile')
        self.totalCollectedExplodeondeath = self.get_total_items_collected('explodeondeath')
        self.totalCollectedDagger = self.get_total_items_collected('dagger')
        self.totalCollectedTooth = self.get_total_items_collected('tooth')
        self.totalCollectedCritglasses = self.get_total_items_collected('critglasses')
        self.totalCollectedHoof = self.get_total_items_collected('hoof')
        self.totalCollectedFeather = self.get_total_items_collected('feather')
        self.totalCollectedChainlightning = self.get_total_items_collected('chainlightning')
        self.totalCollectedSeed = self.get_total_items_collected('seed')
        self.totalCollectedIcicle = self.get_total_items_collected('icicle')
        self.totalCollectedGhostonkill = self.get_total_items_collected('ghostonkill')
        self.totalCollectedMushroom = self.get_total_items_collected('mushroom')
        self.totalCollectedCrowbar = self.get_total_items_collected('crowbar')
        self.totalCollectedAttackspeedoncrit = self.get_total_items_collected('attackspeedoncrit')
        self.totalCollectedBleedonhit = self.get_total_items_collected('bleedonhit')
        self.totalCollectedSprintoutofcombat = self.get_total_items_collected('sprintoutofcombat')
        self.totalCollectedFallboots = self.get_total_items_collected('fallboots')
        self.totalCollectedWardonlevel = self.get_total_items_collected('wardonlevel')
        self.totalCollectedWarcryonmultikill = self.get_total_items_collected('warcryonmultikill')
        self.totalCollectedPhasing = self.get_total_items_collected('phasing')
        self.totalCollectedHealoncrit = self.get_total_items_collected('healoncrit')
        self.totalCollectedHealwhilesafe = self.get_total_items_collected('healwhilesafe')
        self.totalCollectedJumpboost = self.get_total_items_collected('jumpboost')
        self.totalCollectedPersonalshield = self.get_total_items_collected('personalshield')
        self.totalCollectedNovaonheal = self.get_total_items_collected('novaonheal')
        self.totalCollectedMedkit = self.get_total_items_collected('medkit')
        self.totalCollectedEquipmentmagazine = self.get_total_items_collected('equipmentmagazine')
        self.totalCollectedInfusion = self.get_total_items_collected('infusion')
        self.totalCollectedShocknearby = self.get_total_items_collected('shocknearby')
        self.totalCollectedIgniteonkill = self.get_total_items_collected('igniteonkill')
        self.totalCollectedBouncenearby = self.get_total_items_collected('bouncenearby')
        self.totalCollectedFirework = self.get_total_items_collected('firework')
        self.totalCollectedBandolier = self.get_total_items_collected('bandolier')
        self.totalCollectedStunchanceonhit = self.get_total_items_collected('stunchanceonhit')
        self.totalCollectedLunardagger = self.get_total_items_collected('lunardagger')
        self.totalCollectedGoldonhit = self.get_total_items_collected('goldonhit')
        self.totalCollectedShieldonly = self.get_total_items_collected('shieldonly')
        self.totalCollectedAlienhead = self.get_total_items_collected('alienhead')
        self.totalCollectedTalisman = self.get_total_items_collected('talisman')
        self.totalCollectedKnurl = self.get_total_items_collected('knurl')
        self.totalCollectedBeetlegland = self.get_total_items_collected('beetlegland')
        self.totalCollectedSprintbonus = self.get_total_items_collected('sprintbonus')
        self.totalCollectedSecondaryskillmagazine = self.get_total_items_collected('secondaryskillmagazine')
        self.totalCollectedStickybomb = self.get_total_items_collected('stickybomb')
        self.totalCollectedTreasurecache = self.get_total_items_collected('treasurecache')
        self.totalCollectedBossdamagebonus = self.get_total_items_collected('bossdamagebonus')
        self.totalCollectedSprintarmor = self.get_total_items_collected('sprintarmor')
        self.totalCollectedIcering = self.get_total_items_collected('icering')
        self.totalCollectedFirering = self.get_total_items_collected('firering')
        self.totalCollectedSlowonhit = self.get_total_items_collected('slowonhit')
        self.totalCollectedExtralife = self.get_total_items_collected('extralife')
        self.totalCollectedUtilityskillmagazine = self.get_total_items_collected('utilityskillmagazine')
        self.totalCollectedHeadhunter = self.get_total_items_collected('headhunter')
        self.totalCollectedKillelitefrenzy = self.get_total_items_collected('killelitefrenzy')
        self.totalCollectedIncreasehealing = self.get_total_items_collected('increasehealing')
        self.totalCollectedRepeatheal = self.get_total_items_collected('repeatheal')
        self.totalCollectedAutocastequipment = self.get_total_items_collected('autocastequipment')
        self.totalCollectedExecutelowhealthelite = self.get_total_items_collected('executelowhealthelite')
        self.totalCollectedEnergizedonequipmentuse = self.get_total_items_collected('energizedonequipmentuse')
        self.totalCollectedBarrieronoverheal = self.get_total_items_collected('barrieronoverheal')
        self.totalCollectedTitangoldduringtp = self.get_total_items_collected('titangoldduringtp')
        self.totalCollectedSprintwisp = self.get_total_items_collected('sprintwisp')
        self.totalCollectedBarrieronkill = self.get_total_items_collected('barrieronkill')
        self.totalCollectedArmorreductiononhit = self.get_total_items_collected('armorreductiononhit')
        self.totalCollectedTphealingnova = self.get_total_items_collected('tphealingnova')
        self.totalCollectedNearbydamagebonus = self.get_total_items_collected('nearbydamagebonus')
        self.totalCollectedLunarutilityreplacement = self.get_total_items_collected('lunarutilityreplacement')
        self.totalCollectedThorns = self.get_total_items_collected('thorns')
        self.totalCollectedFlathealth = self.get_total_items_collected('flathealth')
        self.totalCollectedPearl = self.get_total_items_collected('pearl')
        self.totalCollectedShinypearl = self.get_total_items_collected('shinypearl')
        self.totalCollectedBonusgoldpackonkill = self.get_total_items_collected('bonusgoldpackonkill')
        self.totalCollectedLaserturbine = self.get_total_items_collected('laserturbine')
        self.totalCollectedLunarprimaryreplacement = self.get_total_items_collected('lunarprimaryreplacement')
        self.totalCollectedNovaonlowhealth = self.get_total_items_collected('novaonlowhealth')
        self.totalCollectedLunartrinket = self.get_total_items_collected('lunartrinket')
        self.totalCollectedRepulsionarmorplate = self.get_total_items_collected('armorplate')
        self.totalCollectedSquidturret = self.get_total_items_collected('squid')
        self.totalCollectedDeathmark = self.get_total_items_collected('deathmark')
        self.totalCollectedInterstellardeskplant = self.get_total_items_collected('plant')
        self.totalCollectedFocusedconvergence = self.get_total_items_collected('focusconvergence')
        self.totalCollectedFireballsonhit = self.get_total_items_collected('fireballsonhit')
        self.totalCollectedLightningstrikeonhit = self.get_total_items_collected('lightningstrikeonhit')
        self.totalCollectedBleedonhitandexplode = self.get_total_items_collected('bleedonhitandexplode')
        self.totalCollectedSiphononlowhealth = self.get_total_items_collected('siphononlowhealth')
        self.totalCollectedMonstersonshrineuse = self.get_total_items_collected('monstersonshrineuse')
        self.totalCollectedRandomdamagezone = self.get_total_items_collected('randomdamagezone')
        self.totalCollectedArtifactkey = self.get_total_items_collected('artifactkey')
        self.totalCollectedCaptaindefensematrix = self.get_total_items_collected('captaindefensematrix')
        self.totalCollectedScrapwhite = self.get_total_items_collected('scrapwhite')
        self.totalCollectedScrapgreen = self.get_total_items_collected('scrapgreen')
        self.totalCollectedScrapred = self.get_total_items_collected('scrapred')
        self.totalCollectedScrapyellow = self.get_total_items_collected('scrapyellow')
        self.totalCollectedLunarbadluck = self.get_total_items_collected('lunarbadluck')
        self.totalCollectedLunarsecondaryreplacement = self.get_total_items_collected('lunarsecondaryreplacement')
        self.totalCollectedRoboballbuddy = self.get_total_items_collected('roboballbuddy')
        self.totalCollectedParentegg = self.get_total_items_collected('parentegg')
        self.totalCollectedLunarspecialreplacement = self.get_total_items_collected('lunarspecialreplacement')
        self.highestCollectedClover = self.get_highest_items_collected('clover')
        self.highestCollectedSyringe = self.get_highest_items_collected('syringe')
        self.highestCollectedBear = self.get_highest_items_collected('bear')
        self.highestCollectedBehemoth = self.get_highest_items_collected('behemoth')
        self.highestCollectedMissile = self.get_highest_items_collected('missile')
        self.highestCollectedExplodeondeath = self.get_highest_items_collected('explodeondeath')
        self.highestCollectedDagger = self.get_highest_items_collected('dagger')
        self.highestCollectedTooth = self.get_highest_items_collected('tooth')
        self.highestCollectedCritglasses = self.get_highest_items_collected('critglasses')
        self.highestCollectedHoof = self.get_highest_items_collected('hoof')
        self.highestCollectedFeather = self.get_highest_items_collected('feather')
        self.highestCollectedChainlightning = self.get_highest_items_collected('chainlightning')
        self.highestCollectedSeed = self.get_highest_items_collected('seed')
        self.highestCollectedIcicle = self.get_highest_items_collected('icicle')
        self.highestCollectedGhostonkill = self.get_highest_items_collected('ghostonkill')
        self.highestCollectedMushroom = self.get_highest_items_collected('mushroom')
        self.highestCollectedCrowbar = self.get_highest_items_collected('crowbar')
        self.highestCollectedAttackspeedoncrit = self.get_highest_items_collected('attackspeedoncrit')
        self.highestCollectedBleedonhit = self.get_highest_items_collected('bleedonhit')
        self.highestCollectedSprintoutofcombat = self.get_highest_items_collected('sprintoutofcombat')
        self.highestCollectedFallboots = self.get_highest_items_collected('fallboots')
        self.highestCollectedWardonlevel = self.get_highest_items_collected('wardonlevel')
        self.highestCollectedWarcryonmultikill = self.get_highest_items_collected('warcryonmultikill')
        self.highestCollectedPhasing = self.get_highest_items_collected('phasing')
        self.highestCollectedHealoncrit = self.get_highest_items_collected('healoncrit')
        self.highestCollectedHealwhilesafe = self.get_highest_items_collected('healwhilesafe')
        self.highestCollectedJumpboost = self.get_highest_items_collected('jumpboost')
        self.highestCollectedPersonalshield = self.get_highest_items_collected('personalshield')
        self.highestCollectedNovaonheal = self.get_highest_items_collected('novaonheal')
        self.highestCollectedMedkit = self.get_highest_items_collected('medkit')
        self.highestCollectedEquipmentmagazine = self.get_highest_items_collected('equipmentmagazine')
        self.highestCollectedInfusion = self.get_highest_items_collected('infusion')
        self.highestCollectedShocknearby = self.get_highest_items_collected('shocknearby')
        self.highestCollectedIgniteonkill = self.get_highest_items_collected('igniteonkill')
        self.highestCollectedBouncenearby = self.get_highest_items_collected('bouncenearby')
        self.highestCollectedFirework = self.get_highest_items_collected('firework')
        self.highestCollectedBandolier = self.get_highest_items_collected('bandolier')
        self.highestCollectedStunchanceonhit = self.get_highest_items_collected('stunchanceonhit')
        self.highestCollectedLunardagger = self.get_highest_items_collected('lunardagger')
        self.highestCollectedGoldonhit = self.get_highest_items_collected('goldonhit')
        self.highestCollectedShieldonly = self.get_highest_items_collected('shieldonly')
        self.highestCollectedAlienhead = self.get_highest_items_collected('alienhead')
        self.highestCollectedTalisman = self.get_highest_items_collected('talisman')
        self.highestCollectedKnurl = self.get_highest_items_collected('knurl')
        self.highestCollectedBeetlegland = self.get_highest_items_collected('beetlegland')
        self.highestCollectedSprintbonus = self.get_highest_items_collected('sprintbonus')
        self.highestCollectedSecondaryskillmagazine = self.get_highest_items_collected('secondaryskillmagazine')
        self.highestCollectedStickybomb = self.get_highest_items_collected('stickybomb')
        self.highestCollectedTreasurecache = self.get_highest_items_collected('treasurecache')
        self.highestCollectedBossdamagebonus = self.get_highest_items_collected('bossdamagebonus')
        self.highestCollectedSprintarmor = self.get_highest_items_collected('sprintarmor')
        self.highestCollectedIcering = self.get_highest_items_collected('icering')
        self.highestCollectedFirering = self.get_highest_items_collected('firering')
        self.highestCollectedSlowonhit = self.get_highest_items_collected('slowonhit')
        self.highestCollectedExtralife = self.get_highest_items_collected('extralife')
        self.highestCollectedUtilityskillmagazine = self.get_highest_items_collected('utilityskillmagazine')
        self.highestCollectedHeadhunter = self.get_highest_items_collected('headhunter')
        self.highestCollectedKillelitefrenzy = self.get_highest_items_collected('killelitefrenzy')
        self.highestCollectedIncreasehealing = self.get_highest_items_collected('increasehealing')
        self.highestCollectedRepeatheal = self.get_highest_items_collected('repeatheal')
        self.highestCollectedAutocastequipment = self.get_highest_items_collected('autocastequipment')
        self.highestCollectedExecutelowhealthelite = self.get_highest_items_collected('executelowhealthelite')
        self.highestCollectedEnergizedonequipmentuse = self.get_highest_items_collected('energizedonequipmentuse')
        self.highestCollectedBarrieronoverheal = self.get_highest_items_collected('barrieronoverheal')
        self.highestCollectedTitangoldduringtp = self.get_highest_items_collected('titangoldduringtp')
        self.highestCollectedSprintwisp = self.get_highest_items_collected('sprintwisp')
        self.highestCollectedBarrieronkill = self.get_highest_items_collected('barrieronkill')
        self.highestCollectedArmorreductiononhit = self.get_highest_items_collected('armorreductiononhit')
        self.highestCollectedTphealingnova = self.get_highest_items_collected('tphealingnova')
        self.highestCollectedNearbydamagebonus = self.get_highest_items_collected('nearbydamagebonus')
        self.highestCollectedLunarutilityreplacement = self.get_highest_items_collected('lunarutilityreplacement')
        self.highestCollectedThorns = self.get_highest_items_collected('thorns')
        self.highestCollectedFlathealth = self.get_highest_items_collected('flathealth')
        self.highestCollectedPearl = self.get_highest_items_collected('pearl')
        self.highestCollectedShinypearl = self.get_highest_items_collected('shinypearl')
        self.highestCollectedBonusgoldpackonkill = self.get_highest_items_collected('bonusgoldpackonkill')
        self.highestCollectedLaserturbine = self.get_highest_items_collected('laserturbine')
        self.highestCollectedLunarprimaryreplacement = self.get_highest_items_collected('lunarprimaryreplacement')
        self.highestCollectedNovaonlowhealth = self.get_highest_items_collected('novaonlowhealth')
        self.highestCollectedLunartrinket = self.get_highest_items_collected('lunartrinket')
        self.highestCollectedRepulsionarmorplate = self.get_highest_items_collected('armorplate')
        self.highestCollectedSquidturret = self.get_highest_items_collected('squid')
        self.highestCollectedDeathmark = self.get_highest_items_collected('deathmark')
        self.highestCollectedInterstellardeskplant = self.get_highest_items_collected('plant')
        self.highestCollectedFocusedconvergence = self.get_highest_items_collected('focusconvergence')
        self.highestCollectedFireballsonhit = self.get_highest_items_collected('fireballsonhit')
        self.highestCollectedLightningstrikeonhit = self.get_highest_items_collected('lightningstrikeonhit')
        self.highestCollectedBleedonhitandexplode = self.get_highest_items_collected('bleedonhitandexplode')
        self.highestCollectedSiphononlowhealth = self.get_highest_items_collected('siphononlowhealth')
        self.highestCollectedMonstersonshrineuse = self.get_highest_items_collected('monstersonshrineuse')
        self.highestCollectedRandomdamagezone = self.get_highest_items_collected('randomdamagezone')
        self.highestCollectedArtifactkey = self.get_highest_items_collected('artifactkey')
        self.highestCollectedCaptaindefensematrix = self.get_highest_items_collected('captaindefensematrix')
        self.highestCollectedScrapwhite = self.get_highest_items_collected('scrapwhite')
        self.highestCollectedScrapgreen = self.get_highest_items_collected('scrapgreen')
        self.highestCollectedScrapred = self.get_highest_items_collected('scrapred')
        self.highestCollectedScrapyellow = self.get_highest_items_collected('scrapyellow')
        self.highestCollectedLunarbadluck = self.get_highest_items_collected('lunarbadluck')
        self.highestCollectedLunarsecondaryreplacement = self.get_highest_items_collected('lunarsecondaryreplacement')
        self.highestCollectedRoboballbuddy = self.get_highest_items_collected('roboballbuddy')
        self.highestCollectedParentegg = self.get_highest_items_collected('parentegg')
        self.highestCollectedLunarspecialreplacement = self.get_highest_items_collected('lunarspecialreplacement')

        # Equipment Info
        self.timeHeldCommandmissile = self.get_time_held('commandmissile')
        self.timeHeldFruit = self.get_time_held('fruit')
        self.timeHeldMeteor = self.get_time_held('meteor')
        self.timeHeldBlackhole = self.get_time_held('blackhole')
        self.timeHeldCritonuse = self.get_time_held('critonuse')
        self.timeHeldDronebackup = self.get_time_held('dronebackup')
        self.timeHeldBfg = self.get_time_held('bfg')
        self.timeHeldJetpack = self.get_time_held('jetpack')
        self.timeHeldLightning = self.get_time_held('lightning')
        self.timeHeldGoldgat = self.get_time_held('goldgat')
        self.timeHeldPassivehealing = self.get_time_held('passivehealing')
        self.timeHeldBurnnearby = self.get_time_held('burnnearby')
        self.timeHeldScanner = self.get_time_held('scanner')
        self.timeHeldCrippleward = self.get_time_held('crippleward')
        self.timeHeldGateway = self.get_time_held('gateway')
        self.timeHeldTonic = self.get_time_held('tonic')
        self.timeHeldCleanse = self.get_time_held('cleanse')
        self.timeHeldFireballdash = self.get_time_held('fireballdash')
        self.timeHeldGainarmor = self.get_time_held('gainarmor')
        self.timeHeldSawmerang = self.get_time_held('saw')
        self.timeHeldRecycler = self.get_time_held('recycle')
        self.timeHeldLifestealonhit = self.get_time_held('lifestealonhit')
        self.timeHeldTeamwarcry = self.get_time_held('teamwarcry')
        self.timeHeldDeathprojectile = self.get_time_held('deathprojectile')
        self.timesFiredCommandmissile = self.get_times_fired('commandmissile')
        self.timesFiredFruit = self.get_times_fired('fruit')
        self.timesFiredMeteor = self.get_times_fired('meteor')
        self.timesFiredBlackhole = self.get_times_fired('blackhole')
        self.timesFiredCritonuse = self.get_times_fired('critonuse')
        self.timesFiredDronebackup = self.get_times_fired('dronebackup')
        self.timesFiredBfg = self.get_times_fired('bfg')
        self.timesFiredJetpack = self.get_times_fired('jetpack')
        self.timesFiredLightning = self.get_times_fired('lightning')
        self.timesFiredGoldgat = self.get_times_fired('goldgat')
        self.timesFiredPassivehealing = self.get_times_fired('passivehealing')
        self.timesFiredBurnnearby = self.get_times_fired('burnnearby')
        self.timesFiredScanner = self.get_times_fired('scanner')
        self.timesFiredCrippleward = self.get_times_fired('crippleward')
        self.timesFiredGateway = self.get_times_fired('gateway')
        self.timesFiredTonic = self.get_times_fired('tonic')
        self.timesFiredCleanse = self.get_times_fired('cleanse')
        self.timesFiredFireballdash = self.get_times_fired('fireballdash')
        self.timesFiredGainarmor = self.get_times_fired('gainarmor')
        self.timesFiredSawmerang = self.get_times_fired('saw')
        self.timesFiredRecycler = self.get_times_fired('recycle')
        self.timesFiredLifestealonhit = self.get_times_fired('lifestealonhit')
        self.timesFiredTeamwarcry = self.get_times_fired('teamwarcry')
        self.timesFiredDeathprojectile = self.get_times_fired('deathprojectile')

        # Stage Info
        self.totalStagesCompleted = self.get_stat('totalStagesCompleted')
        self.highestStagesCompleted = self.get_stat('highestStagesCompleted')
        self.timesVisitedBlackbeach = self.get_times_visited('blackbeach')
        self.timesVisitedGolemplains = self.get_times_visited('golemplains')
        self.timesVisitedGoolake = self.get_times_visited('goolake')
        self.timesVisitedBazaar = self.get_times_visited('bazaar')
        self.timesVisitedFrozenwall = self.get_times_visited('frozenwall')
        self.timesVisitedFoggyswamp = self.get_times_visited('foggyswamp')
        self.timesVisitedDampcave = self.get_times_visited('dampcave')
        self.timesVisitedWispgraveyard = self.get_times_visited('wispgraveyard')
        self.timesVisitedMysteryspace = self.get_times_visited('mysteryspace')
        self.timesVisitedGoldshores = self.get_times_visited('goldshores')
        self.timesVisitedShipgraveyard = self.get_times_visited('shipgraveyard')
        self.timesVisitedRootjungle = self.get_times_visited('rootjungle')
        self.timesVisitedArena = self.get_times_visited('arena')
        self.timesVisitedLimbo = self.get_times_visited('limbo')
        self.timesVisitedSkymeadow = self.get_times_visited('skymeadow')
        self.timesVisitedArtifactworld = self.get_times_visited('artifactworld')
        self.timesVisitedMoon = self.get_times_visited('moon')
        self.timesClearedBlackbeach = self.get_times_cleared('blackbeach')
        self.timesClearedGolemplains = self.get_times_cleared('golemplains')
        self.timesClearedGoolake = self.get_times_cleared('goolake')
        self.timesClearedBazaar = self.get_times_cleared('bazaar')
        self.timesClearedFrozenwall = self.get_times_cleared('frozenwall')
        self.timesClearedFoggyswamp = self.get_times_cleared('foggyswamp')
        self.timesClearedDampcave = self.get_times_cleared('dampcave')
        self.timesClearedWispgraveyard = self.get_times_cleared('wispgraveyard')
        self.timesClearedMysteryspace = self.get_times_cleared('mysteryspace')
        self.timesClearedGoldshores = self.get_times_cleared('goldshores')
        self.timesClearedShipgraveyard = self.get_times_cleared('shipgraveyard')
        self.timesClearedRootjungle = self.get_times_cleared('rootjungle')
        self.timesClearedArena = self.get_times_cleared('arena')
        self.timesClearedLimbo = self.get_times_cleared('limbo')
        self.timesClearedSkymeadow = self.get_times_cleared('skymeadow')
        self.timesClearedArtifactworld = self.get_times_cleared('artifactworld')
        self.timesClearedMoon = self.get_times_cleared('moon')

    def get_stat(self, stat):
        '''Return 0 for specified stat if it doesn't exist.'''
        if self.stat_sheet.findtext(stat) != None:
            return self.stat_sheet.findtext(stat)
        
        else:
            return 0

    def get_kills(self, enemy):
        '''Return number of kills against specified enemy.'''

        kills = 0

        if enemy.lower() != 'brother':
            for field in self.stat_sheet.findall('.//'):
                if ('killsAgainst.'+ enemy +'Body').capitalize() in field.tag.capitalize():
                    kills = field.text
            
            return kills

        else:
            bro = self.stat_sheet.findtext('killsAgainst.BrotherHurtBody')
            bro_kill = 0 if bro == None else bro
            
            return bro_kill

        
    def get_elite_kills(self, enemy):
        '''Return number of kills agaist elite variant of specified enemy.'''
        
        elite_kills = 0

        for field in self.stat_sheet.findall('.//'):
            if ('killsAgainstElite.'+ enemy +'Body').capitalize() in field.tag.capitalize():
                elite_kills = field.text
        
        return elite_kills
        
    def get_damage_dealt(self, enemy):
        '''Return damage dealt to specified enemy.'''
        
        dmg_dealt = 0

        if enemy.lower() != 'brother':
            for field in self.stat_sheet.findall('.//'):
                if ('damageDealtTo.'+ enemy +'Body').capitalize() in field.tag.capitalize():
                    dmg_dealt = field.text
            
            return dmg_dealt
        
        else:
            bro = self.stat_sheet.findtext('damageDealtTo.BrotherBody')
            bro_hrt = self.stat_sheet.findtext('damageDealtTo.BrotherHurtBody')
            
            bro_dmg = 0 if bro == None else bro
            bro_hrt_dmg = 0 if bro_hrt == None else bro_hrt
            
            return int(bro_dmg) + int(bro_hrt_dmg)

        
    def get_damage_taken(self, enemy):
        '''Return damage taken from specified enemy.'''

        dmg_tkn = 0

        if enemy.lower() != 'brother':
            for field in self.stat_sheet.findall('.//'):
                if ('damageTakenFrom.'+ enemy +'Body').capitalize() in field.tag.capitalize():
                    dmg_tkn = field.text
            
            return dmg_tkn
        
        else:
            bro = self.stat_sheet.findtext('damageTakenFrom.BrotherBody')
            bro_hrt = self.stat_sheet.findtext('damageTakenFrom.BrotherHurtBody')
            
            bro_dmg = 0 if bro == None else bro
            bro_hrt_dmg = 0 if bro_hrt == None else bro_hrt
            
            return int(bro_dmg) + int(bro_hrt_dmg)
    
    def get_total_items_collected(self, item):
        '''Return total number of specified item collected.'''

        total_collected = 0

        for field in self.stat_sheet.findall('.//'):
            if ('totalCollected.' + item).capitalize() in field.tag.capitalize():
                total_collected = field.text
        
        return total_collected
        
    def get_highest_items_collected(self, item):
        '''Return highest number of specified item collected.'''

        highest_collected = 0

        for field in self.stat_sheet.findall('.//'):
            if ('highestCollected.' + item).capitalize() in field.tag.capitalize():
                highest_collected = field.text
        
        return highest_collected
        
    def get_time_held(self, equip):
        '''Return time specified equipment was held.'''

        time_held = 0

        for field in self.stat_sheet.findall('.//'):
            if ('totalTimeHeld.' + equip).capitalize() in field.tag.capitalize():
                time_held = field.text
        
        return time_held
        
    def get_times_fired(self, equip):
        '''Return number of times specified equipment was fired.'''

        times_fired = 0

        for field in self.stat_sheet.findall('.//'):
            if ('totalTimesFired.' + equip).capitalize() in field.tag.capitalize():
                times_fired = field.text
        
        return times_fired
        
    def get_times_visited(self, stage):
        '''Return amount of times specified stage was visited.'''

        times_visited = 0

        for field in self.stat_sheet.findall('.//'):
            if ('totalTimesVisited.' + stage).capitalize() in field.tag.capitalize():
                times_visited = field.text
        
        return times_visited
        
    def get_times_cleared(self, stage):
        '''Return amount of times specified stage was cleared.'''

        times_cleared = 0

        for field in self.stat_sheet.findall('.//'):
            if ('totalTimesCleared.' + stage).capitalize() in field.tag.capitalize():
                times_cleared = field.text
        
        return times_cleared
