import argparse
import customcamera
import otherFunctions
import time
import zmq
import picamera
import io

option_parse = argparse.ArgumentParser(description="Set up of Raspberry Pi Camera streaming module")
option_parse.add_argument("--resolution", type=str, default=customcamera.CameraDefaults.CAMERA_RESOLUTION_DEFAULT, help="Set the resolution of the camera", choices=customcamera.get_valid_resolutions())
option_parse.add_argument("--ip", type=str, default=otherFunctions.OtherDefaults.DEFAULT_IP, help="Set the IP address")
option_parse.add_argument("--port", type=int, default=customcamera.CameraDefaults.CAMERA_PORT_DEFAULT, help="Set the port number")
option_parse.add_argument("--framerate", type=int, default=customcamera.CameraDefaults.CAMERA_FRAME_RATE_DEFAULT, help="Set the frame rate", choices=customcamera.get_valid_frame_rate())
option_parse.add_argument("--hflip", type=bool, default=customcamera.CameraDefaults.CAMERA_H_FLIP_DEFAULT, help="Set the h-flip value", choices=customcamera.get_valid_hflip())
option_parse.add_argument("--vflip", type=bool, default=customcamera.CameraDefaults.CAMERA_V_FLIP_DEFAULT, help="Set the v-flip value", choices=customcamera.get_valid_vflip())
option_parse.add_argument("--rotation", type=int, default=customcamera.CameraDefaults.CAMERA_ROTATION_DEFAULT, help="Set the rotation value", choices=customcamera.get_valid_rotation())
option_parse.add_argument("--iso", type=int, default=customcamera.CameraDefaults.CAMERA_ISO_DEFAULT, help="Set the ISO value", choices=customcamera.get_valid_iso())
option_parse.add_argument("--brightness", type=int, default=customcamera.CameraDefaults.CAMERA_BRIGHTNESS_DEFAULT, help="Set the brightness value", choices=customcamera.get_valid_brightness())
option_parse.add_argument("--contrast", type=int, default=customcamera.CameraDefaults.CAMERA_CONTRAST_DEFAULT, help="Set the contrast value", choices=customcamera.get_valid_contrast())
option_parse.add_argument("--saturation", type=int, default=customcamera.CameraDefaults.CAMERA_SATURATION_DEFAULT, help="Set the saturation value", choices=customcamera.get_valid_saturation())
option_parse.add_argument("--stabilization", type=int, default=customcamera.CameraDefaults.CAMERA_STABILIZATION_DEFAULT, help="Set the stabilization value", choices=customcamera.get_valid_stabilization())
option_parse.add_argument("--preview", type=bool, default=customcamera.CameraDefaults.CAMERA_PREVIEW_DEFAULT, help="Shows preview on pi display", choices=customcamera.get_valid_preview())
option_parse.add_argument("--debug", type=bool, default=otherFunctions.OtherDefaults.OTHER_DEBUG, help="Shows debugging information", choices=otherFunctions.get_valid_debug())

camera = customcamera.CustomCamera(resolution=option_parse.parse_args().resolution, framerate=option_parse.parse_args().framerate,
                                   hflip=option_parse.parse_args().hflip, vflip=option_parse.parse_args().vflip,
                                   rotation=option_parse.parse_args().rotation, iso=option_parse.parse_args().iso,
                                   brightness=option_parse.parse_args().brightness, contrast=option_parse.parse_args().contrast,
                                   saturation=option_parse.parse_args().saturation, stabilization=option_parse.parse_args().stabilization,
                                   preview=option_parse.parse_args().preview, port=option_parse.parse_args().port)

other_functions = otherFunctions.OtherFunctions(ip=option_parse.parse_args().ip, debug=option_parse.parse_args().debug)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.set_hwm(1)
socket.bind("tcp://*:" + str(camera.get_camera_port()))

stream = io.BytesIO()
if option_parse.parse_args().preview:
    camera.get_camera().start_preview()

time.sleep(.1)

count_frame = 0
try:
    for frame in camera.get_camera().capture_continuous(stream, format="jpeg", use_video_port=True):
        socket.send(stream.getvalue())
        if other_functions.get_debug:
            print("Sent!\n", count_frame)
        count_frame = (count_frame + 1) % 100
        stream.seek(0)
finally:
    camera.get_camera().close()
    camera.get_camera().stop_preview()
    stream.close()
    socket.close()
