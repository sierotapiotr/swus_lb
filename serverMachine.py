class Server:
    def __init__(self, number_of_slots):
        self.number_of_slots = number_of_slots
        self.uptime = 0  # server's uptime
        self.idletime = 0  # total time of server being idle
        self.worktime_total = 0
        self.worktime_thread_1 = 0
        self.worktime_thread_2 = 0
        self.release_time_thread_1 = 0  # moment when thread will be released
        self.release_time_thread_2 = 0
        self.packets_consumed_thread_1 = 0
        self.packets_consumed_thread_2 = 0
        self.packets_dropped = 0

    def isFree(self, arrival_time):
        if self.isDoubleThreaded() and self.release_time_thread_1 > arrival_time and self.release_time_thread_2 > arrival_time:
            return False
        elif not self.isDoubleThreaded() and self.release_time_thread_1 > arrival_time:
            return False
        else:
            return True

    def isDoubleThreaded(self):
        if self.number_of_slots == 2:
            return True
        else:
            return False

    def servePacketWithSingleThreadServer(self, arrival_time, pst):
        self.idletime += (arrival_time - self.release_time_thread_1)
        self.release_time_thread_1 = arrival_time + pst
        self.packets_consumed_thread_1 += 1
        self.worktime_thread_1 += pst
        return

    def servePacketWithDoubleThreadServer(self, arrival_time, pst):
        #  both threads free
        if arrival_time >= self.release_time_thread_1 and arrival_time >= self.release_time_thread_2:
            if self.release_time_thread_1 >= self.release_time_thread_2:
                self.idletime += (arrival_time - self.release_time_thread_1)
            else:
                self.idletime += (arrival_time - self.release_time_thread_2)
            self.release_time_thread_1 = arrival_time + pst / 2
            self.packets_consumed_thread_1 += 1
            self.worktime_thread_1 += pst / 2

        #  only 1st thread free
        elif arrival_time >= self.release_time_thread_1:
            initial_release_time_thread_1 = self.release_time_thread_1
            self.release_time_thread_1 = arrival_time + pst
            if self.release_time_thread_2 >= self.release_time_thread_1:
                self.release_time_thread_2 += (self.release_time_thread_1 - arrival_time) / 2

            else:
                self.release_time_thread_2 += (self.release_time_thread_2 - arrival_time) / 2

            if self.release_time_thread_2 >= self.release_time_thread_1:
                self.release_time_thread_2 = self.release_time_thread_2 - (
                        self.release_time_thread_2 - self.release_time_thread_1) / 2
            self.packets_consumed_thread_1 += 1
            self.worktime_thread_1 += (self.release_time_thread_1 - initial_release_time_thread_1)

        #  only 2nd thread free
        elif arrival_time >= self.release_time_thread_2:
            initial_release_time_thread_2 = self.release_time_thread_2
            self.release_time_thread_2 = arrival_time + pst

            if self.release_time_thread_1 >= self.release_time_thread_2:
                self.release_time_thread_1 += (self.release_time_thread_2 - arrival_time) / 2

            else:
                self.release_time_thread_1 += (self.release_time_thread_1 - arrival_time) / 2

            if self.release_time_thread_1 >= self.release_time_thread_2:
                self.release_time_thread_1 = self.release_time_thread_1 - (
                            self.release_time_thread_1 - self.release_time_thread_2) / 2
            else:
                self.release_time_thread_2 = self.release_time_thread_2 - (self.release_time_thread_2 - self.release_time_thread_1) / 2
            self.packets_consumed_thread_2 += 1
            self.worktime_thread_2 += (self.release_time_thread_2 - initial_release_time_thread_2)

        else:
            return False
        return True
