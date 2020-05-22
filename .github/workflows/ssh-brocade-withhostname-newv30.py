import paramiko
import glob
import time
import os
import sys
import re
import base64
import datetime
import tqdm
import getpass
from datetime import datetime, timedelta
import requests
import pandas as pd
import io
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import warnings

warnings.simplefilter("ignore")
p = paramiko.SSHClient()
usernm = input("Enter the Switch Username:")
passwd = getpass.getpass(prompt='Enter the Switch Password:')
testVar = input("Enter the hostname in issue:")
wwpn1 = testVar.split(';')
wwpnlen = len(wwpn1)

wwpn = 0

keys = []
values = []
values1 = []
name = []
currentdate = datetime.strftime(datetime.now(), "%Y-%m-%d-%H_%M")
output = testVar+ "-" + currentdate + ".txt"
output1 = testVar + "ISL-" + currentdate + ".txt"
f = open(output, "w")
f.close()
f = open("switchshow.txt", "w")
f.close()
isl = 0


def func1(port, p, wwpnsw, switchname, isl):
    global output,output1
    k = 0
    num = 0
    if isl == 1:
        output = output1
    from tqdm import tqdm
    for i in tqdm(range(len(port))):
        # j=i+1
        # print (len(opt1))
        h = j[k]

        with open(output, 'a') as file:
            file.write ("%s - %s"%(testVar,currentdate))
            file.write("+++++++++++++++++++++++\n")
            file.write("%s\n" % h)
            file.write("%s\n\n" % switchname)
            file.write("+++++++++++++++++++++++\n")
            file.write("%s\n" % h)
            k += 1
            file.write('Portperfshow:\n\n')
            file.close()
            stdin, stdout, stderr = p.exec_command('portperfshow "%s" -t 0' % (port[i]))
            out = stdout.readlines()
            out = "".join(out)
            temp1 = open(output, "a")
            temp1.write(out)
            temp1.close()

        with open(output, 'a') as file:
            file.write("\n")
            file.write("+++++++++++++++++++++++\n")
            file.write('Porterrshow:\n\n')
            file.close()
            stdin, stdout, stderr = p.exec_command('porterrshow "%s"' % (port[i]))
            out = stdout.readlines()
            out = "".join(out)
            temp1 = open(output, "a")
            temp1.write(out)
            temp1.close()

        with open(output, 'a') as file:
            # file.write("%s\n" %ls[3])
            file.write("\n")
            file.write("+++++++++++++++++++++++\n")
            file.write('sfpshow:\n\n')
            file.close()
            stdin, stdout, stderr = p.exec_command('sfpshow "%s"' % (port[i]))
            out = stdout.readlines()
            out = "".join(out)
            temp1 = open(output, "a")
            temp1.write(out)
            temp1.close()
        with open(output, 'a') as file:
            # file.write("%s\n" %ls[3])
            file.write("\n")
            file.write("+++++++++++++++++++++++\n")
            file.write('errdump:\n\n')
            file.close()
            stdin, stdout, stderr = p.exec_command('errdump --reverse|grep -i "%s"' % (port[i]))
            out = stdout.readlines()
            out = "".join(out)
            temp1 = open(output, "a")
            temp1.write(out)
            temp1.close()
        with open(output, 'a') as file:
            if num == 0:
                from datetime import datetime, timedelta
                today2 = datetime.today()
                # day=datetime.strftime(today2,'%#d')
                # day_length=len( str(day))
                # if day_length==1:
                # today1=datetime.strftime(today2,'%b  %d')
                # today4=datetime.strftime(datetime.today() - timedelta(2), '%b  %#d')
                # else:
                # today=[]
                # today6=[]
                today1 = datetime.strftime(today2, '%b %#d')
                today4 = datetime.strftime(datetime.today() - timedelta(1), '%b %#d')
                today5 = today2.year
                today3 = str(today5)
                # today=today4,today3
                # today6=today1,today3
                file.write("\n")
                file.write("+++++++++++++++++++++++\n")
                file.write('Fabriclogshow:\n\n')
                file.write("Time Stamp      Input and *Action                           S, P   Sn,Pn  Port  Xid")
                file.write("===================================================================================")
                # print (today1)
                # print (today4)
                # print (today3)
                file.close()
                stdin, stdout, stderr = p.exec_command('fabriclog -s')
                out = stdout.readlines()
                out = "".join(out)
                temp1 = open("fabriclog.txt", "w")
                temp1.write(out)
                temp1.close()

                with open('fabriclog.txt') as infile, open(output, 'a') as outfile:
                    copy = False
                    for line in infile:
                        count = 0
                        if today4 in line and today3 in line:
                            outfile.write("\n")
                            outfile.write(line)
                            count += 1
                            copy = True
                            continue
                        elif line.strip() == '':
                            copy = False
                            break
                        elif copy:
                            outfile.write(line)
                        if count == 0:
                            count1 = 0
                            if today1 in line and today3 in line:
                                count1 += 1
                                outfile.write("\n")
                                outfile.write(line)
                                copy = True
                                continue
                            elif line.strip() == '':
                                copy = False
                                break
                            elif copy:
                                outfile.write(line)
            num += 1


