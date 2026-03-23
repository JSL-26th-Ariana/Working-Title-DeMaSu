#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
デマス (DeMaSu) 要求事項分析及びシステム設計書 PDF生成
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# ─── フォント設定 ───
font_paths = [
    ("/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc", "HiraginoW3"),
    ("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", "HiraginoW6"),
    ("/System/Library/Fonts/AppleSDGothicNeo.ttc", "AppleSD"),
    ("/Library/Fonts/Arial Unicode.ttf", "ArialUnicode"),
]

FONT_NORMAL = "Helvetica"
FONT_BOLD = "Helvetica-Bold"

for path, name in font_paths:
    if os.path.exists(path):
        try:
            pdfmetrics.registerFont(TTFont(name, path, subfontIndex=0))
            if "W3" in name or "AppleSD" in name or "ArialUnicode" in name:
                FONT_NORMAL = name
            if "W6" in name:
                FONT_BOLD = name
        except:
            pass

if FONT_BOLD == "Helvetica-Bold" and FONT_NORMAL != "Helvetica":
    FONT_BOLD = FONT_NORMAL

# ─── カラー ───
PRIMARY = HexColor("#00C896")
DARK = HexColor("#2D3436")
GRAY = HexColor("#636E72")
LIGHT_BG = HexColor("#F5F5F5")
WHITE = white
ACCENT = HexColor("#0984E3")

# ─── PDF設定 ───
output_path = "/Users/parkminseon/Desktop/DeMaSu_Requirements_Analysis.pdf"
doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    topMargin=25*mm,
    bottomMargin=20*mm,
    leftMargin=20*mm,
    rightMargin=20*mm
)

styles = getSampleStyleSheet()
W = A4[0] - 40*mm

# ─── スタイル定義 ───
def make_style(name, font=FONT_NORMAL, size=10, color=DARK, align=TA_LEFT,
               leading=None, spaceBefore=0, spaceAfter=0, bold=False):
    f = FONT_BOLD if bold else font
    return ParagraphStyle(name, fontName=f, fontSize=size, textColor=color,
                          alignment=align, leading=leading or size*1.5,
                          spaceBefore=spaceBefore, spaceAfter=spaceAfter)

S_COVER_TITLE = make_style("CoverTitle", size=28, bold=True, align=TA_CENTER, color=PRIMARY)
S_COVER_SUB = make_style("CoverSub", size=14, align=TA_CENTER, color=GRAY, spaceAfter=6)
S_H1 = make_style("H1", size=18, bold=True, color=PRIMARY, spaceBefore=16, spaceAfter=10)
S_H2 = make_style("H2", size=14, bold=True, color=DARK, spaceBefore=14, spaceAfter=8)
S_H3 = make_style("H3", size=12, bold=True, color=ACCENT, spaceBefore=10, spaceAfter=6)
S_BODY = make_style("Body", size=10, color=DARK, spaceAfter=4, align=TA_JUSTIFY)
S_BODY_INDENT = make_style("BodyIndent", size=10, color=DARK, spaceAfter=3)
S_SMALL = make_style("Small", size=9, color=GRAY, spaceAfter=2)
S_TABLE_H = make_style("TableH", size=9, bold=True, color=WHITE, align=TA_CENTER)
S_TABLE_D = make_style("TableD", size=9, color=DARK)
S_TABLE_DC = make_style("TableDC", size=9, color=DARK, align=TA_CENTER)

# ─── ヘルパー ───
def heading_bar(text, style=S_H1):
    return Paragraph(text, style)

def body(text):
    return Paragraph(text, S_BODY)

def bullet(text):
    return Paragraph(f"&bull;  {text}", S_BODY_INDENT)

def make_table(headers, rows, col_widths=None):
    hdr = [Paragraph(h, S_TABLE_H) for h in headers]
    data = [hdr]
    for row in rows:
        data.append([Paragraph(str(c), S_TABLE_D) for c in row])

    if not col_widths:
        col_widths = [W / len(headers)] * len(headers)

    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), FONT_BOLD),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#DFE6E9")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    return t

story = []

# ════════════════════════════════════════
# 表紙 (そのまま保持)
# ════════════════════════════════════════
story.append(Spacer(1, 60*mm))
story.append(Paragraph("要求事項分析及びシステム設計書", S_COVER_TITLE))
story.append(Spacer(1, 8*mm))
story.append(Paragraph("Requirements Analysis &amp; System Design", S_COVER_SUB))
story.append(Spacer(1, 15*mm))

