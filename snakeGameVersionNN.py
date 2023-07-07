from cmath import sqrt
from math import exp
from numbers import Real
import pygame
import time
import random
from NN import NN
from enum import Enum
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

# Entrées
# entree1 Mur ou queue à gauche
# entree2 Mur ou queue en face
# entree3 Mur ou queue à droite
# entree4 sin de l'angle entre la tete et la nouriture

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
 
dis_width = 600
dis_height = 400
 
SnakeDirectionMvt = Enum('SnakeDirectionMvt', "rightToLeftMvt LeftToRightMvt Top2BottomMvt Bottom2TopMvt")
SnakeDirectionConsigne = Enum('SnakeDirectionConsigne',"droite gauche haut bas")
 
 
def Your_score(score,dis,score_font):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])
 
 
 
def our_snake(snake_block, snake_list,dis):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])
 
class Snake:
    snake_block = 10
    snake_speed = 50
    Length_of_snake = 1
    direction = 0
    note = 0
    previousX1 = 0
    previousY1 = 0
    
    def __init__(self):
        self.nN = NN(4,5,3)
        self.snakeList = [[dis_width/2,dis_height/2]]        
        self.snakeHead = [dis_width/2,dis_height/2]

    def ComputeDirection(self,x1,y1):
        x2 = self.previousX1
        y2 = self.previousY1
        if x1-x2 < 0 and y1-y2 == 0 :
            return SnakeDirectionMvt.rightToLeftMvt
        elif x1-x2 > 0 and y1-y2 == 0 :
            return SnakeDirectionMvt.LeftToRightMvt
        elif x1-x2 == 0 and y1-y2 > 0 :
            return SnakeDirectionMvt.Top2BottomMvt
        elif x1-x2 == 0 and y1-y2 < 0 :
            return SnakeDirectionMvt.Bottom2TopMvt
        else :
            return SnakeDirectionMvt.Bottom2TopMvt 
            
    
    @staticmethod
    def ComputeEntree4(x1,y1,fx,fy,direction : SnakeDirectionMvt):
        if x1 != fx or y1 != fy:
            match direction :
                case SnakeDirectionMvt.rightToLeftMvt:
                    return (x1-fx)/sqrt(pow(fx-x1,2)+pow(fy-y1,2))
                case SnakeDirectionMvt.LeftToRightMvt:
                    return (fx-x1)/sqrt(pow(fx-x1,2)+pow(fy-y1,2))
                case SnakeDirectionMvt.Top2BottomMvt:
                    return (fy-y1)/sqrt(pow(fx-x1,2)+pow(fy-y1,2))
                case SnakeDirectionMvt.Bottom2TopMvt:
                    return (y1-fy)/sqrt(pow(fx-x1,2)+pow(fy-y1,2))                                               
        return 0
    
    def ComputeEntry(self, foodx, foody):
        x1 = self.snakeHead[0]
        y1 = self.snakeHead[1]
        entree1 = 0
        entree2 = 0
        entree3 = 0
        self.direction = self.ComputeDirection(x1,y1)
        match self.direction:
            case SnakeDirectionMvt.rightToLeftMvt:
                entree1 = 1 if y1 == (dis_height - self.snake_block) else 0
                if entree1 == 0 :
                    for block in self.snakeList:
                        entree1 = 1 if y1 == (block[1] + self.snake_block) and x1 == block[0] else 0
                        if entree1 == 1 :
                            break
                entree2 = 1 if x1 == 0 else 0
                if entree2 == 0 :
                    for block in self.snakeList:
                        entree2 = 1 if x1 == (block[0] + self.snake_block) and y1 == block[1] else 0
                        if entree2 == 1 :
                            break               
                entree3 = 1 if y1 == 0 else 0 
                if entree3 == 0 :
                    for block in self.snakeList:
                        entree3 = 1 if y1 == (block[1] - self.snake_block) and x1 == block[0] else 0
                        if entree3 == 1 :
                            break 
            case SnakeDirectionMvt.LeftToRightMvt:
                entree1 = 1 if y1 == 0 else 0
                if entree1 == 0 :
                    for block in self.snakeList:
                        entree1 = 1 if y1 == (block[1] - self.snake_block) and x1 == block[0] else 0 
                        if entree1 == 1 :
                            break
                entree2 = 1 if x1 == (dis_width - self.snake_block) else 0
                if entree2 == 0 :
                    for block in self.snakeList:
                        entree2 = 1 if x1 == (block[0] - self.snake_block) and y1 == block[1] else 0 
                        if entree2 == 1 :
                            break
                entree3 = 1 if y1 == (dis_height - self.snake_block) else 0
                if entree3 == 0 :
                    for block in self.snakeList:
                        entree3 = 1 if y1 == (block[1] + self.snake_block) and x1 == block[0] else 0  
                        if entree3 == 1 :
                            break               
            case SnakeDirectionMvt.Top2BottomMvt:
                entree1 = 1 if x1 == (dis_width - self.snake_block) else 0
                if entree1 == 0 :
                    for block in self.snakeList:
                        entree1 = 1 if x1 == (block[0] + self.snake_block) and y1 == block[1] else 0 
                        if entree1 == 1 :
                            break                
                entree2 = 1 if y1 == (dis_height - self.snake_block) else 0
                if entree2 == 0 :
                    for block in self.snakeList:
                        entree2 = 1 if y1 == (block[1] - self.snake_block) and x1 == block[0] else 0 
                        if entree2 == 1 :
                            break                 
                entree3 = 1 if x1 == 0 else 0
                if entree3 == 0 :
                    for block in self.snakeList:
                        entree3 = 1 if x1 == (block[0] - self.snake_block) and y1 == block[1] else 0     
                        if entree3 == 1 :
                            break            
            case SnakeDirectionMvt.Bottom2TopMvt:
                entree1 = 1 if x1 == 0 else 0
                if entree1 == 0 :
                    for block in self.snakeList:
                        entree1 = 1 if x1 == (block[0] - self.snake_block) and y1 == block[1] else 0   
                        if entree1 == 1 :
                            break               
                entree2 = 1 if y1 == 0 else 0
                if entree2 == 0 :
                    for block in self.snakeList:
                        entree2 = 1 if y1 == (block[1] + self.snake_block) and x1 == block[0] else 0  
                        if entree2 == 1 :
                            break                 
                entree3 = 1 if x1 == (dis_width - self.snake_block) else 0
                if entree3 == 0:
                    for block in self.snakeList:
                        entree3 = 1 if x1 == (block[0] + self.snake_block) and y1 == block[1] else 0 
                        if entree3 == 1 :
                            break                
        entree4 = self.ComputeEntree4(x1,y1,foodx,foody,self.direction)
        return [entree1, entree2, entree3, entree4]
    
    def UpdateSnake(self,x1,y1):
        self.previousX1 = self.snakeHead[0]
        self.previousY1 = self.snakeHead[1]
        self.snakeHead = []
        self.snakeHead.append(x1)
        self.snakeHead.append(y1)
        self.snakeList.append(self.snakeHead)
        if len(self.snakeList) > self.Length_of_snake:
            del self.snakeList[0]
        for x in self.snakeList[:-1]:
            if x == self.snakeHead:
                return True
        return False
    
