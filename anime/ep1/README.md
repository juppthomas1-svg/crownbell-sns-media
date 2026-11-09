# アニメPR EP1「金の切符」（作業中）

台本と指示文のドキュメント：https://claude.ai/artifact/M546xMGDZazfVNi25FFK8w
動画は Google Flow（flow.google.com、Veo 3.1 Lite、9:16、見えるロゴはオフ）でオーナーが作る。1日50クレジット（毎日 19:50 に戻る）、動画1本10。

## できたもの（src/、すべて 720×1280・24fps・8秒）
- s1_ken_sitting.mp4：雨の夜、グレーのセットアップのケンが落ち込む
- s2_ticket_catch.mp4：窓から金の切符が舞い込み、ケンが受け取る
- s3_ticket_pov.mp4：ケンの目線、横長で文字なしの金の切符

## 編集
- work/ticket.py：s3 の切符を追いかけて「BUSINESS ENGLISH／ビジネス英語実務検定／国際ビジネス言語認定協会」を浮かび上がらせ、1.6秒でドン＋紺×金の帯（track.npy が切符の位置、s3.wav がドンの音）
- zenhan_draft.mp4：前半つなぎ試作（s1 0–3.2秒＋字幕「書類選考、また通らなかった。」→ s2 0.3–8秒を1.3倍速 → s3 文字入り 0–4秒）
- 直すところ：字幕をもう少し下へ（ケンの胸にかかる）。BGM は全部そろってから通しで付ける。

- s4a_realization.mp4（2026-11-09 受け取り）：ケンがハッとする。切符に崩れた文字が出ているので、work/s4a_cut.mp4 で 1.2〜4.8秒を使い、下を切って切符を隠した

## 残り（オーナーが 10/30 19:50 以降に作る）
- 4a：ケンの顔にズーム → ハッとする
- 4b：扉を開けて金の光の中へ飛び出す
- 5：扉を抜けると NY の高層ビル。紺のスーツ・赤いネクタイ・オールバック（横から）
- 6：夜景のオフィスで、白人男性・黒人女性・ラテン系女性と楽しく打ち合わせ
- 最後の画面：初級の受験料 12/25 申込まで無料、検索＋QR（TT）／プロフィールのリンク（IG）、民間資格・合格や就職を約束しない・AIで作成したイメージ
- 投稿時は AI 生成の申告をオン（TikTok isAigc、インスタ isAiGenerated）
- ナレーションを入れるかは、オーナーの返事待ち

## 後半の指示文（2026-11-09 作成・Flow にそのまま貼る）
ケンの顔をそろえるため、work/ken_ref_standing.jpg（場面2の最後のケン）を「画像から動画」の参照画像に使う。

### 4a ハッとする
```
Extreme close-up on KEN's face in the same dark apartment room at night, rain on the window behind him. KEN: a 23-year-old Japanese young man, original stylized 3D animated character, short neat black hair, light gray suit, white shirt, gray tie, round friendly face, big expressive eyes, does not resemble any real person. Warm golden light from a ticket below glows on his face. Slow push-in to his eyes; his eyes widen, he takes a small breath, and his expression shifts from tired sadness to sudden realization and quiet determination. Style: premium stylized 3D animated film look, cinematic lighting, shallow depth of field, deep navy and warm gold color palette, vertical 9:16, no on-screen text, no logos, no brand names.
```

### 4b 扉を開けて光の中へ
```
The same dark apartment room at night. KEN, the same character (a 23-year-old Japanese young man, original stylized 3D animated character, short neat black hair, light gray suit, white shirt, gray tie, does not resemble any real person), holding a glowing blank golden ticket, walks to the front door and pushes it open. Brilliant warm golden light floods in through the doorway, gold sparkles swirl around him, and he steps forward into the light. Camera follows from behind, then the light fills the frame. Style: premium stylized 3D animated film look, cinematic lighting, deep navy and warm gold color palette, vertical 9:16, no on-screen text, no logos, no brand names.
```

### 5 NY の高層ビル（変身したケン）
```
Golden light fades to reveal a grand avenue of glass skyscrapers in a global city at dusk, city lights turning on. KEN, the same character, now transformed: a 23-year-old Japanese young man, original stylized 3D animated character, black hair neatly slicked back, tailored navy suit, crisp white shirt, red tie, does not resemble any real person. He walks forward with calm confidence, seen from the side in a smooth tracking shot, skyline glowing behind him. Style: premium stylized 3D animated film look, cinematic lighting, shallow depth of field, deep navy and warm gold color palette, vertical 9:16, no on-screen text, no logos, no brand names.
```

### 6 夜景のオフィスで打ち合わせ
```
A modern high-rise office meeting room at night with floor-to-ceiling windows and a glittering city skyline. KEN, the same character (a 23-year-old Japanese young man, original stylized 3D animated character, slicked-back black hair, navy suit, white shirt, red tie, does not resemble any real person), leads a friendly discussion around a table with three international colleagues: a Caucasian man, a Black woman and a Latina woman, all original stylized 3D animated characters in business attire, none resembling any real person. They smile, nod and point at a tablet together; warm, energetic teamwork. Slow orbiting shot. Style: premium stylized 3D animated film look, cinematic lighting, shallow depth of field, deep navy and warm gold color palette, vertical 9:16, no on-screen text, no logos, no brand names.
```