cover_info = [
    ["Project", "DeMaSu"],
    ["Team", "JSL-26th-Ariana (6 Members)"],
    ["Period", "2026.03.01 ~ 2026.03.22 (3 Weeks)"],
    ["Version", "1.0"],
    ["Date", "2026.03.19"],
]
ct = Table(cover_info, colWidths=[50*mm, 100*mm])
ct.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (0, -1), FONT_BOLD),
    ('FONTNAME', (1, 0), (1, -1), FONT_NORMAL),
    ('FONTSIZE', (0, 0), (-1, -1), 11),
    ('TEXTCOLOR', (0, 0), (0, -1), GRAY),
    ('TEXTCOLOR', (1, 0), (1, -1), DARK),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('LINEBELOW', (0, 0), (-1, -2), 0.5, HexColor("#DFE6E9")),
    ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
    ('ALIGN', (1, 0), (1, -1), 'LEFT'),
]))
story.append(ct)
story.append(PageBreak())

# ════════════════════════════════════════
# 目次
# ════════════════════════════════════════
story.append(heading_bar("目次"))
story.append(Spacer(1, 5*mm))
toc_items = [
    "1. プロジェクト概要",
    "2. チーム構成",
    "3. 機能要件",
    "4. 非機能要件",
    "5. システムアーキテクチャ",
    "6. データベース設計 (ER図)",
    "7. APIエンドポイント仕様",
    "8. UI/UX 画面フロー",
    "9. セキュリティ設計",
    "10. エラーハンドリング",
]
for item in toc_items:
    story.append(Paragraph(item, make_style("toc", size=12, spaceAfter=6)))
story.append(PageBreak())

# ════════════════════════════════════════
# 1. プロジェクト概要
# ════════════════════════════════════════
story.append(heading_bar("1. プロジェクト概要"))
story.append(body(
    "デマス(DeMaSu)は、韓国を訪れる日本人観光客が近くの公衆トイレを簡単に見つけられるように支援する"
    "Webアプリケーションサービスです。韓国公共データポータル(data.go.kr)の公衆トイレCSVデータを基盤とし、"
    "Naver Maps JavaScript APIを活用した地図ベースの位置検索機能を提供します。"
))
story.append(Spacer(1, 3*mm))

story.append(Paragraph("1.1 背景と目的", S_H2))
story.append(bullet("韓国を訪れる日本人観光客は、清潔でアクセスしやすい公衆トイレを見つけることに困難を感じている"))
story.append(bullet("言語の壁により、韓国語で施設を検索することが難しい"))
story.append(bullet("既存の地図アプリにはトイレの詳細な設備情報(車椅子対応、ウォシュレット、非常ベル等)が不足している"))
story.append(bullet("解決策：日本語対応のトイレ検索サービスに、詳細な設備タグとユーザーレビュー機能を実装"))

story.append(Spacer(1, 3*mm))
story.append(Paragraph("1.2 技術スタック", S_H2))
story.append(make_table(
    ["カテゴリ", "技術"],
    [
        ["Backend", "Spring Boot 4.0.3, Java 17, MyBatis"],
        ["Frontend", "Thymeleaf, HTML5/CSS3/JavaScript"],
        ["Database", "MySQL 8.0"],
        ["認証", "Spring Security, Google OAuth2"],
        ["地図API", "Naver Maps JavaScript API"],
        ["データソース", "公共データポータル CSV"],
        ["ビルドツール", "Gradle (Groovy)"],
        ["IDE", "IntelliJ IDEA"],
        ["バージョン管理", "Git, GitHub"],
    ],
    col_widths=[55*mm, W-55*mm]
))
story.append(PageBreak())

# ════════════════════════════════════════
# 2. チーム構成
# ════════════════════════════════════════
story.append(heading_bar("2. チーム構成"))
story.append(make_table(
    ["名前", "GitHub", "担当"],
    [
        ["パク・ミンソン (リーダー)", "@thisisminseon", "Git管理、地図/検索、プロフィールアイコン、レビューぼかし"],
        ["ハン・スンヨン", "@aaaea1", "トイレ詳細表示、道案内、レビュータブ"],
        ["キム・イェウン", "@yeeun-021120", "管理者ダッシュボード、通報/修正リクエスト管理"],
        ["キム・ジュハ", "@minone64", "UI/UX、スプラッシュ画面、会員登録、ログインモーダル"],
        ["パク・ジユン", "@JiyoonOfficial", "マイページ、最近の閲覧履歴、URL共有"],
        ["チャン・ヒエ", "@anghi-kor", "トイレCRUD、管理者機能"],
    ],
    col_widths=[40*mm, 40*mm, W-80*mm]
))
story.append(Spacer(1, 5*mm))
story.append(Paragraph("2.1 開発期間", S_H2))
story.append(body("2026.03.01 〜 2026.03.22（約3週間）"))
story.append(bullet("第1週：プロジェクト設定、DB設計、基本CRUD実装"))
story.append(bullet("第2週：地図連携、検索/フィルター、レビューシステム、管理者ダッシュボード"))
story.append(bullet("第3週：UI/UXの改善、テスト、バグ修正、デプロイ準備"))
story.append(PageBreak())

