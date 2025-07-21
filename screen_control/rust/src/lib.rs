use enigo::{Enigo, MouseControllable, KeyboardControllable, MouseButton};
use std::ffi::CStr;
use std::os::raw::c_char;

/// Types text using the native keyboard.
#[no_mangle]
pub extern "C" fn type_text_rust(text: *const c_char) {
    if text.is_null() { return; }
    let c_str = unsafe { CStr::from_ptr(text) };
    let text_str = match c_str.to_str() {
        Ok(s) => s,
        Err(_) => return,
    };
    
    let mut enigo = Enigo::new();
    enigo.key_sequence(text_str);
}

/// Scrolls the mouse wheel up or down.
#[no_mangle]
pub extern "C" fn scroll_rust(direction: i32) {
    let mut enigo = Enigo::new();
    // Positive for down, negative for up
    enigo.mouse_scroll_y(direction);
} 