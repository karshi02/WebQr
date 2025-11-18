# # from flask import Flask, request, flash, render_template, url_for, redirect
# # from PIL import Image, ImageDraw, ImageColor   # << รวมไว้บรรทัดนี้
# # from datetime import datetime
# # import io, os, logging
# # import qrcode
# # from qrcode.image.styledpil import StyledPilImage
# # from qrcode.image.styles.moduledrawers import (
# #     SquareModuleDrawer, CircleModuleDrawer, RoundedModuleDrawer
# # )
# # from qrcode.image.styles.colormasks import SolidFillColorMask
# # import re

# # def is_valid_hex_color(color: str) -> bool:
# #     return bool(re.match(r'^#[0-9A-Fa-f]{6}$', color.strip()))
# # # if not is_valid_hex_color(color):
# # #     flash("สี QR ไม่ถูกต้อง กรุณาใช้รหัสสีแบบ #RRGGBB")
# # #     return redirect(url_for("index"))
# # # if not is_valid_hex_color(bg):
# # #     flash("สีพื้นหลังไม่ถูกต้อง กรุณาใช้รหัสสีแบบ #RRGGBB")
# # #     return redirect(url_for("index"))
# # # ตั้งค่า logging
# # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# # app = Flask(__name__)
# # app.secret_key = "change-me"  # ใช้จริงเปลี่ยนเป็นค่าลับๆ
# # app.logger.setLevel(logging.DEBUG)


# # # ====== Config สำหรับการสร้าง QR ======
# # # def to_rgb(val: str, default_hex: str):
# # #     try:
# # #         return ImageColor.getrgb((val or "").strip())
# # #     except Exception:
# # #         return ImageColor.getrgb(default_hex)
# # def to_rgb(val: str, default_hex: str):
# #     app.logger.debug(f"to_rgb input: {val}")
# #     try:
# #         result = ImageColor.getrgb((val or "").strip())
# #         app.logger.debug(f"to_rgb output: {result}")
# #         return result
# #     except Exception as e:
# #         app.logger.debug(f"to_rgb failed: {e}")
# #         return ImageColor.getrgb(default_hex)
    


# # # ====== Config สำหรับหน้า Support ======
# # DONATE_CONFIG = {
# #     "bank_name": "ธนาคารกรุงไทย",
# #     "account_name": "โครงการพัฒนา QR",
# #     "account_number": "123-4-56789-0",
# #     "wallet_provider": "TrueMoney Wallet",
# #     "wallet_number": "08x-xxx-xxxx",
# #     "support_link": "https://example.com/support",
# # }

# # # ====== Utils ======
# # def ensure_url_scheme(u: str) -> str:
# #     u = (u or "").strip()
# #     if not u:
# #         return ""
# #     if not (u.startswith("http://") or u.startswith("https://")):
# #         u = "https://" + u
# #     return u

# # def pick_module_drawer(key: str):
# #     if key == "dot":
# #         return CircleModuleDrawer()
# #     if key == "rounded":
# #         return RoundedModuleDrawer()
# #     return SquareModuleDrawer()  # default

# # def paste_logo_center(base_img: Image.Image, logo_img: Image.Image, ratio=0.23, with_white_circle=True):
# #     """วางโลโก้กลาง + พื้นหลังวงกลมสีขาวโปร่งเล็กน้อยให้อ่านง่าย"""
# #     base = base_img.convert("RGBA")
# #     logo = logo_img.convert("RGBA")

# #     max_side = int(min(base.size) * ratio)
# #     logo.thumbnail((max_side, max_side), Image.LANCZOS)

# #     overlay = logo
# #     if with_white_circle:
# #         pad = max(6, max_side // 8)
# #         bg_size = (logo.width + pad * 2, logo.height + pad * 2)
# #         circle_bg = Image.new("RGBA", bg_size, (255, 255, 255, 230))
# #         mask = Image.new("L", bg_size, 0)
# #         d = ImageDraw.Draw(mask)
# #         d.ellipse([0, 0, bg_size[0], bg_size[1]], fill=255)
# #         circle_bg.putalpha(mask)
# #         circle_bg.paste(logo, (pad, pad), logo)
# #         overlay = circle_bg

