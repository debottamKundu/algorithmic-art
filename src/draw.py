import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import seaborn as sns
import wesanderson
import numpy as np


def get_colors_from_heatmap(cmap_name="viridis", n_colors=5):
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


def get_wes_anderson_colors(movie_name="Darjeeling", noise_param=0.1, n_colors=5):
    # get palatte
    # check if len <= n_colors, return
    # otherwise convert to rgb, add noise
    # convert to hex and return

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


# nextup: mosaic
# get each rectangle, divide into 1 pixel cubes, then convert hex into rgb, add noise, and then plot


def draw_mosaic(df):

    df["RGB"] = df["Color"].apply(lambda x: mcolors.to_rgb(x))
