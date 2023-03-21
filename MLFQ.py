import io
import re

# please make sure and have a data.txt file with the 8 processes inside the same directiory as this file

def main():
    
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
    queueTracker=[1,1,1,1,1,1,1,1]
    readyQueue1 = []
    readyQueue2 = []
    readyQueue3 = []
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

    ioQueue = {
        0:-1,
        1:-1,
        2:-1,
        3:-1,
        4:-1,
        5:-1,
        6:-1,
        7:-1
    }

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

    readyQueue1.append([pList[0][0], 0])
    pList[0].pop(0)
    readyQueue1.append([pList[1][0], 1])
    pList[1].pop(0)
    readyQueue1.append([pList[2][0], 2])
    pList[2].pop(0)
    readyQueue1.append([pList[3][0], 3])
    pList[3].pop(0)
    readyQueue1.append([pList[4][0], 4])
    pList[4].pop(0)
    readyQueue1.append([pList[5][0], 5])
    pList[5].pop(0)
    readyQueue1.append([pList[6][0], 6])
    pList[6].pop(0)
    readyQueue1.append([pList[7][0], 7])
    pList[7].pop(0)

    totalTimer=0
    tLeft=60
    tqRemaining1=5
    tq2List=[10,10,10,10,10,10,10,10]
    currentBurst=None
    def checkIo():
        for x in ioQueue.keys():
            if ioQueue[x]>=0:
                return True
        return False
    while readyQueue1 or readyQueue2 or readyQueue3 or checkIo() or currentBurst:
        for x in range(0,8):
            if pList[x] ==[]and pTurnaroundTime[x]==0:
                pTurnaroundTime[x]=totalTimer
        totalTimer=totalTimer+1
        if currentBurst is None:
            if readyQueue1!=[]:
                currentBurst=readyQueue1.pop()
            elif readyQueue2!=[]:
                currentBurst=readyQueue2.pop()
            elif readyQueue3!=[]:
                currentBurst=readyQueue3.pop()
        if currentBurst!=None and not isTouched[currentBurst[1]]:
            isTouched[currentBurst[1]]=True
            pResponseTime[currentBurst[1]]=totalTimer
        #check if first queue is empty
        if currentBurst != None and queueTracker[currentBurst[1]]==1 :
            
            #subtract from time remaining
            tqRemaining1=tqRemaining1-1
            currentBurst[0]=currentBurst[0]-1

            #handle IO burst
            for x in ioQueue.keys():
                #check if io is done
                ioQueue[x]=ioQueue[x]-1
                if ioQueue[x]==0:
                    if pList[x] != []:
                        readyQueue1.append([pList[x].pop(0),x])
                        ioQueue[x]=-8880000

            #check if burst is done
            if currentBurst[0]==0:
                tqRemaining1=5
                #add io to ioQueue
                if pList[currentBurst[1]]!=[]:
                    ioQueue[currentBurst[1]]=(pList[currentBurst[1]].pop(0))
                currentBurst=None
            #check for downgrade
            elif tqRemaining1<=0:
                tqRemaining1=5
                readyQueue2.append(currentBurst)
                currentBurst=None
        #check if second queue is empty
        elif currentBurst is not None and queueTracker[currentBurst[1]]==2:
            
            #subtract from time remaining
            tq2List[currentBurst[1]]=tq2List[currentBurst[1]]-1
            currentBurst[0]=currentBurst[0]-1
            preempt=False
            #handle IO burst
            for x in ioQueue.keys():
                #check if io is done
                ioQueue[x]=ioQueue[x]-1
                if ioQueue[x]==0:
                    if pList[x] != []:
                        readyQueue1.append([pList[x].pop(0),x])
                        ioQueue[x]=-8880000

            #check if burst is done
            if currentBurst[0]==0:
                tq2List[currentBurst[1]]=10
                #add io to ioQueue
                if pList[currentBurst[1]]!=[]:
                    ioQueue[currentBurst[1]]=(pList[currentBurst[1]].pop(0))
                currentBurst=None
            #check for downgrade
            elif tqRemaining1<=0:
                readyQueue3.append(currentBurst)
                currentBurst=None
            #handle preempt
            if preempt and currentBurst != None:
                readyQueue2.append(currentBurst)
                tq2List[currentBurst[1]]=10
                currentBurst=None
        #check if third queue is empty
        elif currentBurst is not None and queueTracker[currentBurst[1]]==3:
            
            #subtract from time remaining
            currentBurst[0]=currentBurst[0]-1
            preempt=False
            #handle IO burst
            for x in ioQueue.keys():
                #check if io is done
                ioQueue[x]=ioQueue[x]-1
                if ioQueue[x]==0:
                    if pList[x] != []:
                        readyQueue1.append([pList[x].pop(0),x])
                        ioQueue[x]=-8880000
            #check if burst is done
            if currentBurst[0]==0:
                tq2List[currentBurst[1]]=10
                #add io to ioQueue
                if pList[currentBurst[1]]!=[]:
                    ioQueue[currentBurst[1]]=(pList[currentBurst[1]].pop(0))
                currentBurst=None

            #handle preempt
            if preempt and currentBurst != None:
                readyQueue3.append(currentBurst)
                currentBurst=None
        else:
            #non cpu time
            totalDownTime=totalDownTime+1
            for x in ioQueue.keys():
                    #check if io is done
                    ioQueue[x]=ioQueue[x]-1
                    if ioQueue[x]==0:
                        if pList[x] != []:
                            readyQueue1.append([pList[x].pop(0),x])
                            ioQueue[x]=-8880000

    for x in range(0,8):
        pWaitingTime[x]=pTurnaroundTime[x]-pProcessTotalTime[x]
    print("\tMLFQ")
    print("CPU%    : "+str((totalTimer-totalDownTime)/(totalTimer-tLeft)*100)+"%")
    print("Tw      : "+str(pWaitingTime))
    print("Tw  AVG : "+str(sum(pWaitingTime.values())/8))
    print("Ttr     : "+str(pTurnaroundTime))
    print("Ttr AVG : "+str(sum(pTurnaroundTime.values())/8))
    print("Tr      : "+str(pResponseTime))
    print("Tr  AVG : "+str(sum(pResponseTime.values())/8))
if __name__ == "__main__":
    main()