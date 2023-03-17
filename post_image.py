import hashlib
import hmac
import json
import os
import random

import requests

import config
import get_github_link


def postInstagramImage(folder=""):
    # Get the Image
    image_location = get_github_link.get_file_urls(folder)

    if folder == "":
        folder = "diffusion_art"

    if image_location:
        appsecret_proof = hmac.new(
            config.APP_SECRET.encode('utf-8'),
            msg=config.USER_ACCESS_TOKEN.encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()

        post_url = f'https://graph.facebook.com/v10.0/17841407988148701/media?&appsecret_proof={appsecret_proof}'

        # Read hashtags from file
        if folder != "diffusion_art":
            hardcoded_hashtags = ['#art', '#landscapeart', '#vangogh', '#monet', '#manet', '#cezanne',
                                  '#stablediffusion', '#midjourney', '#ai', '#aiart', '#artist', '#artoftheday',
                                  '#artoninstagram', '#artscape', '#galleryart', '#famousart', '#artcollector',
                                  '#artcollective', '#oilpainting']
            with open(os.path.join(config.ROOT_FOLDER, 'hashtags.txt'), 'r') as f:
                all_hashtags = f.read().strip().split(',')
                all_hashtags = [h.strip() for h in all_hashtags]
                remaining_hashtags = list(set(all_hashtags) - set(hardcoded_hashtags))

            if len(remaining_hashtags) >= 10:
                selected_hashtags = random.sample(hardcoded_hashtags, k=20) + random.sample(remaining_hashtags, k=10)
            else:
                selected_hashtags = hardcoded_hashtags + remaining_hashtags

        else:
            with open(os.path.join(folder, 'hashtags.txt'), 'r') as f:
                all_hashtags = f.read().strip().split(',')
                all_hashtags = [h.strip() for h in all_hashtags]
                selected_hashtags = random.sample(all_hashtags, k=min(len(all_hashtags), 30))

        # Add hashtags to the caption
        hashtag_string = ' '.join(selected_hashtags)

        # Generate the caption with folder name and count
        folder_title = ' '.join([word.capitalize() for word in folder.split('_')]).replace('_', '')
        log_file_name = os.path.basename(folder) + '_file_log.txt'
        log_file_path = os.path.join(folder, log_file_name)
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as f:
                count = len(f.readlines())
            caption = f"{folder_title} Series, W.{count} \n-\n-\n-\n-\n-\n-\n{hashtag_string}"
        else:
            with open(log_file_path, 'r') as f:
                count = len(f.readlines())
            caption = f"Diffusion Art {count} \n-\n-\n-\n-\n-\n-\n{hashtag_string}"

        payload = {
            'image_url': image_location,
            'caption': caption,
            'access_token': config.USER_ACCESS_TOKEN
        }

        r = requests.post(post_url, data=payload)
        print(r.text)

        result = json.loads(r.text)

        if 'id' in result:
            creation_id = result['id']
            second_url = f'https://graph.facebook.com/v10.0/17841407988148701/media_publish?&appsecret_proof={appsecret_proof}'
            second_payload = {
                'creation_id': creation_id,
                'access_token': config.USER_ACCESS_TOKEN
            }

            r = requests.post(second_url, data=second_payload)
        else:
            print('Error')
