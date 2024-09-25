from google.cloud import vision_v1
import cv2
from datetime import datetime
import re

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    processed_path = f'processed_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg'
    cv2.imwrite(processed_path, thresh)
    
    return processed_path

def extract_batch_number_from_image(image_file):
    client = vision_v1.ImageAnnotatorClient()

    try:
        processed_image_path = preprocess_image(image_file.filename)  

        with open(processed_image_path, 'rb') as img_file:
            content = img_file.read()
        
        image = vision_v1.Image(content=content)
        response = client.text_detection(image=image)

        if response.error.message:
            raise Exception(f"{response.error.message}")

        extracted_text = response.text_annotations[0].description if response.text_annotations else ""
        
        print("Extracted Text:", extracted_text) 

        patterns = [
        r"Batch No\.\s*(\d+)",
        r'B\.?\s*No\.?\s*:?\s*([A-Z0-9]+)', 
        r'Batch\s*No\.?\s*:?\s*([A-Z0-9]+)',
        r'B\.?\s*No\.?\s*([A-Z0-9]+)',
        r'([A-Z0-9]{5,10})',
        r'Batch\s*Code\s*:?\s*([A-Z0-9]+)',
        r'Lot\s*No\.?\s*:?\s*([A-Z0-9]+)',
        r'Lot\s*:?\s*([A-Z0-9]+)',
        r'L\.?\s*No\.?\s*:?\s*([A-Z0-9]+)',
        r'Lot\s*Code\s*:?\s*([A-Z0-9]+)',
        r'Batch\s*ID\s*:?\s*([A-Z0-9]+)',
        r'Batch\s*Number\s*:?\s*([A-Z0-9]+)',
        r'Control\s*No\.?\s*:?\s*([A-Z0-9]+)',
        r'B/N\s*:?\s*([A-Z0-9]+)',
        r'Lot/B\.?\s*No\.?\s*:?\s*([A-Z0-9]+)',
        r'Mfg\s*Batch\s*:?\s*([A-Z0-9]+)',
        r'Prod\s*Batch\s*:?\s*([A-Z0-9]+)',
        r'([A-Z]{2}[0-9]{3,6})',
        r'[B|L]atch\s*:?\s*([A-Z0-9]+)',
        r'BN\s*:?\s*([A-Z0-9]+)',
        r'Lot[\s/]*Batch\s*:?\s*([A-Z0-9]+)',
        r'[Bb]atch\s*#?\s*:?([A-Z0-9]+)',
        r'B\.?\s*No\.?\s*\.\s*([A-Z0-9]+)', 
        r'Lot\s*No\.?\s*:?\s*([0-9]+)', 
        r'Lot No\.\s*([0-9]{6})',  
    ]

        batch_number = None
        for pattern in patterns:
            match = re.search(pattern, extracted_text, re.IGNORECASE)
            if match:
                batch_number = match.group(1)
                break

        return batch_number if batch_number else None

    except Exception as e:
        print(f"Error in image processing: {str(e)}")
        return None
