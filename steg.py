from PIL import Image

def string_to_binary(secret_message):
    
    converted_secret_message = ""

    for character in secret_message:
        
        converted_character = ' '.join('{0:08b}'.format(ord(character), 'b'))
        converted_secret_message += converted_character
    
    return converted_secret_message
    
def encode_message(secret_message, user_image):

    binary_secret_message = string_to_binary(secret_message)
    
    image_width, image_height = user_image.size

    loaded_user_image = user_image.load()

    raw_encoded_data = []

message = "luke brown"
print(string_to_binary(message))




    
