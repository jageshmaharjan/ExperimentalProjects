'''
Remove unnecessary columns from column_index 11 and above
For a column name "author_name" if "author_name" is "ZegalBot, delete the record
for the column name "author_email" if the email domain is "@zegal.com or @..." that will
  be y axis, other's will be x axis
If the body have nan or null delete the record
'''


import os
import sys
import pandas as pd
import numpy as np

filepath = "/home/jugs/Documents/zegal/chatlogs/conversations.csv"

# with open(filepath, "r") as fp:
#     data = fp.readlines()
#     print("")

data = pd.read_csv(filepath, low_memory=False)

data = data.drop(data.columns[12], axis=1)
data = data.drop(data.columns[11], axis=1)
data = data.drop(data.columns[10], axis=1)
data = data.drop(data.columns[8], axis=1)
data = data.drop(data.columns[5], axis=1)
data = data.drop(data.columns[4], axis=1)
data = data.drop(data.columns[3], axis=1)
data = data.drop(data.columns[2], axis=1)
data = data.drop(data.columns[0], axis=1)


# data = data.head(200)

'''
To Add a record
rw = [["aaa", 222],["bbb",333]]
newDf = pd.DataFrame(rw, columns=["name", "age"])
newDf = newDf.append(pd.Series(["ppp", 2234], index=newDf.columns), ignore_index=True)
'''

for i, row in data.iterrows():
    if row["author_name"] == "ZegalBot":
        data = data.drop(i, axis=0)
    elif (pd.isna(row['body'])):
        data = data.drop(i, axis=0)
    # if row["author_email"] in ["@zegal.com", "@@dragonlaw.com.hk"]:
    #     small_data["zegal_user"] = row["body"]
       # create a new column

user_x = ""
user_y = ""
text_x = ""
text_y = ""
with open("zegalchatlogProcess.csv", "w") as zf:
    zf.write("User_x\t" + "Chat_x\t" + "User_y\t" + "Chat_y\t" + "datetimestamp\t" + "\n")
    for i, row in data.iterrows():
        if len(str(row["author_email"]).split("@")) != 2:
            pass
        else:
            if str(row["author_email"]).split("@")[1] in ["zegal.com", "dragonlaw.com.hk"]:
                if user_y == row["author_email"]:
                    text_y += " " + row["body"].replace("\t", "")
                else:
                    if text_y != "":
                        # TODO: do the bookkeeping for y
                        datatimstamp = str(row["created_at"])
                        zf.write(user_x + "\t" + text_x + "\t" + user_y + "\t" + text_y + "\t" + datatimstamp +  "\n")
                        # print(user_x + " : " + text_x + " :: " + user_y + " : " + text_y)
                        user_y = ""; user_x = ""; text_x = ""; text_y= ""
                    user_y = row["author_email"]
                    text_y = row["body"].replace("\t", "")
            else:
                if user_x == row["author_email"]:
                    text_x += " " + row["body"].replace("\t", "")
                else:
                    user_x = row["author_email"]
                    text_x = row["body"].replace("\t", "")
    zf.close()

print("None")