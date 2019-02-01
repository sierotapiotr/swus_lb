import serverMachine
import numpy as np
import matplotlib.pyplot as plt

# CONFIGURATION
AAP = [5, 5.5, 6, 6.5, 7, 7.5, 10, 12.5, 15, 20, 25, 30, 40, 50, 75, 100, 150, 200]  # 1/LAMBDA - average arrival periods [ms]
AST = 15  # 1/MI - average service time [ms]
NUMBER_OF_PACKETS = 10000  # [packets]
NUMBER_OF_PACKETS_CONSUMED = 0
NUMBER_OF_PACKETS_DROPPED = 0
NUMBER_OF_SINGLE_THREADED_SERVERS = 1
NUMBER_OF_DOUBLE_THREADED_SERVERS = 1
NUMBER_OF_SERVERS = NUMBER_OF_SINGLE_THREADED_SERVERS + NUMBER_OF_DOUBLE_THREADED_SERVERS


# LISTS NEEDED FOR PRESENTING RESULTS
results_worktime_s1_t1 = []
results_worktime_s1_t2 = []
results_worktime_s2 = []

results_uptime = []

results_worktime_to_uptime_s1_t1 = []
results_worktime_to_uptime_s1_t2 = []
results_worktime_to_uptime_s2 = []

results_packets_consumed_s1_t1 = []
results_packets_consumed_s1_t2 = []
results_packets_consumed_s2 = []

results_loss_probability = []

aap_counter = 0

for aap_case in AAP:
    NUMBER_OF_PACKETS_CONSUMED = 0
    NUMBER_OF_PACKETS_DROPPED = 0
    # CREATE SERVERS
    servers_single_threaded = []
    servers_double_threaded = []
    for server_machine in range(NUMBER_OF_DOUBLE_THREADED_SERVERS):
        servers_double_threaded.append(serverMachine.Server(2))
    for server_machine in range(NUMBER_OF_SINGLE_THREADED_SERVERS):
        servers_single_threaded.append(serverMachine.Server(1))
    servers = servers_double_threaded + servers_single_threaded

    # ARRIVALS OF PACKETS
    arrival_time = 0  # time of packet arrival
    for i in range(NUMBER_OF_PACKETS):
        aap_time = np.random.poisson(AAP[aap_counter])  # interval between following packets
        arrival_time += aap_time

        # CHOOSING THE SERVER THAT WILL RECEIVE THE PACKET, STARTING FROM DOUBLE-THREADED
        consuming_server = -1
        for server in servers:
            counter = 0
            if server.isFree(arrival_time):
                consuming_server = counter
                pst = np.random.exponential(AST)  # packet service time
                NUMBER_OF_PACKETS_CONSUMED += 1
                if server.isDoubleThreaded():
                    server.servePacketWithDoubleThreadServer(arrival_time, pst)
                else:
                    server.servePacketWithSingleThreadServer(arrival_time, pst)
                break
            counter += 1
        if consuming_server < 0:
            NUMBER_OF_PACKETS_DROPPED += 1

    for server_number in range(NUMBER_OF_SERVERS):
        servers[server_number].uptime = max(servers[server_number].release_time_thread_1,
                                            servers[server_number].release_time_thread_2)

    results_worktime_s1_t1.append(servers[0].worktime_thread_1)
    results_worktime_s1_t2.append(servers[0].worktime_thread_2)
    results_worktime_s2.append(servers[1].worktime_thread_1)

    results_uptime.append(servers[0].uptime)

    worktime_to_uptime_ratio_s1_t1 = servers[0].worktime_thread_1 / servers[0].uptime
    worktime_to_uptime_ratio_s1_t2 = servers[0].worktime_thread_2 / servers[0].uptime
    worktime_to_uptime_ratio_s2 = servers[1].worktime_thread_1 / servers[0].uptime # yes, servers[0]

    results_worktime_to_uptime_s1_t1.append(worktime_to_uptime_ratio_s1_t1)
    results_worktime_to_uptime_s1_t2.append(worktime_to_uptime_ratio_s1_t2)
    results_worktime_to_uptime_s2.append(worktime_to_uptime_ratio_s2)

    results_packets_consumed_s1_t1.append(servers[0].packets_consumed_thread_1)
    results_packets_consumed_s1_t2.append(servers[0].packets_consumed_thread_2)
    results_packets_consumed_s2.append(servers[1].packets_consumed_thread_1)

    loss_probability = NUMBER_OF_PACKETS_DROPPED / NUMBER_OF_PACKETS
    results_loss_probability.append(loss_probability)

    aap_counter += 1


RO = []
for i in range(len(AAP)):
    RO.append(AST / AAP[i])

plt.plot(RO, results_loss_probability)
plt.title("M/M/2/1")
plt.xlabel("lambda / mi")
plt.ylabel("Probability of packet loss")
plt.show()

plt.plot(RO, results_worktime_to_uptime_s1_t1)
plt.plot(RO, results_worktime_to_uptime_s1_t2)
plt.plot(RO, results_worktime_to_uptime_s2)
plt.title("M/M/2/1")
plt.xlabel("lambda / mi")
plt.ylabel("Worktime to uptime ratio.")
plt.show()