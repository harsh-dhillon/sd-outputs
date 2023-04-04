import schedule
import time
from post_image import postInstagramImage

postInstagramImage("Azure_Dreamscapes")

# Define the function to be scheduled
def run_script():
    postInstagramImage("Azure_Dreamscapes")


start_time = "07:30"
end_time = "20:30"

while True:
    current_time = time.strftime("%H:%M")
    if current_time >= start_time and current_time <= end_time:
        schedule.every().hour.at(":00").do(run_script)
    time.sleep(60)