def func(opt1, port, p, j, switchname, isl):
    global output,output1
    k = 0
    num = 0
    if isl == 1:
        output = output1
    from tqdm import tqdm
    for i in tqdm(range(len(opt1))):
        # j=i+1
        # print (len(opt1))
        h = j[k]

        with open(output, 'a') as file:
            file.write("%s\n\n" % switchname)

            file.write("+++++++++++++++++++++++\n")
            file.write("%s\n" % h)
            k += 1
            file.write('Portperfshow:\n\n')
            file.close()
            stdin, stdout, stderr = p.exec_command('portperfshow "%s"/"%s" -t 0' % (opt1[i], port[i]))
            out = stdout.readlines()
            out = "".join(out)
            temp1 = open(output, "a")
            temp1.write(out)
            temp1.close()

        with open(output, 'a') as file:
            file.write("\n")
            file.write("+++++++++++++++++++++++\n")
            file.write('Porterrshow:\n\n')
            file.close()
            stdin, stdout, stderr = p.exec_command('porterrshow "%s"/"%s"' % (opt1[i], port[i]))
            out = stdout.readlines()
            out = "".join(out)
            temp1 = open(output, "a")
            temp1.write(out)
            temp1.close()

        with open(output, 'a') as file:
            # file.write("%s\n" %ls[3])
            file.write("\n")
            file.write("+++++++++++++++++++++++\n")
            file.write('sfpshow:\n\n')
            file.close()
            stdin, stdout, stderr = p.exec_command('sfpshow "%s"/"%s"' % (opt1[i], port[i]))
            out = stdout.readlines()
            out = "".join(out)
            temp1 = open(output, "a")
            temp1.write(out)
            temp1.close()
        with open(output, 'a') as file:
            # file.write("%s\n" %ls[3])
            file.write("\n")
            file.write("+++++++++++++++++++++++\n")
            file.write('errdump:\n\n')
            file.close()
            stdin, stdout, stderr = p.exec_command('errdump --reverse|grep -i "SLOT "%s""' % (opt1[i]))
            out = stdout.readlines()
            out = "".join(out)
            temp1 = open(output, "a")
            temp1.write(out)
            temp1.close()
        with open(output, 'a') as file:
            if num == 0:
                from datetime import datetime, timedelta
                today2 = datetime.today()
                # day=datetime.strftime(today2,'%#d')
                # day_length=len( str(day))
                # if day_length==1:
                # today1=datetime.strftime(today2,'%b  %d')
                # today4=datetime.strftime(datetime.today() - timedelta(2), '%b  %#d')
                # else:
                # today=[]
                # today6=[]
                today1 = datetime.strftime(today2, '%b %#d')
                today4 = datetime.strftime(datetime.today() - timedelta(1), '%b %#d')
                today5 = today2.year
                today3 = str(today5)
                # today=today4,today3
                # today6=today1,today3
                file.write("\n")
                file.write("+++++++++++++++++++++++\n")
                file.write('Fabriclogshow:\n\n')
                file.write("Time Stamp      Input and *Action                           S, P   Sn,Pn  Port  Xid")
                file.write("===================================================================================")
                # print (today1)
                # print (today4)
                # print (today3)
                file.close()
                stdin, stdout, stderr = p.exec_command('fabriclog -s')
                out = stdout.readlines()
                out = "".join(out)
                temp1 = open("fabriclog.txt", "w")
                temp1.write(out)
                temp1.close()

                with open('fabriclog.txt') as infile, open(output, 'a') as outfile:
                    copy = False
                    for line in infile:
                        count = 0
                        if today4 in line and today3 in line:
                            outfile.write("\n")
                            outfile.write(line)
                            count += 1
                            copy = True
                            continue
                        elif line.strip() == '':
                            copy = False
                            break
                        elif copy:
                            outfile.write(line)
                        if count == 0:
                            count1 = 0
                            if today1 in line and today3 in line:
                                count1 += 1
                                outfile.write("\n")
                                outfile.write(line)
                                copy = True
                                continue
                            elif line.strip() == '':
                                copy = False
                                break
                            elif copy:
                                outfile.write(line)
            num += 1


##string='SmIzcmQxbmc='
##passw=(base64.b64decode(string))
##passwd=passw.decode('utf-8')
# print (base64.b64encode(string.encode()))
# print(passwd)
f = open("database.txt", "w")
f.close()
f = open("memberdatabase.txt", "w")
f.close()
f = open("fabricshow.txt", "w")
f.close()
f = open("newfile.txt", "w")
f.close()
cred = open("cred.csv", "r")
cred = open("cred.csv", "r")
for i in cred.readlines():
    for j in wwpn1:
        line = i.strip()
        ls = line.split(",")
        print("Zone associated to the Host:%s in %s" % (j, ls[3]))
        p.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        p.connect("%s" % ls[0], port=22, username="%s" % usernm, password="%s" % passwd)
        stdin, stdout, stderr = p.exec_command('zoneshow --validate *"%s"*|grep -i -A100 Effective' % (j))
        opt = stdout.readlines()
        opt = "".join(opt)
        temp1 = open("memberdatabase.txt", "a")
        temp1.write(opt)
        print(opt)
        temp1.close()

        if opt:
            stdin, stdout, stderr = p.exec_command('fabricshow')
            opt1 = stdout.readlines()
            opt1 = "".join(opt1)
            print(opt1)
            temp1 = open("fabricshow.txt", "a")
            temp1.write(opt1)
            temp1.close()
cred.close()
bad_words = ['Switch', '-------------------------------------------------------------------------', 'Fabric']
with open('fabricshow.txt', 'r') as oldfile:
    for line in oldfile:
        if not line.isspace():
            if not any(bad_word in line for bad_word in bad_words):
                linesplit = line.strip().split()
                values1.append(linesplit[0])
                keys.append(linesplit[1])
                values.append(linesplit[3])
                name.append(linesplit[5])
if os.stat("memberdatabase.txt").st_size == 0:
    print("no active zones associated to this host")
    sys.exit()