# #     x = (base.width - overlay.width) // 2
# #     y = (base.height - overlay.height) // 2
# #     base.paste(overlay, (x, y), overlay)
# #     return base

# # # ====== Routes ======
# # @app.route("/", methods=["GET"])
# # def index():
# #     # ส่งค่าเริ่มต้นกัน template งงตัวแปร
# #     return render_template(
# #         "index.html",
# #         preview_url=None,
# #         download_url=None,
# #         data="",
# #         color="#000000",
# #         bg="#ffffff",
# #         size=10,
# #         border=2,
# #         qr_style="square"
# #     )

# # @app.route("/", methods=["POST"])
# # def generate_qr():
# #     try:
# #         url_raw = request.form.get("url", "")
# #         url = ensure_url_scheme(url_raw)
# #         color = (request.form.get("color") or request.form.get("color_text") or "#000000").strip()
# #         bg = (request.form.get("bg") or request.form.get("bg_text") or "#ffffff").strip()
# #         size = int(request.form.get("size", 10))
# #         border = int(request.form.get("border", 2))
# #         qr_style = request.form.get("qr_style") or request.form.get("style") or "square"

# #         if not url:
# #             flash("กรุณาใส่ URL ก่อนนะ")
# #             return redirect(url_for("index"))
# #         if url in ("https://", "http://"):
# #             flash("URL ไม่ถูกต้อง ลองกรอกให้ครบ เช่น https://example.com")
# #             return redirect(url_for("index"))

# #         qr = qrcode.QRCode(
# #             version=None,
# #             error_correction=qrcode.constants.ERROR_CORRECT_H,  # H ทนต่อโลโก้
# #             box_size=max(4, min(size, 40)),
# #             border=max(0, min(border, 10)),
# #         )
# #         qr.add_data(url)
# #         qr.make(fit=True)

# #         # img = qr.make_image(
# #         #     image_factory=StyledPilImage,
# #         #     module_drawer=pick_module_drawer(qr_style),
# #         #     color_mask=SolidFillColorMask(back_color=bg, front_color=color),
# #         # ).convert("RGBA")
# #         img = qr.make_image(
# #     image_factory=StyledPilImage,
# #     module_drawer=pick_module_drawer(qr_style),
# #     color_mask=SolidFillColorMask(back_color=to_rgb(bg, "#ffffff"), front_color=to_rgb(color, "#000000")),
# # ).convert("RGBA")
# # #         img = qr.make_image(
# # #     image_factory=StyledPilImage,
# # #     module_drawer=pick_module_drawer(qr_style),
# # #     color_mask=SolidFillColorMask(
# # #         back_color=to_rgb(bg, "#ffffff"),
# # #         front_color=to_rgb(color, "#000000")
# # #     ),
# # # ).convert("RGBA")
# #         # แปลงเป็น RGBA เพื่อรองรับโปร่งใส
# #         img = img.convert("RGBA")   
# #         # วาดพื้นหลัง
# #         if bg and bg.lower() != "#ffffff":
# #             bg_color = to_rgb(bg, "#ffffff")
# #             bg_img = Image.new("RGBA", img.size, bg_color)
# #             img = Image.alpha_composite(bg_img, img)

# #         # โลโก้ (ถ้ามี)
# #         logo_file = request.files.get("logo")
# #         if logo_file and logo_file.filename:
# #             try:
# #                 logo = Image.open(logo_file.stream)
# #                 img = paste_logo_center(img, logo, ratio=0.23, with_white_circle=True)
# #             except Exception as e:
# #                 app.logger.exception("Logo paste failed")
# #                 flash(f"เกิดข้อผิดพลาดในการเพิ่มโลโก้: {e}")

# #         # เซฟสำหรับพรีวิว/ดาวน์โหลด
# #         out_dir = os.path.join("static", "qr")
# #         os.makedirs(out_dir, exist_ok=True)
# #         filename = f"qr_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
# #         out_path = os.path.join(out_dir, filename)
# #         img.save(out_path)

