# 01 学習科学の文献調査（関係詞シリーズ教材設計用）

> 調査日: 2026-11-21 / 作業中（随時追記）
> 表記: 【記憶・未確認】=開いた資料で確認できなかった数値 / 【設計判断】=調査者の推測による設計値

## 作業ログ（調査メモ・随時追記）

### [1] Dunlosky et al. (2013) — 確認状況
- PSPI 本誌（https://doi.org/10.1177/1529100612453266）は sagepub が 403。APS の紹介ページ（https://www.psychologicalscience.org/publications/journals/pspi/learning-techniques.html）で要旨を確認。
- 同著者による一般向け要約 Dunlosky (2013) "Strengthening the Student Toolbox", American Educator, Fall 2013（https://www.aft.org/sites/default/files/dunlosky_0.pdf）を本文確認（PDFをダウンロードしてテキスト抽出）。
- 確認した内容（AFT本文より）:
  - 10技法を評価。practice testing と distributed practice を「最も効果的」（Table 1: "Very effective under a wide array of situations"）。
  - interleaved practice: "Promising for math and concept learning, but needs more research"。elaborative interrogation / self-explanation: "Promising, but needs more research"。
  - rereading: "Distributed rereading can be helpful, but time could be better spent using another strategy"。highlighting: "Not particularly helpful, but can be used as a first step toward further study"。summarization: 訓練を受けた場合のみ有効。keyword mnemonic: 語学で一部有効だが効果は短命。
  - 練習テストの実践法: 再認より再生（recall）を求めるテストの方が効果大／答えを手で隠して書き出し、正答と照合／「フィードバック付きで各項目を少なくとも1回正しく再生できるまで」続ける／別の日に再学習して複数回正答する。
  - 分散学習: 同じ総学習時間でも分散の方が保持が長い。1クラスにつき週2回の短い学習ブロックから始めることを提案。累積テストの活用。
  - 交互練習: Rohrer & Taylor (2007) の再掲で、練習中の正答率はブロック練習の方が高いが、1週間後のテストでは交互練習群が「3倍」良い。ただし **フランス語語彙（カテゴリ別）では差なし**、**高校生のコンマ用法ルール学習では交互練習の効果なし** と明記 → 文法ルール学習への一般化は慎重に。
  - 自己説明: 論理推論問題で最終テスト約90% vs 30%未満（3倍）。練習中の正答率には差がなく、転移問題で差が出る。精緻化質問は前提知識が乏しいと使いにくい。
  - 「答えを隠して想起し、正答と照合する」ノート使用法を推奨（＝赤シート方式に近い）。

### [2a] Roediger & Karpicke (2006) — 本文確認
- PDF: https://www.gwern.net/docs/spaced-repetition/2006-roediger.pdf（Psychological Science 17(3), 249–255 の誌面コピー）
- 実験1: 散文を読み、フィードバックなしの自由再生テスト1回 vs 再学習。5分後は再学習が上（81% vs 75%, d=0.52）、2日後はテスト群が上（68% vs 54%, d=0.95）、1週間後もテスト群が上（56% vs 42%, d=0.83）。
- 実験2: SSSS / SSST / STTT。5分後は SSSS 83% > SSST 78% > STTT 71%。1週間後は STTT 61% > SSST 56% > SSSS 40%。
- 再学習群（SSSS）は「1週間後も覚えている」という自信が高かった（d=0.54〜0.61）＝メタ認知の錯覚。
- 示唆: 解説を読み返すより、答えを隠して想起する方が1週間後の保持が大きい。直後の手応えは当てにならない。

### [2b] Adesope, Trevisan & Sundararajan (2017) — 要旨のみ確認
- 書誌: Review of Educational Research 87(3), 659–701, DOI 10.3102/0034654316689306。WSU リポジトリ（https://rex.libraries.wsu.edu/esploro/outputs/journalArticle/Rethinking-the-Use-of-Tests-A/99900601154801842）で要旨確認。本文PDFは取得できず（WSU の PDF URL はトップページにリダイレクト、Semantic Scholar では CLOSED）。
- 要旨: 練習テストは再学習および他のすべての比較条件より学習に有益。効果量は、テストの特徴・参加者特性・アウトカム・方法論で調整される。
- 数値: 全体 g ≈ 0.61、再学習比 g ≈ 0.51 【記憶・未確認】。118論文・272効果量・15,472人、選択式・混合形式で効果が大きい、フィードバックの有無による差は有意でない、は検索結果の二次要約で見たのみ【未確認】。

