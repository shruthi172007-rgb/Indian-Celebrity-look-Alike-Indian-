from deepface import DeepFace
import os
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import threading

#   BASIC WINDOW SETUP

app = Tk()
app.title("Celebrity Look-Alike Finder")
app.geometry("1000x650")
app.config(bg="white")

# This will store the path of the image selected by the user
user_image_path = None

#   FUNCTION: Display any image in the GUI

def display_image(path, label_widget):
    img = Image.open(path)
    img = img.resize((300, 300))
    img = ImageTk.PhotoImage(img)
    label_widget.config(image=img)
    label_widget.image = img  # keep reference



#   FUNCTION: Let the user pick an image from their computer

def choose_image():
    global user_image_path
    path = filedialog.askopenfilename(
        title="Select Your Photo",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )

    if path:
        user_image_path = path
        display_image(path, user_image_label)
        result_label.config(text="")
        celeb_image_label.config(image="")



#   FUNCTION: Find celebrity look-alike

def find_lookalike():

    if user_image_path is None:
        result_label.config(text="Please select your photo first!")
        return

    celebrity_folder ="celebrity_dataset"
    best_match_path = None
    best_distance = 999  # Smaller = better

    # Compare user image with every celebrity photo
    for filename in os.listdir(celebrity_folder):
        celeb_path = os.path.join(celebrity_folder, filename)

        try:
            result = DeepFace.verify(
                user_image_path,
                celeb_path,
                model_name="VGG-Face"
            )

            distance = result["distance"]

            if distance < best_distance:
                best_distance = distance
                best_match_path = celeb_path

        except Exception:
            continue

    # Show result
    if best_match_path:
        celeb_name = os.path.splitext(os.path.basename(best_match_path))[0].replace("_", " ")
        display_image(best_match_path, celeb_image_label)

        result_label.config(
            text=f"Match Found: {celeb_name}\nSimilarity Score: {round(1 - best_distance, 3)}"
        )
    else:
        result_label.config(text="No match found.")



#   Run matching in a thread so GUI doesn't freeze
def start_matching():
    threading.Thread(target=find_lookalike).start()

#   GUI LAYOUT

left_frame = Frame(app, bg="white")
left_frame.pack(side=LEFT, padx=25)

right_frame = Frame(app, bg="white")
right_frame.pack(side=RIGHT, padx=25)

# User image area
Label(left_frame, text="Your Photo", font=("Arial", 14), bg="white").pack()
user_image_label = Label(left_frame, bg="white")
user_image_label.pack()

# Celebrity result area
Label(right_frame, text="Matched Celebrity", font=("Arial", 14), bg="white").pack()
celeb_image_label = Label(right_frame, bg="white")
celeb_image_label.pack()

# Result text
result_label = Label(app, text="", font=("Arial", 16, "bold"), bg="white", fg="darkblue")
result_label.pack(pady=20)

# Buttons
Button(app, text="Select Your Photo",
       font=("Arial", 16), bg="#4CAF50", fg="white",
       command=choose_image).pack(pady=15)

Button(app, text="Find My Look-Alike",
       font=("Arial", 16), bg="black", fg="white",
       command=start_matching).pack(pady=10)

app.mainloop()
