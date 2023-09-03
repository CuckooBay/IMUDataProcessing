from argparse import ArgumentParser
import os
from typing import *
from dateutil import parser
import pandas as pd
import time

def record_parse_pc(line: str):
    line = line.strip('\n')
    if line == '': return None, None

def parse_line_pc(line: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    line = line.strip('\n')
    if line == '': return None, None, None
    line = line.split('\t')
    time_str = line[0]
    device_str = line[1]
    angle_str = line[11]
    # print(time_str, device_str)
    # print(time_str, device_str, angle_str)
    return time_str, device_str, angle_str




def process_pc(record_filepath: str, output_path: str):
    record_file = open(record_filepath, 'r', encoding='gbk')
    records = record_file.readlines()
    record_file.close()
    # print(records)
    parse_line_pc(records[1])
    record_dict = dict()
    num_lines = len(records)
    record_dict['timestep'] = []
    for i in range(1, num_lines):
        time_str, device_str, angle_str = parse_line_pc(records[i])
        if i % 3 == 0:
            record_dict['timestep'].append(time_str)
        if device_str not in record_dict.keys():
            record_dict[device_str] = []
        record_dict[device_str].append(angle_str)
    for key in record_dict:
        if key == 'timestep': continue
        print("number of records for device {}:\t{}".format(key, len(record_dict[key])))

    # keys = record_dict.keys()
    # record_dict['timestep'] = [item[0] for item in record_dict[list(record_dict.keys())[0]]]
    # for key in keys:
    #     print("{}\tlength:{}".format(key, len(record_dict[key])))
    # print(record_dict)
    # print(record_dict['timestep'])
    df = pd.DataFrame(data=record_dict)
    df.to_csv(output_path)





def process(walker_file_path, user_file_path, output_file_path):
    walker_file = open(walker_file_path, 'r')
    walker_records = walker_file.readlines()
    walker_file.close()
    user_file = open(user_file_path, 'r')
    user_records = user_file.readlines()
    user_file.close()
    parse_line_pc(walker_records)

if __name__ == '__main__':
    parser = ArgumentParser()
    # parser.add_argument('-w', '--walker_filename', required=True, type=str)
    # parser.add_argument('-u', '--user_filename', type=str, required=True)
    parser.add_argument('-n', '--name', type=str, help='records file name in folder records', default='WT9011DCL-BT50_1693676290713_1.txt')

    parser.add_argument('-o', '--output_path', type=str, required=False, default='output/output.csv', help='path to output file(csv)')

    args = parser.parse_args()

    record_filename = args.name
    record_filepath = os.path.join('records', record_filename)
    # walker_filename = args.walker_filename
    # user_filename = args.user_filename
    # walker_filepath = os.path.join('records', walker_filename)
    # user_filepath = os.path.join('records', user_filename)
    # output_dir = args.output_dir
    # output_file_prefix = args.output_file_prefix
    # output_path = os.path.join(output_dir, output_file_prefix + '.csv')
    output_path = args.output_path
    # process(walker_filepath, user_filepath, output_path)
    process_pc(record_filepath, output_path)