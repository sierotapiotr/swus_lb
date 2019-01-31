class Server:
    def __init__(self, number_of_slots):
        self.number_of_slots = number_of_slots
        self.freeSlots = number_of_slots
        self.packets_consumed = 0
        self.packets_dropped = 0

    def consumePacket(self):
        self.packets_consumed += 1

    def dropPacket(self):
        self.packets_dropped += 1
        print("Packet dropped.")

    def startServingPacket(self):
        if self.freeSlots >= 1:
            self.freeSlots -= 1
            self.consumePacket()
        else:
            self.dropPacket()

    def stopServingPacket(self):
        self.freeSlots += 1