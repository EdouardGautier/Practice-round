import locale
import time as time

my_locale = locale.setlocale(locale.LC_ALL, "")

file_1 = "Haschcode 2021\\Practice round\\Input\\a_example"
file_2 = "Haschcode 2021\\Practice round\\Input\\b_little_bit_of_everything.in"
file_3 = "Haschcode 2021\\Practice round\\Input\\c_many_ingredients.in"
file_4 = "Haschcode 2021\\Practice round\\Input\\d_many_pizzas.in"
file_5 = "Haschcode 2021\\Practice round\\Input\\e_many_teams.in"

list_file = [file_1, file_2, file_3, file_4, file_5]


class Main():
    """Class allowing the reading of files"""

    def __init__(self, file: str) -> None:
        """
        Initialization of the class.

        Args:
            file (file text): Input file
        """
        self.file = file
        self.scrore = int()
        self.num_people = int()  # Total number of persons
        self.num_order = int()  # Number of teams delivered
        self.num_pizza_order = int()  # Number of pizzas delivered

        start = time.time()
        self.lecture()
        self.resolution()
        self.time = time.time() - start
        self.write_answer()
        self.write_detail()

        print(self)

    def lecture(self) -> None:
        """
        Reading the file.
        """
        k = int()
        self.list_teams = list()
        self.list_pizzas = list()

        f = open(self.file, encoding='ASCII')
        ligne = f.readline().strip().split()
        num_pizza = int(ligne[0])
        # Creation of teams
        for i in range(1, len(ligne)):
            for j in range(0, int(ligne[i])):
                self.list_teams.append(Team(k + j, i+1))
            k += i
        # Sorting according to the number of menbre
        self.list_teams.sort(key=lambda k: k.num_people, reverse=False)

        # Creation of pizzas
        for i in range(0, num_pizza):
            ligne = f.readline().strip().split()
            self.list_pizzas.append(Pizza(i, ligne[0], ligne))
        # Sorting according to the number of ingredients
        self.list_pizzas.sort(key=lambda k: k.num_ingredients, reverse=True)

        # Data for display
        self.num_pizza = len(self.list_pizzas)
        self.num_teams = len(self.list_teams)
        for team in self.list_teams:
            self.num_people += team.num_people

    def resolution(self) -> None:
        """
        Solving the problem.
        """
        self.team_order = list()
        max_ingredient = int(self.list_pizzas[0].num_ingredients)

        # First step
        # Max number of ingredients in common per pizza
        for min_score in range(0, max_ingredient):
            for pizza in self.list_pizzas:  # Pizza is looking for a team
                for team in self.list_teams:
                    # If there is room left in the team and
                    # if the number of ingredients
                    # in common is less than min_score
                    if len(team.list_order) < team.num_people and \
                            team.order(pizza) <= min_score:
                        team.confirm_order(pizza)
                        # It is withdrawn from the pizzas available
                        self.list_pizzas.remove(pizza)
                        break
                    # The team has no more room
                    elif len(team.list_order) == team.num_people:
                        # It is withdrawn from the teams available
                        self.list_teams.remove(team)
                        # It is added to the teams that have ordered
                        self.team_order.append(team)

        self.list_teams.sort(key=lambda k: k.score,
                             reverse=True)  # Sort by score

        # Second step
        # We add all the pizzas where there's room left over
        while len(self.list_pizzas) > 0:
            try:
                if self.list_teams[0].num_people == \
                        len(self.list_teams[0].list_order):
                    self.team_order.append(self.list_teams[0])
                    del self.list_teams[0]
                else:
                    self.list_teams[0].confirm_order(self.list_pizzas[0])
                    del self.list_pizzas[0]
            except IndexError:
                break

        # Third step
        # The teams with the lowest score give the teams with the highest score
        # to fill the remaining place
        for team in self.list_teams:
            for pizza in self.list_teams[-1].list_order:
                if len(team.list_order) == team.num_people:
                    self.team_order.append(team)
                    self.list_teams.remove(team)
                    break
                else:
                    self.list_teams[-1].list_order.remove(pizza)
                    team.confirm_order(pizza)
                    if len(self.list_teams[-1].list_order) == 0:
                        del self.list_teams[-1]

        # Data for display
        self.num_order = len(self.team_order)
        for team in self.team_order:
            self.num_pizza_order += len(team.list_order)

    def write_answer(self) -> None:
        """
        Writes the response file.
        """
        chaine = str()
        f = open("Haschcode 2021\\Practice round\\Output\\" +
                 self.file[36:] + ".txt", "w")
        f.write(str(len(self.team_order)) + "\n")
        for team in self.team_order:
            chaine += str(team.num_people) + " "
            for pizza in team.list_order:
                chaine += str(pizza.num_pizza) + " "
            f.write(chaine + "\n")
            chaine = str()
            self.scrore += len(team.list_ingredients)**2

    def write_detail(self) -> None:
        chaine = str()
        chaine += self.__str__()
        f = open("Haschcode 2021\\Practice round\\Output Details\\" +
                 self.file[36:] + ".txt", "w", encoding="UTF8")
        for team in self.team_order:
            chaine += str(team)
        f.write(chaine + "\n")

    def __str__(self) -> str:
        """
        Generates a character string with class information.

        Returns:
            str: Character string with class information
        """        
        chaine = 80 * "-"
        chaine += "\n" + self.file[36:] + "\n"
        chaine += "\nThere are {:n} teams with {:n} people.".format(
            self.num_teams, self.num_people)
        chaine += "\n{:n} teams were delivered with {:n} pizzas.".format(
            self.num_order, self.num_pizza_order)
        chaine += "\nThere are {:n} different ingredients.".format(
            self.scrore**(1/2))
        chaine += "\nExecution time: " + \
            time.strftime("%Hh %Mmin %Ss", time.gmtime(self.time))
        chaine += "\nScore: {:n}\n".format(self.scrore) + "\n"
        return chaine


