.syntax unified
.thumb
.section .text.boot
.globl _start
.thumb_func

_start:
    push {r4, r5, r6, r7, lr}
    add r7, sp, #12

    /* Call payload main function */
    bl main

    /* Return cleanly to iBoot command prompt with status 0 */
    movs r0, #0
    pop {r4, r5, r6, r7, pc}
