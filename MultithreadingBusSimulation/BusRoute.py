# usage: python BusRoute.py nstop nbus arrivalrate travelrate maxsimtime

# nstop - number of bus stops
# nbus - number of buses (assumed less than nstop)
# arrivalrate - reciporocal of the mean time between passenger arrivals (per bus stop)
# travelrate - reciporocal of the mean time needed for a bus to go from one bus stop to the next
# maxsimtime - amount of time to be simulated

from SimPy.Simulation import *
import random
import sys

class G: # for Rnd
	stops = []
	buses = []
	Rnd = random.Random(12345)

class BusClass(Process):
	travelRate = None #rate to next stop
	initBuses = 0 #number of buses

	totalCircuits = 0 #total completed circuits
	totalCycleTime = 0.0 #total time completing total circuits

	def __init__(self, travelRate):
		Process.__init__(self)
		BusClass.travelRate = travelRate

		self.currentStop = 0 #buses all start at stop #0
		self.cycleStartTime = now()

		self.busID = BusClass.initBuses
		BusClass.initBuses += 1

	def Run(self):
		while 1:
			#check stop to see if any buses are already at the stop
			if G.stops[self.currentStop].busWaiting == False:
				if G.stops[self.currentStop].passWaiting == False:
					G.stops[self.currentStop].busWaiting = True
					G.stops[self.currentStop].busIndex = self.busID
					yield passivate, self #wait for passenger
				else: #pick up the passenger already waiting
					G.stops[self.currentStop].passWaiting = False

			#travel to next stop
			yield hold, self, G.Rnd.expovariate(BusClass.travelRate)
			self.currentStop += 1
			#cycle if at last stop
			if self.currentStop == len(G.stops):
				self.currentStop = 0

			#if full cycle
			if self.currentStop == 0:
				BusClass.totalCycleTime += now() - self.cycleStartTime
				BusClass.totalCircuits += 1					
				self.cycleStartTime = now()



class StopClass(Process):
	arrivalRatePass = None
	initStops = 0
	passTotal = 0
	passTotalImmedBoard = 0

	def __init__(self, arrivalRate):
		Process.__init__(self)
		StopClass.arrivalRatePass = arrivalRate

		self.passWaiting = False
		self.busWaiting = False
		self.busIndex = None

		self.stopID = StopClass.initStops
		StopClass.initStops += 1
		
	def Run(self):
		while 1:
			yield hold, self, G.Rnd.expovariate(StopClass.arrivalRatePass)
			if self.busWaiting == 1:
				StopClass.passTotal += 1
				StopClass.passTotalImmedBoard += 1
				reactivate(G.buses[self.busIndex])
				self.busWaiting = False
				self.busIndex = None
			else:
				StopClass.passTotal += 1
				self.passWaiting = True


def main():
	initialize()  

	nstop = int(sys.argv[1])
	nbus = int(sys.argv[2])
	arrivalrate = float(sys.argv[3])
	travelrate = float(sys.argv[4])
	MaxSimtime = float(sys.argv[5])

	for i in range(nstop):
		G.stops.append(StopClass(arrivalrate))
		activate(G.stops[i],G.stops[i].Run())

	for i in range(nbus):
		G.buses.append(BusClass(travelrate))
		activate(G.buses[i],G.buses[i].Run())
   
	simulate(until=MaxSimtime)
	
	print 'average circuit time:', float(BusClass.totalCycleTime) / float(BusClass.totalCircuits)
	print 'prop. pass. immed. board:', float(StopClass.passTotalImmedBoard) / float(StopClass.passTotal)


if __name__ == '__main__':  main()