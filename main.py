# Файл:
import random
import tkinter as tk

CELL_SIZE = 20
WIDTH = 20
HEIGHT = 20

# === 1. Мир ===
class World:
    def __init__(self, canvas, info_text):
        self.width = WIDTH
        self.height = HEIGHT
        self.grid = [[Cell() for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.entities = []
        self.ticks = 0
        self.canvas = canvas
        self.info_text = info_text
        self.messages = []

    def tick(self):
        self.ticks += 1
        for row in self.grid:
            for cell in row:
                if isinstance(cell.terrain, Bush):
                    cell.terrain.tick()

        for entity in self.entities[:]:
            entity.act(self)

        self.handle_events()
        self.render()
        self.update_info()

    def render(self):
        self.canvas.delete("all")
        for x in range(self.width):
            for y in range(self.height):
                cell = self.grid[x][y]
                x1, y1 = x * CELL_SIZE, y * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                color = "white"
                if cell.entities:
                    color = "red"
                elif isinstance(cell.terrain, Grass):
                    color = "green"
                elif isinstance(cell.terrain, Bush):
                    color = "darkgreen"
                elif isinstance(cell.terrain, Tree):
                    color = "brown"
                elif isinstance(cell.terrain, Water):
                    color = "blue"
                elif isinstance(cell.terrain, Rock):
                    color = "gray"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

    def update_info(self):
        info_lines = [f"Tick: {self.ticks}\n"]
        for i, entity in enumerate(self.entities):
            info_lines.append(f"Существо {i+1}: HP={entity.hp}, Возраст={entity.age}, Голод={entity.hunger}, Жажда={entity.thirst}, Инвентарь={entity.inventory}\n")
        info_lines += self.messages[-5:]
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert(tk.END, "".join(info_lines))

    def handle_events(self):
        if random.random() < 0.01:
            x, y = random.randint(0, 19), random.randint(0, 19)
            self.messages.append(f"🔥 Пожар в клетке ({x},{y})\n")
        if random.random() < 0.05:
            self.messages.append("🌧 Идёт дождь\n")
            for _ in range(5):
                x, y = random.randint(0, 19), random.randint(0, 19)
                self.grid[y][x].terrain = random.choice([Grass(), Bush(), Water()])
        if random.random() < 0.05:
            x, y = random.randint(0, 19), random.randint(0, 19)
            self.grid[y][x].terrain = Rock()
            self.messages.append(f"☄️ Метеорит ударил в ({x},{y})\n")

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
            try:
                world.grid[self.x][self.y].entities.remove(self)
            except  ValueError:
                pass
            world.entities.remove(self)
            return

        if self.hunger > 70:
            if not self.eat():
                self.short_term_goals.append("найти еду")
        elif self.thirst > 80:
            self.short_term_goals.append("найти воду")
        else:
            self.reproduction_ready += 1

        dx, dy = random.choice([(0,1),(1,0),(-1,0),(0,-1)])
        self.move(dx, dy, world)

    def move(self, dx, dy, world):
        new_x = max(0, min(world.width - 1, self.x + dx))
        new_y = max(0, min(world.height - 1, self.y + dy))
        world.grid[self.x][self.y].entities.remove(self)
        self.x, self.y = new_x, new_y
        world.grid[self.x][self.y].entities.append(self)

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

# === 6. GUI и запуск ===
def main():
    root = tk.Tk()
    root.title("Life Simulator")

    canvas = tk.Canvas(root, width=WIDTH*CELL_SIZE, height=HEIGHT*CELL_SIZE)
    canvas.pack()

    info_text = tk.Text(root, height=10)
    info_text.pack()

    world = World(canvas, info_text)
    ent = Entity(10, 10)
    world.entities.append(ent)
    world.grid[10][10].entities.append(ent)

    def update():
        world.tick()
        root.after(1000, update)

    update()
    root.mainloop()

if __name__ == "__main__":
    main()
