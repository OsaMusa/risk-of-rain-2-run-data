dir_settings = open('../../settings.txt', 'r')
dir_path = dir_settings.readlines()[0].split('= ')[1].strip('\n')
file_path = dir_path + 'Language\en\\'

equip_file = open(file_path+'Equipment.txt')
all_equips = equip_file.readlines()

raw_equip_names = [name.strip('\t\n ,').split(': ') for name in all_equips if '_NAME' in name]
equip_names = [[name[0].strip('\" ')[10:-5],name[1].strip('\"')] for name in raw_equip_names]

unused_equips = ["AFFIXRED", "AFFIXBLUE", "AFFIXGOLD", "AFFIXWHITE",
                 "AFFIXPOISON", "AFFIXHAUNTED", "AFFIXLUNAR", "GHOSTGUN",
                 "QUESTVOLATILEBATTERY", "SOULCORRUPTOR", "SOULJAR"]

def add_time_held(equipment, cursor):
    for equip in equipment:
        if equip[0] not in unused_equips:
            cursor.execute(
                '''
                ALTER TABLE Equipment_Info
                ADD Total_Time_Held_{} INTEGER DEFAULT 0
                '''.format(equip[0])
            )
    
def add_times_fired(equipment, cursor):
    for equip in equipment:
        if equip[0] not in unused_equips:
            cursor.execute(
                '''
                ALTER TABLE Equipment_Info
                ADD Total_Times_Fired_{} INTEGER DEFAULT 0
                '''.format(equip[0])
            )

equip_file.close()
dir_settings.close()