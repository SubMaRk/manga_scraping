import requests as rq
from bs4 import BeautifulSoup as bs
import re
import os
import urllib.parse
from http.client import IncompleteRead
from requests.exceptions import Timeout, RequestException
import time
import subprocess
import threading
import concurrent.futures
import json
import sys

# UserAgent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

clear = lambda: subprocess.call('cls||clear', shell=True)

# Create a lock to avoid multiple threads writing to the same file at the same time
file_lock = threading.Lock()

# Function to download images for a manga URL
def process_manga(manga_url):
    # Get manga id from url
    decoded_url = urllib.parse.urlparse(manga_url)
    manga_name = decoded_url.path.split("/")
    
    # Process manga url
    rsp = rq.get(manga_url, headers=headers)
    soup = bs(rsp.content, "html.parser")
    manga_info = soup.find("div", class_="postbody")

    li_tags = soup.find('div', {'id': 'chapterlist'}).find('ul').find_all('li')
    if li_tags:
        chaptercount = len(li_tags)
        last_li_tag = li_tags[-1]
        getalink = last_li_tag.find('a')['href']
        chapter_url = urllib.parse.unquote(getalink)
    else:
        chaptercount = ''
        chapter_url = ''

    if choice == 3:
        manga_type = manga_info.find('td', text='ประเภท')
        if manga_type:
            category = manga_type.find_next_sibling('td').get_text()
        else:
            category = ''
    elif choice == 12:
        manga_type = manga_info.find('td', text='Type')
        if manga_type:
            category = manga_type.find_next_sibling('td').get_text()
        else:
            category = ''
    else:
        manga_type = manga_info.find_all('div', class_='imptdt')
        if manga_type:
            manga_type = manga_type[1]
            category = manga_type.find('a').text.strip()
        else:
            category = ''

    manga_title = manga_info.find("h1", class_="entry-title")
    if manga_title:
        title = manga_title.text.strip()

    sanitized = re.sub(r'[\\/:"*?<>|]', '', title)

    if choice == 3:
        manga_status = manga_info.find('td', text='สถานะ')
        if manga_status:
            status = manga_status.find_next_sibling('td').get_text()
        else:
            status = ''
    elif choice == 12:
        manga_status = manga_info.find('td', text='Status')
        if manga_status:
            status = manga_status.find_next_sibling('td').get_text()
        else:
            status = ''
    else:
        manga_status = manga_info.find('div', class_='imptdt')
        if manga_status:
            status = manga_status.find('i').text.strip()
        else:
            status = ''

    post_date = manga_info.find("time", itemprop="datePublished")
    if post_date:
        post_time = post_date.get("datetime", "")
    else:
        post_time = ''

    last_update = manga_info.find("time", itemprop="dateModified")
    if last_update:
        update_time = last_update.get("datetime", "")
    else:
        update_time = ''

    # Save manga data
    fail_folder = os.path.join(site_folder, "failed")
    if not os.path.exists(fail_folder):
        os.makedirs(fail_folder)

    # Save manga data
    data_folder = os.path.join(site_folder, "data")
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # Set file data name
    file_data_name = urllib.parse.unquote(manga_name[2])
    file_data_path = os.path.join(data_folder, f"{file_data_name}.txt")

    
    # Set failed filename
    fail_data_path = os.path.join(fail_folder, f"{file_data_name}.txt")
    
    old_type = ''
    savestatus = ''
    lastupdate = ''
    savecount = ''
    type_prefix = "Type : "
    status_prefix = "Status : "
    lastvisit_prefix = "Last Visit : "
    lastupdate_prefix = "Last Update : "
    count_prefix = "Count Chapter : "
    if os.path.exists(file_data_path):
        print(f"Reading file : {file_data_path}...")
        with open(file_data_path, "r", encoding='utf-8') as file:
            for line in file:
                if line.startswith(type_prefix):
                    old_type = line[len(type_prefix):].strip()
                elif line.startswith(status_prefix):
                    savestatus = line[len(status_prefix):].strip()
                elif line.startswith(lastvisit_prefix):
                    chapter_url = line[len(lastvisit_prefix):].strip()
                elif line.startswith(lastupdate_prefix):
                    lastupdate = line[len(lastupdate_prefix):].strip()
                elif line.startswith(count_prefix):
                    savecount = line[len(count_prefix):].strip()
                else:
                    continue
        print(f'Reading data from {file_data_path} finish!')
    else:
        print(f"No manga data found. Writing the new data.")
        with open(file_data_path, "w", encoding='utf-8') as file:
            file.write(f"Title : {title}\n")
            file.write(f"Type : {category}\n")
            file.write(f"Status : {status}\n")
            file.write(f"Post Date : {post_time}\n")
            file.write(f"Last Update : {update_time}\n")
            file.write(f"URL : {manga_url}\n")
            file.write(f"Last Visit : {chapter_url}\n")
            file.write(f"Count Chapter : {chaptercount}")

    # Update status
    if savestatus != '' and savestatus != status:
        with open(file_data_path, "r", encoding='utf-8') as file:
                data = file.readlines()
                newline = []
                save_status = data[2].strip()
                new_status = f"Status : {status}"
                for word in data:
                    newline.append(word.replace(save_status, new_status))

                with open(file_data_path, "w", encoding='utf-8') as file:
                    for line in newline:
                        file.writelines(line)
    # Update last update date
    if lastupdate != '' and lastupdate != update_time:
        with open(file_data_path, "r", encoding='utf-8') as file:
                data = file.readlines()
                newline = []
                last_update = data[4].strip()
                new_update = f"Last Update : {update_time}"
                for word in data:
                    newline.append(word.replace(last_update, new_update))

                with open(file_data_path, "w", encoding='utf-8') as file:
                    for line in newline:
                        file.writelines(line)

    # Update chapter count
    if chaptercount != '' and chaptercount != savecount:
        with open(file_data_path, "r", encoding='utf-8') as file:
                data = file.readlines()
                newline = []
                last_update = data[7].strip()
                new_update = f"Count Chapter : {chaptercount}"
                for word in data:
                    newline.append(word.replace(last_update, new_update))

                with open(file_data_path, "w", encoding='utf-8') as file:
                    for line in newline:
                        file.writelines(line)

    # Get manga folder name
    if category != '' and status != '':
        name = f"[{category}] {sanitized} [{status}]"
        folder_name = os.path.join(site_folder, name)
    elif category == '' and status != '':
        name = f"{sanitized} [{status}]"
        folder_name = os.path.join(site_folder, name)
    elif status == '' and category != '':
        name = f"[{category}] {sanitized}"
        folder_name = os.path.join(site_folder, name)
    else:
        name = f"{sanitized}"
        folder_name = os.path.join(site_folder, name)
    print(f"Folder Name : {folder_name}")
    
    # Get old folder name
    if os.path.exists(file_data_path):
        if old_type != '' and savestatus != '':
            folder = f"[{old_type}] {sanitized} [{savestatus}]"
            old_folder = os.path.join(site_folder, folder)
        elif old_type == '' and savestatus != '':
            folder = f"{sanitized} [{savestatus}]"
            old_folder = os.path.join(site_folder, folder)
        elif savestatus == '' and old_type != '':
            folder = f"[{old_type}] {sanitized}"
            old_folder = os.path.join(site_folder, folder)
        else:
            folder = f"{sanitized}"
            old_folder = os.path.join(site_folder, folder)
        print(f"Old folder name : {old_folder}")
        if old_folder and old_folder != '':
            if old_folder != folder_name:
                safe_rename(old_folder, folder_name)
                
    # Create manga folder
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Fetch cover image
    cover_img = soup.select_one(".thumb img")
    if cover_img:
        cover = cover_img["src"]
    else:
        cover = ''
    if cover:
        file_extension = os.path.splitext(cover)[1]
        cover_name = f"{sanitized}{file_extension}"
        cover_path = os.path.join(folder_name, cover_name)
        if os.path.exists(cover_path):
            print(f"File size Checking : {cover_name}...")
            compare_size(cover, cover_path)
        else:
            rsp = rq.get(cover,headers=headers, stream=True)
            if rsp.status_code == 200:
                with open(cover_path, "wb") as file:
                    for chunk in rsp.iter_content(1024):
                        file.write(chunk)

    # Start process chapters link
    while chapter_url:
        print(f"Title : {title}\nType : {category}\nStatus : {status}\nPost Date : {post_time}\nLast Update : {update_time}\nURL : {manga_url}")
        print(f"Fetching : {chapter_url}")

        # Replace last update date
        with open(file_data_path, "r", encoding='utf-8') as file:
            data = file.readlines()
            newline = []
            last_visit = data[6].strip()
            new_visit = f"Last Visit : {chapter_url}"
            for word in data:
                newline.append(word.replace(last_visit, new_visit))

            with open(file_data_path, "w", encoding='utf-8') as file:
                for line in newline:
                    file.writelines(line)
        
        rsp = rq.get(chapter_url, headers=headers)
        soup = bs(rsp.content, "html.parser")
        
        # Set images div to detect
        readerarea_div = soup.find("div", id ="readerarea")
        
        # Set script detect regex.
        script_tag = soup.find("script", string=re.compile(r'ts_reader\.run'))
        readscript = readerarea_div.find_all("script", string=re.compile(r'eval\(function\(p,a,c,k,e,d\)'))
        jsondata = image_tags = ''
        
        if script_tag:
            # Extract the JSON-like text from the script tag
            pattern = r'ts_reader\.run\((.+?)\);'
            match = re.search(pattern, script_tag.string)

            if match:
                # Load the JSON-like text as a Python dictionary
                try:
                    data = json.loads(match.group(1))
                except json.JSONDecodeError as e:
                    print("Error parsing JSON:", e)
                else:
                    # Now you can access the data as needed
                    jsondata = data
            else:
                print("Script tag content not found.")
        elif readerarea_div:
            if readscript:
                print(f"Found the images controlled by javascript. Can't download them, skipping...")
            else:
                image_tags = readerarea_div.find_all('img')
                if image_tags:
                    print("Found images from readeraarea div.")
                else:
                    print("Can't find images from readerarea div.")
        else:
            print("Script tag and Readerarea div not found.")
            os.makedirs(os.path.dirname(fail_data_path), exist_ok=True)
             # Use the download_with_retry function
            with open(fail_data_path, "a+", encoding='utf-8') as file:
                file.write(f"{chapter_url}\n")
        

        chapter_id = extchapterid(chapter_url, file_data_name)
        print(f"Chapter Number : {chapter_id}")
        chapter_folder = f"Chapter-{chapter_id}"

        if jsondata:
            # Check if 'sources' list exists and is not empty
            if 'sources' in jsondata and len(jsondata['sources']) > 0:
                # Extract image links from the 'images' key
                images_list = jsondata['sources'][0].get('images', [])
                
                for i, img_link in enumerate(images_list):
                    print(f"{img_link}")
                    file_extension = os.path.splitext(img_link)[1]
                    if not file_extension:
                        print(f"Invalid image link, skipping...")
                        continue
                    
                    # Check googleusercontent url for skipping
                    if "googleusercontent.com" in img_link:
                        print(f"Skipping image link: {img_link}")
                        continue

                    image_file_name = f"Chapter-{chapter_id}_image_{i}{file_extension}"
                    image_file_path = os.path.join(folder_name, chapter_folder, image_file_name)
                    if os.path.exists(image_file_path):
                        print(f"File size Checking : {image_file_name}...")
                        compare_size(img_link, image_file_path)
                    else:
                        os.makedirs(os.path.dirname(image_file_path), exist_ok=True)
                        # Use the download_with_retry function
                        download_with_retry(img_link, image_file_path)
                print(f"All image links Downloaded. Checking the number of files.")
                chapter_fd = os.path.join(folder_name, chapter_folder)
                chapter_img_list = [os.path.join(chapter_fd, f) for f in os.listdir(chapter_fd) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]
                local_list_count = len(chapter_img_list)
                img_list_count = len(images_list)
                if local_list_count != img_list_count:
                    print(f"Number of files is not same.\nWriting {chapter_url} to {fail_data_path}.")
                    os.makedirs(os.path.dirname(fail_data_path), exist_ok=True)
                    # Use the download_with_retry function
                    with open(fail_data_path, "a+", encoding='utf-8') as file:
                        file.write(f"{chapter_url}\n")
                else:
                    print(f"Number of files is same, {local_list_count}/{img_list_count} files.")
        elif image_tags:
            images_list = [img['src'] for img in image_tags]
            for i, img_link in enumerate(images_list):
                print(f"{img_link}")
                # Check file extension
                file_extension = os.path.splitext(img_link)[1]
                if not file_extension:
                    print(f"Invalid image link, skipping...")
                    continue
                # Check googleusercontent url for skipping
                if "googleusercontent.com" in img_link:
                    print(f"Skipping image link: {img_link}")
                    continue
                
                image_file_name = f"Chapter-{chapter_id}_image_{i}{file_extension}"
                image_file_path = os.path.join(folder_name, chapter_folder, image_file_name)
                if os.path.exists(image_file_path):
                    print(f"File size Checking : {image_file_name}...")
                    compare_size(img_link, image_file_path)
                else:
                    os.makedirs(os.path.dirname(image_file_path), exist_ok=True)
                    # Use the download_with_retry function
                    download_with_retry(img_link, image_file_path)
            print(f"All image links Downloaded. Checking the number of files.")
            chapter_fd = os.path.join(folder_name, chapter_folder)
            chapter_img_list = [os.path.join(chapter_fd, f) for f in os.listdir(chapter_fd) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]
            local_list_count = len(chapter_img_list)
            img_list_count = len(images_list)
            if local_list_count != img_list_count:
                print(f"Number of files is not same.\nWriting {chapter_url} to {fail_data_path}.")
                os.makedirs(os.path.dirname(fail_data_path), exist_ok=True)
                # Use the download_with_retry function
                with open(fail_data_path, "a+", encoding='utf-8') as file:
                    file.write(f"{chapter_url}\n")
        else:
            print("No image found.")
            os.makedirs(os.path.dirname(fail_data_path), exist_ok=True)
            # Use the download_with_retry function
            with open(fail_data_path, "a+", encoding='utf-8') as file:
                file.write(f"{chapter_url}\n")

        findrocket = soup.find("script", string=re.compile(r'jQuery\(\'\.ch-next-btn\'\)'))
        # Set next chapter url from 'nextUrl' key.
        if jsondata:
            nextURL = jsondata['nextUrl']
            if nextURL != '':
                parseurl = urllib.parse.unquote(nextURL)
                chapter_url = parseurl
                print(f"Next Chpter URL : {chapter_url}")
            else:
                break
        elif image_tags:
            if findrocket:
                findurl_rex = r'jQuery\(\'\.ch-next-btn\'\)\.attr\("href", "(.*?)"\);'
                matchNext = re.search(findurl_rex, findrocket.string)
                findnext = matchNext.group(0)
                pattern = r'"(https?://.*?)"'
                match = re.search(pattern, findnext)
                if match:
                    href_value = match.group(0)
                    url = href_value.replace('"', '')
                    parseurl = urllib.parse.unquote(url)
                    chapter_url = parseurl
                    print(f"Next Chpter URL : {chapter_url}")
                else:
                    print("Next chapter link not found.")
                    break
            else:
                break
        else:
            print("Can't find next chapter link.")
            break

        clear()