values1 = [w[:-1] for w in values1]
keys = [w[-2:] for w in keys]
mapf = dict(zip(keys, values))
domainidm = dict(zip(keys, values1))
domainidip = dict(zip(values1, values))
switchnamemap = dict(zip(keys, name))
switchnamemap1 = dict(zip(values1, name))
print(mapf)
print(domainidm)
print(domainidip)
print(switchnamemap)
data = []
zone = []
cred = open("memberdatabase.txt", "r")
copy = False
count = 0
count1 = 0
for line in cred.readlines():
    line = line.strip()
    cond = "zone:"
    if cond in line.strip():
        copy = True
        if count > 1:
            zone.append(count)
        continue
    elif line.strip() == "------------------------------------":
        copy = False
        continue
    elif copy:
        ##        if "*" in line:
        ##            copy = False
        ##            continue
        ##        else:
        data.append(line)
        count += 1

data_len = len(data)
data_lenh = (data_len) // 2
print(data)
print(data_lenh)
i = 0
k = 0
l = []

##zonelen=len(zone)+1
##new_list=[]  # start with a list containing an empty sub-list
##new_list=[data[i:j] for i, j in zip([0]+zone, zone+[None
##count=0
##for x,item in enumerate(data1):
##  
##  
##  if "*" in item:
##    data.remove(item)  
##    if x == 0 or x % 2 == 0:
##          del data[x]
##          print (data)
##       
##    else :
##        x=x-1
##        del data[x]
##
##
####  else:
####    count+=1
if len(data) == 0:
    sys.exit()

d2 = []
d1 = []
d3 = []
length1 = 0

j = 0
count = 0
cred = open("cred.csv", "r")
for i in cred.readlines():
    if count == len(data):
        break
    for j in range(len(data)):
        ##    if j == data_lenh:
        ##      length1=data_lenh
        ##      data_lenh=data_lenh+data_lenh
        ##      continue
        ##    if j==len(data):
        ##      break

        line = i.strip()
        ls = line.split(",")
        p.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        p.connect("%s" % ls[0], port=22, username="%s" % usernm, password="%s" % passwd)
        stdin, stdout, stderr = p.exec_command('nszonemember "%s"|grep -i -A1 "%s"' % (data[j], data[j]))
        opt = stdout.readlines()
        opt = "".join(opt)

        if opt:
            if "Initiator" in opt:
                d1.append(data[j])
                count += 1
            if "Target" in opt:
                d2.append(data[j])
                count += 1
            if "Unknown" in opt:
                if data[j].startswith("50:"):
                    d2.append(data[j])
                    count += 1
                else:
                    d1.append(data[j])
                    count += 1


        else:
            if data[j].startswith("50:"):
                d2.append(data[j])
                count += 1
            else:
                d1.append(data[j])
                count += 1

if len(d1) == 1:
    halflen = 1
else:
    halflen = len(d1) // 2
length = 0
print(d1)
print(d2)
for i in range(len(d1)):
    print("Initiator:%s" % (d1[i]))
for i in range(len(d2)):
    print("Target:%s" % (d2[i]))

f = open("nodefindatabase.txt", "w")
f.close()
cred = open("cred.csv", "r")
count = 0
local = []

