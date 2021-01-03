import sys
import cv2
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# This program encrypts a jpg With AES-256. The encrypted image contains more data than the original image (e.g. because of 
# padding, IV etc.). Therefore the encrypted image has one row more. Supported are CBC and ECB mode.

# Set mode
mode = AES.MODE_CBC
#mode = AES.MODE_ECB
if mode != AES.MODE_CBC and mode != AES.MODE_ECB:
    print('Only CBC and ECB mode supported...')
    sys.exit()

# Set sizes
keySize = 32
ivSize = AES.block_size if mode == AES.MODE_CBC else 0

#
# Start Encryption ----------------------------------------------------------------------------------------------
#

# Load original image
imageOrig = cv2.imread("topsecret.jpg")
rowOrig, columnOrig, depthOrig = imageOrig.shape

# Check for minimum width
minWidth = (AES.block_size + AES.block_size) // depthOrig + 1
if columnOrig < minWidth:
    print('The minimum width of the image must be {} pixels, so that IV and padding can be stored in a single additional row!'.format(minWidth))
    sys.exit()

# Display original image
cv2.imshow("Original image", imageOrig)
cv2.waitKey()

# Convert original image data to bytes
imageOrigBytes = imageOrig.tobytes()

# Encrypt
key = get_random_bytes(keySize)
iv = get_random_bytes(ivSize)
cipher = AES.new(key, AES.MODE_CBC, iv) if mode == AES.MODE_CBC else AES.new(key, AES.MODE_ECB)
imageOrigBytesPadded = pad(imageOrigBytes, AES.block_size)
ciphertext = cipher.encrypt(imageOrigBytesPadded)

# Convert ciphertext bytes to encrypted image data
#    The additional row contains columnOrig * DepthOrig bytes. Of this, ivSize + paddedSize bytes are used 
#    and void = columnOrig * DepthOrig - ivSize - paddedSize bytes unused
paddedSize = len(imageOrigBytesPadded) - len(imageOrigBytes)
void = columnOrig * depthOrig - ivSize - paddedSize
ivCiphertextVoid = iv + ciphertext + bytes(void)
imageEncrypted = np.frombuffer(ivCiphertextVoid, dtype = imageOrig.dtype).reshape(rowOrig + 1, columnOrig, depthOrig)

# Display encrypted image
cv2.imshow("Encrypted image", imageEncrypted)
cv2.waitKey()

# Save the encrypted image (optional)
#    If the encrypted image is to be stored, a format must be chosen that does not change the data. Otherwise, 
#    decryption is not possible after loading the encrypted image. bmp does not change the data, but jpg does. 
#    When saving with imwrite, the format is controlled by the extension (.jpg, .bmp). The following works:
#    cv2.imwrite("topsecretEnc.bmp", imageEncrypted)
#    imageEncrypted = cv2.imread("topsecretEnc.bmp")

#
# Start Decryption ----------------------------------------------------------------------------------------------
#

# Convert encrypted image data to ciphertext bytes
rowEncrypted, columnOrig, depthOrig = imageEncrypted.shape 
rowOrig = rowEncrypted - 1
encryptedBytes = imageEncrypted.tobytes()
iv = encryptedBytes[:ivSize]
imageOrigBytesSize = rowOrig * columnOrig * depthOrig
paddedSize = (imageOrigBytesSize // AES.block_size + 1) * AES.block_size - imageOrigBytesSize
encrypted = encryptedBytes[ivSize : ivSize + imageOrigBytesSize + paddedSize]

# Decrypt
cipher = AES.new(key, AES.MODE_CBC, iv) if mode == AES.MODE_CBC else AES.new(key, AES.MODE_ECB)
decryptedImageBytesPadded = cipher.decrypt(encrypted)
decryptedImageBytes = unpad(decryptedImageBytesPadded, AES.block_size)

# Convert bytes to decrypted image data
decryptedImage = np.frombuffer(decryptedImageBytes, imageEncrypted.dtype).reshape(rowOrig, columnOrig, depthOrig)

# Display decrypted image
cv2.imshow("Decrypted Image", decryptedImage)
cv2.waitKey()

# Close all windows
cv2.destroyAllWindows()
