
from util import estimatetime

if __name__ == '__main__':
    timearray = []

    help_str = ["Without MultiThreading/Processing: ", str(estimatetime(100, ask=False, method="default"))]
    print(help_str[0]+help_str[1])
    timearray.append(help_str)

    if __name__ == '__main__':
        for i in range(1,51):
            help_str = ["MultiThreading with "+str(i)+" threads: ", str(estimatetime(100, ask=False, method="multithreading", threads_or_processes=i))]
            print(help_str[0], help_str[1])
            timearray.append(help_str)

    if __name__ == '__main__':
        for i in range(1,31):
            help_str = ["MultiProcessing with "+str(i)+" processes: ", str(estimatetime(100, ask=False, method="multiprocessing", threads_or_processes=i))]
            print(help_str[0], help_str[1])
            timearray.append(help_str)

    import operator
    sortedarray = sorted(timearray, key=operator.itemgetter(1), reverse=False)
    file = open("benchmarks.txt","w")
    for t in timearray:
        file.writelines(t[0]+t[1]+"\n")
    file.writelines("-----------Sorted-----------\n")
    for t in sortedarray:
        file.writelines(t[0]+t[1]+"\n")
    file.close()

'''
if __name__ == '__main__':
    timearray = []

    for i in range(100,2500,100):
        help_str = [str(i)+" games played - Without MultiThreading/Processing: ", str(estimatetime(i, ask=False, method="default", test_games=i))]
        print(help_str[0]+help_str[1])
        timearray.append(help_str)

    if __name__ == '__main__':
        for i in range(4,28,4):
            for j in range(100, 2500, 100):
                help_str = [str(j)+" games played - MultiThreading with "+str(i)+" threads: ", str(estimatetime(j, ask=False, method="multithreading", threads_or_processes=i, test_games=j))]
                print(help_str[0], help_str[1])
                timearray.append(help_str)

    if __name__ == '__main__':
        for i in range(4,20,4):
            for j in range(100, 2500, 100):
                help_str = [str(j)+" games played - MultiProcessing with "+str(i)+" processes: ", str(estimatetime(j, ask=False, method="multiprocessing", threads_or_processes=i, test_games=j))]
                print(help_str[0], help_str[1])
                timearray.append(help_str)

    import operator
    sortedarray = sorted(timearray, key=operator.itemgetter(1), reverse=False)
    file = open("benchmarks.txt","w")
    for t in timearray:
        file.writelines(t[0]+t[1]+"\n")
    file.writelines("-----------Sorted-----------\n")
    for t in sortedarray:
        file.writelines(t[0]+t[1]+"\n")
    file.close()
'''
