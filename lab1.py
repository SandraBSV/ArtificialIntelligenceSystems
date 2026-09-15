import math
import time
import heapq
from collections import deque
import tkinter as tk
from tkinter import ttk

# ============================================================
# ГРАФ ТА КООРДИНАТИ ПРАЗЬКОГО МЕТРОПОЛІТЕНУ (Лінії A, B, C)
# ============================================================
subway_graph = {
    # Лінія A (Зелена)
    'Nemocnice Motol': [('Petřiny', 2)],
    'Petřiny': [('Nemocnice Motol', 2), ('Nádraží Veleslavín', 2)],
    'Nádraží Veleslavín': [('Petřiny', 2), ('Bořislavka', 2)],
    'Bořislavka': [('Nádraží Veleslavín', 2), ('Dejvická', 2)],
    'Dejvická': [('Bořislavka', 2), ('Hradčanská', 2)],
    'Hradčanská': [('Dejvická', 2), ('Malostranská', 2)],
    'Malostranská': [('Hradčanská', 2), ('Staroměstská', 2)],
    'Staroměstská': [('Malostranská', 2), ('Můstek', 2)],
    'Můstek': [('Staroměstská', 2), ('Muzeum', 2), ('Národní třída', 2), ('Náměstí Republiky', 2)],  # Пересадка
    'Muzeum': [('Můstek', 2), ('Náměstí Míru', 2), ('Hlavní nádraží', 2), ('I. P. Pavlova', 2)],  # Пересадка
    'Náměstí Míru': [('Muzeum', 2), ('Jiřího z Poděbrad', 2)],
    'Jiřího z Poděbrad': [('Náměstí Míru', 2), ('Flora', 2)],
    'Flora': [('Jiřího z Poděbrad', 2), ('Želivského', 2)],
    'Želivského': [('Flora', 2), ('Strašnická', 3)],
    'Strašnická': [('Želivského', 3), ('Skalka', 2)],
    'Skalka': [('Strašnická', 2), ('Depo Hostivař', 3)],
    'Depo Hostivař': [('Skalka', 3)],

    # Лінія B (Жовта)
    'Zličín': [('Stodůlky', 2)],
    'Stodůlky': [('Zličín', 2), ('Luka', 2)],
    'Luka': [('Stodůlky', 2), ('Lužiny', 2)],
    'Lužiny': [('Luka', 2), ('Hůrka', 2)],
    'Hůrka': [('Lužiny', 2), ('Nové Butovice', 2)],
    'Nové Butovice': [('Hůrka', 2), ('Radlická', 3)],
    'Radlická': [('Nové Butovice', 3), ('Jinonice', 2)],
    'Jinonice': [('Radlická', 2), ('Smíchovské nádraží', 3)],
    'Smíchovské nádraží': [('Jinonice', 3), ('Anděl', 2)],
    'Anděl': [('Smíchovské nádraží', 2), ('Karlovo náměstí', 2)],
    'Karlovo náměstí': [('Anděl', 2), ('Národní třída', 2)],
    'Národní třída': [('Karlovo náměstí', 2), ('Můstek', 2)],
    'Náměstí Republiky': [('Můstek', 2), ('Florenc', 2)],
    'Florenc': [('Náměstí Republiky', 2), ('Křižíkova', 2), ('Vltavská', 2), ('Hlavní nádraží', 2)],  # Пересадка
    'Křižíkova': [('Florenc', 2), ('Invalidovna', 2)],
    'Invalidovna': [('Křižíkova', 2), ('Palmovka', 2)],
    'Palmovka': [('Invalidovna', 2), ('Českomoravská', 3)],
    'Českomoravská': [('Palmovka', 3), ('Vysočanská', 2)],
    'Vysočanská': [('Českomoravská', 2), ('Kolbenova', 2)],
    'Kolbenova': [('Vysočanská', 2), ('Hloubětín', 2)],
    'Hloubětín': [('Kolbenova', 2), ('Rajská zahrada', 3)],
    'Rajská zahrada': [('Hloubětín', 3), ('Černý Most', 2)],
    'Černý Most': [('Rajská zahrada', 2)],

    # Лінія C (Червона)
    'Letňany': [('Prosek', 2)],
    'Prosek': [('Letňany', 2), ('Střížkov', 2)],
    'Střížkov': [('Prosek', 2), ('Ládví', 2)],
    'Ládví': [('Střížkov', 2), ('Kobylisy', 3)],
    'Kobylisy': [('Ládví', 3), ('Nádraží Holešovice', 3)],
    'Nádraží Holešovice': [('Kobylisy', 3), ('Vltavská', 2)],
    'Vltavská': [('Nádraží Holešovice', 2), ('Florenc', 2)],
    'Hlavní nádraží': [('Florenc', 2), ('Muzeum', 2)],
    'I. P. Pavlova': [('Muzeum', 2), ('Vyšehrad', 2)],
    'Vyšehrad': [('I. P. Pavlova', 2), ('Pražského povstání', 2)],
    'Pražského povstání': [('Vyšehrad', 2), ('Pankrác', 2)],
    'Pankrác': [('Pražského povstání', 2), ('Budějovická', 2)],
    'Budějovická': [('Pankrác', 2), ('Kačerov', 2)],
    'Kačerov': [('Budějovická', 2), ('Roztyly', 3)],
    'Roztyly': [('Kačerov', 3), ('Chodov', 2)],
    'Chodov': [('Roztyly', 2), ('Opatov', 2)],
    'Opatov': [('Chodov', 2), ('Háje', 3)],
    'Háje': [('Opatov', 3)]
}

