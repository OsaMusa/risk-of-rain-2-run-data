import sqlite3

con = sqlite3.connect('../run_report_db.db')
cur = con.cursor()

dir_settings = open('../../settings.txt', 'r')
dir_path = dir_settings.readlines()[0].split('= ')[1].strip('\n')
file_path = dir_path + 'Language\en\\'

characters_file = open(file_path+'CharacterBodies.txt', 'r')
all_characters = characters_file.read()

unused_mobs = ['CLAY', 'POD']
non_elites = ['BROTHER','SCAVLUNAR1','SCAVLUNAR2','SCAVLUNAR3',
                'SCAVLUNAR4','ARTIFACTSHELL','TITANGOLD',
                'SUPERROBOBALLBOSS','MAGMAWORM','ELECTRICWORM']

def get_body_names(sect):
    sect_lines = [name.strip(',\t').split(': ') for name in sect.splitlines()]
    body_names = [[name[0].strip('\" ')[:-10],name[1].strip('\"')] for name in sect_lines if '_BODY_NAME' in name[0]]
    return body_names

def add_kills(enemy_names):
    for name in enemy_names:
        if name[0] not in unused_mobs:
            cur.execute(
                '''
                ALTER TABLE Kill_Stats
                ADD Kills_Against_{} INTEGER DEFAULT 0
                '''.format(name[0].replace('_',''))
            )

def add_elite_kills(enemy_names):
    for name in enemy_names:
        if name[0] not in unused_mobs and name[0] not in non_elites:
            cur.execute(
                '''
                ALTER TABLE Kill_Stats
                ADD Kills_Against_Elite_{} INTEGER DEFAULT 0
                '''.format(name[0].replace('_',''))
            )

def add_dmg_dealt(enemy_names):
    for name in enemy_names:
        if name[0] not in unused_mobs:
            cur.execute(
                '''
                ALTER TABLE Damage_Stats
                ADD Damage_Dealt_To_{} INTEGER DEFAULT 0
                '''.format(name[0].replace('_',''))
            )
    
def add_dmg_taken(enemy_names):
    for name in enemy_names:
        if name[0] not in unused_mobs:
            cur.execute(
                '''
                ALTER TABLE Damage_Stats
                ADD Damage_Taken_From_{} INTEGER DEFAULT 0
                '''.format(name[0].replace('_',''))
            )

monsters = all_characters.split('//[')[3]
bosses = all_characters.split('//[')[4]

enemies = get_body_names(monsters) + get_body_names(bosses)

add_kills(enemies)
add_elite_kills(enemies)
add_dmg_dealt(enemies)
add_dmg_taken(enemies)

con.commit()

characters_file.close()
dir_settings.close()
con.close()