# #         preview_url = url_for("static", filename=f"qr/{filename}")
# #         return render_template(
# #             "index.html",
# #             preview_url=preview_url,
# #             download_url=preview_url,
# #             data=url,
# #             color=color,
# #             bg=bg,
# #             size=size,
# #             border=border,
# #             qr_style=qr_style
# #         )
# #     except Exception as e:
# #         app.logger.exception("QR generation failed")
# #         flash(f"เกิดข้อผิดพลาดในการสร้าง QR: {e}")
# #         return redirect(url_for("index"))

# # @app.route("/support")
# # def support():
# #     # สร้าง QR ไปยังลิงก์สนับสนุน (ถ้ามี)
# #     support_qr_url = None
# #     link = DONATE_CONFIG.get("support_link")
# #     if link:
# #         qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
# #         qr.add_data(link)
# #         qr.make(fit=True)
# #         img = qr.make_image(fill_color="black", back_color="white")

# #         out_dir = os.path.join("static", "qr")
# #         os.makedirs(out_dir, exist_ok=True)
# #         filename = f"support_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
# #         img.save(os.path.join(out_dir, filename))
# #         support_qr_url = url_for("static", filename=f"qr/{filename}")

# #     return render_template("support.html", cfg=DONATE_CONFIG, support_qr_url=support_qr_url)

# # if __name__ == "__main__":
# #     # โหมด dev
# #     app.run(host="0.0.0.0", port=5000, debug=True)
# # # -*- coding: utf-8 -*-
# from flask import Flask, request, flash, render_template, url_for, redirect
# from PIL import Image, ImageDraw, ImageColor
# from datetime import datetime
# import os, logging, re
# import qrcode
# from qrcode.image.styledpil import StyledPilImage
# from qrcode.image.styles.moduledrawers import (
#     SquareModuleDrawer, CircleModuleDrawer, RoundedModuleDrawer
# )
# from qrcode.image.styles.colormasks import SolidFillColorMask

# # ตั้งค่า logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# app = Flask(__name__)
# app.secret_key = "change-me"  # ใช้จริงเปลี่ยนเป็นค่าลับๆ
# app.logger.setLevel(logging.DEBUG)
# app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # Limit uploads to 10MB

# # ====== Config สำหรับการสร้าง QR ======
# def to_rgb(val: str, default_hex: str):
#     app.logger.debug(f"to_rgb input: {val}")
#     try:
#         result = ImageColor.getrgb((val or "").strip())
#         app.logger.debug(f"to_rgb output: {result}")
#         return result
#     except Exception as e:
#         app.logger.debug(f"to_rgb failed: {e}")
#         return ImageColor.getrgb(default_hex)

# def is_valid_hex_color(color: str) -> bool:
#     return bool(re.match(r'^#[0-9A-Fa-f]{6}$', color.strip()))

# def is_valid_file(filename: str) -> bool:
#     allowed_extensions = {'png', 'jpg', 'jpeg', 'mp4', 'mov'}
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# def sanitize_filename(filename: str) -> str:
#     # Replace unsafe characters and keep only alphanumeric, dots, and underscores
#     return re.sub(r'[^a-zA-Z0-9._-]', '_', filename)

# # ====== Config สำหรับหน้า Support ======
# DONATE_CONFIG = {
#     "bank_name": "ธนาคารกรุงไทย",
#     "account_name": "โครงการพัฒนา QR",
#     "account_number": "123-4-56789-0",
#     "wallet_provider": "TrueMoney Wallet",
#     "wallet_number": "08x-xxx-xxxx",
#     "support_link": "https://example.com/support",
# }

# # ====== Utils ======
# def ensure_url_scheme(u: str) -> str:
#     u = (u or "").strip()
#     if not u:
#         return ""
#     if not (u.startswith("http://") or u.startswith("https://")):
#         u = "https://" + u
#     return u

# def pick_module_drawer(key: str):
#     if key == "dot":
#         return CircleModuleDrawer()
#     if key == "rounded":
#         return RoundedModuleDrawer()
#     return SquareModuleDrawer()  # default

