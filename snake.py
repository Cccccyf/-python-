import sys
import random
import pygame
ScreenX=600
ScreenY=600

#25为一个单位
class Snake(object):
    def __init__(self):                                #蛇的属性
        self.dirction=pygame.K_RIGHT
        self.body=[]                                 #蛇身的坐标点
        for x in range(5):
            self.eat()

    def eat(self):
        left,top=(0,0)                               #蛇身头坐标初始化
        if self.body:
            left,top=(self.body[0].left,self.body[0].top)
        node=pygame.Rect(left,top,25,25)             #框选蛇身所占的区域
        if self.dirction==pygame.K_LEFT:
            node.left-=25
        elif self.dirction==pygame.K_RIGHT:
            node.left+=25
        elif self.dirction==pygame.K_UP:
            node.top-=25
        elif self.dirction==pygame.K_DOWN:
            node.top+=25
        self.body.insert(0,node)

    def delnode(self):                              #删除
        self.body.pop()

    def isdead(self):                               #判断死亡
        if self.body[0].x not in range(ScreenX):    #撞墙
            return True
        if self.body[0].y not in range(ScreenY):
            return True
        if self.body[0] in self.body[1:]:           #咬到自己
            return True
        return False

    def move(self):                                 #移动
        self.eat()
        self.delnode()

    def changedirction(self,curkey):
        LR=[pygame.K_LEFT,pygame.K_RIGHT]
        UD=[pygame.K_UP,pygame.K_DOWN]
        if curkey in LR+UD:
            if(curkey in LR)and(self.dirction in LR):
                return                             #结束函数，跳出判断
            if(curkey in UD)and(self.dirction in UD):
                return
            self.dirction=curkey

class Food:
    def __init__(self):
        self.rect=pygame.Rect(-25,0,25,25)

    def remove(self):
        self.rect.x=-25

    def set(self):
        if self.rect.x==-25:
            allpos=[]
            for pos in range(25,ScreenX-25,25):
                allpos.append(pos)
            self.rect.left=random.choice(allpos)
            self.rect.top=random.choice(allpos)
            print(self.rect)


def showtext(screen,pos,text,color,font_bold=False,font_size=60,font_italic=False):
    cur_font=pygame.font.SysFont("宋体",font_size)      #获取系统字体，设置文字大小
    cur_font.set_bold(font_bold)                        #设置不加粗
    cur_font.set_italic(font_italic)                    #设置不斜体
    text_fmt=cur_font.render(text,1,color)              #设置文字内容
    screen.blit(text_fmt,pos)                           #在画板上绘制文字



def main():
    #初始化
    pygame.init()
    screen_size=(ScreenX,ScreenY)
    screen=pygame.display.set_mode(screen_size)      #游戏界面创建
    pygame.display.set_caption('贪吃蛇')              #窗口标题命名
    clock=pygame.time.Clock()                        #时间滴答函数（每秒帧数）
    score=0
    isdead=False

    snake=Snake()
    food=Food()


    while True:

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type==pygame.KEYDOWN:
                snake.changedirction(event.key)
                if event.key==pygame.K_SPACE and isdead:
                    return main()

        screen.fill((255, 255, 255))  # 背景颜色白色



        if not isdead:                             #画蛇身
            snake.move()
        for rect in snake.body:
            pygame.draw.rect(screen,(50,50,0),rect,0)

        isdead=snake.isdead()

        if isdead:
            showtext(screen,(140,200),'You Dead',(227,29,18),False,100)
            showtext(screen,(160,260),'press space key to try again',(0,0,22),False,30)

        if food.rect==snake.body[0]:              #判断蛇是否吃到食物
            score+=50
            food.remove()
            snake.eat()

        food.set()
        pygame.draw.rect(screen,(136,0,24),food.rect,0)

        showtext(screen,(50,500),'Current scores:'+str(score),(223,223,223))  #显示分数

        pygame.display.update()                  # 更新时间
        clock.tick(10)


main()


