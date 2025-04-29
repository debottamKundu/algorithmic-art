import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import seaborn as sns
import wesanderson
import numpy as np


def get_colors_from_heatmap(cmap_name="viridis", n_colors=5):
    """Get n colors from a heatmap.

    Args:
        cmap_name (str, optional): Seaborn or matplotlib colormap name. Defaults to "viridis".
        n_colors (int, optional): Number of colors. Defaults to 5.

    Returns:
        np.array: Array of n colors from specified heatmap
    """
    try:
        # Get the Matplotlib colormap object by name (Seaborn uses these)
        cmap = plt.get_cmap(cmap_name)
    except ValueError:
        print(f"Error: Colormap '{cmap_name}' not found.")
        return None

    color_indices = [
        i / (n_colors - 1) if n_colors > 1 else 0.5 for i in range(n_colors)
    ]

    # Sample the colormap at these indices to get RGBA values
    rgba_colors = cmap(color_indices)

    # Convert RGBA to hex codes
    hex_colors = [mcolors.to_hex(rgba) for rgba in rgba_colors]

    return hex_colors


def get_movie_colors(custom=None, movie_name="Darjeeling", noise_param=0.1, n_colors=5):
    """Get colors defined in a custom list or from a wes anderson movie

    Args:
        custom (np.array, optional): Array of Hex colors. Defaults to None.
        movie_name (str, optional): Part/Complete Wes Anderson movie name, all supported by the wesanderson package. Defaults to "Darjeeling".
        noise_param (float, optional): Amount of noise to add to generate more colors. Defaults to 0.1.
        n_colors (int, optional): Total number of colors. Defaults to 5.

    Returns:
        np.array: List of colors
    """
    if custom is not None:
        colors = custom
    else:
        colors = wesanderson.film_palette(movie_name)
    if len(colors) == n_colors:
        return colors
    else:
        total_colors = len(colors)
        rgb_colors = np.asarray([mcolors.to_rgb(color) for color in colors])

        # tile
        rgb_colors_reps = np.tile(rgb_colors, (n_colors // total_colors + 1, 1))[
            :n_colors
        ]

        noise = np.random.normal(0, noise_param, size=(n_colors,))
        choose_columns = np.random.randint(0, 3, n_colors)

        # add noise
        for i in range(n_colors):
            candidate_color = rgb_colors_reps[i, choose_columns[i]] + noise[i]
            if candidate_color < 0 or candidate_color > 1:
                noise[i] = -noise[i]
            rgb_colors_reps[i, choose_columns[i]] += noise[i]

        # convert to hex
        hex_colors = [mcolors.to_hex(rgb) for rgb in rgb_colors_reps]

        return hex_colors


def draw(df):
    """Draw and show the algorithmically generated image

    Args:
        df (pandas.DataFrame): Dataframe containing the details for all the rectangles
    """

    fig, ax = plt.subplots(1)

    for index, row in df.iterrows():
        left = row["Left"]
        bottom = row["Bottom"]
        width = row["Right"] - left
        height = row["Top"] - bottom  # Note: top is usually greater than bottom

        color = row["Color"]

        # Create a Rectangle patch
        rect = patches.Rectangle(
            (left, bottom),
            width,
            height,
            linewidth=1,
            edgecolor="black",
            facecolor=color,
        )

        # Add the patch to the axes
        ax.add_patch(rect)

    # Set the limits of the plot to encompass all rectangles
    all_left = df["Left"].min()
    all_right = df["Right"].max()
    all_bottom = df["Bottom"].min()
    all_top = df["Top"].max()

    ax.set_xlim(all_left - 1, all_right + 1)
    ax.set_ylim(all_bottom - 1, all_top + 1)

    plt.axis("off")
    ax.set_aspect("equal", adjustable="box")

    # Show the plot
    plt.show()


def color_limits(color, noise):
    """Check if adding noise exceeds rgb limits and truncate

    Args:
        color (np.array): 1x3 array of rgb values
        noise (np.array): 1x3 array of noise values

    Returns:
        np.array: 1x3 array of noise added rgb values
    """

    noisy_rgb = color + noise

    lower_bound_violation = noisy_rgb < 0
    upper_bound_violation = noisy_rgb > 1

    if not np.any(lower_bound_violation) and not np.any(upper_bound_violation):
        return tuple(np.clip(noisy_rgb, 0, 1))  # Clip just to be safe

    # Flip the noise for the components that are out of bounds
    noise[lower_bound_violation] *= -1
    noise[upper_bound_violation] *= -1

    # Recalculate with flipped noise
    noisy_rgb = color + noise
    # print(noisy_rgb)

    return noisy_rgb


def draw_mosaic(df):
    """

    Draw and show the algorithmically generated image
    Subdivide each rectangle into unit squares and paint them based on the base color,
    with added noise.

    Args:
        df (pd.dataframe): Dataframe with all the details
    """

    df["RGB"] = np.asarray(df["Color"].apply(lambda x: mcolors.to_rgb(x)))

    # now pick each rectangle and subdivide
    fig, ax = plt.subplots(1)

    for index, row in df.iterrows():

        left = row["Left"]
        bottom = row["Bottom"]
        width = row["Right"] - left
        height = row["Top"] - bottom  # Note: top is usually greater than bottom
        base_color = row["RGB"]

        # Create a Rectangle patch

        # one unit patches
        for x in range(int(left), int(row["Right"])):
            for y in range(int(bottom), int(row["Top"])):
                noise = np.random.normal(0, 0.1, 3)
                square_color = color_limits(base_color, noise)
                square_color = mcolors.to_hex(square_color)
                square = patches.Rectangle((x, y), 1, 1, facecolor=square_color)
                ax.add_patch(square)

    all_left = df["Left"].min()
    all_right = df["Right"].max()
    all_bottom = df["Bottom"].min()
    all_top = df["Top"].max()

    ax.set_xlim(all_left - 1, all_right + 1)
    ax.set_ylim(all_bottom - 1, all_top + 1)

    plt.axis("off")
    ax.set_aspect("equal", adjustable="box")

    # Show the plot
    plt.show()
