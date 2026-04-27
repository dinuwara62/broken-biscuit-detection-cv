# Broken-Biscuit-Detection-CV

Project Title
Broken Biscuit Detection using Classical Image Processing Techniques

Problem Description
In food factories, broken biscuits are a common issue that can lead to waste and unhappy customers. Checking every single biscuit by hand is slow and difficult. This project solves that problem by using a computer vision system that can automatically look at a photo of biscuits and tell which ones are perfect and which ones are broken. It also identifies if the biscuit is a square cracker or a round cookie.

Tools and Libraries Used
The project is built with Python. I used the OpenCV library for all the image processing tasks, like picking out colors and measuring shapes. I also used NumPy to help the computer handle the math and the image data behind the scenes.

Image Processing Methods Used
Instead of just looking at outlines, I used a color-based approach to make the system more reliable:

Color Isolation: I converted the images to HSV color space. This allowed me to create a specific mask that only looks for the golden-brown color of the biscuits, which helps ignore shadows and the white paper background.

Cleaning the Shapes: I used morphological opening and closing. This basically acts like a digital brush that smooths out the edges and fills in the small toasted holes on the biscuit surface so the computer sees a solid object.

Shape Math: Circularity: I used a formula to see how round the object is.

Vertex Counting: The code counts the corners of the shape to tell a square from a circle.

Aspect Ratio: This checks if the width and height of a square biscuit are balanced. If it is too thin, the system knows it is a broken piece.

Instructions to Run the Code
Make sure you have Python installed on your computer.

Install the required tools by typing pip install opencv-python numpy in your terminal.

Place your biscuit photos in a folder named inputs.

Run the script. The system will automatically create an output_images folder where it saves the final results with labels.

Example Output Images
The final images show green boxes and labels for intact biscuits and red boxes for broken ones. For example, a full round biscuit will be labeled as Intact Biscuit (Circle), while a snapped cracker will show up as Broken Biscuit (Square).

(Note: You can see the labeled results in my result_images in this repository.)
<img width="169" height="87" alt="image" src="https://github.com/user-attachments/assets/f4117a55-f07b-42d6-8fa6-b690a3831c08" />