def Accouplement(s1:Snake, s2:Snake):
    BbSnake = Snake() 
    BbSnake.nN.poidsEntrees = np.add(s1.nN.poidsEntrees,s2.nN.poidsEntrees)/2 
    BbSnake.nN.poidsSorties = np.add(s1.nN.poidsSorties,s2.nN.poidsSorties)/2
    return BbSnake
    

def Generation(Individus : list, notes : list):
    size = np.size(Individus)
    indiceMaxValues = np.argsort(notes)
    NouveauxIndividus = []
    weight = []
    for i in range(int(size/5)):
        weight.append(pow(i,10))
    #listIndividusProba = random.choices(indiceMaxValues[int(size/5):],weight,size/2)
    for i in range(int((size)*3/4)):
        ind1 = random.choices(indiceMaxValues[(size-int(size/5)):],weight)[0]
        indiv1 = Individus[ind1]
        indiv2 = Individus[random.choices(indiceMaxValues[(size-int(size/5)):],weight)[0]]
        NouveauxIndividus.append(Accouplement(indiv1,indiv2))
        print("Snake avec note : "+ str(indiv1.note)+" s'accouple avec snake avec note : "+ str(indiv2.note))
    for i in range(int(size/4)):
        NouveauxIndividus.append(Snake())
    print(np.size(NouveauxIndividus))
    return NouveauxIndividus

def message(msg, color,dis,font_style):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])
     
def SnakeReset(s : Snake):
    newSnake = Snake()  
    newSnake.nN = s.nN
    return newSnake
    
