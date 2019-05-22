import multiprocessing as mp
from multiprocessing import cpu_count
try:
    from connect4.game import Game
except:
    from game import Game
try:
    from connect4.ai_input import AIPlayer
except:
    from ai_input import AIPlayer


def playgames_multiprocess(episodes, processes=None, testing=False):
    output = mp.Queue()
    if __name__ == 'connect4.multi_processing' or __name__ == 'multi_processing':
        if processes is not None:
            pro_num = processes
        else:
            pro_num = cpu_count()

        episodesperprocess = int(episodes / pro_num)
        processes = list()
        episodes_array = [episodesperprocess] * pro_num
        episodes_counter = episodesperprocess * pro_num

        for i in range(pro_num):
            if episodes_counter >= episodes:
                break
            episodes_array[i] += 1
            episodes_counter += 1

        for i in range(pro_num):
            processes.append(mp.Process(target=f, args=(episodes_array[i], output, i, pro_num, testing)))

        for p in processes:
            p.start()

        for p in processes:
            p.join()

        results = [output.get() for p in processes]

        stats = [0,0,0]
        for i in range(len(results)):
            stats[0] += results[i][0]
            stats[1] += results[i][1]
            stats[2] += results[i][2]

        return stats


def f(length, output, processnumber, overallprocesses, testing):
    if testing:
        game = Game(AIPlayer("x", randomizer_factor=0.0, training=True),
                      AIPlayer("o", randomizer_factor=0.0, training=True))
    else:
        game = Game(AIPlayer("x", randomizer_factor=0.3, learning_rate=0.75, training=True),
                      AIPlayer("o", randomizer_factor=0.3, learning_rate=0.75, training=True))

    for i in range(length):
        game.play()
        if processnumber == 0:
            if (i+1) % int(10000/overallprocesses) == 0:
                print((i+1)*overallprocesses, "games played")

    output.put(game.stats)
