import random

from node_cluster import NodeCluster

class Node():
    def __init__(self, x,y, freqSent, freqRecv):
        self.x, self.y = x,y
        self.comLog: list[(int, int)] = []          # Record the communication log of the node monitored by this node
        self.monitor = None                         # Rhe node that this node monitor
        self.monitoredBy = None                     # the node that monitor this node

        self.freqSent = freqSent
        self.freqRecv = freqRecv

        self.defaultEnergy = 1

        # self.thresHoldSendRecv = THRESHOLD

    def sendRecvFreqPerSec(self):
        # Uniform distribution of (0,5) for freqSent and freqRecv
        freqSent = max(0, self.freqSent + random.randint(-5,5))
        freqRecv = max(0, self.freqRecv + random.randint(-5,5))
        return freqSent, freqRecv

    def recordComLog(self, freqSent, freqRecv):
        self.comLog.append((freqSent, freqRecv))

    def __str__(self):
        info = f"Position: ({self.x}, {self.y}), sendRecvFreq: ({self.freqSent}, {self.freqRecv})"
        return info


#run:


if __name__ == '__main__':
    nodeCluster = NodeCluster(5, 2)         #5 normal nodes, 2 malicious nodes
    nodeCluster.simulate(10)                #simulate 10 seconds - 10 times loop
