import csv
import sys
import os
def main():
	allTableInfo={}
	readMetaData(allTableInfo)
	processQuery(str(sys.argv[1]),allTableInfo)

def readMetaData(allTableInfo):
	flag=False
	file=open('./metadata.txt','r')
	for row in file:
		if row.strip() == "<begin_table>":
			flag=True
		elif flag==True:
			flag=False
			name=row.strip()
			allTableInfo[name]=[]
		elif row.strip() != "<end_table>":
			allTableInfo[name].append(row.strip())

def readcsvfile(filename,resultlist):
	if os.path.exists(filename)==False:
		sys.exit("Table Not Found!")
	with open(filename,'rb') as file:
		read=csv.reader(file)
		for line in read:
			# print line
			resultlist.append(line)

def removeduplicates(fileData): #removing duplicates from list of lists
	result=[]
	for i in fileData:
		if i not in result:
			result.append(i)
	return result#[x for x in result if x!=[]] 

def selectdistinct(words,allTableInfo):
	if words[2]=="*":
		if words[3].lower()!="from":
			sys.exit("Invalid Syntax!")
		else:
			fileData=[]
			for i in allTableInfo[words[4]]:
				s=words[4]+"."+i
				sys.stdout.write(s+",")
				# print s+",",
			sys.stdout.write("\b")
			print ' '
			readcsvfile(words[4]+'.csv',fileData)
			fileData=removeduplicates(fileData)
			return fileData#list of lists

	else:
		columns=[]
		ind=0
		for x in range(2,len(words)+1):
			if words[x].lower()=="from":
				ind=x
				break
			else:
				temp=words[x].split(",")
				for i in temp:
					if i=="," or i=="":
						continue
					else:
						columns.append(i)
		for i in columns:
			s=words[ind+1]+"."+i
			sys.stdout.write(s+",")
			# print s+",",
		sys.stdout.write("\b")
		print ' '
		fileData=[]
		readcsvfile(words[ind+1]+'.csv',fileData)
		index=[]
		for i in columns:
			index.append(allTableInfo[words[ind+1]].index(i))
		result=[]
		for i in fileData:
			temporary=[]
			for j in index:
				temporary.append(i[j])
			result.append(temporary)
		result=removeduplicates(result)
		return result

def join(cNames,tNames,dictin):
	tNames.reverse()
	# print "here in join"
	fileData = []
	list1 = []

	readcsvfile(tNames[0] + '.csv',list1)

	list2 = []
	readcsvfile(tNames[1] + '.csv',list2)

	
	for i1 in list1:
		for i2 in list2:
			fileData.append(i2 + i1)

	
	dictin["sample"] = []

	#putting sample in dictionary to temporarily represent the joined table data
	#for first table 
	for q in dictin[tNames[1]]:
		dictin["sample"].append(tNames[1] + '.' + q)

	#for 0th table
	for q in dictin[tNames[0]]:
		dictin["sample"].append(tNames[0] + '.' + q)

	#finally making a test entry in dictionary
	dictin["test"] = dictin[tNames[1]] + dictin[tNames[0]]
	
	#removing the entries
	tNames.remove(tNames[0])

	tNames.remove(tNames[0])

	tNames.insert(0,"sample")

	if len(cNames) == 1:
		if cNames[0] == '*':
			cNames = dictin[tNames[0]]

	output =[]

	for d in fileData:
		l=[]
		for col in cNames:
			if '.' in col:
				# print "here  ",
				l.append(d[dictin[tNames[0]].index(col)])
			else:
				# print "there  ",
				l.append(d[dictin["test"].index(col)])
		# print
		output.append(l)
	return output

# def handle(a,cNames,tNames,dictionary):
def handle(l1, l2):
	# print l1
	# print l2
	ans = []
	for i in l1:
		l = []
		for j in i:
			l.append(j)
		for h in l2:
			p = []
			for x in l:
				p.append(x)
			for k in h:
				p.append(k)
			ans.append(p)
	return ans
