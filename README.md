# image-encryption
Encryption / decryption of images with AES (CBC and ECB mode supported) in Python 3

### Dependencies

- opencv (s. https://github.com/skvark/opencv-python)

- pycryptodome (s. https://www.pycryptodome.org/en/latest/)

- numpy (s. https://numpy.org/doc/)

### Configuration

The following settings are possible in PyImgEnc.py:

- Set the mode in section '# Set mode': AES.MODE_CBC or AES.MODE_ECB.

- Set the file path of the image to be encrypted in section '# Load original image': If the image is in the same directory as PyImgEnc.py, only the filename is required, e.g. topsecret.jpg.

### Image formats

- The images to be encrypted can be in one of the common formats (jpg, bmp, etc.). 

- Encrypted images can also be saved. For this purpose a lossless format like bmp must be used.

### Program execution and flow

- Start the program under Windows in the comand prompt with: py pyimgenc.py 

- Once the program is started, the original image is displayed first. A click on any key displays the encrypted image. A further kick displays the decrypted image. Another click deletes all images and exits the program. 

### Example

- Original image
![Alt text](orig.jpg?raw=true "Title")

- Encrypted image (CBC mode)

- Encrypted image (ECB mode)

- Decrypted image
