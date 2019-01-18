import click
import requests
import json
import jsonlines
import os
import subprocess
from multiprocessing import Pool

@click.command()
@click.argument('filename', required=1)
@click.option('--output-folder', default='subtitles', help='Output folder to put video list files.')
@click.option('--processes', default='5', help='Number of parallel downloads. Use with caution, be gentle.')
def get_channel_videos(filename, output_folder, processes):
    """CLI tool to help downloading Subtitles from many Youtube Channels"""
    # Video File Schema: 
    # { name: string, id: string}

    # Open Video File 
    try:
        # start some worker processes
        pool = Pool(processes=5) 
        with jsonlines.open(filename) as reader:
            # Iterate over lines and open some threads
            pool.map(process_video, [video for video in reader]) 

    # I dont think this works, has to do with the subprocess shit in process_video
    except KeyboardInterrupt:
        pool.terminate()
        pool.join()

                
def process_video(video):
    vid = video["id"]
    if vid["kind"] == "youtube#video":
        url = vid["videoId"]
        # download subtitles for each video, save to output folder
        bashCommand = "youtube-dl -o subtitles/%(uploader)s/%(id)s.%(ext)s --write-auto-sub --skip-download https://www.youtube.com/watch?v={0}".format(url)
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        if not error: 
            print output
        else: 
            print error

if __name__ == '__main__':
    get_channel_videos()