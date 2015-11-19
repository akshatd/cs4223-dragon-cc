import sys
import csv
import pylru

arguments = []
for argument in sys.argv:
	arguments.append(argument)

protocol = arguments[1]
input_file = arguments[2]
no_processors = arguments[3]
cache_size = arguments[4]
associativity = arguments[5]
block_size = arguments[6]

word_size = 2
words_per_block = block_size/int(word_size)
fileList = []

cacheSets = int(math.ceil(cache_size/(associativity * block_size)))
CPU = []

#bus signals
# "BusRdNotShared"
# "BusRdShared"
# "BusUpdNotShared"
# "BusUpdShared"

currBusSignal = ""
currBusData = 0
totalBusTraffic = 0

class Processor(object):

	def __init__(self, no, trace, cache):
		self.no = no
		self.trace = trace
		self.cache = cache
		self.stalls = 0
		self.cycles = 0
		self.misses = 0
		self.instr_count = 0
		self.stalled_instr = [0, 0]
		self.finished = False

	def getState(self, address):
		block = int(math.floor(address/block_size))
		blockSet = block % cacheSets
		if block in self.cache[blockSet]:
			return self.cache[blockSet][block]
		else:
			return "I"

	def setState(self, address, state):
		block = int(math.floor(address/block_size))
		blockSet = block % cacheSets
		if state == "I":
			if block in self.cache[blockSet]:
				del self.cache[blockSet][block]			
		else:
			self.cache[blockSet][block] = state

try:
	#initialising
	for i in range(0, no_processors):
		filename = input_file + "/" + input_file + str(i+1) + ".PRG"
		tempFile = open(filename, "rb")

		fileList.append(tempFile) #to close later

		traceFileReader = csv.reader(tempFile, delimiter=' ')
		cache = []
		for j in range(0, cacheSets):
			cache.append(pylru.lrucache(associativity))

		CPU.append(Processor(i, traceFileReader, cache))

	all_done = False

	#starting processing
	while not all_done:
		for core in CPU:
			core.cycles += 1
			if core.stalls = 0:
				try:
					nextMemAccess = core.trace.next()
				except StopIteration:
					#no more left! yay!
					core.done = True
					print "core " + core.no + "ended, and "
					all_done = True
					for doneCore in CPU:
						print "core " + doneCore.no + "is " + str(doneCore.done)
						if doneCore.done = False:
							all_done = False
					continue
				#more left, comtinue
				nextInstr = int(nextMemAccess[0])
				nextAddr  int(nextMemAccess[1])
				core.instr_count += 1

				#fetch instruction
				if nextInstr == 0:
					pass

				#read
				elif nextInstr == 2:
					state = core.getState(nextAddr)
					if state == "M":
						pass
					if state == "E":
						pass
					if state == "Sc":
						pass
					if state == "Sm":
						pass
					#PrRdMiss
					if state == "I":
						core.misses += 1
						core.stalled_instr = [nextInstr, nextAddr]
						totalBusTraffic += block_size
						#check if shared
						shared = False
						for coreShared in CPU:
							if coreShared.getState(nextAddr) != "I"
								shared = True

						if not shared:
							core.stalls += 100
						else:
							core.stalls += words_per_block


				#write
				elif nextInstr == 3:
					state = core.getState(nextAddr)
					if state == "M":
						pass
					if state == "E":
						core.setState(nextAddr, "M")
					if state == "Sc":
						core.stalls += 2
						core.stalled_instr = [nextInstr, nextAddr]
						totalBusTraffic += 2
					if state == "Sm":
						core.stalls += 2
						core.stalled_instr = [nextInstr, nextAddr]
						totalBusTraffic += 2
					#PrWrMiss
					if state == "I":
						core.misses += 1
						core.stalled_instr = [nextInstr, nextAddr]
						totalBusTraffic += block_size
						#check if shared
						shared = False
						for coreShared in CPU:
							if coreShared.getState(nextAddr) != "I"
								shared = True

						if not shared:
							core.stalls += 100
						else:
							core.stalls += words_per_block

				#print no of instr?


				
		
finally:
	#printing statistics
	for f in fileList:
		f.close
