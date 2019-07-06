# coding=utf-8
import requests
import json
import threading
from queue import Queue
import datetime


# 多线程验证代理ip是否可用
class ProxyTest:
	def __init__(self):
		self.test_url = "http://pv.sohu.com/cityjson?ie=utf-8"
		self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",}
		self.request_queue = Queue()

	def parse_url(self, url, proxies, timeout=3):
		return requests.get(url, headers=self.headers, proxies=proxies, timeout=timeout).content.decode()

	# 请求
	def request(self):
		while True:
			# 获取ip地址
			ip = self.request_queue.get()

			# 发起请求
			try:
				starttime = datetime.datetime.now()
				html_str = self.parse_url(self.test_url, proxies={"http": ip}, timeout=5)
				endtime = datetime.datetime.now()
				use_time = endtime - starttime
			except Exception as e:
				# 请求超时
				print("timeout %s" % ip)
				self.request_queue.task_done()
				continue
			
			# 检查返回html
			try:
				json_dict = json.loads(html_str[19:-1])
			except:
				print("fail %s, use time %d" % (ip, use_time.seconds))
				self.request_queue.task_done()
				continue

			if ip.startswith("http://"+json_dict["cip"]):
				# 代理可用
				print("success %s, use time %d, %s" % (ip, use_time.seconds, html_str))
				self.request_queue.task_done()
				# 保存到文件
				with open("proxy_ok.json", "a", encoding="utf-8") as f:
					f.write(ip)
					f.write("\n")
			else:
				# ip不是高匿代理
				print("%s invalid, use time %d" % (ip, use_time.seconds))
				self.request_queue.task_done()

	def run(self):
		# 读取ip地址文件 并存储到队列中
		with open("proxy.json", "r", encoding="utf-8") as f:
			for line in f:
				self.request_queue.put(line.strip())

		# 遍历，发送请求，获取响应
		for i in range(30):
			# daemon=True 把子线程设置为守护线程，该线程不重要主线程结束，子线程结束
			threading.Thread(target=self.request, daemon=True).start()
		
		self.request_queue.join() #让主线程等待阻塞，等待队列的任务完成之后再完成

		print("主线程结束")


if __name__ == '__main__':
	proxy = ProxyTest()
	proxy.run()