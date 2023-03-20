import schedule
import time
from post_image import postInstagramImage

# Define the function to be scheduled
def run_script():
    postInstagramImage("Chroma_Portraits")

# schedule the post_image function to run every 1 hour
schedule.every(1).hour.do(run_script)

while True:
    # run the scheduled tasks
    schedule.run_pending()

    # wait for 1 second
    time.sleep(1)