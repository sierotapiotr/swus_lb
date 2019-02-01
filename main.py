import loadBalancer
import ipPacket
import serverMachine
import numpy as np
import matplotlib.pyplot as plt

# CONFIGURATION
AAP = [2]  # 1/LAMBDA - average arrival periods [ms]
AST = 35  # 1/MI - average service time [ms]
NUMBER_OF_PACKETS = 100000  # [packets]
NUMBER_OF_PACKETS_CONSUMED = 0
NUMBER_OF_PACKETS_DROPPED = 0
NUMBER_OF_SINGLE_THREADED_SERVERS = 1
NUMBER_OF_DOUBLE_THREADED_SERVERS = 1
NUMBER_OF_SERVERS = NUMBER_OF_SINGLE_THREADED_SERVERS + NUMBER_OF_DOUBLE_THREADED_SERVERS

"""balancer = loadBalancer.LoadBalancer()

# CREATING PACKETS
for i in range(NUMBER_OF_PACKETS):
    packet = ipPacket.Packet(i)
    balancer.packet_list.append(packet)"""

# LISTS NEEDED FOR PRESENTING RESULTS
server_worktime_list = []
server_uptime_list = []
server_uptime_worktime_ratio_list = []

aap_counter = 0
for aap_case in AAP:
    # CREATE SERVERS
    servers_single_threaded = []
    servers_double_threaded = []
    for server_machine in range(NUMBER_OF_DOUBLE_THREADED_SERVERS):
        servers_double_threaded.append(serverMachine.Server(2))
    for server_machine in range(NUMBER_OF_SINGLE_THREADED_SERVERS):
        servers_single_threaded.append(serverMachine.Server(1))
    servers = servers_double_threaded + servers_single_threaded

    # FOR EACH SERVER SETTING INITIAL VALUES
    """servers_release_times_thread_1 = []  # time of releasing the server
    servers_release_times_thread_2 = []
    servers_work_times = []  # time of server being in working state
    servers_idle_times = []  # time of server being in idle state
    servers_worktime_to_uptime_ratio = []  # servers' worktime to uptime ratio

    for i in range(NUMBER_OF_SERVERS):
        servers_release_times_thread_1.append(0)
        servers_release_times_thread_2.append(0)
        servers_idle_times.append(0)"""

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

    print("Finished")
    """for server_number in range(NUMBER_OF_SERVERS):
        servers[server_number].uptime = max(servers[server_number].release_time_thread_1,
                                            servers[server_number].release_time_thread_2)
        servers[server_number].worktime_thread_1 = uptime - servers_idle_times[server_number])
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

        plt.plot(RO, loss_probability)
        plt.title("M/M/1/1")
        plt.xlabel("lambda / mi")
        plt.ylabel("Probability of packet loss")
        plt.show()

        plt.plot(RO, server_uptime_worktime_ratio_list)
        plt.title("M/M/1/1")
        plt.xlabel("lambda / mi")
        plt.ylabel("Worktime to uptime ratio.")
        plt.show()"""
