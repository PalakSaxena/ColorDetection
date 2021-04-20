"""
     TASK 2 : COLOR  IDENTIFICATION IN IMAGES completed by PALAK SAXENA
"""

import cv2
import pandas as pd

# Reading the Image
img_path = 'shutterstock.jpg'
img = cv2.imread(img_path)

# Declaring global variables
clicked = False
r = g = b = x_pos = y_pos = 0

# Reading the csv file with pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv("ColorsDetails.csv", names=index, header=None)


# Function to calculate minimum distance from all colors and get the most matching color
def get_color_name(R, G, B):
    minimum = 1000                # This is the threshold value
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname


# Function to get (x,y) coordinates of mouse double click
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, x_pos, y_pos, clicked
        clicked = True
        x_pos = x
        y_pos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


# Setting a name for the window which will be used in setMouseCallback method as a parameter
cv2.namedWindow('MyFrame')

''' SetMouseCallback method is executed whenever a mouse event takes place.
    This gives us the coordinates(x,y) for every mouse event.
    First parameter passed is the name of the window and the second parameter is the function to be called. 
'''
cv2.setMouseCallback('MyFrame', draw_function)

while True:
    cv2.imshow("MyFrame", img)
    if clicked:

        # cv2.rectangle(image name, (start point), (end point), (color), thickness)
        # Thickness : -1 fills the entire rectangle and any other number will give a hollow rectangle with borders only
        cv2.rectangle(img, (20, 20), (700, 60), (b, g, r), -1)

        # Creating text string to display Color name and RGB values
        text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        # cv2.putText(image name, (start point), font(0-7), font scale, color, thickness, Line Type)
        cv2.putText(img, text, (50, 50), 3, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For light colors we will display the text in black color. Otherwise we have used white.
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 3, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False

    # break the loop when user clicks esc key
    ''' When using waitKey(0) in the while loop,
        the debugger never crosses this statement and does not refresh the frame and hence the frame output seems stable
        Hence, we are not using waitkey(0)
    '''
    if cv2.waitKey(10) & 0xFF == 27:
        break

cv2.destroyAllWindows()
