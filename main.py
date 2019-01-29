import loadBalancer
import ipPacket
import server
import numpy as np
import matplotlib.pyplot as plt

#AAP = [15, 20, 30, 50, 75, 100]  # 1/LAMBDA - average arrival periods [ms]
AAP = [15, 25, 35, 45, 75, 150, 300]
AST = 15  # 1/MI - average service time [ms]

# LAMBDA = 1/AAP
# MI = 1/AST

PACKETS_AMOUNT = 1000000  # [packets]
SERVER_NUMBER = 2

balancer = loadBalancer.LoadBalancer()

aap_cases = []
for i in range(len(AAP)):
    aap_cases.append(server.Server())

# CREATING PACKETS
for i in range(PACKETS_AMOUNT):
    packet = ipPacket.Packet(i)
    balancer.packet_list.append(packet)

counter = 0
server_worktime_list = []

server_uptime_worktime_ratio_list = []


for aap_case_server in aap_cases:
    arrival_time = 0  # time of packet arrival
    server_release_time = [0, 0]  # time of releasing the server
    server_idle_time = [0, 0]
    server_worktime = []
    server_worktime_uptime_ratio = []
    # M/M/1 QUEUE SIMULATION
    for i in range(PACKETS_AMOUNT):
        interval = np.random.poisson(AAP[counter])  # interval between following packets
        arrival_time += interval
        if SERVER_NUMBER > 1:
            server_number = int(round(np.random.random(SERVER_NUMBER - 1)[0]))
        else:
            server_number = 0
        if arrival_time >= server_release_time[server_number]: #dla danego serwera
            server_idle_time[server_number] += (arrival_time - server_release_time[server_number])
            aap_case_server.consumePacket()
            pst = np.random.exponential(AST)  # time of service the packet
            server_release_time[server_number] = arrival_time + pst
        else:
            aap_case_server.dropPacket()
    for server_number in range(SERVER_NUMBER):
        server_worktime.append(server_release_time[server_number] - server_idle_time[server_number])
        server_worktime_uptime_ratio.append(server_worktime[server_number]/server_release_time[server_number])
        print("Server worktime/uptime ratio: " + str(server_worktime_uptime_ratio[server_number]))
        print("Lambda/mi ratio: " + str(AST/AAP[counter]))
    server_worktime_list.append(server_worktime)
    server_uptime_worktime_ratio_list.append(server_worktime_uptime_ratio)
    counter += 1

result_consumed_packets = []
for i in range(len(aap_cases)):
    result_consumed_packets.append(aap_cases[i].packets_consumed)

result_dropped_packets = []
for i in range(len(aap_cases)):
    result_dropped_packets.append(aap_cases[i].packets_dropped)

loss_probability = []
for i in range(len(aap_cases)):
    loss_probability.append(result_dropped_packets[i]/PACKETS_AMOUNT)


RO = []
for i in range(len(aap_cases)):
    RO.append(AST/AAP[i])


"""plt.plot(RO, loss_probability)
plt.title("M/M/1/1")
plt.xlabel("lambda / mi")
plt.ylabel("Probability of packet loss")
plt.show()"""

plt.plot(RO, server_uptime_worktime_ratio_list)
plt.title("M/M/1/1")
plt.xlabel("lambda / mi")
plt.ylabel("Worktime to uptime ratio.")
plt.show()



