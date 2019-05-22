import threading
try:
    from connect4.game import Game
except:
    from game import Game
try:
    from connect4.ai_input import AIPlayer
except:
    from ai_input import AIPlayer


def playgames_multithread(episodes, threads=20, testing=False):
    stats = [0, 0, 0]
    if __name__ == 'connect4.multi_threading' or __name__ == 'multi_threading':
        d = threading.local()
        if testing:
            d.game = Game(AIPlayer("x", randomizer_factor=0.0, training=True),
                      AIPlayer("o", randomizer_factor=0.0, training=True))
        else:
            d.game = Game(AIPlayer("x", randomizer_factor=0.3, learning_rate=0.75, training=True),
                  AIPlayer("o", randomizer_factor=0.3, learning_rate=0.75, training=True))

        thread_num = threads
        episodesperthread = int(episodes / thread_num)
        threads = list()

        episodes_array = [episodesperthread] * thread_num
        episodes_counter = episodesperthread * thread_num

        for i in range(thread_num):
            if episodes_counter >= episodes:
                break
            episodes_array[i] += 1
            episodes_counter += 1

        for i in range(thread_num-1):
            t = threading.Thread(target=f_multithread, args=(d, episodes_array[i], stats, testing))
            t.daemon = True
            threads.append(t)
            t.start()

        if threading.current_thread() is threading.main_thread():
            for i in range(episodes_array[thread_num-1]):
                d.game.play()
                if (i+1) % int(10000/thread_num) == 0:
                    print((i+1)*thread_num, "games played")

        for index, thread in enumerate(threads):
            thread.join()

        stats[0] += d.game.stats[0]
        stats[1] += d.game.stats[1]
        stats[2] += d.game.stats[2]

        return stats
    else:
        print("Error:",__name__)


def f_multithread(d, length, stats, testing):
    if testing:
        d.game = Game(AIPlayer("x", randomizer_factor=0.0, training=True),
                  AIPlayer("o", randomizer_factor=0.0, training=True))
    else:
        d.game = Game(AIPlayer("x", randomizer_factor=0.3, learning_rate=0.75, training=True),
              AIPlayer("o", randomizer_factor=0.3, learning_rate=0.75, training=True))

    for i in range(length):
        d.game.play()

    stats[0] += d.game.stats[0]
    stats[1] += d.game.stats[1]
    stats[2] += d.game.stats[2]