### [4b] Wisniewski, Zierer & Hattie (2020) — 本文確認
- PDF: https://www.frontiersin.org/articles/10.3389/fpsyg.2019.03087/pdf（Front. Psychol. 10:3087, オープンアクセス）
- 435研究、k=994、N>61,000。ランダム効果モデルで全体 d=0.48（外れ値除去後、CI 0.44–0.51）。異質性が大きく「フィードバックは単一の処遇ではない」。
- フィードバックの種類別: 強化/罰 d=0.24（k=39）、**正誤＋正答を示す corrective feedback d=0.46（k=238）**、**high-information feedback（正誤・正答に加えて、どう遂行するか／自己調整に関する情報を含む）d=0.99（k=42, CI 0.82–1.15）**。
- アウトカム別: 認知 d=0.51、動機づけ d=0.33。「フィードバックは情報量が多いほど有効」。
- 二次言語の corrective feedback の効果は熟達度などで調整される（本メタ分析ではその調整変数は扱っていないと明記）。
- 示唆: 解答冊子は「正解」だけでなく、なぜ正しいか（手順・根拠）、なぜ他の選択肢が誤りか、次にどう判断すればよいか（自己点検の手順）まで書くと「high-information」側に近づく。

### [4a] Hattie & Timperley (2007) — 本文確認
- PDF: https://www.uky.edu/~gmswan3/575/Hattie_Timperly_2007.pdf（RER 77(1), 81–112 の誌面）
- 12のメタ分析を統合したフィードバックの平均効果量 0.79。称賛・報酬・罰は低い（例: teacher praise 0.14 等）。
- モデル: 3つの問い（Where am I going? / How am I going? / Where to next?）× 4レベル（課題 FT／処理 FP／自己調整 FR／自己 FS）。FS（「よくできたね」）は最も効果が低い。FT（正誤）は誤った解釈を正すときに強力。知識が不足しているならフィードバックより追加の指導の方が有効。FT は他の課題に般化しにくく、FT→FP→FR へ移すのが最も効果的。
- **誤答理由の詳細説明について重要な但し書き**: Kulhavy et al. (1985) では、正答の提示のみの単純なフィードバックの方が、4つの誤答選択肢をそれぞれ説明する複雑なフィードバックより後の成績が高かった（著者らの推測: 誤答情報が誤りの記憶を強めた可能性、または表面的処理）。ただし自信の高い学習者はどの複雑さでも効率よく利用した。
- タイミング: 課題レベル（テスト場面）では若干の遅延が有利（0.36）、処理レベルでは即時が有利（0.28）（Kulik & Kulik 1988）。Clariana et al. (2000): 遅延フィードバックの効果は易問 −0.06、中難度 0.35、難問 1.17。
- 示唆: 解答解説は「正解の根拠（判断手順＝FP）」を主役にし、誤答の説明は"典型的な誤った解釈"に絞って短く。全選択肢の長い誤答説明は逆効果の可能性がある【設計判断】。別冊解答（＝解き終えてから見る、やや遅延）は難問に向く。

### [4c] Shute (2008) "Focus on Formative Feedback" — 本文確認
- PDF: https://myweb.fsu.edu/vshute/pdf/shute%202008_b.pdf（RER 78(1), 153–189）
- 効果的なフィードバックは verification（正誤判定）と elaboration（正答へ導く情報）の両方を含む。elaborated feedback は正答に触れ、「選んだ答えがなぜ誤りか」を説明し、正答を示しうる。response-specific feedback が単純な正誤や「正解するまで解き直し」より有効という合意が広がりつつある。
- 長すぎ・複雑すぎるフィードバックは読まれず、メッセージを薄める。Table 2（すべきこと）: elaborated feedback（what/how/why）を与える／**扱いやすい小さな単位で提示**／具体的・明確に／**できるだけ単純に、ただし単純すぎないように**（Kulhavy et al. 1985）／学習目標志向を促す（誤りは学習の一部）／**解答を試みた後に提示する（先に答えを見せない）**。
- Table 3（避けること）: 他者との比較、点数だけの提示、称賛の多用、**網羅的な誤り分析・診断の多用**（費用に見合う効果が乏しい）、正解で終わる段階的ヒントの乱用。
- Table 4（タイミング）: 難しい新課題・低達成者には即時、易しい課題・高達成者には遅延も可、転移には遅延が有利な可能性。Table 5: 低達成者には directive/corrective フィードバックと足場かけ、高達成者には facilitative フィードバック。
- 示唆: 別冊解答の各問解説は「①正解 ②判断の根拠（1〜3行）③典型誤答1つ＋なぜダメか（1行）」程度の小単位が妥当【設計判断】。問題ページと解答を分冊にし、先に答えが見えない構成は「解答を試みた後に提示」と整合。

