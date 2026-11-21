# 04 AIが作ったように見える文章・デザインの特徴（調査メモ）

対象：大学入試向け英文法教材（日本語解説＋英語例文、印刷用PDF、黒・赤・灰色網の3色）。
目的：AI生成物に典型的な特徴を避け、市販の学習参考書として通用する見た目と文章にする。

> 調査日：2026-11-21。根拠は実際に開いて読んだ資料に限り、末尾の「出典一覧」で確認状況を示す。チェックリストと禁止語リストは本文の後半にある。

---

## 調査メモ（根拠）

### A. 英語：LLMが多用する語

#### A-1. Kobak et al.（arXiv 2406.07016, 2024 → Science Advances 11(27), 2025）
- 2010〜2024年の PubMed 抄録 1,500万件超を対象に「超過語（excess words）」を分析。2024年抄録の**少なくとも13.5%**がLLMで処理されたと推定（分野・国・雑誌により約40%に達する）。
- 2024年の超過語は454語で、うち379語が「文体語」（内容語ではない）。2021年（コロナ）の超過語は190語で、ほぼすべて内容語。
- 本文で数値が出ている語：**delves**（頻度比 r=28.0）、**underscores**（13.8）、**showcasing**（10.7）、**potential**（頻度差 δ=0.052）、**findings**（0.041）、**crucial**（0.037）。
- 頻出の「共通セット」10語：across, additionally, comprehensive, crucial, enhancing, exhibited, insights, notably, particularly, within。
- 稀な語のセット（291語、付録 Figure S6）に delve, intricate, showcasing など。
- 注意：対象は医学論文の抄録。例文の語彙とは文体が違う。それでも、入試英語の例文で delve / showcase / underscore / crucial / intricate が続けて出れば不自然。

#### A-2. Wikipedia "Signs of AI writing"（WikiProject AI Cleanup によるガイド、2026年11月閲覧）
- **AI語彙**：Additionally（特に文頭）, align with, boasts（「持つ」の意味で）, bolstered, crucial, deep dive, delve, emphasizing, enduring, enhance, fostering, garner, highlight（動詞）, interplay, intricate/intricacies, landscape（抽象名詞）, meticulous(ly), pivotal, robust, showcase, tapestry（抽象名詞）, testament, underscore（動詞）, valuable, vibrant。
- 時期別の傾向：GPT-4期（2023〜2024年半ば）は delve, tapestry, testament など。GPT-4o期（2024年半ば〜2025年半ば）は align with, fostering, showcasing など。GPT-5期以降は emphasizing, enhance, highlighting, showcasing。2026年半ば以降は challenge, clearer, dependable, echoed, foster, leverage, matters, multifaceted, practical, prioritize, quietly, steady, universally。文がより短くなる（8〜20語程度）傾向も記載。
- **重要性の誇張**：stands/serves as, is a testament/reminder, a crucial/pivotal/vital/significant/key role/moment, underscores/highlights its importance, reflects broader, symbolizing its ongoing/enduring/lasting, setting the stage for, evolving landscape, focal point, indelible mark, deeply rooted。
- **表面的な分析**：文末に -ing 分詞を付けて意義づけする（highlighting…, ensuring…, reflecting…, contributing to…, fostering…）、valuable insights, align/resonate with。
- **be動詞の回避**：serves as / stands as / functions as / represents、boasts / features / offers。
- **否定の並列**：not only… but also…, It's not X, it's Y, no X, no Y, just Z。
- **三点セット**（rule of three）："adjective, adjective, and adjective"。
- **見た目**：見出しのタイトルケース、太字の多用、太字ラベルで始まる箇条書き（inline-header vertical lists）、見出しや箇条書き頭の絵文字、カーリー引用符。
- **対話の残り**：I hope this helps, Certainly!, Of course!, You're absolutely right!, Would you like…, let me know, here is a…。
- **当てにならない指標**（ページ自身が明記）：文法が完璧、文体が平板、格調高い文体、Additionally / Notably などの接続語だけでは判定できない。単語1つで断定せず、**密度**で見る。

#### A-3. Liang et al.（2024）2本
- **"Monitoring AI-Modified Content at Scale"**（arXiv 2403.07183、ICML 2024）：AI系学会の査読コメントの 6.5〜16.9% がLLMで大きく書き換えられた可能性があると推定。Figure 1 では ICLR 2024 の査読で、文に含まれる確率が **commendable 9.8倍・meticulous 34.7倍・intricate 11.2倍**に増えた。
  - 付録A（偏りの大きい形容詞の上位）：commendable, innovative, meticulous, intricate, notable, versatile, noteworthy, invaluable, pivotal, potent, fresh, ingenious, cogent, ongoing, tangible, profound, methodical, laudable, lucid, appreciable, fascinating, adaptable, admirable, refreshing, proficient, intriguing, thoughtful, credible, exceptional, digestible …
  - 付録B（同、副詞の上位）：meticulously, reportedly, lucidly, innovatively, aptly, methodically, excellently, compellingly, impressively, undoubtedly, scholarly, strategically, intriguingly, competently, intelligently, hitherto, thoughtfully, profoundly, undeniably, admirably, creatively, logically, markedly, thereby, contextually, distinctly, judiciously, cleverly, invariably, successfully …
  - 注意：査読という「評価する文章」での偏り。例文に褒め言葉の形容詞が並ぶと、この型に近づく。
- **"Mapping the Increasing Use of LLMs in Scientific Papers"**（arXiv 2404.01268、2024）：2020〜2024年の約95万本の論文を分析。LLMで書き換えられた割合はCS分野で最大17.5%、数学と Nature 系で最大6.3%。Figure 2 では arXiv CS 抄録で最も偏りの大きい4語として **realm, intricate, showcasing, pivotal** を示す（2022年まで低頻度で、2023年から急増）。

#### A-4. 例文の登場人物名の偏り
- Hamilton & Mimno（Cornell、EMNLP 2026 "Elias in the Lighthouse, Again? Diagnosing Low Diversity in LLM Stories"）。Cornell Chronicle 2026-10-19 の紹介記事で確認（論文本文は未確認）。ChatGPT・Claude・Gemini・OLMo に「物語を書いて」と頼み、2万件を分析。約90%が11個の頻出語のどれかを含み、半数以上に灯台が出る。記事が挙げる語：lighthouse, keeper, **Elias, Mara, Elara**。
- 依頼文の「Sarah / Emily に偏る」という点：**直接の量的研究は見つからなかった**。報道（404 Media、Gizmodo、Vice）やブログでは Elara Voss, Elias Thorne, Marcus Chen, Sarah Chen などが「AIの定番名」とされるが、本文は開いておらず未確認。
- 教材への応用：名前の偏りそのものより、**同じ少数の名前を使い回すこと**と、**英米の白人名＋アジア系の姓1つ**という型が目印になる。例文の人物名は、入試の過去問や市販の参考書と同じく、ありふれた名前（Tom, Ken, Mary, Mr. Brown など）を散らして使い、同じ名前の連続は数で制限する。

