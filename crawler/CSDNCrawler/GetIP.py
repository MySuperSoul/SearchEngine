import requests
from lxml import etree
import threading
import aiohttp
import asyncio
import random
import time


headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "Connection": "close"
           }


# https://lab.crossincode.com/proxy/
def web1():
    result = []
    try:
        res = requests.get("https://lab.crossincode.com/proxy/", headers=headers)
        if res.status_code == 200:
            print("web1: 200")
            html = res.text
            # print(html)
            html = etree.HTML(html)
            a_list = html.xpath('//tr')
            print(len(a_list))
            for i in range(1, len(a_list)):
                tr = a_list[i]
                td_list = tr.xpath('./td')
                ip = td_list[0].text
                port = td_list[1].text
                result.append("http://" + ip + ":" + port)

            print("web1  OK  total: " + str(len(result)))
            return result
        else:
            print("web1: Fail")
            return result
    except Exception as e:
        print(e)
        print("web1: Fail")
        return result


# https://cn-proxy.com/
def web2():
    result = []
    try:
        res = requests.get("https://cn-proxy.com/", headers=headers)
        if res.status_code == 200:
            print("web2: 200")
            html = res.text
            # print(html)
            html = etree.HTML(html)
            a_list = html.xpath('//tbody/tr')
            print(len(a_list))
            for i in range(0, len(a_list)):
                tr = a_list[i]
                td_list = tr.xpath('./td')
                ip = td_list[0].text
                port = td_list[1].text
                result.append("http://" + ip + ":" + port)

            print("web2  OK  total: " + str(len(result)))
            return result
        else:
            print("web2: Fail")
            return result
    except Exception as e:
        print(e)
        print("web2: Fail")
        return result


# https://www.kuaidaili.com/free/
def web3():
    result = []
    try:
        res = requests.get("https://www.kuaidaili.com/free/", headers=headers)
        if res.status_code == 200:
            print("web3: 200")
            html = res.text
            # print(html)
            html = etree.HTML(html)
            a_list = html.xpath('//tbody/tr')
            print(len(a_list))
            for i in range(0, len(a_list)):
                tr = a_list[i]
                td_list = tr.xpath('./td')
                ip = td_list[0].text
                port = td_list[1].text
                result.append("http://" + ip + ":" + port)

            print("web3  OK  total: " + str(len(result)))
            return result
        else:
            print("web3: Fail")
            return result
    except Exception as e:
        print(e)
        print("web3: Fail")
        return result


# https://www.xicidaili.com/
def web4():
    result = []
    try:
        res = requests.get("https://www.xicidaili.com/", headers=headers)
        if res.status_code == 200:
            print("web4: 200")
            html = res.text
            # print(html)
            html = etree.HTML(html)
            a_list = html.xpath('//table/tr')
            print(len(a_list))
            for i in range(2, len(a_list)):
                try:
                    tr = a_list[i]
                    td_list = tr.xpath('./td')

                    ip = td_list[1].text
                    port = td_list[2].text
                    if port.isdigit():
                        if td_list[5].text == "HTTPS":
                            result.append("https://" + ip + ":" + str(int(port)))
                        elif td_list[5].text == "HTTP":
                            result.append("http://" + ip + ":" + str(int(port)))
                except:
                    continue

            print("web4  OK  total: " + str(len(result)))
            return result
        else:
            print("web4: Fail")
            return result
    except Exception as e:
        print(e)
        print("web4: Fail")
        return result


# http://www.xiladaili.com/
def web5():
    result = []
    try:
        res = requests.get("http://www.xiladaili.com/", headers=headers)
        if res.status_code == 200:
            print("web5: 200")
            html = res.text
            # print(html)
            html = etree.HTML(html)
            a_list = html.xpath('//tbody/tr')
            print(len(a_list))
            for i in range(0, len(a_list)):
                tr = a_list[i]
                td_list = tr.xpath('./td')
                if td_list[2].text.find("HTTP"):
                    result.append("http://" + td_list[0].text)
                else:
                    result.append("https://" + td_list[0].text)

            print("web5  OK  total: " + str(len(result)))
            return result
        else:
            print("web5: Fail")
            return result
    except Exception as e:
        print(e)
        print("web5: Fail")
        return result


# http://www.nimadaili.com/
def web6():
    result = []
    try:
        res = requests.get("http://www.nimadaili.com/", headers=headers)
        if res.status_code == 200:
            print("web6: 200")
            html = res.text
            # print(html)
            html = etree.HTML(html)
            a_list = html.xpath('//tbody/tr')
            print(len(a_list))
            for i in range(0, len(a_list)):
                tr = a_list[i]
                td_list = tr.xpath('./td')
                if len(td_list) != 1:
                    if td_list[2].text.find("HTTP"):
                        result.append("http://" + td_list[0].text)
                    else:
                        result.append("https://" + td_list[0].text)

            print("web6  OK  total: " + str(len(result)))
            return result
        else:
            print("web6: Fail")
            return result
    except Exception as e:
        print(e)
        print("web6: Fail")
        return result


# http://www.89ip.cn/
def web7():
    result = []
    try:
        res = requests.get("http://www.89ip.cn/", headers=headers)
        if res.status_code == 200:
            print("web7: 200")
            html = res.text
            # print(html)
            html = etree.HTML(html)
            a_list = html.xpath('//tbody/tr')
            print(len(a_list))
            for i in range(0, len(a_list)):
                tr = a_list[i]
                td_list = tr.xpath('./td')
                try:
                    ip = td_list[0].text.strip()
                    port = td_list[1].text.strip()
                    result.append("http://" + ip + ":" + str(int(port)))
                except Exception as e:
                    continue

            print("web7  OK  total: " + str(len(result)))
            return result
        else:
            print("web7: Fail")
            return result
    except Exception as e:
        print(e)
        print("web7: Fail")
        return result