# ════════════════════════════════════════
# 3. 機能要件
# ════════════════════════════════════════
story.append(heading_bar("3. 機能要件"))

story.append(Paragraph("3.1 ユーザー認証 (FR-AUTH)", S_H2))
story.append(make_table(
    ["ID", "要件", "優先度", "状態"],
    [
        ["FR-AUTH-01", "ローカルログイン（ユーザー名＋パスワード）", "高", "完了"],
        ["FR-AUTH-02", "Google OAuth2 ソーシャルログイン", "高", "完了"],
        ["FR-AUTH-03", "バリデーション付き会員登録", "高", "完了"],
        ["FR-AUTH-04", "重複チェック（ユーザー名、メール、ニックネーム）", "中", "完了"],
        ["FR-AUTH-05", "パスワードリセット（本人確認＋再設定）", "中", "完了"],
        ["FR-AUTH-06", "ロールベースアクセス制御（USER / ADMIN）", "高", "完了"],
        ["FR-AUTH-07", "ログイン失敗処理（停止/削除アカウント）", "中", "完了"],
        ["FR-AUTH-08", "セッションタイムアウト（30分）", "低", "完了"],
    ],
    col_widths=[25*mm, W-75*mm, 25*mm, 25*mm]
))

story.append(Spacer(1, 5*mm))
story.append(Paragraph("3.2 トイレ検索・探索 (FR-TOILET)", S_H2))
story.append(make_table(
    ["ID", "要件", "優先度", "状態"],
    [
        ["FR-TOILET-01", "GPS基準の周辺検索（Haversine公式、半径500m）", "高", "完了"],
        ["FR-TOILET-02", "タグベースフィルタリング（24時間、車椅子、ウォシュレット等）", "高", "完了"],
        ["FR-TOILET-03", "名前/住所によるキーワード検索（AND論理）", "高", "完了"],
        ["FR-TOILET-04", "地域ドロップダウンフィルター（韓国17地域）", "中", "完了"],
        ["FR-TOILET-05", "地図マーカー表示と情報ウィンドウ", "高", "完了"],
        ["FR-TOILET-06", "トイレ詳細表示（情報＋レビュー＋タグ）", "高", "完了"],
        ["FR-TOILET-07", "ユーザーによるトイレ提報（承認待ちステータス）", "中", "完了"],
        ["FR-TOILET-08", "既存トイレの修正リクエスト提出", "低", "完了"],
        ["FR-TOILET-09", "Naver Mapsへのナビゲーションリンク", "中", "完了"],
        ["FR-TOILET-10", "URLによるトイレ共有（?id=toiletId）", "低", "完了"],
        ["FR-TOILET-11", "位置情報拒否時、ソウル市庁にフォールバック", "低", "完了"],
    ],
    col_widths=[30*mm, W-80*mm, 25*mm, 25*mm]
))

story.append(PageBreak())
story.append(Paragraph("3.3 レビューシステム (FR-REVIEW)", S_H2))
story.append(make_table(
    ["ID", "要件", "優先度", "状態"],
    [
        ["FR-REVIEW-01", "レビュー作成（評価＋タグ＋内容＋画像）", "高", "完了"],
        ["FR-REVIEW-02", "自分のレビューの編集・削除", "高", "完了"],
        ["FR-REVIEW-03", "トイレ別レビュー表示（ソート付きリスト）", "高", "完了"],
        ["FR-REVIEW-04", "トイレごとの平均評価表示", "中", "完了"],
        ["FR-REVIEW-05", "画像アップロード（複数枚、各最大10MB）", "中", "完了"],
        ["FR-REVIEW-06", "未ログインユーザーへのレビューぼかし表示", "中", "完了"],
        ["FR-REVIEW-07", "不適切なレビューの通報機能", "中", "完了"],
    ],
    col_widths=[30*mm, W-80*mm, 25*mm, 25*mm]
))

story.append(Spacer(1, 5*mm))
story.append(Paragraph("3.4 ユーザープロフィール / マイページ (FR-MYPAGE)", S_H2))
story.append(make_table(
    ["ID", "要件", "優先度", "状態"],
    [
        ["FR-MYPAGE-01", "プロフィール閲覧・編集（ニックネーム、メール、電話等）", "高", "完了"],
        ["FR-MYPAGE-02", "プリセットプロフィールアイコン選択（Netflix風）", "中", "完了"],
        ["FR-MYPAGE-03", "パスワード変更", "高", "完了"],
        ["FR-MYPAGE-04", "最近閲覧したトイレ（閲覧履歴）", "中", "完了"],
        ["FR-MYPAGE-05", "自分のレビュー一覧", "中", "完了"],
        ["FR-MYPAGE-06", "自分の問い合わせ一覧", "低", "完了"],
    ],
    col_widths=[30*mm, W-80*mm, 25*mm, 25*mm]
))

