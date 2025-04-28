import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import seaborn as sns


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