def test_ip(proxy):
    proxies = {}
    if proxy.find("http") != -1:
        proxies["http"] = proxy
    else:
        proxies["https"] = proxy

    try:
        res = requests.get('http://ip111.cn/', proxies=proxies, timeout=3)
        if res.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        return False


class IPCrawler(threading.Thread):
    def __init__(self, max_threads):
        super(IPCrawler, self).__init__()
        self.stop_flag = True  # 结束线程的标志
        self.tmp_ip_list = []   # 中间IP列表
        self.max_threads = max_threads  # 最大线程数
        self.update_flag = False    # 是否正在更新
        self.ip_map = {}    # IP池
        self.ip_map_lock = threading.Lock()  # IP池的锁

    @staticmethod
    async def test(proxy):
        async with aiohttp.ClientSession() as session:
            async with session.get('http://ip111.cn/', proxy=proxy, timeout=3) as response:
                assert response.status == 200  # 不是200的状态码，就直接抛出异常
                print("Good IP:  " + proxy)
                # html = await response.read()

    async def test_ip(self, task_id, q):
        while not q.empty():
            proxy = await q.get()
            try:
                await self.test(proxy)
                self.tmp_ip_list.append([proxy, 6])  # 好的IP一开始为5
            except Exception as e:
                self.tmp_ip_list.append([proxy, 4])  # 坏的IP一开始为4
        print("Finish " + str(task_id))

    def run(self):
        # 每隔着1分钟去爬IP，并且更新IP池
        while self.stop_flag:
            start_time = time.time()
            print("开始爬取")

            self.tmp_ip_list.clear()    # 把中间list清空
            self.tmp_ip_list.extend(web1())
            self.tmp_ip_list.extend(web2())
            self.tmp_ip_list.extend(web3())
            self.tmp_ip_list.extend(web4())
            self.tmp_ip_list.extend(web5())
            self.tmp_ip_list.extend(web6())
            self.tmp_ip_list.extend(web7())

            print("total: " + str(len(self.tmp_ip_list)))

            # 验证
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            q = asyncio.Queue()
            [q.put_nowait(url) for url in self.tmp_ip_list]  # 放到队列中
            self.tmp_ip_list.clear()    # 把中间list清空
            tasks = [self.test_ip(task_id, q) for task_id in range(self.max_threads)]
            loop.run_until_complete(asyncio.wait(tasks))    # 开始爬取
            loop.close()

            self.update_flag = True  # 开始更新，不让操作ip_map
            time.sleep(2)  # 等待一会，防止出现其他线程对ip_map的改变
            if self.ip_map_lock.acquire():
                self.ip_map.clear()     # 清空ip_map
                for i in self.tmp_ip_list:  # 把检查过的ip以及对应的存活指数放到map中
                    self.ip_map[i[0]] = i[1]    # 更新IP Map
                self.ip_map_lock.release()
            self.update_flag = False    # 更新完毕

            print("爬取并完成验证: " + str(len(self.ip_map)))
            end_time = time.time()
            print("所用时间: " + str(end_time - start_time))
            # print(self.ip_map)
            time.sleep(90)

        time.sleep(2)
        print("结束IPCrawler线程")

    # 暂停IPCrawler线程
    def stop(self):
        self.stop_flag = False

    # 从IP池中拿一个最好的IP
    def get_ip(self):
        while self.update_flag:  # 正在更新就一直等待
            time.sleep(1)
        tmp_list = sorted(self.ip_map.items(), key=lambda item: item[1], reverse=True)  # 根据存活指数从大到小排序
        if len(tmp_list) == 0:  # IP池中没东西就直接返回
            return ""
        else:
            max_value = tmp_list[0][1]  # 得到最大的存活指数
            random_list = []
            for i in tmp_list:  # 把都是这个存活指数的IP拿出来，然后随机选取一个
                if i[1] == max_value:
                    random_list.append(i[0])
            return random.choice(random_list)

    def update_ip_value(self, ip):
        if (not self.update_flag) and self.ip_map_lock.acquire():  # 如果正在更新，就放弃更新map。否则就获得锁，更新map
            if self.ip_map.get(ip, default=None) is None:
                return
            if self.ip_map[ip] > 0:
                self.ip_map[ip] = self.ip_map[ip] - 1
            self.ip_map_lock.release()

    def get_html(self, url, flag=False):  # 爬CSDN, flag传True
        retry = 5
        while retry > 0:
            proxy = self.get_ip()
            proxies = {}
            if proxy.find("http") != -1:
                proxies["http"] = proxy
            else:
                proxies["https"] = proxy
            try:
                res = requests.get(url, headers=headers, proxies=proxies, timeout=5)
                # print(res.text)
                if res.status_code == 200:
                    if not flag:
                        return res.text
                    elif res.text.find("csdn") != -1:
                        return res.text
            except Exception as e:
                self.update_ip_value(proxy)
            retry = retry - 1

        # 直接用自己IP爬
        try:
            time.sleep(3)
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                if not flag:
                    return res.text
                elif res.text.find("csdn") != -1:
                    return res.text
        except Exception as e:
            return ""

        return ""


if __name__ == "__main__":
    # thread = IPCrawler(16)
    # thread.start()
    # thread.join()
    # web4()
    pass