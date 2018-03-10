from urllib import request
from bs4 import	BeautifulSoup

def DownloadReport(blockCount, blockSize, totalLength):
	downloadedSize = blockCount*blockSize
	if(downloadedSize > totalLength):
		downloadedSize = totalLength
	print("%d/%d"%(downloadedSize,totalLength))

class TyporaThemeDownloader:
	def __init__(self):
		self.url_home = "http://theme.typora.io/"

	def show_url(self):
		print(self.url_home)
		return True

	def get_page(self, url):
		with request.urlopen(url) as page:
			return page.read()

	def get_theme_list(self, html, theme_list):
		soup = BeautifulSoup(html, "html.parser")
		for link in soup.find_all('a'):
			href = link.get("href")
			if "theme" in href:
				theme_list.append(href)
		for i in range(len(theme_list)):
			theme_list[i] = self.url_home + theme_list[i]
			
	def get_download_site(self, html):
		soup = BeautifulSoup(html, "html.parser")
		for link in soup.find_all('a'):
				if link.string == "Download":
					site = link.get("href")
					return site
			
	def download_theme(self):
		theme_list = list()
		home_src = self.get_page(self.url_home)
		self.get_theme_list(home_src, theme_list)
		theme_path = list()
		for link in theme_list:
			page = self.get_page(link)
			site = self.get_download_site(page)
			if site != None:
				theme_path.append(site)
		for link in theme_path:
			filename = link.split("?")[0].split("/")[-1]
			if filename == "master.zip":
				fileformat = ".zip"
				filename = link.split("?")[0].split("/")[-3] + fileformat
			print(filename)
			request.urlretrieve(url = link, filename = filename,
			reporthook = DownloadReport)
		
			
instance = TyporaThemeDownloader()
instance.download_theme()