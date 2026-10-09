default rel


section .data
    msg db "Hello World!", 13, 10, 0
    len dq 0

    output_handle dq -11

section .bss
    writen resb 1

section .text
    global main
    extern GetStdHandle
    extern WriteFile

main:
    mov rcx, [output_handle]
    sub rsp, 40
    call GetStdHandle
    add rsp, 40

    mov [len], 12

    mov rcx, rax
    lea rdx, [msg]
    mov r8d, [len]
    lea r9, [writen]

    sub rsp, 40
    mov qword [rsp+32], 0
    call WriteFile
    add rsp, 40

    xor eax, eax
    ret

