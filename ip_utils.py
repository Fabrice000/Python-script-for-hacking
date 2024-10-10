#!/bin/python
# Fonctions du programmes
def load():
    logo = """
    

\t_______________  _____  _________________       
\t____  _/__  __ \\ __  / / /_  /___(_)__  /_______
\t __  / __  /_/ / _  / / /_  __/_  /__  /__  ___/
\t__/ /  _  ____/  / /_/ / / /_ _  / _  / _(__  ) 
\t/___/  /_/       \\____/  \\__/ /_/  /_/  /____/  \033[1;32;40m@by D4rk C4rl\033[0m

    """
    print(logo)
def check_ip(parts):
    try:
        
        return len(parts) == 4 and all(0 <= int(part) < 256 for part in parts)
    except ValueError:
        print("l'IP contient des caractère invalide!")
        return False 
    except (AttributeError, TypeError):
        return False 


        
def check_slash(ip):
    """
    Fonction pour trouver l'ecriture binaire de l'adresse IP entrer par l'utilisateur et renvoyé le binaire, le masque et la classe de l'adresse IP 
    """
    if "/" in ip:
        # s'il a un "/" on utilise le nombre après comme masque
        ip_bytes = ip.split(".")
        ip_slash = ip_bytes[-1].split("/")[-1]
        ip_bytes[-1] = ip_bytes[-1].split("/")[0]
        if check_ip(ip_bytes):

            ip_binary = []
            for i in ip_bytes:
                ip_binary.append(f"{int(i):08b}")
            first_four_bytes = ip_binary[0][:4]
            if first_four_bytes == "0000" or first_four_bytes == "0111":
                ip_class = "A"
            elif first_four_bytes == "1000":
                ip_class = "B"
            elif first_four_bytes == "1100":
                ip_class = "C"
            elif first_four_bytes == "1110":
                ip_class = "D"
            else :
                ip_class = "E"
            return ip_binary,ip_slash,ip_class
            
        else:
            print("Un octet d'une adresse IP ne peut depasser 255")
            exit(0)

    else:
        # Sinon on accorde un masque par defaut en fonction de la classe
        ip_bytes = ip.split(".")

        if check_ip(ip_bytes):

            ip_binary = []
            for i in ip_bytes:
                ip_binary.append(f"{int(i):08b}")
            first_four_bytes = ip_binary[0][:4]
            if first_four_bytes == "0000" or first_four_bytes == "0111":
                ip_class = "A"
                ip_slash = "8"
            elif first_four_bytes == "1000":
                ip_class = "B"
                ip_slash = "16"
            elif first_four_bytes == "1100":
                ip_class = "C"
                ip_slash = "24"
            elif first_four_bytes == "1110":
                ip_class = "D"
                ip_slash = "4"
            else :
                ip_class = "E"
                ip_slash = "4"
            return ip_binary,ip_slash,ip_class
        else:
            print("Un octet d'une adresse IP ne peut depasser 255")
            exit(0)

def find_network_ip(ip_binary_for_network):
    """
    Fonction qui prend le binaire de l'IP entrer par l'utilisateur et change les bits non figés a 0 pour retourner le binaire l'adresse du reseau 
    """
    for i  in range(int(ip_slash),32):
        ip_binary_for_network[i] = str(0)
    ip_binary_for_mask = ip_binary_for_network.copy()
    ip_binary_for_network = "".join(ip_binary_for_network)
    return ip_binary_for_mask,ip_binary_for_network


def find_broadcast_ip(ip_binary_for_broadcast):
    """
    Fonction qui prend le binaire de l'IP entrer par l'utilisateur et change les bits non figés a 1 pour retourner le binaire l'adresse de diffusion 
    """
    for i  in range(int(ip_slash),32):
        ip_binary_for_broadcast[i] = str(1)
    ip_binary_for_broadcast= "".join(ip_binary_for_broadcast)
    return ip_binary_for_broadcast


def find_network_mask(ip_binary_for_mask):
    """
    Fonction qui prend le binaire de l'IP du reseau  et change les bits figés a 1 pour retourner le binaire le masque du reseau 
    """
    for i  in range(int(ip_slash)):
        ip_binary_for_mask[i] = str(1)
    ip_binary_for_mask = "".join(ip_binary_for_mask)
    return ip_binary_for_mask



def transform_all_to_ip(ip_binary_for_network,ip_binary_for_broadcast,ip_binary_for_mask):
    """
    Fonction qui prend les adresses ip en binaire et les transforment en adresse IP (chaque octet en base 10)
    """

    network_ip = [str(int(ip_binary_for_network[:8],2)),str(int(ip_binary_for_network[8:16],2)),str(int(ip_binary_for_network[16:24],2)),str(int(ip_binary_for_network[24:32],2))]
    broadcast_ip = [str(int(ip_binary_for_broadcast[:8],2)),str(int(ip_binary_for_broadcast[8:16],2)),str(int(ip_binary_for_broadcast[16:24],2)),str(int(ip_binary_for_broadcast[24:32],2))]
    mask_ip = [str(int(ip_binary_for_mask[:8],2)),str(int(ip_binary_for_mask[8:16],2)),str(int(ip_binary_for_mask[16:24],2)),str(int(ip_binary_for_mask[24:32],2))]
    return network_ip,broadcast_ip,mask_ip



load()
user_input = input("Entrer une IP: ex(192.168.1.1/8)\n")


ip_binary,ip_slash,ip_class = check_slash(ip=user_input)

ip_binary_str = list("".join(ip_binary))
ip_binary_for_network = ip_binary_str.copy()
ip_binary_for_broadcast = ip_binary_str.copy()
ip_binary_for_mask,ip_binary_for_network = find_network_ip(ip_binary_for_network)
ip_binary_for_broadcast = find_broadcast_ip(ip_binary_for_broadcast)
ip_binary_for_mask = find_network_mask(ip_binary_for_mask)
addresse,broadcast,mask = transform_all_to_ip(ip_binary_for_network,ip_binary_for_broadcast,ip_binary_for_mask)
# Recherche la première adresse utilisable
first = addresse.copy()
first[-1] = str(int(first[-1])+1)

# Recherche la dernière adresse utilisable
last = broadcast.copy()
last[-1] = str(int(last[-1])-1)
infos = {}

# Enregistre tout dans le dictionnaire du debut
infos['classe'] = ip_class
infos["adresse"] = ".".join(addresse)+f"/{ip_slash}"
infos["broadcast"] = ".".join(broadcast)
infos["première adresse utilisable"] = ".".join(first)
infos["dernière adresse utilisable"] = ".".join(last)
infos["bits du reseau"] = "".join(ip_slash)
infos["bits d'hôtes"] = str(32 - int(ip_slash))
infos["masque"] = ".".join(mask)
for key,value in infos.items():
    print(f"{key}: {value}")