import loadBalancer
import ipPacket
import server
import numpy as np

LAMBDA = 1  # average arrival rate [packets/s]
MI = 5  # average service rate [packets/s]
PACKETS_AMOUNT = 200  # [packets]

balancer = loadBalancer.LoadBalancer()
server = server.Server()

# CREATING PACKETS
for i in range(PACKETS_AMOUNT):
    packet = ipPacket.Packet(i)
    balancer.packet_list.append(packet)

arrival_time = 0  # time of packet arrival
server_release_time = 0  # time of releasing the server

# M/M/1 QUEUE SIMULATION
for i in range(PACKETS_AMOUNT):
    interval = np.random.poisson(1000 / LAMBDA)  # interval between following packets
    arrival_time += interval
    if arrival_time >= server_release_time:
        server.consumePacket()
        pst = np.random.exponential(1000 / MI)
        server_release_time = arrival_time + pst
    else:
        server.dropPacket()

print("Packets consumed: " + str(server.packets_consumed))
print("Packets dropped: " + str(server.packets_dropped))