import pandas as pd
from jinja2 import Template
import re



def validate_field_names(df):
    expected_columns = ['type', 'id', 'name','hosts', 'ipv4', 'ipv6',
                         'city name', 'country iso code', 'country name',
                         'latitude', 'longitude', 'geo.name',
                         'location id', 'site id', 'site name',
                         'site uid', 'site category', 'cmbd ci name',
                         'cmdb ci uid', 'cmdb ci parent name', 'cmdb ci parent uid',
                         'cmdb event category','mode', 'timeout', 'wait', 'tags'
                         ]
    
    for column in expected_columns:
        if column not in df.columns:
            raise ValueError(f"Column '{column}' is missing!.")   

    unexpected_columns = set(df.columns) - set(expected_columns)
    if unexpected_columns:
      raise ValueError(f"Unexpected columns present: {', '.join(unexpected_columns)}") #re-direct for input correction
        
def check_mandatory_fields(df):
    mandatory_fields = ['type', 'id', 'name','hosts']

    for field in mandatory_fields:
        if df[field].isnull().any():
            raise ValueError(f"Mandatory field '{field}' contains null values.") #re-direct for input correction and append it in the excel sheet or should the user go back to the excel sheet?
        

# def check_data_types(df): #validate hosts and country and city drop-down
#     expected_data_types = {'type': object, 'id': object, 'hosts': object,
#                            'ipv4': bool, 'ipv6': bool, 'city name': object, 'country iso code': object,
#                            'country name': object, 'latitude': float,
#                            'longitude': float, 'geo.name': object,
#                            'location id': object, 'site id': object,
#                            'site name': object, 'site uid': object,
#                            'site category': object, 'cmbd ci name': object,
#                            'cmdb ci uid': float, 'cmdb ci parent name': object,
#                            'cmdb ci parent uid': float, 'cmdb event category': object ,
#                            'mode': object, 'timeout': object, 'wait': object, 'tags': object
#                            }
    
#     for column, expected_type in expected_data_types.items():
#         if df[column].dtype != expected_type:
#             raise ValueError(f"Invalid data type for column '{column}'. Expected {expected_type}, got {df[column].dtype}.") #remove function, limit to certain fields or add validation in excel


           
def fix_trailing_spaces(df):
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    return df



def validate_ip_addresses(df):
    ipv4_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    ipv6_pattern = re.compile(r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$')

    for _, row in df.iterrows():
        for host in row['hosts'].split(', '):
            if not ipv4_pattern.match(host) and not ipv6_pattern.match(host):
                raise ValueError(f"Invalid IP address format for host '{host}' in row {row.name}") #re-direct for input correction