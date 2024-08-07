import sqlite3
import datetime
import os
import uuid
import json

#call log config class to get logger object
from log_config import LogConfig
log_config = LogConfig()
logger = log_config.get_logger()

#script to track bike expenses, maintenance, and mileage and kwh usage
#database schema
#table: bike_ledger
#columns: id, entry_date, entry_type, bike_id, bike_name, make, manufacture_year, purchase_date, purchase_price, milage, shop_name, website, receipt, notes
#table: bike_expenses
#columns: id, entry_date, expense_date, bike_id, expense_type, title, unit price, quantity, expense_price, shop_name, website, receipt, notes
#table: bike_charging
#columns: id, entry_date, charge_date, bike_id, kwh, ppkwh, solar_charge_percentage, chargable_kwh, price
#table: bike_maintenance
#columns: id, entry_date, maintenance_date, bike_id, maintenance_type, maintenance_price, website, receipt, notes

#a base class with common functions for the indevidual table classes, first check if db exists, if not create it, location sourced from json file
class BikeDatabase:
    def __init__(self, logging_ennabled = False):
        self.logging_ennabled = logging_ennabled
        self.db_file = 'bike_log.db'
        #create db connection
        self.conn = sqlite3.connect(self.db_file)
        self.c = self.conn.cursor()
        self.create_table()
    
    #get tables from json file database_config.json
    def get_tables(self):
        with open('config/database_config.json', 'r') as file:
            data = json.load(file)
        return data['tables']

    #create tables if they dont exist
    def create_table(self, tables):
        for table in tables:
            self.c.execute(f"CREATE TABLE IF NOT EXISTS {table['name']} ({', '.join([f'{columns["name"]} {columns["type"]}' for columns in table['columns']])})")
        self.conn.commit()
    
    def close(self):
        self.conn.close()

    #connect to the database
    def connect(self):
        self.conn = sqlite3.connect(self.db_file)
        self.c = self.conn.cursor()
    
    #check if db exists
    def db_exists(self):
        return os.path.exists(self.db_file)
    
    #sanity check input to ensure its a dictionary
    def is_dict(self, data):
        if isinstance(data, dict):
            return True
        else:
            return False
    
    #function that returns a list of headers for a table
    def get_table_keys(self, table):
        self.c.execute(f"PRAGMA table_info({table})")
        columns = self.c.fetchall()
        column_names = [column[1] for column in columns]
        return column_names
    
    #dump all data from a table to a dictionary
    def dump_table_dic(self, table):
        self.c.execute(f"SELECT * FROM {table}")
        data = self.c.fetchall()
        headings = self.get_table_keys(table)
        data_dict = {}
        for row in data:
            data_dict[row[0]] = dict(zip(headings, row))
        return data_dict
    
    #delete an entry from a table
    def delete_entry(self, table, id):
        self.c.execute(f"DELETE FROM {table} WHERE id = :id", {'id': id})
        self.conn.commit()
    
    #return number of rows in a table
    def count_rows(self, table):
        self.c.execute(f"SELECT COUNT(*) FROM {table}")
        count = self.c.fetchone()
        return count[0]
    
    #get names of all tables in the database
    def get_table_names(self):
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.c.fetchall()
        table_names = [table[0] for table in tables]
        return table_names

    #remove all data from a table
    def clear_table(self, table):
        self.c.execute(f"DELETE FROM {table}")
        self.conn.commit()
    
    #drop a table
    def drop_table(self, table):
        self.c.execute(f"DROP TABLE {table}")
        self.conn.commit()
    
    #import data to a table. inputs are table name, keys, and values list
    def import_table(self, table, keys, values):
        self.c.executemany(f"INSERT INTO {table} VALUES ({', '.join(['?']*len(keys))})", values)
        self.conn.commit()

    #check if a table exists
    def table_exists(self, table):
        self.c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
        if self.c.fetchone():
            return True
        else:
            return False
    
    #add entry to a table ensuring input is a dictionary
    def add_entry(self, table, data):
        if self.is_dict(data):
            data['id'] = str(uuid.uuid4())
            self.c.execute(f"INSERT INTO {table} VALUES ({', '.join(['?']*len(data))})", data)
            self.conn.commit()
        else:
            print('Invalid data')
            return 1
    
    #change entry in a table
    def change_entry(self, table, data):
        if self.is_dict(data):
            self.c.execute(f"UPDATE {table} SET {', '.join([f'{key} = :{key}' for key in data.keys()])} WHERE id = :id", data)
            self.conn.commit()
        else:
            print('Invalid data')
            return 1
    
    #get entry from a table
    def get_entry(self, table, id):
        self.c.execute(f"SELECT * FROM {table} WHERE id = :id", {'id': id})
        entry = self.c.fetchone()
        return entry
    
    #get n entries from a table
    def get_n_entries(self, table, n):
        self.c.execute(f"SELECT * FROM {table} LIMIT {n}")
        entries = self.c.fetchall()
        return entries
    
    #search table data for a string and return all entries in a list
    def search_table(self, table, search_string):
        self.c.execute(f"SELECT * FROM {table}")
        data = self.c.fetchall()
        headings = self.get_table_keys(table)
        search_results = []
        for row in data:
            for item in row:
                if search_string in str(item):
                    search_results.append(dict(zip(headings, row)))
        return search_results

    