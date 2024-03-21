import base64
import cv2
from fastapi import FastAPI, HTTPException

app = FastAPI()

def resize_image(image_data, new_width):
    # Decode base64 image data
    imgdata = base64.b64decode(image_data)
    
    # Decode image using OpenCV
    img = cv2.imdecode(np.frombuffer(imgdata, np.uint8), cv2.IMREAD_COLOR)

    # Calculate new height while preserving aspect ratio
    height, width, _ = img.shape
    new_height = int(new_width * height / width)
    
    # Resize the image
    resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # Encode the resized image to bytes
    _, buffer = cv2.imencode('.jpg', resized_img)
    resized_image_data = buffer.tobytes()

    return resized_image_data

@app.post('/upload_image')
async def upload_image(image: dict):
    if 'image' not in image:
        raise HTTPException(status_code=400, detail='No image data found')

    try:
        # Resize the image
        new_width = 100  # Adjust the new width as needed
        resized_image_data = resize_image(image['image'], new_width)

        # Encode the resized image data as base64
        resized_base64 = base64.b64encode(resized_image_data).decode('utf-8')

        # Return the resized image back
        return {'resized_image': resized_base64}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
