from cloudinary.uploader import upload

def save_image(file):
    print(file,"file")
    upload_img = upload(file)
    return upload_img['url']
