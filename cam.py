from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Create a VideoCapture object to capture video from your camera
cap = cv2.VideoCapture(0)  # 0 represents the default camera, change it if needed

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Encode the frame to JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                break
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
