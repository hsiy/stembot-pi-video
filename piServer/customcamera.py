import picamera
import io
from threading import Thread


class CameraDefaults:
    CAMERA_RESOLUTION_DEFAULT = "720p"
    CAMERA_FRAME_RATE_DEFAULT = 30
    CAMERA_H_FLIP_DEFAULT = False
    CAMERA_V_FLIP_DEFAULT = False
    CAMERA_ROTATION_DEFAULT = 0
    CAMERA_ISO_DEFAULT = 0
    CAMERA_BRIGHTNESS_DEFAULT = 50
    CAMERA_CONTRAST_DEFAULT = 0
    CAMERA_SATURATION_DEFAULT = 0
    CAMERA_STABILIZATION_DEFAULT = False
    OTHER_DEBUG = False


def get_valid_debug():
    """
    Static method that defines list of valid debug values
    :return: list of valid debug values
    """
    # check if need to change to range 0-1600 from docs
    return [True, False]

def get_valid_resolutions():
    """
    Static method that defines list of valid resolutions
    :return: list of valid resolutions
    """
    return ["720p", "480p", "360p", "240p"]


def get_valid_frame_rate():
    """
    Static method that defines list of valid frame rates
    :return: list of valid frame rates
    """
    return [*range(5, 91, 5)]


def get_valid_hflip():
    """
    Static method that defines list of valid h-flip value
    :return: list of valid h-flip values
    """
    return [True, False]


def get_valid_vflip():
    """
    Static method that defines list of valid v-flip value
    :return: list of valid v-flip values
    """
    return [True, False]


def get_valid_rotation():
    """
    Static method that defines list of valid rotation values
    :return: list of valid rotation values
    """
    # check if need to change to range 0-1600 from docs
    return [0, 90, 180, 270]


def get_valid_iso():
    """
    Static method that defines list of valid iso values
    :return: list of valid iso values
    """
    # check if need to change to range 0-1600 from docs
    return [0, 100, 200, 320, 400, 500, 640, 800]


def get_valid_brightness():
    """
    Static method that defines list of valid brightness values
    :return: list of valid brightness values
    """
    # check if need to change to range 0-1600 from docs
    return [*range(0, 101, 1)]


def get_valid_contrast():
    """
    Static method that defines list of valid contrast values
    :return: list of valid contrast values
    """
    # check if need to change to range 0-1600 from docs
    return [*range(-100, 101, 1)]


def get_valid_saturation():
    """
    Static method that defines list of valid saturation values
    :return: list of valid saturation values
    """
    # check if need to change to range 0-1600 from docs
    return [*range(-100, 101, 1)]


def get_valid_stabilization():
    """
    Static method that defines list of valid stabilization values
    :return: list of valid stabilization values
    """
    # check if need to change to range 0-1600 from docs
    return [True, False]