def gameLoop(s : Snake, display = True):
    if display == True :    
        pygame.init()
        clock = pygame.time.Clock()
        font_style = pygame.font.SysFont("bahnschrift", 25)
        dis = pygame.display.set_mode((dis_width, dis_height))
        pygame.display.set_caption('Snake Game by Edureka') 
        score_font = pygame.font.SysFont("comicsansms", 35)

    game_over = False
    time = 0
    flag = 0
    x1 = dis_width / 2
    y1 = dis_height / 2
 
    x1_change = 0
    y1_change = 0
 
    foodx = round(random.randrange(0, dis_width - s.snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - s.snake_block) / 10.0) * 10.0
 
    while not game_over:
 
        entrees = s.ComputeEntry(foodx, foody)
        s.nN.vectEntrees = entrees
        sorties = s.nN.ComputeSorties()
                    
        match s.direction:
            case SnakeDirectionMvt.rightToLeftMvt:
                if sorties == 0 :
                    mvt = SnakeDirectionConsigne.bas
                elif sorties == 1 :
                    mvt = SnakeDirectionConsigne.gauche
                elif sorties == 2 :
                    mvt = SnakeDirectionConsigne.haut
            case SnakeDirectionMvt.LeftToRightMvt:
                if sorties == 0 :
                    mvt = SnakeDirectionConsigne.haut
                elif sorties == 1 :
                    mvt = SnakeDirectionConsigne.droite
                elif sorties == 2 :
                    mvt = SnakeDirectionConsigne.bas
            case SnakeDirectionMvt.Bottom2TopMvt:
                if sorties == 0 :
                    mvt = SnakeDirectionConsigne.gauche
                elif sorties == 1 :
                    mvt = SnakeDirectionConsigne.haut
                elif sorties == 2 :
                    mvt = SnakeDirectionConsigne.droite     
            case SnakeDirectionMvt.Top2BottomMvt:
                if sorties == 0 :
                    mvt = SnakeDirectionConsigne.droite
                elif sorties == 1 :
                    mvt = SnakeDirectionConsigne.bas
                elif sorties == 2 :
                    mvt = SnakeDirectionConsigne.gauche                                   


        if mvt == SnakeDirectionConsigne.gauche:
            x1_change = -s.snake_block
            y1_change = 0
        elif mvt == SnakeDirectionConsigne.droite:
            x1_change = s.snake_block
            y1_change = 0
        elif mvt == SnakeDirectionConsigne.haut:
            y1_change = -s.snake_block
            x1_change = 0
        elif mvt == SnakeDirectionConsigne.bas:
            y1_change = s.snake_block
            x1_change = 0
        
        x1 += x1_change
        y1 += y1_change
        game_over = s.UpdateSnake(x1,y1)         
        if display == True :
            dis.fill(blue)            
            pygame.draw.rect(dis, green, [foodx, foody, s.snake_block, s.snake_block])
            Your_score(s.Length_of_snake - 1,dis,score_font)       
        if display == True :                    
            our_snake(s.snake_block, s.snakeList,dis)
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_over = True
        if display == True :        
            pygame.display.update()
 
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - s.snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - s.snake_block) / 10.0) * 10.0
            s.Length_of_snake += 1
            s.note += 1000
            flag = 0
            
        time+=1 
        flag+=1
        if flag == 150:
            game_over = True
        if display == True :        
            clock.tick(s.snake_speed)
    s.note += time
    if display == True :    
        pygame.QUIT
 
tic = time.perf_counter()
nbreIndividus = 500
nbreGene = 41
listIndividus = []
listeNotes=[]
index=[]
for n in range(nbreIndividus):
    s = Snake()
    listIndividus.append(s)
    gameLoop(s,False)
    listeNotes.append(s.note)
    index.append(n)

exportData = pd.DataFrame(listeNotes, index=index) 
print(listeNotes)

meilleurSnake = Snake()
meilleureNote = 0
listMoyenne = []
for i in range(nbreGene):
    newSnake = Generation(listIndividus,listeNotes)
    listIndividus = []
    listeNotes=[]
    sumMoyenne = 0
    for n in range(nbreIndividus):
        s = newSnake[n]
        listIndividus.append(s)
        gameLoop(s,False)
        listeNotes.append(s.note)
        if s.note > meilleureNote:
            meilleureNote = s.note
            meilleurSnake = s
        sumMoyenne += s.note
    listMoyenne.append(sumMoyenne/nbreIndividus)
    gameLoop(SnakeReset(meilleurSnake))
    if i % 4 == 0 :
        exportData = pd.DataFrame(listeNotes)
        exportData.to_csv('result_'+str(i)+'.csv', encoding='utf-8')
plt.plot(listMoyenne)
plt.show()
toc = time.perf_counter()
print(f"processed in  {toc - tic:0.1f} seconds")