class Team():
    """
    Team building class.
    """

    def __init__(self, num_team: int, num_people: int) -> None:
        """
        Initialization of the class.

        Args:
            num_team (int): team number
            num_people (int): number of people
        """
        self.num_team = int(num_team)
        self.num_people = int(num_people)
        self.list_order = list()  # List of pizzas ordered
        self.list_ingredients = list()  # List of ingredients
        self.score = int()

    def order(self, pizza) -> None:
        """
        We look at how many points the order earns.

        Args:
            pizza (Pizza): the pizza ordered 

        Returns:
            int: points reported by the order
        """
        score = int()
        for ingredient in pizza.ingredients:
            if ingredient in self.list_ingredients:
                score += 1
        return score

    def confirm_order(self, pizza) -> None:
        """
        We confirm that we take this pizza.

        Args:
            pizza (Pizza): the pizza ordered 
        """
        self.list_order.append(pizza)
        for ingredient in pizza.ingredients:  # New ingredients are registered
            if ingredient not in self.list_ingredients:
                self.list_ingredients.append(ingredient)
        self.score = len(self.list_ingredients)

    def __str__(self) -> str:
        """
        Generates a character string with class information.

        Returns:
            str: Character string with class information
        """  
        chaine = "Team n°{:n} with {:n} members, ordered {:n} pizzas:\n".format(
            self.num_team, self.num_people, len(self.list_order))
        for pizza in self.list_order:
            chaine += "\t" + str(pizza) + "\n"
        chaine += "There are {:n} different ingredients.\n\n".format(
            len(self.list_ingredients))
        return chaine


class Pizza():
    """
    Pizza creation class.
    """

    def __init__(self, num_pizza: int, num_ingredients: int,
                 ingredients: list) -> None:
        """
        Initialization of the class.

        Args:
            num_pizza (int): number of pizzas ordered
            num_ingredients (int): number of different ingredients
            ingredients (list): list of different ingredients
        """
        self.num_pizza = num_pizza
        self.num_ingredients = int(num_ingredients)
        del ingredients[0]  # The number of ingredients is removed
        self.ingredients = ingredients

    def __str__(self) -> str:
        """
        Generates a character string with class information.

        Returns:
            str: Character string with class information
        """  
        chaine = "Pizza n°{:n} with {:n} ingredients:\n\t\t".format(
            self.num_pizza, self.num_ingredients)
        for ingredient in self.ingredients:
            chaine += ingredient + ", "
        return chaine


if __name__ == "__main__":
    score = int()
    temps = int()
    print(80 * "#")
    for file in list_file:
        main = Main(file)
        score += main.scrore
        temps += main.time
    print("\nTotal score: {:n}".format(score), "\nTemps total: ",
          time.strftime("%Hh %Mmin %Ss", time.gmtime(temps)))
    print(80 * "#")
