from eudplib import *
import helper


def beforeTriggerExec():
    # process_input()
    update()
    # render()
    EUDExecuteOnce()()
    x = helper.Container(8)()
    EUDEndExecuteOnce()
    x += 1


def update():
    actions = [(EPD(0x5124D8) + game_speed, SetTo, 40) for game_speed in range(7)]
    actions.append((EPD(0x6509A0), SetTo, 0))
    SeqCompute(actions)
