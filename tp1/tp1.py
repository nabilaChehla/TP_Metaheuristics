import random


class Solution:
    ARTICLES_WEIGHTS = []  # Store item weights
    ARTICLES_VALUES = []  # Store item values
    MAX_WEIGHT = 60  # Default max weight
    NUMBER_ITEMS = 10  # Default number of items

    @classmethod
    def set_number_items(cls, number_items: int):
        """Set number of items (should be called once before creating instances)."""
        cls.NUMBER_ITEMS = number_items
        cls.ARTICLES_WEIGHTS = [0] * number_items  # Reset with default values
        cls.ARTICLES_VALUES = [0] * number_items  # Reset with default values

    @classmethod
    def set_articles_weights(cls, articles_weights: list):
        """Set articles' weights, ensuring length matches NUMBER_ITEMS."""
        if len(articles_weights) != cls.NUMBER_ITEMS:
            raise ValueError("articles_weights must have length equal to NUMBER_ITEMS")
        cls.ARTICLES_WEIGHTS = articles_weights

    @classmethod
    def set_articles_values(cls, articles_values: list):
        """Set articles' values, ensuring length matches NUMBER_ITEMS."""
        if len(articles_values) != cls.NUMBER_ITEMS:
            raise ValueError("articles_values must have length equal to NUMBER_ITEMS")
        cls.ARTICLES_VALUES = articles_values

    @classmethod
    def set_max_weight(cls, max_weight: int):
        """Set max weight constraint."""
        cls.MAX_WEIGHT = max_weight

    def __init__(self):
        """Initialize a solution with all items set to 0."""
        self.solution = [0] * self.NUMBER_ITEMS
        self.value = 0
        self.weight = 0
        self.valide = True

    def addItem(self, item_id_list: list):
        """Add items to the solution if within bounds and weight constraint."""
        for item_id in item_id_list:
            if 0 <= item_id < self.NUMBER_ITEMS:  # Ensure item_id is within bounds
                if self.solution[item_id] != 1:
                    self.solution[item_id] = 1
                    self.weight += self.ARTICLES_WEIGHTS[item_id]
                    self.value += self.ARTICLES_VALUES[item_id]
                    if self.weight > self.MAX_WEIGHT:
                        self.valide = False

    def removeItem(self, item_id_list: list):
        """Remove items from the solution."""
        for item_id in item_id_list:
            if 0 <= item_id < self.NUMBER_ITEMS:  # Ensure item_id is within bounds
                if self.solution[item_id] != 0:
                    self.solution[item_id] = 0
                    self.weight -= self.ARTICLES_WEIGHTS[item_id]
                    self.value -= self.ARTICLES_VALUES[item_id]
                    if self.weight <= self.MAX_WEIGHT:
                        self.valide = True

    def generate_random(self):
        """Generate a random solution"""
        steps = random.randint(0, 10)  # Choose number of steps (0 to 10)

        for _ in range(steps):
            action = random.randint(0, 1)  # 0 = add, 1 = remove
            item_id = random.randint(0, self.NUMBER_ITEMS - 1)

            if action == 0:
                self.addItem([item_id])
            else:
                self.removeItem([item_id])

    def validity(self):
        """Return whether the solution is valid"""
        return self.valide

    def value(self):
        """Return whether the solution is valid"""
        return self.value

    def solution_vector(self):
        """Return the solution vector"""
        return self.solution


class Solver:
    def __init__(self):
        # Step 1: Set global parameters
        self.solutions = []

    def solve(self, num_solutions):
        # Step 2: Create solutions instance
        for i in range(num_solutions):
            self.solutions.append(Solution())
        # Step 3: Generate random solutions
        for solution in self.solutions:
            solution.generate_random()

    def print_solutions(self):
        for solution in self.solutions:
            print("Generated solution : ")
            print(solution.solution_vector())
            if solution.valide:
                print("Valide solution")
            else:
                print("invalide solution")

            print("value :", solution.value, "  weight:", solution.weight)
            print("________________________________________________________")

    def get_solutions(self):
        return self.solutions


class Optimazer:
    def __init__(self, solutions: list[Solution]):
        self.solutions = solutions

    def best_solutions(self):
        """Return the solution(s) with the highest value."""
        if not self.solutions:
            return []

        # Find the maximum value among valid solutions
        max_value = max(sol.value for sol in self.solutions if sol.validity())

        # Return all solutions that have this max value and are valid
        return [
            sol for sol in self.solutions if sol.validity() and sol.value == max_value
        ]

    def print_best_solutions(self):
        """Print the best solutions"""
        print("Best Solutions : ")
        for sol in self.best_solutions():
            print(sol.solution_vector())
            print(
                "Validity :", sol.valide, " value :", sol.value, "  weight:", sol.weight
            )
            print("________________________________________________________")


# Simple test for Solution class

# Step 1: Set global parameters
Solution.set_number_items(3)
Solution.set_articles_weights([10, 20, 30])
Solution.set_articles_values([60, 100, 120])
Solution.set_max_weight(40)

solver = Solver()
solver.solve(10)
solver.print_solutions()


optimazer = Optimazer(solutions=solver.get_solutions())
optimazer.print_best_solutions()
