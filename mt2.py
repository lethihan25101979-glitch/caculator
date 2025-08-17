# file: calc_pygame.py
import pygame, sys

pygame.init()
W, H = 400, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Calculator của nghya")
font = pygame.font.SysFont("consolas", 28)
bigfont = pygame.font.SysFont("consolas", 36)

buttons = [
    ["7","8","9","/"],
    ["4","5","6","*"],
    ["1","2","3","-"],
    ["0",".","C","+"],
    ["("," )","="]
]
# chuẩn hóa hàng cuối để có 4 cột hiển thị
buttons[-1] = ["(", ")", "=", ""]

BTN_W, BTN_H = 80, 80
MARGIN_X, MARGIN_Y = 20, 120
GAP = 10

expr = ""

def draw_display():
    pygame.draw.rect(screen, (230,230,230), (20,20,W-40,80), border_radius=10)
    txt = bigfont.render(expr[-18:] if expr else "0", True, (20,20,20))
    screen.blit(txt, (30, 45 - txt.get_height()//2 + 20))

def draw_buttons():
    rects = []
    for r, row in enumerate(buttons):
        for c, label in enumerate(row):
            if not label: 
                rects.append(None); continue
            x = MARGIN_X + c*(BTN_W+GAP)
            y = MARGIN_Y + r*(BTN_H+GAP)
            rect = pygame.Rect(x, y, BTN_W, BTN_H)
            pygame.draw.rect(screen, (245,245,245), rect, border_radius=12)
            pygame.draw.rect(screen, (200,200,200), rect, 2, border_radius=12)
            lab = font.render(label, True, (0,0,0))
            screen.blit(lab, (rect.centerx - lab.get_width()//2,
                              rect.centery - lab.get_height()//2))
            rects.append((rect, label))
    return rects

def evaluate(s):
    try:
        s = s.replace("×","*").replace("÷","/")
        return str(eval(s, {"__builtins__": None}, {}))
    except Exception:
        return "Error"

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            k = event.unicode
            if k in "0123456789.+-*/()":
                expr += k
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                expr = evaluate(expr)
            elif event.key == pygame.K_BACKSPACE:
                expr = expr[:-1]
            elif event.key == pygame.K_ESCAPE:
                expr = ""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for item in draw_buttons():
                if item and item[0].collidepoint(event.pos):
                    label = item[1]
                    if label == "C":
                        expr = ""
                    elif label == "=":
                        expr = evaluate(expr)
                    else:
                        expr += label

    screen.fill((255,255,255))
    draw_display()
    btn_cache = draw_buttons()  # vẽ và có dữ liệu hit-test
    pygame.display.flip()
    clock.tick(60)
