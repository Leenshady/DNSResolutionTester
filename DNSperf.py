import dns.resolver
import time
import numpy as np
import pandas as pd
import json

# DNS循环10次解析同一域名并记录耗时
def dns_perf_test(domain_name,dns_server):
    elapsed_times = []
    i = 0
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_server]
    resolver.timeout = 2
    while(i<10):
        try:
            start_time = time.perf_counter()
            resolver.resolve(domain_name,"A")
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

# 统计解析成功率、最大耗时、最小耗时、平均耗时、平均差
def statistics(resolve_times):
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
        mean_time = np.round(np.mean(success_array),2)
        # 计算每个数据点到均值的绝对偏差
        absolute_deviations = np.abs(success_array - mean_time)
        # 计算平均差
        mean_deviation = np.round(np.mean(absolute_deviations),2)
        #print(f"Average resolving time:{mean_time}ms")
    else:
        max_time = "-"
        min_time = "-"
        mean_time = "-"
        mean_deviation = "-"
        #print("All resolving has failed.")
    return {"success_rate":success_rate,"max_time":max_time,"min_time":min_time,"mean_time":mean_time,"mean_deviation":mean_deviation}

# DNS单次测试数据转换成DataFrame行
def single_data_to_row(domain_name,resolve_times):
    res = statistics(resolve_times)
    new_row = {"Domain":domain_name,
            "Test1":str(resolve_times[0])+"ms",
            "Test2":str(resolve_times[1])+"ms",
            "Test3":str(resolve_times[2])+"ms",
            "Test4":str(resolve_times[3])+"ms",
            "Test5":str(resolve_times[4])+"ms",
            "Test6":str(resolve_times[5])+"ms",
            "Test7":str(resolve_times[6])+"ms",
            "Test8":str(resolve_times[7])+"ms",
            "Test9":str(resolve_times[8])+"ms",
            "Test10":str(resolve_times[9])+"ms",
            "Success_rate":str(res["success_rate"])+"%",
            "Max time":str(res["max_time"])+"ms",
            "Average time":str(res["mean_time"])+"ms"}
    return new_row

# DNS整体测试数据转换成DataFrame行
def overall_data_to_row(dns_server,resolve_times):
    res = statistics(resolve_times)
    new_row = {"DNS server": dns_server, "Success rate":str(res['success_rate'])+"%",
                "Max time":str(res["max_time"])+"ms","Min time":str(res['min_time'])+"ms","Average time":str(res["mean_time"])+"ms",
                "Mean deviation of time":res["mean_deviation"]}
    return new_row

if __name__=="__main__":
    with open('dns_servers.json', 'r') as file:
        dns_servers = json.load(file)
    with open('domain_names.json', 'r') as file:
        domain_names = json.load(file)
    df_overall_perf = pd.DataFrame({
        "DNS server":[],
        "Success rate":[],
        "Max time":[],
        "Min time":[],
        "Average time":[],
        "Mean deviation of time":[]
    },index=[])
    i = 0
    for dns_server in dns_servers:
        print(f"DNS server:{dns_server}")
        df_single_perf = pd.DataFrame({
            "Domain":[],
            "Test1":[],
            "Test2":[],
            "Test3":[],
            "Test4":[],
            "Test5":[],
            "Test7":[],
            "Test8":[],
            "Test9":[],
            "Test10":[],
            "Max time":[],
            "Average time":[],
        },index=[])
        j = 0
        resolve_times = []
        for domain_name in domain_names:
            test_result = dns_perf_test(domain_name,dns_server)
            resolve_times.extend(test_result)
            df_single_perf.loc[j] = single_data_to_row(domain_name,test_result)
            j = j+1
        print(df_single_perf)
        print("----------------")
        df_overall_perf.loc[i] = overall_data_to_row(dns_server,resolve_times)
        i=i+1
    print(df_overall_perf)
    print("\nTips:Mean deviation of time less is better.")