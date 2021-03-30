import const
import sys, os

QUESTION_TOOL='What are the tools used in the attack?'
QUESTION_GROUP='Who is the attack group?'

INPUT_FILE='input/attack_report_raw.txt'
TRAIN_RATE=0.8
VUL_RATE=0.1
LABEL_TRAIN='train'
LABEL_VAL='valid'
LABEL_TEST='test'

SENTENSE_DELIMETER=". "
WORD_DELIMETER=" "
LAVEL_GROUP='B-AT'
LAVEL_I_GROUP='I-AT'
LAVEL_TOOL='B-TL'
LAVEL_I_TOOL='I-TL'
LAVEL_SEC='B-SC'
LAVEL_I_SEC='I-SC'
LAVEL_COM='B-CM'
LAVEL_I_COM='I-CM'
LAVEL_OTHER='O'
DATASET_DELIMETER="\t"
TRAIN_FILE='train.txt'
VAL_FILE='valid.txt'
TEST_FILE='test.txt'

def get_tools():
    tools=[]
    with open(const.OUT_TOOL_FILE, 'r') as file:
        for row in file:
            tool = row.replace(const.NEWLINE, "")
            tool = tool.lower()
            tools.append(tool)
        return tools

def get_groups():
    groups=[]
    with open(const.OUT_GROUP_FILE, 'r') as file:
        for row in file:
            group = row.replace(const.NEWLINE, "")
            group=group.lower()
            groups.append(group)
        return groups

def get_sectors():
    sectors=[]
    with open(const.OUT_SECTOR_FILE, 'r') as file:
        for row in file:
            sector = row.replace(const.NEWLINE, "")
            sector=sector.lower()
            sectors.append(sector)
        return sectors

def get_companies():
    companies=[]
    with open(const.OUT_COMPANY_FILE, 'r') as file:
        for row in file:
            company = row.replace(const.NEWLINE, "")
            company=company.lower()
            companies.append(company)
        return companies

def create_dataset(label,num_data):

    cnt=0

    data=[]

    if label == LABEL_TRAIN:
        data=lines[:num_train-1]
    elif label==LABEL_VAL:
        data=lines[num_train:num_train+num_val]

    else:
        data = lines[num_train+num_val:]

    with open(label+'.txt', "a", encoding='utf8') as out:

        for row in data:

            if cnt>num_data:
                return

            sentenses = row.split(SENTENSE_DELIMETER)
            for sentense in sentenses:
                words= sentense.split(WORD_DELIMETER)
                prev=''
                prev_org=''
                dataset=[]
                index=0
                for word in words:
                    lavel = LAVEL_OTHER
                    word=word.strip()
                    tmp_word=word.lower()

                    # groups
                    if tmp_word in groups:
                        lavel=LAVEL_GROUP

                    elif prev+WORD_DELIMETER+tmp_word in groups:
                        lavel = LAVEL_I_GROUP
                        dataset[index-1]=prev_org + DATASET_DELIMETER + LAVEL_GROUP + const.NEWLINE

                    # tools
                    elif tmp_word in tools:
                        lavel=LAVEL_TOOL

                    elif prev + WORD_DELIMETER + tmp_word in tools:
                        lavel = LAVEL_I_TOOL
                        dataset[index - 1] = prev_org + DATASET_DELIMETER + LAVEL_TOOL + const.NEWLINE

                    # # sectors
                    # elif tmp_word in sectors:
                    #     lavel = LAVEL_SEC
                    #
                    # elif prev + WORD_DELIMETER + tmp_word in sectors:
                    #     lavel = LAVEL_I_SEC
                    #     dataset[index - 1] = prev_org + DATASET_DELIMETER + LAVEL_SEC + const.NEWLINE
                    #
                    # # companies
                    # elif tmp_word in companies:
                    #     lavel = LAVEL_COM
                    #
                    # elif prev + WORD_DELIMETER + tmp_word in companies:
                    #     lavel = LAVEL_I_COM
                    #     dataset[index - 1] = prev_org + DATASET_DELIMETER + LAVEL_COM + const.NEWLINE

                    dataset.append(word + DATASET_DELIMETER + lavel + const.NEWLINE)
                    prev=tmp_word
                    prev_org=word
                    index=index+1

                out.writelines(dataset)
                out.write('.'+ DATASET_DELIMETER+LAVEL_OTHER +const.NEWLINE+const.NEWLINE)

        cnt = cnt + 1

with open(INPUT_FILE, 'r') as file:
    lines = file.readlines()


context=len(lines)
print("total context:" +str(context))

if len(sys.argv)>1:
    context  = int(sys.argv[1])

num_train=round(context*TRAIN_RATE)
num_val=round(context*VUL_RATE)
num_test=context-num_train-num_val
print("num_train:" +str(num_train))
print("num_val:" +str(num_val))
print("num_test:" +str(num_test))

tools=get_tools()
groups=get_groups()
# sectors=get_sectors()
# companies=get_companies()

if os.path.exists(TRAIN_FILE):
    os.remove(TRAIN_FILE)

if os.path.exists(VAL_FILE):
    os.remove(VAL_FILE)

if os.path.exists(TEST_FILE):
    os.remove(TEST_FILE)

create_dataset(LABEL_TRAIN, num_train)
create_dataset(LABEL_VAL, num_val)
create_dataset(LABEL_TEST, num_test)