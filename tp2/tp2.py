from queue import LifoQueue, Queue
import copy
import random
import time


class Solution:
    ARTICLES_WEIGHTS = []  # Store item weights
    ARTICLES_VALUES = []  # Store item values
    MAX_WEIGHT = 60  # Default max weight
    NUMBER_ITEMS = 5  # Default number of items

    @classmethod
    def set_number_items(cls, number_items: int):
        cls.NUMBER_ITEMS = number_items
        cls.ARTICLES_WEIGHTS = [0] * number_items
        cls.ARTICLES_VALUES = [0] * number_items

    @classmethod
    def set_articles_weights(cls, articles_weights: list):
        if len(articles_weights) != cls.NUMBER_ITEMS:
            raise ValueError("articles_weights must have length equal to NUMBER_ITEMS")
        cls.ARTICLES_WEIGHTS = articles_weights

    @classmethod
    def set_articles_values(cls, articles_values: list):
        if len(articles_values) != cls.NUMBER_ITEMS:
            raise ValueError("articles_values must have length equal to NUMBER_ITEMS")
        cls.ARTICLES_VALUES = articles_values

    @classmethod
    def set_max_weight(cls, max_weight: int):
        cls.MAX_WEIGHT = max_weight

    def __init__(self):
        self.solution = [-1] * self.NUMBER_ITEMS
        self.value = 0
        self.weight = 0
        self.valide = True
        self.full = False

    def addItem(self, item_id_list: list):
        for item_id in item_id_list:
            if 0 <= item_id < self.NUMBER_ITEMS and self.solution[item_id] != 1:
                self.solution[item_id] = 1
                self.weight += self.ARTICLES_WEIGHTS[item_id]
                self.value += self.ARTICLES_VALUES[item_id]
                if self.weight > self.MAX_WEIGHT:
                    self.valide = False
                if -1 not in self.solution:
                    self.full = True

    def removeItem(self, item_id_list: list):
        for item_id in item_id_list:
            if 0 <= item_id < self.NUMBER_ITEMS and self.solution[item_id] != 0:
                if self.solution[item_id] == 1:
                    self.weight -= self.ARTICLES_WEIGHTS[item_id]
                    self.value -= self.ARTICLES_VALUES[item_id]
                self.solution[item_id] = 0
                if self.weight <= self.MAX_WEIGHT:
                    self.valide = True
                if -1 not in self.solution:
                    self.full = True

    def get_validity(self):
        return self.valide

    def get_solution_is_full(self):
        return self.full

    def get_value(self):
        return self.value

    def get_solution(self):
        return self.solution

    def get_num_items(self):
        return len(self.solution)


class Optimizer:
    def __init__(self, algo: str = "DFS"):
        self.algo = algo
        if algo == "DFS":
            self.DFS()
        elif algo == "BFS":
            self.BFS()
        else:
            raise ValueError("algo parameter should be DFS or BFS")

    def BFS(self):
        open = Queue()
        closed = set()
        BestSol = []
        sol = Solution()
        BestSol.append(sol)
        open.put((sol, 0))

        while not open.empty():
            node, i = open.get()
            closed.add(tuple(node.get_solution()))

            if (
                node.get_solution_is_full()
                and node.get_validity()
                and node.get_value() >= BestSol[0].get_value()
            ):
                if node.get_value() > BestSol[0].get_value():
                    BestSol = [node]
                else:
                    BestSol.append(node)

            if i < node.get_num_items():
                new_node_add = copy.deepcopy(node)
                new_node_add.addItem([i])
                new_node_remove = copy.deepcopy(node)
                new_node_remove.removeItem([i])

                i += 1
                if tuple(new_node_add.get_solution()) not in closed:
                    open.put((new_node_add, i))
                if tuple(new_node_remove.get_solution()) not in closed:
                    open.put((new_node_remove, i))

        self.solutions = BestSol

    def DFS(self):
        open = LifoQueue()
        closed = set()
        BestSol = []
        sol = Solution()
        BestSol.append(sol)
        open.put((sol, 0))

        while not open.empty():
            node, i = open.get()
            closed.add(tuple(node.get_solution()))

            if (
                node.get_solution_is_full()
                and node.get_validity()
                and node.get_value() >= BestSol[0].get_value()
            ):
                if node.get_value() > BestSol[0].get_value():
                    BestSol = [node]
                else:
                    BestSol.append(node)

            if i < node.get_num_items():
                new_node_add = copy.deepcopy(node)
                new_node_add.addItem([i])
                new_node_remove = copy.deepcopy(node)
                new_node_remove.removeItem([i])

                i += 1
                if tuple(new_node_add.get_solution()) not in closed:
                    open.put((new_node_add, i))
                if tuple(new_node_remove.get_solution()) not in closed:
                    open.put((new_node_remove, i))

        self.solutions = BestSol

    def print_solutions(self):
        for solution in self.solutions:
            print("Best solutions using", self.algo, ":")
            print(solution.get_solution())
            print("Valid solution" if solution.get_validity() else "Invalid solution")
            print(f"Value: {solution.get_value()}  Weight: {solution.weight}")
            print("________________________________________________________")

    def get_solutions(self):
        return self.solutions


# MAIN -----------------------------------------------------------------------------------

for n in range(2, 20):  # Testing with 2 to 99 items
    weights = [random.randint(10, 50) for _ in range(n)]
    values = [random.randint(50, 200) for _ in range(n)]

    # Set problem parameters
    Solution.set_number_items(n)
    Solution.set_articles_weights(weights)
    Solution.set_articles_values(values)
    Solution.set_max_weight(10 * n)  # Adjust as needed

    # Print generated items
    print(f"\nTesting with {n} items")
    print(f"Weights: {weights}")
    print(f"Values: {values}")
    print(f"Limit Weight: {10*n}")
    print("Optimization __________________")

    # Measure DFS execution time
    start_time = time.time()
    optimizer = Optimizer(algo="DFS")
    optimizer.print_solutions()
    dfs_time = time.time() - start_time
    print(f"DFS Execution Time: {dfs_time:.4f} seconds")
    print("________________________")

    # Measure BFS execution time
    start_time = time.time()
    optimizer = Optimizer(algo="BFS")
    optimizer.print_solutions()
    bfs_time = time.time() - start_time
    print(f"BFS Execution Time: {bfs_time:.4f} seconds")
