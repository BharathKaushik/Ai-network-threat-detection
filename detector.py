import joblib
import pandas as pd
from database import save_threat

# Load model
model = joblib.load('model.pkl')
protocol_encoder = joblib.load('protocol_encoder.pkl')
label_encoder = joblib.load('label_encoder.pkl')


def analyze_packet(packet_data):

    try:

        # Encode protocol
        protocol_encoded = protocol_encoder.transform([
            packet_data['protocol']
        ])[0]

        # Create dataframe
        features = pd.DataFrame([{
            'packet_size': packet_data['packet_size'],
            'protocol': protocol_encoded,
            'connection_rate': packet_data['connection_rate']
        }])

        # Predict
        prediction = model.predict(features)[0]

        # Convert prediction back to label
        threat_label = label_encoder.inverse_transform([
            prediction
        ])[0]

        print("Threat Prediction:", threat_label)

        # Save suspicious traffic
        if threat_label != 'Normal':

            alert_data = {
                'src_ip': packet_data['src_ip'],
                'dst_ip': packet_data['dst_ip'],
                'threat_type': threat_label,
                'packet_size': packet_data['packet_size']
            }

            save_threat(alert_data)

            print("ALERT! Threat detected:", threat_label)

    except Exception as e:
        print("Detector error:", e)