coordinates = {
    # Лінія A
    'Nemocnice Motol': (2, 14), 'Petřiny': (4, 14), 'Nádraží Veleslavín': (6, 14),
    'Bořislavka': (8, 14), 'Dejvická': (10, 14), 'Hradčanská': (12, 13),
    'Malostranská': (13, 11), 'Staroměstská': (14, 9), 'Můstek': (15, 8),
    'Muzeum': (16, 7), 'Náměstí Míru': (18, 6), 'Jiřího z Poděbrad': (20, 6),
    'Flora': (22, 6), 'Želivského': (24, 6), 'Strašnická': (26, 5),
    'Skalka': (28, 4), 'Depo Hostivař': (30, 4),

    # Лінія B
    'Zličín': (1, 3), 'Stodůlky': (3, 4), 'Luka': (5, 4), 'Lužiny': (7, 4),
    'Hůrka': (9, 4), 'Nové Butovice': (11, 4), 'Radlická': (11, 6),
    'Jinonice': (11, 8), 'Smíchovské nádraží': (12, 9), 'Anděl': (13, 9),
    'Karlovo náměstí': (14, 8), 'Národní třída': (14, 9), 'Náměstí Republiky': (17, 9),
    'Florenc': (18, 10), 'Křižíkova': (20, 11), 'Invalidovna': (22, 11),
    'Palmovka': (24, 12), 'Českomoravská': (26, 13), 'Vysočanská': (27, 14),
    'Kolbenova': (29, 15), 'Hloubětín': (31, 15), 'Rajská zahrada': (33, 15),
    'Černý Most': (35, 15),

    # Лінія C
    'Letňany': (27, 18), 'Prosek': (26, 17), 'Střížkov': (25, 16),
    'Ládví': (24, 16), 'Kobylisy': (22, 16), 'Nádraží Holešovice': (20, 15),
    'Vltavská': (19, 13), 'Hlavní nádraží': (17, 8), 'I. P. Pavlova': (16, 5),
    'Vyšehrad': (16, 3), 'Pražského povstání': (16, 1), 'Pankrác': (16, -1),
    'Budějovická': (16, -3), 'Kačerov': (16, -5), 'Roztyly': (18, -6),
    'Chodov': (20, -7), 'Opatov': (22, -8), 'Háje': (24, -9)
}


def get_neighbors(station):
    return subway_graph.get(station, [])


def calculate_heuristic(current_station, goal_station):
    if current_station not in coordinates or goal_station not in coordinates:
        return 0.0
    x1, y1 = coordinates[current_station]
    x2, y2 = coordinates[goal_station]
    return (abs(x1 - x2) + abs(y1 - y2)) / 1.8


# ============================================================
# АЛГОРИТМИ ПОШУКУ
# ============================================================
def calculate_route_cost(path):
    if not path or len(path) == 1:
        return 0
    total_cost = 0
    for current, nxt in zip(path, path[1:]):
        for neighbor, minutes in get_neighbors(current):
            if neighbor == nxt:
                total_cost += minutes
                break
    return total_cost


