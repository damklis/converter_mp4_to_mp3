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

def convert_mp4_to_mp3(filepath, prefix="lesson"):
    """
    Converts .mp4 file to mp3 and save it in the provided path.
    """
    filename = prefix + clean_filename(filepath)
    proc = os.getpid()

    if not os.path.exists("audios"):
        os.mkdir("audios")
        print("Directory audios created.")

    try:
        video = AudioSegment.from_file(filepath)
    except OSError as err:
        print("ERROR: " + err)
        
    video.export(
        out_f=f"audios/{filename}.mp3",
        format="mp3",
        bitrate="312k",
        tags={
            "title":f"{filename}",
            "artist":"DamKlis",
            "album": "xxxxxxx"
            },
        cover="assets/cover.png"
        )

    print(f"Converted {filename}.mp4 to {filename}.mp3 by process {proc}.")

def run_conversion():
    """
    Running script using a multiprocessing module.
    """
    pool = multi.Pool(multi.cpu_count())
    pool.map(
        convert_mp4_to_mp3,
        [path for path in glob.glob("videos/*.mp4")]
        )

if __name__ == "__main__":
    run_conversion()

print(f"In seconds: {round(time.time()- start,2)}s.")