from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from time import *
import os,hashlib

"""
ECB没有偏移量
"""
begin_time = time()

#密钥K的生成
user_code = 'cehuixueyuan2020'
sha = hashlib.md5()
sha.update(user_code.encode('utf-8'))
hash_key = sha.hexdigest()
value_list = [int(i,16) for i in list(hash_key)]

def add_to_16(text):
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')

key = hash_key.encode('utf-8')

''' 从txt中获取数据需要的x,y值'''
os.chdir(r'E:\Digital watermarking experience\Experiment data')
txt_str,coor_str,coor_float,ox,oy = [],[],[],[],[]
fn = open('ori_station_coor.txt','r',encoding='utf-8')
fn_r = fn.readlines()
for i in fn_r:
    txt_str.append(i)
fn.close()
for m in range(0,len(txt_str)):
    coor_str.append(txt_str[m].replace(' ',',').split(','))

for n in coor_str:
    d = []
    for t in n:
        d.append(float(t))
    coor_float.append(d)
    ox.append(d[::2])
    oy.append(d[1::2])

Xstr,Ystr = [],[]
Xtext,Ytext = [],[]
cipher_Xtext,cipher_Ytext = [],[]
plain_Xtext,plain_Ytext = [],[]
plain_Xfloat,plain_Yfloat = [],[]
mode = AES.MODE_ECB
cryptos = AES.new(key, mode)
M,Write_txt = [],[]

for i in range(len(ox)):
    xstr,ystr = [],[]
    for j in range(len(ox[i])):
        xstr.append(str(ox[i][j]))
        ystr.append(str(oy[i][j]))
    Xstr.append(xstr), Ystr.append(ystr)

# 加密函数

    xtext,ytext = [],[]
    for j in range(len(Xstr[i])):
        xtext.append(add_to_16(Xstr[i][j]))
        ytext.append(add_to_16(Ystr[i][j]))
    Xtext.append(xtext), Ytext.append(ytext)


    m = []
    cipher_xtext,cipher_ytext = [],[]
    for j in range(len(Xtext[i])):
        cipher_xtext.append(b2a_hex(cryptos.encrypt(Xtext[i][j])))
        cipher_ytext.append(b2a_hex(cryptos.encrypt(Ytext[i][j])))
        m.append([cipher_xtext, cipher_ytext])
    cipher_Xtext.append(cipher_xtext), cipher_Ytext.append(cipher_ytext)
    M.append(m)

print(cipher_Xtext[-1])
print(cipher_Ytext[-1])

end_time = time()
run_time = end_time - begin_time
print('加密时间：',run_time)
# 0.0027591249999998624

mode = AES.MODE_ECB
cryptor = AES.new(key, mode)
# 解密后，去掉补足的空格用strip() 去掉
for i in range(len(cipher_Xtext)):
    plain_xtext,plain_ytext = [],[]
    for j in range(len(cipher_Xtext[i])):
        xplain = cryptor.decrypt(a2b_hex(cipher_Xtext[i][j]))
        yplain = cryptor.decrypt(a2b_hex(cipher_Ytext[i][j]))
        plain_xtext.append(bytes.decode(xplain).rstrip('\0'))
        plain_ytext.append(bytes.decode(yplain).rstrip('\0'))
    plain_Xtext.append(plain_xtext), plain_Ytext.append(plain_ytext)

    plain_xfloat,plain_yfloat = [],[]
    for f in range(len(plain_Xtext[i])):
        str_xfloat = float(plain_Xtext[i][f])
        str_yfloat = float(plain_Ytext[i][f])
        plain_xfloat.append(str_xfloat), plain_yfloat.append(str_yfloat)
    plain_Xfloat.append(plain_xfloat), plain_Yfloat.append(plain_yfloat)


E_x,E_y =[],[]
Xmax,Xmin,Ymax,Ymin = [],[],[],[]
for i in range(len(ox)):
    e_x,e_y = [],[]
    for j in range(len(ox[i])):
        errorx = abs(plain_Xfloat[i][j] - ox[i][j])
        errory = abs(plain_Yfloat[i][j] - oy[i][j])
        e_x.append(errorx), e_y.append(errory)
    xmax = max(e_x)
    ymax = max(e_y)
    Xmax.append(xmax),Ymax.append(ymax)
    xmin = min(e_x)
    yxin = min(e_y)
    Xmin.append(xmin),Ymin.append(yxin)
    E_x.append(e_x), E_y.append(e_y)
XMAX = max(Xmax)
XMIN = min(Xmin)
YMAX = max(Ymax)
YMIN = min(Ymin)

all_max = max(XMAX,YMAX)
all_min = min(XMIN,YMIN)

print(all_max,all_min)


