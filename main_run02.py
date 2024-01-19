import pandas as pd
from jinja2 import Template
from functions import validate_field_names, check_mandatory_fields , fix_trailing_spaces, validate_ip_addresses
from yaml_template import yaml_template
from datetime import datetime
import os

def main():
    # Read Excel data into a Pandas DataFrame
    input_excel = 'heartbeat_base_input_template.xlsx'  
    df = pd.read_excel(input_excel, engine='openpyxl', index_col=None)
    #print(df.columns)

    # Validate field names
    validate_field_names(df)

    # Check for mandatory fields
    check_mandatory_fields(df)

    # Check data types
    #check_data_types(df)

    # Fix trailing spaces
    df = fix_trailing_spaces(df)

    # Validate IP address format
    validate_ip_addresses(df)

    now = datetime.now()

    backup_excel_file = 'backup_heartbeat_config.xlsx'
    if os.path.exists(backup_excel_file):
        backup_df = pd.read_excel(backup_excel_file, engine='openpyxl', index_col=None)
        backup_df = pd.concat([backup_df, df], ignore_index=True)
    else:
        backup_df = df.copy()
        #add a column with current date and time
    backup_df['date']= now.strftime('%d-%m-%y')
    backup_df['time']= now.strftime('%H:%M:%S')

    backup_df.to_excel(backup_excel_file, index=False, engine='openpyxl')


    # Create Jinja2 template object
    template = Template(yaml_template)

    # Render YAML data
    yaml_data = template.render(data=df)

    # Save YAML data to a file
    yaml_file = 'heartbeat yaml config file.yaml'
    with open(yaml_file, 'w') as f:
       f.write(yaml_data)

    print(f"YAML data has been successfully written to {yaml_file}.")

    # Append data to Master Excel sheet
    master_excel_file = 'heartbeat_gen_master_data.xlsx'
    if os.path.exists(master_excel_file):
        # Read existing master data
        master_df = pd.read_excel(master_excel_file, engine='openpyxl', index_col=None) #identifying column(s)?
        # Append the new data to the master data
        master_df = pd.concat([master_df, df], ignore_index=True)
    else:
        # If master Excel file doesn't exist, create a new one
        master_df = df.copy()

    # Add a date column with the current date
    master_df['date'] = now.strftime('%d-%m-%y')
    master_df['time'] = now.strftime('%H:%M:%S')

    # Save the updated master data
    master_df.to_excel(master_excel_file, index=False, engine='openpyxl')

    # Delete contents of the input Excel sheet
    
    # Delete contents of the input Excel sheet, keeping only the column headers
    df.iloc[2:, :].to_excel(input_excel, index=False, engine='openpyxl')


        
    print(f"Data has been successfully appended to {master_excel_file} and input Excel sheet has been cleared.")

if __name__ == "__main__":
    main()
    