#### A-5. 文の長さが均一になる
- Muñoz-Ortiz, Gómez-Rodríguez & Vilares（2024, *Artificial Intelligence Review* 57:265, arXiv 2308.09067。査読あり）：ニュース文で比較すると、人間の文の長さは**ばらつきが大きく**、語彙も多様。LLMは数字・記号・助動詞・代名詞が多い。LLM同士の差より、人間とLLMの差の方が大きい。
- ただし「burstiness（文長のばらつき）」は新しいモデルほど差が小さく、指標そのものにも異論がある（検索結果の要約から。個別論文の本文は未確認）。**判定には使わず、例文集の点検指標（参考値）として使う**のが妥当。
- 教材への応用：例文の語数分布を出す。3〜25語に散らばっているか、同じ長さの例文が並んでいないかを見る。入試の例文には "I know the man who lives there." のような短い文も多い。

#### A-6. 抽象的・説教的な例文（調査からの推論）
- Wikipedia ガイドの「重要性の誇張」「表面的な分析」「三点セット」は、例文にすると次の形になる：
  - × *Education is a key that opens the door to a brighter future.*（抽象・教訓）
  - × *The library, which stands as a testament to the town's rich history, fosters a vibrant community.*（AI語彙の集中）
  - ○ *The library which my father used to visit closed last year.*（具体的・日常的、文法項目が主役）
- 直接の研究は見つかっていない。ここは**推論**として扱う。

### B. 日本語：AIっぽい日本語の特徴

**資料の状況**：日本語のAI文体を数で調べた研究は少ない。今回本文まで読めたのは、査読のない卒業論文1本（大西 2026）、英語圏ツール企業の調査ページ1本（Pangram）、雑誌記事1本（PRESIDENT Online）、個人の開発者ブログ1本のみ。依頼文の「〜しましょう！」「まとめると」「三点セット」については、**日本語での量的な裏付けは見つからなかった**。下の項目は、実測（◎）と、記事・意見レベル（△）を分けて書く。

#### B-1. 大西夢「AI生成文からみた『自然な日本語』についての研究」（広島大学文学部 卒業論文、令和7年度＝2025年度）◎（ただし小規模・査読なし）
- 方法：予備調査は20代16人に AI生成文6本・人間の文3本を読ませて自由記述を集めた（148件）。本調査は「少子高齢化の意見文」と「旅の思い出の作文」の2題で、AI 5種（ChatGPT(GPT-3.5)・Claude・Copilot・Gemini・Grok）各2本と人間10人の文章（約500字）を比較。
- 読み手が「AIらしい」と感じた点（予備調査）：**具体性がない**（「テンプレートのよう」「誰にでも当てはまる」「当たり障りのない」など14件で最多）、日常で使わない抽象語（「福音」「迂回路」「あの夏」）、読点の違和感、文末がワンパターン、大げさな感情表現、説明的な表現、ジャンルの型からずれた表現（「〜にしては○○すぎる」）。
- 実測で分かったこと（本調査）：
  - **均一性**：一文の長さ、読点の数、段落あたりの文数のばらつきが小さい。**極端に長い文・短い文が出にくい**。
  - **接続詞の偏り**：意見文で AI は「一方」「しかし」「また」だけを使い、特に「また」が多い。人間は「あるいは」「そして」「ただ」なども使う。作文では AI は「そして」「また」のみ。
  - **文末の偏り**：意見文では AI の文末の75%以上が「である」「だ」「ている」「ある」「ない」の5種。意見を表す「たい」「思う」「か」は AI で0回、人間では多い。作文では AI に「ている」が多い（人間は155文中9回）。
  - **断定を避ける・一般論に逃げる**：意見文で個人の意見より一般的な事実を述べる。作文でも婉曲・抽象表現を使う。
  - 読点は AI の方がやや多いが、差は大きくない。
- 筆者の整理：AI文の特徴は「均一性／画一性」「ジャンルへの適応（むしろ上手な点）」「技術的な未熟さ（婉曲、一般論、個人の文体が出ない）」の3つ。
- 注意：AIの文章の方が型に沿っている面もあり（意見文で「考える」を使うなど）、「型どおり＝AI」とは言えない。

#### B-2. Pangram「AIによる文章の特徴」（AI検出ツール企業のページ、日付なし）△（企業の調査、方法は簡略）
- 人間とAIの文書数百万件で、1万語あたりの出現頻度を比較。
- マークダウン（太字・見出し）**12倍**、AI定番フレーズ12倍、長ダッシュ（—）10倍、**箇条書き9倍**、**三つ組表現4倍**、「XだけでなくYも」3倍、珍しいUnicode文字3倍、「もちろんです！」型の導入2倍、絵文字2倍（ただし絶対数は少ない）。
- 日本語ページだが、コーパスが日本語かどうかは明記されていない。

#### B-3. 中山順司「AIで作った文章を見抜くたった一つのフレーズ」（PRESIDENT Online、2026-05-07）△（経験にもとづく意見、後半は有料で未読）
- 挙げている特徴：「これにより」型の前置き、「正直に言うと」の後に一般論、同義反復（「柔軟な対応が必要です。そのためには、適応力を高めることが重要です」）、固有名詞・数値がない（「近年、観光業界が注目されています」）、曖昧表現（「多くの企業で」「さまざまな課題」「効果が期待されます」）、抽象語（対応・改善・最適化・推進）、**理由のない「〜が重要です」「〜が必要です」**、**「〜といえるでしょう」**「バランスが重要です」、文の長さが一定で「です・ます」が続く。

#### B-4. Ken Imoto「We measured 180 AI-generated Japanese articles」（DEV Community、2026）△（個人の計測、Zenodo 稿あり。人間側の基準は Qiita 記事7本のみ）
- 6つのLLMで技術ブログ記事180本を作成し16指標で採点。語彙指標（1,000字あたり）は人間0.44に対し Claude 1.52、GPT-4o 1.98。構造（見出し・箇条書き）の指標は文字数で割っていなかったため、後に**撤回**。
- 「さまざまな」「効率的な」を中身のない埋め草の例とし、「いかがでしたでしょうか」を最大の目印とするが、数値はない。別記事の指摘によると「いかがでしたか」はAI以前のSEO記事の型で、AI特有ではない（記事本文は未確認）。

#### B-5. 日本語のまとめ（教材向けの解釈）
- 根拠が比較的しっかりしているもの：**具体性の欠如**、**文長・段落長の均一さ**、**接続詞と文末の偏り**（「また」の多用、同じ文末の連続）、**一般論・婉曲への逃げ**、**マークダウン（太字・見出し）と箇条書きの多用**、**三つ組**。
- 記事・意見レベルのもの：「〜といえるでしょう」「〜が重要です」「さまざまな」「効果が期待されます」「〜しましょう！」「まとめると」「いかがでしたか」。単独では判定に使えないが、**参考書の解説文には本来不要な表現**なので、削っても損はない。

