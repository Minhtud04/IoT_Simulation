import random
class Node():
    def __init__(self, x,y, freqSent, freqRecv):
        self.x, self.y = x,y
        self.comLog: List[(int, int)] = []          #record the communication log of the node monitored by this node
        self.monitor = None                         #the node that this node monitor
        self.monitoredBy = None                     #the node that monitor this node

        self.freqSent = freqSent
        self.freqRecv = freqRecv

        # self.thresHoldSendRecv = THRESHOLD

    def sendRecvFreqPerSec(self):
        #normal distribution of (0,5) for freqSent and freqRecv
        freqSent = max(0, self.freqSent + random.randint(-5,5))
        freqRecv = max(0, self.freqRecv + random.randint(-5,5))
        return freqSent, freqRecv

    def recordComLog(self, freqSent, freqRecv):
        self.comLog.append((freqSent, freqRecv))

    def __str__(self):
        info = f"Position: ({self.x}, {self.y}), sendRecvFreq: ({self.freqSent}, {self.freqRecv})"
        return info
class NodeCluster():
    THRESHOLD = 30
    NOR_BEHAVIOR_SEND_RANGE = (10,20)
    NOR_BEHAVIOR_RECV_RANGE = (15,25)
    MAL_BEHAVIOR_SEND_RANGE = (20,30)
    MAL_BEHAVIOR_RECV_RANGE = (25,35)

    def __init__(self, normalNodes:int, maliciousNodes:int):            #Create NodeCluster from thinAir
        self.nodes = []
        self.n = normalNodes + maliciousNodes
        self.createNodeList(normalNodes)
        self.injectMaliciousNode(maliciousNodes)
        self.assignMonitor()

    #If we have a list of cluster position first - we could use that position List to continue instead
    def createNodeList(self, n):
        for i in range(n):
            x = random.randint(0, 100)
            y = random.randint(0, 100)
            freqSent = random.randint(self.NOR_BEHAVIOR_SEND_RANGE[0], self.NOR_BEHAVIOR_SEND_RANGE[1])
            freqRecv = random.randint(self.NOR_BEHAVIOR_RECV_RANGE[0], self.NOR_BEHAVIOR_RECV_RANGE[1])
            self.nodes.append(Node(x,y, freqSent, freqRecv))

    def injectMaliciousNode(self, n):           #Insert n malicious nodes
        for i in range(n):
            x = random.randint(0, 100)
            y = random.randint(0, 100)
            freqSent = random.randint(self.MAL_BEHAVIOR_SEND_RANGE[0], self.MAL_BEHAVIOR_SEND_RANGE[1])
            freqRecv = random.randint(self.MAL_BEHAVIOR_RECV_RANGE[0], self.MAL_BEHAVIOR_RECV_RANGE[1])
            self.nodes.append(Node(x,y, freqSent, freqRecv))
        random.shuffle(self.nodes)

    def monitorNodeAssigned(self, mainNode, monitoredNode):
        mainNode.monitor = monitoredNode
        monitoredNode.monitoredBy = mainNode
    def assignMonitor(self):        #simple setUp: node[i] will monitor node[i+1] and be monitored by node[i-1]
        for i in range(self.n):
            self.monitorNodeAssigned(self.nodes[i], self.nodes[(i+1)%self.n])

    # Simulation process might be like this:
    # Do a loop of 10 times, each loop will consider like a second
    # In each loop, each node will send n messages and receive m messages
    # They will send (n, m) to their monitor -> monitor will record it inside comLog

    def simulate(self, times):
        for i in range(times):
            for node in self.nodes:
                freqSent, freqRecv = node.sendRecvFreqPerSec()
                monitorNode = node.monitoredBy
                if monitorNode:
                     monitorNode.recordComLog(freqSent, freqRecv)        #Send the freqSent and freqRecv to the monitor

        for node in self.nodes:
            print(str(node))
            print(node.comLog)


#run:


if __name__ == '__main__':
    nodeCluster = NodeCluster(5, 2)         #5 normal nodes, 2 malicious nodes
    nodeCluster.simulate(10)                #simulate 10 seconds - 10 times loop
