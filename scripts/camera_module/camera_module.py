from argparse import ArgumentParser
from picamera import PiCamera
from time import sleep
from pathlib import Path
import os


if __name__ == '__main__':

    parser = ArgumentParser()

    parser.add_argument('--resolution',
                        dest='res',
                        default='1920-1080',
                        help='Supported resolutions: 1920-1080, 3280-2464, 1640-1232, 1640-922, 1280-720, 640-480')

    parser.add_argument('--output',
                        dest='out_folder',
                        default='/camera_output/continuous_captures/',
                        help='Location to store captured photos.')

    parser.add_argument('--interval',
                        dest='interval',
                        default=10,
                        help='Time interval between capture. Default value is 10 seconds.')

    parser.add_argument('--iso',
                        dest='iso',
                        default=100,
                        help='Camera ISO value. Default value is 100')

    # parse command line arguments
    args = parser.parse_args()

    # parse resolution
    res = args.res.split('-')
    res_width = int(res[0])
    res_height = int(res[1])

    # parse output location
    output_folder = args.out_folder

    # parse time interval
    interval = int(args.interval)

    # parse Camera ISO
    iso = int(args.iso)

    # initialize camera
    camera = PiCamera()
    camera_wakeup = camera_cooldown = 2

    # set camera resolution
    camera.resolution = (res_width, res_height)

    # set camera ISO
    camera.iso = iso

    # wait for automatic gain control to settle
    sleep(camera_wakeup)

    # set output folder
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    os.chdir(output_folder)

    camera.start_preview()
    sleep(camera_wakeup)
    
    while True:
        for filename in camera.capture_continuous('img{timestamp:%Y-%m-%d-%H-%M-%S}.jpg'):
            camera.start_preview()
            sleep(camera_wakeup)
            print('image captured... %s' % filename)
            sleep(camera_cooldown)
            camera.stop_preview()
            sleep(interval - camera_wakeup - camera_cooldown)
