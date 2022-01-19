dir_settings = open('../../settings.txt', 'r')
dir_path = dir_settings.readlines()[0].split('= ')[1].strip('\n')
file_path = dir_path + 'Language\en\\'

items_file = open(file_path+'Items.txt', 'r')
all_items = items_file.readlines()

raw_item_names = [name.strip('\t\n ,').split(': ') for name in all_items if '_NAME' in name]
item_names = [[name[0].strip('\" ')[5:-5],name[1].strip('\"')] for name in raw_item_names]

unused_items = ["ANCESTRALINCUBATOR", "COOLDOWNONCRIT", 
                "ELEMENTALRINGS", "EXTRALIFECONSUMED", 
                "LUNARSKILLREPLACEMENTS", "PROTECTIONPOTION", 
                "SKULLCOUNTER", "TONICAFFLICTION"]

def add_total_collected(items, cursor):
    for item in items:
        if item[0] not in unused_items:
            cursor.execute(
                '''
                ALTER TABLE Item_Info
                ADD Total_Collected_{} INTEGER DEFAULT 0
                '''.format(item[0])
            )

def add_highest_collected(items, cursor):
    for item in items:
        if item[0] not in unused_items:
            cursor.execute(
                '''
                ALTER TABLE Item_Info
                ADD Highest_Collected_{} INTEGER DEFAULT 0
                '''.format(item[0])
            )

items_file.close()
dir_settings.close()