def temp2(a,b,c,d,result,symbol1,symbol2,operation):
	# print "in temp2"
	# print operation
	if operation=='and':
		# print "and"
		# print a
		# print b
		# print c
		# print d
		# print
		# print result
		if symbol1=='=' and symbol2=='=':
			output=[]
			for i in result:
				# for j in i:
				# print i[a]
				# print symbol1
				# print i[b]
				# print
				# print i[c]
				# print symbol2
				# print i[d]
				# print 
				# print
				if i[a]==i[b] and i[c]==i[d]:
					output.append(i)
			return output
		if symbol1=='=' and symbol2=='>':
			output=[]
			for i in result:
				# for j in i:
				if i[a]==i[b] and i[c]>i[d]:
					output.append(i)
			return output
		if symbol1=='=' and symbol2=='<':
			output=[]
			for i in result:
				# for j in i:
				if i[a]==i[b] and i[c]<i[d]:
					output.append(i)
			return output
		if symbol1=='=' and symbol2=='>=':
			output=[]
			for i in result:
				# for j in i:
				if i[a]==i[b] and i[c]>=i[d]:
					output.append(i)
			return output
		if symbol1=='=' and symbol2=='<=':
			output=[]
			for i in result:
				# for j in i:
				if i[a]==i[b] and i[c]<=i[d]:
					output.append(i)
			return output

		if symbol1=='>' and symbol2=='=':
			output=[]
			for i in result:
				# for j in i:
				if i[a]>i[b] and i[c]==i[d]:
					output.append(i)
			return output
		if symbol1=='>' and symbol2=='>':
			output=[]
			for i in result:
				# for j in i:
				if i[a]>i[b] and i[c]>i[d]:
					output.append(i)
			return output
		if symbol1=='>' and symbol2=='<':
			output=[]
			for i in result:
				# for j in i:
				if i[a]>i[b] and i[c]<i[d]:
					output.append(i)
			return output
		if symbol1=='>' and symbol2=='>=':
			output=[]
			for i in result:
				# for j in i:
				if i[a]>i[b] and i[c]>=i[d]:
					output.append(i)
			return output
		if symbol1=='>' and symbol2=='<=':
			output=[]
			for i in result:
				# for j in i:
				if i[a]>i[b] and i[c]<=i[d]:
					output.append(i)
			return output

		if symbol1=='<' and symbol2=='=':
			output=[]
			for i in result:
				# for j in i:
				if i[a]<i[b] and i[c]==i[d]:
					output.append(i)
			return output
		if symbol1=='<' and symbol2=='>':
			output=[]
			for i in result:
				# for j in i:
				if i[a]<i[b] and i[c]>i[d]:
					output.append(i)
			return output
		if symbol1=='<' and symbol2=='<':
			output=[]
			for i in result:
				# for j in i:
				if i[a]<i[b] and i[c]<i[d]:
					output.append(i)
			return output
		if symbol1=='<' and symbol2=='>=':
			output=[]
			for i in result:
				# for j in i:
				if i[a]<i[b] and i[c]>=i[d]:
					output.append(i)
			return output
		if symbol1=='<' and symbol2=='<=':
			output=[]
			for i in result:
				# for j in i:
				if i[a]<i[b] and i[c]<=i[d]:
					output.append(i)
			return output

		if symbol1=='>=' and symbol2=='=':
			output=[]
			for i in result:
				# for j in i:
				if i[a]>=i[b] and i[c]==i[d]:
					output.append(i)
			return output
		if symbol1=='>=' and symbol2=='>':
			output=[]
			for i in result:
				# for j in i:
				if i[a]>=i[b] and i[c]>i[d]:
					output.append(i)
			return output
		if symbol1=='>=' and symbol2=='<':
			output=[]
			for i in result:
				# for j in i:
				if i[a]>=i[b] and i[c]<i[d]:
					output.append(i)
			return output
		if symbol1=='>=' and symbol2=='>=':
			output=[]
			for i in result:
				# for j in i:
				if i[a]>=i[b] and i[c]>=i[d]:
					output.append(i)
			return output
		if symbol1=='>=' and symbol2=='<=':
			output=[]
			for i in result:
				# for j in i:
				if i[a]>=i[b] and i[c]<=i[d]:
					output.append(i)
			return output

		if symbol1=='<=' and symbol2=='=':
			output=[]
			for i in result:
				# for j in i:
				if i[a]<=i[b] and i[c]==i[d]:
					output.append(i)
			return output
		if symbol1=='<=' and symbol2=='>':
			output=[]
			for i in result:
				# for j in i:
				if i[a]<=i[b] and i[c]>i[d]:
					output.append(i)
			return output
		if symbol1=='<=' and symbol2=='<':
			output=[]
			for i in result:
				# for j in i:
				if i[a]<=i[b] and i[c]<i[d]:
					output.append(i)
			return output
		if symbol1=='<=' and symbol2=='>=':
			output=[]
			for i in result:
				# for j in i:
				if i[a]<=i[b] and i[c]>=i[d]:
					output.append(i)
			return output
		if symbol1=='<=' and symbol2=='<=':
			output=[]
			for i in result:
				# for j in i:
				if i[a]<=i[b] and i[c]<=i[d]:
					output.append(i)
			return output

	if operation=='or':
		# print "or"
		if symbol1=='=' or symbol2=='=':
			output=[]
			for i in result:
				# for j in i:
				if i[a]==i[b] or i[c]==i[d]:
					output.append(i)
			return output
		if symbol1=='=' or symbol2=='>':
			output=[]
			for i in result:
				# for j in i:
				if i[a]==i[b] or i[c]>i[d]:
					output.append(i)
			return output
		if symbol1=='=' or symbol2=='<':
			output=[]
			for i in result:
				# for j in i:
				if i[a]==i[b] or i[c]<i[d]:
					output.append(i)
			return output
		if symbol1=='=' or symbol2=='>=':
			output=[]
			for i in result:
				# for j in i:
				if i[a]==i[b] or i[c]>=i[d]:
					output.append(i)
			return output
		if symbol1=='=' or symbol2=='<=':
			output=[]
			for i in result:
				# for j in i:
				if i[a]==i[b] or i[c]<=i[d]:
					output.append(i)
			return output

		if symbol1=='>' or symbol2=='=':
			output=[]
			for i in result:
				# for j in i:
				if i[a]>i[b] or i[c]==i[d]:
					output.append(i)
			return output
		if symbol1=='>' or symbol2=='>':
			output=[]
			for i in result:
				# for j in i:
				if i[a]>i[b] or i[c]>i[d]:
					output.append(i)
			return output
		if symbol1=='>' or symbol2=='<':
			output=[]
			for i in result:
				# for j in i:
				if i[a]>i[b] or i[c]<i[d]:
					output.append(i)
			return output
		if symbol1=='>' or symbol2=='>=':
			output=[]
			for i in result:
				# for j in i:
				if i[a]>i[b] or i[c]>=i[d]:
					output.append(i)
			return output
		if symbol1=='>' or symbol2=='<=':
			output=[]
			for i in result:
				# for j in i:
				if i[a]>i[b] or i[c]<=i[d]:
					output.append(i)
			return output

		if symbol1=='<' or symbol2=='=':
			output=[]
			for i in result:
				# for j in i:
				if i[a]<i[b] or i[c]==i[d]:
					output.append(i)
			return output
		if symbol1=='<' or symbol2=='>':
			output=[]
			for i in result:
				# for j in i:
				if i[a]<i[b] or i[c]>i[d]:
					output.append(i)
			return output
		if symbol1=='<' or symbol2=='<':
			output=[]
			for i in result:
				# for j in i:
				if i[a]<i[b] or i[c]<i[d]:
					output.append(i)
			return output
		if symbol1=='<' or symbol2=='>=':
			output=[]
			for i in result:
				# for j in i:
				if i[a]<i[b] or i[c]>=i[d]:
					output.append(i)
			return output
		if symbol1=='<' or symbol2=='<=':
			output=[]
			for i in result:
				# for j in i:
				if i[a]<i[b] or i[c]<=i[d]:
					output.append(i)
			return output

		if symbol1=='>=' or symbol2=='=':
			output=[]
			for i in result:
				# for j in i:
				if i[a]>=i[b] or i[c]==i[d]:
					output.append(i)
			return output
		if symbol1=='>=' or symbol2=='>':
			output=[]
			for i in result:
				# for j in i:
				if i[a]>=i[b] or i[c]>i[d]:
					output.append(i)
			return output
		if symbol1=='>=' or symbol2=='<':
			output=[]
			for i in result:
				# for j in i:
				if i[a]>=i[b] or i[c]<i[d]:
					output.append(i)
			return output
		if symbol1=='>=' or symbol2=='>=':
			output=[]
			for i in result:
				# for j in i:
				if i[a]>=i[b] or i[c]>=i[d]:
					output.append(i)
			return output
		if symbol1=='>=' or symbol2=='<=':
			output=[]
			for i in result:
				# for j in i:
				if i[a]>=i[b] or i[c]<=i[d]:
					output.append(i)
			return output

		if symbol1=='<=' or symbol2=='=':
			output=[]
			for i in result:
				# for j in i:
				if i[a]<=i[b] or i[c]==i[d]:
					output.append(i)
			return output
		if symbol1=='<=' or symbol2=='>':
			output=[]
			for i in result:
				# for j in i:
				if i[a]<=i[b] or i[c]>i[d]:
					output.append(i)
			return output
		if symbol1=='<=' or symbol2=='<':
			output=[]
			for i in result:
				# for j in i:
				if i[a]<=i[b] or i[c]<i[d]:
					output.append(i)
			return output
		if symbol1=='<=' or symbol2=='>=':
			output=[]
			for i in result:
				# for j in i:
				if i[a]<=i[b] or i[c]>=i[d]:
					output.append(i)
			return output
		if symbol1=='<=' or symbol2=='<=':
			output=[]
			for i in result:
				# for j in i:
				if i[a]<=i[b] or i[c]<=i[d]:
					output.append(i)
			return output	
	else:
		sys.exit("Only 'and' and 'or' can be used!")

