import numpy as np

# ฟังก์ชันคำนวณค่าโมดูลาร์อินเวิร์สของตัวเลขภายใต้ mod 256
def mod_inverse(a, mod=256):
    a = a % mod
    for x in range(1, mod):
        if (a * x) % mod == 1:
            return x
    raise ValueError("ไม่มีโมดูลาร์อินเวิร์สสำหรับคีย์นี้")


# ฟังก์ชันสร้างบล็อกจากข้อความ
def create_blocks(message, block_size):
    message_length = len(message)
    if message_length % block_size != 0:
        padding_length = block_size - (message_length % block_size)
        message += ' ' * padding_length  # เพิ่มช่องว่างเป็น padding
    blocks = [message[i:i + block_size] for i in range(0, len(message), block_size)]
    return blocks


# ฟังก์ชันแปลงตัวอักษรเป็นค่า ASCII
def to_ascii(block):
    return [ord(char) for char in block]


# ฟังก์ชันแปลงค่าจาก ASCII กลับเป็นตัวอักษร
def from_ascii(block):
    return ''.join([chr(num) for num in block])

# ฟังก์ชันเข้ารหัส
def encrypt(message, key):
    block_size = key.shape[0]  # ขนาดของเมทริกซ์
    blocks = create_blocks(message, block_size)
   
    encrypted_message = ""
    for block in blocks:
        ascii_block = to_ascii(block)
        # ดำเนินการคูณเมทริกซ์
        encrypted_block = np.dot(key, ascii_block) % 256  # mod 256 เพื่อให้ค่าคงอยู่ในช่วง ASCII
        encrypted_message += ''.join([chr(int(value)) for value in encrypted_block])
   
    return encrypted_message

# ฟังก์ชันถอดรหัส
def decrypt(encrypted_message, inverse_key):
    block_size = inverse_key.shape[0]
    blocks = create_blocks(encrypted_message, block_size)
   
    decrypted_message = ""
    for block in blocks:
        ascii_block = to_ascii(block)
        # ดำเนินการคูณเมทริกซ์กับคีย์อินเวิร์ส
        decrypted_block = np.dot(inverse_key, ascii_block) % 256  # mod 256 เพื่อให้ค่าคงอยู่ในช่วง ASCII
        decrypted_message += ''.join([chr(int(value)) for value in decrypted_block])
    return decrypted_message.strip()  # ลบช่องว่าง padding ออก

# ฟังก์ชันค้นหาโมดูลาร์อินเวิร์สของเมทริกซ์ 2x2 ภายใต้ mod 256
def mod_matrix_inverse(matrix, mod=256):
    det = int(np.round(np.linalg.det(matrix)))  # คำนวณหา determinant ของเมทริกซ์
    det_inv = mod_inverse(det, mod)  # คำนวณหาโมดูลาร์อินเวิร์สของ determinant
   
    # เมทริกซ์อินเวิร์สที่ยังไม่ได้คูณกับ determinant
    inv_matrix = np.linalg.inv(matrix) * det
    adj_matrix = np.round(inv_matrix).astype(int) % mod  # เมทริกซ์ adjugate mod 256
   
    # นำโมดูลาร์อินเวิร์สของ determinant มาคูณเพื่อให้ได้เมทริกซ์อินเวิร์สสุดท้าย
    return (det_inv * adj_matrix) % mod

# ตัวอย่างการใช้งาน
if __name__ == "__main__":
    # เมทริกซ์คีย์เข้ารหัส 2x2
    key = np.array([[3, 3],
                    [2, 5]])

    # คำนวณหาโมดูลาร์อินเวิร์สของเมทริกซ์คีย์เพื่อใช้ในการถอดรหัส
    inverse_key = mod_matrix_inverse(key, mod=256)
   
    # ข้อความที่ต้องการเข้ารหัส
    message = input(f"Type Your Message: ")
    print("Original  Message:", message)
   
    # เข้ารหัสข้อความ
    encrypted_message = encrypt(message, key)
    print("Encrypted Message:", encrypted_message)

    # ถอดรหัสข้อความ
    decrypted_message = decrypt(encrypted_message, inverse_key)
    print("Decrypted Message:", decrypted_message)
    print(f"This is your Key: ", key)