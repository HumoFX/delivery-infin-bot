# from pyzbar.pyzbar import decode
# from pyzbar.pyzbar import ZBarSymbol
# import cv2
#
#
# def read_qr(image_path: str):
#     image = cv2.imread(image_path)
#     codes = decode(image, symbols=[ZBarSymbol.QRCODE])
#     decoded = []
#     for code in codes:
#         codeData = code.data.decode("utf-8")
#         decoded.append(str(codeData))
#     return decoded