def temp(a,b,result,symbol):
	if symbol=='=':
		output=[]
		for i in result:
			# for j in i:
			if i[a]==i[b]:
				output.append(i)
		return output
	if symbol=='>':
		output=[]
		for i in result:
			# for j in i:
			if i[a]>i[b]:
				output.append(i)
		return output
	if symbol=="<":
		output=[]
		for i in result:
			# for j in i:
			if i[a]<i[b]:
				output.append(i)
		return output
	if symbol==">=":
		output=[]
		for i in result:
			# for j in i:
			if i[a]>=i[b]:
				output.append(i)
		return output
	if symbol=="<=":
		output=[]
		for i in result:
			# for j in i:
			if i[a]<=i[b]:
				output.append(i)
		return output


def evaluateJoinWhere(a,columnNames,tableNames,dictionary,result):
	# print "evaluate where join"
	# print a
	if len(a) < 3:
		sys.exit("Invalid Syntax!")
	# print columnNames
	if columnNames[0].split(".")==1:	
		if a[3]=='and':
			output=[]
			for a1 in range(0,len(result)):
				if a[1]=='=' and a[5]=='=':
					if int(result[a1][columnNames.index(a[0])])==int(a[2]) and int(result[a1][columnNames.index(a[4])])==int(a[6]):
						output.append(result[a1])
				if a[1]=='=' and a[5]=='>':
					if int(result[a1][columnNames.index(a[0])])==int(a[2]) and int(result[a1][columnNames.index(a[4])])>int(a[6]):
						output.append(result[a1])
				if a[1]=='=' and a[5]=='<':
					if int(result[a1][columnNames.index(a[0])])==int(a[2]) and int(result[a1][columnNames.index(a[4])])<int(a[6]):
						output.append(result[a1])
				if a[1]=='=' and a[5]=='>=':
					if int(result[a1][columnNames.index(a[0])])==int(a[2]) and int(result[a1][columnNames.index(a[4])])>=int(a[6]):
						output.append(result[a1])
				if a[1]=='=' and a[5]=='<=':
					if int(result[a1][columnNames.index(a[0])])==int(a[2]) and int(result[a1][columnNames.index(a[4])])<=int(a[6]):
						output.append(result[a1])

				if a[1]=='>' and a[5]=='=':
					if int(result[a1][columnNames.index(a[0])])>int(a[2]) and int(result[a1][columnNames.index(a[4])])==int(a[6]):
						output.append(result[a1])
				if a[1]=='>' and a[5]=='>':
					if int(result[a1][columnNames.index(a[0])])>int(a[2]) and int(result[a1][columnNames.index(a[4])])>int(a[6]):
						output.append(result[a1])
				if a[1]=='>' and a[5]=='<':
					if int(result[a1][columnNames.index(a[0])])>int(a[2]) and int(result[a1][columnNames.index(a[4])])<int(a[6]):
						output.append(result[a1])
				if a[1]=='>' and a[5]=='>=':
					if int(result[a1][columnNames.index(a[0])])>int(a[2]) and int(result[a1][columnNames.index(a[4])])>=int(a[6]):
						output.append(result[a1])
				if a[1]=='>' and a[5]=='<=':
					if int(result[a1][columnNames.index(a[0])])>int(a[2]) and int(result[a1][columnNames.index(a[4])])<=int(a[6]):
						output.append(result[a1])

				if a[1]=='<' and a[5]=='=':
					if int(result[a1][columnNames.index(a[0])])<int(a[2]) and int(result[a1][columnNames.index(a[4])])==int(a[6]):
						output.append(result[a1])
				if a[1]=='<' and a[5]=='>':
					if int(result[a1][columnNames.index(a[0])])<int(a[2]) and int(result[a1][columnNames.index(a[4])])>int(a[6]):
						output.append(result[a1])
				if a[1]=='<' and a[5]=='<':
					if int(result[a1][columnNames.index(a[0])])<int(a[2]) and int(result[a1][columnNames.index(a[4])])<int(a[6]):
						output.append(result[a1])
				if a[1]=='<' and a[5]=='>=':
					if int(result[a1][columnNames.index(a[0])])<int(a[2]) and int(result[a1][columnNames.index(a[4])])>=int(a[6]):
						output.append(result[a1])
				if a[1]=='<' and a[5]=='<=':
					if int(result[a1][columnNames.index(a[0])])<int(a[2]) and int(result[a1][columnNames.index(a[4])])<=int(a[6]):
						output.append(result[a1])

				if a[1]=='>=' and a[5]=='=':
					if int(result[a1][columnNames.index(a[0])])>=int(a[2]) and int(result[a1][columnNames.index(a[4])])==int(a[6]):
						output.append(result[a1])
				if a[1]=='>=' and a[5]=='>':
					if int(result[a1][columnNames.index(a[0])])>=int(a[2]) and int(result[a1][columnNames.index(a[4])])>int(a[6]):
						output.append(result[a1])
				if a[1]=='>=' and a[5]=='<':
					if int(result[a1][columnNames.index(a[0])])>=int(a[2]) and int(result[a1][columnNames.index(a[4])])<int(a[6]):
						output.append(result[a1])
				if a[1]=='>=' and a[5]=='>=':
					if int(result[a1][columnNames.index(a[0])])>=int(a[2]) and int(result[a1][columnNames.index(a[4])])>=int(a[6]):
						output.append(result[a1])
				if a[1]=='>=' and a[5]=='<=':
					if int(result[a1][columnNames.index(a[0])])>=int(a[2]) and int(result[a1][columnNames.index(a[4])])<=int(a[6]):
						output.append(result[a1])

				if a[1]=='<=' and a[5]=='=':
					if int(result[a1][columnNames.index(a[0])])<=int(a[2]) and int(result[a1][columnNames.index(a[4])])==int(a[6]):
						output.append(result[a1])
				if a[1]=='<=' and a[5]=='>':
					if int(result[a1][columnNames.index(a[0])])<=int(a[2]) and int(result[a1][columnNames.index(a[4])])>int(a[6]):
						output.append(result[a1])
				if a[1]=='<=' and a[5]=='<':
					if int(result[a1][columnNames.index(a[0])])<=int(a[2]) and int(result[a1][columnNames.index(a[4])])<int(a[6]):
						output.append(result[a1])
				if a[1]=='<=' and a[5]=='>=':
					if int(result[a1][columnNames.index(a[0])])<=int(a[2]) and int(result[a1][columnNames.index(a[4])])>=int(a[6]):
						output.append(result[a1])
				if a[1]=='<=' and a[5]=='<=':
					if int(result[a1][columnNames.index(a[0])])<=int(a[2]) and int(result[a1][columnNames.index(a[4])])<=int(a[6]):
						output.append(result[a1])
			return output
		if a[3]=='or':
			output=[]
			for a1 in range(0,len(result)):
				if a[1]=='=' and a[5]=='=':
					if int(result[a1][columnNames.index(a[0])])==int(a[2]) or int(result[a1][columnNames.index(a[4])])==int(a[6]):
						output.append(result[a1])
				if a[1]=='=' and a[5]=='>':
					if int(result[a1][columnNames.index(a[0])])==int(a[2]) or int(result[a1][columnNames.index(a[4])])>int(a[6]):
						output.append(result[a1])
				if a[1]=='=' and a[5]=='<':
					if int(result[a1][columnNames.index(a[0])])==int(a[2]) or int(result[a1][columnNames.index(a[4])])<int(a[6]):
						output.append(result[a1])
				if a[1]=='=' and a[5]=='>=':
					if int(result[a1][columnNames.index(a[0])])==int(a[2]) or int(result[a1][columnNames.index(a[4])])>=int(a[6]):
						output.append(result[a1])
				if a[1]=='=' and a[5]=='<=':
					if int(result[a1][columnNames.index(a[0])])==int(a[2]) or int(result[a1][columnNames.index(a[4])])<=int(a[6]):
						output.append(result[a1])

				if a[1]=='>' and a[5]=='=':
					if int(result[a1][columnNames.index(a[0])])>int(a[2]) or int(result[a1][columnNames.index(a[4])])==int(a[6]):
						output.append(result[a1])
				if a[1]=='>' and a[5]=='>':
					if int(result[a1][columnNames.index(a[0])])>int(a[2]) or int(result[a1][columnNames.index(a[4])])>int(a[6]):
						output.append(result[a1])
				if a[1]=='>' and a[5]=='<':
					if int(result[a1][columnNames.index(a[0])])>int(a[2]) or int(result[a1][columnNames.index(a[4])])<int(a[6]):
						output.append(result[a1])
				if a[1]=='>' and a[5]=='>=':
					if int(result[a1][columnNames.index(a[0])])>int(a[2]) or int(result[a1][columnNames.index(a[4])])>=int(a[6]):
						output.append(result[a1])
				if a[1]=='>' and a[5]=='<=':
					if int(result[a1][columnNames.index(a[0])])>int(a[2]) or int(result[a1][columnNames.index(a[4])])<=int(a[6]):
						output.append(result[a1])

				if a[1]=='<' and a[5]=='=':
					if int(result[a1][columnNames.index(a[0])])<int(a[2]) or int(result[a1][columnNames.index(a[4])])==int(a[6]):
						output.append(result[a1])
				if a[1]=='<' and a[5]=='>':
					if int(result[a1][columnNames.index(a[0])])<int(a[2]) or int(result[a1][columnNames.index(a[4])])>int(a[6]):
						output.append(result[a1])
				if a[1]=='<' and a[5]=='<':
					if int(result[a1][columnNames.index(a[0])])<int(a[2]) or int(result[a1][columnNames.index(a[4])])<int(a[6]):
						output.append(result[a1])
				if a[1]=='<' and a[5]=='>=':
					if int(result[a1][columnNames.index(a[0])])<int(a[2]) or int(result[a1][columnNames.index(a[4])])>=int(a[6]):
						output.append(result[a1])
				if a[1]=='<' and a[5]=='<=':
					if int(result[a1][columnNames.index(a[0])])<int(a[2]) or int(result[a1][columnNames.index(a[4])])<=int(a[6]):
						output.append(result[a1])

				if a[1]=='>=' and a[5]=='=':
					if int(result[a1][columnNames.index(a[0])])>=int(a[2]) or int(result[a1][columnNames.index(a[4])])==int(a[6]):
						output.append(result[a1])
				if a[1]=='>=' and a[5]=='>':
					if int(result[a1][columnNames.index(a[0])])>=int(a[2]) or int(result[a1][columnNames.index(a[4])])>int(a[6]):
						output.append(result[a1])
				if a[1]=='>=' and a[5]=='<':
					if int(result[a1][columnNames.index(a[0])])>=int(a[2]) or int(result[a1][columnNames.index(a[4])])<int(a[6]):
						output.append(result[a1])
				if a[1]=='>=' and a[5]=='>=':
					if int(result[a1][columnNames.index(a[0])])>=int(a[2]) or int(result[a1][columnNames.index(a[4])])>=int(a[6]):
						output.append(result[a1])
				if a[1]=='>=' and a[5]=='<=':
					if int(result[a1][columnNames.index(a[0])])>=int(a[2]) or int(result[a1][columnNames.index(a[4])])<=int(a[6]):
						output.append(result[a1])

				if a[1]=='<=' and a[5]=='=':
					if int(result[a1][columnNames.index(a[0])])<=int(a[2]) or int(result[a1][columnNames.index(a[4])])==int(a[6]):
						output.append(result[a1])
				if a[1]=='<=' and a[5]=='>':
					if int(result[a1][columnNames.index(a[0])])<=int(a[2]) or int(result[a1][columnNames.index(a[4])])>int(a[6]):
						output.append(result[a1])
				if a[1]=='<=' and a[5]=='<':
					if int(result[a1][columnNames.index(a[0])])<=int(a[2]) or int(result[a1][columnNames.index(a[4])])<int(a[6]):
						output.append(result[a1])
				if a[1]=='<=' and a[5]=='>=':
					if int(result[a1][columnNames.index(a[0])])<=int(a[2]) or int(result[a1][columnNames.index(a[4])])>=int(a[6]):
						output.append(result[a1])
				if a[1]=='<=' and a[5]=='<=':
					if int(result[a1][columnNames.index(a[0])])<=int(a[2]) or int(result[a1][columnNames.index(a[4])])<=int(a[6]):
						output.append(result[a1])

			return output
	else:
		# print columnNames
		cNames = dictionary['sample']
		# print "cNames= "
		# print cNames
		tNames=[]
		index=[]
		ind=0
		for i in cNames:
			x=i.split(".")
			if x[0] in tNames:
				index.append(ind)
				ind+=1
				continue
			if x[0] not in tNames:
				tNames.append(x[0])
				index.append(ind)
			ind+=1
		for i in cNames:
			sys.stdout.write(i+",")
			# print i+",",
		sys.stdout.write("\b")
		print ' '
		# print index
		# print 
		# print tNames
		# print
		file1=[]
		file2=[]
		readcsvfile(tNames[0]+'.csv',file1)
		readcsvfile(tNames[1]+'.csv',file2)
		result = handle(file1,file2)
		
		if len(a)==4:
			return temp(index[0],index[1],result,a[1])
		if len(a)==8:
			return temp2(index[0],index[1],index[2],index[3],result,a[1],a[5],a[3])
		else:
			sys.exit("Only one 'and' or 'or' can be used")
		# if len(a)==
		# print tableNames
		# print dictionary
		# return [[]]
		# return handle(a,cNames,tNames,dictionary)
	return [[]]

