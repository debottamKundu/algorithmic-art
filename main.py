from rectangles import generate_art
from src.draw import draw, get_colors_from_heatmap


def main():
    print("Hello from algorithmic-art!")
    df = generate_art(1200, 800, 30)
    df["Color"] = get_colors_from_heatmap(n_colors=len(df))
    draw(df)


if __name__ == "__main__":
    main()