### C. 見た目：AI生成デザインの特徴

**資料の状況**：すべてウェブUI（ランディングページ、アプリ画面）についての**デザイナー・開発者の記事やツールの規則集**で、査読研究はない。印刷物の参考書に直接あてはまるものではないが、「ウェブ風の飾り」が紙面に持ち込まれるとAIっぽく見えるという点で使える。

#### C-1. Anthropic "Improving frontend design through Skills"（Rajasekaran, Wei, Bricken ほか、2025-11-12）△（AI開発元の解説記事）
- モデルは学習データの「最も典型的な」出力に寄り、ユーザーが **"AI slop" aesthetic** と呼ぶ見た目になる。具体的には「**Inter フォント、白背景に紫のグラデーション、控えめなアニメーション**」。
- 避けるもの：汎用フォント（Inter, Roboto, Arial, Open Sans, Lato, システムフォント。Space Grotesk にも収束しがち）、決まりきった配色（特に白地に紫グラデーション）、予測可能なレイアウトと部品パターン、文脈に合った個性のない量産型デザイン。

#### C-2. 同スキルの改訂（2026-06）についての紹介記事（Ken Imoto, DEV Community, 2026-07-03）△（第三者の紹介。スキル本文は未確認）
- 「いまのAI生成デザインは3つの見た目に集まっている」として、(1) 温かいクリーム色の背景（#F4F1EA 付近）＋コントラストの強いセリフ見出し＋テラコッタ色のアクセント、(2) ほぼ黒の背景＋蛍光グリーンや朱色のアクセント1色、(3) **細罫・角丸なし・新聞のような密な段組み（broadsheet）**。どれも「選んだものではなく既定値」とされる。
- **教材への含意**：「細罫・角丸なし・段組み」は日本の参考書の正統な組版でもある。ウェブ上のAIデザインがこの見た目に寄ってきているので、**罫を使うこと自体が人間らしさの証明にはならない**。罫・段組みは飾りとしてではなく、参考書の慣習（柱・ノンブル・見出し体系）と一緒に、機能があるところだけに使う。

#### C-3. Kosta Canatselis "Spot the slop: a UI designer's guide to fixing AI defaults"（2026-07-23）△（デザイナーのブログ）
- Inter だけのフォント指定、紫→青のグラデーション、中身のない見出し（"Build the future of work"）、**余白・角丸・カードの高さがすべて同じ（均一さ）**、空・読み込み・エラー状態の未設計、同じフェードインの多用、全部を同時に見せる。パネル左端の色付きの線（角が丸い）にも触れている。
- 直し方：主役を大きく重く近くし、脇役を下げる「意図的な差」。色は飾りでなく役割で名づける。

#### C-4. 925studios "AI Slop Fonts and Gradients"（2026、デザイン会社のブログ）△
- Inter、インディゴ→紫のグラデーション（Tailwind の indigo-500 既定値に由来とする）、グラデーションのボタン、**同じ間隔に並ぶ角丸カード3枚（"three-card reflex"）**、カードの淡い影、どの製品にも合う細線アイコン、中身のない見出し（"Build faster. Ship smarter."）。

#### C-5. pixelslop "AI Slop Pattern Catalog"（npm パッケージ pixelslop@0.3.8 同梱の規則集）△（検出ツールの規則。数値の閾値つき）
- 自動検出の規則が具体的なので、検査スクリプトの参考になる。印刷教材に関係するもの：
  - グラデーション文字（`background-clip: text`）、紫→青グラデーション
  - **同一サイズのカード格子**（3つ以上の同じ大きさ・同じ構造の子要素）
  - **角丸（8〜20px）＋影のボックス**が4個超、カードの入れ子
  - **片側だけ太い枠線**（1辺≥3px・他の2辺以上<2px）が2個超 ＝ 色付き左ボーダー
  - **見出しの上にアイコン**（h2〜h4 の直前に SVG・画像）が3つ以上
  - 全部中央揃え（70%超）、余白の値が2種類以下（均一な余白）
  - 見出しと直後の段落で語の40%超が重複（言い換えの繰り返し）
  - ソース検査：`bg-gradient-to-`、`box-shadow`/`shadow-lg`、Inter/Roboto/Open Sans の読み込み
- 規則にない項目：英字大文字の小見出し（eyebrow）、絵文字見出し、ピル型バッジ。

#### C-6. Laith0003 "Anti AI slop ban list"（GitHub wiki、2026-11 最終更新）△（個人の規則集）
- 禁止：**見出し・本文・UIの絵文字**、虹色グラデーション文字、**同じカード3枚の横並び**、重い影、全カードの光彩、すりガラス効果、**すべて同じ角丸**、Title Case、**全部中央揃え**、セクション間に同じ区切り線、"John Doe" などの仮名、切りのいい数字の統計、"empower"/"leverage" などの埋め草動詞、前置きの多い導入。
- 一方で、短いラベルの英大文字やピル型（完全な角丸）は**許容**している。「英字大文字ラベル」がAIの目印かどうかは資料により意見が割れる。

#### C-7. 見た目のまとめ（印刷教材向けの解釈）
- 複数の資料が一致して挙げるもの：**グラデーション**、**角丸カード＋影**、**同じ大きさのカードの格子**、**均一な余白・角丸**、**絵文字・汎用アイコン**、**中身のない見出し**、**Inter などの既定フォント**。
- 1つの資料だけのもの：色付き左ボーダー（Canatselis、pixelslop）、見出し上のアイコン（pixelslop）。
- 英字大文字の小見出し（"POINT" "CHECK" "TIPS"）：AIの目印とする根拠は**見つからなかった**。ただし日本の参考書でも「POINT」「CHECK」は昔から使われるので、**AIっぽさより「ウェブ風か参考書風か」で判断**する（D節）。

### D. 組版：日本の市販参考書らしさと、ウェブページ風の要素

**資料の状況**：W3C「日本語組版処理の要件（JLReq）」で、柱・ノンブル・約物・禁則の基本は確認できた。**学習参考書に特有の組版（2色刷り、網、赤シート対応、見出し体系）を説明した公開資料は見つからなかった**（出版社の編集マニュアルやデザイナーのインタビューを検索したが該当なし）。下の「参考書の慣行」は、JLReq で確かめられる部分と、一般に流通する参考書の慣行（**出典未確認、要実物確認**）を分けて書く。

