import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
key_delta = {  # 練習1
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:  # 練習3
    """
    オブジェクトが画面内or画面外を判定し，真理値タプルを返す関数
    引数：こうかとんRect，または，爆弾Rect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj_rct.right < 0 or WIDTH < obj_rct.left:
        yoko = False
    if obj_rct.bottom < 0 or HEIGHT < obj_rct.top:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bb_img = pg.Surface((20, 20))  # 練習2
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 練習2
    bb_img.set_colorkey((0, 0, 0))  # 練習2
    bb_rct = bb_img.get_rect()  # 練習2
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)  # 練習2
    vx, vy = +5, +5  # 練習2
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):  # 練習4
            print("Game Over")
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, delta in key_delta.items():  # 練習1
            if key_lst[key]:
                sum_mv[0] += delta[0]
                sum_mv[1] += delta[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  # 練習3
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        yoko, tate = check_bound(bb_rct)  # 練習3
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        bb_rct.move_ip(vx, vy)  # 練習2
        screen.blit(bb_img, bb_rct)  # 練習2
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    pg.init()
    main()
    pg.quit()
    sys.exit()
