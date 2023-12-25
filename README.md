# PlayOK Go Bot
Play Go at playok.com via GNU Go (or any other GTP engine)

# How it works?
Python script takes a screenshot, finds the coordinates of
the last move made on board and then sends it to the GTP engine
(GnuGo is default) subprocess to sync the board, then the engine
comes up with a move which is then converted to screen coordinates
where mouse pointer is being placed and the click event gets triggered.

# How to use it
First you need to have python and deps installed to make it run,
then you should calibrate the script parameters to match your
actual screen size/board placement, finally you can assign the
side to play to the script and enjoy the game.<br>
<br>
    CALIBRATE: <strong>python3 playok-go.py</strong><br>
    PLAY: <strong>python3 playok-go.py white</strong><br>
          <strong>python3 playok-go.py black</strong><br>

# See it in action
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/5jhJwHxAY_w/0.jpg)](https://www.youtube.com/watch?v=5jhJwHxAY_w)
