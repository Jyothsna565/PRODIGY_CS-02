from PIL import Image
import numpy as np

def encrypt_decrypt_image(input_path, output_path, key):
    # Open the image
    img = Image.open(input_path)
    
    # Convert image to numpy array
    img_array = np.array(img)
    
    # Convert key to a byte array
    key_bytes = key.to_bytes((key.bit_length() + 7) // 8, 'big')
    
    # Ensure the key length is appropriate for the image size
    key_length = len(key_bytes)
    
    # Check if image is grayscale or color
    if img_array.ndim == 2:  # Grayscale image
        flat_array = img_array.flatten()
        # Repeat key to match the length of flat_array
        key_array = np.resize(np.frombuffer(key_bytes, dtype=np.uint8), len(flat_array))
        encrypted_array = flat_array ^ key_array
        encrypted_img_array = encrypted_array.reshape(img_array.shape)
    else:  # Color image (e.g., RGB)
        encrypted_img_array = img_array.copy()
        for i in range(3):  # Iterate over each channel
            flat_array = img_array[:, :, i].flatten()
            # Repeat key to match the length of flat_array
            key_array = np.resize(np.frombuffer(key_bytes, dtype=np.uint8), len(flat_array))
            encrypted_array = flat_array ^ key_array
            encrypted_img_array[:, :, i] = encrypted_array.reshape(img_array[:, :, i].shape)
    
    # Create a new image from the encrypted array
    encrypted_img = Image.fromarray(encrypted_img_array.astype('uint8'))
    
    # Save the encrypted/decrypted image
    encrypted_img.save(output_path)

def main():
    while True:
        choice = input("Enter 'e' to encrypt, 'd' to decrypt, or 'q' to quit: ").lower()
        
        if choice == 'q':
            break
        
        if choice not in ['e', 'd']:
            print("Invalid choice. Please try again.")
            continue
        
        input_path = input("Enter the path to the input image: ")
        output_path = input("Enter the path for the output image: ")
        key = input("Enter the encryption/decryption key (integer): ")
        
        try:
            key = int(key)
        except ValueError:
            print("Invalid key. Please enter an integer.")
            continue
        
        encrypt_decrypt_image(input_path, output_path, key)
        
        print(f"Image {'encrypted' if choice == 'e' else 'decrypted'} successfully!")

if __name__ == "__main__":
    main()
