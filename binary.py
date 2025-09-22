#rb , wb, read txt , open amd append txt files
with open("image.png", "rb") as fsrc, open( "demo1.png","wb") as a:
    first_image = fsrc.read()
    a.write(first_image)