def make_search_result(path, cost, expanded, generated, max_frontier, start_time):
    elapsed_ms = (time.perf_counter() - start_time) * 1000
    return {
        "found": path is not None,
        "path": path,
        "path_length": len(path) - 1 if path else None,
        "cost": cost,
        "expanded": expanded,
        "generated": generated,
        "max_frontier": max_frontier,
        "time_ms": elapsed_ms
    }


def bfs_search(start, goal):
    start_time = time.perf_counter()
    queue = deque([(start, [start])])
    visited = {start}
    expanded, generated, max_frontier = 0, 1, 1
    while queue:
        current, path = queue.popleft()
        expanded += 1
        if current == goal:
            return make_search_result(path, calculate_route_cost(path), expanded, generated, max_frontier, start_time)
        for neighbor, _ in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
                generated += 1
        max_frontier = max(max_frontier, len(queue))
    return make_search_result(None, None, expanded, generated, max_frontier, start_time)


def dfs_search(start, goal, max_depth=40):
    start_time = time.perf_counter()
    stack = [(start, [start], 0)]
    expanded, generated, max_frontier = 0, 1, 1
    while stack:
        current, path, depth = stack.pop()
        expanded += 1
        if current == goal:
            return make_search_result(path, calculate_route_cost(path), expanded, generated, max_frontier, start_time)
        if depth >= max_depth:
            continue
        for neighbor, _ in reversed(get_neighbors(current)):
            if neighbor not in path:
                stack.append((neighbor, path + [neighbor], depth + 1))
                generated += 1
        max_frontier = max(max_frontier, len(stack))
    return make_search_result(None, None, expanded, generated, max_frontier, start_time)


def ucs_search(start, goal):
    start_time = time.perf_counter()
    priority_queue = [(0, start, [start])]
    best_cost = {start: 0}
    expanded, generated, max_frontier = 0, 1, 1
    while priority_queue:
        current_cost, current, path = heapq.heappop(priority_queue)
        if current_cost > best_cost.get(current, float("inf")):
            continue
        expanded += 1
        if current == goal:
            return make_search_result(path, current_cost, expanded, generated, max_frontier, start_time)
        for neighbor, minutes in get_neighbors(current):
            new_cost = current_cost + minutes
            if new_cost < best_cost.get(neighbor, float("inf")):
                best_cost[neighbor] = new_cost
                heapq.heappush(priority_queue, (new_cost, neighbor, path + [neighbor]))
                generated += 1
        max_frontier = max(max_frontier, len(priority_queue))
    return make_search_result(None, None, expanded, generated, max_frontier, start_time)


def greedy_search(start, goal):
    start_time = time.perf_counter()
    priority_queue = [(calculate_heuristic(start, goal), start, [start])]
    visited = {start}
    expanded, generated, max_frontier = 0, 1, 1
    while priority_queue:
        _, current, path = heapq.heappop(priority_queue)
        expanded += 1
        if current == goal:
            return make_search_result(path, calculate_route_cost(path), expanded, generated, max_frontier, start_time)
        for neighbor, _ in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                h = calculate_heuristic(neighbor, goal)
                heapq.heappush(priority_queue, (h, neighbor, path + [neighbor]))
                generated += 1
        max_frontier = max(max_frontier, len(priority_queue))
    return make_search_result(None, None, expanded, generated, max_frontier, start_time)


def a_star_search(start, goal):
    start_time = time.perf_counter()
    priority_queue = [(calculate_heuristic(start, goal), 0, start, [start])]
    best_cost = {start: 0}
    expanded, generated, max_frontier = 0, 1, 1
    while priority_queue:
        _, current_cost, current, path = heapq.heappop(priority_queue)
        if current_cost > best_cost.get(current, float("inf")):
            continue
        expanded += 1
        if current == goal:
            return make_search_result(path, current_cost, expanded, generated, max_frontier, start_time)
        for neighbor, minutes in get_neighbors(current):
            new_cost = current_cost + minutes
            if new_cost < best_cost.get(neighbor, float("inf")):
                best_cost[neighbor] = new_cost
                new_f = new_cost + calculate_heuristic(neighbor, goal)
                heapq.heappush(priority_queue, (new_f, new_cost, neighbor, path + [neighbor]))
                generated += 1
        max_frontier = max(max_frontier, len(priority_queue))
    return make_search_result(None, None, expanded, generated, max_frontier, start_time)