story.append(Spacer(1, 5*mm))
story.append(Paragraph("3.5 管理者ダッシュボード (FR-ADMIN)", S_H2))
story.append(make_table(
    ["ID", "要件", "優先度", "状態"],
    [
        ["FR-ADMIN-01", "ダッシュボード概要（統計情報）", "高", "完了"],
        ["FR-ADMIN-02", "ユーザー管理（検索、一時停止、削除）", "高", "完了"],
        ["FR-ADMIN-03", "トイレ承認（PENDING → APPROVED/REJECTED）", "高", "完了"],
        ["FR-ADMIN-04", "通報処理（解決 / 却下）", "高", "完了"],
        ["FR-ADMIN-05", "問い合わせ管理（閲覧、回答）", "中", "完了"],
        ["FR-ADMIN-06", "修正リクエストの審査（承認 / 却下）", "中", "完了"],
        ["FR-ADMIN-07", "トイレ情報の直接編集", "中", "完了"],
    ],
    col_widths=[30*mm, W-80*mm, 25*mm, 25*mm]
))
story.append(PageBreak())

# ════════════════════════════════════════
# 4. 非機能要件
# ════════════════════════════════════════
story.append(heading_bar("4. 非機能要件"))
story.append(make_table(
    ["ID", "カテゴリ", "要件"],
    [
        ["NFR-01", "言語", "ターゲットユーザー向けに全UIテキストを日本語で表示"],
        ["NFR-02", "性能", "トイレ検索の応答時間は2秒以内"],
        ["NFR-03", "セキュリティ", "BCryptによるパスワードハッシュ化、CSRF対策"],
        ["NFR-04", "セキュリティ", "ロールベースアクセス制御（RBAC）"],
        ["NFR-05", "使いやすさ", "モバイル/デスクトップ対応のレスポンシブデザイン"],
        ["NFR-06", "データ", "公共データポータルCSVによる初期データインポート"],
        ["NFR-07", "アップロード", "ファイル最大10MB、リクエスト最大20MB"],
        ["NFR-08", "セッション", "30分のセッションタイムアウト"],
        ["NFR-09", "データベース", "ソフトデリートパターン（deleted_atフィールド）"],
        ["NFR-10", "互換性", "Chrome、Safari、Edgeブラウザ対応"],
    ],
    col_widths=[22*mm, 30*mm, W-52*mm]
))
story.append(PageBreak())

# ════════════════════════════════════════
# 5. システムアーキテクチャ
# ════════════════════════════════════════
story.append(heading_bar("5. システムアーキテクチャ"))
story.append(Paragraph("5.1 アーキテクチャ概要", S_H2))
story.append(body("本アプリケーションは、MyBatisをデータアクセス層に採用したレイヤードMVCアーキテクチャで構成されています："))
story.append(Spacer(1, 3*mm))

arch_data = [
    [Paragraph("<b>レイヤー</b>", S_TABLE_H), Paragraph("<b>構成要素</b>", S_TABLE_H), Paragraph("<b>説明</b>", S_TABLE_H)],
    [Paragraph("Presentation", S_TABLE_D), Paragraph("Thymeleaf + JS + CSS", S_TABLE_D), Paragraph("Naver Maps APIを使用したサーバーサイドレンダリングHTML", S_TABLE_D)],
    [Paragraph("Controller", S_TABLE_D), Paragraph("9個のControllerクラス", S_TABLE_D), Paragraph("HTTPリクエスト処理、ルーティング、レスポンス", S_TABLE_D)],
    [Paragraph("Service", S_TABLE_D), Paragraph("9個のServiceクラス", S_TABLE_D), Paragraph("ビジネスロジック、バリデーション、トランザクション管理", S_TABLE_D)],
    [Paragraph("Data Access", S_TABLE_D), Paragraph("10個のMyBatis Mapper", S_TABLE_D), Paragraph("XMLによるSQLマッピング（JPA/Entityは不使用）", S_TABLE_D)],
    [Paragraph("Database", S_TABLE_D), Paragraph("MySQL 8.0", S_TABLE_D), Paragraph("外部キー関係を持つ9つのテーブル", S_TABLE_D)],
]
at = Table(arch_data, colWidths=[35*mm, 45*mm, W-80*mm])
at.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
    ('BACKGROUND', (0, 1), (-1, -1), WHITE),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#DFE6E9")),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
]))
story.append(at)

