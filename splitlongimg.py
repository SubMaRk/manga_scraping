import os
import cv2
import sys
import numpy as np

# Display menu for select support manga website
def display_menu():
    print("Please select a manga folder to clean failed folders.")
    print("[ 1 ] ThaiManga")
    print("[ 2 ] Flash-Manga")
    print("[ 3 ] Manga168")
    print("[ 4 ] TamaManga")
    print("[ 5 ] สดใสเมะ")
    print("[ 6 ] Ped-Manga")
    print("[ 7 ] SING-MANGA")
    print("[ 8 ] MangaKimi")
    print("[ 9 ] Me-Manga")
    print("[ 10 ] Reapertrans")
    print("[ 11 ] Dragon-Manga")
    print("[ 12 ] moodtoon")
    print("[ 13 ] ToomTam-Manga")
    print("[ 14 ] Miku-manga")
    print("[ 15 ] Asurahunter")
    print("[ 16 ] 108-Manga")
    print("[ 17 ] Joji-Manga")
    print("[ 18 ] Spy-manga")
    print("[ 19 ] Murim-Manga")
    print("[ 20 ] Kumomanga")
    print("[ 21 ] Mangastep")
    print("[ 22 ] Jaymanga")
    print("[ 23 ] Hippomanga")
    print("[ 24 ] PopsManga")
    print("[ 25 ] Tanuki-Manga")
    print("[ 26 ] Inu-Manga")
    print("[ 27 ] Lami-Manga")
    print("[ 28 ] Weimanga")
    print("[  ] Exit")

# Get choice from user
def get_user_choice():
    while True:
        try:
            choice = int(input("Enter your choice (1-28): "))
            if 1 <= choice <= 28:
                return choice
            else:
                print("Invalid choice. Please enter number in range 1 to 28")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Get website and setting from choice
def set_website_settings(choice):
    global site_folder
    if choice == 1:
        site_folder = "ThaiManga"
    elif choice == 2:
        site_folder = "Flash-Manga"
    elif choice == 3:
        site_folder = "Manga168"
    elif choice == 4:
        site_folder = "TamaManga"
    elif choice == 5:
        site_folder = "สดใสเมะ"
    elif choice == 6:
        site_folder = "Ped-Manga"
    elif choice == 7:
        site_folder = "SING-MANGA"
    elif choice == 8:
        site_folder = "MangaKimi"
    elif choice == 9:
        site_folder = "Me-Manga"
    elif choice == 10:
        site_folder = "Reapertrans"
    elif choice == 11:
        site_folder = "Dragon-Manga"
    elif choice == 12:
        site_folder = "moodtoon"
    elif choice == 13:
        site_folder = "ToomTam-Manga"
    elif choice == 14:
        site_folder = "Miku-manga"
    elif choice == 15:
        site_folder = "Asurahunter"
    elif choice == 16:
        site_folder = "108-Manga"
    elif choice == 17:
        site_folder = "Joji-Manga"
    elif choice == 18:
        site_folder = "Spy-manga"
    elif choice == 19:
        site_folder = "Murim-Manga"
    elif choice == 20:
        site_folder = "Kumomanga"
    elif choice == 21:
        site_folder = "Mangastep"
    elif choice == 22:
        site_folder = "Jaymanga"
    elif choice == 23:
        site_folder = "Hippomanga"
    elif choice == 24:
        site_folder = "PopsManga"
    elif choice == 25:
        site_folder = "Tanuki-Manga"
    elif choice == 26:
        site_folder = "Inu-Manga"
    elif choice == 27:
        site_folder = "Lami-Manga"
    elif choice == 28:
        site_folder = "Weimanga"
    else:
        print("Invalid choice. Exiting...")
        sys.exit()

def split_image(image_path, num_parts):
    img = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"Failed to read image: {image_path}")
        return
    height, width, _ = img.shape
    part_height = height // num_parts
    image_parts = []

    for i in range(num_parts):
        top = i * part_height
        bottom = (i + 1) * part_height if i < num_parts - 1 else height
        img_part = img[top:bottom, :]
        image_parts.append(img_part)

    return image_parts

def main():
    display_menu()
    global choice
    choice = get_user_choice()
    set_website_settings(choice)
    # Get input path from the user
    output_path = input("Please enter a path: ")
    
    manga_folder = site_folder
    output_folder = os.path.join(output_path, site_folder)

    os.makedirs(output_folder, exist_ok=True)

    for root, _, files in os.walk(manga_folder):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.ico', '.tif', '.tiff', '.jfif', '.jp2')):
                source_path = os.path.join(root, file)
                relative_path = os.path.relpath(source_path, manga_folder)
                output_path = os.path.join(output_folder, relative_path)

                img = cv2.imdecode(np.fromfile(source_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
                if img is None:
                    print(f"Failed to read image: {source_path}")
                    continue
                height, width = img.shape[:2]
                aspect_ratio = (height / width)
                num_parts = int(aspect_ratio / 2)
                if num_parts <= 1:
                    print(f"Image has a perfect aspect ratio. Skipping {source_path}...")
                    continue
                else:    
                    desire_height = height // num_parts
                    print(f"Processing {source_path}...\nWidth = {width}px  |  Height = {height}px\nAspect ratio is {aspect_ratio}\nNumber of parts = {num_parts}\nDesire height = {desire_height}px\n")
                    
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                image_parts = split_image(source_path, num_parts)

                for i, img_part in enumerate(image_parts):
                    filename, extension = os.path.splitext(file)
                    part_filename = f"{filename}-part-{i + 1}{extension}"
                    part_output_path = os.path.join(
                        os.path.dirname(output_path),
                        part_filename
                    )
                    cv2.imwrite(part_output_path, img_part)

                # Remove the original image
                os.remove(source_path)

if __name__ == "__main__":
    main()
