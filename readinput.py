class Instruction:
	def __init__(self,op,destreg,sreg1,sreg2):
		self.op=op
		self.destreg=destreg
		self.sreg1=sreg1
		self.sreg2=sreg2

class ExecutionUnit:
	def __init__(self):
		self.busy=0
		self.currentRS=None
		self.executionStarted=None
		# self.destinationRS=None
		self.remainingcycles=None
		self.op=None
		self.arg1=None
		self.arg2=None

	def clear(self):
		self.busy=0
		self.curentRS=None
		self.executionStarted=None
		self.op=None
		self.argr1=None
		self.arg2=None
		self.op=None

addExecutionUnit=ExecutionUnit()
multExecutionUnit=ExecutionUnit()
currentCycle=1
def isExecutionUnitFree(op):
	if(op==1 or op==0):
		return addExecutionUnit.busy
	elif(op==2 or op==3):
		return multExecutionUnit.busy
	else:
		print('invalid code')

def assignExecutionStation(reservationS,i,cycle):	
	if (reservationS.op==1 or reservationS.op==0):
		addExecutionUnit.busy=1
		addExecutionUnit.currentRS=i
		addExecutionUnit.executionStarted=cycle+1
		addExecutionUnit.op=reservationS.op
		addExecutionUnit.arg1=reservationS.vj
		addExecutionUnit.arg2=reservationS.vk
		return
	
	elif(instr.op==2):
		multExecutionUnit.busy=1
		multExecutionUnit.currentRS=i
		multExecutionUnit.executionStarted=cycle+1
		multExecutionUnit.op=reservationS.op
		multExecutionUnit.arg1=reservationS.vj
		multExecutionUnit.arg2=reservationS.vk
		return
	elif(instr.op==3):
		multExecutionUnit.busy=1
		multExecutionUnit.currentRS=i
		multExecutionUnit.remainingcycles=40
		multExecutionUnit.executionStarted=cycle+1
		multExecutionUnit.op=reservationS.op
		multExecutionUnit.arg1=reservationS.vj
		multExecutionUnit.arg2=reservationS.vk
		return



with open("input.txt","r") as f:
	 content=f.read().splitlines()
print(content)
n=int(content[0])
cycles=int(content[1])
instrList=[]
# reading instructions
for i in range(n):
	temp = [int(value) for value in content[i+2].split()]
	tempInstr=Instruction(temp[0],temp[1],temp[2],temp[3])
	instrList.append(tempInstr)
print(instrList[1].op)

# index i stores Ri register Value
RF=[] #index 0 is empty
for i in range(n+2,n+10):
	RF.append(int(content[i]))
print(RF)

RAT=[None]*8   #TUPLE(I,J) I=0 if it points to RF and I=1 If it points to Register Station
print(RAT)


class ReservationStation:
	def __init__(self,id,busy=1,op=-1,vj=-1,vk=-1,qj=-1,qk=-1,disp=0):
		self.id=id
		self.busy=busy
		self.op=op
		self.vj=vj
		self.vk=vk
		self.qj=qj
		self.qk=qk
		self.disp=disp

	def dispatch(self):
		self.disp=1

	def clear(self):
		self.busy=0
		self.op=-1
		self.vj=-1
		self.vk=-1
		self.qj=-1
		self.qk=-1
		self.disp=0

	def __str__(self):
		return 'RS'+str(self.id)+' 	'+str(self.busy)+'  	'+str(self.op)+'  	'+str(self.vj)+'  	'+str(self.vk)+'  	'+str(self.qj)+'  	'+str(self.qk)+'  	'+str(self.disp)

RS=[]
for i in range(5):
	temp=ReservationStation(busy=0,id=i,op=-1,vj=-1,vk=-1,qj=-1,qk=-1,disp=0)
	RS.append(temp)
# print(RS[0])	
def printReservationStation(RS):
	print('\n Reservation Station')
	print('RS 	busy 	op  	vj  	vk  	qj  	qk  	disp')
	for i in range(len(RS)):
		print(RS[i])
	printRAT(RAT)
def printRAT(RAT):
	for i in range(len(RAT)):
		print('R',i,' ',RAT[i])



#to do's
# 1.iterate each cycle
# 2.issue, dispatch, execute, writeback,capture 