story.append(Spacer(1, 5*mm))
story.append(Paragraph("5.2 パッケージ構成", S_H2))

pkg_data = [
    ["admin/", "管理者ダッシュボード、ユーザー/トイレ/通報管理"],
    ["auth/", "認証、会員登録、OAuth2、ユーザープロフィール"],
    ["common/", "ApiResponse, BusinessException, ErrorCode, GlobalExceptionHandler"],
    ["config/", "SecurityConfig, WebConfig, CustomUserDetails"],
    ["home/", "メインページコントローラー（HomeController）"],
    ["inquiry/", "ユーザー問い合わせCRUD"],
    ["report/", "コンテンツ通報送信"],
    ["review/", "レビューCRUD、画像管理、評価"],
    ["toilet/", "トイレCRUD、検索、フィルター、タグ、修正リクエスト、閲覧履歴"],
]
story.append(make_table(
    ["パッケージ", "説明"],
    pkg_data,
    col_widths=[35*mm, W-35*mm]
))
story.append(PageBreak())

# ════════════════════════════════════════
# 6. データベース設計
# ════════════════════════════════════════
story.append(heading_bar("6. データベース設計"))
story.append(Paragraph("6.1 エンティティリレーションシップ", S_H2))
story.append(body("データベース: jsl26tp  |  文字セット: UTF-8  |  総テーブル数: 9"))
story.append(Spacer(1, 3*mm))

# users table
story.append(Paragraph("6.2 Users テーブル", S_H3))
story.append(make_table(
    ["カラム", "型", "制約", "説明"],
    [
        ["id", "BIGINT", "PK, AUTO_INCREMENT", "ユーザーID"],
        ["username", "VARCHAR(50)", "UNIQUE, NOT NULL", "ログインID"],
        ["password", "VARCHAR(255)", "NOT NULL", "BCryptハッシュ化済み"],
        ["nickname", "VARCHAR(50)", "UNIQUE, NOT NULL", "表示名"],
        ["email", "VARCHAR(100)", "UNIQUE, NOT NULL", "メールアドレス"],
        ["phone", "VARCHAR(20)", "NULL", "電話番号"],
        ["gender", "VARCHAR(10)", "NULL", "性別"],
        ["birthdate", "DATE", "NULL", "生年月日"],
        ["icon_url", "VARCHAR(500)", "NULL", "プロフィールアイコンパス"],
        ["role", "VARCHAR(20)", "DEFAULT 'ROLE_USER'", "ROLE_USER / ROLE_ADMIN"],
        ["social_type", "VARCHAR(20)", "DEFAULT 'LOCAL'", "LOCAL / GOOGLE"],
        ["social_id", "VARCHAR(255)", "NULL", "OAuth2プロバイダーID"],
        ["status", "VARCHAR(20)", "DEFAULT 'ACTIVE'", "ACTIVE / SUSPENDED / DELETED"],
        ["suspend_until", "DATETIME", "NULL", "一時停止終了日"],
        ["created_at", "DATETIME", "DEFAULT NOW()", "作成日時"],
        ["updated_at", "DATETIME", "ON UPDATE NOW()", "更新日時"],
    ],
    col_widths=[30*mm, 28*mm, 42*mm, W-100*mm]
))

story.append(Spacer(1, 5*mm))
story.append(Paragraph("6.3 Toilets テーブル", S_H3))
story.append(make_table(
    ["カラム", "型", "制約", "説明"],
    [
        ["id", "BIGINT", "PK, AUTO_INCREMENT", "トイレID"],
        ["name", "VARCHAR(200)", "NOT NULL", "施設名"],
        ["address", "VARCHAR(500)", "NOT NULL", "住所"],
        ["latitude", "DOUBLE", "NOT NULL", "GPS緯度"],
        ["longitude", "DOUBLE", "NOT NULL", "GPS経度"],
        ["open_hours", "VARCHAR(50)", "NULL", "営業時間"],
        ["is_24hours", "TINYINT(1)", "DEFAULT 0", "24時間利用可能"],
        ["is_wheelchair", "TINYINT(1)", "DEFAULT 0", "車椅子対応"],
        ["has_diaper", "TINYINT(1)", "DEFAULT 0", "おむつ交換台"],
        ["has_emergency", "TINYINT(1)", "DEFAULT 0", "非常ベル"],
        ["has_cctv", "TINYINT(1)", "DEFAULT 0", "CCTV設置済み"],
        ["source", "VARCHAR(20)", "DEFAULT 'PUBLIC_API'", "PUBLIC_API / USER"],
        ["status", "VARCHAR(20)", "DEFAULT 'APPROVED'", "APPROVED / PENDING / REJECTED"],
        ["deleted_at", "DATETIME", "NULL", "ソフトデリート"],
    ],
    col_widths=[30*mm, 28*mm, 42*mm, W-100*mm]
))

