import os
from os.path import isfile
from os.path import join
import docx2txt


def create_zegal_tsv(parent_path):
    datarecords = []
    for x in os.listdir(parent_path):
        if os.path.isdir(join(parent_path, x)):
            files = os.listdir(join(parent_path, x))
            for file in files:
                if file.endswith('.docx'):
                    res = docx2txt.process(join(parent_path + "/" + x, file))
                    res = (res.replace("\n"," ").replace("_", "").replace("Page 1 of 1", "").strip().lower())
                    datarecords.append(x + "\t" + res)
    return datarecords


def write_to_tsv():
    parent_path = "/home/jugs/Documents/zegal/templates/templates/"
    tsv_file_path = "/home/jugs/Documents/zegal/templates/zegal_data.tsv"
    rec = create_zegal_tsv(parent_path)
    with open(tsv_file_path, "w") as fw:
        for line in rec:
            fw.write(line + '\n')
        fw.close()

write_to_tsv()