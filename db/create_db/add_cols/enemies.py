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

def add_kills(enemies, cursor):
    for name in enemies:
        if name[0] not in unused_mobs:
            cursor.execute(
                '''
                ALTER TABLE Kill_Stats
                ADD Kills_Against_{} INTEGER DEFAULT 0
                '''.format(name[0].replace('_',''))
            )

def add_elite_kills(enemies, cursor):
    for name in enemies:
        if name[0] not in unused_mobs and name[0] not in non_elites:
            cursor.execute(
                '''
                ALTER TABLE Kill_Stats
                ADD Kills_Against_Elite_{} INTEGER DEFAULT 0
                '''.format(name[0].replace('_',''))
            )

def add_dmg_dealt(enemies, cursor):
    for name in enemies:
        if name[0] not in unused_mobs:
            cursor.execute(
                '''
                ALTER TABLE Damage_Stats
                ADD Damage_Dealt_To_{} INTEGER DEFAULT 0
                '''.format(name[0].replace('_',''))
            )
    
def add_dmg_taken(enemies, cursor):
    for name in enemies:
        if name[0] not in unused_mobs:
            cursor.execute(
                '''
                ALTER TABLE Damage_Stats
                ADD Damage_Taken_From_{} INTEGER DEFAULT 0
                '''.format(name[0].replace('_',''))
            )

monsters = all_characters.split('//[')[3]
bosses = all_characters.split('//[')[4]

enemy_names = get_body_names(monsters) + get_body_names(bosses)

characters_file.close()
dir_settings.close()