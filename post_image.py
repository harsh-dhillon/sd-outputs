import hashlib
import hmac
import json
import os
import random

import requests

import config
import get_github_link


def postInstagramImage(folder=""):

    if folder == "":
        folder = "diffusion_art"

    # Get the Image
    image_location = get_github_link.get_file_urls(folder)

    if image_location:
        appsecret_proof = hmac.new(
            config.APP_SECRET.encode('utf-8'),
            msg=config.USER_ACCESS_TOKEN.encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()

        post_url = f'https://graph.facebook.com/v10.0/17841407988148701/media?&appsecret_proof={appsecret_proof}'

        # Read hashtags from file
        hardcoded_hashtags = [
            '#art', '#artist', '#artwork', '#portrait', '#artoftheday', '#artistic', '#acrylicpainting', '#artofvisuals',
            '#artistsoninstagram', '#pastels', '#instadaily', '#beautiful',
            '#digitalart', '#illustration', '#oilpainting', '#painting', '#contemporaryart', '#sketch',
            '#stablediffusion', '#fauvism', '#midjourney', '#graphicdesign',
            '#creative', '#artgallery', '#artlovers'
        ]

        if folder != "diffusion_art":
            with open(os.path.join(config.ROOT_FOLDER, 'hashtags.txt'), 'r') as f:
                all_hashtags = f.read().strip().split(',')
        else:
            with open(os.path.join(folder, 'hashtags.txt'), 'r') as f:
                all_hashtags = f.read().strip().split(',')

        all_hashtags = [h.strip() for h in all_hashtags]
        remaining_hashtags = list(set(all_hashtags) - set(hardcoded_hashtags))

        if len(remaining_hashtags) >= 5:
            selected_hashtags = hardcoded_hashtags + random.sample(remaining_hashtags, k=5)
        else:
            selected_hashtags = hardcoded_hashtags + remaining_hashtags

        # Add hashtags to the caption
        hashtag_string = ' '.join(selected_hashtags)

        # Generate the caption with folder name and count
        folder_title = ' '.join([word.capitalize() for word in folder.split('_')]).replace('_', '')
        log_file_name = os.path.basename(folder) + '_file_log.txt'
        log_file_path = os.path.join(folder, log_file_name)
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as f:
                count = len(f.readlines())
            caption = f"{folder_title} Series, W.{count} \n-\n-\n-\n-\n-\n-\n{hashtag_string}".title()
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
            print('Error')
