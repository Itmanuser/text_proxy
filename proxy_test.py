import requests


class ProxyTest:
	def __init__(self):
		self.test_url = "http://pv.sohu.com/cityjson?ie=utf-8"
		self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",}

	def get_ip_list(self):
		with open("proxy.json", "r", encoding="utf-8") as f:
			return [i.strip() for i in f.readlines()]

	def parse_url(self, url, proxies, timeout=3):
		return requests.get(url, headers=self.headers, proxies=proxies, timeout=timeout).content.decode()

	def get_content_list(self, html_str):
		print(html_str)
		try:
			return json.loads(html_str[19:-1])
		except:
			return None

	def save_content_list(self, ip):
		with open("proxy_ok.json", "w+", encoding="utf-8") as f:
			f.write(ip + "\n")

	def run(self):
		ip_list = self.get_ip_list()
		for ip in ip_list:
			print(ip)
			try:
				html_str = self.parse_url(self.test_url, proxies={"http": ip}, timeout=5)
			except:
				# 请求超时
				print("%s timeout" % ip)
				continue
			
			json_dict = self.get_content_list(html_str)
			if json_dict is not None and ip.startswith("http://"+json_dict["cip"]):
				# 代理可用
				print("%s success" % ip)
				self.save_content_list(ip)
			else:
				# ip不是高匿代理
				print("%s fail" % ip)

if __name__ == '__main__':
	spider = ProxyTest()
	spider.run()
