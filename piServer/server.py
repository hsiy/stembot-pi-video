import argparse
import customcamera
import time
import zmq
import picamera
import io

option_parse = argparse.ArgumentParser(description="Set up of Raspberry Pi Camera streaming module")
option_parse.add_argument("--resolution", type=int, default=customcamera.CameraDefaults.CAMERA_RESOLUTION_DEFAULT, help="Set the resolution of the camera", choices=customcamera.get_valid_resolutions())
option_parse.add_argument("--ip", type=str, default=customcamera.CameraDefaults.CAMERA_IP_DEFAULT, help="Set the IP address")
option_parse.add_argument("--port", type=int, default=customcamera.CameraDefaults.CAMERA_PORT_DEFAULT, help="Set the port number")
option_parse.add_argument("--framerate", type=int, default=customcamera.CameraDefaults.CAMERA_FRAMERATE_DEFAULT, help="Set the frame rate", choices=customcamera.get_valid_frame_rate())
option_parse.add_argument("--hflip", type=bool, default=customcamera.CameraDefaults.CAMERA_H_FLIP_DEFAULT, help="Set the h-flip value", choices=customcamera.get_valid_hflip())
option_parse.add_argument("--vflip", type=bool, default=customcamera.CameraDefaults.CAMERA_V_FLIP_DEFAULT, help="Set the v-flip value", choices=customcamera.get_valid_vflip())
option_parse.add_argument("--rotation", type=int, default=customcamera.CameraDefaults.CAMERA_ROTATION_DEFAULT, help="Set the rotation value", choices=customcamera.get_valid_rotation())
option_parse.add_argument("--iso", type=int, default=customcamera.CameraDefaults.CAMERA_ISO_DEFAULT, help="Set the ISO value", choices=customcamera.get_valid_iso())
option_parse.add_argument("--framerate", type=int, default=customcamera.CameraDefaults.CAMERA_FRAMERATE_DEFAULT, help="Set the frame rate", choices=customcamera.get_valid_frame_rate())
option_parse.add_argument("--preview", type=bool, default=customcamera.CameraDefaults.CAMERA_PREVIEW_DEFAULT, help="Shows preview on pi display", choices=customcamera.get_valid_preview())
option_parse.add_argument("--debug", type=bool, default=customcamera.CameraDefaults.OTHER_DEBUG, help="Shows debugging information", choices=customcamera.get_valid_debug())

camera = customcamera.CustomCamera(resolution=option_parse.parse_args().resolution, framerate=option_parse.parse_args().framerate,
                                   hflip=option_parse.parse_args().hflip, vflip=option_parse.parse_args().vflip,
                                   rotation=option_parse.parse_args().rotation, iso=option_parse.parse_args().iso,
                                   brightness=option_parse.parse_args().brightness, contrast=option_parse.parse_args().contrast,
                                   saturation=option_parse.parse_args().saturation, stabilization=option_parse.parse_args().stabilization,
                                   preview=option_parse.parse_args().preview, debug=option_parse.parse_args().debug,
                                   ip=option_parse.parse_args().ip, port=option_parse.parse_args().port)

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
        message = str(stream.getvalue())
        socket.send(stream.getvalue())
        if camera.get_debug:
            print("Sent!\n", count_frame)
        count_frame = (count_frame + 1) % 100
        stream.seek(0)
finally:
    camera.get_camera().close()
    camera.get_camera().stop_preview()
    stream.close()
    socket.close()
