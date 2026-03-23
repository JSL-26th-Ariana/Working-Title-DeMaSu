#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
デマス (DeMaSu) システムアーキテクチャ図 PDF生成
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# ─── フォント設定 ───
FONT_NORMAL = None
FONT_BOLD = None

# Try Hiragino first
hiragino_w3 = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"
hiragino_w6 = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"
apple_sd = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
arial_uni = "/Library/Fonts/Arial Unicode.ttf"

if os.path.exists(hiragino_w3):
    try:
        pdfmetrics.registerFont(TTFont("HiraginoW3", hiragino_w3, subfontIndex=0))
        FONT_NORMAL = "HiraginoW3"
    except:
        pass

if os.path.exists(hiragino_w6):
    try:
        pdfmetrics.registerFont(TTFont("HiraginoW6", hiragino_w6, subfontIndex=0))
        FONT_BOLD = "HiraginoW6"
    except:
        pass

if not FONT_NORMAL and os.path.exists(apple_sd):
    try:
        pdfmetrics.registerFont(TTFont("AppleSD", apple_sd, subfontIndex=0))
        FONT_NORMAL = "AppleSD"
    except:
        pass

if not FONT_NORMAL and os.path.exists(arial_uni):
    try:
        pdfmetrics.registerFont(TTFont("ArialUnicode", arial_uni))
        FONT_NORMAL = "ArialUnicode"
    except:
        pass

if not FONT_NORMAL:
    FONT_NORMAL = "Helvetica"
if not FONT_BOLD:
    FONT_BOLD = FONT_NORMAL

print(f"Using fonts: NORMAL={FONT_NORMAL}, BOLD={FONT_BOLD}")

# ─── カラー ───
PRIMARY = HexColor("#00C896")
PRIMARY_LIGHT = HexColor("#E8FAF4")
DARK = HexColor("#2D3436")
GRAY = HexColor("#636E72")
LIGHT_GRAY = HexColor("#DFE6E9")
LIGHT_BG = HexColor("#F5F5F5")
WHITE = white
ACCENT = HexColor("#0984E3")
PURPLE = HexColor("#6C5CE7")
ORANGE = HexColor("#E17055")

output_path = "/Users/parkminseon/Desktop/DeMaSu_Architecture.pdf"
W, H = A4

c = canvas.Canvas(output_path, pagesize=A4)

# ─── ヘルパー関数 ───
def draw_rounded_rect(x, y, w, h, r=8, fill_color=WHITE, stroke_color=LIGHT_GRAY, stroke_width=1):
    c.setStrokeColor(stroke_color)
    c.setLineWidth(stroke_width)
    c.setFillColor(fill_color)
    c.roundRect(x, y, w, h, r, fill=1, stroke=1)

def draw_text(x, y, text, font=None, size=10, color=DARK, centered=False):
    if font is None:
        font = FONT_NORMAL
    c.setFont(font, size)
    c.setFillColor(color)
    if centered:
        c.drawCentredString(x, y, text)
    else:
        c.drawString(x, y, text)

def draw_box(x, y, w, h, fill_color, text, sub_text=None, text_color=WHITE, font_size=11, sub_size=9):
    draw_rounded_rect(x, y, w, h, r=6, fill_color=fill_color, stroke_color=fill_color, stroke_width=0)
    if sub_text:
        draw_text(x + w/2, y + h/2 + 4, text, FONT_BOLD, font_size, text_color, centered=True)
        draw_text(x + w/2, y + h/2 - 10, sub_text, FONT_NORMAL, sub_size, text_color, centered=True)
    else:
        draw_text(x + w/2, y + h/2 - 3, text, FONT_BOLD, font_size, text_color, centered=True)

def draw_arrow_down(x, y1, y2, color=GRAY):
    c.setStrokeColor(color)
    c.setLineWidth(1.5)
    c.line(x, y1, x, y2)
    c.setFillColor(color)
    s = 4
    p = c.beginPath()
    p.moveTo(x, y2)
    p.lineTo(x - s, y2 + s * 1.5)
    p.lineTo(x + s, y2 + s * 1.5)
    p.close()
    c.drawPath(p, fill=1, stroke=0)

def draw_double_arrow_v(x, y1, y2, color=GRAY):
    c.setStrokeColor(color)
    c.setLineWidth(1.5)
    c.line(x, y1, x, y2)
    c.setFillColor(color)
    s = 4
    p = c.beginPath()
    p.moveTo(x, y2)
    p.lineTo(x - s, y2 + s * 1.5)
    p.lineTo(x + s, y2 + s * 1.5)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    p = c.beginPath()
    p.moveTo(x, y1)
    p.lineTo(x - s, y1 - s * 1.5)
    p.lineTo(x + s, y1 - s * 1.5)
    p.close()
    c.drawPath(p, fill=1, stroke=0)


