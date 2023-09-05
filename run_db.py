import sqlite3
import pandas as pd
from datetime import datetime as dt
from os import listdir
from os.path import isfile, getctime
from models.run_report import Run_Report

DEFAULT_DIR_PATH = 'C:\\SteamLibrary\\steamapps\\common\\Risk of Rain 2\\Risk of Rain 2_Data\\RunReports\\History\\'
DEFAULT_MOST_RECENT_RUN_DATE = '2019-01-01 00:00:00'
DEFAULT_EXPORT_PATH = 'C:\\Users\\Default\\Documents\\'
SETTINGS_FILE_PATH = 'settings.txt'

con = sqlite3.connect('db/run_report_db.db')
cur = con.cursor()

# Read settigns file
try:
    # Convert settings file to dict
    with open(SETTINGS_FILE_PATH, 'r') as settings_file:
        settings = {}
        for line in settings_file.readlines():
            key,value = line.split(' = ')
            settings[key]=value.strip()

except FileNotFoundError:
    # Create settings file if one doesn't exist
    with open(SETTINGS_FILE_PATH, 'w') as settings_file:
        settings_file.writelines(f'dir_path = {DEFAULT_DIR_PATH}\n')
        settings_file.writelines(f'most_recent_run_date = {DEFAULT_MOST_RECENT_RUN_DATE}\n')
        settings_file.writelines(f'export_path = {DEFAULT_EXPORT_PATH}\n')
        
        # Initialize default dict
        settings = {'dir_path':DEFAULT_DIR_PATH, 'most_recent_run_date':DEFAULT_MOST_RECENT_RUN_DATE, 'export_path':DEFAULT_EXPORT_PATH}


def update_recent_run_setting(most_recent_run):
    # Increment most recent date by 1 second
    new_date = most_recent_run.replace(second=most_recent_run.second+1)

    # Read last run time from settings.txt
    with open(SETTINGS_FILE_PATH, 'r') as settings_file:
        init_settings=settings_file.readlines()
    
    # Update the most recent run time
    init_settings[1] = f'most_recent_run_date = {new_date}\n'

    # Writ updated settings.txt
    with open(SETTINGS_FILE_PATH, 'w') as new_settings:
        new_settings.writelines(init_settings)


def export_tables(table_name):
    # Get table field names
    con.row_factory = sqlite3.Row
    h_cur = con.execute(f'SELECT * FROM {table_name}')
    h_row = h_cur.fetchone()
    fields = h_row.keys()

    # Get table data
    res = cur.execute(f'SELECT * FROM {table_name}')
    data = res.fetchall()
    
    # Name export file
    export_path = settings['export_path'] + table_name + '.csv'
    
    # Create dataframe for table and export it as a CSV
    df = pd.DataFrame(data=data, columns=fields)
    df.to_csv(export_path, index=False)


