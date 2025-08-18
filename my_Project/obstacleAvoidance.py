
import mbuild
import mbot2
import event
import time
import cyberpi

import random

# ボタンAが押された際に実行するFunction

@event.is_press('a')
def on_button_a_pressed():

    while True:

        #障害物との距離が10cm以下であることを確認する

        if mbuild.ultrasonic2.get(1) < 10:
            #障害物が見つかった場合は、左右いずれかランダムに90どに開店する
            mbot2.turn(-90)

            mbot2.turn(random.choice([-90,90]))
        else:
            mbot2.forward(10)

        time.sleep(0.1)

