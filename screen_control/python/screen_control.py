import ctypes
import subprocess
import os
import platform
import json

class ScreenControl:
    """A multi-language, modular screen control system."""
    
    def __init__(self, base_path):
        self.base_path = base_path
        self._load_libraries()

    def _load_libraries(self):
        """Loads the C++, Rust, and Assembly shared libraries."""
        # C++ Library
        self.cpp_lib = ctypes.CDLL(os.path.join(self.base_path, 'cpp/screen.so'))
        self.cpp_lib.move_mouse_cpp.argtypes = [ctypes.c_int, ctypes.c_int]
        self.cpp_lib.click_cpp.argtypes = [ctypes.c_int]

        # Rust Library
        self.rust_lib = ctypes.CDLL(os.path.join( 