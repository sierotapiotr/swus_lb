class Server:
    def __init__(self, number_of_slots):
        self.number_of_slots = number_of_slots
        self.free_slots = number_of_slots
        self.release_time_thread_1 = 0
        self.release_time_thread_2 = 0
        self.packets_consumed = 0
        self.packets_dropped = 0


    def startServingPacket(self):
        self.free_slots -= 1

    def stopServingPacket(self):
        self.free_slots += 1

    def isFree(self):
        if self.free_slots > 0:
            return True
        else:
            return False

    def isDoubleThreaded(self):
        if self.number_of_slots == 2:
            return True
        else:
            return False