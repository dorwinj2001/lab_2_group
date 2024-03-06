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
        print(f"MOVE {game_state['turn']
                      }: No safe moves detected! Moving down")
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
    for food in game_state["food"]:
        food_distances.append(abs(food["x"] - my_head_x)) + abs(food["y"])
    if food_distances:
         min_food_distance = min(food_distances)
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


if __name__ == "__main__":
    from server import run_server
    port = "8000"
    for i in range(len(sys.argv) - 1):
        if sys.argv[i] == '--port':
            port = sys.argv[i+1]

    run_server({"info": info, "start": start,
               "move": move, "end": end, "port": port})
