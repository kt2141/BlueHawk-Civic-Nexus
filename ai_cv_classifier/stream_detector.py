import json
import time
from datetime import datetime, timezone

import cv2


def build_payload(category, confidence, frame_shape, source="hawk_edge_cam"):
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "event_category": category,
        "confidence": round(float(confidence), 3),
        "frame": {"width": frame_shape[1], "height": frame_shape[0]},
        "geo": {"lat": 26.5123, "lon": 80.2329},
    }


def classify_frame_simple(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mean_intensity = float(gray.mean())
    if mean_intensity < 45:
        return "security_anomaly", 0.72
    if mean_intensity > 200:
        return "waste_or_drainage_hazard", 0.61
    return "normal", 0.4


def annotate_frame(frame, label, confidence):
    h, w = frame.shape[:2]
    color = (0, 0, 255) if label == "security_anomaly" else (0, 165, 255)
    if label == "normal":
        color = (0, 255, 0)

    x1, y1, x2, y2 = int(0.2 * w), int(0.2 * h), int(0.8 * w), int(0.8 * h)
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    cv2.putText(
        frame,
        f"{label} ({confidence:.2f})",
        (x1, max(y1 - 10, 20)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        color,
        2,
        cv2.LINE_AA,
    )


def run_stream(video_source=0, output_json_path=None):
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        raise RuntimeError(f"Unable to open video source: {video_source}")

    collected = []
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            label, confidence = classify_frame_simple(frame)
            annotate_frame(frame, label, confidence)

            if label != "normal":
                payload = build_payload(label, confidence, frame.shape)
                collected.append(payload)
                print(json.dumps(payload))

            cv2.imshow("BlueHawk Stream Detector", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            time.sleep(0.02)
    finally:
        cap.release()
        cv2.destroyAllWindows()

    if output_json_path:
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(collected, f, indent=2)

    return collected


if __name__ == "__main__":
    run_stream()
