#python script containing utility functions for the project
#sub-functions for the main functions in the project
#functions to manage the database, logging, and other utilities
#Author: Henry Frankland
#Date: 04/08/2024

#imports
import bike_db.py
import log_config.py
import os
import csv

import log_config

class LogUtils:
    # setup logging
    log = log_config.LogConfig()
    logger = log.get_logger()

    @staticmethod
    def log_initialisation():
        LogUtils.logger.info("Initialisation complete")

    @staticmethod
    def log_database_connected():
        LogUtils.logger.info("Database connected")

    @staticmethod
    def log_database_disconnected():
        LogUtils.logger.info("Database disconnected")

class DatabaseUtils:
    # setup database
    db = bike_db.BikeDatabase()
    LogUtils.logger.info("Database connected")

    #get table names
    @staticmethod
    def get_table_names():
        try:
            tables = DatabaseUtils.db.get_table_names()
            LogUtils.logger.info("Table names retrieved")
            return tables
        except Exception as e:
            LogUtils.logger.error(f"Error retrieving table names: {e}")
            return None

    #get heading names for table
    @staticmethod
    def get_table_keys(table_name):
        try:
            keys = DatabaseUtils.db.get_table_keys(table_name)
            LogUtils.logger.info(f"Table keys retrieved for {table_name}")
            return keys
        except Exception as e:
            LogUtils.logger.error(f"Error retrieving table keys for {table_name}: {e}")
            return None

    #count rows in table
    @staticmethod
    def count_rows(table_name):
        try:
            count = DatabaseUtils.db.count_rows(table_name)
            LogUtils.logger.info(f"Counted rows in {table_name}")
            return count
        except Exception as e:
            LogUtils.logger.error(f"Error counting rows in {table_name}: {e}")
            return None

    #compare key of dictionary to table headers. return headers else return None
    @staticmethod
    def key_and_table_heading_compare_dic(table_name, data):
        try:
            table_keys = DatabaseUtils.db.get_table_keys(table_name)
            return data.keys() == table_keys
        except Exception as e:
            LogUtils.logger.error(f"Error comparing keys and table headings: {e}")
            return False

    #add row to table, ensure keys match table headers
    @staticmethod
    def add_row(table_name, data):
        if not DatabaseUtils.key_and_table_heading_compare_dic(table_name, data): return None
        try:
            DatabaseUtils.db.add_row(table_name, data)
            LogUtils.logger.info(f"Row added to {table_name}")
        except Exception as e:
            LogUtils.logger.error(f"Error adding row to {table_name}: {e}")

    #delete row from table
    @staticmethod
    def delete_row(table_name, id):
        try:
            DatabaseUtils.db.delete_entry(table_name, id)
            LogUtils.logger.info(f"Row deleted from {table_name}")
        except Exception as e:
            LogUtils.logger.error(f"Error deleting row from {table_name}: {e}")
    
    #edit row in table
    @staticmethod
    def edit_row(table_name, id, data):
        if not DatabaseUtils.key_and_table_heading_compare_dic(table_name, data): return None
        try:
            DatabaseUtils.db.edit_row(table_name, id, data)
            LogUtils.logger.info(f"Row edited in {table_name}")
        except Exception as e:
            LogUtils.logger.error(f"Error editing row in {table_name}: {e}")

    #compare csv headers to table headers
    @staticmethod
    def key_and_table_heading_compare_csv(table_name, import_file):
        try:
            with open(import_file, 'r') as csvfile:
                reader = csv.reader(csvfile)
                keys = next(reader)
            table_keys = DatabaseUtils.db.get_table_keys(table_name)
            return keys == table_keys
        except Exception as e:
            LogUtils.logger.error(f"Error comparing keys and table headings: {e}")
            return False    

    #csv validation
    @staticmethod
    def validate_csv(import_file, table_name):
        if not os.path.exists(import_file): LogUtils.logger.error("File does not exist"); return False
        if not import_file.endswith('.csv'): LogUtils.logger.error("File is not a CSV"); return False
        if not DatabaseUtils.db.table_exists(table_name): LogUtils.logger.error("Table does not exist"); return False
        if not DatabaseUtils.key_and_table_heading_compare_csv(table_name, import_file): LogUtils.logger.error("Keys do not match table headings"); return False        
        return True

    #import csv to table
    @staticmethod
    def import_table(table_name, import_file):
        #gaurd clause/funtion to validate csv
        if not DatabaseUtils.validate_csv(import_file,table_name): return None
        
        #if all checks pass, import the table
        try:           
            with open(import_file, 'r') as csvfile:
                reader = csv.reader(csvfile)
                # read the first row as the keys
                keys = next(reader)
                # read the rest of the rows as the values
                values = [row for row in reader]
            DatabaseUtils.db.import_table(table_name, keys, values)
            LogUtils.logger.info("Table data imported from CSV")
        except Exception as e:
            LogUtils.logger.error(f"Error importing table data from CSV: {e}")
    
    #import table but drop table first
    @staticmethod
    def import_table_drop(table_name, import_file):
        try:
            DatabaseUtils.db.drop_table(table_name)
            DatabaseUtils.db.create_table(table_name)
            DatabaseUtils.import_table(table_name, import_file)
            LogUtils.logger.info("Table data imported from CSV after dropping table")
        except Exception as e:
            LogUtils.logger.error(f"Error importing table data from CSV after dropping table: {e}")

    #write to csv
    @staticmethod
    def export_table(table_name, export_file):
        try:
            data = DatabaseUtils.db.dump_table_dic(table_name)
            if data:
                with open(export_file, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(data.keys())  # Write the keys as the first row
                    writer.writerows(data.values())  # Write the values as subsequent rows
                LogUtils.logger.info("Table data exported as CSV")
            else:
                LogUtils.logger.warning("No data available to export")
        except Exception as e:
            LogUtils.logger.error(f"Error exporting table data as CSV: {e}")
    
    #close connection
    @staticmethod
    def close_connection():
        try:
            DatabaseUtils.db.close()
            LogUtils.logger.info("Database connection closed")
        except Exception as e:
            LogUtils.logger.error(f"Error closing database connection: {e}")

    #connect to database
    @staticmethod
    def connect():
        try:
            DatabaseUtils.db.connect()
            LogUtils.logger.info("Database connected")
        except Exception as e:
            LogUtils.logger.error(f"Error connecting to database: {e}")

    #export table headers as csv
    @staticmethod
    def export_table_headers(table_name, export_file):
        try:
            keys = DatabaseUtils.db.get_table_keys(table_name)
            with open(export_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(keys)
            LogUtils.logger.info("Table headers exported as CSV")
        except Exception as e:
            LogUtils.logger.error(f"Error exporting table headers as CSV: {e}")
    
    #export all tables keys as csv
    @staticmethod
    def export_all_table_headers(dir):
        try:
            #get all table names
            tables = DatabaseUtils.get_table_names()
            #export all table headers
            for table in tables: DatabaseUtils.export_all_table_headers(table, dir+f'{table}.csv')
            LogUtils.logger.info("All table headers exported as CSV")
        except Exception as e:
            LogUtils.logger.error(f"Error exporting all table headers as CSV: {e}")