story.append(PageBreak())
story.append(Paragraph("6.4 Reviews テーブル", S_H3))
story.append(make_table(
    ["カラム", "型", "制約", "説明"],
    [
        ["id", "BIGINT", "PK, AUTO_INCREMENT", "レビューID"],
        ["toilet_id", "BIGINT", "FK > toilets.id", "対象トイレ"],
        ["user_id", "BIGINT", "FK > users.id", "投稿者"],
        ["clean_score", "VARCHAR(10)", "NOT NULL", "清潔度評価"],
        ["tags", "VARCHAR(255)", "NULL", "カンマ区切りタグ"],
        ["content", "TEXT", "NULL", "レビュー本文"],
        ["status", "VARCHAR(20)", "DEFAULT 'ACTIVE'", "ACTIVE / HIDDEN"],
        ["created_at", "DATETIME", "DEFAULT NOW()", "作成日時"],
        ["deleted_at", "DATETIME", "NULL", "ソフトデリート"],
    ],
    col_widths=[30*mm, 28*mm, 42*mm, W-100*mm]
))

story.append(Spacer(1, 5*mm))
story.append(Paragraph("6.5 その他のテーブル", S_H3))
story.append(make_table(
    ["テーブル", "主要カラム", "リレーションシップ"],
    [
        ["review_images", "id, review_id, image_url", "FK > reviews.id (CASCADE)"],
        ["reports", "id, reporter_id, target_type, target_id, status", "FK > users.id"],
        ["inquiries", "id, writer_id, admin_id, title, status, answer", "FK > users.id"],
        ["toilet_edit_requests", "id, toilet_id, user_id, content, status", "FK > toilets.id, users.id"],
        ["toilet_tags", "id, toilet_id, tag_name", "FK > toilets.id (CASCADE)"],
        ["recent_views", "user_id, toilet_id, viewed_at", "複合PK、UPSERTパターン"],
    ],
    col_widths=[35*mm, 55*mm, W-90*mm]
))

story.append(Spacer(1, 5*mm))
story.append(Paragraph("6.6 ERリレーションシップまとめ", S_H3))
story.append(bullet("Users 1:N Reviews（1ユーザーが複数レビューを作成）"))
story.append(bullet("Users 1:N Reports（1ユーザーが複数通報を送信）"))
story.append(bullet("Users 1:N Inquiries（1ユーザーが複数問い合わせを送信）"))
story.append(bullet("Users N:M Toilets via Recent_Views（閲覧履歴）"))
story.append(bullet("Toilets 1:N Reviews（1トイレに複数レビュー）"))
story.append(bullet("Toilets 1:N Toilet_Tags（1トイレに複数タグ）"))
story.append(bullet("Toilets 1:N Toilet_Edit_Requests（1トイレに複数修正提案）"))
story.append(bullet("Reviews 1:N Review_Images（1レビューに複数画像）"))
story.append(PageBreak())

# ════════════════════════════════════════
# 7. APIエンドポイント仕様
# ════════════════════════════════════════
story.append(heading_bar("7. APIエンドポイント仕様"))

story.append(Paragraph("7.1 認証API", S_H2))
story.append(make_table(
    ["メソッド", "エンドポイント", "認証", "説明"],
    [
        ["POST", "/login", "公開", "フォームログイン（ユーザー名＋パスワード）"],
        ["POST", "/register", "公開", "ユーザー登録"],
        ["POST", "/logout", "User", "セッションログアウト"],
        ["GET", "/api/check-username", "公開", "ユーザー名の利用可否チェック"],
        ["GET", "/api/check-email", "公開", "メールアドレスの利用可否チェック"],
        ["GET", "/api/check-nickname", "公開", "ニックネームの利用可否チェック"],
        ["POST", "/api/users/verify-identity", "公開", "パスワードリセット本人確認"],
        ["POST", "/api/users/reset-password", "公開", "パスワードリセット実行"],
    ],
    col_widths=[18*mm, 52*mm, 18*mm, W-88*mm]
))

story.append(Spacer(1, 5*mm))
story.append(Paragraph("7.2 トイレAPI", S_H2))
story.append(make_table(
    ["メソッド", "エンドポイント", "認証", "説明"],
    [
        ["GET", "/api/toilets?lat=&amp;lng=&amp;radius=", "公開", "周辺トイレ検索（Haversine公式）"],
        ["GET", "/api/toilets/filter?lat=&amp;lng=&amp;...", "公開", "設備タグによるフィルタリング"],
        ["GET", "/api/toilets/search?keyword=", "公開", "キーワード検索（名前/住所）"],
        ["GET", "/api/toilets/{id}", "公開", "トイレ詳細と評価情報"],
        ["GET", "/api/toilets/{id}/tag", "公開", "トイレのタグ一覧"],
        ["POST", "/toilet/add", "User", "新規トイレ提報（PENDING）"],
        ["POST", "/api/toilets/{id}/edit-request", "User", "修正提案の送信"],
    ],
    col_widths=[18*mm, 55*mm, 18*mm, W-91*mm]
))

