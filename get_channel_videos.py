import click
import requests
import json
import jsonlines
import os

@click.command()
@click.option('--channel-filename', default='channels.txt', help='Input file containing channels to scrape.')
@click.option('--output-folder', default='output', help='Output folder to put video list files.')
@click.option('--yt-api-key', prompt='Your Youtube API key is required.',
              help='A Youtube API Key to enumerate Channel Videos.')
def get_channel_videos(channel_filename, output_folder, yt_api_key):
    """CLI tool to help enumerate all the videos belonging to one or more channels"""
    # Channel File Schema: 
    # { name: string, id: string}
    with open(channel_filename, 'r') as channel_file:
        # Setup Output Folder
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        # Iterate over List of Channels
        for line in channel_file:
            channel = json.loads(line.strip())
            channel_name = channel["name"]
            channel_id = channel["id"]

            # Get First Response
            # NOTE: This sorts by viewcount but that doesn't have to be the case. 
            url = "https://www.googleapis.com/youtube/v3/search?key={0}&channelId={1}&part=snippet,id&order=viewcount&maxResults=50".format(yt_api_key, channel_id)
            resp = requests.get(url)

            if resp.status_code == 403:
                print "Something went wrong while processing {0}... You might have exceeded the Youtube Quota.".format(channel_name)
                print "JSON BODY: "
                print resp.json()
                break

            json_resp = resp.json()
            next_page = json_resp["nextPageToken"]

             # Write the First Page of items
            for item in items:
                try: 
                    writer.write(item)
                except UnicodeEncodeError: 
                    pass

            # Setup output file 
            outfile_filename = "{0}.json".format(channel_name.replace(" ", "_"))
            outfile = open(output_folder + "/" + outfile_filename, "w")
            writer = jsonlines.Writer(outfile)

            while True: 
                # Generate List of all Videos in Channel 
                    
                url = "https://www.googleapis.com/youtube/v3/search?key={0}&channelId={1}&part=snippet,id&order=date&maxResults=50&pageToken={2}".format(yt_api_key, channel_id, next_page)

                # Get a page of the list
                resp = requests.get(url)
                # Decode JSON 
                json_resp = resp.json()
                # Get the Items
                try: 
                    items = json_resp["items"]
                except KeyError: 
                    print "Something is wrong... You might have exceeded the Youtube Quota."
                    print resp.json()
                    break

                # Write the current Items
                for item in items:
                    try: 
                        writer.write(item)
                    except UnicodeEncodeError: 
                        continue
                
                #check if there's another page, otherwise break
                try: 
                    next_page = json_resp["nextPageToken"]
                except KeyError: 
                    break
                



            # Download English Subtitles for each video 

if __name__ == '__main__':
    get_channel_videos()