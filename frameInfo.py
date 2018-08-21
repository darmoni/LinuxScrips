import inspect, sys
import functools
from functools import partial

def PrintFrame(index =2):
    callerframerecord = inspect.stack()[1]    # 0 represents this line
                                            # 1 represents line at caller
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    results ={}
    if 4 & int(index):
        results['filename'] = info.filename                       # __FILE__     -> Test.py
        #print (info.filename)
    if 1 & int(index):
        results['function'] = info.function
        #print (info.function)                       # __FUNCTION__ -> Main
    if 2 & int(index):
        results['lineno'] = info.lineno
        #print (info.lineno)                         # __LINE__     -> 13
    return results

if (sys.version_info > (3, 0)):
    printf = functools.partial(print, end="")
    PrintFrame()
else:
    print("python version {} is not supported".format(version_info))
    exit(-1)

def main(argv):
    for index in argv :
        results = PrintFrame(index)
        printf("trigger = {}:".format(index))
        for res in results:
            printf("\t {} = {}".format(res, results[res]))
        print()


if __name__ == "__main__":
       main(list(sys.argv[1:]))
