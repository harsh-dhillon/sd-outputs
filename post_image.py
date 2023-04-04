import hashlib
import hmac
import json
import os
import random

import requests

import config
import get_github_link


def postInstagramImage(folder=None):
    # Get the Image
    image_location, folder = get_github_link.get_file_urls()

    if image_location:
        appsecret_proof = hmac.new(
            config.APP_SECRET.encode('utf-8'),
            msg=config.USER_ACCESS_TOKEN.encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()

        post_url = f'https://graph.facebook.com/v10.0/17841407988148701/media?&appsecret_proof={appsecret_proof}'

        # Read hashtags from file
        hardcoded_hashtags = [
            '#aiartcommunity', '#galleryart', '#wallart', '#torontoartist', '#artoftheday', '#art_dailydose', '#art_viral',
            '#aiart', '#art', '#beautiful', '#artwork', '#artgallery', '#graphicdesign', '#artlovers', '#artistic', '#artofvisuals'
            '#midjourney', '#stablediffusion', '#painting', '#artistoninstagram'
        ]

        # Get hashtags from folder
        hashtags_file = os.path.join(folder, 'hashtags.txt')
        if os.path.exists(hashtags_file):
            with open(hashtags_file, 'r') as f:
                all_hashtags = f.read().strip().split(',')
        else:
            all_hashtags = []

        all_hashtags = [h.strip() for h in all_hashtags]

        # Use 10 hardcoded hashtags and randomly select up to 10 more from folder
        remaining_hashtags = list(set(all_hashtags) - set(hardcoded_hashtags))
        num_selected = min(len(remaining_hashtags), 10)
        selected_hashtags = random.sample(remaining_hashtags, k=num_selected) + hardcoded_hashtags

        # Shuffle the hashtags randomly
        random.shuffle(selected_hashtags)

        # Add hashtags to the caption, limiting the total number to 29
        hashtag_string = ' '.join(selected_hashtags[:30])

        # Generate the caption with folder name and count
        folder_title = ' '.join([word.capitalize() for word in folder.split('_')]).replace('_', '')
        log_file_name = os.path.basename(folder) + '_file_log.txt'
        log_file_path = os.path.join(folder, log_file_name)
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as f:
                count = len(f.readlines())
            caption = f"{folder_title}, W.{count} \n-\n-\n-\n-\n-\n-\n{hashtag_string}".title()
        else:
            with open(log_file_path, 'r') as f:
                count = len(f.readlines())
            caption = f"Diffusion Art, W.{count} \n-\n-\n-\n-\n-\n-\n{hashtag_string}".title()

        payload = {
            'image_url': image_location,
            'caption': caption,
            'access_token': config.USER_ACCESS_TOKEN
        }

        r = requests.post(post_url, data=payload)

        result = json.loads(r.text)

        if 'id' in result:
            creation_id = result['id']
            second_url = f'https://graph.facebook.com/v10.0/17841407988148701/media_publish?&appsecret_proof={appsecret_proof}'
            second_payload = {
                'creation_id': creation_id,
                'access_token': config.USER_ACCESS_TOKEN
            }

            r = requests.post(second_url, data=second_payload)
            print(r.text)
        else:
            print(r.text)