#### D-1. JLReq（W3C Working Group Note）で確認できたこと ◎
- **版面**：本の基本となる版面（基本版面）を決め、文字サイズ・行長・行数・行間・段数をそろえる。行長は文字サイズの整数倍。本文は9ポイントが一般的。
- **柱とノンブル**：位置は基本版面を基準に決める。柱は「両柱」（偶数・奇数の両ページ）と「片柱」（奇数ページのみ）があり、両柱では**偶数ページに上位の見出し（章名）、奇数ページに下位の見出し（節名）**を入れるのが普通。横組みのノンブルはアラビア数字。長すぎる柱は見栄えが悪いので短くする。
- **約物**：句読点・括弧・中点は半角幅が基本で、かなや漢字の隣では二分や四分のアキを足して全角に見せる。約物が続く場合はアキを詰める。行末の句点の後は二分アキを保つ。
- **禁則**：閉じ括弧・句点・読点は行頭に置かない。始め括弧は行末に置かない。ぶら下げ組は句読点だけ。
- **ルビ・圏点**：行間を変えない（ルビが入っても行送りは一定）。
- **段落**：段落の頭は全角下げ。見出し直後を天付きにしてもよいが、全段落に天付きを使うと段落の切れ目が分からなくなる。

#### D-2. 市販参考書の慣行（出典未確認・要実物確認）△
- 見出しに**番号の体系**がある（例：第1章／1／(1)／①、または Lesson 1, 2 …）。番号は目次・柱・索引と対応する。
- 柱に章名・項目名、ノンブルは版面の外側（小口側）の下か上。
- 罫は**細罫（0.1〜0.25mm程度）**と、まれに太罫・二重罫。罫には「囲む」「区切る」「表の枠」という役割がある。
- 色は**意味で使う**：赤＝重要語・正解・注意（赤シートで消える前提で使う本も多い）、網＝例題・まとめ表・ポイントの囲み。
- 例文に**番号**（1, 2, 3 … や ①②③）、和訳を下か右に置く。文法項目の部分を**太字・赤字・下線のどれか1つ**で示す（同時に重ねない）。
- 「POINT」「CHECK」「Advice」のような英字ラベルは**日本の参考書でもよく使われる**。ラベル自体は問題ではなく、使う種類を2〜3個に絞り、毎ページ同じ形で使うことが参考書らしさになる。

#### D-3. ウェブページ風の要素（印刷参考書では使わない）
- 角丸カード＋影、ピル型バッジ、ボタン風のラベル、グラデーション、すりガラス、光彩。
- 絵文字、どの本にも合う汎用アイコン、見出しの上に円や角丸四角に入ったアイコン。
- 色付きの太い左ボーダーだけの囲み（ブロック引用風・通知風）。
- 同じ大きさのカードを2列・3列に均等に並べる格子。
- 青い下線つきリンク色、「クリック」「タップ」「スクロール」「詳しくはこちら」「→ 次へ」など画面操作の言葉。
- 1行ごとの段落、段落の間に空行（ウェブ式の段落分け）。全角下げをせず空行で段落を区切る形。
- 見出しが全部同じ大きさ・同じ形（見出しのレベルに差がない）。
- 余白・囲み・角丸がすべて同じ値（C-3、C-5 の「均一さ」）。

---

## 「避けること」チェックリスト

判定の基本方針（Wikipedia ガイドの「当てにならない指標」と大西 2026 を踏まえる）：**1語・1か所で「AIっぽい」と判断しない。密度と偏りで見る。** 自動検査は「候補を出す」ためのもので、最終判断は人が読む。

正規表現は PCRE／Python `re` 形式。`TEXT` は解説の日本語本文、`EX` は英語例文、`SRC` は HTML/CSS ソースを指す。

### 1. 文章（日本語の解説）

| # | 避けること | 根拠 | 検出方法（自動検査） |
|---|---|---|---|
| J1 | 読者への呼びかけ・号令（「〜しましょう！」「〜してみましょう」「覚えておきましょう」） | 記事レベル（B-5）。参考書の地の文では不要 | `TEXT`: `しましょう[！!]?` `てみましょう` → 1章で3回を超えたら要確認。`！` は解説文では0回を目標：`[！!]` |
| J2 | 理由のない「〜が重要です」「〜が大切です」「〜が必要です」 | 中山 2026（B-3） | `(重要|大切|必要|大事)(です|である|だ)[。！]` を数え、直前の文に理由（「〜ので」「〜ため」「なぜなら」）がないものを拾う |
| J3 | 断定回避の決まり文句（「〜と言えるでしょう」「〜と考えられます」の連続、「〜かもしれません」） | 中山 2026、大西 2026（婉曲・一般論に逃げる） | `(と言|とい)えるでしょう` `と考えられ(ます|る)` `かもしれません` → 文法の説明では原則0回 |
| J4 | 締めの決まり文句（「まとめると」「いかがでしたか」「以上のように」「このように〜ことがわかります」） | B-4、B-5（記事レベル） | `まとめると` `いかがでした(か|でしょうか)` `以上のように` `^このように` |
| J5 | 埋め草の抽象語（「さまざまな」「多くの」「効果的に」「効率的な」「〜において」「〜を通じて」） | 中山 2026、Imoto 2026 | `さまざまな|様々な|効率的な|効果的(な|に)|多くの場面で` → 1ページ2回超で要確認 |
| J6 | 同じ接続詞の多用（特に「また、」）、接続詞の種類が少ない | 大西 2026（実測） | `(^|。)また、` を数え、全接続詞に占める割合が30%を超えたら要確認。接続詞の種類数も数える |
| J7 | 同じ文末が続く（「〜です。」が3文以上連続、「〜ます。」の連続） | 大西 2026（文末の偏り）、中山 2026 | 文を `。` で区切り、末尾3字を比べ、同じものが3連続したら警告 |
| J8 | 文の長さ・段落の長さがそろいすぎている | 大西 2026（実測）、Muñoz-Ortiz 2024 | 1項目内の文字数の標準偏差／平均（変動係数）が0.25未満なら警告。段落の文数がすべて同じなら警告 |
| J9 | 三点セット（「A、B、そしてC」「〜で、〜で、〜です」を繰り返す） | Wikipedia、Pangram（三つ組4倍） | `[^、。]{1,15}、[^、。]{1,15}、(そして)?[^、。]{1,15}` を数え、1ページ2回超で要確認 |
| J10 | 太字の多用（1段落に2か所以上、文全体が太字） | Wikipedia、Pangram（マークダウン12倍） | `SRC`: `<(strong|b)>` と `**` を段落ごとに数える。1段落1か所まで |
| J11 | 箇条書きの多用（説明を箇条書きで済ませる、太字ラベル＋コロンで始まる箇条書き） | Wikipedia（inline-header lists）、Pangram（9倍） | `^\s*([-*・●■]|\d+\.)\s` の行数／本文行数が0.3を超えたら警告。`^\s*[-*・]\s*\*\*[^*]+\*\*[：:]` は原則0 |
| J12 | 対話・接客の言い回し（「もちろんです」「いい質問ですね」「お役に立てば」「ぜひ〜してください」） | Wikipedia（collaborative communication）、Pangram | `もちろん(です)?[！!、]` `いい質問` `お役に立て` `ぜひ` |
| J13 | 同義反復（「柔軟な対応が必要です。そのためには適応力を高めることが重要です」型） | 中山 2026 | 自動検査は困難。隣り合う2文で内容語の重なりが40%超のものを候補にする（pixelslop #19 の応用） |
| J14 | 具体例のない一般論（「英語では関係詞がよく使われます」で終わる） | 大西 2026（最多の指摘「具体性がない」） | 自動検査は困難。各説明段落に例文番号への参照（`例文\d+` `\(\d+\)` `①-⑳`）があるかを確認 |
| J15 | 長いダッシュ「——」「—」を挿入句に使う | Pangram（長ダッシュ10倍）、Wikipedia（2026年9月まで） | `TEXT`: `—|――|——` → 解説文では0回 |
| J16 | 絵文字・装飾記号（✨✅👉💡、★☆を見出しに） | Wikipedia、Pangram | `[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}\x{2B50}\x{2705}]` → 0回 |

