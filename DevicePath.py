if 2/3==0: input = raw_input

def get_path(prior_path):
    new_path = []
    for x in prior_path.split("#"):
        if x.lower().startswith("pciroot("):
            try: val = hex(int(x.split("(")[1].split(")")[0],16))[2:].upper()
            except Exception as e:
                print(e)
                continue
            new_path.append("PciRoot(0x{})".format(val))
        elif x.lower().startswith("pci("):
            try:
                vals = x.split("(")[1].split(")")[0]
                val1,val2 = hex(int(vals[:2],16)).upper()[2:],hex(int(vals[2:],16)).upper()[2:]
            except Exception as e:
                print(e)
                continue
            new_path.append("Pci(0x{},0x{})".format(val1,val2))
    return "/".join(new_path)

def main():
    while True:
        device_path = input("Please enter a Windows device path:  ")
        if not len(device_path): continue
        if device_path.lower() == "q": exit()
        new_path = get_path(device_path)
        if not new_path:
            print("Not properly formatted!")
            continue
        print("{} => {}".format(device_path,new_path))

main()