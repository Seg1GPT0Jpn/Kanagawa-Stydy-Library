# 04 AIが作ったように見える文章・デザインの特徴（調査メモ）

対象：大学入試向け英文法教材（日本語解説＋英語例文、印刷用PDF、黒・赤・灰色網の3色）。
目的：AI生成物に典型的な特徴を避け、市販の学習参考書として通用する見た目と文章にする。

> 作業中のファイル。調べた分から順に書き足している。末尾の「出典一覧」で確認状況を示す。

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

