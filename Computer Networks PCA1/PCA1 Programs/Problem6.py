# Menu Driven Program to Identify the class of a given IP Address

def identify_ip_class(ip):
    try:
        octets = ip.split('.')

        # Check format
        if len(octets) != 4:
            return "Invalid IP address format!"

        # Validate octets
        for octet in octets:
            if not octet.isdigit() or not 0 <= int(octet) <= 255:
                return "Invalid IP address! Each octet must be between 0 and 255."

        first_octet = int(octets[0])

        # Determine class
        if 1 <= first_octet <= 126:
            return "Class A"
        elif first_octet == 127:
            return "Reserved for Loopback (Not a valid class)"
        elif 128 <= first_octet <= 191:
            return "Class B"
        elif 192 <= first_octet <= 223:
            return "Class C"
        elif 224 <= first_octet <= 239:
            return "Class D (Multicast)"
        elif 240 <= first_octet <= 255:
            return "Class E (Experimental)"
        else:
            return "Invalid IP address!"

    except:
        return "Invalid IP address! Please enter correctly."


# ------------------ MAIN MENU ------------------

while True:
    print("\n===== IP ADDRESS CLASS IDENTIFIER =====")
    print("1. Identify Class of an IP Address")
    print("2. Exit")

    choice = input("Enter your choice (1-2): ")

    if choice == '1':
        ip_address = input("Enter IP address in dotted decimal format: ")
        result = identify_ip_class(ip_address)
        print("Result:", result)

    elif choice == '2':
        print("Exiting Program... Thank You!")
        break

    else:
        print("Invalid choice! Please select 1 or 2.")