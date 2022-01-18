import sqlite3

con = sqlite3.connect('../run_report_db.db')
cur = con.cursor()

dir_settings = open('../../settings.txt', 'r')
dir_path = dir_settings.readlines()[0].split('= ')[1].strip('\n')
file_path = dir_path + 'Language\en\\'

stage_file = open(file_path+'Unlockables.txt')
all_stages = stage_file.readlines()

stage_names = [name.strip('\t\n ,').split(': ') for name in all_stages if '_STAGES' in name]
clean_stage_names = [[name[0].strip('\" ')[22:],name[2].strip('\"')] for name in stage_names]

def add_times_visited(stages):
    for stage in stages:
        cur.execute(
            '''
            ALTER TABLE Stage_Info
            ADD Total_Times_Visited_{} INTEGER DEFAULT 0
            '''.format(stage[0])
        )
    
def add_times_completed(stages):
    for stage in stages:
        cur.execute(
            '''
            ALTER TABLE Stage_Info
            ADD Total_Times_Completed_{} INTEGER DEFAULT 0
            '''.format(stage[0])
        )

add_times_visited(clean_stage_names)
add_times_completed(clean_stage_names)

con.commit()

stage_file.close()
dir_settings.close()
con.close()