story.append(Spacer(1, 5*mm))
story.append(Paragraph("7.3 レビューAPI", S_H2))
story.append(make_table(
    ["メソッド", "エンドポイント", "認証", "説明"],
    [
        ["POST", "/review/api/write", "User", "画像付きレビュー作成"],
        ["POST", "/review/api/update", "User", "自分のレビュー更新"],
        ["POST", "/review/api/{id}/delete", "User", "自分のレビューをソフトデリート"],
        ["GET", "/review/api/toilet/{toiletId}", "公開", "トイレ別レビュー取得"],
        ["GET", "/review/api/toilet/{id}/avg", "公開", "平均評価の取得"],
        ["GET", "/review/api/toilet/{id}/cnt", "公開", "レビュー件数の取得"],
    ],
    col_widths=[18*mm, 55*mm, 18*mm, W-91*mm]
))

story.append(PageBreak())
story.append(Paragraph("7.4 管理者API", S_H2))
story.append(make_table(
    ["メソッド", "エンドポイント", "説明"],
    [
        ["GET", "/api/admin/users", "ユーザー一覧（検索、フィルター、ページネーション）"],
        ["POST", "/api/admin/users/{id}/suspend", "ユーザーアカウントの一時停止"],
        ["POST", "/api/admin/users/{id}/delete", "ユーザーアカウントのソフトデリート"],
        ["GET", "/api/admin/toilets", "承認対象トイレ一覧"],
        ["POST", "/api/admin/toilets/{id}/approve", "保留中のトイレを承認"],
        ["POST", "/api/admin/toilets/{id}/reject", "保留中のトイレを却下"],
        ["GET", "/api/admin/reports", "通報一覧（ページネーション）"],
        ["POST", "/api/admin/reports/{id}/resolve", "通報の解決（コンテンツ非表示）"],
        ["POST", "/api/admin/reports/{id}/dismiss", "通報の却下"],
        ["GET", "/api/admin/inquiries", "問い合わせ一覧（ページネーション）"],
        ["POST", "/api/admin/inquiries/{id}/answer", "問い合わせへの回答"],
        ["GET", "/api/admin/edit-requests", "修正リクエスト一覧"],
        ["POST", "/api/admin/edit-requests/{id}/approve", "修正提案の承認"],
    ],
    col_widths=[18*mm, 60*mm, W-78*mm]
))
story.append(PageBreak())

# ════════════════════════════════════════
# 8. UI/UX 画面フロー
# ════════════════════════════════════════
story.append(heading_bar("8. UI/UX 画面フロー"))
story.append(Paragraph("8.1 ユーザーフロー", S_H2))

flow_data = [
    ["メインページ (index.html)", "地図表示＋サイドバーリスト＋検索＋タグフィルター"],
    ["ログインモーダル", "ユーザー名/パスワード入力＋Google OAuth2ボタン"],
    ["会員登録", "リアルタイムバリデーション＋重複チェック付きフォーム"],
    ["トイレ詳細", "情報タブ（概要 / 詳細情報 / レビュー）"],
    ["レビュー作成", "星評価＋タグ選択＋テキスト入力＋画像アップロード"],
    ["マイページ", "プロフィール概要＋サブページへのクイックリンク"],
    ["マイページ/編集", "プロフィール編集フォーム＋アイコン選択モーダル"],
    ["マイページ/閲覧履歴", "最近閲覧したトイレ一覧"],
    ["マイページ/レビュー", "ユーザーのレビュー履歴"],
    ["トイレ追加", "Naver Maps位置ピッカー付き提報フォーム"],
]
story.append(make_table(
    ["画面", "機能"],
    flow_data,
    col_widths=[45*mm, W-45*mm]
))

story.append(Spacer(1, 5*mm))
story.append(Paragraph("8.2 管理者フロー", S_H2))
admin_flow = [
    ["ダッシュボード", "統計情報の概要＋最新アイテム"],
    ["ユーザー管理", "ユーザー検索/フィルター＋一時停止/削除操作"],
    ["トイレ承認", "PENDINGトイレ一覧＋承認/却下＋直接編集"],
    ["通報管理", "未処理の通報＋管理者メモ付き解決/却下"],
    ["問い合わせ管理", "ユーザー問い合わせ＋管理者回答フォーム"],
    ["修正リクエスト審査", "提案されたトイレ修正＋承認/却下"],
]
story.append(make_table(
    ["画面", "機能"],
    admin_flow,
    col_widths=[45*mm, W-45*mm]
))
story.append(PageBreak())

