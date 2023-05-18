#!usr/bin/python3
# -*- coding UTF-8 -*-


import socket
import os
import re


global target_ip
global target_port
global client


# Check whether the ip address is alive
def ip_scan():
    # Only check whether the single host is alive
    global target_ip
    while True:
        target_ip = input("please input your target ip(input \"quit\" to stop):")
        if target_ip == "quit":
            break
        ip_legal = r"(?:\d{1,3}\.){3}\d{1,3}"
        result = re.search(ip_legal, os.popen('ping %s' % target_ip).read())
        time_error = r"Request timed out\."
        value_error = r"^Ping request could not find host\s.*"
        error1 = re.search(time_error, os.popen('ping %s' % target_ip).read())
        error2 = re.match(value_error, os.popen('ping %s' % target_ip).read())
        if error1:
            print("timeout,dead maybe")
            break
        elif error2:
            print("maybe your target ip was wrong,check it then try again")
            break
        target_addr = result.group()
        print("your target: ", target_addr, ": alive")


# Check whether the port of the target website is open
def port_scan():
    global target_ip
    global target_port
    global client
    while True:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target_ip = input("please input your target ip(input quit to stop):")
        target_port = (input("you can specify the ports you want to scan,or you can choose default ports we prepare\
(input \"quit\" to stop)\
                           \ninput port:"))
        single_port_regex = r"\d*"
        range_port_regex = r"\d*-\d{1,3}"
        if re.match(single_port_regex, target_port) and "-" not in target_port:
            try:
                client.connect((target_ip, int(target_port)))
                print(target_port, "open")
                client.close()
            except Exception:
                print(target_port, "close")
        elif re.match(range_port_regex, target_port):
            ports_range_scan()


# Check whether ports in the range of the target website are open
def ports_range_scan():
    global target_ip
    global target_port
    global client
    while True:
        range_port_regex = r"(\d+)-(\d+)"
        start_port = int(re.search(range_port_regex, target_port).group(1))
        end_port = int(re.search(range_port_regex, target_port).group(2))
        ports_range = range(start_port, end_port+1)
        for port in ports_range:
            try:
                client.connect((target_ip, port))
                print(port, ":open")
                client.close()
            except Exception:
                print(port, ":close")
        break


def c_segment_scan():
    global target_ip
    while True:
        target_ip = input("please input your target ip(input \"quit\" to stop):")
        if target_ip == "quit":
            break
        ip_legal = r"(?:\d{1,3}\.){3}\d{1,3}"
        target_ip = socket.gethostbyname(target_ip)
        c_segment = target_ip.split(".")
        i = 1
        for A in range(1, 256):
            c_segment.append(str(i))
            i += 1
            c_segment_result = re.search(ip_legal, os.popen(f"ping {'.'.join(map(str, c_segment[0:3]+[str(c_segment[A])]))}").read())
            time_error = r"Request timed out\."
            value_error = r"^Ping request could not find host\s.*"
            error1 = re.search(time_error, os.popen(f"ping {'.'.join(map(str, c_segment[0:3]+[str(c_segment[A])]))}").read())
            error2 = re.match(value_error, os.popen(f"ping {'.'.join(map(str, c_segment[0:3]+[str(c_segment[A])]))}").read())
            c_segment_addr = c_segment_result.group()
            if error1:
                print("your target: ", c_segment_addr, ": timeout,dead maybe")
            elif error2:
                print("your target: ", c_segment_addr, ": maybe your target ip was wrong,check it then try again")
            else:
                print("your target: ", c_segment_addr, ": alive")



print("READY TO ROCK THE WORLD? \
      \n          /＞　　 フ \
　 　　\n          | 　_　 _| \
　 　 \n         ／` ミ＿xノ \
　　 \n        /　　　 　 | \
　　\n       /　 ヽ　　 ﾉ \
\n   ／￣|　　 |　|　| \
\n   | (￣ヽ＿_ヽ_)__) \
\n　  ＼二つ \
\nMAYBE NOT\n")
print("=========SHITmap=========\n"
      "=======CODE BY KILLA=====")
print("Welcome to SHITmap,here is operation manual\n \
      --ISCAN  Check whether the ip address is alive\n \
      --PSCAN  Check whether the port of the target website is open\n \
      --CSCAN  Check whether ip of the whole c segment is alive"
      )

while True:
    parameter = input("please input the parameter so that you can use its corresponding function\
(input \"quit\" to exit):")
    if parameter.startswith("--"):
        option = parameter[2:]
        if option == "ISCAN":
            ip_scan()
        elif option == "PSCAN":
            port_scan()
        elif option == "CSCAN":
            c_segment_scan()
        else:
            print("please correct your parameter and try again")
            continue
    elif parameter == "quit":
        break
    else:
        print("please correct your parameter and try again")
        continue

