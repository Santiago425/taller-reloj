PI = 3.141592653589793
ESC = chr(27)
WIDTH = 76
LEFT_WIDTH = 45
RIGHT_WIDTH = 30


def sine(angle):
    while angle > PI:
        angle -= 2 * PI
    while angle < -PI:
        angle += 2 * PI
    result = 0
    term = angle
    n = 1
    while n < 20:
        result += term
        term = -term * angle * angle / ((n + 1) * (n + 2))
        n += 2
    return result


def cosine(angle):
    return sine(angle + PI / 2)


def fit(text, width):
    if len(text) > width:
        return text[:width]
    return text + " " * (width - len(text))


def center(text, width):
    if len(text) >= width:
        return text[:width]
    left = (width - len(text)) // 2
    return " " * left + text + " " * (width - len(text) - left)


def visible_length(text):
    length = 0
    index = 0
    while index < len(text):
        if text[index] == ESC:
            while index < len(text) and not text[index].isalpha():
                index += 1
            index += 1
            continue
        length += 1
        index += 1
    return length


def format_duration(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    rest = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{rest:02d}"


class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class CircularDoublyLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def is_empty(self):
        return self.head is None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            new_node.next = self.head
            new_node.prev = self.head
        else:
            last = self.head.prev
            new_node.next = self.head
            self.head.prev = new_node
            new_node.prev = last
            last.next = new_node
            self.head = new_node
        self.size += 1
        return new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            new_node.next = self.head
            new_node.prev = self.head
        else:
            last = self.head.prev
            last.next = new_node
            new_node.prev = last
            new_node.next = self.head
            self.head.prev = new_node
        self.size += 1
        return new_node

    def delete(self, data):
        node = self.find(data)
        if node is None:
            return False
        return self.delete_node(node)

    def delete_node(self, node):
        if self.head is None or node is None:
            return False
        if node.next == node:
            self.head = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
            if node == self.head:
                self.head = node.next
        node.next = None
        node.prev = None
        self.size -= 1
        return True

    def find(self, data):
        if self.head is None:
            return None
        current = self.head
        while True:
            if current.data == data:
                return current
            current = current.next
            if current == self.head:
                return None

    def clear(self):
        self.head = None
        self.size = 0

    def to_list(self):
        items = []
        current = self.head
        if current is not None:
            items.append(current.data)
            current = current.next
            while current != self.head:
                items.append(current.data)
                current = current.next
        return items

    def print_list(self):
        current = self.head
        if current is not None:
            print(current.data)
            current = current.next
            while current != self.head:
                print(current.data)
                current = current.next


class Clock:
    def __init__(self, hour, minute, second):
        self.hours = self.build_ring(24)
        self.minutes = self.build_ring(60)
        self.seconds = self.build_ring(60)
        self.formats = CircularDoublyLinkedList()
        self.formats.insert_at_end("12 horas")
        self.formats.insert_at_end("24 horas")
        self.current_format = self.formats.head
        self.last_steps = []
        self.set_time(hour, minute, second)

    def build_ring(self, amount):
        ring = CircularDoublyLinkedList()
        for value in range(amount):
            ring.insert_at_end(value)
        return ring

    def set_time(self, hour, minute, second):
        self.current_hour = self.hours.find(hour)
        self.current_minute = self.minutes.find(minute)
        self.current_second = self.seconds.find(second)

    def tick(self):
        steps = []
        old = self.current_second.data
        self.current_second = self.current_second.next
        steps.append(f"Segundos: {old:02d} --next--> {self.current_second.data:02d}")
        if self.current_second.data == 0:
            steps.append("  El segundo dio la vuelta, avanza el minuto")
            old = self.current_minute.data
            self.current_minute = self.current_minute.next
            steps.append(f"Minutos:  {old:02d} --next--> {self.current_minute.data:02d}")
            if self.current_minute.data == 0:
                steps.append("  El minuto dio la vuelta, avanza la hora")
                old = self.current_hour.data
                self.current_hour = self.current_hour.next
                steps.append(f"Horas:    {old:02d} --next--> {self.current_hour.data:02d}")
        self.last_steps = steps
        return steps

    def tick_back(self):
        steps = []
        if self.current_second.data == 0:
            steps.append("  El segundo esta en 00, retrocede el minuto")
            if self.current_minute.data == 0:
                steps.append("  El minuto esta en 00, retrocede la hora")
                old = self.current_hour.data
                self.current_hour = self.current_hour.prev
                steps.append(f"Horas:    {old:02d} --prev--> {self.current_hour.data:02d}")
            old = self.current_minute.data
            self.current_minute = self.current_minute.prev
            steps.append(f"Minutos:  {old:02d} --prev--> {self.current_minute.data:02d}")
        old = self.current_second.data
        self.current_second = self.current_second.prev
        steps.append(f"Segundos: {old:02d} --prev--> {self.current_second.data:02d}")
        self.last_steps = steps
        return steps

    def change_format(self):
        self.current_format = self.current_format.next

    def hour(self):
        return self.current_hour.data

    def minute(self):
        return self.current_minute.data

    def second(self):
        return self.current_second.data

    def text(self):
        if self.current_format.data == "24 horas":
            return f"{self.hour():02d}:{self.minute():02d}:{self.second():02d}"
        hour = self.hour() % 12
        if hour == 0:
            hour = 12
        period = "a. m." if self.hour() < 12 else "p. m."
        return f"{hour:02d}:{self.minute():02d}:{self.second():02d} {period}"

    def short_text(self):
        if self.current_format.data == "24 horas":
            return f"{self.hour():02d}:{self.minute():02d}:{self.second():02d}"
        hour = self.hour() % 12
        if hour == 0:
            hour = 12
        period = "AM" if self.hour() < 12 else "PM"
        return f"{hour:02d}:{self.minute():02d}:{self.second():02d} {period}"


class Lap:
    def __init__(self, number, lap_time, total_time):
        self.number = number
        self.lap_time = lap_time
        self.total_time = total_time


class Stopwatch:
    def __init__(self):
        self.laps = CircularDoublyLinkedList()
        self.selected = None
        self.running = False
        self.elapsed = 0
        self.last_lap_total = 0
        self.lap_counter = 0

    def toggle(self):
        self.running = not self.running

    def advance(self, seconds):
        if self.running:
            self.elapsed += seconds

    def go_back(self, seconds):
        if self.running:
            self.elapsed = max(self.last_lap_total, self.elapsed - seconds)

    def add_lap(self):
        if self.elapsed == 0 or self.elapsed == self.last_lap_total:
            return None
        self.lap_counter += 1
        lap = Lap(self.lap_counter, self.elapsed - self.last_lap_total, self.elapsed)
        self.last_lap_total = self.elapsed
        self.selected = self.laps.insert_at_end(lap)
        return lap

    def next_lap(self):
        if self.selected is not None:
            self.selected = self.selected.next

    def previous_lap(self):
        if self.selected is not None:
            self.selected = self.selected.prev

    def delete_selected(self):
        if self.selected is None:
            return False
        following = self.selected.next
        alone = following == self.selected
        self.laps.delete_node(self.selected)
        self.selected = None if alone else following
        return True

    def reset(self):
        self.laps.clear()
        self.selected = None
        self.running = False
        self.elapsed = 0
        self.last_lap_total = 0
        self.lap_counter = 0

    def best_lap(self):
        laps = self.laps.to_list()
        if len(laps) < 2:
            return None
        best = laps[0]
        for lap in laps:
            if lap.lap_time < best.lap_time:
                best = lap
        return best

    def worst_lap(self):
        laps = self.laps.to_list()
        if len(laps) < 2:
            return None
        worst = laps[0]
        for lap in laps:
            if lap.lap_time > worst.lap_time:
                worst = lap
        return worst


class Pacer:
    def __init__(self, loops_per_second=26000000):
        self.loops_per_second = loops_per_second

    def wait_one_second(self):
        counter = 0
        limit = self.loops_per_second
        while counter < limit:
            counter += 1

    def adjust(self, expected_seconds, real_seconds):
        if expected_seconds <= 0 or real_seconds <= 0:
            return False
        self.loops_per_second = int(self.loops_per_second * expected_seconds / real_seconds)
        if self.loops_per_second < 1000:
            self.loops_per_second = 1000
        return True


class Theme:
    def __init__(self, name, frame, accent, hour_hand, minute_hand, second_hand):
        self.name = name
        self.frame = frame
        self.accent = accent
        self.hour_hand = hour_hand
        self.minute_hand = minute_hand
        self.second_hand = second_hand


class Painter:
    def __init__(self, terminal):
        self.terminal = terminal
        self.themes = CircularDoublyLinkedList()
        self.themes.insert_at_end(Theme("Medianoche", "38;5;97", "1;38;5;177", "1;97", "1;38;5;177", "1;38;5;214"))
        self.themes.insert_at_end(Theme("Oceano", "38;5;31", "1;38;5;81", "1;97", "1;38;5;81", "1;38;5;203"))
        self.themes.insert_at_end(Theme("Bosque", "38;5;29", "1;38;5;114", "1;97", "1;38;5;114", "1;38;5;221"))
        self.current_theme = self.themes.head
        if terminal:
            self.box = {"tl": "╔", "tr": "╗", "bl": "╚", "br": "╝", "h": "═", "v": "║",
                        "ml": "╟", "mr": "╢", "t": "─", "split": "│", "up": "┬", "down": "┴"}
        else:
            self.box = {"tl": "+", "tr": "+", "bl": "+", "br": "+", "h": "=", "v": "|",
                        "ml": "+", "mr": "+", "t": "-", "split": "|", "up": "+", "down": "+"}

    def theme(self):
        return self.current_theme.data

    def next_theme(self):
        self.current_theme = self.current_theme.next

    def color(self, text, code):
        if not self.terminal:
            return text
        return f"{ESC}[{code}m{text}{ESC}[0m"

    def frame(self, text):
        return self.color(text, self.theme().frame)

    def accent(self, text):
        return self.color(text, self.theme().accent)

    def title_bar(self, text):
        if not self.terminal:
            return text
        background = self.theme().accent.split(";")[-1]
        return f"{ESC}[1;97;48;5;{background}m{text}{ESC}[0m"

    def muted(self, text):
        return self.color(text, "38;5;244")

    def hands(self, text):
        if not self.terminal:
            return text
        result = ""
        for char in text:
            if char == "#":
                result += self.color("●", self.theme().hour_hand)
            elif char == "*":
                result += self.color("•", self.theme().minute_hand)
            elif char == "+":
                result += self.color("∙", self.theme().second_hand)
            elif char == "@":
                result += self.color("◉", self.theme().second_hand)
            elif char == ".":
                result += self.muted("·")
            elif char in "█▀▄":
                result += self.color(char, "1;97")
            elif char in "0123456789":
                result += self.color(char, "1;97")
            else:
                result += char
        return result

    def highlight(self, text):
        if not self.terminal:
            return text
        result = ""
        index = 0
        while index < len(text):
            if text[index] == "[":
                end = text.find("]", index)
                if end != -1:
                    result += self.accent(text[index:end + 1])
                    index = end + 1
                    continue
            result += text[index]
            index += 1
        return result

    def big_text(self, text):
        font = BLOCK_DIGITS if self.terminal else DIGITS
        lines = ["", "", ""]
        for char in text:
            shape = font.get(char, font[" "])
            for index in range(3):
                lines[index] += shape[index] + " "
        return lines

    def clear(self):
        if self.terminal:
            print(f"{ESC}[2J{ESC}[H", end="")

    def home(self):
        if self.terminal:
            print(f"{ESC}[H", end="")

    def clear_below(self):
        if self.terminal:
            print(f"{ESC}[J", end="")

    def hide_cursor(self):
        if self.terminal:
            print(f"{ESC}[?25l", end="")

    def show_cursor(self):
        if self.terminal:
            print(f"{ESC}[?25h", end="")


DIGITS = {
    "0": [" _ ", "| |", "|_|"],
    "1": ["   ", "  |", "  |"],
    "2": [" _ ", " _|", "|_ "],
    "3": [" _ ", " _|", " _|"],
    "4": ["   ", "|_|", "  |"],
    "5": [" _ ", "|_ ", " _|"],
    "6": [" _ ", "|_ ", "|_|"],
    "7": [" _ ", "  |", "  |"],
    "8": [" _ ", "|_|", "|_|"],
    "9": [" _ ", "|_|", " _|"],
    ":": ["   ", " . ", " . "],
    " ": ["  ", "  ", "  "],
    "A": [" _ ", "|_|", "| |"],
    "P": [" _ ", "|_|", "|  "],
    "M": ["     ", "|\\/| ", "|  | "],
}

BLOCK_DIGITS = {
    "0": ["█▀█", "█ █", "█▄█"],
    "1": ["▄█ ", " █ ", "▄█▄"],
    "2": ["▀▀█", "█▀▀", "█▄▄"],
    "3": ["▀▀█", " ▀█", "▄▄█"],
    "4": ["█ █", "▀▀█", "  █"],
    "5": ["█▀▀", "▀▀█", "▄▄█"],
    "6": ["█▀▀", "█▀█", "█▄█"],
    "7": ["▀▀█", "  █", "  █"],
    "8": ["█▀█", "█▀█", "█▄█"],
    "9": ["█▀█", "▀▀█", "▄▄█"],
    ":": [" ", "▀", "▀"],
    " ": [" ", " ", " "],
    "A": ["█▀█", "█▀█", "▀ ▀"],
    "P": ["█▀█", "█▀▀", "▀  "],
    "M": ["█▄ ▄█", "█ ▀ █", "▀   ▀"],
}


class AnalogFace:
    def __init__(self, clock):
        self.clock = clock
        self.rows = 21
        self.cols = 43
        self.center_row = 10
        self.center_col = 21
        self.radius = 10

    def position(self, step, distance):
        angle = step * 2 * PI / 60 - PI / 2
        row = self.center_row + int(round(distance * sine(angle)))
        col = self.center_col + int(round(distance * 2 * cosine(angle)))
        return row, col

    def put(self, grid, row, col, char):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            grid[row][col] = char

    def draw_hand(self, grid, step, length, char):
        distance = 1
        while distance <= length:
            row, col = self.position(step, distance)
            self.put(grid, row, col, char)
            distance += 0.5

    def lines(self):
        grid = [[" " for _ in range(self.cols)] for _ in range(self.rows)]
        node = self.clock.seconds.head
        while True:
            row, col = self.position(node.data, self.radius)
            if node.data % 5 == 0:
                number = str(node.data // 5 or 12)
                for index, char in enumerate(number):
                    self.put(grid, row, col - len(number) // 2 + index, char)
            else:
                self.put(grid, row, col, ".")
            node = node.next
            if node == self.clock.seconds.head:
                break
        second = self.clock.second()
        minute = self.clock.minute() + second / 60
        hour = self.clock.hour() % 12 + minute / 60
        self.draw_hand(grid, second, 8, "+")
        self.draw_hand(grid, minute, 7, "*")
        self.draw_hand(grid, hour * 5, 4, "#")
        self.put(grid, self.center_row, self.center_col, "@")
        return ["".join(row) for row in grid]


class Window:
    def __init__(self, painter):
        self.painter = painter
        self.box = painter.box

    def border(self, left, fill, right):
        return self.painter.frame(left + fill * WIDTH + right)

    def row(self, content):
        side = self.painter.frame(self.box["v"])
        return side + content + side

    def section(self, text, width):
        if text.startswith("§"):
            return self.painter.accent(fit(" " + text[1:], width))
        return self.painter.highlight(fit(text, width))

    def split_row(self, left, right):
        left_text = " " + self.painter.hands(fit(left, LEFT_WIDTH - 1))
        return self.row(left_text + self.painter.frame(self.box["split"]) + self.section(right, RIGHT_WIDTH))

    def build(self, title, status, body, buttons, message, split=True):
        box = self.box
        lines = [self.border(box["tl"], box["h"], box["tr"])]
        title_text = fit("  " + title, WIDTH - len(status) - 2) + status + "  "
        lines.append(self.row(self.painter.title_bar(title_text)))
        if split:
            lines.append(self.painter.frame(box["ml"] + box["t"] * LEFT_WIDTH + box["up"] + box["t"] * RIGHT_WIDTH + box["mr"]))
            for left, right in body:
                lines.append(self.split_row(left, right))
            lines.append(self.painter.frame(box["ml"] + box["t"] * LEFT_WIDTH + box["down"] + box["t"] * RIGHT_WIDTH + box["mr"]))
        else:
            lines.append(self.border(box["ml"], box["t"], box["mr"]))
            for content in body:
                lines.append(self.row(self.section(content, WIDTH)))
            lines.append(self.border(box["ml"], box["t"], box["mr"]))
        for button_line in buttons:
            lines.append(self.row(self.painter.highlight(fit(button_line, WIDTH))))
        lines.append(self.border(box["ml"], box["t"], box["mr"]))
        lines.append(self.row(self.painter.muted(fit("  " + message, WIDTH))))
        lines.append(self.border(box["bl"], box["h"], box["br"]))
        return lines

    def show(self, lines, redraw=False):
        if redraw:
            self.painter.home()
        else:
            self.painter.clear()
            print()
        for line in lines:
            print(line)
        self.painter.clear_below()


class App:
    def __init__(self, terminal):
        self.painter = Painter(terminal)
        self.window = Window(self.painter)
        self.clock = Clock(0, 0, 0)
        self.face = AnalogFace(self.clock)
        self.stopwatch = Stopwatch()
        self.pacer = Pacer()
        self.message = "Bienvenido. Escribe la letra de un boton y presiona Enter."
        self.screen = "clock"

    def pointer_line(self, label, node):
        return f" {fit(label, 9)}{node.prev.data:02d} <- [{node.data:02d}] -> {node.next.data:02d}"

    def clock_screen(self, status=None):
        right = [
            "§HORA DIGITAL",
            f" {self.clock.text()}",
            f" Formato: {self.clock.current_format.data}",
            "",
            "§MANECILLAS EN LAS LISTAS",
            self.pointer_line("Horas", self.clock.current_hour),
            self.pointer_line("Minutos", self.clock.current_minute),
            self.pointer_line("Segundos", self.clock.current_second),
            "  anterior <- actual -> sig.",
            "",
            "§CRONOMETRO",
            f" {format_duration(self.stopwatch.elapsed)}  {'corriendo' if self.stopwatch.running else 'detenido'}",
            f" Vueltas: {self.stopwatch.laps.size}",
            "",
            " ● hora  • minutos  ∙ segundos" if self.painter.terminal else " # hora   * minutos   + seg.",
            "",
            "§ULTIMO MOVIMIENTO",
        ]
        for step in self.clock.last_steps[-4:]:
            right.append(" " + step.strip())
        if not self.clock.last_steps:
            right.append(" (ninguno todavia)")
        face = self.face.lines()
        body = []
        for index in range(len(face)):
            body.append((face[index], right[index] if index < len(right) else ""))
        digital = self.painter.big_text(self.clock.short_text())
        for line in digital:
            body.append((center(line.rstrip(), LEFT_WIDTH - 1), ""))
        buttons = [
            " [A] Avanzar  [R] Retroceder  [H] Ajustar hora  [M] En marcha  [F] 12/24h",
            " [C] Cronometro [E] Estructura [P] Pruebas [K] Calibrar [T] Tema [S] Salir",
        ]
        title = "RELOJ CIRCULAR  -  Listas circulares dobles"
        return self.window.build(title, status or f"Tema: {self.painter.theme().name}", body, buttons, self.message)

    def ring_lines(self, label, ring, current):
        left = current.prev.prev
        right = current.next.next
        return [
            f"§{fit(label, 9)}({ring.size} nodos)   head = {ring.head.data:02d}   ultimo = {ring.head.prev.data:02d}   ultimo.next = {ring.head.prev.next.data:02d}",
            f"    ... <-> {left.data:02d} <-> {current.prev.data:02d} <-> [{current.data:02d}] <-> {current.next.data:02d} <-> {right.data:02d} <-> ...",
        ]

    def structure_screen(self):
        body = [
            " Cada nodo guarda: data, prev (anterior) y next (siguiente).",
            " El ultimo nodo apunta a head y head al ultimo: la lista es un anillo.",
            "",
        ]
        body += self.ring_lines("HORAS", self.clock.hours, self.clock.current_hour)
        body.append("")
        body += self.ring_lines("MINUTOS", self.clock.minutes, self.clock.current_minute)
        body.append("")
        body += self.ring_lines("SEGUNDOS", self.clock.seconds, self.clock.current_second)
        body.append("")
        body.append(f" Hora actual: {self.clock.text()}")
        body.append("")
        body.append("§ULTIMO PASO")
        steps = self.clock.last_steps or ["(presiona [N] o [B] para mover los punteros)"]
        for step in steps:
            body.append("   " + step)
        while len(body) < 21:
            body.append("")
        buttons = [
            " [N] Siguiente segundo (next)  [B] Segundo anterior (prev)  [H] Ajustar hora",
            " [X] Volver al reloj",
        ]
        return self.window.build("ESTRUCTURA  -  Lista circular doble", self.clock.short_text(), body, buttons, self.message, split=False)

    def stopwatch_screen(self):
        left = [""]
        for line in self.painter.big_text(format_duration(self.stopwatch.elapsed)):
            left.append(center(line.rstrip(), LEFT_WIDTH - 1))
        left.append(center("corriendo" if self.stopwatch.running else "detenido", LEFT_WIDTH - 1))
        left.append("")
        left.append("      Vta  Parcial    Total")
        laps = self.stopwatch.laps.to_list()
        best = self.stopwatch.best_lap()
        worst = self.stopwatch.worst_lap()
        if not laps:
            left.append("   Todavia no hay vueltas.")
        visible = laps
        if len(laps) > 12:
            position = 0
            for index in range(len(laps)):
                if laps[index] is self.stopwatch.selected.data:
                    position = index
            start = max(0, min(position - 6, len(laps) - 12))
            visible = laps[start:start + 12]
        for lap in visible:
            marker = ">>" if self.stopwatch.selected is not None and lap is self.stopwatch.selected.data else "  "
            tag = ""
            if lap is best:
                tag = " rapida"
            elif lap is worst:
                tag = " lenta"
            left.append(f"   {marker} {lap.number:>2}   {format_duration(lap.lap_time)}  {format_duration(lap.total_time)}{tag}")
        right = [
            "§ESTADO",
            f" {'Corriendo' if self.stopwatch.running else 'Detenido'}",
            f" Vueltas: {self.stopwatch.laps.size}",
            "",
            "§VUELTA SELECCIONADA",
        ]
        selected = self.stopwatch.selected
        if selected is None:
            right.append(" ninguna")
        else:
            right.append(f" Vuelta {selected.data.number}: {format_duration(selected.data.lap_time)}")
            right.append(f" prev -> vuelta {selected.prev.data.number}")
            right.append(f" next -> vuelta {selected.next.data.number}")
        right.append("")
        right.append("§MAS RAPIDA")
        right.append(f" Vuelta {best.number}: {format_duration(best.lap_time)}" if best else " -")
        right.append("§MAS LENTA")
        right.append(f" Vuelta {worst.number}: {format_duration(worst.lap_time)}" if worst else " -")
        right.append("")
        right.append(" Avanza junto con el reloj.")
        right.append(f" Reloj: {self.clock.short_text()}")
        body = []
        for index in range(21):
            body.append((left[index] if index < len(left) else "", right[index] if index < len(right) else ""))
        buttons = [
            " [I] Iniciar/Pausar  [V] Vuelta  [A] Avanzar tiempo  [D] Eliminar vuelta",
            " [>] Siguiente vuelta  [<] Vuelta anterior  [Z] Reiniciar  [X] Volver",
        ]
        return self.window.build("CRONOMETRO CON VUELTAS", format_duration(self.stopwatch.elapsed), body, buttons, self.message)

    def tests_screen(self, results):
        body = []
        half = (len(results) + 1) // 2
        for index in range(half):
            left = results[index]
            right = results[index + half] if index + half < len(results) else None
            text = " " + fit(self.result_text(left), 37)
            if right is not None:
                text += " " + self.result_text(right)
            body.append(text)
        while len(body) < 21:
            body.append("")
        buttons = [" [P] Ejecutar otra vez   [X] Volver al reloj"]
        return self.window.build("PRUEBAS DE FUNCIONAMIENTO", "", body, buttons, self.message, split=False)

    def result_text(self, result):
        description, passed = result
        return ("OK    " if passed else "FALLO ") + description

    def render(self):
        if self.screen == "clock":
            self.window.show(self.clock_screen())
        elif self.screen == "structure":
            self.window.show(self.structure_screen())
        elif self.screen == "stopwatch":
            self.window.show(self.stopwatch_screen())

    def move(self, seconds, forward):
        for _ in range(seconds):
            if forward:
                self.clock.tick()
            else:
                self.clock.tick_back()
        if forward:
            self.stopwatch.advance(seconds)
        else:
            self.stopwatch.go_back(seconds)

    def ask_amount(self, verb):
        unit = read_option(f"  {verb} en [S] segundos o [M] minutos: ", "SM")
        if unit == "S":
            return read_int("  Cuantos segundos (1-3600): ", 1, 3600)
        return read_int("  Cuantos minutos (1-1440): ", 1, 1440) * 60

    def ask_time(self):
        hour, minute, second = ask_time()
        self.clock.set_time(hour, minute, second)
        self.clock.last_steps = []
        self.message = f"Hora ajustada a {self.clock.text()}."

    def run_forever(self):
        count = 0
        self.painter.hide_cursor()
        try:
            while True:
                self.message = "Reloj en marcha. Presiona Ctrl+C para usar los botones."
                self.window.show(self.clock_screen(status="EN MARCHA"), redraw=count > 0)
                self.pacer.wait_one_second()
                self.clock.tick()
                self.stopwatch.advance(1)
                count += 1
        except KeyboardInterrupt:
            self.painter.show_cursor()
            self.message = f"Reloj detenido tras {count} segundos. Usa [M] para ponerlo en marcha otra vez."

    def run_live(self):
        if self.painter.terminal:
            self.run_forever()
            return
        seconds = read_int("  Cuantos segundos dejar el reloj en marcha (5-300): ", 5, 300)
        if not self.painter.terminal:
            print()
            print("  Reloj en marcha...")
        for number in range(1, seconds + 1):
            self.pacer.wait_one_second()
            self.clock.tick()
            self.stopwatch.advance(1)
            if self.painter.terminal:
                self.message = f"En marcha: segundo {number} de {seconds}"
                self.window.show(self.clock_screen(status=f"EN MARCHA {number}/{seconds}"))
            else:
                line = f"  {self.clock.text()}"
                if self.stopwatch.running:
                    line += f"    cronometro {format_duration(self.stopwatch.elapsed)}"
                print(line)
        self.message = f"El reloj corrio {seconds} segundos."

    def calibrate(self):
        print()
        print("  CALIBRAR: el reloj va a contar 10 segundos.")
        print("  Al ver 'YA' inicia el cronometro de tu celular y detenlo en 'FIN'.")
        input("  Presiona Enter para empezar...")
        print("  YA")
        for number in range(1, 11):
            self.pacer.wait_one_second()
            print(f"  {number}")
        print("  FIN")
        real = read_int("  Cuantos segundos marco tu celular (1-60): ", 1, 60)
        self.pacer.adjust(10, real)
        if real == 10:
            self.message = "El reloj ya estaba bien calibrado."
        elif real > 10:
            self.message = "El reloj iba lento, ahora va mas rapido."
        else:
            self.message = "El reloj iba rapido, ahora va mas lento."

    def run_tests(self):
        tester = Tester()
        results = tester.run()
        self.message = f"{tester.passed} pruebas correctas, {tester.failed} fallidas."
        while True:
            self.window.show(self.tests_screen(results))
            option = read_option("  Boton: ", "PX")
            if option == "X":
                self.message = "Listo."
                return
            results = tester.run()
            self.message = f"{tester.passed} pruebas correctas, {tester.failed} fallidas."

    def clock_action(self, option):
        if option == "A":
            self.move(self.ask_amount("Avanzar"), True)
            self.message = f"Reloj avanzado. Hora: {self.clock.text()}"
        elif option == "R":
            self.move(self.ask_amount("Retroceder"), False)
            self.message = f"Reloj retrocedido. Hora: {self.clock.text()}"
        elif option == "H":
            self.ask_time()
        elif option == "M":
            self.run_live()
        elif option == "F":
            self.clock.change_format()
            self.message = f"Formato cambiado a {self.clock.current_format.data}."
        elif option == "C":
            self.screen = "stopwatch"
            self.message = "El cronometro avanza cuando avanza el reloj."
        elif option == "E":
            self.screen = "structure"
            self.message = "Mueve los punteros y mira como cambia cada anillo."
        elif option == "P":
            self.run_tests()
        elif option == "K":
            self.calibrate()
        elif option == "T":
            self.painter.next_theme()
            if self.painter.terminal:
                self.message = f"Tema cambiado a {self.painter.theme().name}."
            else:
                self.message = "Los temas de color solo se ven en la terminal del PC."
        elif option == "S":
            return False
        return True

    def structure_action(self, option):
        if option == "N":
            self.clock.tick()
            self.stopwatch.advance(1)
            self.message = "Se movio el puntero con next."
        elif option == "B":
            self.clock.tick_back()
            self.stopwatch.go_back(1)
            self.message = "Se movio el puntero con prev."
        elif option == "H":
            self.ask_time()
        elif option == "X":
            self.screen = "clock"
            self.message = "De vuelta en el reloj."

    def stopwatch_action(self, option):
        if option == "I":
            self.stopwatch.toggle()
            self.message = "Cronometro iniciado." if self.stopwatch.running else "Cronometro en pausa."
        elif option == "V":
            lap = self.stopwatch.add_lap()
            if lap is None:
                self.message = "Primero inicia el cronometro y avanza el tiempo."
            else:
                self.message = f"Vuelta {lap.number} registrada: {format_duration(lap.lap_time)}"
        elif option == "A":
            self.move(self.ask_amount("Avanzar"), True)
            self.message = f"Tiempo avanzado. Cronometro: {format_duration(self.stopwatch.elapsed)}"
        elif option == ">":
            self.stopwatch.next_lap()
            self.message = "Puntero next: siguiente vuelta."
        elif option == "<":
            self.stopwatch.previous_lap()
            self.message = "Puntero prev: vuelta anterior."
        elif option == "D":
            if self.stopwatch.delete_selected():
                self.message = "Vuelta eliminada de la lista."
            else:
                self.message = "No hay vueltas para eliminar."
        elif option == "Z":
            self.stopwatch.reset()
            self.message = "Cronometro reiniciado."
        elif option == "X":
            self.screen = "clock"
            self.message = "De vuelta en el reloj."

    def start(self):
        self.ask_time()
        self.message = "Bienvenido. Escribe la letra de un boton y presiona Enter."
        if self.painter.terminal:
            self.run_forever()
        try:
            self.loop()
        except KeyboardInterrupt:
            print()
            print("  Gracias por usar el reloj circular.")

    def loop(self):
        while True:
            self.render()
            if self.screen == "clock":
                option = read_option("  Boton: ", "ARHMFCEPKTS")
                if not self.clock_action(option):
                    self.painter.clear()
                    print()
                    print("  Gracias por usar el reloj circular.")
                    return
            elif self.screen == "structure":
                self.structure_action(read_option("  Boton: ", "NBHX"))
            else:
                self.stopwatch_action(read_option("  Boton: ", "IVA><DZX"))


class Tester:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.results = []

    def check(self, description, result, expected):
        passed = result == expected
        if passed:
            self.passed += 1
        else:
            self.failed += 1
        self.results.append((description, passed))

    def run(self):
        self.passed = 0
        self.failed = 0
        self.results = []
        self.test_list()
        self.test_clock()
        self.test_stopwatch()
        self.test_drawing()
        return self.results

    def test_list(self):
        numbers = CircularDoublyLinkedList()
        self.check("Lista nueva vacia", numbers.is_empty(), True)
        numbers.insert_at_end(2)
        self.check("Un nodo se apunta a si mismo", numbers.head.next == numbers.head and numbers.head.prev == numbers.head, True)
        numbers.insert_at_end(3)
        numbers.insert_at_beginning(1)
        self.check("Insertar al inicio y al final", numbers.to_list(), [1, 2, 3])
        self.check("Ultimo nodo apunta a head", numbers.head.prev.next.data, 1)
        self.check("head.prev es el ultimo", numbers.head.prev.data, 3)
        self.check("Tamano de la lista", numbers.size, 3)
        self.check("Buscar valor que existe", numbers.find(2).data, 2)
        self.check("Buscar valor que no existe", numbers.find(9), None)
        self.check("Eliminar el head", numbers.delete(1), True)
        self.check("Lista despues de eliminar", numbers.to_list(), [2, 3])
        self.check("Eliminar valor inexistente", numbers.delete(9), False)
        numbers.delete(2)
        numbers.delete(3)
        self.check("Vacia al eliminar todo", numbers.is_empty(), True)

    def test_clock(self):
        clock = Clock(10, 30, 59)
        clock.tick()
        self.check("10:30:59 avanza a 10:31:00", (clock.hour(), clock.minute(), clock.second()), (10, 31, 0))
        clock.set_time(23, 59, 59)
        clock.tick()
        self.check("23:59:59 avanza a 00:00:00", (clock.hour(), clock.minute(), clock.second()), (0, 0, 0))
        clock.tick_back()
        self.check("00:00:00 retrocede a 23:59:59", (clock.hour(), clock.minute(), clock.second()), (23, 59, 59))
        clock.set_time(12, 0, 0)
        for _ in range(3600):
            clock.tick()
        self.check("3600 segundos suman 1 hora", clock.hour(), 13)
        self.check("Formato 12 horas", clock.text(), "01:00:00 p. m.")
        clock.change_format()
        self.check("Formato 24 horas", clock.text(), "13:00:00")
        clock.change_format()
        self.check("Formatos dan la vuelta", clock.current_format.data, "12 horas")
        self.check("Anillo de horas: 24 nodos", clock.hours.size, 24)
        self.check("Anillo de segundos: 60 nodos", clock.seconds.size, 60)

    def test_stopwatch(self):
        stopwatch = Stopwatch()
        stopwatch.advance(10)
        self.check("Cronometro detenido no avanza", stopwatch.elapsed, 0)
        self.check("Sin tiempo no hay vuelta", stopwatch.add_lap(), None)
        stopwatch.toggle()
        stopwatch.advance(20)
        stopwatch.add_lap()
        stopwatch.advance(5)
        stopwatch.add_lap()
        stopwatch.advance(30)
        stopwatch.add_lap()
        self.check("Se registran 3 vueltas", stopwatch.laps.size, 3)
        self.check("Parcial de la vuelta 2", stopwatch.laps.head.next.data.lap_time, 5)
        self.check("Vuelta mas rapida", stopwatch.best_lap().number, 2)
        self.check("Vuelta mas lenta", stopwatch.worst_lap().number, 3)
        stopwatch.next_lap()
        self.check("Tras la ultima sigue la primera", stopwatch.selected.data.number, 1)
        stopwatch.previous_lap()
        self.check("Antes de la 1ra esta la ultima", stopwatch.selected.data.number, 3)
        stopwatch.delete_selected()
        self.check("Eliminar vuelta seleccionada", stopwatch.laps.size, 2)
        stopwatch.reset()
        self.check("Reiniciar borra las vueltas", stopwatch.laps.is_empty(), True)

    def test_drawing(self):
        self.check("Seno de 90 grados", round(sine(PI / 2), 4), 1.0)
        self.check("Coseno de 0 grados", round(cosine(0), 4), 1.0)
        self.check("Formato de duracion", format_duration(3725), "01:02:05")
        self.check("La caratula tiene 21 filas", len(AnalogFace(Clock(3, 0, 0)).lines()), 21)
        for terminal, name in ((False, "texto simple"), (True, "con colores")):
            app = App(terminal)
            app.stopwatch.toggle()
            app.stopwatch.advance(30)
            app.stopwatch.add_lap()
            same = True
            for screen in (app.clock_screen(), app.structure_screen(), app.stopwatch_screen()):
                for line in screen:
                    if visible_length(line) != WIDTH + 2:
                        same = False
            self.check(f"Bordes alineados ({name})", same, True)
        pacer = Pacer(1000000)
        pacer.adjust(10, 20)
        self.check("Calibrar si va lento", pacer.loops_per_second, 500000)
        pacer.adjust(10, 5)
        self.check("Calibrar si va rapido", pacer.loops_per_second, 1000000)
        self.check("No calibrar con tiempo 0", pacer.adjust(10, 0), False)


def read_int(message, minimum, maximum):
    while True:
        value = input(message).strip()
        try:
            number = int(value)
        except ValueError:
            print(f"  Escribe un numero entre {minimum} y {maximum}.")
            continue
        if minimum <= number <= maximum:
            return number
        print(f"  Escribe un numero entre {minimum} y {maximum}.")


def read_option(message, options):
    while True:
        value = input(message).strip().upper()
        if len(value) == 1 and value in options:
            return value
        print(f"  Opcion no valida. Usa una de estas: {' '.join(options)}")


def ask_time():
    print()
    print("  Ingresa la hora inicial del reloj (formato 24 horas)")
    hour = read_int("  Hora (0-23): ", 0, 23)
    minute = read_int("  Minutos (0-59): ", 0, 59)
    second = read_int("  Segundos (0-59): ", 0, 59)
    return hour, minute, second


def main():
    app = App(True)
    painter = app.painter
    painter.clear()
    print()
    print(painter.frame("╔" + "═" * WIDTH + "╗"))
    print(painter.frame("║") + painter.title_bar(center("RELOJ CIRCULAR  -  TALLER DE ESTRUCTURAS DE DATOS", WIDTH)) + painter.frame("║"))
    print(painter.frame("║") + center("Listas circulares doblemente enlazadas", WIDTH) + painter.frame("║"))
    print(painter.frame("╚" + "═" * WIDTH + "╝"))
    app.start()


main()
