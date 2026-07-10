import os
import urllib.request

# The source auto-updating playlist
SOURCE_URL = "https://raw.githubusercontent.com/sm-monirulislam/Toffee-Auto-Update-Playlist/refs/heads/main/toffee_playlist.m3u"

# Target files in your repository
TARGET_1 = "playlist/TF/TF-1.m3u8"
TARGET_6 = "playlist/TF/TF-6.m3u8"

def ensure_dir(file_path):
    """Ensure the directory exists before writing."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

def main():
    # Fetch the latest playlist
    req = urllib.request.Request(SOURCE_URL, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            lines = response.read().decode('utf-8').splitlines()
    except Exception as e:
        print(f"Error fetching source playlist: {e}")
        return

    url_1 = None
    url_6 = None

    # Parse the m3u file to find the links (including their cache tokens)
    for i, line in enumerate(lines):
        if line.startswith("#EXTINF"):
            upper_line = line.upper()
            # Grab the URL on the next line
            if "FIFA WC CHANNEL 1" in upper_line:
                url_1 = lines[i+1].strip()
            elif "FIFA WC CHANNEL 6" in upper_line:
                url_6 = lines[i+1].strip()

    # Write the extracted URL to TF-1.m3u8
    if url_1:
        ensure_dir(TARGET_1)
        with open(TARGET_1, "w") as f:
            f.write(f"#EXTM3U\n{url_1}\n")
        print("Updated TF-1.m3u8 successfully.")
    else:
        print("Could not find FIFA WC CHANNEL 1 in the source.")

    # Write the extracted URL to TF-6.m3u8
    if url_6:
        ensure_dir(TARGET_6)
        with open(TARGET_6, "w") as f:
            f.write(f"#EXTM3U\n{url_6}\n")
        print("Updated TF-6.m3u8 successfully.")
    else:
        print("Could not find FIFA WC CHANNEL 6 in the source.")

if __name__ == "__main__":
    main()
