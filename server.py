class Server:
    def __init__(self):
        self.state = "free"
        self.packets_consumed = 0
        self.packets_dropped = 0

    def consumePacket(self):
        self.packets_consumed += 1

    def dropPacket(self):
        self.packets_dropped += 1
        print("Packet dropped.")

"""
    def startServingPacket(self):
        self.state = "busy"

    def stopServingPacket(self):
        self.state = "free"
"""