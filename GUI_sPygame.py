# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 18:20:44 2020

@author: Richard
"""

import pygame
import numpy as np

# zacina clovek hrat, veliksot 3 vyherni je idealni, vic nema dopsany algoritmus pro chytre hrani
field_size=6
win_count=3
min_pixels=100

zer = np.zeros((field_size,field_size))
matice=zer
#matice[3][3]=2

red_x = pygame.image.load("red_x1.png")
blue_o = pygame.image.load("blue_o1.png")
tnk=pygame.image.load("thinking.jpg")

# Graphics functions:     
     
def grid_count_draw(size_of_game_grid,min_pixel_size_grid):
    
    for i in range(size_of_game_grid-1):
        pygame.draw.line(screen, (0, 0, 0), (0,(i+1)*min_pixel_size_grid), (size_of_game_grid*min_pixel_size_grid,(i+1)*min_pixel_size_grid), 2)
     
    for i in range(size_of_game_grid):
        pygame.draw.line(screen, (0, 0, 0), ((i+1)*min_pixel_size_grid,0), ((i+1)*min_pixel_size_grid,size_of_game_grid*min_pixel_size_grid), 2)
    
def draw_array(numpy_array,min_pixels):
       # Drawing the symbols from array to the pygame screen
       # Finding matches for player 1
       #print("kreslim mapu hry z matice")
       found1=np.where(numpy_array == 1)
      # print(found1)
       for i in range(len(found1[0])):
           x=found1[1][i]*min_pixels+min_pixels/2
           y=found1[0][i]*min_pixels+min_pixels/2
          
           # pygame.draw.circle(screen, (0, 0, 255), (x,y), 25)
           screen.blit(red_x,(x-45,y-45))
       found1=np.where(numpy_array == 2)    
       for i in range(len(found1[0])):
           x=found1[1][i]*min_pixels+min_pixels/2
           y=found1[0][i]*min_pixels+min_pixels/2
           
           screen.blit(blue_o,(x-45,y-45))

def take_clicked_field_to_array(tuple_mouse_coordinates,min_pixel_size_grid,numpy_array):
    # Putting the mouse cursor click pose into array/matrix as a number 1
      #print("Pocitam pozici kurzoru v mrizce") 
      # rows
      a_x=divmod(tuple_mouse_coordinates[0],min_pixel_size_grid) #
      column_clicked=a_x[0]
      # columns
      a_x=divmod(tuple_mouse_coordinates[1],min_pixel_size_grid) #
      row_clicked=a_x[0]
      numpy_array[row_clicked,column_clicked]=1
      #print(numpy_array)
      return numpy_array

def ifwin(numpy_array,how_many_to_win):
    global no_winner
    # see if someone has win or not and write a message
    a=win_rows_count(numpy_array,1,how_many_to_win)
    b=win_collumns_count(numpy_array,1,how_many_to_win)
    c=win_diagonal_count(numpy_array,1,how_many_to_win)
    # Musi se pridat c diagonala
    print("vyhry abc") 
    print(a)
    print(b)
    print(c)
    font = pygame.font.SysFont("verdana", 56)
    if (a+b+c)!=0:
        print("vyrahl hrac 1 -clovek") 
        text = font.render("Vyhral jsi :-)!", True, (0, 0, 0))
        textRect = text.get_rect()  
        textRect.center = (min_pixels*(field_size) // 2, min_pixels*(field_size) // 2) 
        screen.blit(text, textRect) 
        pygame.display.flip()
        no_winner= False
        return False
    a1=win_rows_count(numpy_array,2,how_many_to_win)
    b1=win_collumns_count(numpy_array,2,how_many_to_win) 
    c1=win_diagonal_count(numpy_array,2,how_many_to_win)
    if (a1+b1+c1)!=0:
        print("vyrahl hrac 2 -clovek") 
        text = font.render("PROHRÁL JSI! :-(!", True, (0, 0, 0))
        textRect = text.get_rect()  
        textRect.center = (min_pixels*(field_size) // 2, min_pixels*(field_size) // 2) 
        screen.blit(text, textRect) 
        pygame.display.flip()
        no_winner= False 
        return False
       
  # hraci funkce 

    
# Playing functions:     
def win_rows_count(Play_matrix,win_number,win_count):
    # count all possible wins in rows of input matrix
    # Matrix: 1 - player1, 2- player 2, 0 - empty space
    # Inputs: play matrix = square matrix of playing, 
    # Win number - which numbers in matrix are winning
    # Win count *- how many symbols in a row do we need to win
    possible_wins=0  
    a=len(Play_matrix)
    for i in range(a):
    #iterative for each row:
     radek=Play_matrix[i]
     for j in range(a-win_count+1):
            if radek[j]==win_number:
                if sum(radek[j:(j+win_count)])==win_number*win_count and all(x==radek[j:(j+win_count)][0] for x  in radek[j:(j+win_count)]):
                    possible_wins+=1
            # returning win coun as int for the winni
    return possible_wins

def win_collumns_count(Play_matrix,win_number,win_count):
    # count all possible wins in rows of input matrix
    # Matrix: 1 - player1, 2- player 2, 0 - empty space
    # Inputs: play matrix = square matrix of playing, 
    # Win number - which numbers in matrix are winning
    # Win count *- how many symbols in a row do we need to win
    possible_wins=0  
    a=len(Play_matrix)
    for i in range(a):
    #iterative for each row:
     sloupec=Play_matrix[:,i]
     for j in range(a-win_count+1):
            if sloupec[j]==win_number:
                if sum(sloupec[j:(j+win_count)])==win_number*win_count and all(x==sloupec[j:(j+win_count)][0] for x  in sloupec[j:(j+win_count)]):
                    possible_wins+=1
            # returning win coun as int for the winni
    return possible_wins  

def win_diagonal_count(Play_matrix,win_number,win_count):
    # count all possible diagonal
    # Matrix: 1 - player1, 2- player 2, 0 - empty space
    # Inputs: play matrix = square matrix of playing, 
    # Win number - which numbers in matrix are winning
    # Win count *- how many symbols in a row do we need to win
    
    # numpy.diagonal
    possible_wins=0  
    a=len(Play_matrix)
    b=a+1-win_count
    for i in range(-b,b):
    #iterative for each row:
     diagonal=Play_matrix.diagonal(i)
     for j in range(len(diagonal)):
            if diagonal[j]==win_number:
                if sum(diagonal[j:(j+win_count)])==win_number*win_count and all(x==diagonal[j:(j+win_count)][0] for x  in diagonal[j:(j+win_count)]):
                    possible_wins+=1
            # returning win coun as int for the winnir
    # For other side diagonals
    Play_matrix=np.fliplr(Play_matrix)
    for i in range(-b,b):
    #iterative for each row:
     diagonal=Play_matrix.diagonal(i)
     for j in range(len(diagonal)):
            if diagonal[j]==win_number:
                if sum(diagonal[j:(j+win_count)])==win_number*win_count and all(x==diagonal[j:(j+win_count)][0] for x  in diagonal[j:(j+win_count)]):
                    possible_wins+=1
            # returning win coun as int for the winnir
    return possible_wins  

def is_this_number_winning(matice_vstup,cislo_hrace,win_count):
     a=win_rows_count(matice_vstup,cislo_hrace,win_count)
     b=win_collumns_count(matice_vstup,cislo_hrace,win_count)
     c=win_diagonal_count(matice_vstup,cislo_hrace,win_count)
    
     if a+b+c>0:
        return True
     else:
        return False
    
        
# Computers move functions: 
def someone_is_winning(matice_vstup,win_count):
     a=win_rows_count(matice_vstup,1,win_count)
     b=win_collumns_count(matice_vstup,1,win_count)
     c=win_diagonal_count(matice_vstup,1,win_count)
    
     if a+b+c>0:
        return 1
   
     a=win_rows_count(matice_vstup,2,win_count)
     b=win_collumns_count(matice_vstup,2,win_count)
     c=win_diagonal_count(matice_vstup,2,win_count)
    
     if a+b+c>0:
        return 2
     else:
        return 0

def player_is_winning(matice_vstup,cislo_hrace,win_count):
     a=win_rows_count(matice_vstup,cislo_hrace,win_count)
     b=win_collumns_count(matice_vstup,cislo_hrace,win_count)
     c=win_diagonal_count(matice_vstup,cislo_hrace,win_count)
    
     if a+b+c>0:
        return cislo_hrace
     else:
        return 0
    
def hodnoty_n_minus_1_matic(matice_vstupni,hledam,cislo_hrace,win_count):
    x_best=0
    y_best=0
    score=0
    pomocna=matice_vstupni.copy()
    found1=np.where(pomocna == 0)
    # udela vsecky mozne tahy matice
    # vrati scores 
    scores=np.zeros((1,len(found1[0])))
    for i in range(len(found1[0])):
           pomocna=matice_vstupni.copy()
           x=found1[1][i]
           y=found1[0][i]
           pomocna[y,x]=cislo_hrace
           # Kontrola, jestli ten aktualni stav vitezny, pak score, cislo hrace, jinak nula
           a=player_is_winning(pomocna,cislo_hrace,win_count)
           if a != 0:
               scores[0][i]=a
              # print("somtu")

    if np.sum(scores) != 0:
        if hledam=="maximum":
           # print("hledam max")
            # hledam ty dvojky
            index=np.where(scores==2)
            x_best=found1[1][index[1][0]]
            y_best=found1[0][index[1][0]]
            score=cislo_hrace
        if hledam=="minimum":
           # print("hledam min")
            # hledam jednicky
            index=np.where(scores==1)
            x_best=found1[1][index[1][0]]
            y_best=found1[0][index[1][0]]
            score=cislo_hrace
    # vraci to skore, jhestli se hleda max nebo min a potom x best, y best, kdyz nenajde, tak nuly
    return score,x_best,y_best
    
def tahy_2_dopredu(matice_vstupni,win_count):
    # prohledavani od hloubka 3::
    x_best=0
    y_best=0
    cislo_hrace=2  # prvni tahne PC
    b=0
    pomocna=matice_vstupni.copy()
    print(pomocna)
    found1=np.where(pomocna == 0)
    print(found1)
    scores=np.zeros((1,len(found1[0])))
    for i in range(len(found1[0])):
           pomocna=matice_vstupni.copy()
           x=found1[1][i]
           y=found1[0][i]
           pomocna[y,x]=cislo_hrace
           a=player_is_winning(pomocna,cislo_hrace,win_count)
           if a != 0:
               # dalsi tah pocitace je vyherni
               x_best=x
               y_best=y               
               b=1
               print("pocitac vyhraje dalsim tahem")
               break
           # zkouma dalsi mozne tahy cloveka z matice pomocna, hleda to minimum, teda to, kde je hodnoceni 1
           hodnota,x,y=hodnoty_n_minus_1_matic(pomocna, "minimum", 1, win_count)
           scores[0][i]=hodnota
           print(scores)
    if np.sum(scores) != 0 and b !=1 and (0 in scores):
            b=1
            print("hledam max")
            # hledam ty dvojky
            index=np.where(scores==0)
            x_best=found1[1][index[1][0]]
            y_best=found1[0][index[1][0]]
    if b==0:
        print("jsem v bode b==0")
        x_best=found1[1][0]
        y_best=found1[0][0]
        
    matice_vstupni[y_best,x_best]=2 
    print("xy best je:")    
    print(x_best)
    print(y_best)
    return matice_vstupni  

def tahy_3_dopredu(matice_vstupni,win_count):
    # prohledavani od hloubka 3::
    x_best=0
    y_best=0
    cislo_hrace=2  # prvni tahne PC
    b=0
    pomocna=matice_vstupni.copy()
    print(pomocna)
    found1=np.where(pomocna == 0)
    print(found1)
    scores=np.zeros((1,len(found1[0])))
    for i in range(len(found1[0])):
           pomocna=matice_vstupni.copy()
           x=found1[1][i]
           y=found1[0][i]
           pomocna[y,x]=cislo_hrace
           a=player_is_winning(pomocna,cislo_hrace,win_count)
           if a != 0:
               # dalsi tah pocitace je vyherni
               x_best=x
               y_best=y               
               b=1
               print("pocitac vyhraje nasledujicim tahem")
               break
           # zkouma dalsi mozne tahy cloveka
           found2=np.where(pomocna == 0)
           pomocna2=pomocna.copy()
           cislo_hrace2=1   # hraje clovek
           scores2=np.zeros((1,len(found2[0])))
           for j in range(len(found2[0])):
               pomocna2=pomocna.copy()
               x2=found2[1][j]
               y2=found2[0][j]
               pomocna2[y2,x2]=cislo_hrace2
               a2=player_is_winning(pomocna2,cislo_hrace2,win_count)
               if a2 != 0:
               # dalsi cloveka je vyherni
                   x_best2=x2
                   y_best2=y2               
                   b=2
                   print("clovek vyhraje druhym tahem")
                   scores2[0][j]=1
                   break
               hodnota2,x2,y2=hodnoty_n_minus_1_matic(pomocna2, "maximum", 2, win_count)
               scores2[0][j]=hodnota2
           
           #hodnota,x,y=hodnoty_n_minus_1_matic(pomocna, "minimum", 1, win_count)
           scores[0][i]=np.amin(scores2)
           print(scores)
    if np.sum(scores) != 0 and b !=1 and (0 in scores):
            b=1
            print("hledam max")
            # hledam ty dvojky
            index=np.where(scores==2)
            x_best=found1[1][index[1][0]]
            y_best=found1[0][index[1][0]]
            matice_vstupni[y_best,x_best]=2
    if b==0:
        print("hledam nahradni reseni:")
        #x_best=found1[1][0]
       # y_best=found1[0][0]
        matice_vstupni=nahradni_reseni_kdyz_strom_nic(matice_vstupni,win_count)
    if b==2:
        print("jsem v bode b==2")
        x_best=x_best2
        y_best=y_best2
        matice_vstupni[y_best,x_best]=2
    if b==1:
        matice_vstupni[y_best,x_best]=2
    
    
   # print("xy best je:")    
   # print(x_best)
   # print(y_best)
    return matice_vstupni  

def tahy_rekurze(matice_vstupni,win_count):
    # prohledavani od hloubka 3::
    x_best=0
    y_best=0
    cislo_hrace=2  # prvni tahne PC
    b=0
    pomocna=matice_vstupni.copy()
    print(pomocna)
    found1=np.where(pomocna == 0)
    print(found1)
    scores=np.zeros((1,len(found1[0])))
    for i in range(len(found1[0])):
           pomocna=matice_vstupni.copy()
           x=found1[1][i]
           y=found1[0][i]
           pomocna[y,x]=cislo_hrace
           a=player_is_winning(pomocna,cislo_hrace,win_count)
           if a != 0:
               # dalsi tah pocitace je vyherni
               x_best=x
               y_best=y               
               b=1
               print("pocitac vyhraje nasledujicim tahem")
               break
           # zkouma dalsi mozne tahy cloveka
           found2=np.where(pomocna == 0)
           pomocna2=pomocna.copy()
           cislo_hrace2=1   # hraje clovek
           scores2=np.zeros((1,len(found2[0])))
           
    if np.sum(scores) != 0 and b !=1 and (0 in scores):
            b=1
            print("hledam max")
            # hledam ty dvojky
            index=np.where(scores==2)
            x_best=found1[1][index[1][0]]
            y_best=found1[0][index[1][0]]
            matice_vstupni[y_best,x_best]=2
    if b==0:
        print("hledam nahradni reseni:")
        #x_best=found1[1][0]
       # y_best=found1[0][0]
        matice_vstupni=nahradni_reseni_kdyz_strom_nic(matice_vstupni,win_count)
    if b==2:
        print("jsem v bode b==2")
        x_best=x_best2
        y_best=y_best2
        matice_vstupni[y_best,x_best]=2
    if b==1:
        matice_vstupni[y_best,x_best]=2
    
    
   # print("xy best je:")    
   # print(x_best)
   # print(y_best)
    return matice_vstupni    

def nahradni_reseni_kdyz_strom_nic(matice_vstup,win_count):
   testovaci=matice_vstup.copy()
   found3=np.where(testovaci == 0)
   y_best3=0
   x_best3=0
   pom=0
   pom2=0
   for i in range(len(found3[0])):
        pomocna=testovaci.copy()
        x=found3[1][i]
        y=found3[0][i]
        pomocna[y,x]=2
        found_iter=np.where(pomocna == 0)
        for k in range(len(found3[0])-1):
            pomocna1=pomocna.copy()
            x1=found_iter[1][k]
            y1=found_iter[0][k]
            pomocna1[y1,x1]=2
            found_iter2=np.where(pomocna == 0)
            for k in range(len(found3[0])-2):
                 pomocna2=pomocna1.copy()
                 x1=found_iter2[1][k]
                 y1=found_iter2[0][k]
                 pomocna2[y1,x1]=2
                 if win_count==3: 
                     a1=win_rows_count(pomocna2,2,win_count)
                     b1=win_collumns_count(pomocna2,2,win_count)
                     c1=win_diagonal_count(pomocna2,2,win_count)
                     pom2= pom2+a1+b1+c1
        if pom2>pom:
            y_best3=y
            x_best3=x
            pom=pom2
            
            print("pom je:")
            print(pom)
            print(pomocna2)
        pom2=0       
   if win_count != 3:     
       x_best3=found3[1][1]
       y_best3=found3[0][1]
       
   print("nahradni reseni je")   
   matice_vstup[y_best3,x_best3]=2  
   print(matice_vstup)
   return matice_vstup

screen = pygame.display.set_mode([field_size*min_pixels, field_size*min_pixels])    


pygame.init()
pygame.display.set_caption('Piskworky 1.0')
screen.fill((255, 255, 255))
running = True
no_winner=True
grid_count_draw(field_size,min_pixels)
pygame.display.flip()
transparent = (0, 0, 0, 0)
tnk_rect = tnk.get_rect()
while running:
        
    for event in pygame.event.get(): #
        if event.type == pygame.QUIT:# musi byt kvuli ukonceni programu
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if no_winner:
                print(pygame.mouse.get_pos())
                a=pygame.mouse.get_pos() # vraci to tuple x pozice, y pozice
                matice=take_clicked_field_to_array(a,min_pixels,matice)
                draw_array(matice,min_pixels)
                pygame.display.flip()
                ifwin(matice.copy(),win_count)
                #matice=tahy_2_dopredu(matice.copy(),win_count)
                if  ifwin(matice.copy(),win_count):
                    break
                screen.blit(tnk,(100*field_size/2-150,100*field_size/2-100))
                pygame.display.flip()
                matice=tahy_3_dopredu(matice.copy(),win_count)
                
                screen.fill((255, 255, 255))
                running = True
                no_winner=True
                grid_count_draw(field_size,min_pixels)
                pygame.display.flip()
               # screen.blit(tnk, tnk_rect)
               # pygame.display.flip()
                draw_array(matice,min_pixels)
                pygame.display.flip()
                ifwin(matice.copy(),win_count)
                #if no_winner:
                    #matice=computer_move(matice.copy(),win_count)
                    #draw_array(matice,min_pixels)
                    #pygame.draw.circle(screen, (0, 0, 255), (a[0],a[1]), 25)
                   #pygame.display.flip()
                    #ifwin(matice.copy(),win_count) 
    
    
pygame.quit()