dir_settings = open('../../settings.txt', 'r')
dir_path = dir_settings.readlines()[0].split('= ')[1].strip('\n')
file_path = dir_path + 'Language\en\\'

stage_file = open(file_path+'Unlockables.txt')
all_stages = stage_file.readlines()

raw_stage_names = [name.strip('\t\n ,').split(': ') for name in all_stages if '_STAGES' in name]
stage_names = [[name[0].strip('\" ')[22:],name[2].strip('\"')] for name in raw_stage_names]

def add_times_visited(stages, cursor):
    for stage in stages:
        cursor.execute(
            '''
            ALTER TABLE Stage_Info
            ADD Total_Times_Visited_{} INTEGER DEFAULT 0
            '''.format(stage[0])
        )
    
def add_times_completed(stages, cursor):
    for stage in stages:
        cursor.execute(
            '''
            ALTER TABLE Stage_Info
            ADD Total_Times_Completed_{} INTEGER DEFAULT 0
            '''.format(stage[0])
        )

stage_file.close()
dir_settings.close()