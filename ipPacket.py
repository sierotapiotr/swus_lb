class Packet:
    def __init__(self, id, size, time_reaching_lb):
        self.id = id
        self.size = size
        self.reach_lb_time = time_reaching_lb # time of reaching the load balancer

    def reachServer(self, link_capacity):
        lb_to_server_time = self.size / link_capacity
        self.reach_server_time = self.reach_lb_time + lb_to_server_time