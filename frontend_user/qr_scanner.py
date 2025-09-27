import cv2
from pyzbar.pyzbar import decode

def scan_qr():
    cap = cv2.VideoCapture(0)
    qr_code_data = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        for barcode in decode(frame):
            qr_code_data = barcode.data.decode('utf-8')
            cv2.rectangle(frame, (barcode.rect.left, barcode.rect.top),
                          (barcode.rect.left + barcode.rect.width, barcode.rect.top + barcode.rect.height),
                          (0,255,0), 2)
            cv2.putText(frame, qr_code_data, (barcode.rect.left, barcode.rect.top-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
            break

        cv2.imshow("Scan QR Code", frame)
        if qr_code_data or cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return qr_code_data