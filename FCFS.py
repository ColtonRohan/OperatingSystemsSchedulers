from cgitb import small
import copy

# please make sure and have a data.txt file with the 8 processes inside the same directiory as this file

def main():
    #Setup
    pList = []
    p1List = []
    p2List = []
    p3List = []
    p4List = []
    p5List = []
    p6List = []
    p7List = []
    p8List = []
    pList.append(p1List)
    pList.append(p2List)
    pList.append(p3List)
    pList.append(p4List)
    pList.append(p5List)
    pList.append(p6List)
    pList.append(p7List)
    pList.append(p8List)
    readyQueue = []
    isTouched = {
        0: False,
        1: False,
        2: False,
        3: False,
        4: False,
        5: False,
        6: False,
        7: False
    }
    isDone = {
        0: False,
        1: False,
        2: False,
        3: False,
        4: False,
        5: False,
        6: False,
        7: False
    }
    pProcessTotalTime={
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0
    }
    pWaitingTime = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0
    }
    # this value will subtrack each cpu burstfrom each io time once one or more are below 0 and above -100, we then place the next cpu burst into the readyQueue
    ioQueue = [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        []
    ]

    pTurnaroundTime = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0
    }

    pResponseTime = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0
    }
    
    with open("data.txt", "r") as f:
        lines = [line for line in f]
        for x in range(0, len(lines)):
            lines[x] = lines[x].split(", ")
            lines[x][-1] = lines[x][-1].rstrip('\n')
            for c in lines[x]:
                pList[x].append(int(c))
    
    totalDownTime=0

    #used for calculating wait time
    for x in range(0,8):
        pProcessTotalTime[x]=sum(pList[x])

    readyQueue.append([pList[0][0], 0])
    pList[0].pop(0)
    readyQueue.append([pList[1][0], 1])
    pList[1].pop(0)
    readyQueue.append([pList[2][0], 2])
    pList[2].pop(0)
    readyQueue.append([pList[3][0], 3])
    pList[3].pop(0)
    readyQueue.append([pList[4][0], 4])
    pList[4].pop(0)
    readyQueue.append([pList[5][0], 5])
    pList[5].pop(0)
    readyQueue.append([pList[6][0], 6])
    pList[6].pop(0)
    readyQueue.append([pList[7][0], 7])
    pList[7].pop(0)

    def isNotEmpty(input):
        for x in range(0,8):
            if input[x]!=[]:
                return True
        return False

    totalTimer=0
    tLeft=30
    cpuTimer=0
    #end of setup
    while readyQueue:
        #current CPU burst to calculate
        currentBurst = readyQueue.pop(0)
        totalTimer=totalTimer+currentBurst[0]
        cpuTimer=cpuTimer+currentBurst[0]

        for x in range(0,8):
            #calculate wait times
            #calculate Response time
            if not isTouched[currentBurst[1]]:
                isTouched[currentBurst[1]]=True
            elif not isTouched[x]:
                pResponseTime[x]=pResponseTime[x]+currentBurst[0]
            if ioQueue[x] != []:
                #if there is something in the IOQueue, subtract time from it
                ioQueue[x][0][0]=ioQueue[x][0][0]-int(currentBurst[0])
                #if it is done take it out and add the next cpuburst to the readyqueue
                if ioQueue[x][0][0]<=0:
                    ioQueue[x].pop(0)
                    readyQueue.append((pList[x][0],x))
                    pList[x].pop(0)
        #add the next ioburst after finishing cpuburst
        if pList[currentBurst[1]] !=[]:
            ioQueue[currentBurst[1]].append([pList[currentBurst[1]][0],currentBurst[1]])
            pList[currentBurst[1]].pop(0)
        else:
            isDone[currentBurst[1]]=True
        #if readyqueue is empty but io is not complete the shortest io
        #this is cpu downtime
        if readyQueue==[] and isNotEmpty(ioQueue):
            #find shortest ioBurst
            smallest= None
            for x in range(0,8):                    
                if ioQueue[x]!=[]:
                    if smallest is None:
                        smallest=copy.deepcopy(ioQueue[x])
                    elif smallest[0][0]>ioQueue[x][0][0]:
                        smallest=copy.deepcopy(ioQueue[x])
            for x in range(0,8):
                if not isDone[x]:
                    pTurnaroundTime[x]=pTurnaroundTime[x]+smallest[0][0]
                if ioQueue[x] != []:
                    #if there is something in the IOQueue, subtract time from it
                    ioQueue[x][0][0]=ioQueue[x][0][0]-int(smallest[0][0])
                    #if it is done take it out and add the next cpuburst to the readyqueue
                    if ioQueue[x][0][0]<=0:
                        ioQueue[x].pop(0)
                        readyQueue.append((pList[x][0],x))
                        pList[x].pop(0)
            totalTimer=totalTimer+smallest[0][0]
            totalDownTime=totalDownTime+smallest[0][0]
        #calculating Ttr
        for x in range(0,8):
            if not isDone[x]:
                pTurnaroundTime[x]=pTurnaroundTime[x]+currentBurst[0]
        
        
        #for debug
        # print("Tot "+str(totalTimer))
        # print("CPU "+str(cpuTimer))
        # print("DT  "+str(totalDownTime))
        # print("RDY "+str(readyQueue))
        # print("IO  "+str(ioQueue))
        # print("Ttr "+str(pTurnaroundTime))
        # print("BUR "+str(currentBurst))
        # print("isD "+str(isDone))
        # print("")
    

    for x in range(0,8):
        pWaitingTime[x]=pTurnaroundTime[x]-pProcessTotalTime[x]
    print("\tFCFS")
    print("CPU%    : "+str((totalTimer-totalDownTime)/(totalTimer-tLeft)*100)+"%")
    print("Tw      : "+str(pWaitingTime))
    print("Tw  AVG : "+str(sum(pWaitingTime.values())/8))
    print("Ttr     : "+str(pTurnaroundTime))
    print("Ttr AVG : "+str(sum(pTurnaroundTime.values())/8))
    print("Tr      : "+str(pResponseTime))
    print("Tr  AVG : "+str(sum(pResponseTime.values())/8))


if __name__ == "__main__":
    main()