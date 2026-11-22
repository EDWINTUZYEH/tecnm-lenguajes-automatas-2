    .text
    .globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $16, %rsp
    movl $2, %eax
    movl %eax, -4(%rbp)
    movl $3, %eax
    movl %eax, -8(%rbp)
    movl -4(%rbp), %eax
    pushq %rax
    movl -8(%rbp), %eax
    movl %eax, %r11d
    popq %rcx
    movl %ecx, %eax
    addl %r11d, %eax
    movl %eax, %esi
    leaq .LC0(%rip), %rdi
    movl $0, %eax
    call printf
    movl $0, %eax
    leave
    ret

    .section .rodata
.LC0:
    .string "%d\n"
