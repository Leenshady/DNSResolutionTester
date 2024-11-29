import sys
import argparse
import platform
import dns.resolver
import dns.message
import requests
import time
import numpy as np
import pandas as pd
import json
import logging
import traceback

# 设置常量
TYPE_DNS = "DNS"
TYPE_DOH = "DoH"

# 长度控制
def len_control(num):
    # 超过三位数直接输出整数，三位数保留一位小数，否则保留两位小数
    if(num>1000):
        return int(num)
    elif(num>100):
        return round(num,1)
    else:
        return round(num,2)

# DNS循环10次解析同一域名并记录耗时
def DNS_perf_test(domain_name,DNS_server,type):
    # 解析耗时
    elapsed_times = []
    # 解析是否成功标记
    isSuccess = False
    i = 0
    # 判断是DNS还是DoH
    if(type == TYPE_DNS):
        resolver = dns.resolver.Resolver()
        # 设置DNS服务器
        resolver.nameservers = [DNS_server]
        # 设置超时时间为2秒
        resolver.timeout = 2
    elif(type == TYPE_DOH):
        # DNS解析类型
        rr = dns.rdatatype.A
        # 使用dnspython库生成dns查询message
        message = dns.message.make_query(qname=domain_name, rdtype=rr)
        # 将message压缩转换成含有包含DNS信息的字节码
        dns_req = message.to_wire()
        # 根据DoH服务器的要求设置正确的Content-Type
        headers = {
            'Content-Type': 'application/dns-message'
        }
    while(i<10):
        try:
            
            if(type == TYPE_DNS):
                # 开始计时
                start_time = time.perf_counter()
                answers = resolver.resolve(domain_name,"A")
                # 结束计时
                end_time = time.perf_counter()
                if answers:
                    isSuccess = True
            elif(type == TYPE_DOH):
                # 开始计时
                start_time = time.perf_counter()
                # 发送POST请求
                response = requests.post(DNS_server,headers=headers,data=dns_req)
                # 结束计时
                end_time = time.perf_counter()
                if(response.status_code == 200):
                    # 检查响应体是否包含answer
                    if dns.message.from_wire(response.content).answer:
                        isSuccess = True
            # 检查解析是否成功
            if isSuccess:
                elapsed_time = end_time - start_time
                elapsed_time= elapsed_time * 1000
                elapsed_times.append(len_control(elapsed_time))
            else:
                elapsed_times.append(-4)
        except dns.resolver.NoAnswer:
            logging.error(f"No answer from {DNS_server} for {domain_name}")
            elapsed_times.append(-1)
        except dns.resolver.NXDOMAIN:
            logging.error(f"{domain_name} does not exist")
            elapsed_times.append(-2)
        except dns.resolver.Timeout:
            logging.error(f"Server {DNS_server} answered The DNS operation timed out")
            elapsed_times.append(-3)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            print("An error occurred, please check error.log.")
            elapsed_times.append(-4)
        i = i+1
    return elapsed_times

