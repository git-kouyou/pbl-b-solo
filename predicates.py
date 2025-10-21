def foods_around(head, foods):
    food_directions = []
    if (head["x"] - 1, head["y"]) in foods:
        food_directions.append("left")
    if (head["x"] + 1, head["y"]) in foods:
        food_directions.append("right")
    if (head["x"], head["y"] + 1) in foods:
        food_directions.append("up")
    if (head["x"], head["y"] - 1) in foods:
        food_directions.append("down")
    return food_directions

def unsafes_around(head, unsafes):
    unsafe_directions = []
    if (head["x"] - 1, head["y"]) in unsafes:
        unsafe_directions.append("left")
    if (head["x"] + 1, head["y"]) in unsafes:
        unsafe_directions.append("right")
    if (head["x"], head["y"] + 1) in unsafes:
        unsafe_directions.append("up")
    if (head["x"], head["y"] - 1) in unsafes:
        unsafe_directions.append("down")
    return unsafe_directions

def neck_direction(head, neck):
    if neck[0] < head[0]:
        return "left"
    elif neck[0] > head[0]:
        return "right"
    elif neck[1] < head[1]:
        return "down"
    elif neck[1] > head[1]:
        return "up"
    return None