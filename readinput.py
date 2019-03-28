class Instruction:
	def __init__(self,op,destreg,sreg1,sreg2):
		self.op=op
		self.destreg=destreg
		self.sreg1=sreg1
		self.sreg2=sreg2
	

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

RAT=[-1,-1,-1,-1,-1,-1,-1,-1]   #TUPLE(I,J) I=0 if it points to RF and I=1 If it points to Register Station
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

	def __str__(self):
		return 'RS'+str(self.id)+' 	'+str(self.busy)+'  	'+str(self.op)+'  	'+str(self.vj)+'  	'+str(self.vk)+'  	'+str(self.qj)+'  	'+str(self.qk)+'  	'+str(self.disp)

RS=[]
for i in range(5):
	temp=ReservationStation(busy=0,id=i,op=-1,vj=-1,vk=-1,qj=-1,qk=-1,disp=0)
	RS.append(temp)
# print(RS[0])	
def printReservationStation(RS):
	print('RS 	busy 	op  	vj  	vk  	qj  	qk  	disp')
	for i in range(len(RS)):
		print(RS[i])




#to do's
# 1.iterate each cycle
# 2.issue, dispatch, execute, writeback,capture 

def isRSAvailable(opcode):
	if opcode==0:
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

	elif opcode==1:
		#check is multiply RS available
		if RS[3].busy==0:
			#assign instr to rs0
			return 3
		elif RS[4].busy==0:
			return 4
		else:
			return -1

def simulateCycle():
	#1. issue 
	freestation=isRSAvailable(instrList[0].op)
	if(freestation!=-1):
		#issue the instr
		instr=instrList.pop(0)
		RS[freestation].busy=1
		RS[freestation].op=instr.op
		#first source register
		if(RAT[instr.sreg1]==-1):
			#assign value from RF
			RS[freestation].vj=RF[instr.sreg1]
		else:
			#assign value from RS
			RS[freestation].qj=RF[instr.sreg1]
		#second source register
		if(RAT[instr.sreg2]==-1):
				#assign value from RF
			RS[freestation].vk=RF[instr.sreg1]
		else:
			#assign value from RS
			RS[freestation].qk=RF[instr.sreg1]

		RAT[instr.destreg]=freestation
	else:
		# RS  is not available do nothing
		pass
		
	#2 dispatch


	#3 execute


	#4 writeback

printReservationStation(RS)
simulateCycle()
printReservationStation(RS)



# for i in range(cycles):
# 	simulateCycle()
# print(RS)
# print(RAT)
# print(RF)