dir_path = settings["dir_path"]
last_run = dt.strptime(settings['most_recent_run_date'],'%Y-%m-%d %H:%M:%S')

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
        VALUES (:Run_ID, :Total_Minion_Damage_Dealt, :Total_Damage_Dealt, :Total_Damage_Taken, :Total_Health_Healed, :Highest_Damage_Dealt, :DDT_BEETLE, :DDT_BEETLEGUARD, :DDT_BISON, :DDT_GOLEM, :DDT_WISP, :DDT_GREATERWISP, :DDT_LEMURIAN, :DDT_LEMURIANBRUISER, :DDT_IMP, :DDT_JELLYFISH, :DDT_CLAY, :DDT_HERMIT_CRAB, :DDT_BELL, :DDT_CLAYBRUISER, :DDT_VULTURE, :DDT_ROBOBALLMINI, :DDT_NULLIFIER, :DDT_PARENT, :DDT_MINIMUSHROOM, :DDT_POD, :DDT_LUNARWISP, :DDT_LUNARGOLEM, :DDT_LUNAREXPLODER, :DDT_BEETLEQUEEN, :DDT_CLAYBOSS, :DDT_TITAN, :DDT_TITANGOLD, :DDT_VAGRANT, :DDT_MAGMAWORM, :DDT_ELECTRICWORM, :DDT_IMPBOSS, :DDT_GRAVEKEEPER, :DDT_ROBOBALLBOSS, :DDT_SUPERROBOBALLBOSS, :DDT_SCAV, :DDT_SCAVLUNAR1, :DDT_SCAVLUNAR2, :DDT_SCAVLUNAR3, :DDT_SCAVLUNAR4, :DDT_GRANDPARENT, :DDT_ARTIFACTSHELL, :DDT_BROTHER, :DDT_VERMIN, :DDT_FLYINGVERMIN, :DDT_CLAYGRENADIER, :DDT_GUP, :DDT_GEEP, :DDT_GIP, :DDT_SULFURPOD, :DDT_ACIDLARVA, :DDT_MINORCONSTRUCT, :DDT_MEGACONSTRUCT, :DDT_VOIDMEGACRAB, :DDT_VOIDRAIDCRAB, :DDT_VOIDBARNACLE, :DDT_VOIDJAILER, :DDT_ASSASSIN2, :DDT_VOIDINFESTOR, :DTF_BEETLE, :DTF_BEETLEGUARD, :DTF_BISON, :DTF_GOLEM, :DTF_WISP, :DTF_GREATERWISP, :DTF_LEMURIAN, :DTF_LEMURIANBRUISER, :DTF_IMP, :DTF_JELLYFISH, :DTF_CLAY, :DTF_HERMIT_CRAB, :DTF_BELL, :DTF_CLAYBRUISER, :DTF_VULTURE, :DTF_ROBOBALLMINI, :DTF_NULLIFIER, :DTF_PARENT, :DTF_MINIMUSHROOM, :DTF_POD, :DTF_LUNARWISP, :DTF_LUNARGOLEM, :DTF_LUNAREXPLODER, :DTF_BEETLEQUEEN, :DTF_CLAYBOSS, :DTF_TITAN, :DTF_TITANGOLD, :DTF_VAGRANT, :DTF_MAGMAWORM, :DTF_ELECTRICWORM, :DTF_IMPBOSS, :DTF_GRAVEKEEPER, :DTF_ROBOBALLBOSS, :DTF_SUPERROBOBALLBOSS, :DTF_SCAV, :DTF_SCAVLUNAR1, :DTF_SCAVLUNAR2, :DTF_SCAVLUNAR3, :DTF_SCAVLUNAR4, :DTF_GRANDPARENT, :DTF_ARTIFACTSHELL, :DTF_BROTHER, :DTF_VERMIN, :DTF_FLYINGVERMIN, :DTF_CLAYGRENADIER, :DTF_GUP, :DTF_GEEP, :DTF_GIP, :DTF_SULFURPOD, :DTF_ACIDLARVA, :DTF_MINORCONSTRUCT, :DTF_MEGACONSTRUCT, :DTF_VOIDMEGACRAB, :DTF_VOIDRAIDCRAB, :DTF_VOIDBARNACLE, :DTF_VOIDJAILER, :DTF_ASSASSIN2, :DTF_VOIDINFESTOR)
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
            "DDT_CLAY": report.damageDealtToClay,
            "DDT_HERMIT_CRAB": report.damageDealtToHermit_Crab,
            "DDT_BELL": report.damageDealtToBell,
            "DDT_CLAYBRUISER": report.damageDealtToClaybruiser,
            "DDT_VULTURE": report.damageDealtToVulture,
            "DDT_ROBOBALLMINI": report.damageDealtToRoboballmini,
            "DDT_NULLIFIER": report.damageDealtToNullifier,
            "DDT_PARENT": report.damageDealtToParent,
            "DDT_MINIMUSHROOM": report.damageDealtToMinimushroom,
            "DDT_POD": report.damageDealtToPod,
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
            "DDT_VERMIN": report.damageDealtToVermin,
            "DDT_FLYINGVERMIN": report.damageDealtToFlyingvermin,
            "DDT_CLAYGRENADIER": report.damageDealtToClaygrenadier,
            "DDT_GUP": report.damageDealtToGup,
            "DDT_GEEP": report.damageDealtToGeep,
            "DDT_GIP": report.damageDealtToGip,
            "DDT_SULFURPOD": report.damageDealtToSulfurpod,
            "DDT_ACIDLARVA": report.damageDealtToAcidlarva,
            "DDT_MINORCONSTRUCT": report.damageDealtToMinorconstruct,
            "DDT_MEGACONSTRUCT": report.damageDealtToMegaconstruct,
            "DDT_VOIDMEGACRAB": report.damageDealtToVoidmegacrab,
            "DDT_VOIDRAIDCRAB": report.damageDealtToVoidraidcrab,
            "DDT_VOIDBARNACLE": report.damageDealtToVoidbarnacle,
            "DDT_VOIDJAILER": report.damageDealtToVoidjailer,
            "DDT_ASSASSIN2": report.damageDealtToAssassin2,
            "DDT_VOIDINFESTOR": report.damageDealtToVoidinfestor,
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
            "DTF_CLAY": report.damageTakenFromClay,
            "DTF_HERMIT_CRAB": report.damageTakenFromHermit_Crab,
            "DTF_BELL": report.damageTakenFromBell,
            "DTF_CLAYBRUISER": report.damageTakenFromClaybruiser,
            "DTF_VULTURE": report.damageTakenFromVulture,
            "DTF_ROBOBALLMINI": report.damageTakenFromRoboballmini,
            "DTF_NULLIFIER": report.damageTakenFromNullifier,
            "DTF_PARENT": report.damageTakenFromParent,
            "DTF_MINIMUSHROOM": report.damageTakenFromMinimushroom,
            "DTF_POD": report.damageTakenFromPod,
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
            "DTF_BROTHER": report.damageTakenFromBrother,
            "DTF_VERMIN": report.damageTakenFromVermin,
            "DTF_FLYINGVERMIN": report.damageTakenFromFlyingvermin,
            "DTF_CLAYGRENADIER": report.damageTakenFromClaygrenadier,
            "DTF_GUP": report.damageTakenFromGup,
            "DTF_GEEP": report.damageTakenFromGeep,
            "DTF_GIP": report.damageTakenFromGip,
            "DTF_SULFURPOD": report.damageTakenFromSulfurpod,
            "DTF_ACIDLARVA": report.damageTakenFromAcidlarva,
            "DTF_MINORCONSTRUCT": report.damageTakenFromMinorconstruct,
            "DTF_MEGACONSTRUCT": report.damageTakenFromMegaconstruct,
            "DTF_VOIDMEGACRAB": report.damageTakenFromVoidmegacrab,
            "DTF_VOIDRAIDCRAB": report.damageTakenFromVoidraidcrab,
            "DTF_VOIDBARNACLE": report.damageTakenFromVoidbarnacle,
            "DTF_VOIDJAILER": report.damageTakenFromVoidjailer,
            "DTF_ASSASSIN2": report.damageTakenFromAssassin2,
            "DTF_VOIDINFESTOR": report.damageTakenFromVoidinfestor
        }
    )
    
    cur.execute(
        '''
        INSERT INTO Kill_Stats
        VALUES (:Run_ID, :Total_Minion_Kills, :Total_Kills, :Total_Elite_Kills, :Total_Teleporter_Boss_Kills, :KA_BEETLE, :KA_BEETLEGUARD, :KA_BISON, :KA_GOLEM, :KA_WISP, :KA_GREATERWISP, :KA_LEMURIAN, :KA_LEMURIANBRUISER, :KA_IMP, :KA_JELLYFISH, :KA_CLAY, :KA_HERMIT_CRAB, :KA_BELL, :KA_CLAYBRUISER, :KA_VULTURE, :KA_ROBOBALLMINI, :KA_NULLIFIER, :KA_PARENT, :KA_MINIMUSHROOM, :KA_POD, :KA_LUNARWISP, :KA_LUNARGOLEM, :KA_LUNAREXPLODER, :KA_BEETLEQUEEN, :KA_CLAYBOSS, :KA_TITAN, :KA_TITANGOLD, :KA_VAGRANT, :KA_MAGMAWORM, :KA_ELECTRICWORM, :KA_IMPBOSS, :KA_GRAVEKEEPER, :KA_ROBOBALLBOSS, :KA_SUPERROBOBALLBOSS, :KA_SCAV, :KA_SCAVLUNAR1, :KA_SCAVLUNAR2, :KA_SCAVLUNAR3, :KA_SCAVLUNAR4, :KA_GRANDPARENT, :KA_ARTIFACTSHELL, :KA_BROTHER, :KA_VERMIN, :KA_FLYINGVERMIN, :KA_CLAYGRENADIER, :KA_GUP, :KA_GEEP, :KA_GIP, :KA_SULFURPOD, :KA_ACIDLARVA, :KA_MINORCONSTRUCT, :KA_MEGACONSTRUCT, :KA_VOIDMEGACRAB, :KA_VOIDRAIDCRAB, :KA_VOIDBARNACLE, :KA_VOIDJAILER, :KA_ASSASSIN2, :KA_VOIDINFESTOR, :KAE_BEETLE, :KAE_BEETLEGUARD, :KAE_BISON, :KAE_GOLEM, :KAE_WISP, :KAE_GREATERWISP, :KAE_LEMURIAN, :KAE_LEMURIANBRUISER, :KAE_IMP, :KAE_JELLYFISH, :KAE_CLAY, :KAE_HERMIT_CRAB, :KAE_BELL, :KAE_CLAYBRUISER, :KAE_VULTURE, :KAE_ROBOBALLMINI, :KAE_NULLIFIER, :KAE_PARENT, :KAE_MINIMUSHROOM, :KAE_POD, :KAE_LUNARWISP, :KAE_LUNARGOLEM, :KAE_LUNAREXPLODER, :KAE_BEETLEQUEEN, :KAE_CLAYBOSS, :KAE_TITAN, :KAE_TITANGOLD, :KAE_VAGRANT, :KAE_MAGMAWORM, :KAE_ELECTRICWORM, :KAE_IMPBOSS, :KAE_GRAVEKEEPER, :KAE_ROBOBALLBOSS, :KAE_SUPERROBOBALLBOSS, :KAE_SCAV, :KAE_SCAVLUNAR1, :KAE_SCAVLUNAR2, :KAE_SCAVLUNAR3, :KAE_SCAVLUNAR4, :KAE_GRANDPARENT, :KAE_ARTIFACTSHELL, :KAE_BROTHER, :KAE_VERMIN, :KAE_FLYINGVERMIN, :KAE_CLAYGRENADIER, :KAE_GUP, :KAE_GEEP, :KAE_GIP, :KAE_SULFURPOD, :KAE_ACIDLARVA, :KAE_MINORCONSTRUCT)
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
            "KA_CLAY": report.killsAgainstClay,
            "KA_HERMIT_CRAB": report.killsAgainstHermit_Crab,
            "KA_BELL": report.killsAgainstBell,
            "KA_CLAYBRUISER": report.killsAgainstClaybruiser,
            "KA_VULTURE": report.killsAgainstVulture,
            "KA_ROBOBALLMINI": report.killsAgainstRoboballmini,
            "KA_NULLIFIER": report.killsAgainstNullifier,
            "KA_PARENT": report.killsAgainstParent,
            "KA_MINIMUSHROOM": report.killsAgainstMinimushroom,
            "KA_POD": report.killsAgainstPod,
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
            "KA_VERMIN": report.killsAgainstVermin,
            "KA_FLYINGVERMIN": report.killsAgainstFlyingvermin,
            "KA_CLAYGRENADIER": report.killsAgainstClaygrenadier,
            "KA_GUP": report.killsAgainstGup,
            "KA_GEEP": report.killsAgainstGeep,
            "KA_GIP": report.killsAgainstGip,
            "KA_SULFURPOD": report.killsAgainstSulfurpod,
            "KA_ACIDLARVA": report.killsAgainstAcidlarva,
            "KA_MINORCONSTRUCT": report.killsAgainstMinorconstruct,
            "KA_MEGACONSTRUCT": report.killsAgainstMegaconstruct,
            "KA_VOIDMEGACRAB": report.killsAgainstVoidmegacrab,
            "KA_VOIDRAIDCRAB": report.killsAgainstVoidraidcrab,
            "KA_VOIDBARNACLE": report.killsAgainstVoidbarnacle,
            "KA_VOIDJAILER": report.killsAgainstVoidjailer,
            "KA_ASSASSIN2": report.killsAgainstAssassin2,
            "KA_VOIDINFESTOR": report.killsAgainstVoidinfestor,
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
            "KAE_CLAY": report.killsAgainstEliteClay,
            "KAE_HERMIT_CRAB": report.killsAgainstEliteHermit_Crab,
            "KAE_BELL": report.killsAgainstEliteBell,
            "KAE_CLAYBRUISER": report.killsAgainstEliteClaybruiser,
            "KAE_VULTURE": report.killsAgainstEliteVulture,
            "KAE_ROBOBALLMINI": report.killsAgainstEliteRoboballmini,
            "KAE_NULLIFIER": report.killsAgainstEliteNullifier,
            "KAE_PARENT": report.killsAgainstEliteParent,
            "KAE_MINIMUSHROOM": report.killsAgainstEliteMinimushroom,
            "KAE_POD": report.killsAgainstElitePod,
            "KAE_LUNARWISP": report.killsAgainstEliteLunarwisp,
            "KAE_LUNARGOLEM": report.killsAgainstEliteLunargolem,
            "KAE_LUNAREXPLODER": report.killsAgainstEliteLunarexploder,
            "KAE_BEETLEQUEEN": report.killsAgainstEliteBeetlequeen,
            "KAE_CLAYBOSS": report.killsAgainstEliteClayboss,
            "KAE_TITAN": report.killsAgainstEliteTitan,
            "KAE_TITANGOLD": report.killsAgainstEliteTitangold,
            "KAE_VAGRANT": report.killsAgainstEliteVagrant,
            "KAE_MAGMAWORM": report.killsAgainstEliteMagmaworm,
            "KAE_ELECTRICWORM": report.killsAgainstEliteElectricworm,
            "KAE_IMPBOSS": report.killsAgainstEliteImpboss,
            "KAE_GRAVEKEEPER": report.killsAgainstEliteGravekeeper,
            "KAE_ROBOBALLBOSS": report.killsAgainstEliteRoboballboss,
            "KAE_SUPERROBOBALLBOSS": report.killsAgainstEliteSuperroboballboss,
            "KAE_SCAV": report.killsAgainstEliteScav,
            "KAE_SCAVLUNAR1": report.killsAgainstEliteScavlunar1,
            "KAE_SCAVLUNAR2": report.killsAgainstEliteScavlunar2,
            "KAE_SCAVLUNAR3": report.killsAgainstEliteScavlunar3,
            "KAE_SCAVLUNAR4": report.killsAgainstEliteScavlunar4,
            "KAE_GRANDPARENT": report.killsAgainstEliteGrandparent,
            "KAE_ARTIFACTSHELL": report.killsAgainstEliteArtifactshell,
            "KAE_BROTHER": report.killsAgainstEliteBrother,
            "KAE_VERMIN": report.killsAgainstEliteVermin,
            "KAE_FLYINGVERMIN": report.killsAgainstEliteFlyingvermin,
            "KAE_CLAYGRENADIER": report.killsAgainstEliteClaygrenadier,
            "KAE_GUP": report.killsAgainstEliteGup,
            "KAE_GEEP": report.killsAgainstEliteGeep,
            "KAE_GIP": report.killsAgainstEliteGip,
            "KAE_SULFURPOD": report.killsAgainstEliteSulfurpod,
            "KAE_ACIDLARVA": report.killsAgainstEliteAcidlarva,
            "KAE_MINORCONSTRUCT": report.killsAgainstEliteMinorconstruct
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
        VALUES (:Run_ID, :Total_Items_Collected, :Highest_Items_Collected, :TC_ARMORPLATE, :TC_ATTACKSPEEDANDMOVESPEED, :TC_BARRIERONKILL, :TC_BEAR, :TC_BLEEDONHIT, :TC_BOSSDAMAGEBONUS, :TC_CRITGLASSES, :TC_CROWBAR, :TC_FIREWORK, :TC_FLATHEALTH, :TC_FRAGILEDAMAGEBONUS, :TC_GOLDONHURT, :TC_HEALWHILESAFE, :TC_HEALINGPOTION, :TC_HOOF, :TC_IGNITEONKILL, :TC_MEDKIT, :TC_MUSHROOM, :TC_NEARBYDAMAGEBONUS, :TC_OUTOFCOMBATARMOR, :TC_PERSONALSHIELD, :TC_SCRAPWHITE, :TC_SECONDARYSKILLMAGAZINE, :TC_SPRINTBONUS, :TC_STICKYBOMB, :TC_STUNCHANCEONHIT, :TC_SYRINGE, :TC_TOOTH, :TC_TREASURECACHE, :TC_WARDONLEVEL, :TC_ATTACKSPEEDONCRIT, :TC_BANDOLIER, :TC_BONUSGOLDPACKONKILL, :TC_CHAINLIGHTNING, :TC_DEATHMARK, :TC_ENERGIZEDONEQUIPMENTUSE, :TC_EQUIPMENTMAGAZINE, :TC_EXECUTELOWHEALTHELITE, :TC_EXPLODEONDEATH, :TC_FEATHER, :TC_FIRERING, :TC_FREECHEST, :TC_HEALONCRIT, :TC_ICERING, :TC_INFUSION, :TC_JUMPBOOST, :TC_MISSILE, :TC_MOVESPEEDONKILL, :TC_PHASING, :TC_PRIMARYSKILLSHURIKEN, :TC_REGENERATINGSCRAP, :TC_SCRAPGREEN, :TC_SEED, :TC_SLOWONHIT, :TC_SPRINTARMOR, :TC_SPRINTOUTOFCOMBAT, :TC_SQUID, :TC_STRENGTHENBURN, :TC_TPHEALINGNOVA, :TC_THORNS, :TC_WARCRYONMULTIKILL, :TC_ALIENHEAD, :TC_ARMORREDUCTIONONHIT, :TC_BARRIERONOVERHEAL, :TC_BEHEMOTH, :TC_BOUNCENEARBY, :TC_CAPTAINDEFENSEMATRIX, :TC_CLOVER, :TC_CRITDAMAGE, :TC_DAGGER, :TC_DRONEWEAPONS, :TC_EXTRALIFE, :TC_FALLBOOTS, :TC_GHOSTONKILL, :TC_HEADHUNTER, :TC_ICICLE, :TC_IMMUNETODEBUFF, :TC_INCREASEHEALING, :TC_KILLELITEFRENZY, :TC_LASERTURBINE, :TC_MOREMISSILE, :TC_NOVAONHEAL, :TC_PERMANENTDEBUFFONHIT, :TC_PLANT, :TC_RANDOMEQUIPMENTTRIGGER, :TC_SCRAPRED, :TC_SHOCKNEARBY, :TC_TALISMAN, :TC_UTILITYSKILLMAGAZINE, :TC_AUTOCASTEQUIPMENT, :TC_FOCUSCONVERGENCE, :TC_GOLDONHIT, :TC_HALFATTACKSPEEDHALFCOOLDOWNS, :TC_HALFSPEEDDOUBLEHEALTH, :TC_LUNARBADLUCK, :TC_LUNARDAGGER, :TC_LUNARPRIMARYREPLACEMENT, :TC_LUNARSECONDARYREPLACEMENT, :TC_LUNARSPECIALREPLACEMENT, :TC_LUNARSUN, :TC_LUNARTRINKET, :TC_LUNARUTILITYREPLACEMENT, :TC_MONSTERSONSHRINEUSE, :TC_RANDOMDAMAGEZONE, :TC_RANDOMLYLUNAR, :TC_REPEATHEAL, :TC_SHIELDONLY, :TC_ARTIFACTKEY, :TC_BEETLEGLAND, :TC_BLEEDONHITANDEXPLODE, :TC_FIREBALLSONHIT, :TC_KNURL, :TC_LIGHTNINGSTRIKEONHIT, :TC_MINORCONSTRUCTONKILL, :TC_NOVAONLOWHEALTH, :TC_PARENTEGG, :TC_PEARL, :TC_ROBOBALLBUDDY, :TC_SCRAPYELLOW, :TC_SHINYPEARL, :TC_SIPHONONLOWHEALTH, :TC_SPRINTWISP, :TC_TITANGOLDDURINGTP, :TC_BEARVOID, :TC_BLEEDONHITVOID, :TC_CRITGLASSESVOID, :TC_MUSHROOMVOID, :TC_TREASURECACHEVOID, :TC_CHAINLIGHTNINGVOID, :TC_ELEMENTALRINGVOID, :TC_EQUIPMENTMAGAZINEVOID, :TC_EXPLODEONDEATHVOID, :TC_MISSILEVOID, :TC_SLOWONHITVOID, :TC_CLOVERVOID, :TC_EXTRALIFEVOID, :TC_VOIDMEGACRABITEM, :HC_ARMORPLATE, :HC_ATTACKSPEEDANDMOVESPEED, :HC_BARRIERONKILL, :HC_BEAR, :HC_BLEEDONHIT, :HC_BOSSDAMAGEBONUS, :HC_CRITGLASSES, :HC_CROWBAR, :HC_FIREWORK, :HC_FLATHEALTH, :HC_FRAGILEDAMAGEBONUS, :HC_GOLDONHURT, :HC_HEALWHILESAFE, :HC_HEALINGPOTION, :HC_HOOF, :HC_IGNITEONKILL, :HC_MEDKIT, :HC_MUSHROOM, :HC_NEARBYDAMAGEBONUS, :HC_OUTOFCOMBATARMOR, :HC_PERSONALSHIELD, :HC_SCRAPWHITE, :HC_SECONDARYSKILLMAGAZINE, :HC_SPRINTBONUS, :HC_STICKYBOMB, :HC_STUNCHANCEONHIT, :HC_SYRINGE, :HC_TOOTH, :HC_TREASURECACHE, :HC_WARDONLEVEL, :HC_ATTACKSPEEDONCRIT, :HC_BANDOLIER, :HC_BONUSGOLDPACKONKILL, :HC_CHAINLIGHTNING, :HC_DEATHMARK, :HC_ENERGIZEDONEQUIPMENTUSE, :HC_EQUIPMENTMAGAZINE, :HC_EXECUTELOWHEALTHELITE, :HC_EXPLODEONDEATH, :HC_FEATHER, :HC_FIRERING, :HC_FREECHEST, :HC_HEALONCRIT, :HC_ICERING, :HC_INFUSION, :HC_JUMPBOOST, :HC_MISSILE, :HC_MOVESPEEDONKILL, :HC_PHASING, :HC_PRIMARYSKILLSHURIKEN, :HC_REGENERATINGSCRAP, :HC_SCRAPGREEN, :HC_SEED, :HC_SLOWONHIT, :HC_SPRINTARMOR, :HC_SPRINTOUTOFCOMBAT, :HC_SQUID, :HC_STRENGTHENBURN, :HC_TPHEALINGNOVA, :HC_THORNS, :HC_WARCRYONMULTIKILL, :HC_ALIENHEAD, :HC_ARMORREDUCTIONONHIT, :HC_BARRIERONOVERHEAL, :HC_BEHEMOTH, :HC_BOUNCENEARBY, :HC_CAPTAINDEFENSEMATRIX, :HC_CLOVER, :HC_CRITDAMAGE, :HC_DAGGER, :HC_DRONEWEAPONS, :HC_EXTRALIFE, :HC_FALLBOOTS, :HC_GHOSTONKILL, :HC_HEADHUNTER, :HC_ICICLE, :HC_IMMUNETODEBUFF, :HC_INCREASEHEALING, :HC_KILLELITEFRENZY, :HC_LASERTURBINE, :HC_MOREMISSILE, :HC_NOVAONHEAL, :HC_PERMANENTDEBUFFONHIT, :HC_PLANT, :HC_RANDOMEQUIPMENTTRIGGER, :HC_SCRAPRED, :HC_SHOCKNEARBY, :HC_TALISMAN, :HC_UTILITYSKILLMAGAZINE, :HC_AUTOCASTEQUIPMENT, :HC_FOCUSCONVERGENCE, :HC_GOLDONHIT, :HC_HALFATTACKSPEEDHALFCOOLDOWNS, :HC_HALFSPEEDDOUBLEHEALTH, :HC_LUNARBADLUCK, :HC_LUNARDAGGER, :HC_LUNARPRIMARYREPLACEMENT, :HC_LUNARSECONDARYREPLACEMENT, :HC_LUNARSPECIALREPLACEMENT, :HC_LUNARSUN, :HC_LUNARTRINKET, :HC_LUNARUTILITYREPLACEMENT, :HC_MONSTERSONSHRINEUSE, :HC_RANDOMDAMAGEZONE, :HC_RANDOMLYLUNAR, :HC_REPEATHEAL, :HC_SHIELDONLY, :HC_ARTIFACTKEY, :HC_BEETLEGLAND, :HC_BLEEDONHITANDEXPLODE, :HC_FIREBALLSONHIT, :HC_KNURL, :HC_LIGHTNINGSTRIKEONHIT, :HC_MINORCONSTRUCTONKILL, :HC_NOVAONLOWHEALTH, :HC_PARENTEGG, :HC_PEARL, :HC_ROBOBALLBUDDY, :HC_SCRAPYELLOW, :HC_SHINYPEARL, :HC_SIPHONONLOWHEALTH, :HC_SPRINTWISP, :HC_TITANGOLDDURINGTP, :HC_BEARVOID, :HC_BLEEDONHITVOID, :HC_CRITGLASSESVOID, :HC_MUSHROOMVOID, :HC_TREASURECACHEVOID, :HC_CHAINLIGHTNINGVOID, :HC_ELEMENTALRINGVOID, :HC_EQUIPMENTMAGAZINEVOID, :HC_EXPLODEONDEATHVOID, :HC_MISSILEVOID, :HC_SLOWONHITVOID, :HC_CLOVERVOID, :HC_EXTRALIFEVOID, :HC_VOIDMEGACRABITEM)
        ''',
        {
            "Run_ID": report.run_id,
            "Total_Items_Collected": report.totalItemsCollected,
            "Highest_Items_Collected": report.highestItemsCollected,
            "TC_ARMORPLATE": report.totalCollectedArmorplate,
            "TC_ATTACKSPEEDANDMOVESPEED": report.totalCollectedAttackspeedandmovespeed,
            "TC_BARRIERONKILL": report.totalCollectedBarrieronkill,
            "TC_BEAR": report.totalCollectedBear,
            "TC_BLEEDONHIT": report.totalCollectedBleedonhit,
            "TC_BOSSDAMAGEBONUS": report.totalCollectedBossdamagebonus,
            "TC_CRITGLASSES": report.totalCollectedCritglasses,
            "TC_CROWBAR": report.totalCollectedCrowbar,
            "TC_FIREWORK": report.totalCollectedFirework,
            "TC_FLATHEALTH": report.totalCollectedFlathealth,
            "TC_FRAGILEDAMAGEBONUS": report.totalCollectedFragiledamagebonus,
            "TC_GOLDONHURT": report.totalCollectedGoldonhurt,
            "TC_HEALWHILESAFE": report.totalCollectedHealwhilesafe,
            "TC_HEALINGPOTION": report.totalCollectedHealingpotion,
            "TC_HOOF": report.totalCollectedHoof,
            "TC_IGNITEONKILL": report.totalCollectedIgniteonkill,
            "TC_MEDKIT": report.totalCollectedMedkit,
            "TC_MUSHROOM": report.totalCollectedMushroom,
            "TC_NEARBYDAMAGEBONUS": report.totalCollectedNearbydamagebonus,
            "TC_OUTOFCOMBATARMOR": report.totalCollectedOutofcombatarmor,
            "TC_PERSONALSHIELD": report.totalCollectedPersonalshield,
            "TC_SCRAPWHITE": report.totalCollectedScrapwhite,
            "TC_SECONDARYSKILLMAGAZINE": report.totalCollectedSecondaryskillmagazine,
            "TC_SPRINTBONUS": report.totalCollectedSprintbonus,
            "TC_STICKYBOMB": report.totalCollectedStickybomb,
            "TC_STUNCHANCEONHIT": report.totalCollectedStunchanceonhit,
            "TC_SYRINGE": report.totalCollectedSyringe,
            "TC_TOOTH": report.totalCollectedTooth,
            "TC_TREASURECACHE": report.totalCollectedTreasurecache,
            "TC_WARDONLEVEL": report.totalCollectedWardonlevel,
            "TC_ATTACKSPEEDONCRIT": report.totalCollectedAttackspeedoncrit,
            "TC_BANDOLIER": report.totalCollectedBandolier,
            "TC_BONUSGOLDPACKONKILL": report.totalCollectedBonusgoldpackonkill,
            "TC_CHAINLIGHTNING": report.totalCollectedChainlightning,
            "TC_DEATHMARK": report.totalCollectedDeathmark,
            "TC_ENERGIZEDONEQUIPMENTUSE": report.totalCollectedEnergizedonequipmentuse,
            "TC_EQUIPMENTMAGAZINE": report.totalCollectedEquipmentmagazine,
            "TC_EXECUTELOWHEALTHELITE": report.totalCollectedExecutelowhealthelite,
            "TC_EXPLODEONDEATH": report.totalCollectedExplodeondeath,
            "TC_FEATHER": report.totalCollectedFeather,
            "TC_FIRERING": report.totalCollectedFirering,
            "TC_FREECHEST": report.totalCollectedFreechest,
            "TC_HEALONCRIT": report.totalCollectedHealoncrit,
            "TC_ICERING": report.totalCollectedIcering,
            "TC_INFUSION": report.totalCollectedInfusion,
            "TC_JUMPBOOST": report.totalCollectedJumpboost,
            "TC_MISSILE": report.totalCollectedMissile,
            "TC_MOVESPEEDONKILL": report.totalCollectedMovespeedonkill,
            "TC_PHASING": report.totalCollectedPhasing,
            "TC_PRIMARYSKILLSHURIKEN": report.totalCollectedPrimaryskillshuriken,
            "TC_REGENERATINGSCRAP": report.totalCollectedRegeneratingscrap,
            "TC_SCRAPGREEN": report.totalCollectedScrapgreen,
            "TC_SEED": report.totalCollectedSeed,
            "TC_SLOWONHIT": report.totalCollectedSlowonhit,
            "TC_SPRINTARMOR": report.totalCollectedSprintarmor,
            "TC_SPRINTOUTOFCOMBAT": report.totalCollectedSprintoutofcombat,
            "TC_SQUID": report.totalCollectedSquid,
            "TC_STRENGTHENBURN": report.totalCollectedStrengthenburn,
            "TC_TPHEALINGNOVA": report.totalCollectedTphealingnova,
            "TC_THORNS": report.totalCollectedThorns,
            "TC_WARCRYONMULTIKILL": report.totalCollectedWarcryonmultikill,
            "TC_ALIENHEAD": report.totalCollectedAlienhead,
            "TC_ARMORREDUCTIONONHIT": report.totalCollectedArmorreductiononhit,
            "TC_BARRIERONOVERHEAL": report.totalCollectedBarrieronoverheal,
            "TC_BEHEMOTH": report.totalCollectedBehemoth,
            "TC_BOUNCENEARBY": report.totalCollectedBouncenearby,
            "TC_CAPTAINDEFENSEMATRIX": report.totalCollectedCaptaindefensematrix,
            "TC_CLOVER": report.totalCollectedClover,
            "TC_CRITDAMAGE": report.totalCollectedCritdamage,
            "TC_DAGGER": report.totalCollectedDagger,
            "TC_DRONEWEAPONS": report.totalCollectedDroneweapons,
            "TC_EXTRALIFE": report.totalCollectedExtralife,
            "TC_FALLBOOTS": report.totalCollectedFallboots,
            "TC_GHOSTONKILL": report.totalCollectedGhostonkill,
            "TC_HEADHUNTER": report.totalCollectedHeadhunter,
            "TC_ICICLE": report.totalCollectedIcicle,
            "TC_IMMUNETODEBUFF": report.totalCollectedImmunetodebuff,
            "TC_INCREASEHEALING": report.totalCollectedIncreasehealing,
            "TC_KILLELITEFRENZY": report.totalCollectedKillelitefrenzy,
            "TC_LASERTURBINE": report.totalCollectedLaserturbine,
            "TC_MOREMISSILE": report.totalCollectedMoremissile,
            "TC_NOVAONHEAL": report.totalCollectedNovaonheal,
            "TC_PERMANENTDEBUFFONHIT": report.totalCollectedPermanentdebuffonhit,
            "TC_PLANT": report.totalCollectedPlant,
            "TC_RANDOMEQUIPMENTTRIGGER": report.totalCollectedRandomequipmenttrigger,
            "TC_SCRAPRED": report.totalCollectedScrapred,
            "TC_SHOCKNEARBY": report.totalCollectedShocknearby,
            "TC_TALISMAN": report.totalCollectedTalisman,
            "TC_UTILITYSKILLMAGAZINE": report.totalCollectedUtilityskillmagazine,
            "TC_AUTOCASTEQUIPMENT": report.totalCollectedAutocastequipment,
            "TC_FOCUSCONVERGENCE": report.totalCollectedFocusconvergence,
            "TC_GOLDONHIT": report.totalCollectedGoldonhit,
            "TC_HALFATTACKSPEEDHALFCOOLDOWNS": report.totalCollectedHalfattackspeedhalfcooldowns,
            "TC_HALFSPEEDDOUBLEHEALTH": report.totalCollectedHalfspeeddoublehealth,
            "TC_LUNARBADLUCK": report.totalCollectedLunarbadluck,
            "TC_LUNARDAGGER": report.totalCollectedLunardagger,
            "TC_LUNARPRIMARYREPLACEMENT": report.totalCollectedLunarprimaryreplacement,
            "TC_LUNARSECONDARYREPLACEMENT": report.totalCollectedLunarsecondaryreplacement,
            "TC_LUNARSPECIALREPLACEMENT": report.totalCollectedLunarspecialreplacement,
            "TC_LUNARSUN": report.totalCollectedLunarsun,
            "TC_LUNARTRINKET": report.totalCollectedLunartrinket,
            "TC_LUNARUTILITYREPLACEMENT": report.totalCollectedLunarutilityreplacement,
            "TC_MONSTERSONSHRINEUSE": report.totalCollectedMonstersonshrineuse,
            "TC_RANDOMDAMAGEZONE": report.totalCollectedRandomdamagezone,
            "TC_RANDOMLYLUNAR": report.totalCollectedRandomlylunar,
            "TC_REPEATHEAL": report.totalCollectedRepeatheal,
            "TC_SHIELDONLY": report.totalCollectedShieldonly,
            "TC_ARTIFACTKEY": report.totalCollectedArtifactkey,
            "TC_BEETLEGLAND": report.totalCollectedBeetlegland,
            "TC_BLEEDONHITANDEXPLODE": report.totalCollectedBleedonhitandexplode,
            "TC_FIREBALLSONHIT": report.totalCollectedFireballsonhit,
            "TC_KNURL": report.totalCollectedKnurl,
            "TC_LIGHTNINGSTRIKEONHIT": report.totalCollectedLightningstrikeonhit,
            "TC_MINORCONSTRUCTONKILL": report.totalCollectedMinorconstructonkill,
            "TC_NOVAONLOWHEALTH": report.totalCollectedNovaonlowhealth,
            "TC_PARENTEGG": report.totalCollectedParentegg,
            "TC_PEARL": report.totalCollectedPearl,
            "TC_ROBOBALLBUDDY": report.totalCollectedRoboballbuddy,
            "TC_SCRAPYELLOW": report.totalCollectedScrapyellow,
            "TC_SHINYPEARL": report.totalCollectedShinypearl,
            "TC_SIPHONONLOWHEALTH": report.totalCollectedSiphononlowhealth,
            "TC_SPRINTWISP": report.totalCollectedSprintwisp,
            "TC_TITANGOLDDURINGTP": report.totalCollectedTitangoldduringtp,
            "TC_BEARVOID": report.totalCollectedBearvoid,
            "TC_BLEEDONHITVOID": report.totalCollectedBleedonhitvoid,
            "TC_CRITGLASSESVOID": report.totalCollectedCritglassesvoid,
            "TC_MUSHROOMVOID": report.totalCollectedMushroomvoid,
            "TC_TREASURECACHEVOID": report.totalCollectedTreasurecachevoid,
            "TC_CHAINLIGHTNINGVOID": report.totalCollectedChainlightningvoid,
            "TC_ELEMENTALRINGVOID": report.totalCollectedElementalringvoid,
            "TC_EQUIPMENTMAGAZINEVOID": report.totalCollectedEquipmentmagazinevoid,
            "TC_EXPLODEONDEATHVOID": report.totalCollectedExplodeondeathvoid,
            "TC_MISSILEVOID": report.totalCollectedMissilevoid,
            "TC_SLOWONHITVOID": report.totalCollectedSlowonhitvoid,
            "TC_CLOVERVOID": report.totalCollectedClovervoid,
            "TC_EXTRALIFEVOID": report.totalCollectedExtralifevoid,
            "TC_VOIDMEGACRABITEM": report.totalCollectedVoidmegacrabitem,
            "HC_ARMORPLATE": report.highestCollectedArmorplate,
            "HC_ATTACKSPEEDANDMOVESPEED": report.highestCollectedAttackspeedandmovespeed,
            "HC_BARRIERONKILL": report.highestCollectedBarrieronkill,
            "HC_BEAR": report.highestCollectedBear,
            "HC_BLEEDONHIT": report.highestCollectedBleedonhit,
            "HC_BOSSDAMAGEBONUS": report.highestCollectedBossdamagebonus,
            "HC_CRITGLASSES": report.highestCollectedCritglasses,
            "HC_CROWBAR": report.highestCollectedCrowbar,
            "HC_FIREWORK": report.highestCollectedFirework,
            "HC_FLATHEALTH": report.highestCollectedFlathealth,
            "HC_FRAGILEDAMAGEBONUS": report.highestCollectedFragiledamagebonus,
            "HC_GOLDONHURT": report.highestCollectedGoldonhurt,
            "HC_HEALWHILESAFE": report.highestCollectedHealwhilesafe,
            "HC_HEALINGPOTION": report.highestCollectedHealingpotion,
            "HC_HOOF": report.highestCollectedHoof,
            "HC_IGNITEONKILL": report.highestCollectedIgniteonkill,
            "HC_MEDKIT": report.highestCollectedMedkit,
            "HC_MUSHROOM": report.highestCollectedMushroom,
            "HC_NEARBYDAMAGEBONUS": report.highestCollectedNearbydamagebonus,
            "HC_OUTOFCOMBATARMOR": report.highestCollectedOutofcombatarmor,
            "HC_PERSONALSHIELD": report.highestCollectedPersonalshield,
            "HC_SCRAPWHITE": report.highestCollectedScrapwhite,
            "HC_SECONDARYSKILLMAGAZINE": report.highestCollectedSecondaryskillmagazine,
            "HC_SPRINTBONUS": report.highestCollectedSprintbonus,
            "HC_STICKYBOMB": report.highestCollectedStickybomb,
            "HC_STUNCHANCEONHIT": report.highestCollectedStunchanceonhit,
            "HC_SYRINGE": report.highestCollectedSyringe,
            "HC_TOOTH": report.highestCollectedTooth,
            "HC_TREASURECACHE": report.highestCollectedTreasurecache,
            "HC_WARDONLEVEL": report.highestCollectedWardonlevel,
            "HC_ATTACKSPEEDONCRIT": report.highestCollectedAttackspeedoncrit,
            "HC_BANDOLIER": report.highestCollectedBandolier,
            "HC_BONUSGOLDPACKONKILL": report.highestCollectedBonusgoldpackonkill,
            "HC_CHAINLIGHTNING": report.highestCollectedChainlightning,
            "HC_DEATHMARK": report.highestCollectedDeathmark,
            "HC_ENERGIZEDONEQUIPMENTUSE": report.highestCollectedEnergizedonequipmentuse,
            "HC_EQUIPMENTMAGAZINE": report.highestCollectedEquipmentmagazine,
            "HC_EXECUTELOWHEALTHELITE": report.highestCollectedExecutelowhealthelite,
            "HC_EXPLODEONDEATH": report.highestCollectedExplodeondeath,
            "HC_FEATHER": report.highestCollectedFeather,
            "HC_FIRERING": report.highestCollectedFirering,
            "HC_FREECHEST": report.highestCollectedFreechest,
            "HC_HEALONCRIT": report.highestCollectedHealoncrit,
            "HC_ICERING": report.highestCollectedIcering,
            "HC_INFUSION": report.highestCollectedInfusion,
            "HC_JUMPBOOST": report.highestCollectedJumpboost,
            "HC_MISSILE": report.highestCollectedMissile,
            "HC_MOVESPEEDONKILL": report.highestCollectedMovespeedonkill,
            "HC_PHASING": report.highestCollectedPhasing,
            "HC_PRIMARYSKILLSHURIKEN": report.highestCollectedPrimaryskillshuriken,
            "HC_REGENERATINGSCRAP": report.highestCollectedRegeneratingscrap,
            "HC_SCRAPGREEN": report.highestCollectedScrapgreen,
            "HC_SEED": report.highestCollectedSeed,
            "HC_SLOWONHIT": report.highestCollectedSlowonhit,
            "HC_SPRINTARMOR": report.highestCollectedSprintarmor,
            "HC_SPRINTOUTOFCOMBAT": report.highestCollectedSprintoutofcombat,
            "HC_SQUID": report.highestCollectedSquid,
            "HC_STRENGTHENBURN": report.highestCollectedStrengthenburn,
            "HC_TPHEALINGNOVA": report.highestCollectedTphealingnova,
            "HC_THORNS": report.highestCollectedThorns,
            "HC_WARCRYONMULTIKILL": report.highestCollectedWarcryonmultikill,
            "HC_ALIENHEAD": report.highestCollectedAlienhead,
            "HC_ARMORREDUCTIONONHIT": report.highestCollectedArmorreductiononhit,
            "HC_BARRIERONOVERHEAL": report.highestCollectedBarrieronoverheal,
            "HC_BEHEMOTH": report.highestCollectedBehemoth,
            "HC_BOUNCENEARBY": report.highestCollectedBouncenearby,
            "HC_CAPTAINDEFENSEMATRIX": report.highestCollectedCaptaindefensematrix,
            "HC_CLOVER": report.highestCollectedClover,
            "HC_CRITDAMAGE": report.highestCollectedCritdamage,
            "HC_DAGGER": report.highestCollectedDagger,
            "HC_DRONEWEAPONS": report.highestCollectedDroneweapons,
            "HC_EXTRALIFE": report.highestCollectedExtralife,
            "HC_FALLBOOTS": report.highestCollectedFallboots,
            "HC_GHOSTONKILL": report.highestCollectedGhostonkill,
            "HC_HEADHUNTER": report.highestCollectedHeadhunter,
            "HC_ICICLE": report.highestCollectedIcicle,
            "HC_IMMUNETODEBUFF": report.highestCollectedImmunetodebuff,
            "HC_INCREASEHEALING": report.highestCollectedIncreasehealing,
            "HC_KILLELITEFRENZY": report.highestCollectedKillelitefrenzy,
            "HC_LASERTURBINE": report.highestCollectedLaserturbine,
            "HC_MOREMISSILE": report.highestCollectedMoremissile,
            "HC_NOVAONHEAL": report.highestCollectedNovaonheal,
            "HC_PERMANENTDEBUFFONHIT": report.highestCollectedPermanentdebuffonhit,
            "HC_PLANT": report.highestCollectedPlant,
            "HC_RANDOMEQUIPMENTTRIGGER": report.highestCollectedRandomequipmenttrigger,
            "HC_SCRAPRED": report.highestCollectedScrapred,
            "HC_SHOCKNEARBY": report.highestCollectedShocknearby,
            "HC_TALISMAN": report.highestCollectedTalisman,
            "HC_UTILITYSKILLMAGAZINE": report.highestCollectedUtilityskillmagazine,
            "HC_AUTOCASTEQUIPMENT": report.highestCollectedAutocastequipment,
            "HC_FOCUSCONVERGENCE": report.highestCollectedFocusconvergence,
            "HC_GOLDONHIT": report.highestCollectedGoldonhit,
            "HC_HALFATTACKSPEEDHALFCOOLDOWNS": report.highestCollectedHalfattackspeedhalfcooldowns,
            "HC_HALFSPEEDDOUBLEHEALTH": report.highestCollectedHalfspeeddoublehealth,
            "HC_LUNARBADLUCK": report.highestCollectedLunarbadluck,
            "HC_LUNARDAGGER": report.highestCollectedLunardagger,
            "HC_LUNARPRIMARYREPLACEMENT": report.highestCollectedLunarprimaryreplacement,
            "HC_LUNARSECONDARYREPLACEMENT": report.highestCollectedLunarsecondaryreplacement,
            "HC_LUNARSPECIALREPLACEMENT": report.highestCollectedLunarspecialreplacement,
            "HC_LUNARSUN": report.highestCollectedLunarsun,
            "HC_LUNARTRINKET": report.highestCollectedLunartrinket,
            "HC_LUNARUTILITYREPLACEMENT": report.highestCollectedLunarutilityreplacement,
            "HC_MONSTERSONSHRINEUSE": report.highestCollectedMonstersonshrineuse,
            "HC_RANDOMDAMAGEZONE": report.highestCollectedRandomdamagezone,
            "HC_RANDOMLYLUNAR": report.highestCollectedRandomlylunar,
            "HC_REPEATHEAL": report.highestCollectedRepeatheal,
            "HC_SHIELDONLY": report.highestCollectedShieldonly,
            "HC_ARTIFACTKEY": report.highestCollectedArtifactkey,
            "HC_BEETLEGLAND": report.highestCollectedBeetlegland,
            "HC_BLEEDONHITANDEXPLODE": report.highestCollectedBleedonhitandexplode,
            "HC_FIREBALLSONHIT": report.highestCollectedFireballsonhit,
            "HC_KNURL": report.highestCollectedKnurl,
            "HC_LIGHTNINGSTRIKEONHIT": report.highestCollectedLightningstrikeonhit,
            "HC_MINORCONSTRUCTONKILL": report.highestCollectedMinorconstructonkill,
            "HC_NOVAONLOWHEALTH": report.highestCollectedNovaonlowhealth,
            "HC_PARENTEGG": report.highestCollectedParentegg,
            "HC_PEARL": report.highestCollectedPearl,
            "HC_ROBOBALLBUDDY": report.highestCollectedRoboballbuddy,
            "HC_SCRAPYELLOW": report.highestCollectedScrapyellow,
            "HC_SHINYPEARL": report.highestCollectedShinypearl,
            "HC_SIPHONONLOWHEALTH": report.highestCollectedSiphononlowhealth,
            "HC_SPRINTWISP": report.highestCollectedSprintwisp,
            "HC_TITANGOLDDURINGTP": report.highestCollectedTitangoldduringtp,
            "HC_BEARVOID": report.highestCollectedBearvoid,
            "HC_BLEEDONHITVOID": report.highestCollectedBleedonhitvoid,
            "HC_CRITGLASSESVOID": report.highestCollectedCritglassesvoid,
            "HC_MUSHROOMVOID": report.highestCollectedMushroomvoid,
            "HC_TREASURECACHEVOID": report.highestCollectedTreasurecachevoid,
            "HC_CHAINLIGHTNINGVOID": report.highestCollectedChainlightningvoid,
            "HC_ELEMENTALRINGVOID": report.highestCollectedElementalringvoid,
            "HC_EQUIPMENTMAGAZINEVOID": report.highestCollectedEquipmentmagazinevoid,
            "HC_EXPLODEONDEATHVOID": report.highestCollectedExplodeondeathvoid,
            "HC_MISSILEVOID": report.highestCollectedMissilevoid,
            "HC_SLOWONHITVOID": report.highestCollectedSlowonhitvoid,
            "HC_CLOVERVOID": report.highestCollectedClovervoid,
            "HC_EXTRALIFEVOID": report.highestCollectedExtralifevoid,
            "HC_VOIDMEGACRABITEM": report.highestCollectedVoidmegacrabitem
        }
    )
    
    cur.execute(
        '''
        INSERT INTO Equipment_Info
        VALUES (:Run_ID, :TH_BFG, :TH_BLACKHOLE, :TH_BOSSHUNTER, :TH_BURNNEARBY, :TH_CLEANSE, :TH_COMMANDMISSILE, :TH_CRIPPLEWARD, :TH_CRITONUSE, :TH_DEATHPROJECTILE, :TH_DRONEBACKUP, :TH_FIREBALLDASH, :TH_FRUIT, :TH_GAINARMOR, :TH_GATEWAY, :TH_GOLDGAT, :TH_GUMMYCLONE, :TH_JETPACK, :TH_LIFESTEALONHIT, :TH_LIGHTNING, :TH_METEOR, :TH_MOLOTOV, :TH_MULTISHOPCARD, :TH_PASSIVEHEALING, :TH_RECYCLE, :TH_SAW, :TH_SCANNER, :TH_TEAMWARCRY, :TH_TONIC, :TH_VENDINGMACHINE, :TF_BFG, :TF_BLACKHOLE, :TF_BOSSHUNTER, :TF_BURNNEARBY, :TF_CLEANSE, :TF_COMMANDMISSILE, :TF_CRIPPLEWARD, :TF_CRITONUSE, :TF_DEATHPROJECTILE, :TF_DRONEBACKUP, :TF_FIREBALLDASH, :TF_FRUIT, :TF_GAINARMOR, :TF_GATEWAY, :TF_GOLDGAT, :TF_GUMMYCLONE, :TF_JETPACK, :TF_LIFESTEALONHIT, :TF_LIGHTNING, :TF_METEOR, :TF_MOLOTOV, :TF_MULTISHOPCARD, :TF_PASSIVEHEALING, :TF_RECYCLE, :TF_SAW, :TF_SCANNER, :TF_TEAMWARCRY, :TF_TONIC, :TF_VENDINGMACHINE)
        ''',
        {
            "Run_ID": report.run_id,
            "TH_BFG": report.timeHeldBfg,
            "TH_BLACKHOLE": report.timeHeldBlackhole,
            "TH_BOSSHUNTER": report.timeHeldBosshunter,
            "TH_BURNNEARBY": report.timeHeldBurnnearby,
            "TH_CLEANSE": report.timeHeldCleanse,
            "TH_COMMANDMISSILE": report.timeHeldCommandmissile,
            "TH_CRIPPLEWARD": report.timeHeldCrippleward,
            "TH_CRITONUSE": report.timeHeldCritonuse,
            "TH_DEATHPROJECTILE": report.timeHeldDeathprojectile,
            "TH_DRONEBACKUP": report.timeHeldDronebackup,
            "TH_FIREBALLDASH": report.timeHeldFireballdash,
            "TH_FRUIT": report.timeHeldFruit,
            "TH_GAINARMOR": report.timeHeldGainarmor,
            "TH_GATEWAY": report.timeHeldGateway,
            "TH_GOLDGAT": report.timeHeldGoldgat,
            "TH_GUMMYCLONE": report.timeHeldGummyclone,
            "TH_JETPACK": report.timeHeldJetpack,
            "TH_LIFESTEALONHIT": report.timeHeldLifestealonhit,
            "TH_LIGHTNING": report.timeHeldLightning,
            "TH_METEOR": report.timeHeldMeteor,
            "TH_MOLOTOV": report.timeHeldMolotov,
            "TH_MULTISHOPCARD": report.timeHeldMultishopcard,
            "TH_PASSIVEHEALING": report.timeHeldPassivehealing,
            "TH_RECYCLE": report.timeHeldRecycle,
            "TH_SAW": report.timeHeldSaw,
            "TH_SCANNER": report.timeHeldScanner,
            "TH_TEAMWARCRY": report.timeHeldTeamwarcry,
            "TH_TONIC": report.timeHeldTonic,
            "TH_VENDINGMACHINE": report.timeHeldVendingmachine,
            "TF_BFG": report.timesFiredBfg,
            "TF_BLACKHOLE": report.timesFiredBlackhole,
            "TF_BOSSHUNTER": report.timesFiredBosshunter,
            "TF_BURNNEARBY": report.timesFiredBurnnearby,
            "TF_CLEANSE": report.timesFiredCleanse,
            "TF_COMMANDMISSILE": report.timesFiredCommandmissile,
            "TF_CRIPPLEWARD": report.timesFiredCrippleward,
            "TF_CRITONUSE": report.timesFiredCritonuse,
            "TF_DEATHPROJECTILE": report.timesFiredDeathprojectile,
            "TF_DRONEBACKUP": report.timesFiredDronebackup,
            "TF_FIREBALLDASH": report.timesFiredFireballdash,
            "TF_FRUIT": report.timesFiredFruit,
            "TF_GAINARMOR": report.timesFiredGainarmor,
            "TF_GATEWAY": report.timesFiredGateway,
            "TF_GOLDGAT": report.timesFiredGoldgat,
            "TF_GUMMYCLONE": report.timesFiredGummyclone,
            "TF_JETPACK": report.timesFiredJetpack,
            "TF_LIFESTEALONHIT": report.timesFiredLifestealonhit,
            "TF_LIGHTNING": report.timesFiredLightning,
            "TF_METEOR": report.timesFiredMeteor,
            "TF_MOLOTOV": report.timesFiredMolotov,
            "TF_MULTISHOPCARD": report.timesFiredMultishopcard,
            "TF_PASSIVEHEALING": report.timesFiredPassivehealing,
            "TF_RECYCLE": report.timesFiredRecycle,
            "TF_SAW": report.timesFiredSaw,
            "TF_SCANNER": report.timesFiredScanner,
            "TF_TEAMWARCRY": report.timesFiredTeamwarcry,
            "TF_TONIC": report.timesFiredTonic,
            "TF_VENDINGMACHINE": report.timesFiredVendingmachine
        }
    )
    
    cur.execute(
        '''
        INSERT INTO Stage_Info
        VALUES (:Run_ID, :Total_Stages_Completed, :Highest_Stages_Completed, :TV_BLACKBEACH, :TV_GOLEMPLAINS, :TV_GOOLAKE, :TV_BAZAAR, :TV_FROZENWALL, :TV_FOGGYSWAMP, :TV_DAMPCAVE, :TV_WISPGRAVEYARD, :TV_MYSTERYSPACE, :TV_GOLDSHORES, :TV_SHIPGRAVEYARD, :TV_ROOTJUNGLE, :TV_ARENA, :TV_LIMBO, :TV_SKYMEADOW, :TV_ARTIFACTWORLD, :TV_MOON, :TV_ANCIENTLOFT, :TV_SNOWYFOREST, :TV_SULFURPOOLS, :TV_VOIDSTAGE, :TV_VOIDRAID, :TC_BLACKBEACH, :TC_GOLEMPLAINS, :TC_GOOLAKE, :TC_BAZAAR, :TC_FROZENWALL, :TC_FOGGYSWAMP, :TC_DAMPCAVE, :TC_WISPGRAVEYARD, :TC_MYSTERYSPACE, :TC_GOLDSHORES, :TC_SHIPGRAVEYARD, :TC_ROOTJUNGLE, :TC_ARENA, :TC_LIMBO, :TC_SKYMEADOW, :TC_ARTIFACTWORLD, :TC_MOON, :TC_ANCIENTLOFT, :TC_SNOWYFOREST, :TC_SULFURPOOLS, :TC_VOIDSTAGE, :TC_VOIDRAID)
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
            "TV_ANCIENTLOFT": report.timesVisitedAncientloft,
            "TV_SNOWYFOREST": report.timesVisitedSnowyforest,
            "TV_SULFURPOOLS": report.timesVisitedSulfurpools,
            "TV_VOIDSTAGE": report.timesVisitedVoidstage,
            "TV_VOIDRAID": report.timesVisitedVoidraid,
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
            "TC_MOON": report.timesClearedMoon,
            "TC_ANCIENTLOFT": report.timesClearedAncientloft,
            "TC_SNOWYFOREST": report.timesClearedSnowyforest,
            "TC_SULFURPOOLS": report.timesClearedSulfurpools,
            "TC_VOIDSTAGE": report.timesClearedVoidstage,
            "TC_VOIDRAID": report.timesClearedVoidraid
        }
    )
    
    con.commit()


for run in runs:
    data_entry(run)

print(f'Run data for {len(runs)} runs added to database.')

try:
    # Update most recent run date
    most_recent = max([run.date for run in runs])
    update_recent_run_setting(most_recent)
    
    print('Most recent run date updated in settings file.')

    # Export updated data
    tbl_qry = cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tbl_names = tbl_qry.fetchall()
    
    for tbl in tbl_names:
        export_tables(tbl[0])
    
    print('Run data CSVs updated.')

except ValueError:
    print('No new runs!')

con.close()