### [2c] Cepeda, Pashler, Vul, Wixted & Rohrer (2006) メタ分析 — 本文確認
- PDF: https://www.gwern.net/docs/www/uweb.cas.usf.edu/f1052ecdd92f0ecc3f57bdd890a4a6558483ec45.pdf（Psychological Bulletin 132(3), 354–380）
- 184論文・317実験・839評価。言語的再生課題。同じ学習時間なら、間隔をあけた学習（spaced）は集中（massed）より再生率が高く、これは保持期間（1分未満〜1か月超）にかかわらず成立。
- 最適な学習間隔（ISI）は保持期間が長いほど長くなる。保持期間1か月超の研究はすべて、数週〜数か月にわたる分散が1日間隔より有利。平均的な分散の利益は 15%（ポイント）。「少なくとも1日あけることは長期保持の最大化に極めて有用」。
- 同著者の一般向け: Pashler, Rohrer & Cepeda (2006) "Temporal Spacing and Learning", APS Observer（https://www.yorku.ca/ncepeda/publications/PRC2006.pdf）も開いて確認（導入部のみ精読）。

### [2d] Cepeda, Vul, Rohrer, Wixted & Pashler (2008) — 本文確認
- PDF: https://www.yorku.ca/ncepeda/publications/CVRWP2008.pdf（Psychological Science 19(11), 1095–1102）
- 1,350人以上がオンラインで事実（雑学）を学習し、0〜105日の間隔で復習、7/35/70/350日後に最終テスト。
- 最適間隔: 再生の補間推定で 7日後テスト→約3日、35日→約8日、70日→約12日、350日→約27日（保持期間の 43%, 23%, 17%, 8%）。要旨: 1週間後テストでは保持期間の約20〜40%、1年後テストでは約5〜10%。
- 効果: 最適間隔は0日間隔に比べ最終再生を64%増（d=1.1）。
- **間隔が最適より長すぎるコストは、短すぎるコストよりずっと小さい**（正答率は間隔とともに急上昇し、その後ゆるやかに低下）。
- 「1つの単元を1週間で詰め込む」慣行は、直後の高い習熟が長期に残らない「誤解を招く」結果を生むと明言。
- 示唆（入試まで数か月〜1年）: 復習は数週間単位の間隔が目安。各章末に「前の章の復習問題（数問）」を混ぜる、問題集に「1回目／1週後／1か月後」の日付記入欄を設ける等【設計判断】。

### [2e] Rohrer & Taylor (2007) — 本文確認
- PDF: https://www.gwern.net/doc/psychology/spaced-repetition/2007-rohrer.pdf（Instructional Science 35, 481–498）
- 実験2（大学生、4種類の立体の体積問題）: 練習中の正答率はブロック群 89% > 混合群 60%。1週間後テストでは **混合群 63% vs ブロック群 20%（d=1.34）**。実験1: 同一タイプの練習を1回に集中させるより2セッションに分散させる方が1週間後の成績が高い。
- 著者の説明: ブロック練習では「どの解法を使うか」の判断が不要になる。混合練習はその識別を練習させる。
- 注意: 対象は数学（大学生）。小規模（実験2は群あたり十数名）。

