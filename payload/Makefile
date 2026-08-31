CC = clang
LD = ld.lld
OBJCOPY = llvm-objcopy

CFLAGS = -target armv7a-none-eabi -mcpu=cortex-a15 -mthumb -O2 -nostdlib -ffreestanding -Wall -fno-pic -fno-pie
ASFLAGS = -target armv7a-none-eabi -mcpu=cortex-a15 -mthumb -nostdlib

all: payload.bin

start.o: start.s
	$(CC) $(ASFLAGS) -c start.s -o start.o

main.o: main.c font.h
	$(CC) $(CFLAGS) -c main.c -o main.o

font.o: font.c font.h
	$(CC) $(CFLAGS) -c font.c -o font.o

payload.elf: linker.ld start.o main.o font.o
	$(LD) -T linker.ld start.o main.o font.o -o payload.elf

payload.bin: payload.elf
	$(OBJCOPY) -O binary payload.elf payload.bin

clean:
	rm -f *.o *.elf payload.bin
