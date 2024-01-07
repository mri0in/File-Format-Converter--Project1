import sys
import os
import glob
import json
import re
import pandas as pd


def get_column_names(schema,table_name,sorting_key = 'column_position'):
    column_details = schema[table_name]
    columns = sorted(column_details, key = lambda col: col[sorting_key])
    return [col['column_name'] for col in columns]

def read_csv(file, schemas):
    file_path_list = re.split('[/\\\\]', file)
    data_set_name = file_path_list[-2]
    colmuns = get_column_names(schemas, data_set_name)
    data_frame = pd.read_csv(file, names=colmuns)
    return data_frame

def to_json(data_frame, trg_base_dir, data_set_name, file_name):
    json_file_path = f'{trg_base_dir}/{data_set_name}/{file_name}'
    os.makedirs(f'{trg_base_dir}/{data_set_name}', exist_ok=True)
    data_frame.to_json(json_file_path, orient='records',lines= True)

def file_convertor(data_set_name, src_base_dir, trg_base_dir):

    schemas = json.load(open(f'{src_base_dir}/schemas.json'))
    files =  glob.glob(f'{src_base_dir}/{data_set_name}/part-*')                     
    if len(files)==0:
        raise NameError(f'No files found for {data_set_name}')

    for file in files:
        data_frame = read_csv(file, schemas)
        file_name = re.split('[/\\\\]', file)[-1]
        to_json(data_frame, trg_base_dir, data_set_name, file_name)

def process_files(data_set_names=None):
    src_base_dir = os.environ.get('SRC_BASE_DIR')
    trg_base_dir = os.environ.get('TRG_BASE_DIR')

    schemas = json.load(open(f'{src_base_dir}/schemas.json'))

    if not data_set_names:
        data_set_names = schemas.keys()
    for data_set in data_set_names:
        try:
            print(f'Processing {data_set}')
            file_convertor(data_set, src_base_dir, trg_base_dir)
        except NameError as ne:
            print(ne)
            print(f'Error processing {data_set}')
            pass


if __name__ == '__main__':
    if len(sys.argv)==2:
        data_set_names = json.loads(sys.argv[1])
        process_files(data_set_names)
    else:
        process_files()