init = []
tgt = []
index1 = []
initiator = []
target = []
count = 0
count1 = 0
for i in cred.readlines():

    line = i.strip()
    ls = line.split(",")
    p.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    p.connect("%s" % ls[0], port=22, username="%s" % usernm, password="%s" % passwd)
    if length == len(d1):
        length = len(d1) // 2

    ## print(range(length,halflen))
    f = 1
    if count1 == len(data):
        break
    for j in range(length, halflen):

        if count1 == len(data):
            break
        stdin, stdout, stderr = p.exec_command('nodefind "%s"|grep -A1 Pid|grep -v Pid' % d1[j])

        opt = stdout.readlines()
        opt = "".join(opt)
        temp1 = open("test.txt", "w")
        ##    print (opt)
        temp1.write(opt)
        if opt:
            count1 += 1
        if not opt:
            count += 1
            if "*" in d1[j]:
                print('"%s"is offline,check the port status using partner fabric port details' % d1[j])
            if count == (halflen - 1):
                length = halflen
                halflen = len(d1)
                break
            continue
        temp1.close()
        with open("test.txt") as input_file:
            for line in input_file:
                linesplit = line.strip().split()  # splits by whitespace
                init = (str(linesplit[1]))
                initiator = (int((init[2:4]), 16))
                initdomainid = (init[0:2])
        if os.stat("test.txt").st_size == 0:
            continue
        stdin, stdout, stderr = p.exec_command('nodefind "%s"|grep -A1 Pid|grep -v Pid' % d2[j])
        opt1 = stdout.readlines()
        opt1 = "".join(opt1)
        temp2 = open("test.txt", "w")
        temp2.write(opt1)
        if opt1:
            count1 += 1
        if not opt1:
            count += 1
            if "*" in d2[j]:
                print('"%s"is offline, check the port status using partner fabric port details' % d2[j])
            if count == (halflen - 1):
                length = halflen
                halflen = len(d1)
                break
            continue
        temp2.close()
        with open("test.txt") as input_file:
            for line in input_file:
                linesplit = line.strip().split()  # splits by whitespace
                tgt = (str(linesplit[1]))
                target = (int((tgt[2:4]), 16))
                tgtdomainid = (tgt[0:2])
        if os.stat("test.txt").st_size == 0:
            continue
        p.connect("%s" % mapf[initdomainid], port=22, username="%s" % usernm, password="%s" % passwd)
        stdin, stdout, stderr = p.exec_command('pathinfo %s %s %s' % (domainidm[tgtdomainid], initiator, target))
        switchname = switchnamemap[initdomainid]
        print('pathinfo %s %s %s' % (domainidm[tgtdomainid], initiator, target))
        opt2 = stdout.readlines()
        opt2 = "".join(opt2)
        temp = open("pathinfo.txt", "w")
        temp.write(opt2)
        temp.close()
        f = open("switchshow.txt", "w")
        f.close()
        data1 = list(dict.fromkeys(data))
        opt1 = []
        port = []
        wwpnsw = []
        with open("pathinfo.txt") as f:
            with open(output, "a") as f1:
                for line in f:
                    if "ROW" in line:
                        f1.write(line)
        if "self" in opt2:
            if tgt:
                init1 = init[0:-2]
                tgt1 = tgt[0:-2]
                # p.connect("%s"%mapf[initdomainid],port =22, username = "admin", password="%s"%passwd)
                stdin, stdout, stderr = p.exec_command('switchshow|grep "%s";switchshow|grep "%s"' % (init1, tgt1))
                opt = stdout.readlines()
                opt = "".join(opt)
                ##         print (opt)
                temp = open("switchshow.txt", "w")
                temp.write(opt)
                temp.close()
                stdout.flush()
                stdin, stdout, stderr = p.exec_command('switchshow|grep Slot|grep Port')
                res = stdout.readlines()
                res = "".join(res)
                if res:
                    with open('switchshow.txt') as f:
                        for line in f:
                            # print (line)
                            linesplit = line.strip().split()
                            opt1.append(int(linesplit[1]))  # 2nd index
                            port.append(int(linesplit[2]))
                            wwpnsw.append(linesplit[9:])
                        f.close()
                    print('Switchname:"%s",Slot:"%s",Port:"%s"' % (switchname, opt1, port))
                    isl = 0
                    func(opt1, port, p, wwpnsw, switchname, isl)
                else:
                    with open('switchshow.txt') as f:
                        for line in f:
                            # print (line)
                            linesplit = line.strip().split()
                            # 2nd index
                            port.append(int(linesplit[1]))
                            wwpnsw.append(linesplit[8:])
                        f.close()
                    print('Switchname:"%s",Port:"%s"' % (switchname, port))
                    isl = 0
                    func1(port, p, wwpnsw, switchname, isl)
        else:
            pathdomain = []
            with open('pathinfo.txt') as input_data:
                # Skips text before the beginning of the interesting block:
                for line in input_data:
                    if line.strip() == '-----------------------------------------------------------------------------':  # Or whatever test is needed
                        break
                # Reads text until the end of the block:
                for line in input_data:  # This keeps reading the file
                    if line.strip() == '':
                        break
                    linesplit = line.strip().split()
                    pathdomain.append(linesplit[2])

            pathdomainlen = len(pathdomain)

            for x, y in enumerate(pathdomain):
                if x == 0:
                    opt1 = []
                    port = []
                    wwpnsw = []
                    init1 = (init[0:-2])
                    p.connect("%s" % domainidip[y], port=22, username="%s" % usernm, password="%s" % passwd)
                    stdin, stdout, stderr = p.exec_command('switchshow|grep "%s";switchshow|grep "E-Port"' % init1)
                    switchname = switchnamemap1[y]
                    opt = stdout.readlines()
                    opt = "".join(opt)
                    ##         print (opt)
                    temp = open("switchshow.txt", "w")
                    temp.write(opt)
                    temp.close()
                    stdout.flush()
                    stdin, stdout, stderr = p.exec_command('switchshow|grep Slot|grep Port')
                    res = stdout.readlines()
                    res = "".join(res)
                    if res:
                        with open('switchshow.txt') as f:
                            for line in f:
                                # print (line)
                                linesplit = line.strip().split()
                                opt1.append(int(linesplit[1]))  # 2nd index
                                port.append(int(linesplit[2]))
                                wwpnsw.append(linesplit[9:])
                            f.close()
                        print('Switchname:"%s",Slot:"%s",Port:"%s"' % (switchname, opt1, port))
                        isl = 1
                        func(opt1, port, p, wwpnsw, switchname, isl)
                    else:
                        with open('switchshow.txt') as f:
                            for line in f:
                                # print (line)
                                linesplit = line.strip().split()
                                # 2nd index
                                port.append(int(linesplit[1]))
                                wwpnsw.append(linesplit[8:])
                            f.close()
                            print('Switchname:"%s",Port:"%s"' % (switchname, port))
                            isl = 1
                            func1(port, p, wwpnsw, switchname, isl)
                elif x == (len(pathdomain) - 1):
                    print(y)
                    tgt1 = (tgt[0:-2])
                    opt1 = []
                    port = []
                    wwpnsw = []
                    p.connect("%s" % domainidip[y], port=22, username="%s" % usernm, password="%s" % passwd)
                    stdin, stdout, stderr = p.exec_command('switchshow|grep "%s"' % tgt1)
                    switchname = switchnamemap1[y]
                    opt = stdout.readlines()
                    opt = "".join(opt)
                    temp = open("switchshow.txt", "w")
                    temp.write(opt)
                    temp.close()
                    stdout.flush()
                    stdin, stdout, stderr = p.exec_command('switchshow|grep Slot|grep Port')
                    res = stdout.readlines()
                    res = "".join(res)
                    if res:

                        with open('switchshow.txt') as f:
                            for line in f:
                                # print (line)
                                linesplit = line.strip().split()
                                opt1.append(int(linesplit[1]))  # 2nd index
                                port.append(int(linesplit[2]))
                                wwpnsw.append(linesplit[9:])
                            f.close()
                            print('Switchname:"%s",Slot:"%s",Port:"%s"' % (switchname, opt1, port))
                            isl = 0
                            func(opt1, port, p, wwpnsw, switchname, isl)
                            if j == (halflen - 1):
                                length = halflen
                                halflen = len(d1)
                                break
                    else:
                        with open('switchshow.txt') as f:
                            for line in f:
                                # print (line)
                                linesplit = line.strip().split()
                                # 2nd index
                                port.append(int(linesplit[1]))
                                wwpnsw.append(linesplit[8:])
                            f.close()
                            print('Switchname:"%s",Port:"%s"' % (switchname, port))
                            isl = 0
                            func1(port, p, wwpnsw, switchname, isl)

                            if j == (halflen - 1):
                                length = halflen
                                halflen = len(d1)
                                break

                ##           print (length,halflen,count)

                else:
                    opt1 = []
                    port = []
                    wwpnsw = []
                    p.connect("%s" % domainidip[y], port=22, username="%s" % usernm, password="%s" % passwd)
                    stdin, stdout, stderr = p.exec_command('switchshow|grep "E-Port"')
                    switchname = switchnamemap1[y]
                    opt = stdout.readlines()
                    opt = "".join(opt)
                    temp = open("switchshow.txt", "w")
                    temp.write(opt)
                    temp.close()
                    stdout.flush()
                    stdin, stdout, stderr = p.exec_command('switchshow|grep Slot|grep Port')
                    res = stdout.readlines()
                    res = "".join(res)
                    if res:
                        with open('switchshow.txt') as f:
                            for line in f:
                                # print (line)
                                linesplit = line.strip().split()
                                opt1.append(int(linesplit[1]))  # 2nd index
                                port.append(int(linesplit[2]))
                                wwpnsw.append(linesplit[9:])
                            f.close()
                        print('Switchname:"%s",Slot:"%s",Port:"%s"' % (switchname, opt1, port))
                        isl = 1
                        func(opt1, port, p, wwpnsw, switchname, isl)
                    else:
                        with open('switchshow.txt') as f:
                            for line in f:
                                # print (line)
                                linesplit = line.strip().split()
                                # 2nd index
                                port.append(int(linesplit[1]))
                                wwpnsw.append(linesplit[8:])
                            f.close()
                        print('Switchname:"%s",Port:"%s"' % (switchname, port))
                        isl = 1
                        func1(port, p, wwpnsw, switchname, isl)

    if len(d1) < 1 or len(d2) < 1:
        sys.exit()
    if j == len(d1):
        continue

    if j == (halflen - 1):
        length = halflen
        halflen = len(d1)
        continue