### 2. 英語例文

| # | 避けること | 根拠 | 検出方法（自動検査） |
|---|---|---|---|
| E1 | LLMの多用語（delve, showcase, underscore, tapestry, testament, pivotal, intricate, meticulous, realm, vibrant, foster など） | Kobak 2025、Liang 2024a/b、Wikipedia | 下の「禁止語リスト（英語・強）」を単語境界つきで照合：`\b(delv(e|es|ed|ing)|showcas(e|es|ed|ing)|…)\b`（大文字小文字を区別しない）。1件でも出たら差し替えを検討 |
| E2 | 重要性を誇張する定型句（stands as, serves as a testament, plays a crucial role, a rich history, deeply rooted） | Wikipedia | 「英語・句」リストを照合 |
| E3 | 文末の分詞で意義づけ（…, highlighting the importance of…, …, ensuring that…） | Wikipedia（superficial analyses） | `,\s+(highlighting|underscoring|emphasizing|ensuring|reflecting|symbolizing|contributing to|fostering|showcasing)\b` |
| E4 | 抽象・教訓・説教調の例文（Education is the key to…, Kindness can change the world.） | 推論（Wikipedia の誇張・表面的分析の型）。大西 2026 の「具体性がない」 | 主語が抽象名詞（education, success, life, kindness, technology, knowledge, happiness）で始まる例文を数える：`^(Education|Success|Life|Kindness|Technology|Knowledge|Happiness|Friendship|Hard work)\b`。全例文の10%を超えたら要確認 |
| E5 | 同じ名前の使い回し、AI物語の定番名（Elias, Elara, Mara, Voss, Thorne, Marcus Chen, Sarah Chen） | Hamilton & Mimno 2026（報道で確認）、ほかは未確認 | 大文字始まりの人名を抽出して頻度表を作る。同じ名前が1冊で5回超、または定番名リストに当たれば警告 |
| E6 | 例文の長さがそろいすぎる（どれも12〜16語） | Muñoz-Ortiz 2024、大西 2026 | 例文ごとの語数を数え、1節の変動係数が0.25未満、または±2語の幅に60%以上が入れば警告 |
| E7 | not only … but also、not X but Y、rather than を飾りとして多用 | Wikipedia（negative parallelism）、Pangram（3倍） | `\bnot only\b.*\bbut( also)?\b` `\bnot just\b` `\bit'?s not\b.*\bit'?s\b` を数える。**ただし入試の構文項目として扱う章は除外** |
| E8 | 3つ並べの形容詞・名詞（kind, smart, and brave） | Wikipedia、Pangram | `\b\w+,\s+\w+,?\s+and\s+\w+\b` を数え、例文の10%超で要確認 |
| E9 | 褒め言葉の形容詞・副詞の集中（innovative, remarkable, invaluable, exceptional, impressively） | Liang 2024a（査読文で偏る形容詞・副詞） | 「英語・注意」リストの照合。1例文に2語以上なら差し替え |
| E10 | 文頭の Additionally / Moreover / Furthermore / Notably の連続 | Kobak 2025（additionally, notably）、Wikipedia | `^(Additionally|Moreover|Furthermore|Notably|Importantly),` |
| E11 | 長いダッシュ（—）の多用 | Pangram、Wikipedia | `EX`: `—` を数える。例文では原則使わない（使うならコンマ・括弧） |
| E12 | 例文に入る「AIの語り」の舞台（lighthouse, keeper, whispering, a small town where…） | Hamilton & Mimno 2026 | `\b(lighthouse|keeper)\b` `\bwhisper(s|ed|ing)?\b` を数える |

### 3. 見た目

| # | 避けること | 根拠 | 検出方法（自動検査） |
|---|---|---|---|
| V1 | グラデーション（背景・文字・ボタン） | Anthropic 2025、Canatselis 2026、925studios、pixelslop #1/#5 | `SRC`: `(linear|radial|conic)-gradient\(` `background-clip:\s*text` `bg-gradient-to-` → 0回 |
| V2 | 影 | pixelslop #10/S6、925studios、Laith | `box-shadow:(?!\s*none)` `text-shadow:(?!\s*none)` `filter:\s*drop-shadow` `shadow-(sm|md|lg|xl)` → 0回 |
| V3 | 角丸の囲み・カード | pixelslop #10、Canatselis（同じ角丸の均一さ） | `border-radius:\s*(?!0(px)?\b)` → 0回が原則（使うなら1種類・2px以下・意味のある1種類の部品だけ） |
| V4 | 色付きの太い左ボーダーだけの囲み | Canatselis 2026、pixelslop #15 | `border-left:\s*([3-9]|\d{2,})px` `border-left-width:\s*([3-9]|\d{2,})px`。左右上下のうち1辺だけ太い要素が2つ超で警告 |
| V5 | 絵文字の見出し・アイコン、汎用アイコンの多用、見出し上のアイコン | Wikipedia、Laith、pixelslop #18、925studios | 本文・見出しで絵文字の正規表現（J16）→ 0回。`SRC`: `<svg` `<i class="(fa|bi|icon)` `material-icons` の数 → 原則0 |
| V6 | 同じ大きさのカードを均等に並べる格子 | pixelslop #7、925studios（three-card reflex）、Laith | `SRC`: `grid-template-columns:\s*repeat\(\s*[2-4]\s*,\s*1fr\s*\)` `display:\s*grid` の箇所を目視確認。同じクラスの兄弟要素が3つ以上並ぶ箇所を候補にする |
| V7 | 囲みばかり（ページの大半が箱に入っている）、箱の入れ子 | pixelslop #9/#23 | 1ページの枠つき要素が6個超で警告。枠つき要素の中の枠つき要素は0 |
| V8 | 余白・角丸・見出しサイズがすべて同じ値 | Canatselis 2026、pixelslop #21 | `SRC` の `margin`/`padding` の値の種類数が2以下で警告。見出しレベルごとのフォントサイズが全部同じなら警告 |
| V9 | すりガラス・光彩・ネオン | pixelslop #2/#3/#22、Laith | `backdrop-filter` `filter:\s*blur` → 0回 |
| V10 | 既定のウェブ用フォント（Inter, Roboto, Arial, Open Sans, Lato, Space Grotesk）を欧文に使う | Anthropic 2025、pixelslop #8 | `font-family:[^;]*\b(Inter|Roboto|Arial|Open Sans|Lato|Space Grotesk|Helvetica)\b` |
| V11 | 指定の3色（黒・赤・灰網）以外の色 | 依頼の仕様。Canatselis「色は役割で使う」 | `SRC` から `#[0-9a-fA-F]{3,8}\b` `rgba?\(` `hsla?\(` を全部抜き出し、許可リスト（黒・赤1色・灰の濃度数段）と照合 |
| V12 | 全部中央揃え | pixelslop #17、Laith | `text-align:\s*center` の数が見出し・段落要素の70%超で警告 |
| V13 | 英字大文字のラベルが多種類（POINT, CHECK, TIPS, NOTE, KEY, ADVANCED…） | 根拠は弱い（C-6 は許容）。参考書の慣行でラベルは2〜3種 | `\b[A-Z]{3,}\b` を見出し・ラベル要素から抜き出して種類を数え、4種以上で警告。`text-transform:\s*uppercase` `letter-spacing` の箇所も確認 |

