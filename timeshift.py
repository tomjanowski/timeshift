#!/usr/bin/python3
import datetime,zoneinfo,os,pwd,grp,sys
SHIFT=0
#try: 
for i in sys.argv:
  try:
    SHIFT=float(i)
    break
  except:
    continue
#except Exception as x:
#  print(x)
#  raise x
#  SHIFT=83509910
#  SHIFT=0

lcolor=True
for i in sys.argv:
  if i=="--no-color": lcolor=False

print(f'Color: {lcolor}, SHIFT: {SHIFT}')

x=datetime.datetime.strptime("02/13/2022 02:57:13","%m/%d/%Y %H:%M:%S")
# make the object have the same numerical date/time, but with interpretation of local timezone
y=x.astimezone()
# Now we can convert to to UTC
z=y.astimezone(zoneinfo.ZoneInfo("UTC"))
# Make addition in UTC and recalculate to the local timezone
w=(z+datetime.timedelta(seconds=SHIFT)).astimezone()
# please note that direct addition of timedelta to y produces wrong result, it seems the 
# addition does not take DST into account, but it does when converting from/to UTC, while
# UTC+timedelta does not need any awarness of DST.
#
def mode_str(mode):
  string=list('----------')
  bit=1
  for i,j in enumerate(('x','w','r')*3):
    if bit&mode: string[-i-1]=j
    bit<<=1
#   print(f'{bit:b} {j}')
  if bit&mode:
    if 1&mode: string[-1]='t'
    else:      string[-1]='T'
  bit<<=1
  if bit&mode:
    if 1&mode: string[-4]='s'
    else:      string[-4]='S'
  bit<<=1
  if bit&mode:
    if 1&mode: string[-7]='s'
    else:      string[-7]='S'
  if (mode&0o170000)&0o140000==0o140000:
    string[0]='s'
    return "".join(string)
  if (mode&0o170000)&0o120000==0o120000:
    string[0]='l'
    return "".join(string)
  if (mode&0o170000)&0o60000==0o60000:
    string[0]='b'
    return "".join(string)
  if (mode&0o170000)&0o40000==0o40000:
    string[0]='d'
    return "".join(string)
  if (mode&0o170000)&0o20000==0o20000:
    string[0]='c'
    return "".join(string)
  if (mode&0o170000)&0o10000==0o10000:
    string[0]='p'
  return "".join(string)
filelist=[]
maxsize=0
maxuser=0
maxgroup=0
for i in os.listdir("."):
  try:
    j=os.stat(i,follow_symlinks=False)
  except FileNotFoundError:
    print("=================== ",i)
    j=os.stat(i,follow_symlinks=False)
  stamp=datetime.datetime.fromtimestamp(int(j.st_mtime))
  stamp=stamp.astimezone()
  stamp=stamp.astimezone(zoneinfo.ZoneInfo("UTC"))
  stamp=stamp+datetime.timedelta(seconds=SHIFT)
  stamp=stamp.astimezone()
  stamp=stamp.strftime("%Y-%m-%d %H:%M:%S")
  user=pwd.getpwuid( j.st_uid).pw_name
  group=grp.getgrgid(j.st_gid).gr_name
# print(f'{mode_str(j.st_mode)} {j.st_nlink:3} {user:10} {group:10} {j.st_size:11} {stamp} {i}')
  if (x:=len(str(j.st_size)))>maxsize: maxsize=x
  if (x:=len(user))>maxuser: maxuser=x
  if (x:=len(group))>maxgroup: maxgroup=x
  filelist.append((mode_str(j.st_mode),\
                   j.st_nlink,\
                   user,\
                   group,\
                   j.st_size,\
                   stamp,\
                   j.st_mtime,\
                   i))
for i in sorted(filelist,key=lambda x: x[6]):
  color=""
  reset=""
  if lcolor:
    if i[0][0]=="d": 
      color='\x1b[01;34m'
      reset='\x1b[0m'
    elif i[0][0]=="l": 
      color='\x1b[31;01m'
      reset='\x1b[0m'
    elif i[0][0]=="s": 
      color='\x1b[35;01m'
      reset='\x1b[0m'
    elif i[0][0]=="p": 
      color='\x1b[33m'
      reset='\x1b[0m'
    elif i[0][3]=="x" or i[0][6]=="x" or i[0][9]=="x":
      color='\x1b[01;32m'
      reset='\x1b[0m'
  print(f'{i[0]} {i[1]:3} {i[2]:{maxuser}} {i[3]:{maxgroup}} {i[4]:{maxsize}} {i[5]} ',end="")
  print(color,end="")
  print(f'{i[7]}',end="")
  print(reset)
