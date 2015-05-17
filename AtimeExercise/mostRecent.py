# Commandline Usage: python mostRecent.py fileName[ fileName]
#
# Depending on mount options/OS defaults, there may be inconsistencies:
#		if noatime, atimes are never updated, so we return an error message
#		if nodiratime, directory atimes are never updated, so we ignore directories
#		if relatime, only atimes older than 24hrs are updated, so there may be inaccurate results
#
#		I compare the atimes I can find, and print any errors to the console
#
# Tested on python2.7

import os, sys
import datetime


class CompareAtime:
	def __init__(self, files):
		#uses set exclusivity to prevent redundant searching for a file if entered multiple times
		self.files = files
		self.newestAtime = 0

	def compare(self):
		for filePath in self.files:
			#check file mount noatime option
			if os.path.exists(filePath):
				try:
					#get atime
					fileAtime = os.path.getatime(filePath)
				except OSError as e:
					#getatime() throws an error if DNE or inaccessible. 
					#Because DNE is already checked, this should exclusively tell us if noatime or nodiratime is set
					if os.path.isdir(filePath):
						#accounts for nodiratime option, continues checking atimes for rest of self.files
						print "Perhaps nodiratime option is set: unable to find access time for directory " + filePath
						continue #to next iteration
					else:
						return "noatime option set in /etc/fstab, unable to find most recent access times"
			else:
				print "Unable to find file: " + filePath
				continue #to next iteration

			# Don't think it's necessary to worry about two files somehow with the same atime
			if(fileAtime > self.newestAtime):
				self.newestAtime = fileAtime
				self.newestPath = filePath

		#verify at least one file was found
		if(self.newestAtime == 0): #no files were found
			return "Unable to locate access times for listed files"
		else:
			return self.newestPath # + " was most recently accessed (at " + str(datetime.datetime.fromtimestamp(self.newestAtime)) + ")"


def main():
	#check number of arguments
	if(len(sys.argv) == 1):
		print "Error: missing arguments\nUsage: python mostRecent.py fileName[ fileName]"
		return

	comparedFiles = CompareAtime(set(sys.argv[1:]))
	print comparedFiles.compare()


if __name__ == '__main__': main()