class CustomCamera:
    __camera_dictionary = dict()
    __camera = picamera.PiCamera()
    __raw_data = io.BytesIO()

    def __init__(self, args):
        self.initialize_dictionary()
        self.set_debug(args["debug"])
        self.set_resolution(args["resolution"])
        self.set_frame_rate(args["framerate"])
        self.set_hflip(args["hflip"])
        self.set_vflip(args["vflip"])
        self.set_rotation(args["rotation"])
        self.set_iso(args["iso"])
        self.set_brightness(args["brightness"])
        self.set_contrast(args["contrast"])
        self.set_saturation(args["saturation"])
        self.set_stabilization(args["stabilization"])
        self.__stream = self.__camera.capture_continuous(self.__raw_data, format="jpeg", use_video_port=True)
        self.__frame = None
        self.__stopped = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        self.__camera.close()
        self.__raw_data.close()

    def initialize_dictionary(self):
        self.__camera_dictionary["resolution"] = CameraDefaults.CAMERA_RESOLUTION_DEFAULT
        self.__camera_dictionary["framerate"] = CameraDefaults.CAMERA_FRAME_RATE_DEFAULT
        self.__camera_dictionary["hflip"] = CameraDefaults.CAMERA_H_FLIP_DEFAULT
        self.__camera_dictionary["vflip"] = CameraDefaults.CAMERA_V_FLIP_DEFAULT
        self.__camera_dictionary["rotation"] = CameraDefaults.CAMERA_ROTATION_DEFAULT
        self.__camera_dictionary["iso"] = CameraDefaults.CAMERA_ISO_DEFAULT
        self.__camera_dictionary["brightness"] = CameraDefaults.CAMERA_BRIGHTNESS_DEFAULT
        self.__camera_dictionary["contrast"] = CameraDefaults.CAMERA_CONTRAST_DEFAULT
        self.__camera_dictionary["saturation"] = CameraDefaults.CAMERA_SATURATION_DEFAULT
        self.__camera_dictionary["stabilization"] = CameraDefaults.CAMERA_STABILIZATION_DEFAULT
        self.__camera_dictionary["debug"] = CameraDefaults.OTHER_DEBUG

    def get_frame(self):
        """
        Returns the frame byte data of the current frame
        :return: self.__frame
        """
        return self.__frame

    def is_stopped(self):
        """
        Returns the frame byte data of the current frame
        :return: !self.__stopped
        """
        return not self.__stopped

    def start(self):
        """
        Starts up the thread to read frames from the pi video stream
        :return: self
        """
        Thread(target=self.update, args=()).start()
        self.__stopped = False
        return self

    def stop(self):
        """
        Stops the current video stream
        :return: self
        """
        self.__stopped = True
        return self
    
    def update(self):
        """
        Returns the camera object from the picamera module
        :return: self
        """
        for f in self.__stream:
            self.__frame = f.getvalue()
            self.__raw_data.seek(0)
            if self.__stopped:
                self.__stream.close()
                break
        return self

    def get_camera(self):
        """
        Returns the camera object from the picamera module
        :return: self.__camera
        """
        return self.__camera

    def get_camera_dictionary(self):
        """
        Returns the camera object from the picamera module
        :return: self.__camera
        """
        return self.__camera_dictionary

    def set_resolution(self, resolution):
        """
        Setting the resolution value of the CustomCamera class
        :param resolution: The resolution value we are trying to set
        """
        if resolution == self.get_resolution():
            return
        for val in get_valid_resolutions():
            if resolution == val:
                self.__camera_dictionary["resolution"] = resolution
                self.__camera.resolution = resolution
                return
        if self.get_debug():
            print("Error: Invalid Resolution Value")

    def get_resolution(self):
        """
        Returns the resolution of that is stored
        :return: the resolution value
        """
        return self.__camera_dictionary["resolution"]

    def set_frame_rate(self, framerate):
        """
        Setting the framerate value of the CustomCamera class
        :param framerate: The framerate value we are trying to set
        """
        if framerate == self.get_frame_rate():
            return
        for val in get_valid_frame_rate():
            if framerate == val:
                self.__camera_dictionary["framerate"] = framerate
                self.__camera.framerate = framerate
                return
        if self.get_debug():
            print("Error: Invalid Framerate Value")

    def get_frame_rate(self):
        """
        Returns the value of the current framerate value
        :return: the framerate value
        """
        return self.__camera_dictionary["framerate"]

    def set_hflip(self, hflip):
        """
        Setting the hflip value of the CustomCamera class
        :param hflip: The hflip value we are trying to set
        """
        if hflip == self.get_hflip():
            return
        for val in get_valid_hflip():
            if hflip == val:
                self.__camera_dictionary["hflip"] = hflip
                self.__camera.hflip = hflip
                return
        if self.get_debug():
            print("Error: Invalid hflip Value")

    def get_hflip(self):
        """
        Returns the value of the current stabilization value
        :return: the stabilization value
        """
        return self.__camera_dictionary["hflip"]

    def set_vflip(self, vflip):
        """
        Setting the vflip value of the CustomCamera class
        :param vflip: The vflip value we are trying to set
        """
        if vflip == self.get_vflip():
            return
        for val in get_valid_vflip():
            if vflip == val:
                self.__camera_dictionary["vflip"] = vflip
                self.__camera.vflip = vflip
                return
        if self.get_debug():
            print("Error: Invalid vflip Value")

    def get_vflip(self):
        """
        Returns the value of the current stabilization value
        :return: the stabilization value
        """
        return self.__camera_dictionary["vflip"]

    def set_rotation(self, rotation):
        """
        Setting the rotation value of the CustomCamera class
        :param rotation: The rotation value we are trying to set
        """
        if rotation == self.get_rotation():
            return
        for val in get_valid_rotation():
            if rotation == val:
                self.__camera_dictionary["rotation"] = rotation
                self.__camera.rotation = rotation
                return
        if self.get_debug():
            print("Error: Invalid Rotation Value")

    def get_rotation(self):
        """
        Returns the value of the current rotation value
        :return: the rotation value
        """
        return self.__camera_dictionary["rotation"]

    def set_iso(self, iso):
        """
        Setting the iso value of the CustomCamera class
        :param iso: The iso value we are trying to set
        """
        if iso == self.get_iso():
            return
        for val in get_valid_stabilization():
            if iso == val:
                self.__camera_dictionary["iso"] = iso
                self.__camera.iso = iso
                return
        if self.get_debug():
            print("Error: Invalid ISO Value")

    def get_iso(self):
        """
        Returns the value of the current iso value
        :return: the iso value
        """
        return self.__camera_dictionary["iso"]

    def set_brightness(self, brightness):
        """
        Setting the brightness value of the CustomCamera class
        :param brightness: The brightness value we are trying to set
        """
        if brightness == self.get_brightness():
            return
        for val in get_valid_stabilization():
            if brightness == val:
                self.__camera_dictionary["brightness"] = brightness
                self.__camera.brightness = brightness
                return
        if self.get_debug():
            print("Error: Invalid Brightness Value")

    def get_brightness(self):
        """
        Returns the value of the current brightness value
        :return: the brightness value
        """
        return self.__camera_dictionary["brightness"]

    def set_contrast(self, contrast):
        """
        Setting the contrast value of the CustomCamera class
        :param contrast: The contrast value we are trying to set
        """
        if contrast == self.get_contrast():
            return
        for val in get_valid_stabilization():
            if contrast == val:
                self.__camera_dictionary["contrast"] = contrast
                self.__camera.contrast = contrast
                return
        if self.get_debug():
            print("Error: Invalid Contrast Value")

    def get_contrast(self):
        """
        Returns the value of the current contrast value
        :return: the contrast value
        """
        return self.__camera_dictionary["contrast"]

    def set_saturation(self, saturation):
        """
        Setting the saturation value of the CustomCamera class
        :param saturation: The saturation value we are trying to set
        """
        if saturation == self.get_saturation():
            return
        for val in get_valid_stabilization():
            if saturation == val:
                self.__camera_dictionary["saturation"] = saturation
                self.__camera.saturation = saturation
                return
        if self.get_debug():
            print("Error: Invalid Saturation Value")

    def get_saturation(self):
        """
        Returns the value of the current saturation value
        :return: the saturation value
        """
        return self.__camera_dictionary["saturation"]

    def set_stabilization(self, stabilization):
        """
        Setting the stabilization value of the CustomCamera class
        :param stabilization: The stabilization value we are trying to set
        """
        if stabilization == self.get_stabilization():
            return
        for val in get_valid_stabilization():
            if stabilization == val:
                self.__camera_dictionary["stabilization"] = stabilization
                self.__camera.iso = stabilization
                return
        if self.get_debug():
            print("Error: Invalid Stabilization Value")

    def get_stabilization(self):
        """
        Returns the value of the current iso value
        :return: the iso value
        """
        return self.__camera_dictionary["stabilization"]
    
    def set_debug(self, debug):
        """
        Setting the debug value of the CustomCamera class
        :param debug: The debug value we are trying to set
        """
        if debug == self.get_debug():
            return
        for val in get_valid_debug():
            if debug == val:
                self.__camera_dictionary["debug"] = debug
                return
        if self.get_debug():
            print("Error: Invalid Debug Value")

    def get_debug(self):
        """
        Returns the value of the current debug value
        :return: the debug value
        """
        return self.__camera_dictionary["debug"]
    
    def __str__(self):
        """
        Returns the string representation of the class
        :return: the string representation
        """
        return "Resolution: {}\nFramerate: {}\nhflip: {}\nvflip: {}\nRotation: {}\nISO: {}\nBrightness: {}\nContrast: {}\nSaturation: {}\nStabilization: {}\nDebug: {}\n".format(self.get_resolution(), self.get_frame_rate(), self.get_hflip(), self.get_vflip(), self.get_rotation(), self.get_iso(), self.get_brightness(), self.get_contrast(), self.get_saturation(), self.get_stabilization(), self.get_debug())
