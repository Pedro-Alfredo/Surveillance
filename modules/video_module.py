import cv2
import threading

person_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
video_score = 0

def analisar_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    pessoas = person_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)
    risco = 1 if len(pessoas) > 3 else 0
    return risco, pessoas

def processar_video(capture_url=0):
    global video_score
    cap = cv2.VideoCapture(capture_url)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        risco, pessoas = analisar_frame(frame)
        video_score = risco
        for (x, y, w, h) in pessoas:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
        cv2.imshow('Máquina Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def iniciar_video_thread(capture_url=0):
    thread = threading.Thread(target=processar_video, args=(capture_url,), daemon=True)
    thread.start()
