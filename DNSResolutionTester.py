import dns.resolver
import time
import numpy as np
import pandas as pd
import json

def dns_test(domain,dns_server):
    elapsed_times = []
    i = 0
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_server]
    resolver.timeout = 2
    while(i<10):
        try:
            start_time = time.perf_counter()
            resolver.resolve(domain,"A")
            end_time = time.perf_counter()
            # for rdata in answers:
            #     print(rdata.to_text())
            elapsed_time = end_time - start_time
            elapsed_times.append(round(elapsed_time*1000,2))
        except dns.resolver.NoAnswer:
            #print(f"No answer from {dns_server} for {domain}")
            elapsed_times.append(-1)
        except dns.resolver.NXDOMAIN:
            #print(f"{domain} does not exist")
            elapsed_times.append(-2)
        except dns.resolver.Timeout:
            #print(f"Server {dns_server} answered The DNS operation timed out")
            elapsed_times.append(-3)
        except Exception as e:
            #print(f"An error occurred: {e}")
            elapsed_times.append(-4)
        i = i+1
    return elapsed_times

def process(resolve_times):
    tmp_array = np.array(resolve_times)
    # 使用布尔索引选择非负元素
    non_negative_indices = tmp_array >= 0
    # 计算解析成功率
    success_array = tmp_array[non_negative_indices]
    success_rate = round(len(success_array)/len(tmp_array)*100,2)  
    #print(f"Success rate of resolve:{success_rate}%")
    # 域名解析耗时取平均值
    if(len(success_array)>0):
        max_time = np.max(success_array)
        min_time = np.min(success_array)
        avg_time = np.round(np.mean(success_array),2)
        # 计算每个数据点到均值的绝对偏差
        absolute_deviations = np.abs(success_array - avg_time)
        # 计算平均差
        mean_deviation = np.round(np.mean(absolute_deviations),2)
        #print(f"Average resolving time:{avg_time}ms")
    else:
        max_time = "-"
        min_time = "-"
        avg_time = "-"
        mean_deviation = "-"
        #print("All resolving has failed.")
    return {"success_rate":success_rate,"max_time":max_time,"min_time":min_time,"avg_time":avg_time,"mean_deviation":mean_deviation}

def dns_process(domain,resolve_times):
    res = process(resolve_times)
    new_row = {"Domain":domain,
            "One":str(resolve_times[0])+"ms",
            "Two":str(resolve_times[1])+"ms",
            "Three":str(resolve_times[2])+"ms",
            "Four":str(resolve_times[3])+"ms",
            "Five":str(resolve_times[4])+"ms",
            "Six":str(resolve_times[5])+"ms",
            "Seven":str(resolve_times[6])+"ms",
            "Eight":str(resolve_times[7])+"ms",
            "Nine":str(resolve_times[8])+"ms",
            "Ten":str(resolve_times[9])+"ms",
            "Success_rate":str(res["success_rate"])+"%",
            "Max time":str(res["max_time"])+"ms",
            "Average time":str(res["avg_time"])+"ms"}
    return new_row

def summary_process(dns_server,resolve_times):
    res = process(resolve_times)
    new_row = {"DNS server": dns_server, "Success rate":str(res['success_rate'])+"%",
                "Max time":str(res["max_time"])+"ms","Min time":str(res['min_time'])+"ms","Average time":str(res["avg_time"])+"ms",
                "Mean deviation of time":res["mean_deviation"]}
    return new_row

if __name__=="__main__":
    #domains = ["www.baidu.com","www.qq.com","www.sina.com","www.taobao.com","www.bilibili.com","www.douyin.com","www.google.com","www.youtube.com"]
    #dns_servers = ["223.5.5.5","223.6.6.6","119.29.29.29","114.114.114.114","8.8.8.8","101.226.4.6","218.30.118.6"]
    with open('dns_servers.json', 'r') as file:
        dns_servers = json.load(file)
    with open('domains.json', 'r') as file:
        domains = json.load(file)
    df_all = pd.DataFrame({
        "DNS server":[],
        "Success rate":[],
        "Max time":[],
        "Min time":[],
        "Average time":[],
        "Mean deviation of time":[]
    },index=[])
    i = 0
    #df.columns = ["DNS server","Success rate","Max time","Min time","Average time","Mean deviation of time"]
    for dns_server in dns_servers:
        print(f"DNS server:{dns_server}")
        df_dns = pd.DataFrame({
            "Domain":[],
            "One":[],
            "Two":[],
            "Four":[],
            "Five":[],
            "Six":[],
            "Seven":[],
            "Eight":[],
            "Nine":[],
            "Ten":[],
            "Max time":[],
            "Average time":[],
        },index=[])
        j = 0
        resolve_times = []
        for domain in domains:
            # print(f"Domain:{domain},DNS Server:{dns_server}")
            test_result = dns_test(domain,dns_server)
            resolve_times.extend(test_result)
            df_dns.loc[j] = dns_process(domain,test_result)
            j = j+1
        print(df_dns)
        df_all.loc[i] = summary_process(dns_server,resolve_times)
        i=i+1
    print(df_all)
    print("\nHint:Mean deviation of time less is better")