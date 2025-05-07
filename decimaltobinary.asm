    .text
    .globl main

main:
    # Initialize the input number (for example, 29)
    li $t0, 29        # $t0 = 29 (decimal number to convert)
    li $t1, 2         # $t1 = 2 (target base, binary)
    li $t2, 0         # $t2 = 0 (counter for binary digit storage)
    li $t3, 0         # $t3 = 0 (register for the remainder)

convert_loop:
    mod $t3, $t0, $t1
    addi $a0, $t3, 48
    li $v0, 11
    syscall


    div $t0, $t0, $t1
    mflo $t0

    bnez $t0, convert_loop

    li $v0, 10
    syscall
