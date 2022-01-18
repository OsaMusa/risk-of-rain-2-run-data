import sqlite3

con = sqlite3.connect('../run_report_db.db')
cur = con.cursor()

dir_settings = open('../../settings.txt', 'r')
dir_path = dir_settings.readlines()[0].split('= ')[1].strip('\n')
file_path = dir_path + 'Language\en\\'

equip_file = open(file_path+'Equipment.txt')
all_equips = equip_file.readlines()

equip_names = [name.strip('\t\n ,').split(': ') for name in all_equips if '_NAME' in name]
clean_equip_names = [[name[0].strip('\" ')[10:-5],name[1].strip('\"')] for name in equip_names]

unused_equips = ["AFFIXRED", "AFFIXBLUE", "AFFIXGOLD", "AFFIXWHITE", "AFFIXPOISON", "AFFIXHAUNTED", "AFFIXLUNAR", "GHOSTGUN", "QUESTVOLATILEBATTERY", "SOULCORRUPTOR", "SOULJAR"]

def add_time_held(equipment):
    for equip in equipment:
        if equip[0] not in unused_equips:
            cur.execute(
                '''
                ALTER TABLE Equipment_Info
                ADD Total_Time_Held_{} INTEGER DEFAULT 0
                '''.format(equip[0])
            )
    
def add_times_fired(equipment):
    for equip in equipment:
        if equip[0] not in unused_equips:
            cur.execute(
                '''
                ALTER TABLE Equipment_Info
                ADD Total_Times_Fired_{} INTEGER DEFAULT 0
                '''.format(equip[0])
            )

add_time_held(clean_equip_names)
add_times_fired(clean_equip_names)

con.commit()

equip_file.close()
dir_settings.close()
con.close()