def isRSAvailable(opcode):
	print('opcode',opcode)
	if (opcode==0 or opcode==1):
		#check if add RS is available
		if RS[0].busy==0:
			#assign instr to rs0
			return 0
		elif RS[1].busy==0:
			return 1
		elif RS[2].busy==0:
			return 2
		else:
			# reservation station is not available do not issue instr
			return -1

	elif (opcode==2 or opcode==3):
		#check is multiply RS available
		if RS[3].busy==0:
			#assign instr to rs0
			return 3
		elif RS[4].busy==0:
			return 4
		else:
			return -1


def writeBack():
	if addExecutionUnit.busy==1:
		if (currentCycle== addExecutionUnit.executionStarted+2):
			currentRS=addExecutionUnit.currentRS
			if(addExecutionUnit.op==0):
				result=addExecutionUnit.vj+ addExecutionUnit.vk
			else:
				result=addExecutionUnit.vj-addExecutionUnit.vk			
			for i in range(len(RAT)):
				if(RAT[i]== currentRS):
					RF[i]= result
					RAT[i]=None
			for i in range(len(RS)):
				if(RS[i].qk==currentRS):
					RS[i].vk=result
					RS[i].qk=-1
				if(RS[i].qj==currentRS):
					RS[i].vj=result
					RS[i].qj=-1
			RS[currentRS].clear()
			addExecutionUnit.clear()
			print('add or sub done result is ',result)

	if multExecutionUnit.busy==1:
			if (multExecutionUnit.op==2 and currentCycle== addExecutionUnit.executionStarted+10):
				currentRS=multExecutionUnit.currentRS
				result=multExecutionUnit.vj* multExecutionUnit.vk			
				for i in range(len(RAT)):
					if(RAT[i]== currentRS):
						RF[i]= result
						RAT[i]=None
				for i in range(len(RS)):
					if(RS[i].qk==currentRS):
						RS[i].vk=result
						RS[i].qk=-1
					if(RS[i].qj==currentRS):
						RS[i].vj=result
						RS[i].qj=-1
				RS[currentRS].clear()
				multExecutionUnit.clear()
				print('multiplication done result is ',result)

			elif (multExecutionUnit.op==3 and currentCycle== addExecutionUnit.executionStarted+40):
				currentRS=multExecutionUnit.currentRS
				result=multExecutionUnit.vj/ multExecutionUnit.vk			
				for i in range(len(RAT)):
					if(RAT[i]== currentRS):
						RF[i]= result
						RAT[i]=None
				for i in range(len(RS)):
					if(RS[i].qk==currentRS):
						RS[i].vk=result
						RS[i].qk=-1
					if(RS[i].qj==currentRS):
						RS[i].vj=result
						RS[i].qj=-1
				RS[currentRS].clear()
				multExecutionUnit.clear()
				print('division done result is ',result)







def simulateCycle():
	#1. issue 
	if len(instrList)>0:
		freestation=isRSAvailable(instrList[0].op)
		print('freestation',freestation)
		if(freestation!=-1):
			#issue the instr
			instr=instrList.pop(0)
			RS[freestation].busy=1
			RS[freestation].op=instr.op
			#first source register
			if(RAT[instr.sreg1]==None):
				#assign value from RF
				RS[freestation].vj=RF[instr.sreg1]
			else:
				#assign value from RS
				RS[freestation].qj=RF[instr.sreg1]
			#second source register
			if(RAT[instr.sreg2]==None):
					#assign value from RF
				RS[freestation].vk=RF[instr.sreg2]
			else:
				#assign value from RS
				RS[freestation].qk=RF[instr.sreg2]

			RAT[instr.destreg]=freestation
		else:
			# RS  is not available do nothing
			pass
		
	#2 dispatch
	# see if among RS their is any station with both ready values
	for i in range(len(RS)):
		if(RS[i].busy==1 and RS[i].disp==0):
			if(RS[i].vk!=-1 or RS[i].vk!=-1):
				if(isExecutionUnitFree(RS[i].op)==1):
					RS[i].disp=1
					assignExecutionStation(RS[i],i,currentCycle)
	#3 execute

	#4 writeback
	writeBack()

	print('-------------Current Cycle-------',currentCycle)
	global currentCycle
	currentCycle+=1



printReservationStation(RS)


for i in range(13):
	simulateCycle()

printReservationStation(RS)

# for i in range(cycles):
# 	simulateCycle()
# print(RS)
# print(RAT)
# print(RF)












