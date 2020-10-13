# TODO: Dit in een klasse schrijven.

import qrcode

def generate_qrcode(data):
    '''Generates QR code based on data given'''
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.show()

generate_qrcode('123456')