import loadBalancer
import ipPacket
import server
import numpy as np
import matplotlib.pyplot as plt


def servePacketWithDoubleThreadServer(server, pst, idle_time, t1_release_time, t2_release_time):
    #  both threads free
    if arrival_time >= t1_release_time and arrival_time >= t2_release_time:
        if t1_release_time >= t2_release_time:
            idle_time += (arrival_time - t1_release_time)
        else:
            idle_time += (arrival_time - t2_release_time)
        t1_release_time = arrival_time + pst

    #  only 1st thread free
    elif arrival_time >= t1_release_time:
        t1_release_time = arrival_time + pst
        t2_release_time += (t2_release_time - arrival_time)  # sprawdzic czy zgadzaja sie formaty liczb +
        if t1_release_time >= t2_release_time:
            t1_release_time = t1_release_time - (t1_release_time - t2_release_time)
        else:
            t2_release_time = t2_release_time - (t2_release_time - t1_release_time)

    #  only 2nd thread free
    elif arrival_time >= t2_release_time:
        t2_release_time = arrival_time + pst
        t1_release_time = (t1_release_time - arrival_time) / 2  # sprawdzic czy zgadzaja sie formaty liczb +
        if t1_release_time >= t2_release_time:
            t1_release_time = t1_release_time - (t1_release_time - t2_release_time)
        else:
            t2_release_time = t2_release_time - (t2_release_time - t1_release_time)
    else:
        server.dropPacket()

    return [idle_time, t1_release_time, t2_release_time]


# CONFIGURATION
AAP = [15, 25, 35, 45, 75, 150, 300]  # 1/LAMBDA - average arrival periods [ms]
AST = 15  # 1/MI - average service time [ms]
NUMBER_OF_PACKETS = 100000  # [packets]
NUMBER_OF_SERVERS = 2

balancer = loadBalancer.LoadBalancer()
aap_cases = []


for i in range(len(AAP)):
    aap_cases.append(server.Server())

# CREATING PACKETS
for i in range(NUMBER_OF_PACKETS):
    packet = ipPacket.Packet(i)
    balancer.packet_list.append(packet)

aap_counter = 0
server_worktime_list = []
server_uptime_worktime_ratio_list = []

for aap_case_server in aap_cases:

    # FOR EACH SERVER SETTING INITIAL VALUES
    servers_release_times = []  # time of releasing the server
    servers_work_times = []   # time of server being in working state
    servers_idle_times = []  # time of server being in idle state
    servers_worktime_to_uptime_ratio = []  # servers' worktime to uptime ratio
    for i in range(NUMBER_OF_SERVERS):
        servers_release_times.append(0)
        servers_idle_times.append(0)

    # ARRIVALS OF PACKETS
    arrival_time = 0  # time of packet arrival
    for i in range(NUMBER_OF_PACKETS):
        aap_time = np.random.poisson(AAP[aap_counter])  # interval between following packets
        arrival_time += aap_time

        # CHOOSING THE SERVER THAT WILL RECEIVE THE PACKET
        if NUMBER_OF_SERVERS > 1:
            server_number = int(round(np.random.random(NUMBER_OF_SERVERS - 1)[0]))
        else:
            server_number = 0

        if arrival_time >= servers_release_times[server_number]:  # dla danego serwera
            servers_idle_times[server_number] += (arrival_time - servers_release_times[server_number])
            aap_case_server.consumePacket()
            pst = np.random.exponential(AST)  # packet service time
            servers_release_times[server_number] = arrival_time + pst
        else:
            aap_case_server.dropPacket()
    for server_number in range(NUMBER_OF_SERVERS):
        servers_work_times.append(servers_release_times[server_number] - servers_idle_times[server_number])
        servers_worktime_to_uptime_ratio.append(servers_work_times[server_number] / servers_release_times[server_number])
        print("Server worktime/uptime ratio: " + str(servers_worktime_to_uptime_ratio[server_number]))
        print("Lambda/mi ratio: " + str(AST / AAP[aap_counter]))
    server_worktime_list.append(servers_work_times)
    server_uptime_worktime_ratio_list.append(servers_worktime_to_uptime_ratio)
    aap_counter += 1

# RESULTS
result_consumed_packets = []
for i in range(len(aap_cases)):
    result_consumed_packets.append(aap_cases[i].packets_consumed)

result_dropped_packets = []
for i in range(len(aap_cases)):
    result_dropped_packets.append(aap_cases[i].packets_dropped)

loss_probability = []
for i in range(len(aap_cases)):
    loss_probability.append(result_dropped_packets[i] / NUMBER_OF_PACKETS)

RO = []
for i in range(len(aap_cases)):
    RO.append(AST / AAP[i])

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
