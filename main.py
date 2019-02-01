import loadBalancer
import ipPacket
import server
import numpy as np
import matplotlib.pyplot as plt


def servePacketWithSingleThreadServer(arrival_time, pst, idle_time, release_time):
    idle_time += (arrival_time - release_time)
    release_time = arrival_time + pst
    return [idle_time, release_time]

def servePacketWithDoubleThreadServer(arrival_time, pst, idle_time, t1_release_time, t2_release_time):
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
        return False
    return [idle_time, t1_release_time, t2_release_time]


# CONFIGURATION
AAP = [15, 25, 35, 45, 75, 150, 300]  # 1/LAMBDA - average arrival periods [ms]
AST = 15  # 1/MI - average service time [ms]
NUMBER_OF_PACKETS = 100000  # [packets]
NUMBER_OF_PACKETS_CONSUMED = 0
NUMBER_OF_PACKETS_DROPPED = 0
NUMBER_OF_SINGLE_THREADED_SERVERS = 2
NUMBER_OF_DOUBLE_THREADED_SERVERS = 1
NUMBER_OF_SERVERS = NUMBER_OF_SINGLE_THREADED_SERVERS + NUMBER_OF_DOUBLE_THREADED_SERVERS

"""balancer = loadBalancer.LoadBalancer()

# CREATING PACKETS
for i in range(NUMBER_OF_PACKETS):
    packet = ipPacket.Packet(i)
    balancer.packet_list.append(packet)"""

server_worktime_list = []
server_uptime_worktime_ratio_list = []

aap_counter = 0
for aap_case in AAP:
    # CREATE SERVERS
    servers_single_threaded = []
    servers_double_threaded = []

    for server_machine in range(NUMBER_OF_SINGLE_THREADED_SERVERS):
        servers_single_threaded.append(server.Server(1))
    for server_machine in range(NUMBER_OF_DOUBLE_THREADED_SERVERS):
        servers_double_threaded.append(server.Server(2))
    servers = servers_single_threaded + servers_double_threaded

    # FOR EACH SERVER SETTING INITIAL VALUES
    servers_release_times_thread_1 = []  # time of releasing the server
    servers_release_times_thread_2 = []
    servers_work_times = []   # time of server being in working state
    servers_idle_times = []  # time of server being in idle state
    servers_worktime_to_uptime_ratio = []  # servers' worktime to uptime ratio

    for i in range(NUMBER_OF_SERVERS):
        servers_release_times_thread_1.append(0)
        servers_release_times_thread_2.append(0)
        servers_idle_times.append(0)

    # ARRIVALS OF PACKETS
    arrival_time = 0  # time of packet arrival
    for i in range(NUMBER_OF_PACKETS):
        aap_time = np.random.poisson(AAP[aap_counter])  # interval between following packets
        arrival_time += aap_time

        current_consuming_server = -1

        # CHOOSING THE SERVER THAT WILL RECEIVE THE PACKET, STARTING FROM DOUBLE-THREADED
        for server in servers:
            counter = 0
            if server.isFree():
                server.startServingPacket()
                current_consuming_server = counter
                NUMBER_OF_PACKETS_CONSUMED += 1
                pst = np.random.exponential(AST)  # packet service time
                if server.isDoubleThreaded():
                    servePacketWithDoubleThreadServer(
                        arrival_time,
                        pst,
                        servers_idle_times[current_consuming_server],
                        servers_release_times_thread_1[current_consuming_server],
                        servers_release_times_thread_2[current_consuming_server]
                    )
                else:
                    servePacketWithSingleThreadServer(
                    arrival_time,
                    pst,
                    servers_idle_times[current_consuming_server],
                    servers_release_times_thread_1[current_consuming_server])
                break
            counter += 1
        if current_consuming_server < 0:
            NUMBER_OF_PACKETS_DROPPED += 1

    for server_number in range(NUMBER_OF_SERVERS):
        uptime = max(servers_release_times_thread_1[server_number], servers_release_times_thread_2[server_number])
        servers_work_times.append(uptime - servers_idle_times[server_number])
        servers_worktime_to_uptime_ratio.append(servers_work_times[server_number] / uptime)
        print("Server worktime/uptime ratio: " + str(servers_worktime_to_uptime_ratio[server_number]))
        print("Lambda/mi ratio: " + str(AST / AAP[aap_counter]))
    server_worktime_list.append(servers_work_times)
    server_uptime_worktime_ratio_list.append(servers_worktime_to_uptime_ratio)
    aap_counter += 1

# RESULTS
result_consumed_packets = []
for i in range(len(AAP)):
    result_consumed_packets.append(AAP[i].packets_consumed)

result_dropped_packets = []
for i in range(len(AAP)):
    result_dropped_packets.append(AAP[i].packets_dropped)

loss_probability = []
for i in range(len(AAP)):
    loss_probability.append(result_dropped_packets[i] / NUMBER_OF_PACKETS)

RO = []
for i in range(len(AAP)):
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
