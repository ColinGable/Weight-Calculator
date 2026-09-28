import sys

from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QFont
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QInputDialog,
)


BAR_WEIGHT = 45
PLATES = [45, 25, 10, 5, 2.5]

# Keeps references to every open calculator window
open_windows = []


def calculate_plates(total_weight):
    """
    Calculate the number of plate PAIRS needed for a target barbell weight.
    """

    if total_weight < BAR_WEIGHT:
        raise ValueError(
            f"Weight must be at least {BAR_WEIGHT} lb."
        )

    weight_to_load = total_weight - BAR_WEIGHT

    # Plates must be evenly loaded on both sides.
    # With 2.5 lb plates as the smallest plates,
    # the total weight changes in 5 lb increments.
    if weight_to_load % 5 != 0:
        raise ValueError(
            "With 2.5 lb plates as the smallest plates, "
            "total weight must increase in 5 lb increments."
        )

    per_side = weight_to_load / 2

    result = {}

    for plate in PLATES:

        count = int(per_side // plate)

        result[plate] = count

        per_side -= count * plate

    if abs(per_side) > 1e-9:
        raise ValueError(
            "That weight cannot be created with the available plates."
        )

    return result


class BarbellCanvas(QWidget):

    def __init__(self):

        super().__init__()

        self.plate_counts = {
            plate: 0 for plate in PLATES
        }

        # Canvas can resize with the window
        self.setMinimumSize(650, 300)

    def set_plate_counts(self, plate_counts):

        self.plate_counts = plate_counts

        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        # -------------------------
        # CANVAS
        # -------------------------

        width = self.width()
        height = self.height()

        center_x = width / 2
        center_y = height / 2 + 20

        painter.fillRect(
            self.rect(),
            QColor("white")
        )

        # -------------------------
        # TITLE
        # -------------------------

        painter.setPen(
            QPen(QColor("black"))
        )

        painter.setFont(
            QFont(
                "Arial",
                13,
                QFont.Weight.Bold
            )
        )

        painter.drawText(
            QRectF(
                0,
                10,
                width,
                35
            ),
            Qt.AlignmentFlag.AlignCenter,
            "Barbell Visualization"
        )

        # -------------------------
        # FIXED-SIZE BAR
        # -------------------------

        BAR_LENGTH = 600
        BAR_HEIGHT = 16

        bar_left = center_x - BAR_LENGTH / 2

        bar_top = center_y - BAR_HEIGHT / 2

        painter.setPen(
            QPen(
                QColor("black"),
                1
            )
        )

        painter.setBrush(
            QBrush(
                QColor("silver")
            )
        )

        # One continuous solid bar
        painter.drawRoundedRect(
            QRectF(
                bar_left,
                bar_top,
                BAR_LENGTH,
                BAR_HEIGHT
            ),
            4,
            4
        )

        # -------------------------
        # PLATE COLORS
        # -------------------------

        color_map = {

            45: QColor("#2f66d0"),  # Blue

            25: QColor("#2e8b57"),  # Green

            10: QColor("#d8a31a"),  # Yellow

            5: QColor("#ef8b2c"),   # Orange

            2.5: QColor("#d94a4a"), # Red
        }

        # -------------------------
        # PLATE HEIGHTS
        # -------------------------

        height_map = {

            45: 175,

            25: 150,

            10: 126,

            5: 104,

            2.5: 82,
        }

        PLATE_WIDTH = 20

        GAP = 5

        # Plates start near the center of the bar
        INNER_OFFSET = 105

        left_x = center_x - INNER_OFFSET

        right_x = center_x + INNER_OFFSET

        painter.setFont(
            QFont(
                "Arial",
                7,
                QFont.Weight.Bold
            )
        )

        # -------------------------
        # DRAW PLATES
        # -------------------------

        for plate in PLATES:

            count = self.plate_counts.get(
                plate,
                0
            )

            for _ in range(count):

                plate_height = height_map[plate]

                top = (
                    center_y -
                    plate_height / 2
                )

                painter.setPen(
                    QPen(
                        QColor("black"),
                        2
                    )
                )

                painter.setBrush(
                    QBrush(
                        color_map[plate]
                    )
                )

                # -------------------------
                # LEFT PLATE
                # -------------------------

                left_rect = QRectF(
                    left_x - PLATE_WIDTH,
                    top,
                    PLATE_WIDTH,
                    plate_height
                )

                painter.drawRoundedRect(
                    left_rect,
                    3,
                    3
                )

                # -------------------------
                # RIGHT PLATE
                # -------------------------

                right_rect = QRectF(
                    right_x,
                    top,
                    PLATE_WIDTH,
                    plate_height
                )

                painter.drawRoundedRect(
                    right_rect,
                    3,
                    3
                )

                # -------------------------
                # PLATE LABEL
                # -------------------------

                painter.setPen(
                    QPen(
                        QColor("black")
                    )
                )

                if float(plate).is_integer():

                    label = str(
                        int(plate)
                    )

                else:

                    label = str(
                        plate
                    )

                # Left plate label
                painter.save()

                painter.translate(
                    left_rect.center()
                )

                painter.rotate(-90)

                painter.drawText(
                    QRectF(
                        -25,
                        -8,
                        50,
                        16
                    ),
                    Qt.AlignmentFlag.AlignCenter,
                    label
                )

                painter.restore()

                # Right plate label
                painter.save()

                painter.translate(
                    right_rect.center()
                )

                painter.rotate(90)

                painter.drawText(
                    QRectF(
                        -25,
                        -8,
                        50,
                        16
                    ),
                    Qt.AlignmentFlag.AlignCenter,
                    label
                )

                painter.restore()

                # Move outward for next plate
                left_x -= (
                    PLATE_WIDTH +
                    GAP
                )

                right_x += (
                    PLATE_WIDTH +
                    GAP
                )


class WeightliftingCalculator(QWidget):

    def __init__(self, window_name):

        super().__init__()

        self.window_name = window_name

        # -------------------------
        # WINDOW
        # -------------------------

        self.setWindowTitle(
            f"{window_name} - Weight Calculator"
        )

        # Window can now be resized
        self.resize(
            750,
            550
        )

        self.setMinimumSize(
            680,
            500
        )

        main_layout = QVBoxLayout(
            self
        )

        # -------------------------
        # TITLE
        # -------------------------

        title = QLabel(
            window_name
        )

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title.setFont(
            QFont(
                "Arial",
                22,
                QFont.Weight.Bold
            )
        )



        instructions = QLabel(
            "Enter the total barbell weight, including the 45 lb bar."
        )

        instructions.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        main_layout.addWidget(
            instructions
        )

        # -------------------------
        # INPUT AREA
        # -------------------------

        input_layout = QHBoxLayout()

        input_layout.addStretch()

        input_layout.addWidget(
            QLabel(
                "Target Weight (lb):"
            )
        )

        self.weight_input = QLineEdit(
            "225"
        )

        self.weight_input.setMaximumWidth(
            140
        )

        self.weight_input.returnPressed.connect(
            self.update_barbell
        )

        input_layout.addWidget(
            self.weight_input
        )

        # -------------------------
        # CALCULATE BUTTON
        # -------------------------

        calculate_button = QPushButton(
            "Calculate"
        )

        calculate_button.clicked.connect(
            self.update_barbell
        )

        input_layout.addWidget(
            calculate_button
        )

        # -------------------------
        # NEW WINDOW BUTTON
        # -------------------------

        new_window_button = QPushButton(
            "New Window"
        )

        new_window_button.clicked.connect(
            self.create_new_window
        )

        input_layout.addWidget(
            new_window_button
        )

        input_layout.addStretch()

        main_layout.addLayout(
            input_layout
        )

        # -------------------------
        # RESULT
        # -------------------------

        self.result_label = QLabel(
            ""
        )

        self.result_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.result_label.setWordWrap(
            True
        )

        self.result_label.setFont(
            QFont(
                "Arial",
                11
            )
        )

        main_layout.addWidget(
            self.result_label
        )

        # -------------------------
        # BARBELL DISPLAY
        # -------------------------

        self.barbell_canvas = BarbellCanvas()

        main_layout.addWidget(
            self.barbell_canvas,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.update_barbell()

    def update_barbell(self):

        try:

            total_weight = float(
                self.weight_input.text()
            )

            if total_weight.is_integer():

                total_weight = int(
                    total_weight
                )

            plate_counts = calculate_plates(
                total_weight
            )

            parts = []

            for plate in PLATES:

                pairs = plate_counts[plate]

                if pairs:

                    if float(plate).is_integer():

                        plate_label = int(
                            plate
                        )

                    else:

                        plate_label = plate

                    parts.append(
                        f"{pairs} pair"
                        f"{'s' if pairs != 1 else ''} "
                        f"of {plate_label} lb"
                    )

            if parts:

                summary = ", ".join(
                    parts
                )

            else:

                summary = (
                    "No plates needed — "
                    "empty 45 lb bar."
                )

            self.result_label.setText(
                f"<b>Total:</b> "
                f"{total_weight} lb"
                f"<br>"
                f"<b>Load:</b> "
                f"{summary}"
            )

            self.barbell_canvas.set_plate_counts(
                plate_counts
            )

        except ValueError as exc:

            QMessageBox.warning(
                self,
                "Invalid Weight",
                str(exc)
            )

    def create_new_window(self):

        name, ok = QInputDialog.getText(
            self,
            "New Weight Calculator",
            "Enter a name for this window:"
        )

        if not ok:
            return

        name = name.strip()

        if name == "":
            name = "Weight Calculator"

        new_window = WeightliftingCalculator(
            name
        )

        open_windows.append(
            new_window
        )

        new_window.show()

    def closeEvent(self, event):

        if self in open_windows:

            open_windows.remove(
                self
            )

        event.accept()


def get_starting_name():

    name, ok = QInputDialog.getText(
        None,
        "Weight Calculator",
        "Enter a name for this window:"
    )

    if not ok:

        return None

    name = name.strip()

    if name == "":

        name = "Weight Calculator"

    return name


if __name__ == "__main__":

    app = QApplication(
        sys.argv
    )

    # Ask for the first window's name
    starting_name = get_starting_name()

    if starting_name is None:

        sys.exit()

    # Create the first calculator
    window = WeightliftingCalculator(
        starting_name
    )

    open_windows.append(
        window
    )

    window.show()

    sys.exit(
        app.exec()
    )