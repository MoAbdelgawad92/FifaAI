import numpy as np
import random as rand
import cv2
from raycast import raycast
from gamebase import Goal,Ball,Player

class Game():
    def __init__(self,rows=45,cols=91):
        self.world = np.zeros((rows,cols))
        self.hight = rows
        self.width = cols
        # self goal 
        self.goalLeft  = Goal(True ,10,self.world.shape)
        self.goalRight = Goal(False,10,self.world.shape)
        self.RGB = False
        self.reward = 0
        self.n_actions = 5
        self.observation_shape = self.reset().shape

    def reset(self):
        self.world  = np.zeros(self.world.shape)
        self.player = Player(rand.randint(1,self.hight-1),rand.randint(1,self.width-1),self.world.shape,2)
        self.ball   =   Ball(rand.randint(1,self.hight-1),rand.randint(1,self.width-1),self.world.shape,128)
        self.reward = 0
        observation = raycast([self.ball],self.player)
        return observation

    def takeAction(self,action):
        self.player.move(action)
        self.ball.move(action,self.player)
    
    def CheckGameStatus(self):
        if self.goalLeft.isBallInGoal(self.ball): return - 50
        elif self.goalRight.isBallInGoal(self.ball): return 50
        else: return 0

    
    def step(self,action,state):
        done = 0
        self.takeAction(action)
        observation = raycast([self.ball],self.player)
        goal = self.CheckGameStatus()
        if abs(state[-2]) < abs(state[-4]):
            self.reward += 1
        if self.ball.checkPlayerHasBall(self.player):
            self.reward = 500
            done = 1
        # if goal == -50 :
        #     self.reward = 0
        #     done = 1
        # elif goal == 50:
        #     self.reward += goal
        #     done = 1
        # else:
        #     pass
        return observation, self.reward, done,"",f"player: {self.player.loc}, ball: {self.ball.loc}, reward: {self.reward}."
    

    def _fillCanvas(self,listOfObj):
        # self.world   = np.zeros((45,91))
        if self.RGB:
            renderCanves = np.zeros((450,910,3))
            for element in listOfObj:
                self.world[element.h,element.w] = 1
                renderCanves[element.h*10:element.h*10+element.size,
                             element.w*10:element.w*10+element.size] = element.color
            return renderCanves

    def render(self,RGB = True,Manual = False):
        self.RGB = RGB
        if self.RGB:
            img = self._fillCanvas([self.goalLeft,self.goalRight,self.player,self.ball])
            cv2.imshow("game",img)
            if not Manual:
                return cv2
            key = cv2.waitKey(0) % 256 
            if key == ord('s'):
                x = self.takeAction(1)
            elif key == ord('w'):
                x = self.takeAction(2)
            elif key == ord('d'):
                x = self.takeAction(3)
            elif key == ord('a'):
                x = self.takeAction(4)
            else:
                return
            
            
        