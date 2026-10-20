# 自動運用の手順書（予約タスクが毎回これを読んで動く）

オーナー：辻 佑介（トーマス）。関西弁で、簡単に、短く報告する。SNS には一切触れたくない人。
頼まれていないことは勝手に変えない。大きな変更は「案」として報告に書き、OK をもらってから。

## 0. 最初に読むもの（この順で。ぶつかったら上が勝つ）
1. rules/00_最優先ルール.md
2. rules/02_SNS運用メモ_最新.md
3. rules/01_自動運用メモ.md
4. log/posted.md（これまでに出したネタ。同じネタ・同じ動画は二度と出さない）

## 1. 先週の数字を見る（Metricool, blogId 7511201, timezone Asia/Tokyo）
- getAnalyticsAvailableMetrics で TikTok（connector: posts）と Instagram（reels）の指標を確認し、
  getAnalyticsDataByMetrics で前回実行以降の投稿ごとの再生・いいね・保存・シェアを取る。
- 伸びた投稿の共通点（フックの型、時間、ネタの種類）を1〜3行でまとめる。

## 2. 次の期間の投稿を決める
- 期間：この実行日の翌日から、次の実行日まで。
- 本数：Metricool 無料プランは月20投稿まで（X 不可）。今月すでに予約・公開した本数を getScheduledPosts と log/posted.md で数え、
  月末まで毎日出せるように均等に割る（足りなければ1日1本、TikTok とインスタを交互）。上限を絶対に超えない。
  ※オーナーが有料プランに切り替えたと rules/00 に書いてあれば、メモどおりの本数（TikTok 1日2〜3本、インスタ 1日1〜2本、X も）にする。
- 時間：TikTok もインスタも **朝7:30** が基本（オーナー指示）。2本目以降を出せるときは 12:00・21:00。土日は 8〜10時・19〜22時。
- 割合：クイズ多め、宣伝少なめ（目安 4:1）。宣伝は連続させない。
- クイズ：人物入り（"figure": true）が基本。毎回オリジナル。本番の問題・お試しの問題・log にあるネタは使わない。選択肢は本当に迷うもの。正解の位置は A/B/C で偏らせない。
  - TikTok：フックは軽いあおり、または「正解できたらすごい」系（例：この英語が分からないなら、正直まずいです。）
  - インスタ：「『〇〇』英語で言えますか？」形式が強い
- 宣伝：人物入り（"figure": true、rules/00 参照）＋ターゲットの帯（"target": "就活生必見" など）が基本。最初に課題（書類選考が通らない／ガクチカが思いつかない／履歴書がスカスカ／資格欄が空白）→ 解決（検定）。
  宣伝は毎回同じ形にせず、新しい型も1つ試す（rules/00 の「宣伝動画は新しい試みも」参照）。安っぽく見えるものは作らない。
  合格や内定を約束しない。「※合格した場合」「最短」「民間資格」を必ず添える。「ガクチカになる」とは言わない。

## 3. 動画を作る
- content/ に新しい JSON を作る（形式は content/week1.json と同じ。kind=quiz|promo、platform=tt|ig）。
- `bash gen/make.sh content/<新しいファイル>.json` → videos/<id>.mp4（10秒・60fps・音あり）と表紙ができる。
- TikTok・インスタ用（platform が tt / ig）は自動で「safe」配置になる。上160px・右170px・下470px は TikTok/インスタのボタンや投稿文が重なる場所なので、大事な文字・QR・人物の顔や合格証が入っていないか必ず確認する（gen/ttmask.py（使い方: python3 -I gen/ttmask.py 出力.png コマ1.png コマ2.png ...） と同じように赤くぬって確認するとよい）。
- コマの書き出しは node gen/snap.js <作業フォルダ> <id> 0 1600 4000 6300 9000（gen フォルダの中で実行）
- 全部の動画で、0秒（表紙。最初から文字が全部見えていること）・1.6秒・4秒・6.3秒・9秒のコマを書き出して目で見る。文字のはみ出し・折り返しの崩れ・重なりがあれば直して作り直す。
- git add → commit → push（videos/ と content/ と log/）。

## 4. Metricool に予約する
- media は `https://raw.githubusercontent.com/juppthomas1-svg/crownbell-sns-media/main/videos/<id>.mp4`（作り直した動画は同じ名前だと古いのが使われることがあるので、<id>_v2.mp4 のように新しい名前で置く）
- TikTok：tiktokData に title（20字以内の見出し）、privacyOption は PUBLIC_TO_EVERYONE、commercialContentOwnBrand は true、isAigc は false。
  firstCommentText は使わない（TikTok には付かない）。本文の最後の行に URL だけ：https://crownbell-kentei.netlify.app/tiktok
- インスタ：instagramData の type は REEL、videoCoverMilliseconds は 1600。本文は「プロフィールのリンクから」で締める。
- 本文 = caption + 改行 + tags（ハッシュタグ3〜5個）。TikTok はさらに改行 + caption_tail（URLだけの行）。
- 予約したら log/posted.md に「日付 時刻｜SNS｜id｜ネタ」を1行ずつ足して push。

## 5. オーナーに報告（SendUserMessage で。短く、関西弁で）
- 先週の数字（いちばん伸びた投稿と、その理由の見立て）
- 今回予約した一覧（日時・SNS・ネタ）
- 今月の残り投稿数
- 気づいたこと・提案（あれば1〜2個。実行はせず案として）
- 「気になる投稿があったら Metricool で消してな（消さんかったらそのまま出る）」の一言
