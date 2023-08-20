from PIL import Image, ImageDraw, ImageFont

print(ImageFont)

def create_locker_num_img(num):
    width, height = 125, 61
    background_color = (0, 0, 0)
    locker_num_image = Image.new('RGB', (width, height), background_color)

    font_size = 40
    font = ImageFont.truetype("arial.ttf", font_size)
    print(type(font))
    draw = ImageDraw.Draw(locker_num_image)

    text = str(num)
    text_color = (255, 255, 255)
    text_position = (width / 2 - 50, 0)

    draw.text(text_position, text, fill=text_color, font=font)

    return locker_num_image

def create_ESL_locker_img(origin_img_src, save_src,num):
    original_image = Image.open(origin_img_src)

    width = 250
    height = 122

    insert_image = create_locker_num_img(num)

    # 삽입할 위치의 좌표
    insert_left = width//2
    insert_top = height//2

    # 이미지 삽입
    original_image.paste(insert_image, (insert_left, insert_top))
    original_image.save(f'{save_src}/ESL-locker-{num}.png')



