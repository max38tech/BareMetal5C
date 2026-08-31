ENTRY(_start)

SECTIONS
{
    . = 0x80000030;

    .text : {
        *(.text.boot)
        *(.text*)
    }

    .rodata : {
        *(.rodata*)
    }

    .data : {
        *(.data*)
    }

    .bss : {
        __bss_start = .;
        *(.bss*)
        *(COMMON)
        __bss_end = .;
    }

    . = ALIGN(16);
    _stack_bottom = .;
    . = . + 0x10000; /* 64KB stack */
    _stack_top = .;
}
