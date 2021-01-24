import locale
import time as time

ma_locale = locale.setlocale(locale.LC_ALL, "")

fichier_1 = "Haschcode 2021\\Practice round\\Input\\a_example"
fichier_2 = "Haschcode 2021\\Practice round\\Input\\b_little_bit_of_everything.in"
fichier_3 = "Haschcode 2021\\Practice round\\Input\\c_many_ingredients.in"
fichier_4 = "Haschcode 2021\\Practice round\\Input\\d_many_pizzas.in"
fichier_5 = "Haschcode 2021\\Practice round\\Input\\e_many_teams.in"

liste_fichier = [fichier_1, fichier_2, fichier_3, fichier_4, fichier_5]

class Main():
    """
    Class permettant la lecture des fichiers
    """    
    def __init__(self, fichier):
        """
        Initialisation de la classe

        Args:
            fichier (ficheir texte): fichier en entré
        """        
        self.fichier = fichier
        self.scrore = int()
        debut = time.time()
        self.lecture()
        self.resolution()
        self.write()
        self.temps = time.time() - debut

        print("Score: {:n}".format(self.scrore))
        print("Temps:", time.strftime("%Hh %Mmin %Ss", time.gmtime(self.temps)))
        print()

    def lecture(self):
        """
        Lecture du fichier
        """        
        k = int()
        self.list_teams = list()
        self.list_pizzas = list()
        f = open(self.fichier, encoding='ASCII')
        ligne = f.readline().strip().split()
        num_pizza = int(ligne[0])
        for i in range(1, len(ligne)):
            for j in range(0, int(ligne[i])):
                self.list_teams.append(Team(k + j, i+1))
            k += i

        self.list_teams.sort(key=lambda k: k.num_person, reverse=False)
        for i in range(0, num_pizza):
            ligne = f.readline().strip().split()
            self.list_pizzas.append(Pizza(i, ligne[0], ligne))
        self.list_pizzas.sort(key=lambda k: k.num_ingredients, reverse=True)

    def resolution(self):
        self.team_order = list()
        max_ingredient = int(self.list_pizzas[0].num_ingredients)
        for min_score in range(0, max_ingredient):
            for pizza in self.list_pizzas:
                for team in self.list_teams:
                    if len(team.list_order) < team.num_person and team.order(pizza) <= min_score:
                        team.confirm_order(pizza)
                        self.list_pizzas.remove(pizza)
                        break
                    elif len(team.list_order) == team.num_person:
                        #print(team)
                        self.list_teams.remove(team)
                        self.team_order.append(team)
        self.list_teams.sort(key=lambda k: k.score, reverse=True)
        while len(self.list_pizzas) > 0:
            try:
                if self.list_teams[0].num_person == len(self.list_teams[0].list_order):
                    self.team_order.append(self.list_teams[0])
                    del self.list_teams[0]
                else:
                    self.list_teams[0].confirm_order(self.list_pizzas[0])
                    del self.list_pizzas[0]
            except IndexError:
                break

        for team in self.list_teams:
            for pizza in self.list_teams[-1].list_order:
                if len(team.list_order) == team.num_person:
                    self.team_order.append(team)
                    self.list_teams.remove(team)
                    break
                else:
                    self.list_teams[-1].list_order.remove(pizza)
                    team.confirm_order(pizza)
                    if len(self.list_teams[-1].list_order) == 0:
                        del self.list_teams[-1]

    def write(self):
        chaine = str()
        f = open("Haschcode 2021\\Practice round\\Output\\" + self.fichier[36:] + ".txt", "w")
        f.write(str(len(self.team_order)) + "\n")
        for team in self.team_order:
            #print(team)
            chaine += str(team.num_person) + " "
            for pizza in team.list_order:
                chaine += str(pizza.num_pizza) + " "
            f.write(chaine + "\n")
            chaine = str()
            self.scrore += len(team.list_ingredients)**2


class Team():

    def __init__(self, num_team, num_person):
        self.num_team = int(num_team)
        self.num_person = int(num_person)
        self.list_order = list()
        self.list_ingredients = list()
        self.score = int()

    def order(self, pizza):
        score = int()
        for ingredient in pizza.ingredients:
            if ingredient in self.list_ingredients:
                score +=1
        return score

    def confirm_order(self, pizza):
        self.list_order.append(pizza)
        for ingredient in pizza.ingredients:
            if ingredient not in self.list_ingredients:
                self.list_ingredients.append(ingredient)
        self.score = len(self.list_ingredients)

    def __str__(self):
        chaine = "Equipe n°" + str(self.num_team) + " avec " + str(self.num_person) + " de membres, a commandé " + str(len(self.list_order)) + " pizzas:\n"
        for pizza in self.list_order:
            chaine += str(pizza) + "\n"
        chaine += "Il y a " + str(len(self.list_ingredients)) + " ingrédients différents.\n"
        return chaine

class Pizza():

    def __init__(self, num_pizza, num_ingredients, ingredients) -> None:
        self.num_pizza = num_pizza
        self.num_ingredients = num_ingredients
        del ingredients[0]
        self.ingredients = ingredients

    def __str__(self):
        chaine = "Pizza n°" + str(self.num_pizza) + " avec " + str(self.num_ingredients) + " ingrédients:\n\t"
        for ingredient in self.ingredients:
            chaine += ingredient + ", "
        return chaine


if __name__ == "__main__":
    score = int()
    temps = int()
    for fichier in liste_fichier: 
        print(fichier[36:])
        main = Main(fichier)
        score += main.scrore
        temps += main.temps
    #Main(fichier_1)
    print("\nScore total: {:n}".format(score), "\nTemps total: ",
          time.strftime("%Hh %Mmin %Ss", time.gmtime(temps)))