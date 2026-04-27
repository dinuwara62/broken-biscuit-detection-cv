# Broken-Biscuit-Detection-CV
How the System Works
The logic follows a step-by-step process to turn a raw photo into a clear result:

Color Recognition: Instead of just looking at black and white images, the code converts the photo into HSV color space. This makes it much easier to pick out the golden-brown color of the biscuits while ignoring the shadows and the white paper background.

Creating a Clean Mask: By setting a specific color range, the system creates a mask where the biscuits are white and the background is black.

Cleaning Up Noise: To make sure the system doesn't get confused by small crumbs or the little holes on the cracker's surface, it uses morphological operations like Opening and Closing. This "heals" the shape so the computer sees a solid object.

Shape Analysis:

Circularity: The code calculates how close the shape is to a perfect circle.

Vertex Counting: It counts the "corners" of the shape. For example, an intact square should have 4 corners, while a circle has many more approximated points.

Aspect Ratio: This checks if the width and height are balanced, which helps identify if a square biscuit has been snapped into a thin rectangle.

Libraries Used
The project is written in Python and relies on two main tools:

OpenCV: Used for all the heavy lifting like color filtering, finding shapes, and drawing the labels.

NumPy: Used to handle the image data and math behind the shape detection.
