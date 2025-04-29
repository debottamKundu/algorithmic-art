import pandas as pd
import numpy as np



def initialize_dataframe(canvas_width, canvas_height):

    df = pd.DataFrame(columns=["Left", "Right", "Top", "Bottom", "Area", "Color"])
    df.loc[0] = [0, canvas_width, canvas_height, 0, canvas_width * canvas_height, 0]
    return df


def choosebreak(a, b):
    fraction = np.random.uniform(0, 1)
    return a + np.round(fraction * (b - a))


def compute_area(df, location):
    return (df.loc[location, "Right"] - df.loc[location, "Left"]) * (
        df.loc[location, "Top"] - df.loc[location, "Bottom"]
    )


def split_horizontally(df, row_index):

    # row_index is chosen randomly by the passing function
    # split up the rectange at row_index by width

    break_point = choosebreak(df.loc[row_index, "Left"], df.loc[row_index, "Right"])

    df.loc[len(df)] = [
        break_point,
        df.loc[row_index, "Right"],
        df.loc[row_index, "Top"],
        df.loc[row_index, "Bottom"],
        0,
        0,
    ]

    df.loc[row_index, "Right"] = break_point
    df.loc[row_index, "Area"] = compute_area(df, row_index)
    df.loc[len(df) - 1, "Area"] = compute_area(df, len(df) - 1)

    return df


def split_vertically(df, row_index):

    break_point = choosebreak(df.loc[row_index, "Top"], df.loc[row_index, "Bottom"])

    df.loc[len(df)] = [
        df.loc[row_index, "Left"],
        df.loc[row_index, "Right"],
        df.loc[row_index, "Top"],
        break_point,
        0,
        0,
    ]

    df.loc[row_index, "Top"] = break_point
    df.loc[row_index, "Area"] = compute_area(df, row_index)
    df.loc[len(df) - 1, "Area"] = compute_area(df, len(df) - 1)

    return df


def generate_art(canvas_width, canvas_height, iterations):
    df = initialize_dataframe(canvas_width, canvas_height)

    for itx in range(iterations):
        # choose row index based on area
        p_areas = df["Area"] / df["Area"].sum()
        row_index = np.random.choice(df.index, p=p_areas)
        split_choice = np.random.choice([0, 1])
        if split_choice == 0:
            df = split_horizontally(df, row_index)
        else:
            df = split_vertically(df, row_index)
    return df