#for join of 2 tables

def processJoinWhere(whereStr,cNames,tNames,diction):
	# print "whereStr",
	# print whereStr
	tNames.reverse()
	fileData = []
	# print columnNames
	list1 = []
	readcsvfile(tNames[0] + '.csv',list1)
	list2 = []
	# print tableNames
	
	readcsvfile(tNames[1] + '.csv',list2)

	
	for item1 in list1:
		for item2 in list2:
			fileData.append(item2 + item1)

	#creating a sample entery in dictionary
	diction["sample"] = []

	#entries wrt 1st table
	for q in diction[tNames[1]]:
		diction["sample"].append(tNames[1] + '.' + q)

	#entries wrt 0th table
	for q in diction[tNames[0]]:
		diction["sample"].append(tNames[0] + '.' + q)

	#making test entry
	diction["test"] = diction[tNames[1]] + diction[tNames[0]]

	#removing tables
	tNames.remove(tNames[0])

	tNames.remove(tNames[0])

	#inserting sample table in tNames
	tNames.insert(0,"sample")

	if len(cNames) == 1:
		if cNames[0] == '*':
			cNames = diction[tNames[0]]

	
	for i in cNames:
		sys.stdout.write(i+",")
		# print i+",",
	sys.stdout.write("\b")
	print ' '

	a = whereStr.split(" ")


	check = 0
	for data in fileData:
		string = evaluate(a,tNames,diction,data)
		for col in cNames:
			if eval(string):
				check = 1
				if '.' in col:
					sys.stdout.write(data[diction[tNames[0]].index(col)]+",")
					# print data[diction[tNames[0]].index(col)]+",",
				else:
					sys.stdout.write(data[diction["test"].index(col)]+",")
					# print data[diction["test"].index(col)]+",",
		if check == 1:
			check = 0
			sys.stdout.write("\b")
			print ' '

	del diction['sample']



