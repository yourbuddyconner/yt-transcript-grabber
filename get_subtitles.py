import click
import requests
import json
import jsonlines
import os
import subprocess

@click.command()
@click.argument('filename', required=1)
@click.option('--output-folder', default='subtitles', help='Output folder to put video list files.')
def get_channel_videos(filename, output_folder):
    """CLI tool to help downloading Subtitles from many Youtube Channels"""
    # Video File Schema: 
    # { name: string, id: string}

    # Open Video File 
    with jsonlines.open(filename) as reader:
        # Iterate over lines
        for video in reader: 
            vid = video["id"]
            if vid["kind"] == "youtube#video":
                url = vid["videoId"]
                # download subtitles for each video, save to output folder
                bashCommand = "youtube-dl -o subtitles/%(uploader)s/%(title)s-%(id)s.%(ext)s --write-auto-sub --skip-download https://www.youtube.com/watch?v={0}".format(url)
                process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
                output, error = process.communicate()
                if not error: 
                    print output
                else: 
                    print error
 #    

if __name__ == '__main__':
    get_channel_videos()