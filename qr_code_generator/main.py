import qrcode

def generate_qr(data: str, filename: str = "qrcode.png", size: int = 10):
    """
    Generate a QR code from the given data.
    
    Parameters:
    - data (str): The text or URL to encode in the QR code.
    - filename (str): The name of the output file (default: 'qrcode.png').
    - size (int): The size of the QR code (default: 10, adjusts box size).
    """
    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR code
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
        box_size=size,  # Size of each box in the QR code grid
        border=4  # Border thickness
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill='black', back_color='white')
    img.save(filename)
    print(f"QR code saved as {filename}")

if __name__ == "__main__":
    text = input("Enter text or URL to generate QR code: ")
    generate_qr(text)
