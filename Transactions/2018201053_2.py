import sys
from collections import OrderedDict
filename=sys.argv[1]
f = open(filename, "r")
output=open("./output.txt","w+")

lines=list(f)

lines[0]=lines[0][0:-1]
st=lines[0].split(" ")
states=OrderedDict()  #of variables in the disk
i=0
while i<len(st):
	states[st[i]]=st[i+1]
	i+=2


new_lines=[]
for i in lines:
	if(i!='\n'):
		new_lines.append(i[0:-1])



new_lines=new_lines[1:]

all_trans=[]

for i in new_lines:
	if "START" in i:
		splits=i.split(" ")
		if len(splits)==2:
			trans=splits[1].split(">")
			all_trans.append(trans[0])


commit_flag=OrderedDict()
for i in all_trans:
	commit_flag[i]=0

for i in range(len(new_lines)-1,-1,-1):
	string=new_lines[i]
	if "COMMIT" in string:
		splits=string.split(" ")
		trans=splits[1].split(">")
		commit_flag[trans[0]]=1
	else:
		splits=string.split(" ")
		if len(splits)==3:
			trans=splits[0].split("<")
			t=trans[1][:-1]
			var=splits[1].strip()
			var=var.strip()
			var=var[:-1]
			value=splits[2].strip()
			value=value.split(">")
			value=value[0]
			if commit_flag[t]==0:
				states[var]=value
				print var,"=",value

line=""
for i in sorted(states.keys()):
	line+=i+' '+str(states[i])+' '
line=line[:-1]
line+='\n'
output.write(line)