cred.close()
my = os.getcwd()
testVar1 = "graph\\"
testVar1 = testVar1 + testVar
my_folder = os.path.join(my, testVar1)
if not os.path.exists(my_folder):
    os.makedirs(my_folder)
endTime = datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%MZ")
startTime = datetime.strftime(datetime.now() - timedelta(1), "%Y-%m-%dT%H:%MZ")
cred = open("DM_report.csv", "r")
array_name = []
Lun_name = []
portname1 = []
portname = []
for i in cred.readlines():
    line = i.strip()
    ls = line.split(",")
    if testVar in line:
        array_name.append(ls[1])
        Lun_name.append(ls[3])
        portname1.append(ls[4])

array_name = list(dict.fromkeys(array_name))
Lun_name = list(dict.fromkeys(Lun_name))
portname = [x for xs in portname1 for x in xs.split(';')]
portname = list(dict.fromkeys(portname))
cred1 = open("DM_IP.csv", "r")
array_instancename = []
array_instanceip = []

for i in cred1.readlines():
    for y in array_name:
        line = i.strip()
        ls = line.split(",")

        if y in ls:
            array_instancename.append(ls[3])
            array_instanceip.append(ls[4])

date = time.strftime("%Y-%m-%d")
for i in range(len(array_name)):
    params = (
        ('agentType', 'RAID'),
        ('agentInstanceName', array_name[i]),
        ('fields',
         'DATETIME\x1FLDEV_NUMBER\x1FREAD_IO_COUNT\x1FWRITE_IO_COUNT\x1FREAD_MBYTES\x1FWRITE_MBYTES\x1FREAD_RESPONSE_RATE\x1FWRITE_RESPONSE_RATE\x1FTOTAL_RESPONSE_RATE'),
        ('pfmHostName', array_instancename[i]),
        ('startTime', startTime),
        ('endTime', endTime),
        ('LDEV_NUMBER', Lun_name),
    )

response = requests.get('http://%s:24221/TuningAgent/v1/objects/PI_LDS' % array_instanceip[i], params=params,
                        verify=False)

# print (response.content)
df = pd.read_csv(io.StringIO(response.content.decode('ascii')))
df1 = df.drop(df.index[0])
df.to_csv(''+array_instancename[i]+'-'+testVar+'LUNperfdetails.csv')
df1['DATETIME'] = pd.to_datetime(df1['DATETIME'])
for i in range(len(Lun_name)):
    # plt.plot(df.loc[df['LDEV_NUMBER'] =='%s'%Lun_name[i]]['RECORD_TIME'], df.loc[df['LDEV_NUMBER'] == '%s'%Lun_name[i]]['READ_IO_COUNT'])
    X = list(df1.loc[df1['LDEV_NUMBER'] == '%s' % Lun_name[i]]['DATETIME'])
    Y = list(df1.loc[df1['LDEV_NUMBER'] == '%s' % Lun_name[i]]['READ_IO_COUNT'])
    ax = plt.axes()
    ax.xaxis.set_minor_locator(dates.HourLocator(interval=4))  # every 4 hours
    ax.xaxis.set_minor_formatter(dates.DateFormatter('%H:%M'))  # hours and minutes
    ax.xaxis.set_major_locator(dates.DayLocator(interval=1))  # every day
    ax.xaxis.set_major_formatter(dates.DateFormatter('\n%d-%m-%Y'))

    for i in range(len(Y)):
        Y[i] = int(Y[i])
    plt.plot(X, Y)
    plt.ylabel('Read IOPS/sec')
    plt.xlabel('Time')
    plt.legend(Lun_name)

