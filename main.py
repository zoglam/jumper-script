# Device Pixel Ratio: 1.500 = 150%

import pyautogui
from time import sleep
import keyboard
import win32api
import win32con


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, other_point):
        x_coord = other_point.x - self.x
        y_coord = other_point.y - self.y
        return (x_coord*x_coord + y_coord*y_coord)**(0.5)

    def jump_to(self, figure_pos):
        win32api.SetCursorPos((self.x, self.y))
        sleep(0.2)
        win32api.SetCursorPos((figure_pos.x, figure_pos.y))
        dist = self.distance_to(figure_pos)
        print(f'distance: {dist}')
        print(f'player: {self}')
        print(f'figure: {figure_pos}\n')
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        sleep(dist/605)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        sleep(1.1)

    def __str__(self):
        return f'x: {self.x} y: {self.y}'


INIT_X = 606
INIT_Y = 337


if __name__ == '__main__':
    while not keyboard.is_pressed('q'):
        img = pyautogui.screenshot(region=(INIT_X, INIT_Y, 1126, 448))

        for x in range(1, 57):
            figure = pyautogui.locate(
                f'filtered_img/{x}.png',
                img,
                confidence=0.65
            )
            if figure:
                print(f'picture: {x}.png - {figure}')

                player = None
                for i in range(1, 4):
                    player = pyautogui.locate(
                        f'filtered_img/player{i}.png',
                        img,
                        confidence=0.5
                    )
                    if player:
                        print(f'picture: player{i}.png - {player}')
                        break

                if player:
                    player_pos = Point(
                        INIT_X+player.left+(player.width//2),
                        INIT_Y+player.top+(player.height//2)
                    )
                    figure_pos = Point(
                        INIT_X+figure.left+(figure.width//2),
                        INIT_Y+figure.top+(figure.height//2)
                    )
                    player_pos.jump_to(figure_pos)
                    break
