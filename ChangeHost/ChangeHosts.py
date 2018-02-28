#!/usr/bin/python
from urllib import request
from os import getenv,path
from sys import argv
import argparse



configPath = "hosts.conf"
hostsPath = "/etc/hosts"
print(hostsPath)
tmpPath = "hosts.tmp"
if(path.exists(tmpPath)):
	print("Tmp file exits.")
else:
	open(tmpPath, 'w').close()

numList = list(range(0, 10))

def DownloadReport(blockCount, blockSize, totalLength):
	downloadedSize = blockCount*blockSize
	if(downloadedSize > totalLength):
		downloadedSize = totalLength
	print("%d/%d"%(downloadedSize,totalLength))

def ReadConfig():
	with open(configPath, "r") as configFile:
		urls = configFile.readlines()
		return urls

def Init(urls):
	with open(tmpPath, 'w') as tmpFile:
		for (url,number) in zip(urls, numList):
			print(url)
			with request.urlopen(url) as hostsSrc:
				headers = hostsSrc.getheaders()
				tmpFile.write(str(headers[10]))
				tmpFile.write("\n")
				request.urlretrieve(url,"hosts_"+str(number), DownloadReport)

def Update(urls):
	updateFlag = False

	tmpFile = open(tmpPath, 'r')
	hostsLength = tmpFile.read().splitlines()
	tmpFile.close()

	for (url,length,number) in zip(urls,hostsLength,numList):
		print(url)
		with request.urlopen(url) as hostsSrc:
			headers = hostsSrc.getheaders()
			print("%s\n%s"%(length, str(headers[10])))
			if(length == str(headers[10])):
				print("No update.")
			else:
				updateFlag = True
				hostsLength[number] = str(headers[10])
				request.urlretrieve(url, "hosts_"+str(number), DownloadReport, None )
	tmpFile = open(tmpPath, "w")
	for elem in hostsLength:
		tmpFile.write(elem)
		tmpFile.write("\n")
	tmpFile.close()
	if updateFlag:
		return True
	else :
		return False


def WritetoFile(urls):
	with open(hostsPath,"w") as hostsDes:
			for (url, num) in zip(urls, numList):
					with open("hosts_"+str(num),'r') as hostsSrc:
							hostsDes.write(hostsSrc.read())

class InitAction(argparse.Action):
	def __call__(self, parser, namespace, values, option_string=None):
		urls = ReadConfig()
		Init(urls)
		WritetoFile(urls)

class UpdateAction(argparse.Action):
	def __call__(self, parser, namespace, values, option_string=None):
		urls = ReadConfig()
		if Update(urls):
			WritetoFile(urls)

class WriteAction(argparse.Action):
	def __call__(self, parser, namespace, values, option_string=None):
		urls = ReadConfig()
		WritetoFile(urls)

parser = argparse.ArgumentParser(argument_default="--help", description="A tool to change hosts writen by python3.")
parser.add_argument("-i", "--init", nargs=0, action=InitAction, help="Init the Program.")
parser.add_argument("-u", "--update", nargs=0, action=UpdateAction, help="Update the hosts if has a new version.")
parser.add_argument("-w", "--write", nargs=0, action=WriteAction, help="write the downloaded file to hosts.")
parser.parse_args()