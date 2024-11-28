from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import messagebox

# Set initial drawing color and thickness
color = 'black'
thickness = 3

# Variables to store the previous mouse position
pastX, pastY = None, None

# Variables to indicate if the user is currently drawing
is_drawing = None

# Lists to store strokes for undo/redo functionality
strokes = []  # All drawn strokes
undone_strokes = []  # Strokes that were undone
deletestrokes=[]

def changecolor():
    """Function to change the drawing color using a color chooser dialog."""
    global color
    chosen_color = askcolor()[1]  # Open the color chooser dialog
    if chosen_color:
        color = chosen_color

def change_thickness(val):
    """Function to change the drawing thickness using the slider."""
    global thickness
    thickness = int(val)

def start_draw(event):
    """Event handler for when the user starts drawing."""
    global is_drawing, pastX, pastY
    is_drawing = True  # Set drawing flag to True
    pastX = event.x  # Get the starting x position
    pastY = event.y  # Get the starting y position
    strokes.append([])  # Start a new stroke (list of line segments)

def draw(event):
    """Event handler for drawing on the canvas when the mouse moves."""
    global is_drawing, pastX, pastY, color, thickness
    current_x, current_y = event.x, event.y  # Get the current mouse position
    if is_drawing:
        # Draw a line from the last position to the current position with the selected thickness
        line = canvasboard.create_line(pastX, pastY, current_x, current_y, fill=color, width=thickness)
        strokes[-1].append(line)  # Add the line to the current stroke
        print("inside draw",strokes)
        # Update past positions for the next line segment
        pastX = current_x
        pastY = current_y

def stop_draw(event):
    """Event handler for when the user stops drawing."""
    global is_drawing
    is_drawing = False  # Set drawing flag to False

def undo_last_action():
    """Function to undo the last stroke drawn."""
    global strokes, undone_strokes, deletestrokes
    if strokes:
        last_stroke = strokes.pop()  # Get the last stroke (list of line segments)
        print("inside undo function",last_stroke)
        for line in last_stroke:
            print("inside undo function 2",line)
            deletestrokes.append(line)
            canvasboard.delete(line)  # Delete each line in the last stroke
        undone_strokes.append(last_stroke)  # Add the undone stroke to the undone list

def redo_last_action():
    """Function to redo the last undone stroke."""
    global strokes, undone_strokes, deletestrokes
    if undone_strokes:
        redo_stroke = undone_strokes.pop()  # Get the last undone stroke
        for line in redo_stroke:
            # Redraw the lines that were undone
            reline = canvasboard.create_line(line[0], line[1], line[2], line[3], fill=color, width=thickness)
            canvasboard.itemconfig(reline, state='normal')
        strokes.append(redo_stroke)  # Add the stroke back to the strokes list

def clear_canvas():
    """Function to confirm before clearing the canvas."""
    response = messagebox.askyesno("Clear Canvas", "Are you sure you want to clear the canvas?")
    if response:
        canvasboard.delete('all')
        strokes.clear()  # Clear the stroke history
        undone_strokes.clear()  # Clear the undone strokes

# Initialize the main application window
dashboard = Tk()
dashboard.title("Drawing Application")

# Create a canvas widget for drawing
canvasboard = Canvas(dashboard, bg='white')
canvasboard.pack(fill="both", expand=True)

# Bind mouse events to canvas for drawing actions
canvasboard.bind('<Button-1>', start_draw)  # Start drawing on left mouse button click
canvasboard.bind('<B1-Motion>', draw)  # Draw while moving the mouse with the left button pressed
canvasboard.bind('<ButtonRelease-1>', stop_draw)  # Stop drawing when the left mouse button is released

# Create a frame for holding additional widgets
pain = Frame(dashboard)
pain.pack(fill='x')

# Create buttons for clearing the canvas, changing color, undoing, and redoing
clear_button = Button(pain, text='Clear', command=clear_canvas)
clear_button.pack(side='left')
colbut = Button(pain, text='Change Color', command=changecolor)
colbut.pack(side='right')
undo_button = Button(pain, text='Undo', command=undo_last_action)
undo_button.pack(side='left')
redo_button = Button(pain, text='Redo', command=redo_last_action)
redo_button.pack(side='left')

# Add a slider to adjust the line thickness
thickness_slider = Scale(pain, from_=1, to=10, orient=HORIZONTAL, label="Line Thickness")
thickness_slider.set(thickness)  # Set initial thickness value
thickness_slider.pack(side='left')

# Update the thickness dynamically based on the slider value
thickness_slider.bind("<Motion>", lambda event: change_thickness(thickness_slider.get()))

# Start the Tkinter event loop
dashboard.mainloop()

