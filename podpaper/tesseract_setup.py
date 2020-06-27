from distro import id as get_os_name
from platform import win32_ver


#
# Class for storing path to tesseract executable
#
# This is needed for using pytesseract
#
class TesseractSetup:
    def __init__(self):
        os_name = get_os_name()
        windows_version = win32_ver()[0]
        if os_name == "ubuntu":
            self.path_to_tesseract_executable = "resources/tesseract_ubuntu"
        elif windows_version != "":
            self.path_to_tesseract_executable = "resources/tesseract_windows.exe"
        else:
            raise NotImplementedError("OS is not supported.")

