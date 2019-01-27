import loadBalancer
import ipPacket

balancer = loadBalancer.LoadBalancer()
stream_length = 5
packet_size = 60

# CREATING PACKETS
for i in range(stream_length):
    packet = ipPacket.Packet(i, packet_size, 2)
    balancer.packet_list.append(packet)

print(balancer.packet_list)