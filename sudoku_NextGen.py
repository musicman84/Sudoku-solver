#USE: Make sure that example file sudokuExample.txt and Python code are in the same file

#Every square in the board is a node

class node:
    
    #Data structure used.. node: Each node has its own unique node number
    #                      x,y: Coordinates of node in board
    #                      block: Defines which of the 9 3x3 blocks the node belongs to
    #                      opt: Possible solution values for the node stored as a list
    #                           note when len(opt)==1 the solution is found at the node
    
    def __init__(self,node=0,x=0,y=0,block=0,opt=range(1,10)):
        self.node=node#define data entries for class and set value as argument
        self.x=x
        self.y=y
        self.block=block
        self.opt=opt

    def setentry(self,sol):
        self.opt=[int(sol)]
        

    def removeentry(self,number):
        #This method removes a number from a list, normally use 'remove' standard method but had problems with it.
        temp=[]
        for i in self.opt:
            if i==number: 
                pass 
            else: #could have used 'if not' instead
                temp.append(i)            
        self.opt=temp


    def printNode(self):
        #simply prints out the data associated with a node object, used for debugging
        print (str(self.node)+':' + \
              str(self.x)+':' + \
              str(self.y)+':' + \
              str(self.block)+':' + \
              str(self.opt))
        
        
#make an ordered container class for all nodes called board
class board:
    def __init__(self,nextNode=None,nextOpt=[]):#Initialise board
        self.nodes=[]
        count=0
        for i in range(9):
            for j in range(9):
                block=int(i/3)*3+int(j/3)
                self.nodes.append(node(count,i,j,block))#initialising nodes
                count+=1
                
    def printBoard(self):#Print current board, for debugging
        for i in self.nodes:
            i.printNode()


    def loadBoard(self):#Load in from data file
        import os
        cwd=os.getcwd() #get local file directory
        file_read = open('AI Escargot.txt','r')#open file to read
        for i in range(9):
            lineAsRead=file_read.readline()
            lineAsRead=lineAsRead.rstrip('\n') #remove \n from end of string
            lineSplit=lineAsRead.split(',')
            for j in range(9):
                if lineSplit[j]=='*':
                    pass
                else:
                    self.setsolution(i,j,lineSplit[j])

    def writesoltoscreen(self):#write final solution to screen
        solList=[[0 for j in range(9)] for i in range(9)]#define empty 9x9 array
        self.PutBoardInList(solList)
        for i in range(9):
            print(solList[0:9][i])

    def PutBoardInList(self,solList): #reformat solution for screen print
        for i in range(81):
            row=self.nodes[i].x
            col=self.nodes[i].y
            if len(self.nodes[i].opt)==1:
                solList[row][col]=self.nodes[i].opt[0]
            else:
                solList[row][col]=0

        return solList
    

    def setsolution(self,ith,jth,sol):#removes all other entries from opt list other than known solution
        for i in range(81):
            if self.nodes[i].x==ith:
                if self.nodes[i].y==jth:
                    self.nodes[i].setentry(sol)


    #Solve method: Beginning of main solver: loops through every node checking if solution is known.
    #If solution is known it calls cancel function.
    #If progress==False then solve is done on one node only, not a loop

    def solve(self,node=0):
        if len(self.nodes[node].opt)==1:#check that current node is solved
            #print 'solve sent :'+str(self.nodes[node].x)+','+str(self.nodes[node].y)
            self.cancel(self.nodes[node].x, self.nodes[node].y, self.nodes[node].block, self.nodes[node].opt[0])

        if node<80:
            self.solve(node+1)#Progress to next node

    #Cancel method: When known solution is found-> remove the solution as a possible solution for all nodes in the same
    #row, column and block.

    def cancel(self,xth,yth,blockth, value):
        #remove options based on current solution
        for i in range(81):
            if self.nodes[i].x==xth or self.nodes[i].y==yth or self.nodes[i].block==blockth:
                if int(value) in self.nodes[i].opt:
                    if len(self.nodes[i].opt)>1:# check that the solution isn't already found
                        self.nodes[i].removeentry(value)
                        if len(self.nodes[i].opt)==1:
                            self.cancel(self.nodes[i].x, self.nodes[i].y, self.nodes[i].block, self.nodes[i].opt[0])

    #If during cancellation process a new known solution is given
    #then the new solution is used as the start of a new chain of cancellation calls.

    def checkSol(self,solved=True):
        #check each node only has one solution
        optLen=10
        for i in range(81):
            if len(self.nodes[i].opt)>1:
                solved=False
                if len(self.nodes[i].opt)<optLen:
                    self.optLen=len(self.nodes[i].opt)
                    self.nextNode=i
                    self.nextOpt=self.nodes[i].opt
                #print(self.optLen,self.nextNode,self.nextOpt)
                return solved
            
        #check that solution is valid
        #creating check lists for each row, column and block
        rowCheck=[[1,2,3,4,5,6,7,8,9] for i in range(9)]
        colCheck=[[1,2,3,4,5,6,7,8,9] for i in range(9)]
        blockCheck=[[1,2,3,4,5,6,7,8,9] for i in range(9)]

        #check there is no duplication within any column, row or block
        for i in range(81):
            #print(rowCheck[self.nodes[i].x][self.nodes[i].opt[0]-1])
            if rowCheck[self.nodes[i].x][self.nodes[i].opt[0]-1]==0:
                solved=False
                return solved
            else:
                rowCheck[self.nodes[i].x][self.nodes[i].opt[0]-1]=0
        for i in range(9):
            for j in range(9):
                if rowCheck[i][j]!=0:
                    solved=False
                    return solved

        for i in range(81):
            #print(colCheck[self.nodes[i].x][self.nodes[i].opt[0]-1])
            if colCheck[self.nodes[i].y][self.nodes[i].opt[0]-1]==0:
                solved=False
                return solved
            else:
                colCheck[self.nodes[i].y][self.nodes[i].opt[0]-1]=0
        for i in range(9):
            for j in range(9):
                if colCheck[i][j]!=0:
                    solved=False
                    return solved

        for i in range(81):
            #print(rowCheck[self.nodes[i].x][self.nodes[i].opt[0]-1])
            if blockCheck[self.nodes[i].block][self.nodes[i].opt[0]-1]==0:
                solved=False
                return solved
            else:
                blockCheck[self.nodes[i].block][self.nodes[i].opt[0]-1]=0
        for i in range(9):
            for j in range(9):
                if blockCheck[i][j]!=0:
                    solved=False
                    return solved
                
        return solved
                            
class solutionSpace:
    def __init__(self):
        self.solList=[]
        self.solList.append(board())#define data entries for class and set value as argument

    def loadBoard(self):
        self.solList[0].loadBoard()

    def solve(self):
        flag=True
        while flag:
            self.solList[0].solve()

            #Uncomment below to write solution to screen (ugly format)
            #print ('Data Structure')
            #solSpace.solList[0].printBoard()
            #solSpace.solList[0].writesoltoscreen()

            #check if solution is found
            if self.solList[0].checkSol():
                print ('Solution')
                self.solList[0].writesoltoscreen()
                flag=False
            else:#if solution isn't found
                print ('Searching')
                for i in self.solList[0].nextOpt:
                    holder=copy.deepcopy(self.solList[0])#copy previous partial solution
                    holder.nodes[self.solList[0].nextNode].setentry(i)#set entry into new partial solutions
                    self.solList.append(holder)
            
                self.solList.pop(0)#remove previous partial solution from list
######Main Program######
import copy #allows copying of objects

solSpace=solutionSpace()
solSpace.loadBoard()
solSpace.solve()

        







