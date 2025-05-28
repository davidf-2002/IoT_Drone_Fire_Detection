import os
import time
from datetime import datetime
import requests
from picamera2 import Picamera2

# Azure Custom Vision API configuration
ENDPOINT_URL = "https://firedetectiondrone-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/06ad55d9-c113-4972-886b-f9a1eaa11250/classify/iterations/FirePredictionModel/image"
PREDICTION_KEY = "AtrcWuyZCegEsda1LCsvm7WBC73mx3St4wYGEl0hOlUJjc9JdQf0JQQJ99BDAC5RqLJXJ3w3AAAIACOGq016"

class FireDetection:
    def __init__(self):
        self.picam2 = None

    def initialize_camera(self):
        """Initialize camera with specific configuration"""
        self.picam2 = Picamera2()
        camera_config = self.picam2.create_still_configuration(main={"size": (1920, 1080)})
        self.picam2.configure(camera_config)
        self.picam2.start()
        time.sleep(2)  # Give camera time to warm up

    def capture_image(self):
        """Capture an image and save it temporarily"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = f"/tmp/fire_detection_{timestamp}.jpg"
            print(f"Attempting to capture image to {image_path}")
            
            # Capture image with metadata
            self.picam2.capture_file(image_path)
            
            # Verify file exists and has size
            if os.path.exists(image_path):
                file_size = os.path.getsize(image_path)
                print(f"Image captured successfully. File size: {file_size} bytes")
                if file_size == 0:
                    print("Warning: Captured image file is empty!")
                    return None
                return image_path
            else:
                print("Error: Image file was not created!")
                return None
                
        except Exception as e:
            print(f"Error capturing image: {str(e)}")
            return None

    def analyze_image(self, image_path):
        """Send image to Azure Custom Vision API and get prediction"""
        try:
            print(f"Opening image file: {image_path}")
            with open(image_path, 'rb') as image_file:
                # Read file content
                image_data = image_file.read()
                print(f"Read {len(image_data)} bytes from image file")
                
                headers = {
                    'Prediction-Key': PREDICTION_KEY,
                    'Content-Type': 'application/octet-stream'
                }
                print("Sending request to Azure Custom Vision API...")
                response = requests.post(ENDPOINT_URL, headers=headers, data=image_data)
                print(f"Response status code: {response.status_code}")
                print(f"Response content: {response.text}")
                
                if response.status_code != 200:
                    print(f"Error: API returned status code {response.status_code}")
                    return None
                    
                return response.json()
        except Exception as e:
            print(f"Error in analyze_image: {str(e)}")
            return None

    def process_capture(self):
        """Process a single capture-analyze cycle"""
        print("\nStarting new capture cycle...")
        image_path = self.capture_image()
        
        if image_path and os.path.exists(image_path):
            print("Analyzing image for fire...")
            result = self.analyze_image(image_path)
            
            if result:
                # Check predictions
                for prediction in result.get('predictions', []):
                    print(f"Prediction: {prediction['tagName']} - {prediction['probability']*100:.2f}%")
                    if prediction['tagName'] == 'fire' and prediction['probability'] > 0.7:
                        print(f"Fire detected with {prediction['probability']*100:.2f}% confidence!")
                        return {
                            'detected': True,
                            'confidence': prediction['probability'],
                            'timestamp': datetime.utcnow().isoformat()
                        }
                else:
                    print("No fire detected.")
                    return {
                        'detected': False,
                        'confidence': 0.0
                    }
            
            # Clean up temporary image
            try:
                os.remove(image_path)
                print(f"Cleaned up temporary image: {image_path}")
            except Exception as e:
                print(f"Error cleaning up image: {str(e)}")
        else:
            print("Failed to capture or save image.")
            return {
                'detected': False,
                'confidence': 0.0,
                'timestamp': datetime.utcnow().isoformat()
            }

    def shutdown(self):
        """Clean up resources"""
        if self.picam2:
            self.picam2.stop()
            print("Camera stopped")

# Example usage:
"""
if __name__ == "__main__":
    fire_detection = FireDetection()
    try:
        fire_detection.initialize_camera()
        
        while True:
            # Countdown
            for i in range(5, 0, -1):
                print(f"Capturing in {i} seconds...")
                time.sleep(1)
            
            fire_detected = fire_detection.process_capture()
            print(f"Fire detected: {fire_detected}")
            
            # Wait between captures
            print("\nWaiting 10 seconds before next capture...")
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    finally:
        fire_detection.shutdown()
""" 