# ════════════════════════════════════════
# ページ1: レイヤードアーキテクチャ
# ════════════════════════════════════════

# タイトル
draw_text(W/2, H - 45, "DeMaSu System Architecture", FONT_BOLD, 22, PRIMARY, centered=True)
draw_text(W/2, H - 65, "Layered MVC Architecture", FONT_NORMAL, 12, GRAY, centered=True)

# 背景枠
margin = 35
content_top = H - 85
content_bottom = 40
draw_rounded_rect(margin, content_bottom, W - 2*margin, content_top - content_bottom, r=12, fill_color=LIGHT_BG, stroke_color=LIGHT_GRAY)

# レイヤー定義
layer_x = 65
layer_w = W - 130
layer_h = 58
gap = 20
start_y = content_top - 25

layers = [
    {
        "name": "Presentation Layer",
        "sub": "Thymeleaf  |  HTML5/CSS3  |  JavaScript  |  Naver Maps API",
        "color": HexColor("#00C896"),
    },
    {
        "name": "Controller Layer  (9 Controllers)",
        "sub": "Home | Auth | Toilet | Review | Admin | Inquiry | Report | MyPage | ...",
        "color": HexColor("#00B386"),
    },
    {
        "name": "Service Layer  (9 Services)",
        "sub": "ToiletService | ReviewService | AuthService | AdminService | ...",
        "color": HexColor("#009973"),
    },
    {
        "name": "Data Access Layer  -  MyBatis  (10 Mappers)",
        "sub": "ToiletMapper.xml | ReviewMapper.xml | UserMapper.xml | ... (No JPA/Entity)",
        "color": HexColor("#008060"),
    },
    {
        "name": "Database  -  MySQL 8.0",
        "sub": "jsl26tp  |  9 Tables  |  UTF-8  |  Foreign Key Relationships",
        "color": HexColor("#006B50"),
    },
]

for i, layer in enumerate(layers):
    y = start_y - i * (layer_h + gap)
    draw_box(layer_x, y - layer_h, layer_w, layer_h,
             layer["color"], layer["name"], layer["sub"], WHITE, 12, 9)

    if i < len(layers) - 1:
        draw_arrow_down(W/2, y - layer_h - 2, y - layer_h - gap + 2, GRAY)

# 左ラベル
labels = ["View", "Controller", "Business Logic", "SQL Mapping", "Storage"]
for i, label in enumerate(labels):
    y = start_y - i * (layer_h + gap) - layer_h/2
    c.saveState()
    c.translate(50, y)
    c.rotate(90)
    draw_text(0, 0, label, FONT_NORMAL, 7, GRAY, centered=True)
    c.restoreState()

# フッター
draw_text(W/2, 20, "DeMaSu - JSL-26th-Ariana  |  Page 1/2", FONT_NORMAL, 8, GRAY, centered=True)

# ════════════════════════════════════════
# ページ2: システム全体構成図
# ════════════════════════════════════════
c.showPage()

# タイトル
draw_text(W/2, H - 45, "DeMaSu System Architecture", FONT_BOLD, 22, PRIMARY, centered=True)
draw_text(W/2, H - 65, "System Overview Diagram", FONT_NORMAL, 12, GRAY, centered=True)

# 背景枠
draw_rounded_rect(margin, content_bottom, W - 2*margin, content_top - content_bottom, r=12, fill_color=LIGHT_BG, stroke_color=LIGHT_GRAY)

# ── クライアント ──
client_y = content_top - 50
client_x = W/2 - 110
client_w = 220
client_h = 42

draw_text(margin + 15, client_y + 8, "CLIENT", FONT_BOLD, 9, GRAY)
draw_box(client_x, client_y - client_h, client_w, client_h,
         HexColor("#636E72"), "Browser (Chrome / Safari / Edge)", "HTML + CSS + JavaScript", WHITE, 11, 8)

# 矢印
draw_double_arrow_v(W/2, client_y - client_h - 5, client_y - client_h - 30, PRIMARY)
draw_text(W/2 + 30, client_y - client_h - 18, "HTTP Request / Response", FONT_NORMAL, 7, PRIMARY, centered=True)

# ── サーバー ──
server_top = client_y - client_h - 35
server_h = 270
server_x = margin + 15
server_w = W - 2*margin - 30

draw_rounded_rect(server_x, server_top - server_h, server_w, server_h, r=10,
                 fill_color=PRIMARY_LIGHT, stroke_color=PRIMARY, stroke_width=1.5)

draw_text(server_x + 10, server_top - 18, "SPRING BOOT APPLICATION SERVER", FONT_BOLD, 10, PRIMARY)

# 内部コンポーネント
comp_h = 35
comp_gap = 10
inner_margin = 15
inner_x = server_x + inner_margin
inner_w = server_w - 2*inner_margin

