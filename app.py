from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    watermark_text = request.form['watermark_text']
    font_size = int(request.form['font_size'])
    font_weight = int(request.form['font_weight'])
    font_color = request.form['font_color']
    position = request.form['position']

    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Add watermark
        img = Image.open(filepath)
        draw = ImageDraw.Draw(img)

        # Ganti path font dengan path yang benar
        font_path = "/Library/Fonts/Arial.ttf"  # Ganti dengan path font yang Anda miliki
        font = ImageFont.truetype(font_path, font_size)

        text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
        textwidth, textheight = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
        width, height = img.size

        if position == 'top_left':
            x, y = 10, 10
        elif position == 'top_right':
            x, y = width - textwidth - 10, 10
        elif position == 'bottom_left':
            x, y = 10, height - textheight - 10
        elif position == 'bottom_right':
            x, y = width - textwidth - 10, height - textheight - 10
        elif position == 'center':
            x, y = (width - textwidth) // 2, (height - textheight) // 2

        # Hanya gunakan fill tanpa stroke
        draw.text((x, y), watermark_text, font=font, fill=font_color)
        img.save(filepath)

        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)
