import sqlite3
from datetime import datetime as dt
from os import listdir
from os.path import isfile, getctime
from models.run_report import Run_Report

def update_recent_run_setting(init_settings, most_recent_run):
    start_date = most_recent_run.replace(second=most_recent_run.second+1)
    init_settings[1] = 'most_recent_run_date = {}\n'.format(start_date)

    new_settings = open('settings.txt', 'w')
    new_settings.writelines(init_settings)
    new_settings.close()

con = sqlite3.connect('db/run_report_db.db')
cur = con.cursor()

settings_file = open('settings.txt', 'r')
settings = settings_file.readlines()

dir_path = settings[0].split('= ')[1].strip('\n') + 'RunReports\History\\'
last_run = dt.strptime(settings[1].split('= ')[1].strip('\n'),'%Y-%m-%d %H:%M:%S')

# Create list of run report files
reports = []
for file in listdir(dir_path):
    creation_date = dt.fromtimestamp(getctime(dir_path + file))

    if isfile(dir_path + file) and creation_date > last_run:
        reports.append(dir_path + file)

runs = [Run_Report(report) for report in reports]

# Enter data
def data_entry(report):
    cur.execute(
        '''
        INSERT INTO Run_Meta_Data
        VALUES (:Run_ID, :Game_Mode, :Difficulty, :Ending, :Run_Date)
        ''',
        {
            "Run_ID": report.run_id,
            "Game_Mode": report.gameMode,
            "Difficulty": report.difficulty,
            "Ending": report.ending,
            "Run_Date": report.date
        }
    )

    cur.execute(
        '''
        INSERT INTO Player_Info
        VALUES (:Run_ID, :Player_Name, :Survivor, :Total_Time_Alive, :Total_Distance_Traveled, :Died, :Killer, :Highest_Level, :Total_Deaths)
        ''',
        {
            "Run_ID": report.run_id,
            "Player_Name": report.playerName,
            "Survivor": report.survivor,
            "Total_Time_Alive": report.totalTimeAlive,
            "Total_Distance_Traveled": report.totalDistanceTraveled,
            "Died": report.died,
            "Killer": report.killer,
            "Highest_Level": report.highestLevel,
            "Total_Deaths": report.totalDeaths
        }
    )

    cur.execute(
        '''
        INSERT INTO Damage_Stats
        VALUES (:Run_ID, :Total_Minion_Damage_Dealt, :Total_Damage_Dealt, :Total_Damage_Taken, :Total_Health_Healed, :Highest_Damage_Dealt, :DDT_BEETLE, :DDT_BEETLEGUARD, :DDT_BISON, :DDT_GOLEM, :DDT_WISP, :DDT_GREATERWISP, :DDT_LEMURIAN, :DDT_LEMURIANBRUISER, :DDT_IMP, :DDT_JELLYFISH, :DDT_HERMITCRAB, :DDT_BELL, :DDT_CLAYBRUISER, :DDT_VULTURE, :DDT_ROBOBALLMINI, :DDT_NULLIFIER, :DDT_PARENT, :DDT_MINIMUSHROOM, :DDT_LUNARWISP, :DDT_LUNARGOLEM, :DDT_LUNAREXPLODER, :DDT_BEETLEQUEEN, :DDT_CLAYBOSS, :DDT_TITAN, :DDT_TITANGOLD, :DDT_VAGRANT, :DDT_MAGMAWORM, :DDT_ELECTRICWORM, :DDT_IMPBOSS, :DDT_GRAVEKEEPER, :DDT_ROBOBALLBOSS, :DDT_SUPERROBOBALLBOSS, :DDT_SCAV, :DDT_SCAVLUNAR1, :DDT_SCAVLUNAR2, :DDT_SCAVLUNAR3, :DDT_SCAVLUNAR4, :DDT_GRANDPARENT, :DDT_ARTIFACTSHELL, :DDT_BROTHER, :DTF_BEETLE, :DTF_BEETLEGUARD, :DTF_BISON, :DTF_GOLEM, :DTF_WISP, :DTF_GREATERWISP, :DTF_LEMURIAN, :DTF_LEMURIANBRUISER, :DTF_IMP, :DTF_JELLYFISH, :DTF_HERMITCRAB, :DTF_BELL, :DTF_CLAYBRUISER, :DTF_VULTURE, :DTF_ROBOBALLMINI, :DTF_NULLIFIER, :DTF_PARENT, :DTF_MINIMUSHROOM, :DTF_LUNARWISP, :DTF_LUNARGOLEM, :DTF_LUNAREXPLODER, :DTF_BEETLEQUEEN, :DTF_CLAYBOSS, :DTF_TITAN, :DTF_TITANGOLD, :DTF_VAGRANT, :DTF_MAGMAWORM, :DTF_ELECTRICWORM, :DTF_IMPBOSS, :DTF_GRAVEKEEPER, :DTF_ROBOBALLBOSS, :DTF_SUPERROBOBALLBOSS, :DTF_SCAV, :DTF_SCAVLUNAR1, :DTF_SCAVLUNAR2, :DTF_SCAVLUNAR3, :DTF_SCAVLUNAR4, :DTF_GRANDPARENT, :DTF_ARTIFACTSHELL, :DTF_BROTHER)
        ''',
        {
            "Run_ID": report.run_id,
            "Total_Minion_Damage_Dealt": report.totalMinionDamageDealt,
            "Total_Damage_Dealt": report.totalDamageDealt,
            "Total_Damage_Taken": report.totalDamageTaken,
            "Total_Health_Healed": report.totalHealthHealed,
            "Highest_Damage_Dealt": report.highestDamageDealt,
            "DDT_BEETLE": report.damageDealtToBeetle,
            "DDT_BEETLEGUARD": report.damageDealtToBeetleguard,
            "DDT_BISON": report.damageDealtToBison,
            "DDT_GOLEM": report.damageDealtToGolem,
            "DDT_WISP": report.damageDealtToWisp,
            "DDT_GREATERWISP": report.damageDealtToGreaterwisp,
            "DDT_LEMURIAN": report.damageDealtToLemurian,
            "DDT_LEMURIANBRUISER": report.damageDealtToLemurianbruiser,
            "DDT_IMP": report.damageDealtToImp,
            "DDT_JELLYFISH": report.damageDealtToJellyfish,
            "DDT_HERMITCRAB": report.damageDealtToHermitcrab,
            "DDT_BELL": report.damageDealtToBell,
            "DDT_CLAYBRUISER": report.damageDealtToClaybruiser,
            "DDT_VULTURE": report.damageDealtToVulture,
            "DDT_ROBOBALLMINI": report.damageDealtToRoboballmini,
            "DDT_NULLIFIER": report.damageDealtToNullifier,
            "DDT_PARENT": report.damageDealtToParent,
            "DDT_MINIMUSHROOM": report.damageDealtToMinimushroom,
            "DDT_LUNARWISP": report.damageDealtToLunarwisp,
            "DDT_LUNARGOLEM": report.damageDealtToLunargolem,
            "DDT_LUNAREXPLODER": report.damageDealtToLunarexploder,
            "DDT_BEETLEQUEEN": report.damageDealtToBeetlequeen,
            "DDT_CLAYBOSS": report.damageDealtToClayboss,
            "DDT_TITAN": report.damageDealtToTitan,
            "DDT_TITANGOLD": report.damageDealtToTitangold,
            "DDT_VAGRANT": report.damageDealtToVagrant,
            "DDT_MAGMAWORM": report.damageDealtToMagmaworm,
            "DDT_ELECTRICWORM": report.damageDealtToElectricworm,
            "DDT_IMPBOSS": report.damageDealtToImpboss,
            "DDT_GRAVEKEEPER": report.damageDealtToGravekeeper,
            "DDT_ROBOBALLBOSS": report.damageDealtToRoboballboss,
            "DDT_SUPERROBOBALLBOSS": report.damageDealtToSuperroboballboss,
            "DDT_SCAV": report.damageDealtToScav,
            "DDT_SCAVLUNAR1": report.damageDealtToScavlunar1,
            "DDT_SCAVLUNAR2": report.damageDealtToScavlunar2,
            "DDT_SCAVLUNAR3": report.damageDealtToScavlunar3,
            "DDT_SCAVLUNAR4": report.damageDealtToScavlunar4,
            "DDT_GRANDPARENT": report.damageDealtToGrandparent,
            "DDT_ARTIFACTSHELL": report.damageDealtToArtifactshell,
            "DDT_BROTHER": report.damageDealtToBrother,
            "DTF_BEETLE": report.damageTakenFromBeetle,
            "DTF_BEETLEGUARD": report.damageTakenFromBeetleguard,
            "DTF_BISON": report.damageTakenFromBison,
            "DTF_GOLEM": report.damageTakenFromGolem,
            "DTF_WISP": report.damageTakenFromWisp,
            "DTF_GREATERWISP": report.damageTakenFromGreaterwisp,
            "DTF_LEMURIAN": report.damageTakenFromLemurian,
            "DTF_LEMURIANBRUISER": report.damageTakenFromLemurianbruiser,
            "DTF_IMP": report.damageTakenFromImp,
            "DTF_JELLYFISH": report.damageTakenFromJellyfish,
            "DTF_HERMITCRAB": report.damageTakenFromHermitcrab,
            "DTF_BELL": report.damageTakenFromBell,
            "DTF_CLAYBRUISER": report.damageTakenFromClaybruiser,
            "DTF_VULTURE": report.damageTakenFromVulture,
            "DTF_ROBOBALLMINI": report.damageTakenFromRoboballmini,
            "DTF_NULLIFIER": report.damageTakenFromNullifier,
            "DTF_PARENT": report.damageTakenFromParent,
            "DTF_MINIMUSHROOM": report.damageTakenFromMinimushroom,
            "DTF_LUNARWISP": report.damageTakenFromLunarwisp,
            "DTF_LUNARGOLEM": report.damageTakenFromLunargolem,
            "DTF_LUNAREXPLODER": report.damageTakenFromLunarexploder,
            "DTF_BEETLEQUEEN": report.damageTakenFromBeetlequeen,
            "DTF_CLAYBOSS": report.damageTakenFromClayboss,
            "DTF_TITAN": report.damageTakenFromTitan,
            "DTF_TITANGOLD": report.damageTakenFromTitangold,
            "DTF_VAGRANT": report.damageTakenFromVagrant,
            "DTF_MAGMAWORM": report.damageTakenFromMagmaworm,
            "DTF_ELECTRICWORM": report.damageTakenFromElectricworm,
            "DTF_IMPBOSS": report.damageTakenFromImpboss,
            "DTF_GRAVEKEEPER": report.damageTakenFromGravekeeper,
            "DTF_ROBOBALLBOSS": report.damageTakenFromRoboballboss,
            "DTF_SUPERROBOBALLBOSS": report.damageTakenFromSuperroboballboss,
            "DTF_SCAV": report.damageTakenFromScav,
            "DTF_SCAVLUNAR1": report.damageTakenFromScavlunar1,
            "DTF_SCAVLUNAR2": report.damageTakenFromScavlunar2,
            "DTF_SCAVLUNAR3": report.damageTakenFromScavlunar3,
            "DTF_SCAVLUNAR4": report.damageTakenFromScavlunar4,
            "DTF_GRANDPARENT": report.damageTakenFromGrandparent,
            "DTF_ARTIFACTSHELL": report.damageTakenFromArtifactshell,
            "DTF_BROTHER": report.damageTakenFromBrother
        }
    )
    
    cur.execute(
        '''
        INSERT INTO Kill_Stats
        VALUES (:Run_ID, :Total_Minion_Kills, :Total_Kills, :Total_Elite_Kills, :Total_Teleporter_Boss_Kills, :KA_BEETLE, :KA_BEETLEGUARD, :KA_BISON, :KA_GOLEM, :KA_WISP, :KA_GREATERWISP, :KA_LEMURIAN, :KA_LEMURIANBRUISER, :KA_IMP, :KA_JELLYFISH, :KA_HERMITCRAB, :KA_BELL, :KA_CLAYBRUISER, :KA_VULTURE, :KA_ROBOBALLMINI, :KA_NULLIFIER, :KA_PARENT, :KA_MINIMUSHROOM, :KA_LUNARWISP, :KA_LUNARGOLEM, :KA_LUNAREXPLODER, :KA_BEETLEQUEEN, :KA_CLAYBOSS, :KA_TITAN, :KA_TITANGOLD, :KA_VAGRANT, :KA_MAGMAWORM, :KA_ELECTRICWORM, :KA_IMPBOSS, :KA_GRAVEKEEPER, :KA_ROBOBALLBOSS, :KA_SUPERROBOBALLBOSS, :KA_SCAV, :KA_SCAVLUNAR1, :KA_SCAVLUNAR2, :KA_SCAVLUNAR3, :KA_SCAVLUNAR4, :KA_GRANDPARENT, :KA_ARTIFACTSHELL, :KA_BROTHER, :KAE_BEETLE, :KAE_BEETLEGUARD, :KAE_BISON, :KAE_GOLEM, :KAE_WISP, :KAE_GREATERWISP, :KAE_LEMURIAN, :KAE_LEMURIANBRUISER, :KAE_IMP, :KAE_JELLYFISH, :KAE_HERMITCRAB, :KAE_BELL, :KAE_CLAYBRUISER, :KAE_VULTURE, :KAE_ROBOBALLMINI, :KAE_NULLIFIER, :KAE_PARENT, :KAE_MINIMUSHROOM, :KAE_LUNARWISP, :KAE_LUNARGOLEM, :KAE_LUNAREXPLODER, :KAE_BEETLEQUEEN, :KAE_CLAYBOSS, :KAE_TITAN, :KAE_VAGRANT, :KAE_IMPBOSS, :KAE_GRAVEKEEPER, :KAE_ROBOBALLBOSS, :KAE_SCAV, :KAE_GRANDPARENT)
        ''',
        {
            "Run_ID": report.run_id,
            "Total_Minion_Kills": report.totalMinionKills,
            "Total_Kills": report.totalKills,
            "Total_Elite_Kills": report.totalEliteKills,
            "Total_Teleporter_Boss_Kills": report.totalTeleporterBossKills,
            "KA_BEETLE": report.killsAgainstBeetle,
            "KA_BEETLEGUARD": report.killsAgainstBeetleguard,
            "KA_BISON": report.killsAgainstBison,
            "KA_GOLEM": report.killsAgainstGolem,
            "KA_WISP": report.killsAgainstWisp,
            "KA_GREATERWISP": report.killsAgainstGreaterwisp,
            "KA_LEMURIAN": report.killsAgainstLemurian,
            "KA_LEMURIANBRUISER": report.killsAgainstLemurianbruiser,
            "KA_IMP": report.killsAgainstImp,
            "KA_JELLYFISH": report.killsAgainstJellyfish,
            "KA_HERMITCRAB": report.killsAgainstHermitcrab,
            "KA_BELL": report.killsAgainstBell,
            "KA_CLAYBRUISER": report.killsAgainstClaybruiser,
            "KA_VULTURE": report.killsAgainstVulture,
            "KA_ROBOBALLMINI": report.killsAgainstRoboballmini,
            "KA_NULLIFIER": report.killsAgainstNullifier,
            "KA_PARENT": report.killsAgainstParent,
            "KA_MINIMUSHROOM": report.killsAgainstMinimushroom,
            "KA_LUNARWISP": report.killsAgainstLunarwisp,
            "KA_LUNARGOLEM": report.killsAgainstLunargolem,
            "KA_LUNAREXPLODER": report.killsAgainstLunarexploder,
            "KA_BEETLEQUEEN": report.killsAgainstBeetlequeen,
            "KA_CLAYBOSS": report.killsAgainstClayboss,
            "KA_TITAN": report.killsAgainstTitan,
            "KA_TITANGOLD": report.killsAgainstTitangold,
            "KA_VAGRANT": report.killsAgainstVagrant,
            "KA_MAGMAWORM": report.killsAgainstMagmaworm,
            "KA_ELECTRICWORM": report.killsAgainstElectricworm,
            "KA_IMPBOSS": report.killsAgainstImpboss,
            "KA_GRAVEKEEPER": report.killsAgainstGravekeeper,
            "KA_ROBOBALLBOSS": report.killsAgainstRoboballboss,
            "KA_SUPERROBOBALLBOSS": report.killsAgainstSuperroboballboss,
            "KA_SCAV": report.killsAgainstScav,
            "KA_SCAVLUNAR1": report.killsAgainstScavlunar1,
            "KA_SCAVLUNAR2": report.killsAgainstScavlunar2,
            "KA_SCAVLUNAR3": report.killsAgainstScavlunar3,
            "KA_SCAVLUNAR4": report.killsAgainstScavlunar4,
            "KA_GRANDPARENT": report.killsAgainstGrandparent,
            "KA_ARTIFACTSHELL": report.killsAgainstArtifactshell,
            "KA_BROTHER": report.killsAgainstBrother,
            "KAE_BEETLE": report.killsAgainstEliteBeetle,
            "KAE_BEETLEGUARD": report.killsAgainstEliteBeetleguard,
            "KAE_BISON": report.killsAgainstEliteBison,
            "KAE_GOLEM": report.killsAgainstEliteGolem,
            "KAE_WISP": report.killsAgainstEliteWisp,
            "KAE_GREATERWISP": report.killsAgainstEliteGreaterwisp,
            "KAE_LEMURIAN": report.killsAgainstEliteLemurian,
            "KAE_LEMURIANBRUISER": report.killsAgainstEliteLemurianbruiser,
            "KAE_IMP": report.killsAgainstEliteImp,
            "KAE_JELLYFISH": report.killsAgainstEliteJellyfish,
            "KAE_HERMITCRAB": report.killsAgainstEliteHermitcrab,
            "KAE_BELL": report.killsAgainstEliteBell,
            "KAE_CLAYBRUISER": report.killsAgainstEliteClaybruiser,
            "KAE_VULTURE": report.killsAgainstEliteVulture,
            "KAE_ROBOBALLMINI": report.killsAgainstEliteRoboballmini,
            "KAE_NULLIFIER": report.killsAgainstEliteNullifier,
            "KAE_PARENT": report.killsAgainstEliteParent,
            "KAE_MINIMUSHROOM": report.killsAgainstEliteMinimushroom,
            "KAE_LUNARWISP": report.killsAgainstEliteLunarwisp,
            "KAE_LUNARGOLEM": report.killsAgainstEliteLunargolem,
            "KAE_LUNAREXPLODER": report.killsAgainstEliteLunarexploder,
            "KAE_BEETLEQUEEN": report.killsAgainstEliteBeetlequeen,
            "KAE_CLAYBOSS": report.killsAgainstEliteClayboss,
            "KAE_TITAN": report.killsAgainstEliteTitan,
            "KAE_VAGRANT": report.killsAgainstEliteVagrant,
            "KAE_IMPBOSS": report.killsAgainstEliteImpboss,
            "KAE_GRAVEKEEPER": report.killsAgainstEliteGravekeeper,
            "KAE_ROBOBALLBOSS": report.killsAgainstEliteRoboballboss,
            "KAE_SCAV": report.killsAgainstEliteScav,
            "KAE_GRANDPARENT": report.killsAgainstEliteGrandparent
        }
    )
    
    cur.execute(
        '''
        INSERT INTO Purchases
        VALUES (:Run_ID, :Total_Gold_Collected, :Max_Gold_Collected, :Total_Purchases, :Highest_Purchases, :Total_Gold_Purchases, :Highest_Gold_Purchases, :Total_Blood_Purchases, :Highest_Blood_Purchases, :Total_Lunar_Purchases, :Highest_Lunar_Purchases, :Total_Drones_Purchased, :Total_Turrets_Purchased)
        ''',
        {
            "Run_ID": report.run_id,
            "Total_Gold_Collected": report.totalGoldCollected,
            "Max_Gold_Collected": report.maxGoldCollected,
            "Total_Purchases": report.totalPurchases,
            "Highest_Purchases": report.highestPurchases,
            "Total_Gold_Purchases": report.totalGoldPurchases,
            "Highest_Gold_Purchases": report.highestGoldPurchases,
            "Total_Blood_Purchases": report.totalBloodPurchases,
            "Highest_Blood_Purchases": report.highestBloodPurchases,
            "Total_Lunar_Purchases": report.totalLunarPurchases,
            "Highest_Lunar_Purchases": report.highestLunarPurchases,
            "Total_Drones_Purchased": report.totalDronesPurchased,
            "Total_Turrets_Purchased": report.totalTurretsPurchased
        }
    )
    
    cur.execute(
        '''
        INSERT INTO Item_Info
        VALUES (:Run_ID, :Total_Items_Collected, :Highest_Items_Collected, :TC_CLOVER, :TC_SYRINGE, :TC_BEAR, :TC_BEHEMOTH, :TC_MISSILE, :TC_EXPLODEONDEATH, :TC_DAGGER, :TC_TOOTH, :TC_CRITGLASSES, :TC_HOOF, :TC_FEATHER, :TC_CHAINLIGHTNING, :TC_SEED, :TC_ICICLE, :TC_GHOSTONKILL, :TC_MUSHROOM, :TC_CROWBAR, :TC_ATTACKSPEEDONCRIT, :TC_BLEEDONHIT, :TC_SPRINTOUTOFCOMBAT, :TC_FALLBOOTS, :TC_WARDONLEVEL, :TC_WARCRYONMULTIKILL, :TC_PHASING, :TC_HEALONCRIT, :TC_HEALWHILESAFE, :TC_JUMPBOOST, :TC_PERSONALSHIELD, :TC_NOVAONHEAL, :TC_MEDKIT, :TC_EQUIPMENTMAGAZINE, :TC_INFUSION, :TC_SHOCKNEARBY, :TC_IGNITEONKILL, :TC_BOUNCENEARBY, :TC_FIREWORK, :TC_BANDOLIER, :TC_STUNCHANCEONHIT, :TC_LUNARDAGGER, :TC_GOLDONHIT, :TC_SHIELDONLY, :TC_ALIENHEAD, :TC_TALISMAN, :TC_KNURL, :TC_BEETLEGLAND, :TC_SPRINTBONUS, :TC_SECONDARYSKILLMAGAZINE, :TC_STICKYBOMB, :TC_TREASURECACHE, :TC_BOSSDAMAGEBONUS, :TC_SPRINTARMOR, :TC_ICERING, :TC_FIRERING, :TC_SLOWONHIT, :TC_EXTRALIFE, :TC_UTILITYSKILLMAGAZINE, :TC_HEADHUNTER, :TC_KILLELITEFRENZY, :TC_INCREASEHEALING, :TC_REPEATHEAL, :TC_AUTOCASTEQUIPMENT, :TC_EXECUTELOWHEALTHELITE, :TC_ENERGIZEDONEQUIPMENTUSE, :TC_BARRIERONOVERHEAL, :TC_TITANGOLDDURINGTP, :TC_SPRINTWISP, :TC_BARRIERONKILL, :TC_ARMORREDUCTIONONHIT, :TC_TPHEALINGNOVA, :TC_NEARBYDAMAGEBONUS, :TC_LUNARUTILITYREPLACEMENT, :TC_THORNS, :TC_FLATHEALTH, :TC_PEARL, :TC_SHINYPEARL, :TC_BONUSGOLDPACKONKILL, :TC_LASERTURBINE, :TC_LUNARPRIMARYREPLACEMENT, :TC_NOVAONLOWHEALTH, :TC_LUNARTRINKET, :TC_REPULSIONARMORPLATE, :TC_SQUIDTURRET, :TC_DEATHMARK, :TC_INTERSTELLARDESKPLANT, :TC_FOCUSEDCONVERGENCE, :TC_FIREBALLSONHIT, :TC_LIGHTNINGSTRIKEONHIT, :TC_BLEEDONHITANDEXPLODE, :TC_SIPHONONLOWHEALTH, :TC_MONSTERSONSHRINEUSE, :TC_RANDOMDAMAGEZONE, :TC_ARTIFACTKEY, :TC_CAPTAINDEFENSEMATRIX, :TC_SCRAPWHITE, :TC_SCRAPGREEN, :TC_SCRAPRED, :TC_SCRAPYELLOW, :TC_LUNARBADLUCK, :TC_LUNARSECONDARYREPLACEMENT, :TC_ROBOBALLBUDDY, :TC_PARENTEGG, :TC_LUNARSPECIALREPLACEMENT, :HC_CLOVER, :HC_SYRINGE, :HC_BEAR, :HC_BEHEMOTH, :HC_MISSILE, :HC_EXPLODEONDEATH, :HC_DAGGER, :HC_TOOTH, :HC_CRITGLASSES, :HC_HOOF, :HC_FEATHER, :HC_CHAINLIGHTNING, :HC_SEED, :HC_ICICLE, :HC_GHOSTONKILL, :HC_MUSHROOM, :HC_CROWBAR, :HC_ATTACKSPEEDONCRIT, :HC_BLEEDONHIT, :HC_SPRINTOUTOFCOMBAT, :HC_FALLBOOTS, :HC_WARDONLEVEL, :HC_WARCRYONMULTIKILL, :HC_PHASING, :HC_HEALONCRIT, :HC_HEALWHILESAFE, :HC_JUMPBOOST, :HC_PERSONALSHIELD, :HC_NOVAONHEAL, :HC_MEDKIT, :HC_EQUIPMENTMAGAZINE, :HC_INFUSION, :HC_SHOCKNEARBY, :HC_IGNITEONKILL, :HC_BOUNCENEARBY, :HC_FIREWORK, :HC_BANDOLIER, :HC_STUNCHANCEONHIT, :HC_LUNARDAGGER, :HC_GOLDONHIT, :HC_SHIELDONLY, :HC_ALIENHEAD, :HC_TALISMAN, :HC_KNURL, :HC_BEETLEGLAND, :HC_SPRINTBONUS, :HC_SECONDARYSKILLMAGAZINE, :HC_STICKYBOMB, :HC_TREASURECACHE, :HC_BOSSDAMAGEBONUS, :HC_SPRINTARMOR, :HC_ICERING, :HC_FIRERING, :HC_SLOWONHIT, :HC_EXTRALIFE, :HC_UTILITYSKILLMAGAZINE, :HC_HEADHUNTER, :HC_KILLELITEFRENZY, :HC_INCREASEHEALING, :HC_REPEATHEAL, :HC_AUTOCASTEQUIPMENT, :HC_EXECUTELOWHEALTHELITE, :HC_ENERGIZEDONEQUIPMENTUSE, :HC_BARRIERONOVERHEAL, :HC_TITANGOLDDURINGTP, :HC_SPRINTWISP, :HC_BARRIERONKILL, :HC_ARMORREDUCTIONONHIT, :HC_TPHEALINGNOVA, :HC_NEARBYDAMAGEBONUS, :HC_LUNARUTILITYREPLACEMENT, :HC_THORNS, :HC_FLATHEALTH, :HC_PEARL, :HC_SHINYPEARL, :HC_BONUSGOLDPACKONKILL, :HC_LASERTURBINE, :HC_LUNARPRIMARYREPLACEMENT, :HC_NOVAONLOWHEALTH, :HC_LUNARTRINKET, :HC_REPULSIONARMORPLATE, :HC_SQUIDTURRET, :HC_DEATHMARK, :HC_INTERSTELLARDESKPLANT, :HC_FOCUSEDCONVERGENCE, :HC_FIREBALLSONHIT, :HC_LIGHTNINGSTRIKEONHIT, :HC_BLEEDONHITANDEXPLODE, :HC_SIPHONONLOWHEALTH, :HC_MONSTERSONSHRINEUSE, :HC_RANDOMDAMAGEZONE, :HC_ARTIFACTKEY, :HC_CAPTAINDEFENSEMATRIX, :HC_SCRAPWHITE, :HC_SCRAPGREEN, :HC_SCRAPRED, :HC_SCRAPYELLOW, :HC_LUNARBADLUCK, :HC_LUNARSECONDARYREPLACEMENT, :HC_ROBOBALLBUDDY, :HC_PARENTEGG, :HC_LUNARSPECIALREPLACEMENT)
        ''',
        {
            "Run_ID": report.run_id,
            "Total_Items_Collected": report.totalItemsCollected,
            "Highest_Items_Collected": report.highestItemsCollected,
            "TC_CLOVER": report.totalCollectedClover,
            "TC_SYRINGE": report.totalCollectedSyringe,
            "TC_BEAR": report.totalCollectedBear,
            "TC_BEHEMOTH": report.totalCollectedBehemoth,
            "TC_MISSILE": report.totalCollectedMissile,
            "TC_EXPLODEONDEATH": report.totalCollectedExplodeondeath,
            "TC_DAGGER": report.totalCollectedDagger,
            "TC_TOOTH": report.totalCollectedTooth,
            "TC_CRITGLASSES": report.totalCollectedCritglasses,
            "TC_HOOF": report.totalCollectedHoof,
            "TC_FEATHER": report.totalCollectedFeather,
            "TC_CHAINLIGHTNING": report.totalCollectedChainlightning,
            "TC_SEED": report.totalCollectedSeed,
            "TC_ICICLE": report.totalCollectedIcicle,
            "TC_GHOSTONKILL": report.totalCollectedGhostonkill,
            "TC_MUSHROOM": report.totalCollectedMushroom,
            "TC_CROWBAR": report.totalCollectedCrowbar,
            "TC_ATTACKSPEEDONCRIT": report.totalCollectedAttackspeedoncrit,
            "TC_BLEEDONHIT": report.totalCollectedBleedonhit,
            "TC_SPRINTOUTOFCOMBAT": report.totalCollectedSprintoutofcombat,
            "TC_FALLBOOTS": report.totalCollectedFallboots,
            "TC_WARDONLEVEL": report.totalCollectedWardonlevel,
            "TC_WARCRYONMULTIKILL": report.totalCollectedWarcryonmultikill,
            "TC_PHASING": report.totalCollectedPhasing,
            "TC_HEALONCRIT": report.totalCollectedHealoncrit,
            "TC_HEALWHILESAFE": report.totalCollectedHealwhilesafe,
            "TC_JUMPBOOST": report.totalCollectedJumpboost,
            "TC_PERSONALSHIELD": report.totalCollectedPersonalshield,
            "TC_NOVAONHEAL": report.totalCollectedNovaonheal,
            "TC_MEDKIT": report.totalCollectedMedkit,
            "TC_EQUIPMENTMAGAZINE": report.totalCollectedEquipmentmagazine,
            "TC_INFUSION": report.totalCollectedInfusion,
            "TC_SHOCKNEARBY": report.totalCollectedShocknearby,
            "TC_IGNITEONKILL": report.totalCollectedIgniteonkill,
            "TC_BOUNCENEARBY": report.totalCollectedBouncenearby,
            "TC_FIREWORK": report.totalCollectedFirework,
            "TC_BANDOLIER": report.totalCollectedBandolier,
            "TC_STUNCHANCEONHIT": report.totalCollectedStunchanceonhit,
            "TC_LUNARDAGGER": report.totalCollectedLunardagger,
            "TC_GOLDONHIT": report.totalCollectedGoldonhit,
            "TC_SHIELDONLY": report.totalCollectedShieldonly,
            "TC_ALIENHEAD": report.totalCollectedAlienhead,
            "TC_TALISMAN": report.totalCollectedTalisman,
            "TC_KNURL": report.totalCollectedKnurl,
            "TC_BEETLEGLAND": report.totalCollectedBeetlegland,
            "TC_SPRINTBONUS": report.totalCollectedSprintbonus,
            "TC_SECONDARYSKILLMAGAZINE": report.totalCollectedSecondaryskillmagazine,
            "TC_STICKYBOMB": report.totalCollectedStickybomb,
            "TC_TREASURECACHE": report.totalCollectedTreasurecache,
            "TC_BOSSDAMAGEBONUS": report.totalCollectedBossdamagebonus,
            "TC_SPRINTARMOR": report.totalCollectedSprintarmor,
            "TC_ICERING": report.totalCollectedIcering,
            "TC_FIRERING": report.totalCollectedFirering,
            "TC_SLOWONHIT": report.totalCollectedSlowonhit,
            "TC_EXTRALIFE": report.totalCollectedExtralife,
            "TC_UTILITYSKILLMAGAZINE": report.totalCollectedUtilityskillmagazine,
            "TC_HEADHUNTER": report.totalCollectedHeadhunter,
            "TC_KILLELITEFRENZY": report.totalCollectedKillelitefrenzy,
            "TC_INCREASEHEALING": report.totalCollectedIncreasehealing,
            "TC_REPEATHEAL": report.totalCollectedRepeatheal,
            "TC_AUTOCASTEQUIPMENT": report.totalCollectedAutocastequipment,
            "TC_EXECUTELOWHEALTHELITE": report.totalCollectedExecutelowhealthelite,
            "TC_ENERGIZEDONEQUIPMENTUSE": report.totalCollectedEnergizedonequipmentuse,
            "TC_BARRIERONOVERHEAL": report.totalCollectedBarrieronoverheal,
            "TC_TITANGOLDDURINGTP": report.totalCollectedTitangoldduringtp,
            "TC_SPRINTWISP": report.totalCollectedSprintwisp,
            "TC_BARRIERONKILL": report.totalCollectedBarrieronkill,
            "TC_ARMORREDUCTIONONHIT": report.totalCollectedArmorreductiononhit,
            "TC_TPHEALINGNOVA": report.totalCollectedTphealingnova,
            "TC_NEARBYDAMAGEBONUS": report.totalCollectedNearbydamagebonus,
            "TC_LUNARUTILITYREPLACEMENT": report.totalCollectedLunarutilityreplacement,
            "TC_THORNS": report.totalCollectedThorns,
            "TC_FLATHEALTH": report.totalCollectedFlathealth,
            "TC_PEARL": report.totalCollectedPearl,
            "TC_SHINYPEARL": report.totalCollectedShinypearl,
            "TC_BONUSGOLDPACKONKILL": report.totalCollectedBonusgoldpackonkill,
            "TC_LASERTURBINE": report.totalCollectedLaserturbine,
            "TC_LUNARPRIMARYREPLACEMENT": report.totalCollectedLunarprimaryreplacement,
            "TC_NOVAONLOWHEALTH": report.totalCollectedNovaonlowhealth,
            "TC_LUNARTRINKET": report.totalCollectedLunartrinket,
            "TC_REPULSIONARMORPLATE": report.totalCollectedRepulsionarmorplate,
            "TC_SQUIDTURRET": report.totalCollectedSquidturret,
            "TC_DEATHMARK": report.totalCollectedDeathmark,
            "TC_INTERSTELLARDESKPLANT": report.totalCollectedInterstellardeskplant,
            "TC_FOCUSEDCONVERGENCE": report.totalCollectedFocusedconvergence,
            "TC_FIREBALLSONHIT": report.totalCollectedFireballsonhit,
            "TC_LIGHTNINGSTRIKEONHIT": report.totalCollectedLightningstrikeonhit,
            "TC_BLEEDONHITANDEXPLODE": report.totalCollectedBleedonhitandexplode,
            "TC_SIPHONONLOWHEALTH": report.totalCollectedSiphononlowhealth,
            "TC_MONSTERSONSHRINEUSE": report.totalCollectedMonstersonshrineuse,
            "TC_RANDOMDAMAGEZONE": report.totalCollectedRandomdamagezone,
            "TC_ARTIFACTKEY": report.totalCollectedArtifactkey,
            "TC_CAPTAINDEFENSEMATRIX": report.totalCollectedCaptaindefensematrix,
            "TC_SCRAPWHITE": report.totalCollectedScrapwhite,
            "TC_SCRAPGREEN": report.totalCollectedScrapgreen,
            "TC_SCRAPRED": report.totalCollectedScrapred,
            "TC_SCRAPYELLOW": report.totalCollectedScrapyellow,
            "TC_LUNARBADLUCK": report.totalCollectedLunarbadluck,
            "TC_LUNARSECONDARYREPLACEMENT": report.totalCollectedLunarsecondaryreplacement,
            "TC_ROBOBALLBUDDY": report.totalCollectedRoboballbuddy,
            "TC_PARENTEGG": report.totalCollectedParentegg,
            "TC_LUNARSPECIALREPLACEMENT": report.totalCollectedLunarspecialreplacement,
            "HC_CLOVER": report.highestCollectedClover,
            "HC_SYRINGE": report.highestCollectedSyringe,
            "HC_BEAR": report.highestCollectedBear,
            "HC_BEHEMOTH": report.highestCollectedBehemoth,
            "HC_MISSILE": report.highestCollectedMissile,
            "HC_EXPLODEONDEATH": report.highestCollectedExplodeondeath,
            "HC_DAGGER": report.highestCollectedDagger,
            "HC_TOOTH": report.highestCollectedTooth,
            "HC_CRITGLASSES": report.highestCollectedCritglasses,
            "HC_HOOF": report.highestCollectedHoof,
            "HC_FEATHER": report.highestCollectedFeather,
            "HC_CHAINLIGHTNING": report.highestCollectedChainlightning,
            "HC_SEED": report.highestCollectedSeed,
            "HC_ICICLE": report.highestCollectedIcicle,
            "HC_GHOSTONKILL": report.highestCollectedGhostonkill,
            "HC_MUSHROOM": report.highestCollectedMushroom,
            "HC_CROWBAR": report.highestCollectedCrowbar,
            "HC_ATTACKSPEEDONCRIT": report.highestCollectedAttackspeedoncrit,
            "HC_BLEEDONHIT": report.highestCollectedBleedonhit,
            "HC_SPRINTOUTOFCOMBAT": report.highestCollectedSprintoutofcombat,
            "HC_FALLBOOTS": report.highestCollectedFallboots,
            "HC_WARDONLEVEL": report.highestCollectedWardonlevel,
            "HC_WARCRYONMULTIKILL": report.highestCollectedWarcryonmultikill,
            "HC_PHASING": report.highestCollectedPhasing,
            "HC_HEALONCRIT": report.highestCollectedHealoncrit,
            "HC_HEALWHILESAFE": report.highestCollectedHealwhilesafe,
            "HC_JUMPBOOST": report.highestCollectedJumpboost,
            "HC_PERSONALSHIELD": report.highestCollectedPersonalshield,
            "HC_NOVAONHEAL": report.highestCollectedNovaonheal,
            "HC_MEDKIT": report.highestCollectedMedkit,
            "HC_EQUIPMENTMAGAZINE": report.highestCollectedEquipmentmagazine,
            "HC_INFUSION": report.highestCollectedInfusion,
            "HC_SHOCKNEARBY": report.highestCollectedShocknearby,
            "HC_IGNITEONKILL": report.highestCollectedIgniteonkill,
            "HC_BOUNCENEARBY": report.highestCollectedBouncenearby,
            "HC_FIREWORK": report.highestCollectedFirework,
            "HC_BANDOLIER": report.highestCollectedBandolier,
            "HC_STUNCHANCEONHIT": report.highestCollectedStunchanceonhit,
            "HC_LUNARDAGGER": report.highestCollectedLunardagger,
            "HC_GOLDONHIT": report.highestCollectedGoldonhit,
            "HC_SHIELDONLY": report.highestCollectedShieldonly,
            "HC_ALIENHEAD": report.highestCollectedAlienhead,
            "HC_TALISMAN": report.highestCollectedTalisman,
            "HC_KNURL": report.highestCollectedKnurl,
            "HC_BEETLEGLAND": report.highestCollectedBeetlegland,
            "HC_SPRINTBONUS": report.highestCollectedSprintbonus,
            "HC_SECONDARYSKILLMAGAZINE": report.highestCollectedSecondaryskillmagazine,
            "HC_STICKYBOMB": report.highestCollectedStickybomb,
            "HC_TREASURECACHE": report.highestCollectedTreasurecache,
            "HC_BOSSDAMAGEBONUS": report.highestCollectedBossdamagebonus,
            "HC_SPRINTARMOR": report.highestCollectedSprintarmor,
            "HC_ICERING": report.highestCollectedIcering,
            "HC_FIRERING": report.highestCollectedFirering,
            "HC_SLOWONHIT": report.highestCollectedSlowonhit,
            "HC_EXTRALIFE": report.highestCollectedExtralife,
            "HC_UTILITYSKILLMAGAZINE": report.highestCollectedUtilityskillmagazine,
            "HC_HEADHUNTER": report.highestCollectedHeadhunter,
            "HC_KILLELITEFRENZY": report.highestCollectedKillelitefrenzy,
            "HC_INCREASEHEALING": report.highestCollectedIncreasehealing,
            "HC_REPEATHEAL": report.highestCollectedRepeatheal,
            "HC_AUTOCASTEQUIPMENT": report.highestCollectedAutocastequipment,
            "HC_EXECUTELOWHEALTHELITE": report.highestCollectedExecutelowhealthelite,
            "HC_ENERGIZEDONEQUIPMENTUSE": report.highestCollectedEnergizedonequipmentuse,
            "HC_BARRIERONOVERHEAL": report.highestCollectedBarrieronoverheal,
            "HC_TITANGOLDDURINGTP": report.highestCollectedTitangoldduringtp,
            "HC_SPRINTWISP": report.highestCollectedSprintwisp,
            "HC_BARRIERONKILL": report.highestCollectedBarrieronkill,
            "HC_ARMORREDUCTIONONHIT": report.highestCollectedArmorreductiononhit,
            "HC_TPHEALINGNOVA": report.highestCollectedTphealingnova,
            "HC_NEARBYDAMAGEBONUS": report.highestCollectedNearbydamagebonus,
            "HC_LUNARUTILITYREPLACEMENT": report.highestCollectedLunarutilityreplacement,
            "HC_THORNS": report.highestCollectedThorns,
            "HC_FLATHEALTH": report.highestCollectedFlathealth,
            "HC_PEARL": report.highestCollectedPearl,
            "HC_SHINYPEARL": report.highestCollectedShinypearl,
            "HC_BONUSGOLDPACKONKILL": report.highestCollectedBonusgoldpackonkill,
            "HC_LASERTURBINE": report.highestCollectedLaserturbine,
            "HC_LUNARPRIMARYREPLACEMENT": report.highestCollectedLunarprimaryreplacement,
            "HC_NOVAONLOWHEALTH": report.highestCollectedNovaonlowhealth,
            "HC_LUNARTRINKET": report.highestCollectedLunartrinket,
            "HC_REPULSIONARMORPLATE": report.highestCollectedRepulsionarmorplate,
            "HC_SQUIDTURRET": report.highestCollectedSquidturret,
            "HC_DEATHMARK": report.highestCollectedDeathmark,
            "HC_INTERSTELLARDESKPLANT": report.highestCollectedInterstellardeskplant,
            "HC_FOCUSEDCONVERGENCE": report.highestCollectedFocusedconvergence,
            "HC_FIREBALLSONHIT": report.highestCollectedFireballsonhit,
            "HC_LIGHTNINGSTRIKEONHIT": report.highestCollectedLightningstrikeonhit,
            "HC_BLEEDONHITANDEXPLODE": report.highestCollectedBleedonhitandexplode,
            "HC_SIPHONONLOWHEALTH": report.highestCollectedSiphononlowhealth,
            "HC_MONSTERSONSHRINEUSE": report.highestCollectedMonstersonshrineuse,
            "HC_RANDOMDAMAGEZONE": report.highestCollectedRandomdamagezone,
            "HC_ARTIFACTKEY": report.highestCollectedArtifactkey,
            "HC_CAPTAINDEFENSEMATRIX": report.highestCollectedCaptaindefensematrix,
            "HC_SCRAPWHITE": report.highestCollectedScrapwhite,
            "HC_SCRAPGREEN": report.highestCollectedScrapgreen,
            "HC_SCRAPRED": report.highestCollectedScrapred,
            "HC_SCRAPYELLOW": report.highestCollectedScrapyellow,
            "HC_LUNARBADLUCK": report.highestCollectedLunarbadluck,
            "HC_LUNARSECONDARYREPLACEMENT": report.highestCollectedLunarsecondaryreplacement,
            "HC_ROBOBALLBUDDY": report.highestCollectedRoboballbuddy,
            "HC_PARENTEGG": report.highestCollectedParentegg,
            "HC_LUNARSPECIALREPLACEMENT": report.highestCollectedLunarspecialreplacement
        }
    )
    
    cur.execute(
        '''
        INSERT INTO Equipment_Info
        VALUES (:Run_ID, :TH_COMMANDMISSILE, :TH_FRUIT, :TH_METEOR, :TH_BLACKHOLE, :TH_CRITONUSE, :TH_DRONEBACKUP, :TH_BFG, :TH_JETPACK, :TH_LIGHTNING, :TH_GOLDGAT, :TH_PASSIVEHEALING, :TH_BURNNEARBY, :TH_SCANNER, :TH_CRIPPLEWARD, :TH_GATEWAY, :TH_TONIC, :TH_CLEANSE, :TH_FIREBALLDASH, :TH_GAINARMOR, :TH_SAWMERANG, :TH_RECYCLER, :TH_LIFESTEALONHIT, :TH_TEAMWARCRY, :TH_DEATHPROJECTILE, :TF_COMMANDMISSILE, :TF_FRUIT, :TF_METEOR, :TF_BLACKHOLE, :TF_CRITONUSE, :TF_DRONEBACKUP, :TF_BFG, :TF_JETPACK, :TF_LIGHTNING, :TF_GOLDGAT, :TF_PASSIVEHEALING, :TF_BURNNEARBY, :TF_SCANNER, :TF_CRIPPLEWARD, :TF_GATEWAY, :TF_TONIC, :TF_CLEANSE, :TF_FIREBALLDASH, :TF_GAINARMOR, :TF_SAWMERANG, :TF_RECYCLER, :TF_LIFESTEALONHIT, :TF_TEAMWARCRY, :TF_DEATHPROJECTILE)
        ''',
        {
            "Run_ID": report.run_id,
            "TH_COMMANDMISSILE": report.timeHeldCommandmissile,
            "TH_FRUIT": report.timeHeldFruit,
            "TH_METEOR": report.timeHeldMeteor,
            "TH_BLACKHOLE": report.timeHeldBlackhole,
            "TH_CRITONUSE": report.timeHeldCritonuse,
            "TH_DRONEBACKUP": report.timeHeldDronebackup,
            "TH_BFG": report.timeHeldBfg,
            "TH_JETPACK": report.timeHeldJetpack,
            "TH_LIGHTNING": report.timeHeldLightning,
            "TH_GOLDGAT": report.timeHeldGoldgat,
            "TH_PASSIVEHEALING": report.timeHeldPassivehealing,
            "TH_BURNNEARBY": report.timeHeldBurnnearby,
            "TH_SCANNER": report.timeHeldScanner,
            "TH_CRIPPLEWARD": report.timeHeldCrippleward,
            "TH_GATEWAY": report.timeHeldGateway,
            "TH_TONIC": report.timeHeldTonic,
            "TH_CLEANSE": report.timeHeldCleanse,
            "TH_FIREBALLDASH": report.timeHeldFireballdash,
            "TH_GAINARMOR": report.timeHeldGainarmor,
            "TH_SAWMERANG": report.timeHeldSawmerang,
            "TH_RECYCLER": report.timeHeldRecycler,
            "TH_LIFESTEALONHIT": report.timeHeldLifestealonhit,
            "TH_TEAMWARCRY": report.timeHeldTeamwarcry,
            "TH_DEATHPROJECTILE": report.timeHeldDeathprojectile,
            "TF_COMMANDMISSILE": report.timesFiredCommandmissile,
            "TF_FRUIT": report.timesFiredFruit,
            "TF_METEOR": report.timesFiredMeteor,
            "TF_BLACKHOLE": report.timesFiredBlackhole,
            "TF_CRITONUSE": report.timesFiredCritonuse,
            "TF_DRONEBACKUP": report.timesFiredDronebackup,
            "TF_BFG": report.timesFiredBfg,
            "TF_JETPACK": report.timesFiredJetpack,
            "TF_LIGHTNING": report.timesFiredLightning,
            "TF_GOLDGAT": report.timesFiredGoldgat,
            "TF_PASSIVEHEALING": report.timesFiredPassivehealing,
            "TF_BURNNEARBY": report.timesFiredBurnnearby,
            "TF_SCANNER": report.timesFiredScanner,
            "TF_CRIPPLEWARD": report.timesFiredCrippleward,
            "TF_GATEWAY": report.timesFiredGateway,
            "TF_TONIC": report.timesFiredTonic,
            "TF_CLEANSE": report.timesFiredCleanse,
            "TF_FIREBALLDASH": report.timesFiredFireballdash,
            "TF_GAINARMOR": report.timesFiredGainarmor,
            "TF_SAWMERANG": report.timesFiredSawmerang,
            "TF_RECYCLER": report.timesFiredRecycler,
            "TF_LIFESTEALONHIT": report.timesFiredLifestealonhit,
            "TF_TEAMWARCRY": report.timesFiredTeamwarcry,
            "TF_DEATHPROJECTILE": report.timesFiredDeathprojectile
        }
    )
    
    cur.execute(
        '''
        INSERT INTO Stage_Info
        VALUES (:Run_ID, :Total_Stages_Completed, :Highest_Stages_Completed, :TV_BLACKBEACH, :TV_GOLEMPLAINS, :TV_GOOLAKE, :TV_BAZAAR, :TV_FROZENWALL, :TV_FOGGYSWAMP, :TV_DAMPCAVE, :TV_WISPGRAVEYARD, :TV_MYSTERYSPACE, :TV_GOLDSHORES, :TV_SHIPGRAVEYARD, :TV_ROOTJUNGLE, :TV_ARENA, :TV_LIMBO, :TV_SKYMEADOW, :TV_ARTIFACTWORLD, :TV_MOON, :TC_BLACKBEACH, :TC_GOLEMPLAINS, :TC_GOOLAKE, :TC_BAZAAR, :TC_FROZENWALL, :TC_FOGGYSWAMP, :TC_DAMPCAVE, :TC_WISPGRAVEYARD, :TC_MYSTERYSPACE, :TC_GOLDSHORES, :TC_SHIPGRAVEYARD, :TC_ROOTJUNGLE, :TC_ARENA, :TC_LIMBO, :TC_SKYMEADOW, :TC_ARTIFACTWORLD, :TC_MOON)
        ''',
        {
            "Run_ID": report.run_id,
            "Total_Stages_Completed": report.totalStagesCompleted,
            "Highest_Stages_Completed": report.highestStagesCompleted,
            "TV_BLACKBEACH": report.timesVisitedBlackbeach,
            "TV_GOLEMPLAINS": report.timesVisitedGolemplains,
            "TV_GOOLAKE": report.timesVisitedGoolake,
            "TV_BAZAAR": report.timesVisitedBazaar,
            "TV_FROZENWALL": report.timesVisitedFrozenwall,
            "TV_FOGGYSWAMP": report.timesVisitedFoggyswamp,
            "TV_DAMPCAVE": report.timesVisitedDampcave,
            "TV_WISPGRAVEYARD": report.timesVisitedWispgraveyard,
            "TV_MYSTERYSPACE": report.timesVisitedMysteryspace,
            "TV_GOLDSHORES": report.timesVisitedGoldshores,
            "TV_SHIPGRAVEYARD": report.timesVisitedShipgraveyard,
            "TV_ROOTJUNGLE": report.timesVisitedRootjungle,
            "TV_ARENA": report.timesVisitedArena,
            "TV_LIMBO": report.timesVisitedLimbo,
            "TV_SKYMEADOW": report.timesVisitedSkymeadow,
            "TV_ARTIFACTWORLD": report.timesVisitedArtifactworld,
            "TV_MOON": report.timesVisitedMoon,
            "TC_BLACKBEACH": report.timesClearedBlackbeach,
            "TC_GOLEMPLAINS": report.timesClearedGolemplains,
            "TC_GOOLAKE": report.timesClearedGoolake,
            "TC_BAZAAR": report.timesClearedBazaar,
            "TC_FROZENWALL": report.timesClearedFrozenwall,
            "TC_FOGGYSWAMP": report.timesClearedFoggyswamp,
            "TC_DAMPCAVE": report.timesClearedDampcave,
            "TC_WISPGRAVEYARD": report.timesClearedWispgraveyard,
            "TC_MYSTERYSPACE": report.timesClearedMysteryspace,
            "TC_GOLDSHORES": report.timesClearedGoldshores,
            "TC_SHIPGRAVEYARD": report.timesClearedShipgraveyard,
            "TC_ROOTJUNGLE": report.timesClearedRootjungle,
            "TC_ARENA": report.timesClearedArena,
            "TC_LIMBO": report.timesClearedLimbo,
            "TC_SKYMEADOW": report.timesClearedSkymeadow,
            "TC_ARTIFACTWORLD": report.timesClearedArtifactworld,
            "TC_MOON": report.timesClearedMoon
        }
    )
    
    con.commit()

for run in runs:
    data_entry(run)

# Update most recent run date
try:
    most_recent = max([run.date for run in runs])

    update_recent_run_setting(settings, most_recent)

except ValueError:
    print('No new runs!')

settings_file.close()
con.close()