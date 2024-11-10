import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
page_style="""
<style>
[data-testid="stAppViewContainer"], [data-testid="stHeader"]{
    background-color: #0e1118;
}
[data-testid="stHeadingWithActionElements"], [data-testid="stMarkdownContainer"]{
    color: #fff
}
[data-testid="stMarkdown"]{
    background-color: green;
    padding: 20;
    font-size: 17;
}
</style>
"""

# Load Model
model = tf.keras.models.load_model('model/img_predict_model.h5')
# Faire des prédictions
# probability_model = tf.keras.Sequential([
#     model,
#     tf.keras.layers.Softmax()
# ])

print(model.summary())

st.markdown(page_style, unsafe_allow_html=True)
st.title("Fashion mnist Classifier")

upload_image = st.file_uploader(
    "Upload an image of a fashion item",
    type=["jpg", "png"]
    #accept_multiple_files=True
)

def import_predict_image(image_up):
    image_up = image_up.convert('L')
    sizes = (28,28)
    image = ImageOps.fit(image_up, sizes)
    img = np.asarray(image).astype('float32') / 255.0 # Normalize pixel values
    img = np.expand_dims(img, axis=-1) # Add the grayscale channel dimension
    img_reshape = (np.expand_dims(img, 0)) # Add batch dimension
    return img_reshape # Shape should be (1, 28, 28, 1)

def predict_func(model, img):
    predictions = model.predict(img)
    max_prob = np.argmax(predictions, axis=1)[0]  # Get the index of the max probability
    return class_names[max_prob]


if upload_image==None:
    st.write("Please upload an image")
else:
    aff_image = Image.open(upload_image)
    st.image(aff_image.convert('L'), use_container_width=True)
    upload_image = import_predict_image(aff_image)
    result = predict_func(model, upload_image)
    st.write('Prediction Result is : ', result)