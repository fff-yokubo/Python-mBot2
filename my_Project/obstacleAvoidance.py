'''

コードの説明
このプログラムは CyberPi と mBuild の超音波センサー を使って、センサーの測定距離を画面に表示し、さらに距離によって LED の色と警告表示を切り替えるものです。

処理の流れ

初期表示
    CyberPi の画面に "Range:" というラベルを表示します。

メインループ（無限ループ）
    mbuild.ultrasonic2.get(index=1) を使って、超音波センサーで前方までの距離（cm）を取得します。
    取得した距離を CyberPi の画面に数値として表示します。

障害物の判定
    距離が 10cm 未満の場合：
    LED を 赤色 に点灯させます。
    画面に "Obstacle!" と表示して、障害物が近いことを知らせます。

    距離が 10cm 以上の場合：

        LED を 緑色 に点灯させます。

        画面に "No Obstacle" と表示して、障害物がないことを示します。

'''

import math


import mbuild, mbot2, cyberpi, event, mbuild, time



class US_ObstacleSensor():

    '''
    超音波センサーを使って障害物を検知するクラス
        IIRフィルタを使用してセンサ値のノイズを除去
        センサ値が一定の範囲内にあるかを判定する
    '''

    POS_Y = 50


    def __init__(self, THRESHOLD = 10):

        #上下限値: 下記の値を逸脱した場合は異常値とみなす
        self.UB = 100#
        self.LB = 4
        self.alpha = 0.9 # IIRフィルタの係数
        self.THRESHOLD = THRESHOLD #障害物の検知距離(cm)


        #センサ値の初期値

        self.range = (self.UB+self.LB)/2
        cyberpi.display.show_label("Range:", 12, 0, self.POS_Y, index = 0)

        # cyberpi.display.show_label(text,size,x,y,index)

        cyberpi.display.show_label(self.range, 12, 50, self.POS_Y, index = 1)


        for _ in range(200):
            self.getRange()



    def getRange(self):
        """
        センサ値を取得する関数
        IIRフィルタを使用してノイズを除去
        """
        # 測定値を取得
        rangeval = mbuild.ultrasonic2.get(index=1)

        #測定値下限以下→下限値を代入
        rangeval = max(self.LB, rangeval)

        #測定値が上限超→上限値を代入

        rangeval = min(self.UB, rangeval)

        # IIRフィルタを適用
        self.range = (self.range * (1 - self.alpha)) + (rangeval * self.alpha)
        self.range = round(self.range,0)
        cyberpi.display.show_label("%.0f"%self.range, 12, 50, self.POS_Y, index=1)

        return self.range



    def chk_obstacle(self):
        """
        障害物を検知する関数
        センサ値が10cm未満の場合は障害物ありと判定
        """
        range = self.getRange()
        if range < self.THRESHOLD:
            return True
        else:
            return False

'''
'''

def mbot2_go(Base, Diff, left=True):
    if left:
        mbot2.EM_set_speed((Base + Diff),"EM1")
        mbot2.EM_set_speed((Base - Diff),"EM2")
    else:
        mbot2.EM_set_speed(-1 * ((Base - Diff)),"EM1")
        mbot2.EM_set_speed(-1 * ((Base + Diff)),"EM2")


def obstacle_avoidance(uos):
    '''
    障害物回避行動のメイン関数

    コの字に避ける

      ↓
    ┌-┘
    |
    └-┐


    '''
    POS_Y = 20

    dist_x = 20
    dist_y = 25

    #障害物検知(発動)

    cyberpi.display.show_label("Obstacle Avoidance", 12, 0, POS_Y, index = 2)
    time.sleep(1)

    #Step1
    #┌-┘



    #90度左に回転
    #
    cyberpi.display.show_label("Turn Left 90",12,0,POS_Y + 10,3)
    mbot2.turn(-90)
    time.sleep(1)

    #横方向にdist_x cm
    mbot2.straight(dist_x)
    cyberpi.display.show_label("Avoid %s cm"%dist_x,12,0,POS_Y + 10,3)
    time.sleep(1)

    #90度右に回転(元の進行方向に戻す)
    cyberpi.display.show_label("Turn Right 90",12,0,POS_Y + 10,3)
    mbot2.turn(90)
    time.sleep(1)


    #進行方向に対し、dist_y cm 直進
    mbot2.straight(dist_y)
    cyberpi.display.show_label("Avoid %s cm"%dist_y,12,0,POS_Y + 10,3)
    time.sleep(1)



    #障害物をよけきれたかどうか判定する

    while inavoidance_chk(uos):
        mbot2.straight(dist_y)
        time.sleep(1)


    #dist_x cm 直進
    mbot2.straight(dist_x)
    cyberpi.display.show_label("Avoid %s cm"%dist_x,12,0,POS_Y + 10,3)
    time.sleep(1)




    #90度左に回転
    cyberpi.display.show_label("Turn Left 90",12,0,POS_Y + 10,3)
    mbot2.turn(-90)
    time.sleep(1)


def inavoidance_chk(uos):
    '''
    回避中チェック
    90度回転して障害物の有無を確認
        障害物あり → -90度回転(もとの向きに戻して)　True
        障害物なし → False
    を返す
    '''

    mbot2.turn(90)

    if uos.getRange() < 15:
        mbot2.turn(-90)
        return True
    else:
        return False


uos = US_ObstacleSensor()



obstacle_avoidance(uos)

# while True:


#     if uos.chk_obstacle():
#         cyberpi.led.on(255,0,0,id="all")
#         cyberpi.display.show_label("Obstacle!", 16, 0, 20, index = 2)
#     else:
#         cyberpi.led.on(0,255,0,id="all")
#         cyberpi.display.show_label("No Obstacle", 16, 0, 20, index = 2)


