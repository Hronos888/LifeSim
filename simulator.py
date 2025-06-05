# Файл:
import random
import time

# === 1. Мир ===
class World:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.grid = [[Cell() for _ in range(width)] for _ in range(height)]
        self.entities = []
        self.ticks = 0

    def tick(self):
        self.ticks += 1
        for entity in self.entities:
            entity.act(self)
        self.handle_events()

    def render(self):
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                if self.grid[y][x].entities:
                    row += "E"
                elif self.grid[y][x].terrain:
                    row += self.grid[y][x].terrain.symbol
                else:
                    row += "."
            print(row)
        print("\n")

    def handle_events(self):
        if random.random() < 0.01:
            x, y = random.randint(0, 19), random.randint(0, 19)
            print(f"\n🔥 Fire starts at ({x},{y})!")
        if random.random() < 0.05:
            print("\n🌧 Rain event")
            for _ in range(5):
                x, y = random.randint(0, 19), random.randint(0, 19)
                self.grid[y][x].terrain = random.choice([Grass(), Bush(), Water()])
        if random.random() < 0.05:
            x, y = random.randint(0, 19), random.randint(0, 19)
            print(f"\n☄️ Meteor hits ({x},{y})!")
            self.grid[y][x].terrain = Rock()

# === 2. Рецепты ===
class Recipes:
    ALL = {
        'жилище': {'бревно': 3, 'ветка': 2, 'трава': 5},
        'топор': {'ветка': 2, 'камень': 1, 'трава': 1},
        'нить': {'трава': 2},
        'лук': {'ветка': 1, 'нить': 1},
    }

# === 3. Клетка ===
class Cell:
    def __init__(self):
        self.terrain = random.choice([None, Grass(), Bush(), Tree(), Water(), Rock()])
        self.entities = []

# === 4. Существо ===
class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 100
        self.strength = 10
        self.meat = 3
        self.age = 0
        self.max_age = 150
        self.reproduction_ready = 0
        self.thirst = 0
        self.hunger = 0
        self.inventory = []
        self.known_recipes = ['жилище', 'топор']
        self.long_term_goals = ['размножиться', 'накопить 5 еды']
        self.short_term_goals = []

    def act(self, world):
        self.age += 1
        self.hunger += 6
        self.thirst += 3
        if self.hunger >= 100 or self.thirst >= 100 or self.age >= self.max_age:
            world.entities.remove(self)
            return

        if self.hunger > 70:
            if not self.eat():
                self.short_term_goals.append("найти еду")
        elif self.thirst > 80:
            self.short_term_goals.append("найти воду")
        else:
            self.reproduction_ready += 1

        # Для простоты: случайное перемещение
        dx, dy = random.choice([(0,1),(1,0),(-1,0),(0,-1)])
        self.move(dx, dy, world)

    def move(self, dx, dy, world):
        new_x = max(0, min(world.width - 1, self.x + dx))
        new_y = max(0, min(world.height - 1, self.y + dy))
        world.grid[self.y][self.x].entities.remove(self)
        self.x, self.y = new_x, new_y
        world.grid[self.y][self.x].entities.append(self)

    def eat(self):
        for i, item in enumerate(self.inventory):
            if item == 'ягоды':
                del self.inventory[i]
                self.hunger = max(0, self.hunger - 20)
                return True
        return False

    def reproduce(self):
        child = Entity(self.x, self.y)
        child.max_age = self.max_age + random.choice([-5, 0, 5]) if random.random() < 0.1 else self.max_age
        child.strength = self.strength + random.choice([-1, 0, 1]) if random.random() < 0.1 else self.strength
        return child

# === 5. Объекты ===
class Grass:
    name = "трава"
    symbol = "g"

class Bush:
    name = "куст"
    symbol = "b"
    def __init__(self):
        self.age = 0
        self.has_berries = False

    def tick(self):
        self.age += 1
        if self.age >= 3:
            self.has_berries = True

class Tree:
    name = "дерево"
    symbol = "t"

class Water:
    name = "вода"
    symbol = "w"
    def __init__(self):
        self.strength = 2

class Rock:
    name = "камень"
    symbol = "r"

# === 6. Тест симуляции ===
if __name__ == "__main__":
    world = World()
    ent = Entity(5, 5)
    world.entities.append(ent)
    world.grid[5][5].entities.append(ent)

    for _ in range(10):
        world.render()
        world.tick()
        time.sleep(2)