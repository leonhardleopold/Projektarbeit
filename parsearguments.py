import sys, getopt


def parse(args, type):
    parseargs = {}
    try:
        if type == "tictactoe":
            options, arguments = getopt.getopt(args, 'm:x:o:t', ['test', 'firstplayer=', 'first=', 'p1=', 'secondplayer=', 'second=', 'p2=', 'training'])
            for opt, arg in options:
                if opt in ('-m', '--mode'):
                    parseargs['mode'] = int(arg)
                if opt in ('-x', '--firstplayer', '--first', '--p1'):
                    parseargs['x'] = arg
                if opt in ('-o', '--secondplayer', '--second', '--p2'):
                    parseargs['o'] = arg
                if opt in ('-t','--training', '--test'):
                    parseargs['test'] = True

            if ('x' in parseargs and 'o' not in parseargs) or ('o' in parseargs and 'x' not in parseargs):
                print("Either both or no player has to be set!")
                printusage(type)
                sys.exit(2)
            if 'mode' in parseargs and ('o' in parseargs or 'x' in parseargs or 'test' in parseargs):
                print("Info: If the mode is set, other arguments like -x, -o and --test will be ignored")
            if 'test' in parseargs and ('o' in parseargs or 'x' in parseargs):
                print("Info: If testing is set, other arguments like -x and -o will be ignored")

            return parseargs


        elif type == "connect4":
            options, arguments = getopt.getopt(args, 'm:t:p:dx:o:t', ['test', 'threads=', 'processes=', 'default', 'firstplayer=', 'first=', 'p1=', 'secondplayer=', 'second=', 'p2=', 'training'])
            parseargs['method'] = 'unset'
            for opt, arg in options:
                if opt in ('-m', '--mode'):
                    parseargs['mode'] = int(arg)
                if opt in ('-t', '--threads'):
                    parseargs['multithreading'] = int(arg)
                    parseargs['method'] = 'multithreading'
                if opt in ('-p', '--processes'):
                    parseargs['multiprocessing'] = int(arg)
                    parseargs['method'] = 'multiprocessing'
                if opt in ('-d', '--default'):
                    parseargs['default'] = True
                    parseargs['method'] = 'default'
                if opt in ('-x', '--firstplayer', '--first', '--p1'):
                    parseargs['x'] = arg
                if opt in ('-o', '--secondplayer', '--second', '--p2'):
                    parseargs['o'] = arg
                if opt in ('--test', '--training'):
                    parseargs['test'] = True

            if ('x' in parseargs and 'o' not in parseargs) or ('o' in parseargs and 'x' not in parseargs):
                print("Either both or no player has to be set!")
                printusage(type)
                sys.exit(2)
            if 'mode' in parseargs and ('o' in parseargs or 'x' in parseargs or 'test' in parseargs):
                print("Info: If the mode is set, other arguments like -x, -o and --test will be ignored.")
            if 'test' in parseargs and ('o' in parseargs or 'x' in parseargs):
                print("Info: If testing is set, other arguments like -x and -o will be ignored.")
            if sum(item is True for item in ['default' in parseargs, 'multiprocessing' in parseargs, 'multithreading' in parseargs]) > 1:
                print("Info: Multiple methods selected: Multiprocessing will be used.")
                parseargs['method'] = 'multiprocessing'
                if 'multiprocessing' not in parseargs:
                    parseargs['multiprocessing'] = 8

            return parseargs
    except (getopt.GetoptError, ValueError):
        printusage(type)
        sys.exit(2)


def printusage(type):
    if type == "tictactoe":
        print("There was an error encountered! Correct usage: \n"
              "-m : mode [1,2,3] 1 = Human vs Human, 2 = Human vs AI, 3 = AI vs AI\n"
              "-x : type of first player [r,a,h,t] r = Randomized Input, a = AI, h = Human, t = AI without randomizer factor\n"
              "-o : type of second player [r,a,h,t] r = Randomized Input, a = AI, h = Human, t = AI without randomizer factor\n"
              "-t : testing - no argument needed - both players are AI's without randomizer factor")
    elif type == "connect4":
        print("There was an error encountered! Correct usage: \n "
              "-m : mode [1,2,3] 1 = Human vs Human, 2 = Human vs AI, 3 = AI vs AI\n"
              "-t : multithreading [number of threads used] \n"
              "-p : multiprocessing [number of processes used] \n"
              "-d : default - no multithreading or multiprocessing used\n"
              "-x : type of first player [r,a,h] r = Randomized Input, a = AI, h = Human, t = AI without randomizer factor\n"
              "-o : type of second player [r,a,h] r = Randomized Input, a = AI, h = Human, t = AI without randomizer factor\n"
              "--test : testing - no argument needed - both players are AI's without randomizer factor")