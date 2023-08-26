import re
import os
import sys
import shutil

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

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def keep_last_subfolder(path):
    for folder in os.listdir(path):
        folder_path = os.path.join(path, folder)
        if os.path.isdir(folder_path):
            subfolders = [subfolder for subfolder in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, subfolder))]
            if subfolders:
                subfolders.sort(key=natural_sort_key)
                lastsub = subfolders[-1]
                print(f"Last subfolder is {lastsub}")
                for subfolder in subfolders[:-1]:
                    subfolder_path = os.path.join(folder_path, subfolder)
                    print(f"Removing subfolder: {subfolder_path}")
                    try:
                        shutil.rmtree(subfolder_path)  # Remove subfolder
                    except OSError as e:
                        print(f"Error removing {subfolder_path}: {e}")
                    else:
                        print(f"{subfolder_path} has been removed.")
                    
            print()

def main():
    display_menu()
    global choice
    choice = get_user_choice()
    set_website_settings(choice)
    current_path = os.path.join(os.getcwd(), site_folder)
    print(f"Keeping only the last subfolder in each main folder in current path '{current_path}':")
    keep_last_subfolder(current_path)
        
if __name__ == "__main__":
    main()