plt.savefig('' + my_folder + '\lunreadiocount' + date + '.png')
plt.clf()
plt.close()
for i in range(len(Lun_name)):
    X = []
    Y = []
    # plt.plot(df.loc[df['LDEV_NUMBER'] =='%s'%Lun_name[i]]['RECORD_TIME'], df.loc[df['LDEV_NUMBER'] == '%s'%Lun_name[i]]['READ_IO_COUNT'])
    X = list(df1.loc[df1['LDEV_NUMBER'] == '%s' % Lun_name[i]]['DATETIME'])
    Y = list(df1.loc[df1['LDEV_NUMBER'] == '%s' % Lun_name[i]]['WRITE_IO_COUNT'])
    ax = plt.axes()
    ax.xaxis.set_minor_locator(dates.HourLocator(interval=4))  # every 4 hours
    ax.xaxis.set_minor_formatter(dates.DateFormatter('%H:%M'))  # hours and minutes
    ax.xaxis.set_major_locator(dates.DayLocator(interval=1))  # every day
    ax.xaxis.set_major_formatter(dates.DateFormatter('\n%d-%m-%Y'))
    for i in range(len(Y)):
        Y[i] = int(Y[i])
    plt.plot(X, Y)
    plt.ylabel('Write IOPS/sec')
    plt.xlabel('Time')
    plt.legend(Lun_name)

plt.savefig('' + my_folder + '\lunwriteiocount' + date + '.png')
plt.clf()
plt.close()
for i in range(len(Lun_name)):
    X = []
    Y = []
    # plt.plot(df.loc[df['LDEV_NUMBER'] =='%s'%Lun_name[i]]['RECORD_TIME'], df.loc[df['LDEV_NUMBER'] == '%s'%Lun_name[i]]['READ_IO_COUNT'])
    X = list(df1.loc[df1['LDEV_NUMBER'] == '%s' % Lun_name[i]]['DATETIME'])
    Y = list(df1.loc[df1['LDEV_NUMBER'] == '%s' % Lun_name[i]]['READ_MBYTES'])
    ax = plt.axes()
    ax.xaxis.set_minor_locator(dates.HourLocator(interval=4))  # every 4 hours
    ax.xaxis.set_minor_formatter(dates.DateFormatter('%H:%M'))  # hours and minutes
    ax.xaxis.set_major_locator(dates.DayLocator(interval=1))  # every day
    ax.xaxis.set_major_formatter(dates.DateFormatter('\n%d-%m-%Y'))
    for i in range(len(Y)):
        Y[i] = int(Y[i])
    print("Max lun read bandwidth:", max(Y))
    plt.plot(X, Y)
    plt.ylabel('Read Bandwidth(MB/s)')
    plt.xlabel('Time')
    plt.legend(Lun_name)

plt.savefig('' + my_folder + '\lunreadbandwidth' + date + '.png')
plt.clf()
plt.close()
for i in range(len(Lun_name)):
    X = []
    Y = []
    # plt.plot(df.loc[df['LDEV_NUMBER'] =='%s'%Lun_name[i]]['RECORD_TIME'], df.loc[df['LDEV_NUMBER'] == '%s'%Lun_name[i]]['READ_IO_COUNT'])
    X = list(df1.loc[df1['LDEV_NUMBER'] == '%s' % Lun_name[i]]['DATETIME'])
    Y = list(df1.loc[df1['LDEV_NUMBER'] == '%s' % Lun_name[i]]['WRITE_MBYTES'])
    ax = plt.axes()
    ax.xaxis.set_minor_locator(dates.HourLocator(interval=4))  # every 4 hours
    ax.xaxis.set_minor_formatter(dates.DateFormatter('%H:%M'))  # hours and minutes
    ax.xaxis.set_major_locator(dates.DayLocator(interval=1))  # every day
    ax.xaxis.set_major_formatter(dates.DateFormatter('\n%d-%m-%Y'))
    for i in range(len(Y)):
        Y[i] = int(Y[i])
    print("Max lun write bandwidth:", max(Y))
    plt.plot(X, Y)
    plt.legend(Lun_name)
    plt.ylabel('Write Bandwidth(MB/s)')
    plt.xlabel('Time')

plt.savefig('' + my_folder + '\lunwritebandwidth' + date + '.png')
plt.clf()
plt.close()
for i in range(len(Lun_name)):
    X = []
    Y = []
    # plt.plot(df.loc[df['LDEV_NUMBER'] =='%s'%Lun_name[i]]['RECORD_TIME'], df.loc[df['LDEV_NUMBER'] == '%s'%Lun_name[i]]['READ_IO_COUNT'])
    X = list(df1.loc[df1['LDEV_NUMBER'] == '%s' % Lun_name[i]]['DATETIME'])
    Y = list(df1.loc[df1['LDEV_NUMBER'] == '%s' % Lun_name[i]]['READ_RESPONSE_RATE'])
    ax = plt.axes()
    ax.xaxis.set_minor_locator(dates.HourLocator(interval=4))  # every 4 hours
    ax.xaxis.set_minor_formatter(dates.DateFormatter('%H:%M'))  # hours and minutes
    ax.xaxis.set_major_locator(dates.DayLocator(interval=1))  # every day
    ax.xaxis.set_major_formatter(dates.DateFormatter('\n%d-%m-%Y'))
    for i in range(len(Y)):
        Y[i] = float(Y[i])
    plt.plot(X, Y)
    plt.legend(Lun_name)
    plt.ylabel('Read latency(Micro seconds)')
    plt.xlabel('Time')