# Security + OAuth2
comp_y = server_top - 40
sec_w = inner_w * 0.48
oauth_w = inner_w * 0.48
draw_box(inner_x, comp_y - comp_h, sec_w, comp_h,
         ACCENT, "Spring Security", "RBAC / CSRF / BCrypt", WHITE, 10, 8)
draw_box(inner_x + inner_w - oauth_w, comp_y - comp_h, oauth_w, comp_h,
         PURPLE, "Google OAuth2", "Social Login", WHITE, 10, 8)

# Controller
comp_y2 = comp_y - comp_h - comp_gap
draw_box(inner_x, comp_y2 - comp_h, inner_w, comp_h,
         HexColor("#00C896"), "Controller Layer (9 Controllers)",
         "Home | Auth | Toilet | Review | Admin | Inquiry | Report | MyPage", WHITE, 10, 7)

# Service
comp_y3 = comp_y2 - comp_h - comp_gap
draw_box(inner_x, comp_y3 - comp_h, inner_w, comp_h,
         HexColor("#00B386"), "Service Layer (9 Services)",
         "Business Logic | Validation | Haversine Distance", WHITE, 10, 8)

# MyBatis
comp_y4 = comp_y3 - comp_h - comp_gap
draw_box(inner_x, comp_y4 - comp_h, inner_w, comp_h,
         HexColor("#009973"), "MyBatis Mapper (XML)",
         "SQL Mapping | No JPA/Entity | 10 Mapper Files", WHITE, 10, 8)

# Thymeleaf
comp_y5 = comp_y4 - comp_h - comp_gap
draw_box(inner_x, comp_y5 - 28, inner_w, 28,
         HexColor("#008060"), "Thymeleaf Template Engine (Server-Side Rendering)", None, WHITE, 9)

# 矢印
draw_arrow_down(W/2, comp_y - comp_h - 1, comp_y2, GRAY)
draw_arrow_down(W/2, comp_y2 - comp_h - 1, comp_y3, GRAY)
draw_arrow_down(W/2, comp_y3 - comp_h - 1, comp_y4, GRAY)

# ── DB ──
db_y = server_top - server_h - 45
db_x = W/2 - 90
db_w = 180
db_h = 42

draw_text(margin + 15, db_y + 10, "DATABASE", FONT_BOLD, 9, GRAY)
draw_box(db_x, db_y - db_h, db_w, db_h,
         DARK, "MySQL 8.0", "jsl26tp | 9 Tables | UTF-8", WHITE, 12, 8)

draw_double_arrow_v(W/2, server_top - server_h - 5, db_y + 2, HexColor("#009973"))
draw_text(W/2 + 30, server_top - server_h - 22, "SQL Query / Result", FONT_NORMAL, 7, HexColor("#009973"), centered=True)

# ── 外部API ──
api_y = db_y - db_h - 35
api_h = 38

draw_text(margin + 15, api_y + 10, "EXTERNAL API", FONT_BOLD, 9, GRAY)

naver_x = margin + 40
naver_w = 155
draw_box(naver_x, api_y - api_h, naver_w, api_h,
         HexColor("#2DB400"), "Naver Maps API", "Map / Marker / Navigation", WHITE, 10, 8)

google_x = W - margin - 40 - 155
google_w = 155
draw_box(google_x, api_y - api_h, google_w, api_h,
         HexColor("#4285F4"), "Google OAuth2 API", "Social Login Auth", WHITE, 10, 8)

# 点線接続
c.setDash(3, 3)
c.setStrokeColor(HexColor("#2DB400"))
c.setLineWidth(1.2)
naver_mid = naver_x + naver_w/2
c.line(naver_mid, api_y, naver_mid, api_y + 15)
c.line(naver_mid, api_y + 15, W/2 - 50, api_y + 15)
c.line(W/2 - 50, api_y + 15, W/2 - 50, server_top - server_h - 5)

c.setStrokeColor(HexColor("#4285F4"))
google_mid = google_x + google_w/2
c.line(google_mid, api_y, google_mid, api_y + 15)
c.line(google_mid, api_y + 15, W/2 + 50, api_y + 15)
c.line(W/2 + 50, api_y + 15, W/2 + 50, server_top - server_h - 5)
c.setDash()

# CSV
csv_x = W/2 - 80
csv_w = 160
csv_y = api_y - api_h - 28
draw_box(csv_x, csv_y - 28, csv_w, 28,
         ORANGE, "Public Data CSV (data.go.kr)", "Initial Toilet Data Import", WHITE, 9, 7)

# フッター
draw_text(W/2, 20, "DeMaSu - JSL-26th-Ariana  |  Page 2/2", FONT_NORMAL, 8, GRAY, centered=True)

# 保存
c.save()
print(f"PDF created: {output_path}")