### 4. 組版

| # | 避けること | 根拠 | 検出方法（自動検査） |
|---|---|---|---|
| T1 | 柱・ノンブルがない／位置がページごとにずれる | JLReq（基本版面基準） | PDF の各ページで上端・下端のテキストを抜き出し、ノンブルが連番で同じ座標にあるか確認（`pdftotext -bbox` など） |
| T2 | 見出しに番号体系がない、番号の形が混ざる（1. と ① と (1) が同じレベルで混在） | 参考書の慣行（出典未確認） | 見出し要素ごとに先頭の番号形式を正規表現で分類：`^第\d+章` `^\d+\s` `^\(\d+\)` `^[①-⑳]`。同じレベルで2種以上なら警告 |
| T3 | 空行で段落を区切る、段落頭を下げない（ウェブ式） | JLReq（段落頭は全角下げ） | `SRC`: `text-indent` が本文段落に 1em 指定されているか。`<p>` の間に `<br>` や空段落がないか |
| T4 | 禁則違反（行頭の「、。」）」、行末の「（「」） | JLReq | PDF から行ごとに抜き出し、`^[、。，．）」』】〕・ー]` と `[（「『【〔]$` を検出 |
| T5 | 約物の不統一（「，．」と「、。」の混在、全角・半角の括弧の混在、和文中の半角「,」「.」「!」「?」） | JLReq（約物の扱い）、表記の一貫性 | `TEXT`: `[、。]` と `[，．]` の両方が出たら警告。和文の間の半角約物：`(?<=[\p{Han}\p{Hiragana}\p{Katakana}])[,.!?()](?=[\p{Han}\p{Hiragana}\p{Katakana}])` |
| T6 | 和文中のカーリー引用符（“ ”）や英語式の引用 | Wikipedia の指摘は wiki 文脈。**英文例文中の “ ” は印刷では正しい組版なので対象外** | 和文中の `[“”‘’]` を検出（例文の中は除外） |
| T7 | ルビ・圏点で行間が変わる | JLReq（行送り一定） | PDF のベースライン間隔を測り、ばらつきがあれば警告 |
| T8 | 画面操作の言葉、リンク表現 | D-3 | `クリック|タップ|スクロール|こちら(から|を)|リンク|ボタン` → 0回。`SRC`: `<a href` → 0回（印刷用） |
| T9 | 色を飾りに使う（見出し全部が赤、網を背景装飾に） | 参考書の慣行、Canatselis | 赤の使用箇所を数え、「重要語・正解・注意」以外の要素（見出し、罫、背景）での使用を確認 |

---

## 「やること」チェックリスト

### 文章（日本語の解説）
- [ ] 1つの説明に1つ以上の**具体的な例文番号**を必ず結びつける（「例文③の who は…」）。
- [ ] 規則を言い切る。「〜と言えるでしょう」ではなく「〜である／〜する」。例外があるなら例外を具体的に書く。
- [ ] 「重要」と書くなら、なぜ重要か（入試で何が問われるか、どこで間違えやすいか）を同じ文か次の文に書く。
- [ ] 文末を散らす（「〜である」「〜する」「〜だ」「〜に注意」、体言止め、問いかけ）。同じ文末を3回続けない。
- [ ] 接続詞は「また」に頼らず、「ただし」「つまり」「一方」「たとえば」などを内容に合わせて選ぶ。
- [ ] 文の長さに差をつける。短い一文の断定（「先行詞は人である。」）と長い説明を混ぜる。
- [ ] 太字は**1段落に1か所まで**、または太字を使わず赤字・下線の一方に統一する。
- [ ] 箇条書きは「手順」「対比」「一覧表」に限り、説明は段落の文章で書く。
- [ ] 文体（だ・である調か、です・ます調か）を1冊で統一する。参考書の地の文は「だ・である」または簡潔な「です・ます」。

### 英語例文
- [ ] 日常の具体的な場面（家族、学校、店、駅、天気、部活）を使い、固有の物・数・時を入れる。
- [ ] 入試の過去問や定評ある文法書の例文の**長さの幅**（5〜25語程度）に合わせ、短い文と長い文を混ぜる。
- [ ] 文法項目（関係詞）が主役になるよう、他の要素は平易に保つ。語彙は高校の範囲に収める。
- [ ] 人名は名前リストを作って順に割り当て、同じ名前の連続を防ぐ。教科書的な名前（Tom, Ken, Mary, Mr. Smith など）と日本人名を混ぜる。
- [ ] 例文ごとに語数を表にして、ばらつきを点検する（E6）。
- [ ] 教訓・格言調の例文は1章に1〜2個までにし、入れる場合は実際のことわざや出典のある文にする。
- [ ] 英文の確認はネイティブまたは信頼できる例文コーパスで行う（AIの言い換えをそのまま採らない）。

### 見た目
- [ ] 色は**意味で使う**：赤＝文法の要点・正解・注意、灰網＝例文ブロックや表の見出し行、黒＝それ以外。各色の用途を1枚の仕様表に書く。
- [ ] 囲みは四角（角丸なし・影なし）、細罫か網のどちらか一方。囲みの種類は3種以内。
- [ ] 見出しのレベルごとに大きさ・太さ・罫の有無をはっきり変える（主役と脇役の差、C-3）。
- [ ] 英字ラベルを使うなら2〜3種に絞り（例：POINT／注意）、毎回同じ位置・同じ形で出す。
- [ ] 図やアイコンは「意味のある図解」（先行詞と関係詞を結ぶ矢印、文構造の図）だけにする。

