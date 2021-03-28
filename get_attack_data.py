import sys
import json
from glob import glob
import os
import const
import csv

MISP_TA='attack_data/threat-actor.json'
SECTOR='attack_data/sector.json'
COMPMAY='attack_data/companies_sorted.csv'
MISP_TOOL='attack_data/mitre-enterprise-attack-tool.json'


tool_dir_name = sys.argv[1]
group_dir_name = sys.argv[2]

def get_tools():
    if (os.path.exists(const.OUT_TOOL_FILE)):
        os.remove(const.OUT_TOOL_FILE)

    tool_list = []

    for file in glob(tool_dir_name + '/*.json'):
        json_open = open(file, 'r')
        data = json.load(json_open)
        tool_name = data.get('objects')[0].get('name')
        tool_list.append(tool_name+ const.NEWLINE)

    json_open = open(MISP_TOOL, 'r')
    data = json.load(json_open)
    values = data.get('values')
    for value in values:
        tool_name=value.get('value').split('-')[0].strip()
        tool_list.append(tool_name+ const.NEWLINE)

        meta = value.get('meta')
        groups = []
        if meta is not None:
            synonyms = meta.get('synonyms')

        if synonyms is not None:
            for synonym in synonyms:
                tool_list.append(synonym.split('-')[0].strip()+ const.NEWLINE)

    for tool_name in tool_list:
        with open(const.OUT_TOOL_FILE, "a", encoding='utf8') as out:
            out.writelines(list(set(tool_list)))


def get_groups():
    if (os.path.exists(const.OUT_GROUP_FILE)):
        os.remove(const.OUT_GROUP_FILE)

    group_list=[]
    for dir in glob(group_dir_name + '/G*'):
        for file in glob(dir + '/*.json'):
            json_open = open(file, 'r')
            data = json.load(json_open)
            group_name = data.get('name')
            group_name=group_name.split(' (')[0]
            group_list.append(group_name+const.NEWLINE)


        json_open = open(MISP_TA, 'r')
        data = json.load(json_open)

        values = data.get('values')

        for value in values:
            group_name=value.get('value')
            group_list.append(group_name+const.NEWLINE)

            meta=value.get('meta')
            groups=[]
            if meta is not None:
                synonyms=meta.get('synonyms')

            if synonyms is not None:
                for synonym in synonyms:
                    group_list.append(synonym+const.NEWLINE)


        with open(const.OUT_GROUP_FILE, "a", encoding='utf8') as out:
            out.writelines(list(set(group_list)))

def get_sectors():
    if (os.path.exists(const.OUT_SECTOR_FILE)):
        os.remove(const.OUT_SECTOR_FILE)

    json_open = open(SECTOR, 'r')
    data = json.load(json_open)
    values = data.get('values')
    for value in values:
        sector=value.get('value')
        with open(const.OUT_SECTOR_FILE, "a", encoding='utf8') as out:
            out.write(sector +const.NEWLINE)

def get_company():
    if (os.path.exists(const.OUT_COMPANY_FILE)):
        os.remove(const.OUT_COMPANY_FILE)

    file = csv.reader(COMPMAY, delimiter=",", doublequote=True, lineterminator=const.NEWLINE, quotechar='"',
                   skipinitialspace=True)

    with open(COMPMAY) as f:
        reader = csv.reader(f)
        next(reader)
        with open(const.OUT_COMPANY_FILE, "a", encoding='utf8') as out:
            for row in reader:
                out.write(row[1] + const.NEWLINE)

get_tools()
# get_groups()
# get_sectors()
#get_company()

