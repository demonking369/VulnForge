section .text
global calculate_offset

; Simple function to add two integers (rdi + rsi)
; Used to demonstrate calling assembly from Python
calculate_offset:
    mov rax, rdi    ; Move the first parameter (x) into rax
    add rax, rsi    ; Add the second parameter (offset) to rax
    ret             ; Return the result (in rax) 