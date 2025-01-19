import numpy as np

# Function คำนวณโมดูลาร์ผกผันต่่ำกว่า 256
def mod_inverse(a, mod=256):
    a = a % mod
    for x in range(1, mod):
        if (a * x) % mod == 1:
            return x
    raise ValueError("No modular inverse exists for this key.")

def create_blocks(message, block_size):
    message_length = len(message)
    if message_length % block_size != 0:
        padding_length = block_size - (message_length % block_size)
        message += ' ' * padding_length  # Add spaces as padding
    blocks = [message[i:i + block_size] for i in range(0, len(message), block_size)]
    print(f"Blocks: {blocks}")  # Print blocks
    return blocks

# Function เปลี่ยนตัวอักษรเป็น ASCII
def to_ascii(block):
    ascii_values = [ord(char) for char in block]
    print(f"ASCII Values for block '{block}': {ascii_values}")  # Print ASCII values
    return ascii_values
    
# เข้ารหัส
def encrypt(message, key):
    block_size = key.shape[0]  # Size of the matrix
    blocks = create_blocks(message, block_size)
    
    encrypted_message = ""
    for block in blocks:
        ascii_block = to_ascii(block)
        # คูณเมทริกซ์
        encrypted_block = np.dot(key, ascii_block) % 256  # mod 256 ให้ค่าอยู่ในรหัส ASCII
        encrypted_message += ''.join([chr(int(value)) for value in encrypted_block])
    
    return encrypted_message

# ถอดรหัส
def decrypt(encrypted_message, inverse_key):
    block_size = inverse_key.shape[0]
    blocks = create_blocks(encrypted_message, block_size)
    
    decrypted_message = ""
    for block in blocks:
        ascii_block = to_ascii(block)
        # คูณเมทริกซ์กับเมทริกซ์ของคีย์เมทริกซ์
        decrypted_block = np.dot(inverse_key, ascii_block) % 256  # Mod 256 to keep values in ASCII range
        decrypted_message += ''.join([chr(int(value)) for value in decrypted_block])
    
    return decrypted_message.strip()

# Function คำนวณโมดูลาร์ผกผัน mod 256
def mod_matrix_inverse(matrix, mod=256):
    det = int(np.round(np.linalg.det(matrix)))  # หาค่าดีเทอร์มินันต์
    det_inv = mod_inverse(det, mod)  # mod 256
    
    
    inv_matrix = np.linalg.inv(matrix) * det
    adj_matrix = np.round(inv_matrix).astype(int) % mod
    
    return (det_inv * adj_matrix) % mod

# ตัวอย่าง
if __name__ == "__main__":
    # คีย์เมทริกซ์ 2x2 สำหรับเข้ารหัส
    key = np.array([[3, 3],
                    [2, 5]])

    inverse_key = mod_matrix_inverse(key, mod=256)
    
    message = input(f"Type Your Message: ")
    print("Original  Message:", message)
    
    print(f"This is your Key: ", key)

    encrypted_message = encrypt(message, key)
    print("Encrypted Message:", encrypted_message)


    decrypted_message = decrypt(encrypted_message, inverse_key)
    print("Decrypted Message:", decrypted_message)
