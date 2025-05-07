li $t0, 1
li $t5, 100

loop:
mod $t1, $t0, 15
beq $t1, $zero, fizzbuzz

mod $t1, $t0, 3
beq $t1, $zero, fizz

mod $t1, $t0, 5
beq $t1, $zero, buzz

move $a0, $t0
li $v0, 1
syscall
li $v0, 11
li $a0, 10
syscall
j next

fizzbuzz:
li $v0, 4
la $a0, fbstr
syscall
j next

fizz:
li $v0, 4
la $a0, fstr
syscall
j next

buzz:
li $v0, 4
la $a0, bstr
syscall
j next

next:
addi $t0, $t0, 1
ble $t0, $t5, loop
li $v0, 10
syscall

.data
fstr: .asciiz "Fizz\n"
bstr: .asciiz "Buzz\n"
fbstr: .asciiz "FizzBuzz\n"