### [2f] Brunmair & Richter (2019) — 本文確認（受理稿）
- PDF: https://www.psychologie.uni-wuerzburg.de/fileadmin/06020400/2019/Brunmair_Richter_in_press__2019_META-ANALYSIS_OF_INTERLEAVED_LEARNING.pdf（Psychological Bulletin 145(11), DOI 10.1037/bul0000209 の受理稿）
- 59研究・238効果量・158サンプル。全体 g=0.42（中程度）。絵画 g=0.67、数学 g=0.34、説明文・味は有意でない、**単語（words）ではブロックの方が有利 g=−0.39**。
- 調整変数: カテゴリ間の類似度が高いほど、カテゴリ内の類似度が低いほど、教材が複雑なほど交互練習の効果が大きい（注意の逐次理論＝カテゴリ間の差異に気づくことが鍵）。保持期間による調整は見られず。
- **実践的含意（本文）: 「数学課題・説明文・文法規則・外国語・単語のような教材に交互練習を推奨することにはためらいがある。これらの教材では、ブロック提示に比べて学習を妨げることさえありうる」**。ただし語・文法のデータは少なく、解釈に注意とも明記。
- 示唆: 関係詞は「which/where/what/that の選択」という、似たカテゴリの識別課題の側面がある（カテゴリ間類似度が高い＝交互練習が効きやすい条件）。一方、文法規則の交互練習に直接の支持はない。→ **新規項目の導入はブロック（単元ごと）で行い、識別が求められる段階（章末・総合演習）で混合する**という折衷が妥当【設計判断】。

### [3a] Weinstein, Madan & Sumeracki (2018) "Teaching the science of learning" — 本文確認
- 全文: Europe PMC PMC5780548（Cognitive Research: Principles and Implications 3:2, オープンアクセス）https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5780548/fullTextXML
- 精緻化: 精緻化質問（how/why を問い、答えようとする）は比較的強い証拠がある。**ただし生成した内容が貧弱だと学習を損なうことがあるので、答えを教材や教師と照合することが重要**（Clinton et al. 2016）。自己説明のプロンプトを教材中に散りばめて足場かけできる。
- 具体例: 抽象概念を具体例で補うと理解・記憶しやすい。**2つの例の共通点を説明させ、根底の構造を抽出させると転移に役立つ**。具体例と抽象的指示が矛盾すると学習者は具体例に従う（LeFevre & Dixon 1986）。初心者は表面的特徴を覚えがち。**表面の異なる複数の例**は1例より転移を助ける（Gick & Holyoak 1983）。面白い例は概念記憶を損なわないが、**概念と無関係な面白さ（seductive details）は学習を損なう**（Harp & Mayer 1998）。
- 精緻化・具体例・二重符号化は想起練習の一部として用いると最もよく機能する。

### [3b] Bisra, Liu, Nesbit, Salimi & Winne (2018) 自己説明メタ分析 — 本文確認
- PDF: https://www.gwern.net/doc/psychology/spaced-repetition/2018-bisra.pdf（Educational Psychology Review 30, 703–725）
- 64報告・69効果量・N=5,917。自己説明プロンプトの全体効果 **g=0.55（95%CI 0.45–0.65）**。比較条件別: 追加説明なし g=0.67、**教師（教材）による説明を与えた群との比較では g=0.35**、他の方略との比較 g=0.30。
- 示唆: 解説を読ませるだけより「なぜそうなるか」を自分で書かせる方がよいが、良質な解説を与えることとの差は小さめ。自己説明は時間がかかる（Chi et al. 1994 では約2倍の時間）。
- 第二言語文法への適用: 本メタ分析に Wylie et al. (2011) "Effects of adaptive prompted self-explanation on robust learning of second language grammar"（英語冠詞）が含まれる。検索結果の抜粋では同グループが「第二言語文法学習の先行研究では、練習のみに対する自己説明の優位は見られなかった」と述べているが、**原文未確認**（Wylie, Koedinger & Mitamura 2009 の PDF は escholarship が 403）。→ 文法では自己説明は短い選択式（メニュー型：「この空所が which になる理由は？ ①先行詞が物 ②後ろが不完全文…」）に留め、問題演習量を削らない方が無難【設計判断】。
- 精緻化質問の前提: 既有知識が乏しいと答えを生成できない（Dunlosky AFT 2013）。→ 「なぜ？」の問いは解説を読んだ後・解説の中で提示し、自力で答えた後に照合できる形にする【設計判断】。

