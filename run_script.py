import schedule
import time
from post_image import postInstagramImage

# Define the function to be scheduled
def run_script():
    postInstagramImage("gloaming")

# schedule the post_image function to run every hour for 25 hours
for i in range(25):
    schedule.every(i+1).hours.do(run_script)

while True:
    # run the scheduled tasks
    schedule.run_pending()

    # wait for 1 second
    time.sleep(1)