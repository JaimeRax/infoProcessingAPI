import pytesseract
import cv2

# function to extract the data
def get_best_text(cropped_image):
    aux_texts = []
    gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

    for threshold_value in range(50,220,10):
        _, thresholded_img = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY) # use umbral

        text = pytesseract.image_to_string(thresholded_img, config=f"--tessdata-dir /usr/share/tesseract-ocr/5/tessdata --psm 6 -l spa")

        # add text in the list
        if text.strip():
            aux_texts.append(text.strip())

    if aux_texts:
        best_text = max(aux_texts, key=aux_texts.count)  
        return best_text.replace('\n', ' ')  # return text
    else:
        return ""  

# Function to extract paragraph text
def extract_paragraph_text(image):
    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Extract text as a single paragraph
    text = pytesseract.image_to_string(
        gray_image, 
        config="--tessdata-dir /usr/share/tesseract-ocr/5/tessdata --psm 6 -l spa"
    )
    
    # Clean up the text (remove newline characters)
    return text.replace('\n', ' ').strip()
