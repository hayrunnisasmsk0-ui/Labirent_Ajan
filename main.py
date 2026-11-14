
import pygame
from collections import deque
import heapq
import time

# 1. Pygame'i başlat
pygame.init()

# 2. Labirent boyutları
ROWS = 20
COLS = 50
CELL_SIZE = 18

# 3. Pencere boyutları
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

# 4. Ekranı oluştur
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Labirentte Yol Bulan Ajan")

# 5. Renkleri tanımla
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (220, 0, 0)
GRAY = (180, 180, 180)

# 6. Başlangıç ve hedef
start = (0, 0)
goal = (ROWS - 1, COLS - 1)

# 7. Labirent listesini oluştur
maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]
visited_cells = set()
path_cells = set()

# Animasyon için değişkenler
animation_order = []
animation_index = 0

animation_path = []
path_animation_index = 0

animation_running = False
showing_path = False


# Manhattan mesafesi - A* ALGORİTMASI İÇİN
def heuristic(a, b):

    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# BFS - Breadth First Search
def bfs():

    # 1. Başlangıç kuyruğu
    queue = deque([start])

    # 2. Ziyaret edilen hücreler
    visited = {start}

    # 3. Her hücrenin önceki hücresini tut
    parent = {}

    # 4. Arama sırasını kaydet
    visited_order = []

    # 5. Kuyruk boşalana kadar devam et
    while queue:

        # Kuyruğun başındaki hücreyi al
        current = queue.popleft()

        # Ziyaret sırasına ekle
        visited_order.append(current)

        # Hedefe ulaştık mı?
        if current == goal:

            # Bulunan yolu geriye doğru oluştur
            path = []
            node = goal

            while node != start:
                path.append(node)
                node = parent[node]

            path.append(start)

            # Başlangıçtan hedefe doğru sırala
            path.reverse()

            return visited_order, path

        # Dört hareket yönü
        directions = [
            (-1, 0),  # Yukarı
            (1, 0),   # Aşağı
            (0, -1),  # Sol
            (0, 1)    # Sağ
        ]

        # Komşuları kontrol et
        for dr, dc in directions:

            new_row = current[0] + dr
            new_col = current[1] + dc

            neighbor = (new_row, new_col)

            # Grid sınırları içinde mi?
            if 0 <= new_row < ROWS and 0 <= new_col < COLS:

                # Duvar değil ve daha önce ziyaret edilmemiş mi?
                if maze[new_row][new_col] == 0 and neighbor not in visited:

                    # Ziyaret edildi olarak işaretle
                    visited.add(neighbor)

                    # Önceki hücreyi kaydet
                    parent[neighbor] = current

                    # Kuyruğa ekle
                    queue.append(neighbor)

    # Hedefe ulaşılmadıysa
    return visited_order, []

# DFS - Depth First Search
def dfs():

    # Başlangıç yığını
    stack = [start]

    # Ziyaret edilen hücreler
    visited = {start}

    # Önceki hücreleri tut
    parent = {}

    # Ziyaret sırası
    visited_order = []

    # Yığın boşalana kadar devam et
    while stack:

        # Son eklenen hücreyi al
        current = stack.pop()

        visited_order.append(current)

        # Hedefe ulaştık mı?
        if current == goal:

            path = []
            node = goal

            while node != start:
                path.append(node)
                node = parent[node]

            path.append(start)
            path.reverse()

            return visited_order, path

        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

        for dr, dc in directions:

            new_row = current[0] + dr
            new_col = current[1] + dc

            neighbor = (new_row, new_col)

            if 0 <= new_row < ROWS and 0 <= new_col < COLS:

                if maze[new_row][new_col] == 0 and neighbor not in visited:

                    visited.add(neighbor)

                    parent[neighbor] = current

                    stack.append(neighbor)

    return visited_order, []

# A* - A Star Search
def astar():
    

    # Öncelik kuyruğu
    open_list = []

    # Başlangıç hücresini kuyruğa ekle
    heapq.heappush(
        open_list,
        (heuristic(start, goal), 0, start)
    )

    # Hücrelerin önceki konumları
    parent = {}

    # Başlangıçtan hücreye gerçek maliyet
    g_score = {start: 0}

    # Ziyaret edilen hücreler
    visited = set()

    # Ziyaret sırası
    visited_order = []

    while open_list:

        # En düşük tahmini maliyetli hücreyi al
        f, g, current = heapq.heappop(open_list)

        # Daha önce işlendi ise atla
        if current in visited:
            continue

        visited.add(current)
        visited_order.append(current)

        # Hedefe ulaşıldı mı?
        if current == goal:

            path = []
            node = goal

            while node != start:
                path.append(node)
                node = parent[node]

            path.append(start)
            path.reverse()

            return visited_order, path

        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

        for dr, dc in directions:

            new_row = current[0] + dr
            new_col = current[1] + dc

            neighbor = (new_row, new_col)

            # Grid sınırlarını kontrol et
            if 0 <= new_row < ROWS and 0 <= new_col < COLS:

                # Duvar kontrolü
                if maze[new_row][new_col] == 0:

                    if neighbor not in visited:

                        # Yeni gerçek maliyet
                        tentative_g = g_score[current] + 1

                        if tentative_g < g_score.get(neighbor, float("inf")):

                            parent[neighbor] = current

                            g_score[neighbor] = tentative_g

                            f_score = (
                                tentative_g +
                                heuristic(neighbor, goal)
                            )

                            heapq.heappush(
                                open_list,
                                (f_score, tentative_g, neighbor)
                            )

    return visited_order, []


