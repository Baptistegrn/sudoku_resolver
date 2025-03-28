import pyxel
import time

import webbrowser
class ResolutionSudoku:
    def __init__(self,s):
        self.sudoku = s
        self.sudoku_backtracking = [ligne[:] for ligne in self.sudoku]
        self.sudoku_naif = [ligne[:] for ligne in self.sudoku]

    def ligne_complete(self, sudoku, y_ligne):
        liste = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for x in sudoku[y_ligne]:
            if x in liste:
                liste.remove(x)
            else:
                return False
        return True

    def colonne_complete(self, sudoku, x_colonne):
        liste = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for y in range(9):
            if sudoku[y][x_colonne] in liste:
                liste.remove(sudoku[y][x_colonne])
            else:
                return False
        return True

    def carre_complet(self, sudoku, x_carre, y_carre):
        liste = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        x_carre, y_carre = (x_carre // 3) * 3, (y_carre // 3) * 3
        for y in range(3):
            for x in range(3):
                if sudoku[y + y_carre][x + x_carre] in liste:
                    liste.remove(sudoku[y + y_carre][x + x_carre])
                else:
                    return False
        return True

    def sudoku_resolu(self, sudoku):
        for i in range(9):
            if not self.ligne_complete(sudoku, i) or not self.colonne_complete(sudoku, i):
                return False
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                if not self.carre_complet(sudoku, i, j):
                    return False
        return True

    def ligne(self, sudoku, y_ligne):
        return [sudoku[y_ligne][x] for x in range(9) if sudoku[y_ligne][x] != 0]

    def colonne(self, sudoku, x_colonne):
        return [sudoku[y][x_colonne] for y in range(9) if sudoku[y][x_colonne] != 0]

    def carre(self, sudoku, x_carre, y_carre):
        x_carre, y_carre = (x_carre // 3) * 3, (y_carre // 3) * 3
        return [sudoku[y + y_carre][x + x_carre] for y in range(3) for x in range(3) if sudoku[y + y_carre][x + x_carre] != 0]

    def conflit(self, sudoku, x, y):
        return list(set(self.ligne(sudoku, y) + self.colonne(sudoku, x) + self.carre(sudoku, x, y)))

    def possibilite_case(self, sudoku, x, y):
        return list(set(range(1, 10)) - set(self.conflit(sudoku, x, y)))

    def algorithme_naif(self):
        debut = time.time()
        modifie = True  

        while not self.sudoku_resolu(self.sudoku_naif):  
            modifie = False  

            for y in range(9):  
                for x in range(9): 
                    if self.sudoku_naif[y][x] == 0:  
                        possibilites = self.possibilite_case(self.sudoku_naif, x, y)

                        if len(possibilites) == 1:  
                            self.sudoku_naif[y][x] = float(possibilites[0])
                            modifie = True
            

            if not modifie:
                break


        fin = time.time()
        if self.sudoku_resolu(self.sudoku_naif):
            return self.sudoku_naif, (fin - debut) * 1000  
        else:

            return None, (fin - debut) * 1000  




    def backtracking(self, x=0, y=0):
        debut = time.time()  

        if x == 9 and y != 8:
            y += 1
            x = 0
        if y == 8 and x == 9: 
            fin = time.time()  
            return self.sudoku_backtracking, (fin - debut) * 1000  

        elif self.sudoku_backtracking[y][x] != 0:
            return self.backtracking(x + 1, y)  
        else:
            possibilites = self.possibilite_case(self.sudoku_backtracking, x, y)
            for chiffre in possibilites:
                self.sudoku_backtracking[y][x] = float(chiffre)
                resultat, temp = self.backtracking(x + 1, y)
                if resultat is not None:
                    fin = time.time()  
                    return resultat, (fin - debut) * 1000  

            self.sudoku_backtracking[y][x] = 0.0

        fin = time.time()  
        return None, (fin - debut) * 1000  
    
    
    
    
    
    
PAL = PAL = [
    0x2B1B0F, 0x3E2615, 0x53301A, 0x6A3C21,  
    0x814828, 0x9A5630, 0xB36539, 0xCD7543,  
    0xE78650, 0xFFA45E, 0xFFB770, 0xFFC985,  
    0xFFD99A, 0xFFE6B0, 0xFFF2C6, 0xFFFFFF  
]


class JeuSudoku:
    def __init__(self):
        
        self.page = 0
        pyxel.init(260, 120, fps=200)
        pyxel.load("sudoku.pyxres")
        pyxel.colors.from_list(PAL)
        self.resolu = False
        self.posx = 0
        self.posy = 0
        self.indicex =0
        self.indicey= 0
        self.tableau_sudoku = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]
        pyxel.run(self.update,self.draw)

    def update(self):
        pyxel.mouse(True)
        if self.page ==2:
            if pyxel.btnp(pyxel.KEY_Z) and self.indicey>0:
                self.indicey-=1
                self.posy-=8
            if pyxel.btnp(pyxel.KEY_S) and self.indicey<8:
                self.indicey+=1
                self.posy+=8
            if pyxel.btnp(pyxel.KEY_D) and self.indicex<8:
                self.indicex+=1
                self.posx+=8
            if pyxel.btnp(pyxel.KEY_Q)and self.indicex>0 :
                self.indicex-=1
                self.posx-=8


            if pyxel.btnp(pyxel.KEY_1):
                self.tableau_sudoku[self.indicey][self.indicex] = 1
            elif pyxel.btnp(pyxel.KEY_2):
                self.tableau_sudoku[self.indicey][self.indicex] = 2
            elif pyxel.btnp(pyxel.KEY_3):
                self.tableau_sudoku[self.indicey][self.indicex] = 3
            elif pyxel.btnp(pyxel.KEY_4):
                self.tableau_sudoku[self.indicey][self.indicex] = 4
            elif pyxel.btnp(pyxel.KEY_5):
                self.tableau_sudoku[self.indicey][self.indicex] = 5
            elif pyxel.btnp(pyxel.KEY_6):
                self.tableau_sudoku[self.indicey][self.indicex] = 6
            elif pyxel.btnp(pyxel.KEY_7):
                self.tableau_sudoku[self.indicey][self.indicex] = 7
            elif pyxel.btnp(pyxel.KEY_8):
                self.tableau_sudoku[self.indicey][self.indicex] = 8
            elif pyxel.btnp(pyxel.KEY_9):
                self.tableau_sudoku[self.indicey][self.indicex] = 9
            elif pyxel.btnp(pyxel.KEY_0):
                self.tableau_sudoku[self.indicey][self.indicex] = 0

            if 115 <= pyxel.mouse_x <= 155 and 100 <= pyxel.mouse_y <= 110:
                if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                    self.page = 1
                    
        if self.page == 1:
            if not(self.resolu) :
                self.sudoku = ResolutionSudoku(self.tableau_sudoku)
                self.sudokuoriginal = [ligne[:] for ligne in self.sudoku.sudoku]
                self.sudokunaif, self.tempnaif = self.sudoku.algorithme_naif()
                self.sudokuback,self.tempback= self.sudoku.backtracking()
                self.resolu = True
        
        if self.page == 0:
            if 110 <= pyxel.mouse_x <= 150 and 20 <= pyxel.mouse_y <= 30:
                if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                    self.page = 2
            if 110 <= pyxel.mouse_x <= 150 and 90 <= pyxel.mouse_y <= 100:
                if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                    pyxel.quit()
            
            if 110 <= pyxel.mouse_x <= 150 and 55 <= pyxel.mouse_y <= 65:
                if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                    webbrowser.open("https://gist.github.com/Baptistegrn") 

    def draw(self):
        if self.page == 0:
            pyxel.cls(0)
            pyxel.blt(110,20,2,0,0,40,10)
            pyxel.blt(110,55,2,0,0,40,10)
            pyxel.blt(110,90,2,0,0,40,10)
            
            pyxel.text(112,22,"Solve",10)
            pyxel.text(116,57,"Git",10)
            pyxel.text(114,92,"Quit",10)                   


        if self.page == 2 :

            pyxel.cls(0)           
            pyxel.blt(90, 20, 0, 0, 0, 72, 72)
            pyxel.blt(115,100,2,0,0,40,10)            
            pyxel.text(119,102,"Save",10)
            self.afficher_sudoku(self.tableau_sudoku, 90, 22)            
            pyxel.rect(self.posx+90,self.posy+20,8,8,9)
            
            
            
        if self.page == 1 : 
            pyxel.cls(0) 
            pyxel.blt(10, 20, 0, 0, 0, 72, 72)
            pyxel.text(10,10,"Sudoku a résoudre ! ",8) 
            pyxel.blt(90, 20, 0, 0, 0, 72, 72)
            pyxel.text(90,10,"Sudoku backtracking ",8)
            pyxel.text(170,10,"Sudoku algo naif",8) 
            self.afficher_sudoku(self.sudokuoriginal, 10, 22)
            
            if self.sudokuback is not None or self.sudoku.sudoku_resolu(self.sudokuback):
                self.afficher_sudoku(self.sudokuback, 90, 22)
            else:
                pyxel.blt(90+28, 57, 2, 0, 192, 16, 16)
                
            if self.sudokunaif is not None :
                self.afficher_sudoku(self.sudokunaif, 170, 22)
            else:
            
                pyxel.blt(170+28, 57, 2, 0, 192, 16, 16)            
                

    def afficher_sudoku(self, sudoku, x_offset, y_offset):
        y = -8
        for ligne in sudoku:
            x = 0
            y += 8
            for ele in ligne:
                if isinstance(ele, int):
                    pyxel.text(x + x_offset + 2, y + y, str(ele), 8)  
                elif isinstance(ele, float):  
                    pyxel.text(x + x_offset + 2, y + y, str(int(ele)), 10)  
                x += 8

JeuSudoku()
