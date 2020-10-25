class CameraDefaults:
    CAMERA_RESOLUTION_DEFAULT = "720"
    CAMERA_IP_DEFAULT = "localhost"
    CAMERA_PORT_DEFAULT = 5454
    CAMERA_FRAME_RATE_DEFAULT = 30
    CAMERA_H_FLIP_DEFAULT = False
    CAMERA_V_FLIP_DEFAULT = False
    CAMERA_ROTATION_DEFAULT = 0
    CAMERA_ISO_DEFAULT = 0
    CAMERA_BRIGHTNESS_DEFAULT = 50
    CAMERA_CONTRAST_DEFAULT = 0
    CAMERA_SATURATION_DEFAULT = 0
    CAMERA_STABILIZATION_DEFAULT = False


def get_valid_resolutions():
    """
    Static method that defines list of valid resolutions
    :return: list of valid resolutions
    """
    return ["720", "480", "360"]


def get_valid_frame_rate():
    """
    Static method that defines list of valid frame rates
    :return: list of valid frame rates
    """
    return [range(5, 91, 5)]


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
    return [range(0, 101, 1)]


def get_valid_contrast():
    """
    Static method that defines list of valid contrast values
    :return: list of valid contrast values
    """
    # check if need to change to range 0-1600 from docs
    return [range(-100, 101, 1)]


def get_valid_saturation():
    """
    Static method that defines list of valid saturation values
    :return: list of valid saturation values
    """
    # check if need to change to range 0-1600 from docs
    return [range(-100, 101, 1)]


def get_valid_stabilization():
    """
    Static method that defines list of valid stabilization values
    :return: list of valid stabilization values
    """
    # check if need to change to range 0-1600 from docs
    return [True, False]
