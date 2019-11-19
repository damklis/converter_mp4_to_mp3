from pydub import AudioSegment
import glob
import os
import time
import multiprocessing as multi


## Measuring script execution time.
start = time.time()

def clean_filename(filepath):
    """
    Returns filename without .mp4 type.
    """
    return filepath.split("/")[-1].replace(".mp4", "")

def directory_status(dir_name):
    """
    Checks if provided direcotry exists.
    If not, creates one in the project root direcotory.
    Returns True.
    """
    try:
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
            print(f"Directory {dir_name} created.")
            return True
    except OSError as err:
        print(f"ERROR: {err}")
        return False

def convert_mp4_to_mp3(filepath, dir_name ,prefix):
    """
    Converts .mp4 file to mp3 and save it in the provided path.
    """
    filename = prefix + clean_filename(filepath)

    try:
        video = AudioSegment.from_file(filepath)
    except OSError as err:
        print(f"ERROR: {err}")
        
    if directory_status(dir_name):
        video.export(
            out_f=f"{dir_name}/{filename}.mp3",
            format="mp3",
            bitrate="312k",
            tags={
                "title":f"{filename}",
                "artist":"Example",
                "album": "Example"
                },
            cover="assets/cover.png"
            )

    print(f"Converted {filename}.mp4 to {filename}.mp3. Process:{os.getpid()}.")

def run_conversion():
    """
    Running script using a multiprocessing module.
    """
    pool = multi.Pool(multi.cpu_count())
    pool.starmap(
        convert_mp4_to_mp3,
        [(path, "audios", "example") for path in glob.glob("videos/*.mp4")]
        )

if __name__ == "__main__":
    run_conversion()

print(f"In seconds: {round(time.time()- start,2)}s.")