# ════════════════════════════════════════
# 9. セキュリティ設計
# ════════════════════════════════════════
story.append(heading_bar("9. セキュリティ設計"))

story.append(Paragraph("9.1 認証", S_H2))
story.append(bullet("パスワードハッシュ化：BCrypt（BCryptPasswordEncoder）"))
story.append(bullet("セッション管理：Spring Security HttpSession（30分タイムアウト）"))
story.append(bullet("OAuth2：Googleログインによる自動ユーザー作成"))
story.append(bullet("ログイン失敗：一時停止/削除アカウント専用のエラーコード"))

story.append(Spacer(1, 3*mm))
story.append(Paragraph("9.2 認可 (RBAC)", S_H2))
story.append(make_table(
    ["リソース", "公開", "ROLE_USER", "ROLE_ADMIN"],
    [
        ["メインページ / 地図", "O", "O", "O"],
        ["トイレ検索API", "O", "O", "O"],
        ["レビュー一覧（ぼかし表示）", "O（ぼかし）", "O（完全表示）", "O（完全表示）"],
        ["レビュー作成", "X", "O", "O"],
        ["マイページ", "X", "O", "O"],
        ["トイレ提報", "X", "O", "O"],
        ["コンテンツ通報", "X", "O", "O"],
        ["管理者ダッシュボード", "X", "X", "O"],
        ["ユーザー管理", "X", "X", "O"],
        ["トイレ承認", "X", "X", "O"],
    ],
    col_widths=[45*mm, 30*mm, 30*mm, 30*mm]
))

story.append(Spacer(1, 3*mm))
story.append(Paragraph("9.3 データ保護", S_H2))
story.append(bullet("ソフトデリートパターン：物理削除ではなくdeleted_atタイムスタンプを使用"))
story.append(bullet("ユーザーステータスライフサイクル：ACTIVE → SUSPENDED → DELETED"))
story.append(bullet("ファイルアップロード：UUID接頭辞のファイル名で衝突を防止"))
story.append(bullet("application.propertiesをGit管理外（.gitignore）に設定し、機密情報を保護"))
story.append(bullet("APIエンドポイントのみCSRFを無効化"))
story.append(PageBreak())

# ════════════════════════════════════════
# 10. エラーハンドリング
# ════════════════════════════════════════
story.append(heading_bar("10. エラーハンドリング"))

story.append(Paragraph("10.1 エラーコード体系", S_H2))
story.append(make_table(
    ["エラーコード", "HTTPステータス", "説明"],
    [
        ["TOILET_NOT_FOUND", "404", "指定されたトイレが存在しない"],
        ["REVIEW_NOT_FOUND", "404", "レビューが見つからないか非表示状態"],
        ["INVALID_PASSWORD", "400", "パスワードが8文字未満"],
        ["USERNAME_TAKEN", "409", "ユーザー名が既に登録済み"],
        ["EMAIL_TAKEN", "409", "メールアドレスが既に登録済み"],
        ["NICKNAME_TAKEN", "409", "ニックネームが既に登録済み"],
        ["INTERNAL_ERROR", "500", "サーバー側エラー（ファイルアップロード失敗等）"],
    ],
    col_widths=[40*mm, 25*mm, W-65*mm]
))

story.append(Spacer(1, 5*mm))
story.append(Paragraph("10.2 APIレスポンス形式", S_H2))
story.append(body("すべてのAPIレスポンスは、統一されたJSON構造に従います："))
story.append(Spacer(1, 2*mm))

resp_data = [
    ["success", "Boolean", "true / false"],
    ["data", "Object / null", "レスポンスペイロード"],
    ["message", "String / null", "エラーメッセージ（success=false時）"],
    ["errorCode", "String / null", "エラーコードenum値"],
]
story.append(make_table(
    ["フィールド", "型", "説明"],
    resp_data,
    col_widths=[30*mm, 35*mm, W-65*mm]
))

story.append(Spacer(1, 5*mm))
story.append(Paragraph("10.3 グローバル例外ハンドラー", S_H2))
story.append(bullet("BusinessException：ErrorCodeマッピング付きカスタム例外"))
story.append(bullet("GlobalExceptionHandler：@RestControllerAdviceによる一元的なエラー処理"))
story.append(bullet("未処理の例外はすべてINTERNAL_ERRORとしてHTTP 500を返却"))

# ─── PDF ビルド ───
doc.build(story)
print(f"PDF created: {output_path}")
