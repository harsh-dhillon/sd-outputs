import schedule
import time
from datetime import datetime, timedelta
from post_image import postInstagramImage


# Define the function to be scheduled
def run_script():
    postInstagramImage("Azure_Dreamscapes")

# Schedule the first job at 7:30 AM
schedule.every().day.at("07:30").do(run_script)

# Schedule subsequent jobs every hour from 7:30 AM to 8:30 PM
next_hour = datetime.strptime("07:30", "%H:%M") + timedelta(hours=1)
while next_hour.strftime("%H:%M") <= "20:30":
    schedule.every().day.at(next_hour.strftime("%H:%M")).do(run_script)
    next_hour += timedelta(hours=1)

while True:
    schedule.run_pending()
    time.sleep(60)