#for single table
def processWhere(wStr,cNames,tNames,dictin):
	a = wStr.split(" ")

	# print a

	if(len(cNames) == 1 and cNames[0] == '*'):
		cNames = dictin[tNames[0]]

	# printHeader(columnNames,tableNames,dictionary)

	# tName1 = 
	fileData = []
	readcsvfile(tNames[0] + '.csv',fileData)

	check = 0
	for d in fileData:
		string = evaluate(a,tNames,dictin,d)
		# print tableNames
		for col in cNames:
			# print string
			if eval(string):
				check = 1
				sys.stdout.write(d[dictin[tNames[0]].index(col)]+",")
				# print d[dictin[tNames[0]].index(col)]+",",
		if check == 1:
			check = 0
			sys.stdout.write("\b")
			print ' '

def evaluate(a1,tNames1,dictin1,d1):
	string = ""
	a=a1
	tNames=tNames1
	dictin=dictin1
	d=d1
	# print a
	for i in a:
		# print i
		if i == '=':
			string += i*2
		elif i in dictin[tNames[0]] :
			string += d[dictin[tNames[0]].index(i)]
		elif i.lower() == 'and' or i.lower() == 'or':
			string += ' ' + i.lower() + ' '
		else:
			string += i
		# print string
	return string



def select(words,allTableInfo):
	# for distinct
	if words[1]=="distinct":
		return selectdistinct(words,allTableInfo)

	#for * with one or join of two tables no where clause
	if words[1]=="*" and len(words)==4:
		if words[2].lower()!="from":
			sys.exit("Invalid Syntax!")
		else:
			fileData=[]
			l=words[3].split(",")
			if len(l)!=1:
				# print l
				names=[]
				for i in l:
					if i==",":
						continue
					x=allTableInfo[i]
					for j in x:
						if j not in names:
							names.append(j)
				for a in names:
					sys.stdout.write(a+",")
					# print a+",",
				sys.stdout.write("\b")
				print ' ' 
				return join(names,l,allTableInfo)

			for i in allTableInfo[words[3]]:
				s=words[3]+"."+i
				sys.stdout.write(s+",")
				# print s+",",
			sys.stdout.write("\b")
			print ' ' 
			readcsvfile(words[3]+'.csv',fileData)
			return fileData #list of lists
	
	#for * with one or more tables with where clause
	elif words[1]=="*":
		if words[2].lower()!="from":
			sys.exit("Invalid Syntax!")
		if words[4].lower()!="where":
			sys.exit("Invalid Syntax!")
		else:
			l=words[3].split(",")
			if len(l)==2:
				# print "tables",
				# print l
				names=['*']
				# for i in l:
				# 	if i==",":
				# 		continue
				# 	x=allTableInfo[i]
				# 	for j in x:
				# 		# if j not in names:
				# 		names.append(j)
				# for a in names:
				# 	print " "+a+" ",
				# print 
				# result=join(names,l,allTableInfo)
				# print "tables again ",
				# print l
				whereStr=""
				for i1 in range(5,len(words)):
					whereStr+=str(words[i1])+" "
				processJoinWhere(whereStr,names,l,allTableInfo)
				return [[]]
				 
			elif len(l)==1:
				names=[]
				for i in l:
					if i==",":
						continue
					x=allTableInfo[i]
					for j in x:
						if "." in j:
							t=j.split(".")
							if t not in names:
								names.append(t)
						else:
							if j not in names:
								names.append(j)
				for a in names:
					sys.stdout.write(a+",")
					# print a+",",
				sys.stdout.write("\b")
				print ' '
				file1=[]
				file2=[]
				readcsvfile(l[0]+'.csv',file1)
				# print "names",
				# print names
				whereStr=""
				for i1 in range(5,len(words)):
					# print words[i1].split(".")
					if len(words[i1].split("."))>1:
						# print "entered for= ",words[i1], "len= ", len(words[i1].split("."))
						whereStr+=str(words[i1].split(".")[1])+" "
					else:
						whereStr+=str(words[i1])+" "
					# elif words[i1]=='=' or words[i1]=='>' or words[i1]=='<' or words[i1]=='>=' or words[i1]=='<=':
					# 	whereStr+=str(words[i1])+" "
					# else:
						
						
				processWhere(whereStr,names,l,allTableInfo)
				return [[]]
			else:
				sys.exit("join of only two tables is allowed!")

	s=words[1]
	l=s.split('(')
	if l[0]=="count":
		temp=l[1].split(')')
		if words[2].lower()!="from":
			sys.exit("Invalid Syntax!")
		else:
			fileData=[]
			check=words[3].split(',')
			if len(check)!=1:
				sys.exit("Count can't be performed for more than one columns!")

			readcsvfile(words[3]+'.csv',fileData)
			print words[3]+"."+temp[0]

			# ind=allTableInfo[words[3]].index(temp[0])
			count=0
			for i in fileData:
				count+=1
			return [[str(count)]]

	elif l[0]=="max":
		temp=l[1].split(')')
		if words[2].lower()!="from":
			sys.exit("Invalid Syntax!")
		else:
			fileData=[]
			readcsvfile(words[3]+'.csv',fileData)
			print words[3]+"."+temp[0]

			ind=allTableInfo[words[3]].index(temp[0])
			max_value=-sys.maxint-1
			for i in fileData:
				max_value=max(max_value,int(i[ind]))
			return [[str(max_value)]]

	elif l[0]=="min":
		temp=l[1].split(')')
		if words[2].lower()!="from":
			sys.exit("Invalid Syntax!")
		else:
			fileData=[]
			readcsvfile(words[3]+'.csv',fileData)
			print words[3]+"."+temp[0]
			ind=allTableInfo[words[3]].index(temp[0])
			min_value=sys.maxint
			for i in fileData:
				min_value=min(min_value,int(i[ind]))
			return [[str(min_value)]]

	elif l[0]=="sum":
		temp=l[1].split(')')
		if words[2].lower()!="from":
			sys.exit("Invalid Syntax!")
		else:
			fileData=[]
			readcsvfile(words[3]+'.csv',fileData)
			print words[3]+"."+temp[0]
			ind=allTableInfo[words[3]].index(temp[0])
			res=0
			for i in fileData:
				res+=int(i[ind])
			return [[str(res)]]

	elif l[0]=="avg":
		temp=l[1].split(')')
		if words[2].lower()!="from":
			sys.exit("Invalid Syntax!")
		else:
			fileData=[]
			readcsvfile(words[3]+'.csv',fileData)
			print words[3]+"."+temp[0]
			ind=allTableInfo[words[3]].index(temp[0])
			res=0
			count=0
			for i in fileData:
				res+=int(i[ind])
				count+=1
			res=float(res)/count
			return [[str(res)]]
	
	elif len(words)==4:
		# print "last else"
		if words[2].lower()!='from':
			sys.exit("Invalid Syntax!")
		if l[0]=="":
			# print "1"
			sys.exit("Invalid Syntax!")
		if len(l)>1:
			# print "2"
			sys.exit("Invalid Syntax!")
		# print "here"
		# print l
		# print l[0]
		check=l[0].split(" ")
		# print len(check)
		# print check
		if len(check)>1:
			# print "3"
			sys.exit("Invalid Syntax!")

		columns=l[0].split(",")
		# print "here"
		# print columns
		ind=-1
		for x in range(2,len(words)+1):
			if words[x].lower()=="from":
				ind=x
				break
		if ind==-1:
			# print "4"
			sys.exit("Invalid Syntax!")

		# check=words[3].split(" ")
		# if len(check)>1:
		# 	sys.exit("Invalid Syntax!")
		# print words
		tables=words[3].split(",")
		
		# print "and here"
		# print tables
		#no join is to be performed only single table 
		if len(tables)==1:	
			# print columns
			for i in columns:
				s=words[ind+1]+"."+i
				sys.stdout.write(s+",")
				# print s+",",
			sys.stdout.write("\b")
			print ' '
			fileData=[]
			readcsvfile(words[ind+1]+'.csv',fileData)
			index=[]
			for i in columns:
				if i in allTableInfo:
					index.append(allTableInfo[words[ind+1]].index(i))
				else:
					sys.exit("column "+str(i)+" is not in the table!")
			result=[]
			for i in fileData:
				temporary=[]
				for j in index:
					temporary.append(i[j])
				result.append(temporary)
			# result=removeduplicates(result)
			return result

		else:#join is to be performed 
			# print "here"
			s=""
			for i in columns:
				sys.stdout.write(i+",")
				# print i+",",
				
			sys.stdout.write("\b")
			print ' '
			# fileData1=[]
			# fileData2=[]
			# readcsvfile(tables[0]+'.csv',fileData1)
			# readcsvfile(tables[1]+'.csv',fileData2)
			output=join(columns,tables,allTableInfo)
			return output

	elif len(words)>4:
		# print "congo"
		if words[2].lower()!="from":
			sys.exit("Invalid Syntax!")
		if words[4].lower()!="where":
			sys.exit("Invalid Syntax!")
		if len(words)>12:
			sys.exit("Invalid Syntax!")
		else:
			l=words[3].split(",")
			if len(l)==2:
				# print "2 tables"
				names=[]
				cols=words[1].split(",")
				# print cols
				for i in l:
					if i==",":
						continue
					x=allTableInfo[i]
					for j in x:
						if j not in names:
							names.append(j)
				# for a in cols:
				# 	print a+" ",
				# print 
				# result=join(names,l,allTableInfo)

				whereStr=""
				for i1 in range(5,len(words)):
					whereStr+=str(words[i1])+" "
				processJoinWhere(whereStr,cols,l,allTableInfo)
				return [[]]
				 
			elif len(l)==1:
				cols=words[1].split(",")
				# print cols
				# names=[]
				# for i in l:
				# 	if i==",":
				# 		continue
				# 	x=allTableInfo[i]
				# 	for j in x:
				# 		if j not in names:
				# 			names.append(j)
				for a in cols:
					sys.stdout.write(a+",")
					# print a+",",
				sys.stdout.write("\b")
				print ' ' 
				file1=[]
				file2=[]
				readcsvfile(l[0]+'.csv',file1)
				
				whereStr=""
				for i1 in range(5,len(words)):
					whereStr+=str(words[i1])+" "
				processWhere(whereStr,cols,l,allTableInfo)
				return [[]]

			else:
				sys.exit("Join of only two tables can be performed!")
			# return [[]]
		# return [[]]
allTableInfo={}
readMetaData(allTableInfo)
query=sys.argv[1]
words=[]
query=query.strip() #remove leading and trailing whitespaces
for string in query.split():
	string=string.strip()
	words.append(string)
if words[-1]!=";":
	sys.exit("end the statement with semicolon")

del words[-1]
if words[0].lower()!='select':
	sys.exit("Accepting only select queries1")

else:
	for i in range(len(words)):
		if words[i][0]=="'" and words[i][-1]=="'":
			words[i]=words[i][1:-1]
	result=select(words,allTableInfo)
	for i in result:
		for j in i:
			sys.stdout.write(j+",")
			# print j+",",
			# sys.stdout.write("\b")
		sys.stdout.write("\b")
		print ' '


