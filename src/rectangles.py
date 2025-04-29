import pandas as pd
import numpy as np


def initialize_dataframe(canvas_width, canvas_height):
    """Initialize the dataframe with one big rectangle

    Args:
        canvas_width (int): Canvas width
        canvas_height (int): Canvas height

    Returns:
        pandas.DataFrame: Dataframe with one big rectangle
    """

    df = pd.DataFrame(columns=["Left", "Right", "Top", "Bottom", "Area", "Color"])
    df.loc[0] = [0, canvas_width, canvas_height, 0, canvas_width * canvas_height, 0]
    return df


def choosebreak(a, b):
    """choose  a point to split the rectangle

    Args:
        a (int): point for left or top
        b (int): point for right or bottom

    Returns:
        int: point to break
    """
    fraction = np.random.uniform(0, 1)
    return a + np.round(fraction * (b - a))


def compute_area(df, location):
    """computes the area of the rectangle

    Args:
        df (pd.DataFrame): pandas dataframe
        location (int): row index

    Returns:
        df: pd.DataFrame with updated area
    """
    return (df.loc[location, "Right"] - df.loc[location, "Left"]) * (
        df.loc[location, "Top"] - df.loc[location, "Bottom"]
    )


def split_horizontally(df, row_index):
    """split the rectangle horizontally

    Args:
        df (pd.DataFrame): pandas dataframe with rectangles
        row_index (int): row to split

    Returns:
        pd.DataFrame: dataframe with new rectangle added
    """

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
    """split the rectangle vertically

    Args:
        df (pd.DataFrame): pandas dataframe with rectangles
        row_index (int): row to split

    Returns:
        pd.DataFrame: dataframe with new rectangle added
    """

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
    """Generates the main dataframe that stores everything

    Args:
        canvas_width (int): width of the canvas
        canvas_height (int): height of the canvas
        iterations (int): total number of splits to make

    Returns:
        pd.DataFrame: Dataframe with rectangles, add color and paint
    """
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