# HYBRID - BFS + A*
def hybrid():

    print("\n--- HIBRIT ALGORITMA BASLADI ---")

    # 1. Aşama: BFS ile erişilebilirliği kontrol et
    bfs_order, bfs_path = bfs()

    print("BFS kontrolu tamamlandi.")
    print("BFS ziyaret edilen:", len(bfs_order))

    # BFS hedefe ulaşamadıysa işlemi bitir
    if not bfs_path:
        print("Hedefe ulasilamiyor!")
        return bfs_order, [], len(bfs_order), 0

    # 2. Aşama: A* ile en kısa yolu bul
    astar_order, astar_path = astar()

    print("A* aramasi tamamlandi.")
    print("A* ziyaret edilen:", len(astar_order))

    # İki algoritmanın ziyaret sırasını birleştir
    combined_order = list(dict.fromkeys(
        bfs_order + astar_order
    ))

    return (
        combined_order,
        astar_path,
        len(bfs_order),
        len(astar_order)
    )


# 8. Labirenti ekrana çiz
def draw_grid():

    for row in range(ROWS):
        for col in range(COLS):

            x = col * CELL_SIZE
            y = row * CELL_SIZE

            rect = pygame.Rect(
                x, y, CELL_SIZE, CELL_SIZE
            )

            cell = (row, col)

            if cell == start:
                color = GREEN

            elif cell == goal:
                color = RED

            elif maze[row][col] == 1:
                color = BLACK

            elif cell in path_cells:
                color = (255, 220, 0)

            elif cell in visited_cells:
                color = (100, 180, 255)

            else:
                color = WHITE

            pygame.draw.rect(screen, color, rect)

            pygame.draw.rect(screen, GRAY, rect, 1)



# 9. Ana program döngüsü

running = True
clock = pygame.time.Clock()

while running:

    for event in pygame.event.get():

        # Pencereyi kapatma
        if event.type == pygame.QUIT:
            running = False

        # Fare tıklaması
        elif event.type == pygame.MOUSEBUTTONDOWN:

            x, y = pygame.mouse.get_pos()

            col = x // CELL_SIZE
            row = y // CELL_SIZE

            if (row, col) != start and (row, col) != goal:

                # Sol tık: Duvar ekle
                if event.button == 1:
                    maze[row][col] = 1

                # Sağ tık: Duvar sil
                elif event.button == 3:
                    maze[row][col] = 0

    

        # Klavye kontrolleri
        elif event.type == pygame.KEYDOWN:

            # B tuşu: BFS
            if event.key == pygame.K_b:

                start_time = time.perf_counter()
                visited_order, path = bfs()
                end_time = time.perf_counter()

                elapsed_time = end_time - start_time

                visited_cells.clear()
                path_cells.clear()

                animation_order = visited_order
                animation_index = 0
                animation_path = path
                path_animation_index = 0

                animation_running = True
                showing_path = False

                print("BFS ziyaret edilen:", len(visited_order))
                print("BFS yol uzunluğu:", len(path))
                print("BFS çalışma süresi:", round(elapsed_time * 1000, 3), "ms")

            # D tuşu: DFS
            elif event.key == pygame.K_d:

                start_time = time.perf_counter()
                visited_order, path = dfs()
                end_time = time.perf_counter()

                elapsed_time = end_time - start_time

                visited_cells.clear()
                path_cells.clear()

                animation_order = visited_order
                animation_index = 0
                animation_path = path
                path_animation_index = 0

                animation_running = True
                showing_path = False

                print("DFS ziyaret edilen:", len(visited_order))
                print("DFS yol uzunluğu:", len(path))
                print("DFS çalışma süresi:", round(elapsed_time * 1000, 3), "ms")

            # A tuşu: A*
            elif event.key == pygame.K_a:

                start_time = time.perf_counter()
                visited_order, path = astar()
                end_time = time.perf_counter()

                elapsed_time = end_time - start_time

                visited_cells.clear()
                path_cells.clear()

                animation_order = visited_order
                animation_index = 0
                animation_path = path
                path_animation_index = 0

                animation_running = True
                showing_path = False

                print("A* ziyaret edilen:", len(visited_order))
                print("A* yol uzunluğu:", len(path))
                print("A* çalışma süresi:", round(elapsed_time * 1000, 3), "ms")

            # H tuşu: Hibrit BFS + A*
            elif event.key == pygame.K_h:

                start_time = time.perf_counter()
                visited_order, path, bfs_count, astar_count = hybrid()
                end_time = time.perf_counter()

                elapsed_time = end_time - start_time

                visited_cells.clear()
                path_cells.clear()

                animation_order = visited_order
                animation_index = 0
                animation_path = path
                path_animation_index = 0

                animation_running = True
                showing_path = False

                print("Hibrit toplam benzersiz ziyaret:", len(visited_order))
                print("Hibrit yol uzunluğu:", len(path))
                print("BFS ziyaret:", bfs_count)
                print("A* ziyaret:", astar_count)
                print("Hibrit çalışma süresi:", round(elapsed_time * 1000, 3), "ms")

    # Animasyon
    if animation_running:

        # Önce ziyaret edilen hücreleri göster
        if not showing_path:

            for _ in range(5):

                if animation_index < len(animation_order):

                    cell = animation_order[animation_index]
                    visited_cells.add(cell)
                    animation_index += 1

                else:
                    showing_path = True
                    break

            if animation_index >= len(animation_order):
                showing_path = True

        # Sonra bulunan yolu göster
        else:

            for _ in range(2):

                if path_animation_index < len(animation_path):

                    cell = animation_path[path_animation_index]
                    path_cells.add(cell)
                    path_animation_index += 1

                else:
                    animation_running = False
                    break

            if path_animation_index >= len(animation_path):
                animation_running = False

    # Ekranı güncelle
    screen.fill(WHITE)
    draw_grid()
    pygame.display.update()

    clock.tick(60)

pygame.quit()
