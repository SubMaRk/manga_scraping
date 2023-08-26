import os
import sys

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

def main():
    display_menu()
    global choice
    choice = get_user_choice()
    set_website_settings(choice)
    data_path = os.path.join(site_folder, "data")  # Path to your folder
    fail_path = os.path.join(site_folder, "failed")

    # Get a list of filenames (without extensions) in the data folder
    datafilenames = os.listdir(data_path)
    datanames = [filename for filename in datafilenames]

    # Get a list of filenames (without extensions) in the failed folder
    failfilenames = os.listdir(fail_path)
    faildatanames = [filename for filename in failfilenames]

    for fail in faildatanames:
        if fail in datanames:
            # Set files path
            datafilepath = os.path.join(data_path, fail)
            failfilepath = os.path.join(fail_path, fail)
            
            print(f"Match {fail} and {fail}\n")
            print(f"Removing fail and data files : {fail}")
            
            # Remove data file
            if os.path.exists(datafilepath):
                print(f"Deleting {datafilepath}...")
                os.remove(datafilepath)
                print(f"{datafilepath} has been deleted.")
            else:
               print("File not found.")
            
            # Remove failed file
            if os.path.exists(failfilepath):
                print(f"Deleting {failfilepath}...")
                os.remove(failfilepath)
                print(f"{failfilepath} has been deleted.")
            else:
                print("File not found.")
            
        else:
            continue
        
if __name__ == "__main__":
    main()
