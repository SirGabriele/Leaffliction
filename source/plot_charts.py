from matplotlib import pyplot as plt


def plot_charts(root_directory: str, labels: list[str], counts: list[int]):
    # Uses the tab10 colour map to assign a colour to all labels
    colour_map = plt.cm.tab10
    colours = [colour_map(i % colour_map.N) for i in range(len(counts))]

    # Creates the whole figure with custom size
    plt.figure(num="Data set", figsize=(10, 6))

    # Pie chart
    plt.subplot(1, 2, 1)
    plt.pie(counts, autopct="%1.1f%%", colors=colours)
    plt.title(f"{root_directory} class distribution", loc="left", y=0.95)

    # Bar chart
    plt.subplot(1, 2, 2)
    plt.gca().set_facecolor('lightgray')
    plt.grid(axis='y', color='white', linewidth=1, zorder=1)
    plt.bar(labels, counts, color=colours, zorder=2)
    plt.xticks(rotation=45, ha="right")

    # Fixes overlapping labels between all charts and edges
    plt.tight_layout()
    plt.show()
