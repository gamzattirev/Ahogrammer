import const
import sys, os
import string
import random


QUESTION_TOOL='What are the tools used in the attack?'
QUESTION_GROUP='Who is the attack group?'

INPUT_FILE='input/attack_report_raw.txt'
TRAIN_RATE=0.6
VUL_RATE=0.2
LABEL_TRAIN='train'
LABEL_VAL='dev'
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
VAL_FILE='dev.txt'
TEST_FILE='test.txt'
MAX_WORD_NUM=200
MAX_WORD=1000
NUM_SENTENSE_PER_ROW=100
LONG_SENTENSE='long.txt'
O_RATE=1
EXCLUSIVE_LIST=['at']
LEN_RANDOM=10
alldataset={}

KEYWORD_TOOL='tool'
KEYWORD_GROUP='group'

keyword_train={}
keyword_train[KEYWORD_TOOL]=[]
keyword_train[KEYWORD_GROUP]=[]

keyword_dev={}

def get_tools():
    tools=[]
    with open(const.OUT_TOOL_FILE, 'r') as file:
        for row in file:
            tool = row.replace(const.NEWLINE, "")
            #tool = tool.lower()
            tools.append(tool)
        return tools

def get_groups():
    groups=[]
    with open(const.OUT_GROUP_FILE, 'r') as file:
        for row in file:
            group = row.replace(const.NEWLINE, "")
            #group=group.lower()
            groups.append(group)
        return groups

def get_sectors():
    sectors=[]
    with open(const.OUT_SECTOR_FILE, 'r') as file:
        for row in file:
            sector = row.replace(const.NEWLINE, "")
            #sector=sector.lower()
            sectors.append(sector)
        return sectors

def get_companies():
    companies=[]
    with open(const.OUT_COMPANY_FILE, 'r') as file:
        for row in file:
            company = row.replace(const.NEWLINE, "")
            #company=company.lower()
            companies.append(company)
        return companies

def random_str(word):
    dat = string.digits + string.ascii_lowercase + string.ascii_uppercase
    return ''.join([random.choice(dat) for i in range(len(word))]).lower()

def create_dataset(mode,num_dataset):

    cnt=0

    data=[]
    data_O=[]
    data_tag = []

    if mode == LABEL_TRAIN:
        data=lines[:num_train-1]
    elif mode==LABEL_VAL:
        data=lines[num_train:num_train+num_val]

    else:
        data = lines[num_train+num_val:]

    for row in data:

        if cnt>num_dataset:
            print("Exceed "+str(num_data))
            return

        sentenses = row.split(SENTENSE_DELIMETER)
        #print(str(len(sentenses)))
        for sentense in sentenses:
            words= sentense.split(WORD_DELIMETER)
            if len(words) >=MAX_WORD_NUM:
                # with open(LONG_SENTENSE, "a", encoding='utf8') as out_sentense:
                #     out_sentense.write(sentense + const.NEWLINE)
                continue

            len_word=0
            for word in words:
                len_word=len_word+len(word)
            if len_word >= MAX_WORD:
                continue


            prev=''
            prev_org=''
            dataset=[]
            index=0
            for word in words:
                lavel = LAVEL_OTHER
                word=word.strip()
                #tmp_word=word.lower()
                tmp_word = word

                # groups
                if tmp_word in groups:
                    lavel=LAVEL_GROUP

                elif prev+WORD_DELIMETER+tmp_word in groups:
                    lavel = LAVEL_I_GROUP
                    #prev_org = random_str(prev_org)
                    dataset[index - 1] = prev_org + DATASET_DELIMETER + LAVEL_GROUP + const.NEWLINE


                # tools

                elif tmp_word in tools and tmp_word.lower() not in EXCLUSIVE_LIST:
                    lavel=LAVEL_TOOL

                elif prev + WORD_DELIMETER + tmp_word in tools:
                    lavel = LAVEL_I_TOOL
                    #prev_org = random_str(prev_org)
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

                if lavel != LAVEL_OTHER:
                    # word=random_str(word)
                    word = word

                dataset.append(word + DATASET_DELIMETER + lavel + const.NEWLINE)
                prev=tmp_word
                prev_org=word
                index=index+1

            num_data=0
            for item in dataset:
                label=item.split(DATASET_DELIMETER)[1].strip()
                if label!=LAVEL_OTHER:
                    num_data=num_data+1

            if num_data == 0:
                data_O.append(dataset)

            else:
                flag=mode

                if mode == LABEL_TRAIN:
                    data_tag.append(dataset)
                    for item in dataset:
                        word = item.split(DATASET_DELIMETER)[0]
                        label = item.split(DATASET_DELIMETER)[1].strip()
                        if label == LAVEL_GROUP:
                            keyword_train[KEYWORD_GROUP].append(word)
                        elif label == LAVEL_TOOL:
                            keyword_train[KEYWORD_TOOL].append(word)
                else:
                    for item in dataset:
                        word = item.split(DATASET_DELIMETER)[0].strip()
                        label = item.split(DATASET_DELIMETER)[1].strip()
                        if (label == LAVEL_GROUP and word in keyword_train[KEYWORD_GROUP])\
                                or (label == LAVEL_TOOL and word in keyword_train[KEYWORD_TOOL]):
                            flag=LABEL_TRAIN
                            print(word)
                            continue

                    if flag==mode:
                        data_tag.append(dataset)
                    else:
                        alldataset[flag].append(dataset)


        cnt = cnt + 1

    O_num = len(data_O)
    max_O_num = int(O_num* O_RATE)

    alldataset[mode]=data_tag+data_O[:max_O_num]

    return(mode)

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

if os.path.exists(LONG_SENTENSE):
    os.remove(LONG_SENTENSE)

create_dataset(LABEL_TRAIN, num_train)
create_dataset(LABEL_VAL, num_val)
create_dataset(LABEL_TEST, num_test)

with open(LABEL_TRAIN + '.txt', "a", encoding='utf8') as out:
    for dataset in alldataset[LABEL_TRAIN]:
        out.writelines(dataset)
        out.write('.' + DATASET_DELIMETER + LAVEL_OTHER + const.NEWLINE + const.NEWLINE)

with open(LABEL_VAL + '.txt', "a", encoding='utf8') as out:
    for dataset in alldataset[LABEL_VAL]:
        out.writelines(dataset)
        out.write('.' + DATASET_DELIMETER + LAVEL_OTHER + const.NEWLINE + const.NEWLINE)

with open(LABEL_TEST + '.txt', "a", encoding='utf8') as out:
    for dataset in alldataset[LABEL_TEST]:
        out.writelines(dataset)
        out.write('.' + DATASET_DELIMETER + LAVEL_OTHER + const.NEWLINE + const.NEWLINE)