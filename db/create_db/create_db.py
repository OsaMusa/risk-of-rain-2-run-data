import sqlite3
from add_cols import enemies
from add_cols import items
from add_cols import equipment
from add_cols import stages

con = sqlite3.connect('../run_report_db.db')
cur = con.cursor()

cur.executescript(
    '''
    CREATE TABLE Run_Meta_Data (
        Run_ID TEXT NOT NULL,
        Game_Mode TEXT NOT NULL,
        Difficulty TEXT NOT NULL,
        Ending TEXT NOT NULL,
        Run_Date TEXT NOT NULL,
        PRIMARY KEY (Run_ID)
    );
    
    CREATE TABLE Player_Info (
        Run_ID INTEGER NOT NULL,
        Player_Name TEXT NOT NULL,
        Survivor TEXT NOT NULL,
        Total_Time_Alive REAL NOT NULL,
        Total_Distance_Traveled REAL NOT NULL,
        Died TEXT NOT NULL,
        Killer TEXT NOT NULL,
        Highest_Level INTEGER NOT NULL,
        Total_Deaths INTEGER NOT NULL,
        PRIMARY KEY (Run_ID, Player_Name),
        FOREIGN KEY (Run_ID) REFERENCES Run_Meta_Data(Run_ID)
    );

    CREATE TABLE Damage_Stats (
        Run_ID INTEGER NOT NULL,
        Total_Minion_Damage_Dealt INTEGER DEFAULT 0,
        Total_Damage_Dealt INTEGER DEFAULT 0,
        Total_Damage_Taken INTEGER DEFAULT 0,
        Total_Health_Healed INTEGER DEFAULT 0,
        Highest_Damage_Dealt INTEGER DEFAULT 0,
        FOREIGN KEY (Run_ID) REFERENCES Run_Meta_Data(Run_ID)
    );

    CREATE TABLE Kill_Stats (
        Run_ID INTEGER NOT NULL,
        Total_Minion_Kills INTEGER DEFAULT 0,
        Total_Kills INTEGER DEFAULT 0,
        Total_Elite_Kills INTEGER DEFAULT 0,
        Total_Teleporter_Boss_Kills INTEGER DEFAULT 0,
        FOREIGN KEY (Run_ID) REFERENCES Run_Meta_Data(Run_ID)
    );

    CREATE TABLE Purchases (
        Run_ID INTEGER NOT NULL,
        Total_Gold_Collected INTEGER DEFAULT 0,
        Max_Gold_Collected INTEGER DEFAULT 0,
        Total_Purchases INTEGER DEFAULT 0,
        Highest_Purchases INTEGER DEFAULT 0,
        Total_Gold_Purchases INTEGER DEFAULT 0,
        Highest_Gold_Purchases INTEGER DEFAULT 0,
        Total_Blood_Purchases INTEGER DEFAULT 0,
        Highest_Blood_Purchases INTEGER DEFAULT 0,
        Total_Lunar_Purchases INTEGER DEFAULT 0,
        Highest_Lunar_Purchases INTEGER DEFAULT 0,
        Total_Drones_Purchased INTEGER DEFAULT 0,
        Total_Turrets_Purchased INTEGER DEFAULT 0,
        FOREIGN KEY (Run_ID) REFERENCES Run_Meta_Data(Run_ID)
    );

    CREATE TABLE Item_Info (
        Run_ID INTEGER NOT NULL,
        Total_Items_Collected INTEGER DEFAULT 0,
        Highest_Items_Collected INTEGER DEFAULT 0,
        FOREIGN KEY (Run_ID) REFERENCES Run_Meta_Data(Run_ID)
    );

    CREATE TABLE Equipment_Info (
        Run_ID INTEGER NOT NULL,
        FOREIGN KEY (Run_ID) REFERENCES Run_Meta_Data(Run_ID)
    );

    CREATE TABLE Stage_Info (
        Run_ID INTEGER NOT NULL,
        Total_Stages_Completed INTEGER DEFAULT 0,
        Highest_Stages_Completed INTEGER DEFAULT 0,
        FOREIGN KEY (Run_ID) REFERENCES Run_Meta_Data(Run_ID)
    );
    '''
)

enemies.add_dmg_dealt(enemies.enemy_names, cur)
enemies.add_dmg_taken(enemies.enemy_names, cur)
enemies.add_kills(enemies.enemy_names, cur)
enemies.add_elite_kills(enemies.enemy_names, cur)

items.add_total_collected(items.item_names, cur)
items.add_highest_collected(items.item_names, cur)

equipment.add_time_held(equipment.equip_names, cur)
equipment.add_times_fired(equipment.equip_names, cur)

stages.add_times_visited(stages.stage_names, cur)
stages.add_times_completed(stages.stage_names, cur)

con.commit()
con.close()