plt.savefig('' + my_folder + '\lunreadlatency' + date + '.png')
plt.clf()
plt.close()
for i in range(len(Lun_name)):
    X = []
    Y = []
    # plt.plot(df.loc[df['LDEV_NUMBER'] =='%s'%Lun_name[i]]['RECORD_TIME'], df.loc[df['LDEV_NUMBER'] == '%s'%Lun_name[i]]['READ_IO_COUNT'])
    X = list(df1.loc[df1['LDEV_NUMBER'] == '%s' % Lun_name[i]]['DATETIME'])
    Y = list(df1.loc[df1['LDEV_NUMBER'] == '%s' % Lun_name[i]]['WRITE_RESPONSE_RATE'])
    ax = plt.axes()
    ax.xaxis.set_minor_locator(dates.HourLocator(interval=4))  # every 4 hours
    ax.xaxis.set_minor_formatter(dates.DateFormatter('%H:%M'))  # hours and minutes
    ax.xaxis.set_major_locator(dates.DayLocator(interval=1))  # every day
    ax.xaxis.set_major_formatter(dates.DateFormatter('\n%d-%m-%Y'))
    for i in range(len(Y)):
        Y[i] = float(Y[i])
    plt.plot(X, Y)
    plt.legend(Lun_name)
    plt.ylabel('write latency(Micro seconds)')
    plt.xlabel('Time')

plt.savefig('' + my_folder + '\lunwritelatency' + date + '.png')
plt.clf()
plt.close()
for i in range(len(array_name)):
    params1 = (
        ('agentType', 'RAID'),
        ('agentInstanceName', array_name[i]),
        ('fields', 'DATETIME\x1FPORT_NAME\x1FTOTAL_MBYTES\x1FREAD_TOTAL_RESPONSE\x1FWRITE_TOTAL_RESPONSE'),
        ('pfmHostName', array_instancename[i]),
        ('startTime', startTime),
        ('endTime', endTime),
        ('PORT_NAME', portname),
    )
response1 = requests.get('http://161.89.194.57:24221/TuningAgent/v1/objects/PI_PTS', params=params1, verify=False)
df2 = pd.read_csv(io.StringIO(response1.content.decode('ascii')))
df3 = df2.drop(df2.index[0])
df2.to_csv(''+array_instancename[i]+'-Portperfdetails.csv')
df3['DATETIME'] = pd.to_datetime(df3['DATETIME'])
# print("port total bytes:", df3['TOTAL_MBYTES'].max())
# print("port total read response:", df3['READ_TOTAL_RESPONSE'].max())
# print("port total write response:", df3['WRITE_TOTAL_RESPONSE'].max())
for i in range(len(portname)):
    # plt.plot(df.loc[df['LDEV_NUMBER'] =='%s'%Lun_name[i]]['RECORD_TIME'], df.loc[df['LDEV_NUMBER'] == '%s'%Lun_name[i]]['READ_IO_COUNT'])
    X = []
    Y = []
    X = list(df3.loc[df3['PORT_NAME'] == '%s' % portname[i]]['DATETIME'])
    Y = list(df3.loc[df3['PORT_NAME'] == '%s' % portname[i]]['TOTAL_MBYTES'])
    ax = plt.axes()
    ax.xaxis.set_minor_locator(dates.HourLocator(interval=4))  # every 4 hours
    ax.xaxis.set_minor_formatter(dates.DateFormatter('%H:%M'))  # hours and minutes
    ax.xaxis.set_major_locator(dates.DayLocator(interval=1))  # every day
    ax.xaxis.set_major_formatter(dates.DateFormatter('\n%d-%m-%Y'))

    for i in range(len(Y)):
        Y[i] = int(Y[i])
    plt.plot(X, Y)
    plt.ylabel('Port throughput')
    plt.xlabel('Time')
    plt.legend(portname)
plt.savefig('' + my_folder + '\port_throughput' + date + '.png')
plt.clf()
plt.close()

for i in range(len(portname)):
    # plt.plot(df.loc[df['LDEV_NUMBER'] =='%s'%Lun_name[i]]['RECORD_TIME'], df.loc[df['LDEV_NUMBER'] == '%s'%Lun_name[i]]['READ_IO_COUNT'])
    X = []
    Y = []
    X = list(df3.loc[df3['PORT_NAME'] == '%s' % portname[i]]['DATETIME'])
    Y = list(df3.loc[df3['PORT_NAME'] == '%s' % portname[i]]['READ_TOTAL_RESPONSE'])

    ax = plt.axes()
    ax.xaxis.set_minor_locator(dates.HourLocator(interval=4))  # every 4 hours
    ax.xaxis.set_minor_formatter(dates.DateFormatter('%H:%M'))  # hours and minutes
    ax.xaxis.set_major_locator(dates.DayLocator(interval=1))  # every day
    ax.xaxis.set_major_formatter(dates.DateFormatter('\n%d-%m-%Y'))

    for i in range(len(Y)):
        Y[i] = float(Y[i])
    plt.plot(X, Y)
    plt.ylabel('Processor READ_TOTAL_RESPONSE')
    plt.xlabel('Time')
    plt.legend(portname)
