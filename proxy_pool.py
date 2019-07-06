import random
import requests


class ProxyPool:
	def __init__(self, proxy_list):
		self.proxy_list = [{"ip": i, "count": 0} for i in proxy_list]

	def get_proxy(self):
		proxy_list = sorted(self.proxy_list, key=lambda x: x["count"])
		proxy_list = proxy_list[:3]
		# print(proxy_list)
		proxy = random.choice(proxy_list)
		proxy["count"] += 1
		return proxy["ip"]


if __name__ == '__main__':
	# 读取ip地址文件 并存储到队列中
	proxy_list = []
	with open("proxy_ok.json", "r", encoding="utf-8") as f:
		for line in f:
			proxy_list.append(line.strip())

	# 代理ip池
	proxy_pool = ProxyPool(proxy_list)
	for i in range(100):
		print(proxy_pool.get_proxy())
