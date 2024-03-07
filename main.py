# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
import sys


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Group9",  # TODO: Your Battlesnake Username
        "color": "#355e3b",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"
    width = game_state["board"]["width"]
    height = game_state["board"]["height"]

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False
    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False
    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False
    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # Extract board dimensions
    head_x = game_state["you"]["head"]["x"]
    head_y = game_state["you"]["head"]["y"]

    # Available moves (up, down, left, right)
    possible_moves = ["up", "down", "left", "right"]

    # Removing moves that would lead out of bounds
    if head_x == 0:
        possible_moves.remove("left")
    if head_x == width - 1:
        possible_moves.remove("right")
    if head_y == 0:
        possible_moves.remove("down")
    if head_y == height - 1:
        possible_moves.remove("up")

    # Are there any safe moves left?
    visited_positions = set()
    for segment in game_state["you"]["body"]:
        visited_positions.add((segment["x"], segment["y"]))

    safe_moves = []
    for move in possible_moves:
        next_position = calculate_next_position(my_head, move)
        if is_move_within_bounds(next_position, game_state) and not is_move_colliding(next_position, visited_positions):
            safe_moves.append(move)
    

    print("Safe moves:", safe_moves)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    print(f"MOVE {game_state['turn']}: {next_move}")

    return {"move": next_move}


def calculate_next_position(head: dict, move: str) -> typing.Tuple[int, int]:
    if move == "up":
        return head["x"], head["y"] + 1
    elif move == "down":
        return head["x"], head["y"] - 1
    elif move == "left":
        return head["x"] - 1, head["y"]
    elif move == "right":
        return head["x"] + 1, head["y"]


def is_move_within_bounds(position: typing.Tuple[int, int], game_state: typing.Dict) -> bool:
    width = game_state["board"]["width"]
    height = game_state["board"]["height"]
    return 0 <= position[0] < width and 0 <= position[1] < height


def is_move_colliding(position: typing.Tuple[int, int], visited_positions: set) -> bool:
    return position in visited_positions

def evaluation_function(game_state:typing.Dict)->float:
    health = game_state["you"]["health"]
    my_head_x = game_state["you"]["body"][0]["x"]
    my_head_y = game_state["you"]["body"][0]["y"]

    food_distance = []
    if "food" in game_state:
         for food in game_state["food"]:
            food_distances.append(abs(food["x"] - my_head_x) + abs(food["y"] - my_head_y))
    if food_distance:
        min_food_distance = min(food_distance)
    else:
        min_food_distance = 0
    
    enemy_head_distances = []
    for snake in game_state["board"]["snakes"]:
        if snake["id"] != game_state["you"]["id"]:
            enemy_head_x = snake["body"][0]["x"]
            enemy_head_y = snake["body"][0]["y"]
            enemy_head_distances.append(abs(enemy_head_x - my_head_x) + abs(enemy_head_y - my_head_y))
    if enemy_head_distances:
        min_enemy_head_distance = min(enemy_head_distances)
    else:
        min_enemy_head_distance = 0
    
    # Calculate the overall evaluation score
    # You can adjust the weights for each factor according to your strategy
    evaluation_score = 0.5 * health - 0.2 * min_food_distance - 0.3 * min_enemy_head_distance

    return evaluation_score

class Node:
    def __init__(self, pos, parent=None):
        self.parent = parent
        self.pos = pos
        self.f = 0
        self.g = 0
        self.h = 0

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(position, game_state):
    neighbors = []
    directions = [('up', (0, -1)), ('down', (0, 1)), ('left', (-1, 0)), ('right', (1, 0))]
    for direction, (dx, dy) in directions:
        new_pos = (position[0] + dx, position[1] + dy)
        if is_move_safe(new_pos, game_state):
            neighbors.append((new_pos, direction))
    return neighbors

def is_move_safe(position, game_state):
    x, y = position
    if x < 0 or x >= game_state["board"]["width"] or y < 0 or y >= game_state["board"]["height"]:
        return False
    for snake in game_state["board"]["snakes"]:
        if position in [(segment["x"], segment["y"]) for segment in snake["body"]]:
            return False
    return True

def a_star_search(start, goal, game_state):
    open_set = {start}
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = min(open_set, key=lambda pos: f_score.get(pos, float('inf')))
        if current == goal:
            path = []
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]  # Return reversed path
        open_set.remove(current)
        for neighbor, direction in get_neighbors(current, game_state):
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                open_set.add(neighbor)
    return []

def find_closest_food(my_head, foods):
    closest_food = None
    min_distance = float('inf')
    for food in foods:
        food_pos = (food["x"], food["y"])
        distance = heuristic(my_head, food_pos)
        if distance < min_distance:
            closest_food = food_pos
            min_distance = distance
    return closest_food

def move(game_state: typing.Dict) -> typing.Dict:
    my_head = (game_state["you"]["body"][0]["x"], game_state["you"]["body"][0]["y"])
    foods = game_state["board"]["food"]
    if foods:
        goal = find_closest_food(my_head, foods)
        path = a_star_search(my_head, goal, game_state)
        if path:
            next_pos = path[0]
            direction = get_direction(my_head, next_pos)
            return {"move": direction}
    return {"move": "up"}  # Fallback move

def get_direction(from_pos, to_pos):
    dx = to_pos[0] - from_pos[0]
    dy = to_pos[1] - from_pos[1]
    if dx == 1:
        return "right"
    elif dx == -1:
        return "left"
    elif dy == 1:
        return "down"
    elif dy == -1:
        return "up"

if __name__ == "__main__":
    from server import run_server
    port = "8000"
    for i in range(len(sys.argv) - 1):
        if sys.argv[i] == '--port':
            port = sys.argv[i+1]

    run_server({"info": info, "start": start,
               "move": move, "end": end, "port": port})
