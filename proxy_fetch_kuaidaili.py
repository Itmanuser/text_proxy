import requests
from lxml import etree


# 爬取免费代理IP 来源kuaidaili.com
class ProxyFetch:
	def __init__(self):
		self.headers = {
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, ", # auto delete br encoding. cos requests and scrapy can not decode it.
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": (
                "Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1562386551; "
                "Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1562386476; "
                "_ga=GA1.2.2146346282.1562386476; "
                "_gat=1; "
                "_gid=GA1.2.1536217319.1562386476; "
                "channelid=0; "
                "sid=1562386470339940; "
            ),
            "Host": "www.kuaidaili.com",
            "Referer": "https://www.kuaidaili.com/free/inha/1/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
		}

	def start_urls(self):
		return ["https://www.kuaidaili.com/free/inha/%d/" % i for i in range(1,100)]

	def parse_url(self, url):
		return requests.get(url, headers=self.headers).content.decode()

	def get_content_list(self, html_str):
		content_list = []
		html = etree.HTML(html_str)
		tr_list = html.xpath('//div[@id="list"]/table/tbody/tr')
		for tr in tr_list:
			item = {}
			item["ip"] = tr.xpath('./td[1]/text()')[0]
			item["port"] = tr.xpath('./td[2]/text()')[0]
			content_list.append(item)
		return content_list

	def save_content_list(self, content_list):
		with open("proxy.json", "a", encoding="utf-8") as f:
			for ip in content_list:
				f.write("http://%s:%s" % (ip["ip"], ip["port"]))
				f.write("\n")

	def run(self):
		start_urls = self.start_urls()
		for url in start_urls:
			html_str = self.parse_url(url)
			# print(html_str)
			content_list = self.get_content_list(html_str)
			self.save_content_list(content_list)

if __name__ == '__main__':
	spider = ProxyFetch()
	spider.run()