### 組版
- [ ] 基本版面を決める（判型、本文サイズ、行長は文字サイズの整数倍、行数、行間）。
- [ ] 柱：偶数ページに章名、奇数ページに節名（両柱）。ノンブルは小口側に、全ページ同じ位置。
- [ ] 見出し番号の体系を決める（例：第1章 → 1 → (1) → ①）。目次・柱と一致させる。
- [ ] 段落頭は全角下げ、段落の間に空行を入れない。
- [ ] 約物を統一する（「、。」か「，．」のどちらか）。和欧混植のアキ（四分程度）をそろえる。
- [ ] 禁則処理を確認する（行頭の句読点・閉じ括弧、行末の開き括弧）。
- [ ] 例文に通し番号、和訳の位置を統一。ページをまたぐ例文と和訳の分離を避ける。
- [ ] 印刷して紙で見る（画面だけで判断しない）。灰網の濃度は実際の印刷で確認する。

---

## 自動検査用の禁止語リスト

使い方：大文字小文字を区別せず、英語は単語境界（`\b`）つきで照合する。**強**は例文に出たら差し替えを検討、**注意**は密度で判断（1章で複数回、または1文に2語以上で警告）。根拠は A・B 節。

### 英語・強（単語。活用形を含む）
```
delve
delves
delved
delving
showcase
showcases
showcased
showcasing
underscore
underscores
underscored
underscoring
tapestry
testament
pivotal
intricate
intricacies
meticulous
meticulously
realm
vibrant
commendable
garner
garnered
bolster
bolstered
interplay
multifaceted
noteworthy
invaluable
laudable
```

### 英語・強（句）
```
stands as
serves as a
a testament to
plays a crucial role
plays a pivotal role
a pivotal moment
a key role
deep dive
rich tapestry
evolving landscape
indelible mark
deeply rooted
setting the stage for
reflects broader
valuable insights
resonate with
align with
not just
i hope this helps
certainly!
```

### 英語・注意（単語）
```
crucial
robust
foster
fostering
enhance
enhancing
landscape
additionally
notably
moreover
furthermore
comprehensive
insights
valuable
enduring
boasts
innovative
versatile
remarkable
exceptional
profound
seamless
leverage
navigate
embark
journey
unwavering
undoubtedly
undeniably
impressively
```
注：seamless, navigate, embark, journey, unwavering, remarkable、および句の it is important to note / in today's world / in conclusion は今回開いた資料には根拠がない（一般にAI語として挙げられるが**未確認**）。単語は注意リストにのみ置き、句はリストから外した（参考書の解説や例文で使う理由がないので、目視で避ければ足りる）。

### 英語・定番名（物語系AIの名前。頻度で判定）
```
Elias
Elara
Mara
Voss
Thorne
Marcus Chen
Sarah Chen
lighthouse
```

### 日本語・強
```
しましょう！
てみましょう
と言えるでしょう
といえるでしょう
いかがでしたか
いかがでしたでしょうか
まとめると
もちろんです
いい質問
お役に立て
効果が期待されます
バランスが重要
ケース・バイ・ケース
正直に言うと
クリック
タップ
スクロール
```

### 日本語・注意（密度で判定）
```
重要です
大切です
必要です
と考えられます
かもしれません
さまざまな
様々な
効率的な
効果的に
多くの
以上のように
このように
これにより
また、
において
ぜひ
を通じて
ポイントは
注目されています
```

---

## 出典一覧

証拠の強さ：◎査読論文／○プレプリント・学位論文／△記事・ブログ・企業ページ・規則集。確認状況：「本文確認」＝本文（または該当部分）を開いて読んだ、「一部確認」＝抄録・紹介記事・一部のみ、「未確認」＝開けなかった・読んでいない。

