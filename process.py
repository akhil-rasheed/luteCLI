import os
import eyed3
import argparse
import multiprocessing


def get_song_titles(folder_path):
    song_titles = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and file_name.endswith(".mp3"):
            try:
                audio = eyed3.load(file_path)
                if audio.tag is not None:
                    if audio.tag.title:
                        title = audio.tag.title
                        artist = audio.tag.artist if audio.tag.artist else "Unknown Artist"
                        song_title = f"{artist} - {title}"
                        song_titles.append(song_title)
            except Exception as e:
                print(f"Error reading file: {file_name} - {str(e)}")
    return song_titles


def create_text_file(folder_path, song_titles):
    playlist_dir = os.path.join(os.getcwd(), "playlists")
    os.makedirs(playlist_dir, exist_ok=True)
    dir_name = os.path.basename(folder_path)
    text_file_path = os.path.join(playlist_dir, f"{dir_name}.txt")
    with open(text_file_path, "w") as file:
        for title in song_titles:
            file.write(title + "\n")


def process_folder(folder_path):
    song_titles = get_song_titles(folder_path)
    if song_titles:
        create_text_file(folder_path, song_titles)
        print(f"Text file created for {folder_path}")


# Parse command line arguments
parser = argparse.ArgumentParser(description="Generate playlists from MP3 files.")
parser.add_argument("folder_path", help="Path to the folder containing the MP3 files.")
args = parser.parse_args()

# Process the folder
print("Processing folder...")
processes = []
for dir_name, subdirs, file_names in os.walk(args.folder_path):
    if subdirs or file_names:
        p = multiprocessing.Process(target=process_folder, args=(dir_name,))
        processes.append(p)
        p.start()

for p in processes:
    p.join()

print("Folder processing complete.")