# ============================================================
# ГРАФІЧНИЙ ІНТЕРФЕЙС
# ============================================================
class PragueSubwayApp:
    BG = "#1A1D24"
    PANEL = "#222631"
    CARD = "#2B303F"
    BORDER = "#3E455A"
    TEXT = "#FFFFFF"
    MUTED = "#A0AABF"
    ACCENT = "#00FFCC"
    ROUTE_COLOR = "#00E5FF"

    LINE_A = "#2E7D32"
    LINE_B = "#FBC02D"
    LINE_C = "#D32F2F"

    def __init__(self, root):
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.collections import LineCollection

        self.LineCollection = LineCollection
        self.root = root
        self.root.title("Metro v Praze • Схема & Навігація")
        self.root.geometry("1440x850")
        self.root.configure(bg=self.BG)

        self.stations = sorted(coordinates.keys())

        main_layout = tk.Frame(self.root, bg=self.BG)
        main_layout.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Ліва частина (Граф карти)
        self.left_frame = tk.Frame(main_layout, bg=self.PANEL, bd=1, relief=tk.SOLID)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Верхня панель
        self.top_control = tk.Frame(self.left_frame, bg=self.PANEL, pady=10, padx=10)
        self.top_control.pack(fill=tk.X)

        tk.Label(self.top_control, text="Звідки:", bg=self.PANEL, fg=self.TEXT, font=("Arial", 10, "bold")).pack(
            side=tk.LEFT, padx=5)
        self.start_box = ttk.Combobox(self.top_control, values=self.stations, width=20, font=("Arial", 10))
        self.start_box.pack(side=tk.LEFT, padx=5)

        tk.Label(self.top_control, text="Куди:", bg=self.PANEL, fg=self.TEXT, font=("Arial", 10, "bold")).pack(
            side=tk.LEFT, padx=5)
        self.goal_box = ttk.Combobox(self.top_control, values=self.stations, width=20, font=("Arial", 10))
        self.goal_box.pack(side=tk.LEFT, padx=5)

        tk.Label(self.top_control, text="Алгоритм:", bg=self.PANEL, fg=self.TEXT, font=("Arial", 10, "bold")).pack(
            side=tk.LEFT, padx=5)
        self.algo_box = ttk.Combobox(self.top_control, values=["BFS", "DFS", "UCS", "Greedy", "A*"], width=10,
                                     state="readonly", font=("Arial", 10))
        self.algo_box.set("A*")
        self.algo_box.pack(side=tk.LEFT, padx=5)

        self.btn_search = tk.Button(self.top_control, text="ПОШУК", bg=self.ACCENT, fg="#000000",
                                    font=("Arial", 10, "bold"), bd=0, padx=15, command=self.find_route)
        self.btn_search.pack(side=tk.LEFT, padx=10)

        # Права частина (Панель управління та логів)
        self.right_frame = tk.Frame(main_layout, bg=self.PANEL, width=350, bd=1, relief=tk.SOLID)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.right_frame.pack_propagate(False)

        header_card = tk.Frame(self.right_frame, bg=self.CARD, height=80)
        header_card.pack(fill=tk.X, padx=15, pady=15)
        header_card.pack_propagate(False)

        self.route_title = tk.Label(header_card, text="Оберіть маршрут", bg=self.CARD, fg=self.TEXT,
                                    font=("Arial", 12, "bold"))
        self.route_title.pack(anchor="w", padx=10, pady=(10, 2))
        self.route_info = tk.Label(header_card, text="Празький метрополітен", bg=self.CARD, fg=self.MUTED,
                                   font=("Arial", 9))
        self.route_info.pack(anchor="w", padx=10)

        self.txt_log = tk.Text(self.right_frame, bg=self.BG, fg=self.TEXT, insertbackground=self.TEXT,
                               font=("Courier New", 10), bd=0, padx=10, pady=10)
        self.txt_log.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        # Графік Matplotlib
        self.fig = Figure(figsize=(8, 6), facecolor=self.PANEL)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor(self.BG)

        self.draw_subway_edges()

        self.route_plot, = self.ax.plot([], [], color=self.ROUTE_COLOR, linewidth=4.5, zorder=5)
        self.special_points = self.ax.scatter([], [], s=180, c=self.ACCENT, edgecolors=self.TEXT, zorder=6)

        xs = [coordinates[s][0] for s in self.stations]
        ys = [coordinates[s][1] for s in self.stations]
        self.ax.scatter(xs, ys, s=50, c=self.MUTED, edgecolors=self.BORDER, zorder=3)

        for station, (x, y) in coordinates.items():
            self.ax.text(x + 0.3, y + 0.3, station, fontsize=7, color=self.MUTED, alpha=0.85, zorder=4)

        self.ax.set_axis_off()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.left_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def draw_subway_edges(self):
        for line_color, stations_list in [
            (self.LINE_A, ['Nemocnice Motol', 'Petřiny', 'Nádraží Veleslavín', 'Bořislavka', 'Dejvická', 'Hradčanská',
                           'Malostranská', 'Staroměstská', 'Můstek', 'Muzeum', 'Náměstí Míru', 'Jiřího z Poděbrad',
                           'Flora', 'Želivského', 'Strašnická', 'Skalka', 'Depo Hostivař']),
            (self.LINE_B, ['Zličín', 'Stodůlky', 'Luka', 'Lužiny', 'Hůrka', 'Nové Butovice', 'Radlická', 'Jinonice',
                           'Smíchovské nádraží', 'Anděl', 'Karlovo náměstí', 'Národní třída', 'Můstek',
                           'Náměstí Republiky', 'Florenc', 'Křižíkova', 'Invalidovna', 'Palmovka', 'Českomoravská',
                           'Vysočanská', 'Kolbenova', 'Hloubětín', 'Rajská zahrada', 'Černý Most']),
            (self.LINE_C,
             ['Letňany', 'Prosek', 'Střížkov', 'Ládví', 'Kobylisy', 'Nádraží Holešovice', 'Vltavská', 'Florenc',
              'Hlavní nádraží', 'Muzeum', 'I. P. Pavlova', 'Vyšehrad', 'Pražského povstání', 'Pankrác', 'Budějovická',
              'Kačerov', 'Roztyly', 'Chodov', 'Opatov', 'Háje'])
        ]:
            segs = []
            for i in range(len(stations_list) - 1):
                s1, s2 = stations_list[i], stations_list[i + 1]
                if s1 in coordinates and s2 in coordinates:
                    segs.append([coordinates[s1], coordinates[s2]])
            lc = self.LineCollection(segs, colors=line_color, linewidths=2.5, alpha=0.75, zorder=2)
            self.ax.add_collection(lc)

    def find_route(self):
        start = self.start_box.get().strip()
        goal = self.goal_box.get().strip()
        algo = self.algo_box.get()

        if start not in coordinates or goal not in coordinates:
            return

        if algo == "BFS":
            res = bfs_search(start, goal)
        elif algo == "DFS":
            res = dfs_search(start, goal, 40)
        elif algo == "UCS":
            res = ucs_search(start, goal)
        elif algo == "Greedy":
            res = greedy_search(start, goal)
        else:
            res = a_star_search(start, goal)

        if res["found"]:
            path = res["path"]
            rx = [coordinates[s][0] for s in path]
            ry = [coordinates[s][1] for s in path]
            self.route_plot.set_data(rx, ry)
            self.special_points.set_offsets([coordinates[start], coordinates[goal]])

            self.ax.set_xlim(min(rx) - 3, max(rx) + 3)
            self.ax.set_ylim(min(ry) - 3, max(ry) + 3)
            self.canvas.draw_idle()

            self.route_title.config(text=f"{start} → {goal}")
            self.route_info.config(text=f"Час: {res['cost']} хв | Пересадок: {res['path_length']}")

            log_output = (
                    f"[МАРШРУТ ЗНАЙДЕНО]\n"
                    f"Алгоритм: {algo}\n"
                    f"Загальний час: {res['cost']} хв.\n"
                    f"К-сть станцій: {len(path)}\n"
                    f"Розрахунок за: {res['time_ms']:.4f} ms\n\n"
                    f"Досліджено вузлів (Expanded): {res['expanded']}\n"
                    f"Згенеровано вузлів (Generated): {res['generated']}\n"
                    f"Макс. фронтир: {res['max_frontier']}\n\n"
                    f"Порядок прямування:\n" +
                    "\n".join([f"  {i + 1}. {st}" for i, st in enumerate(path)])
            )
            self.txt_log.delete("1.0", tk.END)
            self.txt_log.insert(tk.END, log_output)


if __name__ == "__main__":
    app_root = tk.Tk()
    PragueSubwayApp(app_root)
    app_root.mainloop()