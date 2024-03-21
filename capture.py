import time
import datetime
import os
import subprocess
import logging
import timelapseconfig

# prepare the output folder
write_path = timelapseconfig.output_dir + datetime.datetime.today().strftime(timelapseconfig.daily_foldername_date_formatstring)
if not os.path.exists(write_path):
    os.makedirs(write_path)

time.sleep(10)
print ("Starting capture")
starttime = datetime.datetime.now().timestamp()
failed = 0
succeeded = 0
while datetime.datetime.now().timestamp() < starttime + timelapseconfig.cronjob_repeat_time:
    cycle_starttime = datetime.datetime.now().timestamp()
    file_name = write_path + "/" + str(int(datetime.datetime.now().timestamp())) + ".png"
    print(file_name)
    logging.info(f"Capturing image {succeeded + failed + 1}...")
    res = subprocess.call(
        f"ffmpeg -y -loglevel fatal -rtsp_transport tcp -i {timelapseconfig.rtsp_url} -frames:v 1 {file_name}",
        shell=True,
    )
    if res == 0:
        succeeded += 1
    else:
        failed += 1
    end = time.time()    
    logging.info(f"Succeeded: {succeeded}, failed: {failed}")
    #camera.video_take_snapshot(0,file_name,1920,1080)

    while datetime.datetime.now().timestamp() < cycle_starttime + timelapseconfig.delay_between_images:
        time.sleep(0.1)
