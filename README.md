# 🚻 デマス 〜なんか出る気がする〜
> 韓国旅行中の日本人観光客のための公衆トイレ検索サービス
> 
<br>

## 🚽 About Our PROJECT

**デマス (DeMaSu)** は、韓国を訪れる日本人観光客が近くの公衆トイレを簡単に見つけられるよう支援するウェブアプリケーションサービスです。  
韓国の行政安全部が提供する公共データポータルの公衆トイレCSVデータをもとに、Naver Maps APIを活用してユーザーの現在地に基づいた地図検索機能を提供しています。
<br>
<br>
## 🗓 Period

2026.03.01 ~ 2026.03.22 (約3週)
<br>
<br>

## 👥 MEMBERS

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/thisisminseon">
        <img src="https://github.com/thisisminseon.png" width="120" /><br />
        <b>パク・ミンソン</b>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/aaaea1">
        <img src="https://github.com/aaaea1.png" width="120" /><br />
        <b>ハン・スンヨン</b>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/yeeun-021120">
        <img src="https://github.com/yeeun-021120.png" width="120" /><br />
        <b>キム・イェウン</b>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/minone64">
        <img src="https://github.com/minone64.png" width="120" /><br />
        <b>キム・ジュハ</b>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/JiyoonOfficial">
        <img src="https://github.com/JiyoonOfficial.png" width="120" /><br />
        <b>パク・ジユン</b>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/anghi-kor">
        <img src="https://github.com/anghi-kor.png" width="120" /><br />
        <b>チャン・ヒエ</b>
      </a>
    </td>
  </tr>
</table>
<br>
<br>

## 🛠 Tech Stack
### Environment
![IntelliJ IDEA](https://img.shields.io/badge/IntelliJ%20IDEA-000000?style=for-the-badge&logo=intellijidea&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)

### Development
![Java](https://img.shields.io/badge/Java%2017-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-6DB33F?style=for-the-badge&logo=springboot&logoColor=white)
![Spring Security](https://img.shields.io/badge/Spring%20Security-6DB33F?style=for-the-badge&logo=springsecurity&logoColor=white)
![MyBatis](https://img.shields.io/badge/MyBatis-000000?style=for-the-badge&logo=mybatis&logoColor=white)
![Thymeleaf](https://img.shields.io/badge/Thymeleaf-005F0F?style=for-the-badge&logo=thymeleaf&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

### Database
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)

### API
![Naver Maps](https://img.shields.io/badge/Naver%20Maps-03C75A?style=for-the-badge&logo=naver&logoColor=white)
![Google OAuth2](https://img.shields.io/badge/Google%20OAuth2-4285F4?style=for-the-badge&logo=google&logoColor=white)

### Collaboration
![Figma](https://img.shields.io/badge/Figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white)
<br>
<br>

## 📁 プロジェクト構造

```
src/main/java/com/jsl26tp/jsl26tp/
├── admin/ # 管理者ダッシュボード
├── auth/ # 認証 (ログイン/会員登録/OAuth2)
├── common/ # 共通レスポンス処理
├── config/ # Spring Security, Web設定
├── home/ # メインページ
├── inquiry/ # お問い合わせ機能
├── mypage/ # マイページ
├── report/ # 通報機能
├── review/ # レビュー CRUD
└── toilet/ # トイレ CRUD, 検索
```
<br>
<br>

## ✨ Key Features

### 🗺 地図ベースのトイレ検索
- 現在地ベースの周辺トイレ表示
- 地域別ドロップダウン + キーワード検索
- タグフィルタリング (24時間, ビデ, 車椅子, 非常ベル等)
- 位置情報未許可時、ソウル市庁基準で自動検索

### 📝 レビューシステム
- トイレ別レビュー作成/修正/削除
- 星評価 + タグ + 写真添付
- 未ログインユーザーのレビューぼかし処理 (ログイン誘導)

### 👤 ユーザー
- 会員登録 / ログイン / Google OAuth2 ソーシャルログイン
- プリセットプロフィールアイコン選択
- マイページ (最近の閲覧, マイレビュー, お問い合わせ履歴)

### 🔧 管理者
- 管理者ダッシュボード
- トイレ情報の修正提案管理
- ユーザー通報処理
- ユーザーアカウント管理