| # | 著者・年 | タイトル | URL | 確認した内容 | 強さ | 確認状況 |
|---|---|---|---|---|---|---|
| 1 | Kobak, González-Márquez, Horvát, Lause（2024 arXiv／2025 *Science Advances* 11(27)） | Delving into ChatGPT usage in academic writing through excess vocabulary（arXiv 版の題名。雑誌版の題名は未確認） | https://arxiv.org/abs/2406.07016 ／ https://arxiv.org/html/2406.07016 | 2024年抄録の13.5%以上がLLM処理。delves r=28.0、underscores 13.8、showcasing 10.7、potential/findings/crucial の頻度差、共通セット10語 | ◎（雑誌掲載） | 本文確認（HTML版）。付録 Figure S6 の全語は未確認 |
| 2 | Liang, Izzo, Zhang ほか（2024、ICML 2024） | Monitoring AI-Modified Content at Scale: A Case Study on the Impact of ChatGPT on AI Conference Peer Reviews | https://arxiv.org/abs/2403.07183 ／ https://arxiv.org/html/2403.07183 | 査読の6.5〜16.9%。commendable 9.8倍、meticulous 34.7倍、intricate 11.2倍。付録A・Bの形容詞・副詞上位30 | ◎（国際会議） | 本文確認 |
| 3 | Liang, Zhang, Wu ほか（2024） | Mapping the Increasing Use of LLMs in Scientific Papers | https://arxiv.org/abs/2404.01268 ／ https://arxiv.org/html/2404.01268 | 約95万本、CS最大17.5%。Figure 2 の4語 realm, intricate, showcasing, pivotal | ○（その後 COLM 2024 採録とされるが未確認） | 本文一部確認 |
| 4 | WikiProject AI Cleanup（Wikipedia 編集者、随時更新、2026-11閲覧） | Wikipedia:Signs of AI writing | https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing | AI語彙（時期別）、誇張・表面的分析・否定の並列・三点セット、太字・タイトルケース・絵文字・カーリー引用符、対話表現、当てにならない指標 | △（編集者コミュニティの手引き。経験則の集積） | 本文確認（約25万字中、前半20万字） |
| 5 | Muñoz-Ortiz, Gómez-Rodríguez, Vilares（2024、*Artificial Intelligence Review* 57:265） | Contrasting Linguistic Patterns in Human and LLM-Generated News Text | https://arxiv.org/abs/2308.09067 | 人間の文長はばらつきが大きく語彙が多様。LLMは数字・記号・助動詞・代名詞が多い | ◎ | 抄録確認（本文の数値は未確認） |
| 6 | Hamilton, Mimno（2026、EMNLP 2026） | Elias in the Lighthouse, Again? Diagnosing Low Diversity in LLM Stories | 紹介記事 https://news.cornell.edu/node/333804 （DiPietro, Cornell Chronicle, 2026-10-19） | 4モデル2万話、約90%が11語のどれかを含む。lighthouse, keeper, Elias, Mara, Elara | ◎（会議論文。ただし確認は紹介記事） | 一部確認（論文本文は未確認） |
| 7 | 報道各社（404 Media, Gizmodo, Vice）・各種ブログ | Elias Thorne／Elara Voss／Marcus Chen などAIの定番名 | https://404media.co/elias-thorne-chatbots-llms-chatgpt-lighthouse-keeper-story/ ほか | 検索結果の要約のみ | △ | 未確認 |
| 8 | Shieh, Vassel, Sugimoto, Monroe-White（2024 arXiv／2026 *Nature Communications* 17:1243） | Laissez-Faire Harms: Algorithmic Biases in Generative Language Models | https://arxiv.org/abs/2404.07475 | 抄録に名前の頻度表はなし（Sarah/Emily の偏りの根拠にはならない） | ◎ | 抄録のみ確認（HTML版は404） |
| 9 | 大西夢（2025年度、広島大学文学部 卒業論文） | AI生成文からみた「自然な日本語」についての研究 | https://home.hiroshima-u.ac.jp/jshira/papers/AI生成文からみた「自然な日本語」についての研究（大西夢）.pdf | 予備調査148件の自由記述、文長・読点・接続詞・文末の偏り、婉曲・一般論 | ○（学位論文・査読なし・小規模） | 本文確認（PDFからテキスト抽出） |
| 10 | Pangram（日付なし） | AIによる文章の特徴（Signs of AI writing） | https://www.pangram.com/ja/signs-of-ai-writing | 1万語あたりの頻度比：マークダウン12倍、箇条書き9倍、長ダッシュ10倍、三つ組4倍など | △（検出ツール企業。コーパスの言語・詳細不明） | 本文確認 |
| 11 | 中山順司（2026-05-07、PRESIDENT Online） | AIで作った文章を見抜くたった一つのフレーズ | https://president.jp/articles/-/112658 | 「〜が重要です」「〜といえるでしょう」、抽象語、同義反復、文のリズムの均質化 | △（経験にもとづく記事） | 一部確認（有料部分は未読） |
| 12 | Ken Imoto（2026、DEV Community） | We Measured 180 AI-Generated Japanese Articles | https://dev.to/kenimo49/we-measured-180-ai-generated-japanese-articles-the-results-were-not-what-we-expected-4k7e | 6モデル180本、語彙指標、構造指標の撤回 | △（個人の計測、Zenodo 稿は未確認） | 本文確認 |
| 13 | 飯田一史（PRESIDENT Online） | AIの論文調の言い回しに関する記事 | https://president.jp/articles/-/119779 | 検索結果の要約のみ（「〜を示唆している」など論文調） | △ | 未確認 |
| 14 | fyve.co.jp（記事） | AI文章判定の俗説（いかがでしたか はSEO記事由来など） | https://fyve.co.jp/ai-advisor/articles/ai-text-detection-myths-japan | 検索結果の要約のみ | △ | 未確認 |
| 15 | Rajasekaran, Wei, Bricken ほか（Anthropic、2025-11-12） | Improving frontend design through Skills | https://claude.com/resources/articles/improving-frontend-design-through-skills | "AI slop" aesthetic：Inter、白地に紫グラデーション、控えめなアニメーション、予測可能なレイアウト | △（AI開発元の解説） | 本文確認 |
| 16 | Ken Imoto（2026-07-03、DEV Community） | Anthropic Rewrote frontend-design Skill: 3 AI Design Clichés Named with Hex Codes | https://dev.to/kenimo49/anthropic-rewrote-frontend-design-skill-3-ai-design-cliches-named-with-hex-codes-22m4 | 3つの定番の見た目（クリーム＋セリフ＋テラコッタ、黒＋蛍光1色、細罫・角丸なしの新聞風） | △（第三者の紹介） | 本文確認（スキル本文そのものは未確認） |
| 17 | Kosta Canatselis（2026-07-23） | Spot the slop: a UI designer's guide to fixing AI defaults | https://world.hey.com/kostac/spot-the-slop-a-ui-designer-s-guide-to-fixing-ai-defaults-4c448c9c | 均一な余白・角丸・カード、紫青グラデーション、中身のない見出し、色を役割で使う | △（デザイナーのブログ） | 本文確認 |
| 18 | 925studios（2026） | AI Slop Fonts and Gradients: The Tells That Give Away AI Design | https://www.925studios.co/blog/ai-slop-design-tells | Inter、インディゴ紫グラデーション、3枚の角丸カード、淡い影、汎用アイコン | △（デザイン会社のブログ） | 本文確認 |
| 19 | pixelslop（npm パッケージ v0.3.8） | AI Slop Pattern Catalog | https://cdn.jsdelivr.net/npm/pixelslop@0.3.8/dist/skill/resources/ai-slop-patterns.md | 視覚26・ソース16の検出規則と閾値 | △（ツールの規則集） | 本文確認 |
| 20 | Laith0003（GitHub wiki、2026-11 更新） | Anti AI slop ban list | https://github.com/Laith0003/ux-skill/wiki/Anti-AI-slop-ban-list | 絵文字・グラデーション文字・同じカード3枚・重い影・均一な角丸・中央揃えの禁止。大文字ラベル・ピルは許容 | △（個人の規則集） | 本文確認 |
| 21 | W3C（Japanese Layout Task Force） | Requirements for Japanese Text Layout（日本語組版処理の要件, JLReq） | https://www.w3.org/TR/jlreq/ | 基本版面、柱（両柱・片柱）とノンブル、約物のアキ、禁則、ルビと行送り、段落の字下げ | ◎（W3C 技術文書。査読論文ではないが規範的資料） | 一部確認（約54万字中、前半20万字） |
| 22 | JIS X 4051 | 日本語文書の組版方法 | — | JLReq 経由で言及のみ | ◎（規格） | 未確認 |
| 23 | 学習参考書の組版・2色刷りに関する公開資料 | — | — | 検索したが該当資料が見つからない（出版社の編集マニュアル、デザイナーのインタビュー） | — | 未確認（資料なし） |

---

## 調査の限界
- 英語のAI語彙研究は**学術論文・査読文**が対象で、教材の例文に直接あてはまるかは検証されていない。語彙リストは「例文で使う理由がほぼない語」として使うのが妥当。
- 「Sarah / Emily に偏る」という主張は、**今回の調査では裏付けが見つからなかった**。確認できたのは物語での Elias / Elara / Mara の偏り（紹介記事経由）のみ。
- 日本語のAI文体の量的研究は、小規模な卒業論文1本と企業ページ1本だけ。「〜しましょう」「まとめると」「三点セット」が日本語AI文で多いことは、**数値では確認できていない**（意見記事レベル）。
- デザインの「AIっぽさ」はすべてウェブUIについての記事・規則集で、査読研究はない。印刷参考書への応用は推論。
- 学習参考書の組版の慣行は公開資料が見つからず、D-2 は実物の参考書で確認が必要。
