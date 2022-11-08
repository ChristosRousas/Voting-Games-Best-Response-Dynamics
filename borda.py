import numpy as np
import matplotlib as plt
import csv
from sys import argv

class Player:
    def __init__(self):
        self.preferences = []
        self.choice = []
    def getPref(self):
        return self.preferences
    def setPref(self,pref):
        self.preferences = list(pref)
    
    def utilityCandidate(self,i): #Calculates player's utility for i-th candidate
        return len(self.preferences)-self.preferences.index(i)
    
    def calculateResult(self,choices):
        m = len(self.preferences)
        result = [0 for i in range(m)]
        for i in range(len(choices)):
            for j in range(m):
                result[choices[i][j]] += (m-j-1) # borda rule score
        return result
    
    def canChange(self,choices,i): # returns change to increase utility (or nothing)
        result = self.calculateResult(choices) # results of starting choices
        winner = result.index(max(result)) # winner of starting choices
        inChoice = choices[i]
        if winner == inChoice[0]: # skip players that their choice is winning
            return inChoice
        m = len(self.preferences)-1
        choice = choices[i][:]
        others = choice[1:] # every candidate except wanted winner
        othersScores = [result[j] for j in others]
        o = others[:] # duplicate others list for key function
        others.sort(key = lambda j: othersScores[o.index(j)]) # sort others by score
        othersScores.sort()
        choice = choice[:1]+others
        choices[i] = choice
        newResult = self.calculateResult(choices) # results of new choices
        newWinner = newResult.index(max(newResult)) # winner of new choices
        if self.utilityCandidate(newWinner)>self.utilityCandidate(winner):
            return choice
        return inChoice


def csvToTable(csvName):
    with open(csvName, 'r', encoding='utf-8-sig') as read_obj:
    
        # Return a reader object which will
        # iterate over lines in the given csvfile
        csv_reader = csv.reader(read_obj)
      
        # convert string to list
        list_of_csv = list(csv_reader)
        list_of_csv = [[int(i) for i in x] for x in list_of_csv]

        return list_of_csv


def createRandomGame(n,m,seed):
    lista = []
    #lista = [[0, 2, 1, 3],[1, 0, 2, 3],[1, 0, 3, 2],[2, 0, 3, 1]]
    for i in range(n):
        lista.append(np.random.RandomState(seed+8*i).permutation(m))
    return lista


def brd(game):
    n,m = np.asarray(game).shape
    players,choices = [],[]
    for i in range(n):
        players.append(Player())
        players[i].setPref(game[i])
        choices.append(players[i].getPref())
        players[i].choice = choices[i]
    
    resultStart = players[0].calculateResult(choices) # results of starting choices

    print()
    for t in range(1000):
        isPlayer = False
        for p in players:
            i = players.index(p)
            choice = p.choice
            newChoice = p.canChange(choices[:],i) # changed (or not) choice
            if choice != newChoice: # if choice is changed
                p.choice = newChoice
                choices[i] = newChoice
                isPlayer = True
                break # go to next round
        if isPlayer == False: # no player wants to change
            print("Nash Equilibrium, ended at",t,"iterations.")
            print()
            resultEnd = players[0].calculateResult(choices)
            return choices, t, resultStart, resultEnd
    print("Limit exceeded, nothing found",i)




def main(argv):
    
    if argv[1] == "random":
        n,m = int(argv[2]),int(argv[3])
        game = createRandomGame(n,m,0)
        choices = brd(game)
        for i in range(len(choices[0])):
            print(choices[0][i])
    
    elif argv[1] == "csv":
        game = csvToTable(argv[2])
        choices = brd(game)
        for i in range(len(choices[0])):
            print(choices[0][i])
    
    elif argv[1] == "test":
        
        n_list = [5,10,20,40]
        m_list = [5,10,15,20]
        print("Testing for", str(n_list)[1:-1], "players")
        print("and", str(m_list)[1:-1], "candidates")
        choice_data = [[],[],[],[],[],[],[]]
        for n in n_list:
            for m in m_list:
                for i in range(20):
                    game = createRandomGame(n,m,i)
                    choiceStart = game
                    c = brd(game) # output of brd
                    resultStart = c[2]
                    resultEnd = c[3]
                    winnerStart = resultStart.index(max(resultStart))
                    winnerEnd = resultEnd.index(max(resultEnd))
                    choice_data[0].append(n) # no. of players
                    choice_data[1].append(m) # no. of candidates
                    choice_data[2].append(c[2]) # starting choices
                    choice_data[3].append(c[0]) # final strategy
                    choice_data[4].append(winnerStart)
                    choice_data[5].append(winnerEnd)
                    choice_data[6].append(c[1]) # no. of iterations
        
        # get data for report
        
        #c,s,c2,s2 = 0,0,0,0
        #for i in range(len(choice_data[6])):
        #    num = choice_data[6][i]
        #    c+=1
        #    s+=num
        #    if num != 0:
        #        c2+=1
        #        s2+=num
        #print(s/c)
        #print(s2/c2)
        #
        #c,s = 0,0
        #for i in range(len(choice_data[2])):
        #    rStart = choice_data[2][i]
        #    wStart = choice_data[4][i]
        #    wEnd = choice_data[5][i]
        #    print(rStart[wEnd]-rStart[wStart], wStart, wEnd)
        
        
        
        choice_out_data = np.array(choice_data,dtype=object).T.tolist()
        with open("out.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(choice_out_data)
    



if __name__ == "__main__":
    main(argv)
