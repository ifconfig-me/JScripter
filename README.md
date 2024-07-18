## JScripter - A Noob-Friendly JavaScript Scraper!
JScripter is a Python script designed to scrape and save unique JavaScript files from a list of URLs or a single URL.

## Disclaimer

> This tool is intended only for educational purposes and for testing in corporate environments. https://twitter.com/nav1n0x/ and https://github.com/ifconfig-me take no responsibility for the misuse of this code. Use it at your own risk. Do not attack a target you don't have permission to engage with.

Feelfee to fork and make this script your own :)
 

## Features

- Scrape JavaScript files from multiple URLs concurrently using threading.
- Save unique JavaScript files to a specified directory and - Print confirmation.
- Removed duplicate JSFiles
- Display detailed progress information, including the number of URLs processed, elapsed time, and approximate remaining time.
- Silent mode for minimal output.

## Screenshots
### Single URL Mode:
![image](https://github.com/user-attachments/assets/adc50477-0352-4208-9b9c-22f617859faf)

### Multi-urls Mode
![image](https://github.com/user-attachments/assets/0a35f788-3e9b-40d8-bf54-7a926df3d776)

### Deduplicates Automativally:
![image](https://github.com/user-attachments/assets/df056d65-7384-4b8c-aa9c-d78e422cef85)

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library
- `colorama` library
- `tqdm` library

You can install the required libraries using pip:

```
pip install requests beautifulsoup4 colorama tqdm
```

## Installation

1. Clone the repository:

    * git clone https://github.com/ifconfig-me/JScripter/JScripter.git
    * cd JScripter
``
2. Ensure that GAU, hakrawler, and FFUF are installed and accessible from the command line.

## Usage

### From a List of URLs
1. Create a file containing the list of target URLs (e.g., urls.txt).
2. Run the script:

```python JScripter.py -f urls.txt -d saved_js_files -t 10```

### From a Single URL
1. Run the script with a single URL:
```python JScripter.py -u https://example.com -d saved_js_files -t 10```

## Command-Line Arguments
* -f, --file: File containing list of target URLs.
* -u, --url: Single target URL.
* -d, --directory: Directory to save unique JavaScript files (required).
* -s, --silent: Silent mode. No banner, no progress, only URLs.
* -t, --threads: Number of threads to use for concurrent processing (default is 5).
