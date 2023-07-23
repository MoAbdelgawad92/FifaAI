
class Point():
    def __init__(self,h,w,gameShape,Ptype,size = 0,color = [0,0,0]):
        self.h = h
        self.w = w
        self.size = size
        self.color = color
        self.action = 0
        self.type = Ptype
        self.gameShape = gameShape
        self.loc = (h,w)
    
    def move(self,action):
        if action == 0  : return # dont move
        if self.h + 1 == self.gameShape[0]: 
            self.h -= 1
            return
        if self.h - 1 == -1: 
            self.h += 1
            return
        if self.w - 1 == -1: 
            self.w += 1
            return
        if self.w + 1 == self.gameShape[1]: 
            self.w -= 1
            return
        
        if action == 1  : self.h += 1 # move down 
        elif action == 2: self.h -= 1 # move up  
        elif action == 3: self.w += 1 # move right
        elif action == 4: self.w -= 1 # move left
        else            : print("error unsupported action")
        self.action = action

class Goal(Point):
    def __init__(self,side,size,gameShape):
        self.side = side        
        self.top = gameShape[0]//2 - size
        self.bot = gameShape[0]//2 + size
        h = self.top
        if(side):
            w = gameShape[1]-1
            Ptype = 200
        else:
            w = 0
            Ptype = 201
        
        super().__init__(h,w,gameShape,Ptype,size,color=[0,255,0])
    def move(self, action):
        pass
        return
        
    
    def isBallInGoal(self,ball):
        if self.side:
            if ball.w != 0: return False
            if ball.h > self.top and ball.h < self.bot: 
                return True
            return False
        else:
            # to fix to be on the Right
            if ball.w != self.gameWidth: return False
            if ball.h > self.top and ball.h < self.bot: 
                return True
            return False

class Player(Point):
    def __init__(self,h,w,gameShape,Ptype):
        super().__init__(h,w,gameShape,Ptype,size = 20,color=[255,255,255])
    
class Ball(Point):
    def __init__(self,h,w,gameShape,Ptype):
        super().__init__(h,w,gameShape,Ptype,size =10,color=[255,0,0])

    def checkPlayerHasBall(self,player):
        if self.h not in [player.h-1,player.h,player.h+1]: return 0
        if self.w not in [player.w-1,player.w,player.w+1]: return 0
        return 1

    def move(self,action,player):
        if not self.checkPlayerHasBall(player): return
        self.h = player.h
        self.w = player.w
        super().move(action)