# def paste_logo_center(base_img: Image.Image, logo_img: Image.Image, ratio=0.23, with_white_circle=True):
#     base = base_img.convert("RGBA")
#     logo = logo_img.convert("RGBA")
#     max_side = int(min(base.size) * ratio)
#     logo.thumbnail((max_side, max_side), Image.LANCZOS)
#     overlay = logo
#     if with_white_circle:
#         pad = max(6, max_side // 8)
#         bg_size = (logo.width + pad * 2, logo.height + pad * 2)
#         circle_bg = Image.new("RGBA", bg_size, (255, 255, 255, 230))
#         mask = Image.new("L", bg_size, 0)
#         d = ImageDraw.Draw(mask)
#         d.ellipse([0, 0, bg_size[0], bg_size[1]], fill=255)
#         circle_bg.putalpha(mask)
#         circle_bg.paste(logo, (pad, pad), logo)
#         overlay = circle_bg
#     x = (base.width - overlay.width) // 2
#     y = (base.height - overlay.height) // 2
#     base.paste(overlay, (x, y), overlay)
#     return base

# # ====== Routes ======
# @app.route("/", methods=["GET"])
# def index():
#     return render_template(
#         "index.html",
#         preview_url=None,
#         download_url=None,
#         data="",
#         color="#000000",
#         bg="#ffffff",
#         size=10,
#         border=2,
#         qr_style="square",
#         input_type="url"
#     )

# @app.route("/", methods=["POST"])
# def generate_qr():
#     try:
#         input_type = request.form.get("input_type", "url")
#         url = ""
#         if input_type == "url":
#             url_raw = request.form.get("url", "")
#             url = ensure_url_scheme(url_raw)
#             if not url:
#                 flash("กรุณาใส่ URL ก่อนนะ")
#                 return redirect(url_for("index"))
#             if url in ("https://", "http://"):
#                 flash("URL ไม่ถูกต้อง ลองกรอกให้ครบ เช่น https://example.com")
#                 return redirect(url_for("index"))
#         elif input_type == "file":
#             file = request.files.get("media_file")
#             if not file or not file.filename:
#                 flash("กรุณาอัปโหลดไฟล์ภาพหรือวิดีโอก่อน")
#                 return redirect(url_for("index"))
#             if not is_valid_file(file.filename):
#                 flash("ไฟล์ไม่รองรับ กรุณาอัปโหลดไฟล์ PNG, JPEG, MP4 หรือ MOV")
#                 return redirect(url_for("index"))
#             # Save the uploaded file
#             upload_dir = os.path.join("static", "uploads")
#             os.makedirs(upload_dir, exist_ok=True)
#             filename = sanitize_filename(f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
#             file_path = os.path.join(upload_dir, filename)
#             file.save(file_path)
#             # Generate URL for the file
#             url = url_for("static", filename=f"uploads/{filename}", _external=True)

#         color = (request.form.get("color") or request.form.get("color_text") or "#000000").strip()
#         bg = (request.form.get("bg") or request.form.get("bg_text") or "#ffffff").strip()
#         size = int(request.form.get("size", 10))
#         border = int(request.form.get("border", 2))
#         qr_style = request.form.get("qr_style") or request.form.get("style") or "square"

#         app.logger.debug(f"Form inputs - input_type: {input_type}, url: {url}, color: {color}, bg: {bg}, size: {size}, border: {border}, qr_style: {qr_style}")

#         if not is_valid_hex_color(color):
#             flash("สี QR ไม่ถูกต้อง กรุณาใช้รหัสสีแบบ #RRGGBB")
#             return redirect(url_for("index"))
#         if not is_valid_hex_color(bg):
#             flash("สีพื้นหลังไม่ถูกต้อง กรุณาใช้รหัสสีแบบ #RRGGBB")
#             return redirect(url_for("index"))

#         qr = qrcode.QRCode(
#             version=None,
#             error_correction=qrcode.constants.ERROR_CORRECT_H,
#             box_size=max(4, min(size, 40)),
#             border=max(0, min(border, 10)),
#         )
#         qr.add_data(url)
#         qr.make(fit=True)

