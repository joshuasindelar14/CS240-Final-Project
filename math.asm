li $t0, 3
li $t1, 5
add $t3, $t1, $t2
pow $t4, $t0, 2
sqrt $t5, $t3
move $a0, $t4
li $v0, 1
syscall
li $v0, 11
li $a0, 10
syscall
move $a0, $t5
li $v0, 1
syscall
li $v0, 11
li $a0, 10
syscall