plt.savefig('' + my_folder + '\port_READ_RESPONSE' + date + '.png')
plt.clf()
plt.close()
for i in range(len(portname)):
    X = []
    Y = []
    # plt.plot(df.loc[df['LDEV_NUMBER'] =='%s'%Lun_name[i]]['RECORD_TIME'], df.loc[df['LDEV_NUMBER'] == '%s'%Lun_name[i]]['READ_IO_COUNT'])
    X = list(df3.loc[df3['PORT_NAME'] == '%s' % portname[i]]['DATETIME'])
    Y = list(df3.loc[df3['PORT_NAME'] == '%s' % portname[i]]['WRITE_TOTAL_RESPONSE'])

    ax = plt.axes()
    ax.xaxis.set_minor_locator(dates.HourLocator(interval=4))  # every 4 hours
    ax.xaxis.set_minor_formatter(dates.DateFormatter('%H:%M'))  # hours and minutes
    ax.xaxis.set_major_locator(dates.DayLocator(interval=1))  # every day
    ax.xaxis.set_major_formatter(dates.DateFormatter('\n%d-%m-%Y'))

    for i in range(len(Y)):
        Y[i] = float(Y[i])
    plt.plot(X, Y)
    plt.ylabel('Processor WRITE_TOTAL_RESPONSE')
    plt.xlabel('Time')
    plt.legend(portname)
plt.savefig('' + my_folder + '\port_WRITE_RESPONSE' + date + '.png')
plt.clf()
plt.close()
for i in range(len(array_name)):
    params2 = (
        ('agentType', 'RAID'),
        ('agentInstanceName', array_name[i]),
        ('fields', 'DATETIME\x1FADAPTOR_ID\x1FPROCESSOR_ID\x1FPROCESSOR_BUSY_RATE'),
        ('pfmHostName', array_instancename[i]),
        ('startTime', startTime),
        ('endTime', endTime),
    )
response2 = requests.get('http://161.89.194.57:24221/TuningAgent/v1/objects/PI_PRCS', params=params2, verify=False)
df4 = pd.read_csv(io.StringIO(response2.content.decode('ascii')))
df5 = df4.drop(df4.index[0])
df4.to_csv(''+array_instancename[i]+'-Processorbusyrate.csv')
df5['DATETIME'] = pd.to_datetime(df5['DATETIME'])
adaptorid = list(dict.fromkeys(df5['ADAPTOR_ID']))
for i in range (len(adaptorid)):
    X = []
    Y = []
    X = list(df5.loc[(df5['ADAPTOR_ID'] == '%s'%adaptorid[i]) & (df5['PROCESSOR_ID']=='_Total')]['DATETIME'])
    Y = list(df5.loc[(df5['ADAPTOR_ID'] == '%s'%adaptorid[i]) & (df5['PROCESSOR_ID']== '_Total')]['PROCESSOR_BUSY_RATE'])
    ax = plt.axes()
    ax.xaxis.set_minor_locator(dates.HourLocator(interval=4))  # every 4 hours
    ax.xaxis.set_minor_formatter(dates.DateFormatter('%H:%M'))  # hours and minutes
    ax.xaxis.set_major_locator(dates.DayLocator(interval=1))  # every day
    ax.xaxis.set_major_formatter(dates.DateFormatter('\n%d-%m-%Y'))

    for i in range(len(Y)):
        Y[i] = float(Y[i])
    plt.plot(X, Y)
    plt.ylabel('processor')
    plt.xlabel('Time')
    plt.legend(adaptorid)
plt.savefig('' + my_folder + '\processor' + date + '.png')
plt.clf()
plt.close()
for i in range(len(array_name)):
    params3 = (
        ('agentType', 'RAID'),
        ('agentInstanceName', array_name[i]),
        ('fields', 'DATETIME\x1FCLPR_NUMBER\x1FCACHE_WRITE_PENDING_RATE'),
        ('pfmHostName', array_instancename[i]),
        ('startTime', startTime),
        ('endTime', endTime),
    )

response3 = requests.get('http://161.89.194.57:24221/TuningAgent/v1/objects/PI_CLPS', params=params3, verify=False)
df6 = pd.read_csv(io.StringIO(response3.content.decode('ascii')))


df7 = df6.drop(df6.index[0])
df6.to_csv(''+array_instancename[i]+'-CWP.csv')
clpr = list(dict.fromkeys(df7['CLPR_NUMBER']))
df7['DATETIME'] = pd.to_datetime(df7['DATETIME'])

for i in range(len(clpr)):
    X = []
    Y = []
    # plt.plot(df.loc[df['LDEV_NUMBER'] =='%s'%Lun_name[i]]['RECORD_TIME'], df.loc[df['LDEV_NUMBER'] == '%s'%Lun_name[i]]['READ_IO_COUNT'])
    X = list(df7.loc[df7['CLPR_NUMBER'] == '%s' % clpr[i]]['DATETIME'])
    Y = list(df7.loc[df7['CLPR_NUMBER'] == '%s' % clpr[i]]['CACHE_WRITE_PENDING_RATE'])

    ax = plt.axes()
    ax.xaxis.set_minor_locator(dates.HourLocator(interval=4))  # every 4 hours
    ax.xaxis.set_minor_formatter(dates.DateFormatter('%H:%M'))  # hours and minutes
    ax.xaxis.set_major_locator(dates.DayLocator(interval=1))  # every day
    ax.xaxis.set_major_formatter(dates.DateFormatter('\n%d-%m-%Y'))

    for i in range(len(Y)):
        Y[i] = float(Y[i])
    plt.plot(X, Y)
    plt.ylabel('CWP')
    plt.xlabel('Time')
    plt.legend(clpr)

plt.savefig('' + my_folder + '\cwp' + date + '.png')
plt.clf()
plt.close()