#         img = qr.make_image(
#             image_factory=StyledPilImage,
#             module_drawer=pick_module_drawer(qr_style),
#             color_mask=SolidFillColorMask(
#                 back_color=to_rgb(bg, "#ffffff"),
#                 front_color=to_rgb(color, "#000000")
#             )
#         )

#         # โลโก้ (ถ้ามี)
#         logo_file = request.files.get("logo")
#         if logo_file and logo_file.filename:
#             try:
#                 logo = Image.open(logo_file.stream)
#                 img = paste_logo_center(img, logo, ratio=0.23, with_white_circle=True)
#             except Exception as e:
#                 app.logger.exception("Logo paste failed")
#                 flash(f"เกิดข้อผิดพลาดในการเพิ่มโลโก้: {e}")

#         # เซฟ QR Code
#         out_dir = os.path.join("static", "qr")
#         os.makedirs(out_dir, exist_ok=True)
#         qr_filename = f"qr_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
#         out_path = os.path.join(out_dir, qr_filename)
#         img.save(out_path)

#         preview_url = url_for("static", filename=f"qr/{qr_filename}")
#         return render_template(
#             "index.html",
#             preview_url=preview_url,
#             download_url=preview_url,
#             data=url,
#             color=color,
#             bg=bg,
#             size=size,
#             border=border,
#             qr_style=qr_style,
#             input_type=input_type
#         )
#     except Exception as e:
#         app.logger.exception("QR generation failed")
#         flash(f"เกิดข้อผิดพลาดในการสร้าง QR: {e}")
#         return redirect(url_for("index"))

# @app.route("/support")
# def support():
#     support_qr_url = None
#     link = DONATE_CONFIG.get("support_link")
#     if link:
#         qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
#         qr.add_data(link)
#         qr.make(fit=True)
#         img = qr.make_image(fill_color="black", back_color="white")
#         out_dir = os.path.join("static", "qr")
#         os.makedirs(out_dir, exist_ok=True)
#         filename = f"support_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
#         img.save(os.path.join(out_dir, filename))
#         support_qr_url = url_for("static", filename=f"qr/{filename}")

#     return render_template("support.html", cfg=DONATE_CONFIG, support_qr_url=support_qr_url)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)
# # -*- coding: utf-8 -*-




# -*- coding: utf-8 -*-
from flask import Flask, request, flash, render_template, url_for, redirect
from PIL import Image, ImageDraw, ImageColor
from datetime import datetime
import os, logging, re
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    SquareModuleDrawer, CircleModuleDrawer, RoundedModuleDrawer
)
from qrcode.image.styles.colormasks import SolidFillColorMask

# ตั้งค่า logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
app = Flask(__name__)
app.secret_key = "change-me"
app.logger.setLevel(logging.DEBUG)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # Limit uploads to 10MB

# ====== Config ======
def to_rgb(val: str, default_hex: str):
    app.logger.debug(f"to_rgb input: {val}")
    try:
        result = ImageColor.getrgb((val or "").strip())
        app.logger.debug(f"to_rgb output: {result}")
        return result
    except Exception as e:
        app.logger.debug(f"to_rgb failed: {e}")
        return ImageColor.getrgb(default_hex)

def is_valid_hex_color(color: str) -> bool:
    return bool(re.match(r'^#[0-9A-Fa-f]{6}$', color.strip()))

