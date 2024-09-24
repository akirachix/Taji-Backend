from image__upload.models import ImageUpload

def process_image(image_instance):
    extracted_text = extract_text_from_image(image_instance)
    image_upload = ImageUpload.objects.create(image_file=image_instance, extracted_text=extracted_text)
    return image_upload  

def extract_text_from_image(image_instance):
    extracted_text = "sample text from image"
    print(f"Extracted text: {extracted_text}")
    return extracted_text
