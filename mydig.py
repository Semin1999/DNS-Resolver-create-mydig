import sys, dns, time, dns.query
from datetime import datetime

root_servers = ["198.41.0.4", "199.9.14.201", "192.33.4.12",  # Dns root server
                "199.7.91.13", "192.203.230.10", "192.5.5.241",
                "192.112.36.4", "198.97.190.53", "192.36.148.17",
                "192.58.128.30", "193.0.14.129", "199.7.83.42",
                "202.12.27.33"]

domain_name = str(sys.argv[1]).strip()  # Make args for domain

question_flag = True  # question_flag


def resolve_dns(domain_name, server_ip):  # initialize def
    global question_flag  # make question_flag as global variable
    request = dns.message.make_query(domain_name, "A")  # query for "A" record
    if question_flag:  # answer section writing with first domain
        domain_split_1 = str(request.question[0]).split()[0]  # split for formally writing
        domain_split_2 = str(request.question[0]).split()[1]  # split for formally writing
        domain_split_3 = str(request.question[0]).split()[2]  # split for formally writing
        output_file.write(  # write in file
            domain_split_1 + "\t\t" + domain_split_2 + "\t" + domain_split_3 + "\n\n"
        )
        output_file.write(";; ANSWER SECTION:\n")  # write "answer section"
        question_flag = False
    response = dns.query.udp(request, server_ip, timeout=3)  # get response with query
    while len(response.answer) == 0:  # check answer is empty, if not, iterate all
        if len(response.additional) != 0:  # if we have additional section
            for n in range(len(response.additional)):
                if response.additional[n].rdtype == 1:  # check if it's type A
                    ip_add = str(response.additional[n].items).split()[4]  # get ip address
                    ip_add = ip_add[:-2]  # get clear ip address
                    response = dns.query.udp(request, ip_add, timeout = 3)  # get response from next ip
                    break
        elif len(response.authority) != 0:  # if empty additional section but there's authority section
            for n in range(len(response.authority)):
                if response.authority[n].rdtype == 2:  # check is this type NS
                    next_domain = str(response.authority[n].items).split()[4]  # get clear server ip
                    next_domain = next_domain[:-2]  # get clear server ip
                    server_ip = str(resolve_dns(next_domain, server_ip)).split()[4]  # get server ip
                    return resolve_dns(domain_name, server_ip)  # recursive call server ip
    if response.answer[0].rdtype == 5:  # check is this type Cname
        return resolve_dns(str(response.answer[0]).split()[4], server_ip)  # recursive call with Cname
    else:
        return response.answer[0]  # return final answer    # return final answer


output_file = open("mydig_output.txt", "w")  # write file open
output_file.write(";; QUESTION SECTION:\n")  # write file
server = ""
start_time = time.time()  # time that we start
for i in range(len(root_servers)):
    try:
        server = root_servers[i]
        answer = resolve_dns(domain_name, root_servers[i])
        break
    except Exception as e:
        if i == len(root_servers) - 1:  # error handling
            output_file.write("Error Occurred")
            output_file.close()
            sys.exit()
        else:
            print("Error Occurred: ")
            print(e)
            sys.exit()

output_file.write(domain_name + " \t" + " " + str(answer).split(" ", 1)[1] + "\n")  # write answer section
end_time = time.time()  # end time
output_file.write(
    "\n" + ";; Query time: " + str(int(1000 * (end_time - start_time))) + " msec" + "\n")  # write query time
output_file.write(";; WHEN: " + datetime.now().strftime('%A %B %d %H:%M:%S %Y\n'))  # write time
output_file.close()  # close file
print("success to create file")  # success message
sys.exit()
