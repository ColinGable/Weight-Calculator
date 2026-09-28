import tkinter as tk
from tkinter import messagebox


BAR_WEIGHT = 45
PLATES = [45, 25, 10, 5, 2.5]


def calculate_plates(total_weight):
    """
    Calculate the number of plate PAIRS needed for a target barbell weight.
    Returns a dictionary like {45: 2, 25: 1, ...}.
    """
    if total_weight < BAR_WEIGHT:
        raise ValueError(f"Weight must be at least {BAR_WEIGHT} lb.")

    weight_to_load = total_weight - BAR_WEIGHT

    # Because plates must be loaded evenly on both sides
    if weight_to_load % 5 != 0:
        raise ValueError(
            "With 2.5 lb plates as the smallest plates, total weight must increase in 5 lb increments."
        )

    per_side = weight_to_load / 2
    result = {}

    for plate in PLATES:
        count = int(per_side // plate)
        result[plate] = count
        per_side -= count * plate

    if abs(per_side) > 1e-9:
        raise ValueError("That weight cannot be created with the available plates.")

    return result


class WeightPlateCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Competitive Weightlifting Plate Calculator")
        self.root.geometry("900x520")
        self.root.minsize(760, 460)

        title = tk.Label(
            root,
            text="Competitive Weightlifting Load Calculator",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=(15, 5))

        subtitle = tk.Label(
            root,
            text="Enter the total barbell weight, including the 45 lb bar.",
            font=("Arial", 10)
        )
        subtitle.pack(pady=(0, 10))

        input_frame = tk.Frame(root)
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Target Weight (lb):", font=("Arial", 11)).pack(side=tk.LEFT, padx=5)

        self.weight_entry = tk.Entry(input_frame, width=12, font=("Arial", 11))
        self.weight_entry.pack(side=tk.LEFT, padx=5)
        self.weight_entry.insert(0, "225")
        self.weight_entry.bind("<Return>", lambda event: self.update_display())

        tk.Button(
            input_frame,
            text="Calculate",
            command=self.update_display,
            font=("Arial", 10, "bold"),
            padx=14
        ).pack(side=tk.LEFT, padx=8)

        self.result_label = tk.Label(
            root,
            text="",
            font=("Arial", 11),
            justify=tk.LEFT
        )
        self.result_label.pack(pady=8)

        self.canvas = tk.Canvas(
            root,
            width=850,
            height=260,
            bg="white",
            highlightthickness=1,
            highlightbackground="gray"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=(5, 20))

        self.update_display()

    def update_display(self):
        try:
            total_weight = float(self.weight_entry.get())

            if total_weight.is_integer():
                total_weight = int(total_weight)

            plate_counts = calculate_plates(total_weight)

            plate_text = []
            for plate in PLATES:
                pairs = plate_counts[plate]
                if pairs:
                    label = int(plate) if float(plate).is_integer() else plate
                    plate_text.append(f"{pairs} pair{'s' if pairs != 1 else ''} of {label} lb")

            if plate_text:
                summary = ", ".join(plate_text)
            else:
                summary = "No plates needed — empty 45 lb bar."

            self.result_label.config(
                text=f"Total: {total_weight} lb\nLoad: {summary}"
            )
            self.draw_barbell(plate_counts)

        except ValueError as exc:
            messagebox.showerror("Invalid Weight", str(exc))

    def draw_barbell(self, plate_counts):
        self.canvas.delete("all")

        width = max(self.canvas.winfo_width(), 850)
        height = max(self.canvas.winfo_height(), 260)
        center_x = width / 2
        center_y = height / 2

        # Bar
        bar_left = 70
        bar_right = width - 70
        self.canvas.create_rectangle(
            bar_left,
            center_y - 6,
            bar_right,
            center_y + 6,
            fill="dim gray",
            outline="black"
        )

        # Center knurl area
        self.canvas.create_rectangle(
            center_x - 55,
            center_y - 8,
            center_x + 55,
            center_y + 8,
            fill="gray",
            outline="black"
        )

        # Sleeves
        sleeve_len = 180
        sleeve_start_left = center_x - 85
        sleeve_start_right = center_x + 85

        self.canvas.create_rectangle(
            sleeve_start_left - sleeve_len,
            center_y - 10,
            sleeve_start_left,
            center_y + 10,
            fill="silver",
            outline="black"
        )
        self.canvas.create_rectangle(
            sleeve_start_right,
            center_y - 10,
            sleeve_start_right + sleeve_len,
            center_y + 10,
            fill="silver",
            outline="black"
        )

        colors = {
            45: "royal blue",
            25: "goldenrod",
            10: "forest green",
            5: "orange",
            2.5: "red"
        }

        heights = {
            45: 150,
            25: 132,
            10: 112,
            5: 92,
            2.5: 74
        }

        x_left = sleeve_start_left - 12
        x_right = sleeve_start_right + 12

        plate_width = 18
        gap = 4

        # Draw largest plates nearest the inside on both sides
        for plate in PLATES:
            count = plate_counts[plate]
            for _ in range(count):
                h = heights[plate]
                color = colors[plate]

                # Left
                self.canvas.create_rectangle(
                    x_left - plate_width,
                    center_y - h / 2,
                    x_left,
                    center_y + h / 2,
                    fill=color,
                    outline="black",
                    width=2
                )
                self.canvas.create_text(
                    x_left - plate_width / 2,
                    center_y,
                    text=str(plate),
                    angle=90,
                    font=("Arial", 7, "bold")
                )
                x_left -= plate_width + gap

                # Right
                self.canvas.create_rectangle(
                    x_right,
                    center_y - h / 2,
                    x_right + plate_width,
                    center_y + h / 2,
                    fill=color,
                    outline="black",
                    width=2
                )
                self.canvas.create_text(
                    x_right + plate_width / 2,
                    center_y,
                    text=str(plate),
                    angle=90,
                    font=("Arial", 7, "bold")
                )
                x_right += plate_width + gap

        self.canvas.create_text(
            center_x,
            25,
            text="Barbell Visualization",
            font=("Arial", 13, "bold")
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = WeightPlateCalculator(root)
    root.mainloop()
