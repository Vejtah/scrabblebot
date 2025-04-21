from PIL import Image, ImageDraw, ImageFont


# 1) define your “unit” in pixels
px_per_unit = 100   # e.g. 100 px per unit

# 2) dimensions in units
w_units, h_units = 2, 3
background_color = (240, 240, 240)

# compute pixel dims
width_px  = w_units * px_per_unit
height_px = h_units * px_per_unit

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


# 3) create white canvas

def make_img(letter:str):
    global background_color
    img = Image.new("RGB", (width_px, height_px), color=background_color)
    draw = ImageDraw.Draw(img)

    # 4) choose a font and size (you may need to install a TTF font file)
    font_size = int(px_per_unit * 2.3)  # adjust so letter nearly fills height
    font = ImageFont.truetype("News Gothic Bold.ttf", font_size)

    # 5) the letter to draw
    # measure text size so we can center it
    bbox = draw.textbbox((0, 0), letter, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    if False:
        print(text_w)
        print(text_h)

    # compute top‑left corner to center the text
    x = (width_px - text_w) / 2 - bbox[0]
    y = (height_px - text_h) / 2 - bbox[1]

    if False: # boudnaryies
        draw.line(
            [(x, y), (x, y + text_h)],  # endpoints (x1,y1) → (x2,y2)
            fill="red",  # color
            width=1  # line thickness in pixels
        )

        draw.line(
            [(x, y), (x + text_w, y)],  # endpoints (x1,y1) → (x2,y2)
            fill="red",  # color
            width=1  # line thickness in pixels
        )

    # 6) draw the letter in black
    draw.text((x, y), letter, fill="black", font=font)

    return img

if __name__ == "__main__":
    for letter in letters:
        img = make_img(letter=letter)
        img.save("letters_images/" + letter + ".png")
#        img.show()

# 7) save or show
