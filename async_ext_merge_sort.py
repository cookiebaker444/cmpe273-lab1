#Author : Kuang Sheng
import os
import linecache
import asyncio

def sortSingleFiles():#sort all the files and save as individual files
    #import os
    count = 0
    path = os.path.realpath('cmpe273-spring20-labs-master/lab1/input/') #This may need to be changed to a proper path
    
    os.chdir(path)
    realMax = 0
    for filename in os.listdir(path):
        if filename[0:2] == "un": 
            count += 1
            with open (filename, "r") as f:
                
                lines = f.readlines()
                for i in range(0, len(lines)):
                    lines[i] = int(lines[i])
                for i in range(0, len(lines)):
                    for j in range(i + 1, len(lines)):
                        if (lines[i] > lines[j]):
                            temp = lines[i]
                            lines[i] = lines[j]
                            lines[j] = temp    
                
                realMax = max(realMax, max(lines))
                if filename[9:11] != "10":
                    newName = filename[2:9] + "0" + filename[9:]
                else:
                    newName = filename[2:]
                fw = open(newName, 'w')
                for i in range(len(lines)):
                    fw.write(str(lines[i]))
                    fw.write("\n")
                
                fw.close()
                f.close()
    return count, realMax
#loop = asyncio.get_event_loop()
#loop.run_until_complete(sortSingleFiles())
#loop.close()
def enterSortFiles(count, tupleStore):# store elements into the store list first time
    #path = os.getcwd()
    store = [0]*count
    ##for i in range (count):
        ##store.append(0)
    fileName = [' ']*10
    for i in range(len(os.listdir())):
        filename = os.listdir()[i]
        if filename[0:2] == "so":
            with open (filename, "r") as f:
                fileName[int(filename[7:9])-1] = filename
                #print (int(f.readline()))
                #store.insert(int(filename[7:9]) - 1,int(f.readline()))
                store[int(filename[7:9]) - 1] += int(f.readline())
                f.close()
    return store, fileName
    #putInQueue(store, fileName, tupleStore[1], myQueue)
async def putInQueue(store, fileName, realMax, myQueue): #merge to a single file from all sorted files
    #path = os.getcwd()
    #resTemp = []
    pos = [2] * 10
    while min(store) != realMax + 1:
        #fw = open('result.txt', 'a')#
        #fw.write(str(min(store)))#
        #fw.write("\n")#
        #resTemp.append(min(store))
        #await asyncio.sleep(1)
        await myQueue.put(str(min(store)))
        
        minIndex = store.index(min(store))
        filename = fileName[minIndex]
        if linecache.getline(filename, pos[minIndex]):
            store[minIndex] = int(linecache.getline(filename, pos[minIndex]))
            linecache.clearcache()
            pos[minIndex] += 1
        else:
            store[minIndex] = realMax + 1
    #fw.close()#
async def queueToFile(myQueue):
    while not myQueue.empty():
        #item = await myQueue.get()
        
        fw = open('async_sorted.txt', 'a')
        await asyncio.sleep(0)
        fw.write(await myQueue.get())
        #print("Queue size is:" + str(myQueue.qsize()))
        #myQueue.task_done()
        fw.write("\n")
    #myQueue.task_done()
    fw.close()
if __name__ == '__main__':
    
    myQueue = asyncio.Queue(maxsize = 20)
    #myQueue = queue.Queue()
    tupleStore = sortSingleFiles()
    tupleStore2 = enterSortFiles(tupleStore[0], tupleStore)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(putInQueue(tupleStore2[0], tupleStore2[1], tupleStore[1], myQueue), queueToFile(myQueue)))
    #enterSortFiles(tupleStore[0], tupleStore)    
