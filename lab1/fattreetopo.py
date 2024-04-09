from mininet.topo import Topo

class FatTreeTopo(Topo):
    def build(self, k=4):
        self.k = k
        self.pods = k
        self.core_switches = (k//2) ** 2
        self.aggr_switches = self.pods * (k//2)
        self.edge_switches = self.aggr_switches
        self.hosts_per_pod = (k//2) ** 2

        self.construct_topology()

    def construct_topology(self):
        self.add_core_switches()
        self.add_aggregation_switches()
        self.add_edge_switches()
        self.add_hosts()
        self.add_links()

    def add_core_switches(self):
        for switch in range(self.core_switches):
            self.addSwitch("c{}".format(switch + 1), stp=True, failMode='standalone')

    def add_aggregation_switches(self):
        for pod in range(self.pods):
            for switch in range(self.k//2):
                self.addSwitch("a{}{}".format(pod + 1, switch + 1), stp=True, failMode='standalone')

    def add_edge_switches(self):
        for pod in range(self.pods):
            for switch in range(self.k//2):
                self.addSwitch("e{}{}".format(pod + 1, switch + 1), stp=True, failMode='standalone')

    def add_hosts(self):
        for pod in range(self.pods):
            for switch in range(self.k//2):
                for host in range(self.k//2):
                    self.addHost("h{}{}{}".format(pod + 1, switch + 1, host + 1))

    def add_links(self):
        for pod in range(self.pods):
            for switch in range(self.k//2):
                # Connect edge switches to hosts
                for host in range(self.k//2):
                    self.addLink("e{}{}".format(pod + 1, switch + 1),
                                 "h{}{}{}".format(pod + 1, switch + 1, host + 1))
                
                # Connect edge switches to aggregation switches
                for aggr in range(self.k//2):
                    self.addLink("e{}{}".format(pod + 1, switch + 1),
                                 "a{}{}".format(pod + 1, aggr + 1))

            # Connect aggregation switches to core switches
            for aggr in range(self.k//2):
                for core in range(self.k//2):
                    self.addLink("a{}{}".format(pod + 1, aggr + 1),
                                 "c{}".format(core + aggr * (self.k//2)  + 1))

topos = { 'fattreetopo': ( lambda: FatTreeTopo() ) }

