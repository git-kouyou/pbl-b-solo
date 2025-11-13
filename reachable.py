import typing
from collections import deque

X = 0
Y = 1

# 盤面表現: board[y][x]
# セル値: 0 = safe, -1 = food, >0 = body (その値はそのマスが何ターン後に空くかを示す)

DEBUG = False

class Reachable:
    def __init__(self, foods, bodies, width, height) -> None:
        self.width = width
        self.height = height
        self.board = self.generate_board(foods, bodies)
        if DEBUG:
            self.print_board()


    def generate_board(self, foods, bodies):
        # 盤面を初期化
        result = [[0] * (self.width) for _ in range(self.height)]
        # 体
        for i, body in enumerate(bodies):
            if body[X] - 1 < 0 and body[Y] - 1 < 0:
                continue
            result[body[Y] - 1][body[X] - 1] = len(bodies) - i
        # 食べ物
        for food in foods:
            result[food[Y] - 1][food[X] - 1] = -1
        return result

    def is_reachable_tail(self, start: tuple[int, int], goal: tuple[int, int]) -> int:
        start = (start[X] - 1, start[Y] - 1)
        goal = (goal[X] - 1, goal[Y] - 1)
        if start == goal:
            return True
        visited = [[False] * self.width for _ in range(self.height)]
        visited[start[Y]][start[X]] = True

        queue = deque([(start[X], start[Y], 0)])
        while queue:
            x, y, depth = queue.popleft()
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                nd = depth + 1
                if 0 <= nx < self.width and 0 <= ny < self.height and not visited[ny][nx]:
                    if self.board[ny][nx] <= depth:
                        if (nx, ny) == goal:
                            return True
                        visited[ny][nx] = True
                        queue.append((nx, ny, nd))
        return False
    
    def is_reachable_tail_food_avoidance(self, start: tuple[int, int], goal: tuple[int, int]) -> bool:
        start = (start[X] - 1, start[Y] - 1)
        goal = (goal[X] - 1, goal[Y] - 1)
        if start == goal:
            return True
        visited = [[False] * self.height for _ in range(self.width)]
        visited[start[Y]][start[X]] = True

        queue = deque([(start[X], start[Y], 0)])
        while queue:
            x, y, depth = queue.popleft()
            nd = depth + 1
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.height and 0 <= ny < self.width and not visited[ny][nx]:
                    if 0 <= self.board[ny][nx] <= depth:
                        if (nx, ny) == goal:
                            return True
                        visited[ny][nx] = True
                        queue.append((nx, ny, nd))
        return False
    
    def print_board(self):
        for y in reversed(range(self.height)):
            row = ""
            for x in range(self.width):
                row += f"{self.board[y][x]}".rjust(2) + " "
            print(row)
        print()
    
if __name__ == "__main__":
    DEBUG = True
    foods = {(1, 2), (4, 1), (4, 5)}
    bodies = deque([(2, 5), (1, 5), (1, 4), (2, 4)])
    print(Reachable(foods = foods, bodies = bodies, width = 6, height = 6).is_reachable_tail_food_avoidance((3, 2), (5, 1)))