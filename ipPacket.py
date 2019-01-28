class Packet:
    def __init__(self, id):
        self.id = id
        self.reach_lb_time = 1 #time_reaching_lb # time of reaching the load balancer

    def reachServer(self):
        self.reach_server_time = self.reach_lb_time