Barbell Plate Calculator

A Python desktop application that calculates the barbell plates needed to reach a target weight and displays the result using an interactive graphical barbell.

The project includes a modern PyQt6 implementation as well as an earlier Tkinter implementation, showing the progression of the application as I explored different Python GUI frameworks.

Features

Calculates the number of plate pairs required for a target barbell weight

Supports 45, 25, 10, 5, and 2.5 lb plates

Validates user input and prevents impossible plate combinations

Graphically displays plates on both sides of the barbell

Uses different plate sizes and colors for easy identification

Supports multiple calculator windows

Allows users to give each calculator window a custom name

Resizable graphical interface

Built With

Python

PyQt6

Tkinter

How It Works

The calculator assumes a standard 45 lb barbell.

After entering a target weight, the application:

Subtracts the weight of the bar.

Divides the remaining weight equally between both sides.

Determines the largest available plates that can be used.

Continues through the available plate sizes until the required weight is reached.

Displays both the calculated plate configuration and a graphical representation of the loaded barbell.

For example, entering 225 lb produces:

2 pairs of 45 lb plates
