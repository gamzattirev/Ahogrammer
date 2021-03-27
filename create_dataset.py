import const
import sys, os

QUESTION_TOOL='What are the tools used in the attack?'
QUESTION_GROUP='Who is the attack group?'

INPUT_FILE='input/attack_report_raw.txt'
VUL_RATE=0.2
LABEL_TRAIN='train'
LABEL_VAL='validation'
SENTENSE_DELIMETER=". "
WORD_DELIMETER=" "
LAVEL_GROUP='B-AT'
LAVEL_I_GROUP='I-AT'
LAVEL_TOOL='B-TL'
LAVEL_I_TOOL='I-TL'
LAVEL_OTHER='0'
DATASET_DELIMETER="\t"
TRAIN_FILE='train.txt'

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

def create_dataset(label,num_data):

    cnt=0

    data=[]

    if label == LABEL_TRAIN:
        data=lines[0:num_data-1]
    elif label==LABEL_VAL:
        data=lines[-num_data:]

    with open(TRAIN_FILE, "a", encoding='utf8') as out:

        for row in data:

            if cnt>num_data:
                return

            sentenses = row.split(SENTENSE_DELIMETER)
            for sentense in sentenses:
                #print(sentense)
                words= sentense.split(WORD_DELIMETER)
                prev=''
                prev_org=''
                dataset=[]
                index=0
                for word in words:
                    lavel = LAVEL_OTHER
                    tmp_word=word.lower()
                    if tmp_word in groups:
                        lavel=LAVEL_GROUP

                    elif prev+WORD_DELIMETER+tmp_word in groups:
                        lavel = LAVEL_I_GROUP
                        #word=prev_org+WORD_DELIMETER+word
                        dataset[index-1]=prev_org + DATASET_DELIMETER + LAVEL_GROUP + const.NEWLINE

                    elif tmp_word in tools or prev+WORD_DELIMETER+tmp_word in tools:
                        lavel=LAVEL_TOOL

                    elif prev + WORD_DELIMETER + tmp_word in tools:
                        lavel = LAVEL_I_TOOL
                        #word = prev_org + WORD_DELIMETER + word
                        dataset[index - 1] = prev_org + DATASET_DELIMETER + LAVEL_TOOL + const.NEWLINE

                    dataset.append(word + DATASET_DELIMETER + lavel + const.NEWLINE)
                    prev=tmp_word
                    prev_org=word
                    index=index+1

                out.writelines(dataset)
                out.write('.'+const.NEWLINE+const.NEWLINE)

        cnt = cnt + 1

with open(INPUT_FILE, 'r') as file:
    lines = file.readlines()


context=len(lines)
print("total context:" +str(context))

if len(sys.argv)>1:
    context  = int(sys.argv[1])

num_val=round(context*VUL_RATE)
num_train=context-num_val
print("num_train:" +str(num_train))
print("num_val:" +str(num_val))

tools=get_tools()
groups=get_groups()

if os.path.exists(TRAIN_FILE):
    os.remove(TRAIN_FILE)

create_dataset(LABEL_TRAIN, num_train)
