import sys
from collections import OrderedDict
filename=sys.argv[1]
f = open(filename, "r")
output=open("./output.txt","w+")
x=sys.argv[2]
lines=list(f)


lines[0]=lines[0][0:-1]
st=lines[0].split(" ")
states=OrderedDict()  #of variables in the disk
i=0
while i<len(st):
	states[st[i]]=st[i+1]
	i+=2

main_memory=OrderedDict()

new_lines=[]
for i in lines:
	if(i!='\n'):
		new_lines.append(i[0:-1])



new_lines=new_lines[1:]

transactions=OrderedDict()
i=0
while i<len(new_lines):
	l=new_lines[i].split(" ")
	transactions[l[0]]=[]
	for j in range(int(l[1])):
		transactions[l[0]].append(new_lines[i+1+j])
	
	i+=int(l[1])+1


all_trans=transactions.keys()

def start_transaction(t):
	output.write("<START "+t+">\n")
	line=""
	for i in sorted(main_memory.keys()):
		line+=i+' '+str(main_memory[i])+' '
	line=line[:-1]
	line+='\n'
	output.write(line)
	line=""
	for i in sorted(states.keys()):
		line+=i+' '+states[i]+' '
	line=line[:-1]
	line+='\n'
	output.write(line)

def commit_transaction(t):
	output.write("<COMMIT "+t+">\n")
	line=""
	for i in sorted(main_memory.keys()):
		line+=i+' '+str(main_memory[i])+' '
	line=line[:-1]
	line+='\n'
	output.write(line)
	line=""
	for i in sorted(states.keys()):
		line+=i+' '+str(states[i])+' '
	line=line[:-1]
	line+='\n'
	output.write(line)

transaction_variables={}
commit_flag=OrderedDict()
for i in all_trans:
	# transaction_variables[i]={}
	commit_flag[i]=0

def process_action(t,string):
	# print string
	if "READ" in string:
		splits=string.split('(')
		var=splits[1].split(',')
		trans_var=var[1].split(')')
		# dict_temp=transaction_variables[t]
		var[0]=var[0].strip()
		trans_var[0]=trans_var[0].strip()
		# print var[0]

		if var[0] not in main_memory.keys():
			transaction_variables[trans_var[0]]=states[var[0]]
			main_memory[var[0]]=states[var[0]]
		else:
			transaction_variables[trans_var[0]]=main_memory[var[0]]
		# print dict_temp
		# transaction_variables[t]=dict_temp
		# print transaction_variables
		

	elif "WRITE" in string:
		splits=string.split('(')
		var=splits[1].split(',')
		trans_var=var[1].split(')')
		var[0]=var[0].strip()
		trans_var[0]=trans_var[0].strip()
		
		if var[0] not in main_memory.keys():
			line="<"+t+", "+var[0]+', '+str(states[var[0]])+'>\n'
		else:
			line="<"+t+", "+var[0]+', '+str(main_memory[var[0]])+'>\n'
		output.write(line)
		main_memory[var[0]]=transaction_variables[trans_var[0]]
		line=""
		for i in sorted(main_memory.keys()):
			line+=i+' '+str(main_memory[i])+' '
		line=line[:-1]
		line+='\n'
		output.write(line)
		line=""
		for i in sorted(states.keys()):
			line+=i+' '+str(states[i])+' '
		line=line[:-1]
		line+='\n'
		output.write(line)

		
	elif "OUTPUT" in string:
		var=string.split('(')
		var[1]=var[1].strip()
		temp_var=var[1].split(')')
		var=temp_var[0]
		# print var
		states[var]=main_memory[var]

	elif "=" in string:
		splits=string.split(' := ')
		if '+' in splits[1]:
			operate=splits[1].split('+')
			operate[1]=operate[1].strip()
			if operate[1] in transaction_variables.keys():
				transaction_variables[splits[0]]=int(transaction_variables[operate[0]])+int(transaction_variables[operate[1]])
			else:
				# print transaction_variables[t][operate[0]]
				# print operate[1]
				transaction_variables[splits[0]]=int(transaction_variables[operate[0]])+int(operate[1])
		if '-' in splits[1]:
			operate=splits[1].split('-')
			operate[1]=operate[1].strip()
			if operate[1] in transaction_variables.keys():
				transaction_variables[splits[0]]=int(transaction_variables[operate[0]])-int(transaction_variables[operate[1]])
			else:
				transaction_variables[splits[0]]=int(transaction_variables[operate[0]])-int(operate[1])
		if '*' in splits[1]:
			operate=splits[1].split('*')
			operate[1]=operate[1].strip()
			if operate[1] in transaction_variables.keys():
				transaction_variables[splits[0]]=int(transaction_variables[operate[0]])*int(transaction_variables[operate[1]])
			else:
				transaction_variables[splits[0]]=int(transaction_variables[operate[0]])*int(operate[1])
		if '/' in splits[1]:
			operate=splits[1].split('/')
			operate[1]=operate[1].strip()
			if operate[1] in transaction_variables.keys():
				transaction_variables[splits[0]]=int(transaction_variables[operate[0]])/int(transaction_variables[operate[1]])
			else:
				transaction_variables[splits[0]]=int(transaction_variables[operate[0]])/int(operate[1])


def roundrobin(keys,dict,timeslice):
	list_lengths=[]
	times=0
	for i in keys:
		list_lengths.append(len(dict[i]))
		times+=len(dict[i])
	# print list_lengths

	while times!=0:
		# print times
		for i in keys:
			
			if list_lengths[keys.index(i)]==len(dict[i]):
				start_transaction(i)

			x=timeslice
			while x>0:
				
				if(list_lengths[keys.index(i)]!=0):
					process_action(i,dict[i][len(dict[i])-list_lengths[keys.index(i)]])
					list_lengths[keys.index(i)]-=1
					if list_lengths[keys.index(i)]==0:
						if commit_flag[i]==0:
							commit_flag[i]=1
							commit_transaction(i)
				else:
					if commit_flag[i]==0:
						commit_flag[i]=1
						commit_transaction(i)

				x-=1
		times-=1


roundrobin(all_trans,transactions,int(x))