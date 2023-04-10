import re
if 2/3==0: input = raw_input

def hexy(integer,pad_to=0):
        return "0x"+hex(integer)[2:].upper().rjust(pad_to,"0")

def sanitize_device_path(device_path):
        # Walk the device_path, gather the addresses, and rebuild it
        if not device_path.lower().startswith("pciroot("):
            # Not a device path - bail
            return
        # Strip out PciRoot() and Pci() - then split by separators
        adrs = re.split(r"#|\/",device_path.lower().replace("pciroot(","").replace("pci(","").replace(")",""))
        new_path = []
        overflow_path = []
        for i,adr in enumerate(adrs):
            if i == 0:
                # Check for roots
                if "," in adr: return # Broken
                try:
                    adr = int(adr,16)
                    new_path.append("PciRoot({})".format(hexy(adr)))
                    overflow_path.append("PciRoot({})".format(hexy(0 if adr>0xFF else adr)))
                except: return # Broken again :(
            else:
                if "," in adr: # Not Windows formatted
                    try: adr1,adr2 = [int(x,16) for x in adr.split(",")]
                    except: return # REEEEEEEEEE
                else:
                    try:
                        adr = int(adr,16)
                        adr2,adr1 = adr & 0xFF, adr >> 8 & 0xFF
                    except: return # AAAUUUGGGHHHHHHHH
                # Should have adr1 and adr2 - let's add them
                new_path.append("Pci({},{})".format(hexy(adr1),hexy(adr2)))
                overflow_path.append("Pci({},{})".format(
                    hexy(0 if adr1>0xFF else adr1),
                    hexy(0 if adr2>0xFF else adr2)
                ))
        return ("/".join(new_path),"/".join(overflow_path))

def main():
    while True:
        device_path = input("Please enter a Windows device path:  ")
        if not len(device_path): continue
        if device_path.lower() == "q": exit()
        new_path = sanitize_device_path(device_path)
        if not new_path:
            print("Not properly formatted!")
            continue
        if new_path[0] != new_path[1]: # Got an overflow
            print("\nADDRESS OVERFLOWS:\n {}\nWill Be Seen By macOS As:\n {}\n".format(new_path[0],new_path[1]))
        else:
            print("\n {}\n".format(new_path[0]))

main()
