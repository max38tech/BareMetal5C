# BareMetal5C

A deep-dive hardware hack to execute a custom bare-metal payload directly on the iPhone 5c (A6 / S5L8950X) processor, completely bypassing iOS and taking full control of the Retina display pipeline.

This project was built as an exploration into turning obsolete Apple hardware into a standalone AI assistant device. While we ultimately pivoted to a jailbroken iOS approach (to easily utilize Wi-Fi/Audio drivers), this repository serves as a testament to exploiting checkm8 to run custom embedded C code directly in the device's RAM with zero operating system.

## Features
- **checkm8 Exploit Delivery:** Exploits the Bootrom via USB DFU mode to bypass signature checks.
- **Custom iBoot Chain:** Uploads and executes patched iBSS and iBEC bootloaders.
- **Direct Framebuffer Access:** Writes directly to the ARGB `0xBF7AA000` scanout buffer to manually draw pixels to the 1136x640 Retina LCD.
- **Img3 Container Packaging:** Wraps raw `.bin` payloads into valid Img3 containers so Apple's `iBEC` `go` command can successfully parse and execute them.
- **Custom Linker Mapping:** Compensates for a 48-byte Img3 header injection by shifting the bare-metal base LMA to `0x80000030`, preventing memory offset bugs in `.rodata` and font arrays.

## How to Use (Tethered)
Due to the read-only nature of the Bootrom, this payload cannot be flashed permanently to the device for untethered boot. It must be injected via USB while the device is in DFU mode.

1. Connect the iPhone 5c via USB and place it into DFU mode (Hold Power + Home for 10s, then release Power and hold Home for 10s).
2. Run the exploit script to put the device into PWNED DFU mode:
   ```bash
   cd scripts
   ./pwn.sh
   ```
3. Compile the payload and boot the patched bootchain:
   ```bash
   ./boot_payload.sh
   ```
4. The device screen will initialize, display the neon-cyan cyberpunk UI, and execute the bare-metal C loop indefinitely.