def is_valid_file(filename: str) -> bool:
    allowed_extensions = {'png', 'jpg', 'jpeg', 'mp4', 'mov'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def sanitize_filename(filename: str) -> str:
    return re.sub(r'[^a-zA-Z0-9._-]', '_', filename)

# ====== Page Config ======
DONATE_CONFIG = {
    "bank_name": "ธนาคารกรุงไทย",
    "account_name": "โครงการพัฒนา QR",
    "account_number": "123-4-56789-0",
    "wallet_provider": "TrueMoney Wallet",
    "wallet_number": "08x-xxx-xxxx",
    "support_link": "https://example.com/support",
}

# ====== Utils ======
def ensure_url_scheme(u: str) -> str:
    u = (u or "").strip()
    if not u:
        return ""
    if not (u.startswith("http://") or u.startswith("https://")):
        u = "https://" + u
    return u

def pick_module_drawer(key: str):
    if key == "dot":
        return CircleModuleDrawer()
    if key == "rounded":
        return RoundedModuleDrawer()
    return SquareModuleDrawer()

def paste_logo_center(base_img: Image.Image, logo_img: Image.Image, ratio=0.23, with_white_circle=True):
    base = base_img.convert("RGBA")
    logo = logo_img.convert("RGBA")
    max_side = int(min(base.size) * ratio)
    logo.thumbnail((max_side, max_side), Image.LANCZOS)

    overlay = logo
    if with_white_circle:
        pad = max(6, max_side // 8)
        bg_size = (logo.width + pad * 2, logo.height + pad * 2)
        circle_bg = Image.new("RGBA", bg_size, (255, 255, 255, 230))

        mask = Image.new("L", bg_size, 0)
        d = ImageDraw.Draw(mask)
        d.ellipse([0, 0, bg_size[0], bg_size[1]], fill=255)
        circle_bg.putalpha(mask)
        circle_bg.paste(logo, (pad, pad), logo)
        overlay = circle_bg

    x = (base.width - overlay.width) // 2
    y = (base.height - overlay.height) // 2
    base.paste(overlay, (x, y), overlay)
    return base

# ====== Routes ======
@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        preview_url=None,
        download_url=None,
        data="",
        color="#000000",
        bg="#ffffff",
        size=10,
        border=2,
        qr_style="square",
        input_type="url"
    )

@app.route("/", methods=["POST"])
def generate_qr():
    try:
        input_type = request.form.get("input_type", "url")
        url = ""

        if input_type == "url":
            url_raw = request.form.get("url", "")
            url = ensure_url_scheme(url_raw)
            if not url:
                flash("กรุณาใส่ URL ก่อนนะ")
                return redirect(url_for("index"))

        elif input_type == "file":
            file = request.files.get("media_file")
            if not file or not file.filename:
                flash("กรุณาอัปโหลดไฟล์ก่อน")
                return redirect(url_for("index"))

            upload_dir = os.path.join("static", "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            filename = sanitize_filename(f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
            file_path = os.path.join(upload_dir, filename)
            file.save(file_path)

            url = url_for("static", filename=f"uploads/{filename}", _external=True)

        color = request.form.get("color", "#000000").strip()
        bg = request.form.get("bg", "#ffffff").strip()
        size = int(request.form.get("size", 10))
        border = int(request.form.get("border", 2))
        qr_style = request.form.get("qr_style", "square")

        if not is_valid_hex_color(color) or not is_valid_hex_color(bg):
            flash("สีไม่ถูกต้อง")
            return redirect(url_for("index"))

        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=max(4, min(size, 40)),
            border=max(0, min(border, 10)),
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=pick_module_drawer(qr_style),
            color_mask=SolidFillColorMask(
                back_color=to_rgb(bg, "#ffffff"),
                front_color=to_rgb(color, "#000000")
            )
        )

        # Save QR
        out_dir = os.path.join("static", "qr")
        os.makedirs(out_dir, exist_ok=True)
        filename = f"qr_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        img.save(os.path.join(out_dir, filename))

        preview_url = url_for("static", filename=f"qr/{filename}")
        return render_template(
            "index.html",
            preview_url=preview_url,
            download_url=preview_url,
            data=url,
            color=color,
            bg=bg,
            size=size,
            border=border,
            qr_style=qr_style,
            input_type=input_type
        )

    except Exception as e:
        app.logger.exception("QR generation failed")
        flash(f"เกิดข้อผิดพลาด: {e}")
        return redirect(url_for("index"))

@app.route("/support")
def support():
    return render_template("support.html", cfg=DONATE_CONFIG)

# ❗ ไม่มี app.run() ตรงนี้ — Render ใช้ gunicorn