def safe_rename(old_folder_name, new_folder_name):
    try:
        os.rename(old_folder_name, new_folder_name)
        print(f"Renamed {old_folder_name} to {new_folder_name}")
    except OSError as e:
        print(f"Error renaming {old_folder_name} to {new_folder_name}: {e}")

def get_content_size(url):
    try:
        response = rq.head(url)
        if response.status_code == 200:
            content_size = int(response.headers.get('Content-Length', 0))
            return content_size
        else:
            print(f"Failed to retrieve content size. Status code: {response.status_code}")
    except rq.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return None

def compare_size(img_link, image_file_path):
    content_size = get_content_size(img_link)
    if content_size is not None:
        image_file_size = os.path.getsize(image_file_path)
        if image_file_size == content_size:
            print("Image file size and content size match.")
        else:
            print("Image file size and content size do not match.")
            print(f"Image file size: {image_file_size} bytes")
            print(f"Content size: {content_size} bytes")
            download_with_retry(img_link, image_file_path)
    else:
        print("Failed to get content size from the URL.")

def download_with_retry(url, destination, timeout=15, max_retries=3):
    for i in range(max_retries):
        try:
            response = rq.get(url, headers=headers, stream=True, timeout=timeout)
            response.raise_for_status()

            with open(destination, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

            compare_size(url, destination)
            break
        except (rq.exceptions.ChunkedEncodingError, IncompleteRead, rq.exceptions.RequestException) as e:
            print(f"Error downloading {url}. Retry {i + 1}/{max_retries}")
            # Wait for a short time before retrying (e.g., 1 second)
            time.sleep(1)
        except rq.exceptions.Timeout as e:
            print(f"Timeout error downloading {url}. Retry {i + 1}/{max_retries}")
            # Wait for a longer time before retrying (e.g., 5 seconds)
        except Exception as e:
            break
    else:
        print(f"Failed to download {url} after {max_retries} retries.")

# Extract manga id from url
def extchapterid(chapter_url, file_data_name):
    manga_id = file_data_name
    getNum = chapter_url.split("/")
    chapterNum = getNum[-2]
    # Unquote the URL-encoded text
    chapter = urllib.parse.unquote(chapterNum)
    manga = chapter.replace(manga_id,'')
    # Attempt to find the pattern \d+-\d+\-\d+
    match1 = re.search(r'\d+-\d+', manga[::-1])
    
    if match1:
        get2lastnum = match1.group()[::-1]
        chapter_id = get2lastnum
    else:
        # Attempt to find the pattern \d+-\d+
        match_2 = re.search(r'\d+', manga[::-1])
        
        if match_2:
            getlastnum = match_2.group()[::-1]
            chapter_id = getlastnum
        else:
            # Use the existing logic if no pattern is found
            chapter_id = '-'.join(filter(lambda x: x.isdigit(), manga.split('-')[-2:]))
                
            if not chapter_id:
                chapter_id = '-'.join(filter(lambda x: x.isdigit() or x == "-", manga.split('%')[0].split('-')))
    
    return chapter_id

def process_manga_thread(manga_url):
    try:
        process_manga(manga_url)
    except Exception as e:
        print(f"Error processing manga URL {manga_url}: {e}")

# Display menu for select support manga website
def display_menu():
    print("Please select a manga website.")
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
    global main_url, site_folder
    if choice == 1:
        main_url = "https://www.thaimanga.net/manga-list"
        site_folder = "ThaiManga"
    elif choice == 2:
        main_url = "https://www.flash-manga.com/manga-list"
        site_folder = "Flash-Manga"
    elif choice == 3:
        main_url = "https://manga168.com/a-z"
        site_folder = "Manga168"
    elif choice == 4:
        main_url = "https://www.tamamanga.com/manga-list"
        site_folder = "TamaManga"
    elif choice == 5:
        main_url = "https://www.xn--l3c0azab5a2gta.com/manga-list"
        site_folder = "สดใสเมะ"
    elif choice == 6:
        main_url = "https://ped-manga.com/%E0%B8%A1%E0%B8%B1%E0%B8%87%E0%B8%87%E0%B8%B0-a-z"
        site_folder = "Ped-Manga"
    elif choice == 7:
        main_url = "https://www.sing-manga.com/manga-list"
        site_folder = "SING-MANGA"
    elif choice == 8:
        main_url = "https://www.mangakimi.com/manga-list"
        site_folder = "MangaKimi"
    elif choice == 9:
        main_url = "https://www.me-manga.com/manga-list"
        site_folder = "Me-Manga"
    elif choice == 10:
        main_url = "https://reapertrans.com/%E0%B8%A1%E0%B8%B1%E0%B8%87%E0%B8%87%E0%B8%B0-a-z"
        site_folder = "Reapertrans"
    elif choice == 11:
        main_url = "https://www.dragon-manga.com/manga-list"
        site_folder = "Dragon-Manga"
    elif choice == 12:
        main_url = "https://moodtoon.com/az-lists"
        site_folder = "moodtoon"
    elif choice == 13:
        main_url = "https://toomtam-manga.com/%E0%B8%A1%E0%B8%B1%E0%B8%87%E0%B8%87%E0%B8%B0-a-z"
        site_folder = "ToomTam-Manga"
    elif choice == 14:
        main_url == "https://miku-manga.com/%E0%B8%A1%E0%B8%B1%E0%B8%87%E0%B8%87%E0%B8%B0-a-z"
        site_folder = "Miku-manga"
    elif choice == 15:
        main_url = "https://asurahunter.com/%E0%B8%A1%E0%B8%B1%E0%B8%87%E0%B8%87%E0%B8%B0-a-z"
        site_folder = "Asurahunter"
    elif choice == 16:
        main_url = "https://www.108-manga.com/manga-list"
        site_folder = "108-Manga"
    elif choice == 17:
        main_url = "https://joji-manga.com/%E0%B8%A1%E0%B8%B1%E0%B8%87%E0%B8%87%E0%B8%B0%20a-z"
        site_folder = "Joji-Manga"
    elif choice == 18:
        main_url = "https://spy-manga.com/%E0%B8%A1%E0%B8%B1%E0%B8%87%E0%B8%87%E0%B8%B0-a-z"
        site_folder = "Spy-manga"
    elif choice == 19:
        main_url = "https://murim-manga.com/%E0%B8%A1%E0%B8%B1%E0%B8%87%E0%B8%87%E0%B8%B0-a-z"
        site_folder = "Murim-Manga"
    elif choice == 20:
        main_url = "https://kumomanga.net/a-z"
        site_folder = "Kumomanga"
    elif choice == 21:
        main_url = "https://mangastep.com/a-z"
        site_folder = "Mangastep"
    elif choice == 22:
        main_url = "https://jaymanga.com/%E0%B8%A1%E0%B8%B1%E0%B8%87%E0%B8%87%E0%B8%B0-a-z"
        site_folder = "Jaymanga"
    elif choice == 23:
        main_url = "https://hippomanga.com/%E0%B8%A1%E0%B8%B1%E0%B8%87%E0%B8%87%E0%B8%B0-a-z"
        site_folder = "Hippomanga"
    elif choice == 24:
        main_url = "https://popsmanga.com/%E0%B8%A1%E0%B8%B1%E0%B8%87%E0%B8%87%E0%B8%B0-a-z"
        site_folder = "PopsManga"
    elif choice == 25:
        main_url = "https://www.tanuki-manga.com/manga-list"
        site_folder = "Tanuki-Manga"
    elif choice == 26:
        main_url = "https://www.inu-manga.com/manga-list"
        site_folder = "Inu-Manga"
    elif choice == 27:
        main_url = "https://www.lami-manga.com/%E0%B8%A1%E0%B8%B1%E0%B8%87%E0%B8%87%E0%B8%B0-a-z"
        site_folder = "Lami-Manga"
    elif choice == 28:
        main_url = "https://weimanga.com/a-z"
        site_folder = "Weimanga"
    else:
        print("Invalid choice. Exiting...")
        sys.exit()

def main():
    display_menu()
    global choice
    choice = get_user_choice()
    set_website_settings(choice)
    # Set main URL
    if main_url is None:
        print("Invalid choice. Exiting...")
        return
    
    show_url = "?show="
    variations = ["."] + ["0-9"] + [chr(i) for i in range(ord("A"), ord("Z") + 1)]
    folder_list = os.path.join(site_folder, "list")
    folder_error = os.path.join(site_folder, "failed")
    manga_url = []
    
    # Loop fetching manga url
    for variation in variations:
        list_name = f"{variation}.txt"
        list_path = os.path.join(folder_list, list_name)
        if os.path.exists(list_path):
            with open(list_path, "r", encoding='utf-8') as file:
                urls = file.readlines()
                manga_url.extend(url.strip() for url in urls)
        else:
            page_number = 1
            while True:
                page_url = f"{main_url}/page/{page_number}/{show_url}{variation}"
                print(f"Fetching list from {page_url}")

                response = rq.get(page_url, headers=headers)
                soup = bs(response.content, 'html.parser')
                manga_list = soup.select('.bs .bsx')
                if not manga_list:
                    page_number = 0
                    break

                for data in manga_list:
                    url = data.find('a')['href']
                    unquote = urllib.parse.unquote(url)
                    manga_url.append(unquote)
                    print(unquote)

                    list_name = f"{variation}.txt"
                    list_path = os.path.join(folder_list, list_name)
                    if os.path.exists(list_path):
                        with open(list_path, "a+", encoding='utf-8') as file:
                            file.write(f"{unquote}\n")
                    else:
                        os.makedirs(os.path.dirname(list_path), exist_ok=True)
                        # Use the download_with_retry function
                        with open(list_path, "a+", encoding='utf-8') as file:
                            file.write(f"{unquote}\n")
                    
                print(f"Save urls to file : {list_name} successful.")

                page_number += 1
    manga_count = len(manga_url)
    print(f"Total URL: {manga_count}")
    
    # Reading error manga id from files
    if os.path.exists(folder_error):
        errorpath = os.listdir(folder_error)
        errorlist = [file[:-4] for file in os.listdir(errorpath) if os.path.isfile(os.path.join(errorpath, file)) and '.' in file]
    else:
        errorlist = []

    # Create a ThreadPoolExecutor with 16 workers
    with concurrent.futures.ThreadPoolExecutor(max_workers=24) as executor:
        # List to store the submitted futures
        futures = []
        # Submit manga URLs for processing and store the futures
        for manga in manga_url:
            # Get manga id from url
            decoded_url = urllib.parse.urlparse(manga)
            manga_name = decoded_url.path.split("/")
            data_name = urllib.parse.unquote(manga_name[2])
            if data_name in errorlist:
                print(f"Found {data_name} in error list, skipping...")
                continue
            else:
                future = executor.submit(process_manga_thread, manga)
                futures.append(future)

        # Process futures as they complete
        for future in concurrent.futures.as_completed(futures):
            try:
                # Get the result of the completed future (if any)
                result = future.result()
                if result is not None:
                    print(f"Thread completed successfully: {result}")
                else:
                    print("Thread did not return any result.")
            except Exception as e:
                print(f"Error processing manga URL: {e}")
                
# Main
if __name__ == "__main__":
    main()
