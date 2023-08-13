# Manga Downloader

A Python script for downloading manga chapters from various Thailand manga websites.

## Table of Contents

- [Description](#description)
- [Dependencies](#dependencies)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Supported Websites](#supported-websites)
- [Contributing](#contributing)
- [License](#license)

## Description

This Python script allows you to download manga chapters from various websites. It utilizes the `requests` library to fetch web pages and the `BeautifulSoup` library to parse HTML content. The script supports multi-threading for faster downloading of multiple chapters.

## Dependencies

- `requests`: Used for making HTTP requests.
- `BeautifulSoup`: Used for parsing HTML content.
- `os`: Used for file and directory operations.
- `re`: Used for regular expressions.
- `urllib.parse`: Used for URL parsing.
- `http.client.IncompleteRead`: Used for handling incomplete HTTP reads.
- `time`: Used for time-related operations.
- `subprocess`: Used for executing shell commands.
- `threading`: Used for managing threads.
- `concurrent.futures`: Used for managing concurrent tasks.
- `json`: Used for parsing JSON data.
- `sys`: Used for interacting with the system.

## Features

- Downloads manga chapters from a variety of supported websites.
- Handles different types of websites with custom parsing logic.
- Utilizes multi-threading to speed up the downloading process.
- Supports updating existing manga data with new chapter information.

## Installation

1. Make sure you have Python 3.x installed on your system.
2. Clone or Download this repository to your local machine.
3. Install the required dependencies by running the following command:

   ```bash
   pip install requests beautifulsoup4
   ```
## Usage

1. Run the script using a Python interpreter: `python thmangadownloader.py`.
2. Select a manga website from the displayed menu (options 1-28).
3. The script will fetch manga URLs from the selected website.
4. It will process each manga URL, downloading images and updating metadata.

## Supported Websites
The script supports downloading manga from the following websites:

- ThaiManga
- Flash-Manga
- Manga168
- TamaManga
- สดใสเมะ
- Ped-Manga
- SING-MANGA
- MangaKimi
- Me-Manga
- Reapertrans
- Dragon-Manga
- moodtoon
- ToomTam-Manga
- Miku-manga
- Asurahunter
- 108-Manga
- Joji-Manga
- Spy-manga
- Murim-Manga
- Kumomanga
- Mangastep
- Jaymanga
- Hippomanga
- PopsManga
- Tanuki-Manga
- Inu-Manga
- Lami-Manga
- Weimanga

(Note: This list may not be exhaustive. Please refer to the script for the complete list of supported websites.)

## Contributing
Contributions are welcome! If you have any suggestions, bug fixes, or new features, please feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License.
