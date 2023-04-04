import time
from post_image import postInstagramImage

# Define the function to be scheduled
def run_script():
    postInstagramImage()

# Run the script every hour
while True:
    run_script()
    time.sleep(3600)  # Sleep for 1 hour (3600 seconds)
