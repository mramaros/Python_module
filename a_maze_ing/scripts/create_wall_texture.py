from PIL import Image, ImageDraw

W = H = 64
img = Image.new('RGBA', (W, H), (80, 140, 40, 255))
d = ImageDraw.Draw(img)
# add subtle border and noise-like pattern
for i in range(0, W, 8):
    d.line((i, 0, i, H), fill=(60, 110, 30, 255), width=1)
for j in range(0, H, 8):
    d.line((0, j, W, j), fill=(60, 110, 30, 255), width=1)
# darker vignette border
for k in range(3):
    d.rectangle((k, k, W-1-k, H-1-k), outline=(30, 50, 20, 255))

img.save('wall_texture.png')
print('wall_texture.png created')