### [5a] Mayer (2023) "Research-Based Principles for Designing Multimedia Instruction" — 本文確認
- PDF: https://www.unh.edu/teaching-learning-resource-hub/sites/default/files/media/2023-06/itow-research-based-principles-for-designing-multimedia-instruction-mayer.pdf（APA Division 2 の電子書籍 "In Their Own Words" 所収。数値は Mayer 2021 のメタ分析に基づく）
- ※ 依頼にあった Mayer (2008) American Psychologist 本体は開けていない（未確認）。同じ原則の最新版として本章を使用。
- 外在的処理を減らす原則（中央値 d）:
  - **一貫性（coherence）**: 無関係な素材を除く。19中18で支持、d=0.86。面白いが無関係な情報（seductive details）を除くと転移が向上。低ワーキングメモリ学習者・興味を引く余計な素材で効果大。
  - **信号化（signaling）**: 重要素材の構成を示す手がかりを加える。28中26、d=0.70（言語的信号＝見出し・アウトライン・下線などの強調・first/second 等 d=0.69、視覚的信号＝矢印など d=0.71）。**低知識学習者・複雑な素材で、かつ信号を控えめに使うとき効果が強い**。
  - **冗長（redundancy）**: ナレーション付き図に画面テキストを加えても深く学べない。12中8、d=0.10 と小さい。**L2 の語・短い文・図がない教材などでは効果が弱まるか逆転**。→ 紙教材では「図と本文で同じ内容を二重に長々と書かない」程度に解釈【設計判断】。
  - **空間的近接（spatial contiguity）**: 対応する文字と図を離さず近くに置く。9中9、d=0.82。Ginns (2006)、Schroeder & Cenkci (2018) のメタ分析でも同様（後者 g=0.63 は検索結果の要旨抜粋のみで確認）。低既有知識・複雑な教材で効果大。
- 本質的処理を管理する原則: **分割（segmenting）** d=0.67、**事前訓練（pre-training: 主要概念の名称と特徴を先に学ぶ）** d=0.78（高既有知識者には効かない可能性）。
- 示唆: 例文の直下・直横に構造図（先行詞→関係詞→節の範囲を括弧や矢印で）を置く。赤は「信号」として1見開きにつき要点数か所に限定（多用すると信号の価値が下がる）【設計判断】。章冒頭で「先行詞・格・完全文/不完全文」などの用語を先に教える（pre-training）。雑学コラムは本文と分離し、無関係な面白情報は入れない。

### [6c] Kalyuga (2007) expertise reversal — 本文確認
- PDF: https://www.uky.edu/~gmswan3/EDC608/Kalyuga2007_Article_ExpertiseReversalEffectAndItsI.pdf（Educational Psychology Review 19, 509–539）
- 定義: 初心者に有効な手法（統合された図と文、詳しい説明、ワークドエグザンプル）が、知識の多い学習者には冗長になり効果がなくなる／逆転する。
- split-attention と redundancy の関係: 初心者では文と図を統合した形式が最良（split-attention 効果）だが、熟達につれ統合形式の効果は下がり、図のみの方が良くなる（Kalyuga et al. 1998）。
- **語注（glossary）の研究（Yeung et al. 1998; Yeung 1999）**: 未知語の定義を本文の語の直上に統合した形式は、小学5年生・補習ESLクラスの低知識8年生では読解成績が良かったが、大学生・高知識の生徒では巻末の別置き語彙集の方が良かった。→ **統合語注の有効性は学習者の熟達度に依存**。
- ワークドエグザンプル→問題演習: 低知識の高校生はよく誘導されたワークドエグザンプルで有利、高知識者は問題解決演習で有利（Kalyuga & Sweller 2004）。初心者は例題→類題ペア、熟達者は問題→例題ペアやフェーディング例題で有利（Reisslein et al. 2006）。低知識者はゆっくりのフェーディング、高知識者は速い移行が有利（Reisslein 2005）。
- first-step 診断法: 課題を短時間提示し「最初の一手」を答えさせて熟達度を素早く判定できる。これに基づく適応的指導は知識獲得を向上。
- 注: 本レビュー自体は文法学習の研究を扱っていない（数学・工学・技術系が中心）。文法への適用は類推【設計判断】。
- 示唆: 完全解説bookは初心者向けに「例題（判断手順を全部書いたワークドエグザンプル）→類題」の対で始め、章内で手順の一部を空欄にするフェーディングへ。問題集は各章冒頭に「最初の一手」型の診断数問を置き、正答なら解説を飛ばして演習へ進める分岐を明示する【設計判断】。語注は「本文で初出の難語のみ近接配置」し、上級者が無視しやすい小さな書体にする【設計判断】。