# 循环测试所有DNS
def overall_perf_test(df_overall_perf,DNS_servers,domain_names,type,index):
    i = index
    for DNS_server in DNS_servers:
        print_or_log(log_file,f"DNS server:{DNS_server['name']}[{DNS_server['addr']}]")
        df_single_perf = pd.DataFrame({
            "Domain name":[],
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
            test_result = DNS_perf_test(domain_name,DNS_server['addr'],type)
            # 输出进度条
            sys.stdout.write(f"{DNS_server['name']}[{DNS_server['addr']}] testing progress: {round((j+1)/len(domain_names)*100,2)} %  \r")
            # 确保输出被立即显示
            sys.stdout.flush()
            resolve_times.extend(test_result)
            df_single_perf.loc[j] = single_data_to_row(domain_name,test_result)
            j = j+1
        print_or_log(log_file,df_single_perf)
        print_or_log(log_file,"----------------\n")
        DNS_server_title = DNS_server['name'] + '[' + DNS_server['addr'] + ']'
        df_overall_perf.loc[i] = overall_data_to_row(DNS_server_title, resolve_times)
        i=i+1
    return i
        
# 统计解析成功率、最大耗时、最小耗时、平均耗时、平均差
def statistics(resolve_times):
    tmp_array = np.array(resolve_times)
    # 使用布尔索引选择非负元素
    non_negative_indices = tmp_array >= 0
    # 计算解析成功率
    success_array = tmp_array[non_negative_indices]
    success_rate = round(len(success_array)/len(tmp_array)*100,2)  
    # 域名解析耗时取平均值
    if(len(success_array)>0):
        max_time = len_control(np.max(success_array))
        min_time = len_control(np.min(success_array))
        mean_time = len_control(np.round(np.mean(success_array),2))
        # 计算每个数据点到均值的绝对偏差
        absolute_deviations = np.abs(success_array - mean_time)
        # 计算平均差
        mean_deviation = len_control(np.mean(absolute_deviations))
    else:
        max_time = "-"
        min_time = "-"
        mean_time = "-"
        mean_deviation = "9999"
    return {"success_rate":success_rate,"max_time":max_time,"min_time":min_time,"mean_time":mean_time,"mean_deviation":mean_deviation}

# DNS单次测试数据转换成DataFrame行
def single_data_to_row(domain_name,resolve_times):
    res = statistics(resolve_times)
    new_row = {"Domain name":domain_name,
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
def overall_data_to_row(DNS_server,resolve_times):
    res = statistics(resolve_times)
    new_row = {"DNS server": DNS_server,
               "Success rate":str(res['success_rate'])+"%",
                "Max time":str(res["max_time"])+"ms",
                "Min time":str(res['min_time'])+"ms",
                "Average time":str(res["mean_time"])+"ms",
                "Mean deviation of time":res["mean_deviation"]}
    return new_row

#根据log_file判断是输出到文件还是命令行
def print_or_log(log_file,content,sep:str|None=None):
    if log_file:
        if isinstance(content,pd.DataFrame):
            log_file.write("\r\n")
            log_file.write(content.to_csv(index=False,header=True,sep=sep if sep else '\t',encoding='utf-8'))
        else:
            log_file.write(content)
    else:
        print(content)

if __name__=="__main__":
    system_name = platform.system()
    logging.basicConfig(filename='error.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
    # 设置命令行参数
    parser = argparse.ArgumentParser(description="DNSperf is a DNS server performance tester that can help you choose the most suitable DNS for your local network.")
    # --log参数可以把结果输出到指定文件
    parser.add_argument("-l","--log", type=str,default=None, help="Example: -l Result")
    args = parser.parse_args()
    log_file = None
    if args.log is not None:
        log_file = open(args.log+".log","w", encoding='utf-8')
    DNS_servers = []
    DoH_servers = []
    domain_names = []
    try:
        with open('dns_servers.json', 'r', encoding='utf-8') as file:
            servers_data = json.load(file)
            DNS_servers = servers_data["DNS"]
            DoH_servers = servers_data["DoH"]
        with open('domain_names.json', 'r') as file:
            domain_names = json.load(file)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print("An error occurred, please check error.log.")
        input("Press Enter to continue...")
    df_overall_perf = pd.DataFrame({
        "DNS server":[],
        "Success rate":[],
        "Max time":[],
        "Min time":[],
        "Average time":[],
        "Mean deviation of time":[]
    },index=[])
    index = 0
    # 设置列名与值对齐
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)
    # 不换行显示
    pd.set_option('display.width', 1000)
    # 测试DNS
    index = overall_perf_test(df_overall_perf,DNS_servers,domain_names,TYPE_DNS,index)
    # 测试DoH
    overall_perf_test(df_overall_perf,DoH_servers,domain_names,TYPE_DOH,index)
    # 按照Mean deviation of time从小到大排序
    df_overall_perf = df_overall_perf.sort_values(by='Mean deviation of time', ascending=True)
    print_or_log(log_file,df_overall_perf,"|")
    print_or_log(log_file,"\nTips:Mean deviation of time less is better.")
    print_or_log(log_file,"\nIf the time is negative, please refer to here or check error.log.\n-1ms : NoAnswer.\n-2ms : NXDOMAIN.\n-3ms : Timeout.\n-4ms : other error.")
    # 输出到文件时，完成提示
    if args.log is not None:
        print(f"Test completed.Please check {args.log+".log"}.")
    if system_name != 'Linux':
        input("Press Enter to continue...")