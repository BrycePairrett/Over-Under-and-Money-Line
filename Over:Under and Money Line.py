#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 11:34:56 2020

@author: bryce
"""


import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random 
import pandas as pd
import os
import warnings

df1 = pd.read_excel(r'/Users/bryce/Documents/Python/NBA_PROJECT/nba odds 2018-19.xlsx', sheet_name = 'OVER UNDERS')
df2 = pd.read_excel(r'/Users/bryce/Documents/Python/NBA_PROJECT/nba odds 2018-19.xlsx', sheet_name='DATA')

overUnder = df1["Open"].to_list()
gameTotal = df1["Total Scores"].to_list()
Team = df2["Team"].to_list()
Score = df2["Final"].to_list()
ML = df2["ML"].to_list()
HomeOrAway =df2['VH'].to_list()
AtlanticDiv = ['Boston', 'Brooklyn', 'NewYork', 'Philadelphia','Toronto']
CentralDiv = ['Chicago', 'Cleveland', 'Detroit', 'Indiana', 'Milwaukee']
SouthEastDiv = ['Atlanta', 'Charlotte', 'Miami', 'Orlando', 'Washington']
SouthWestDiv = ['Dallas', 'Houston', 'Memphis', 'NewOrleans', 'SanAntonio']
NorthWestDiv = ['Denver', 'Minnesota', 'OklahomaCity', 'Portland', 'Utah']
PacificDiv = ['GoldenState', 'LAClippers', 'LALakers', 'Phoenix', 'Sacramento']
NBA = ['Boston', 'Brooklyn', 'NewYork', 'Philadelphia','Toronto','Chicago', 'Cleveland', 'Detroit', 'Indiana', 'Milwaukee','Atlanta', 'Charlotte', 'Miami', 'Orlando', 'Washington','Dallas', 'Houston', 'Memphis', 'NewOrleans', 'SanAntonio','Denver', 'Minnesota', 'OklahomaCity', 'Portland', 'Utah','GoldenState', 'LAClippers', 'LALakers', 'Phoenix', 'Sacramento']


def moneyLine(teamName):
    counter = 0
    wager = 100 # wagering 100 dollars per game 
    balance = 0  
    while counter < len(Team):
        x = ML[counter] #gets the betting odds for a win or a loss
        if teamName == Team[counter]:
            if HomeOrAway[counter] == 'V':
                if Score[counter]> Score[counter+1]:    # the way the spreadsheet is formatted the 'V' or visiting is always the 
                                                        # row above their opponents. so to get the opposing team data we must 
                                                        # increase the index by 1 and vice versa if they were the home team
                    if x> 0:
                        return_rate = x/100         #turns into a rate for favored games
                    else: 
                        return_rate = (100/x) * -1
                    amt = wager * return_rate     #takes the correct rate of return and multiplys it by the wagered amount
                    balance += amt
                else:
                    balance += (wager * -1)          
            else: 
                if Score[counter]> Score[counter-1]:
                    if x> 0:
                        return_rate = x/100         #turns into a rate for favored games
                    else: 
                        return_rate = (100/x) * -1
                    amt = wager * return_rate     #takes the correct rate of return and multiplys it by the wagered amount
                    balance += amt
                else:
                    balance += (wager * -1)      
                
                #this accounts for the losses thats why the wager is multiplied by negative one to correctly add the total
        counter +=1       
    #print(f'This is how much you would owe or make, ${balance:.2f}')
    return round((balance),2)


def gamesWon(teamName):
    counter = 0 
    homeWins = 0
    homeLosses = 0 
    awayWins = 0
    awayLosses = 0
    while counter < len(Team):
        if teamName == Team[counter]:
            if HomeOrAway[counter]=='H':
                if Score[counter]> Score[counter-1]:
                    homeWins +=1 
                else:
                    homeLosses +=1
        
            else: 
                if Score[counter] > Score[counter+1]:
                    awayWins +=1 
                else: 
                    awayLosses +=1 
        counter +=1
    print()
    print("{} 2019 record".format(teamName))  
    print()
    print("Home Record: ", homeWins, "-", homeLosses, "(", round(homeWins/(homeWins + homeLosses),3), ")")
    print("Away Record: ", awayWins, "-", awayLosses, "(", round(awayWins/(awayWins + awayLosses),3),")")
    print("Overall Record: ", homeWins+awayWins, "-", homeLosses+awayLosses, "(", round((homeWins+awayWins)/(homeWins+homeLosses + awayWins+awayLosses),3),")")

gamesWon

def overUndercalc(): # this calculates the overal percentage of over vs unders for the 2019 season and also takes into account pushes
    counter = 0 
    overHit = 0
    underHit = 0 
    push = 0
    
    for score in gameTotal:
        if gameTotal[counter]> overUnder[counter]:
            overHit +=1 
        elif gameTotal[counter]< overUnder[counter]:
            underHit +=1
        else: 
            push +=1 
        counter +=1 
    print()
    print("Your 2019 over/under statistics")       
    print("Over: ", round(overHit/len(gameTotal),3))
    print("Under: ", round(underHit/len(gameTotal),3))
    print("Push: ", round(push/len(gameTotal),3))
    return overHit, underHit, push
    

def overUnderSim(simulations): #based on 100 dollar bets paying(-110) or 90.90 dollars 
    global winList
    winList = []
    for num in range(simulations):
    
        money = 0
        counter = 0 
        while counter<len(overUnder):
                
            OverorUnder = random.randint(0,1) # this represents randomly selecting over or under 
               
            if OverorUnder == 0: 
                if gameTotal[counter]>overUnder[counter]:
                    money += 90.90
                elif gameTotal[counter]<overUnder[counter]:
                    money -= 100
                        
            else: 
                if gameTotal[counter]>overUnder[counter]:
                    money -= 100
                elif gameTotal[counter]<overUnder[counter]:
                    money -+ 90.90
            counter+=1 
        winList.append(money)
    
    return winList
 
    
def testMoneyLine(division):# this is test function that calls the moneyLine function for each team in a division
    global mlList
    mlList = []
    for team in division:
        x = moneyLine(team)
        mlList.append(x)
        
    df = pd.DataFrame({'team':NBA, 'val':mlList})
    ax = df.plot.bar(x= 'team', y = 'val')  
    
    
def testGamesWon(division): # this return the record of each team 
    for team in division:
        gamesWon(team)


def overUnderScatter(): # this returns a scatter plot of an over/under simulation     
    n = 500
    x = np.random.rand(n)
    y = winList
    colors = (0,0,0)    
    plt.scatter(x,y, c=colors, alpha = 0.5)
    plt.set(title="Over Under Sim Returns")
    plt.ylabel('Profit')
    plt.xaxis('U.S. Dollar (Thousands)')
    plt.show()
   
def overUnderPie():
    labels = ['Over', 'Under', 'Push']
    sizes = [overUndercalc()]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
    ax1.axis('equal')
    ax1.set(title='Over/Under Pie Chart')
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    plt.show()
    
testMoneyLine(NBA)

testGamesWon(NBA)

overUndercalc()

overUnderSim(500) # i need to run this in order to have winList for the scatter plot

overUnderPie()

    
