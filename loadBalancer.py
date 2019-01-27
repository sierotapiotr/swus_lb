class LoadBalancer:
    def __init__(self):
        self.packet_list = []
        self.packets_passed = 0
        self.packets_dropped = 0

    def sendPacketToServer(self, packet_id):
        self.packets_passed += 1
        self.packet_list[packet_id].pop()

    def dropPacket(self, packet_id):
        self.packets_dropped += 1
        self.packet_list[packet_id].pop()