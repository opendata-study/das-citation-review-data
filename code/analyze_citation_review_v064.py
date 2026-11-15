#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DAS(データ利用可能性声明)の類型と、被引用数・査読期間の関係を分析する。 v27 CSV の実際の列名に合わせた版。(v064: --export-public で、題名の語数 title_words_adj のうち題名の長さを WoS の題名から取った行[title_len_source が wos]を、WoS 由来なので公開しない: その行の title_words_adj を PMC の題名から数えた title_words に置き換えて出す(列名は title_words_adj のまま。title_words・title_len_source は出さない)。置き換えた件数をログ・README_data.md・data_dictionary.csv に書く。--export-keep-wos-title で置き換えを止める。推定・表・図は v063 と同じ。) (v063: --export-public の修正4点(①OpenAlex の取得記録の有無を counts と topics に分けて確かめ、片方でも欠ければ警告する[従来は meta が 1 つでもあれば警告しなかった]②取得記録のない topics の取得日を --export-oa-topics-date で渡すと、openalex_raw/openalex_topics_retrieval_note.txt と README_data.md に書く③code/ に別の版のコードが残っていれば知らせる④oa_cy_2026 は部分年であることを data_dictionary.csv と README_data.md に書く)。推定・表・図は v062 と同じ。) (v062: --export-public の修正3点(①同じ出力先に再実行すると OpenAlex の取得記録 openalex_*meta*.json が一覧・警告に出ない不具合を直し、常に上書きしてコピーする ②出力先に既存のファイルがあれば知らせる ③data_dictionary.csv に pub_month・date_accepted の説明を足す)。推定・表・図は v061 と同じ。) (v061: --export-public を追加(論文の Data availability statement に書いた公開用データを GitHub・Zenodo 用のフォルダに書き出す。論文単位の分析データ[識別子・雑誌・年・DAS ラベル・PMC の論文の特徴・査読期間・PMC cited-by・OpenAlex の分野と年次被引用数]・参照セットと混同行列・OpenAlex の生データと取得記録・コードと設定・WoS の再取得の手順を出し、WoS 由来の列と DAS の本文は出さない。回帰は走らせない)。--export-labels の参照セットの書き出しを関数 _export_reference に分けた(出力は変わらない)。推定・表・図は v060 と同じ。) (v060: fig0 の先頭パネルの題名を「All N journals combined」にして太字にし、注に「合算」を明記した(CSV の Journal 列は従来どおり All journals)。推定・表・他の図は v059 と同じ。) (v059: 本論の図の縦の高さを詰めた(fig5c の行の高さ 0.55→0.40 インチ、fig7 0.55→0.36、fig6c 0.80→0.58、fig4c 0.30→0.25、雑誌別フォレスト図 fig8 0.27→0.24)。fig5c は凡例の余白を広げた(rect の下端 0.07→0.10)。推定・表・他の図は v058 と同じ。) (v058: --check-extra ratiodir を追加(JASIST 査読対応: WoS と PMC の雑誌×類型の率比が 1 の同じ側にある数を、保存済みの check_extra_ratio_by_journal_<tag>.csv から数える。回帰は走らせない。--check-extra ratio の出力にも同じ要約を足した)。既存の推定・表・図は v057 と同じ。) (v056: --das-platform-report を追加(JASIST 査読対応: 識別子のないリポジトリ共有の量の概算。DAS の本文 das_text から、類型ごと・P について雑誌群別・年別に、データ置き場の名前[Zenodo・Figshare・Dryad・OSF など]と、コード置き場の名前[GitHub など]を含む文の割合を、識別子らしい文字列[DOI・受入番号・Zenodo の番号つき URL など]の有無で分けて数え、人手で確かめる標本を CSV に書き出す。回帰は走らせない)。既存の推定・表・図は v055 と同じ。) (v055: --check-extra repo を追加(JASIST 査読対応: PLOS OSI の「リポジトリ共有」と本稿の類型を同じ土俵に並べる。F+M(任意で F+M+P)を 1・それ以外を 0 とする 2 値の DAS で、主モデルと同じ NB を推定し、率比と「%」表記の変化率を出す。--repo-defs・--repo-specs・--repo-adj・--repo-ref-pct)。既存の推定・表・図は v054 と同じ。) (v054: --check-extra subfield の一覧・適合度 CSV を、--subfield-variants を名前に含めて保存。別の指定で上書きされない) (v053: --export-labels の reference_set.csv に PMCID の列を足す(--ref-id-col、既定 PMCID。列がなければ入れない)/ --classifier-report の雑誌群別の表で、人手の件数が --clf-min-n(既定 5)未満のセルを「--」にする(CSV の値は変えない)/ PPV の表の注に「点推定」を明記。推定・他の表・図は v052 と同じ。) (v052: JASIST 査読対応として --classifier-report(参照セットでのカテゴリ別の分類性能: 混同行列・適合率・再現率・F1・雑誌群別・コーパス上の PPV と LaTeX 表)と --export-labels(DOI ごとの DAS ラベルと 3 LLM の個別ラベル・参照セット・混同行列を Zenodo 用フォルダに書き出す)を追加。回帰は走らせない。既存の推定・表・図は v051 と同じ。) (v051: 雑誌別フォレスト図(fig8_journal_forest・fig8_journal_forest_review)を 6 パネル 1 行から 2 段×3 列に変え、縦置きの紙の幅に収めても文字が小さくならないようにした(約 6.6×7.6 インチ、文字 7〜10 pt)。推定・表・他の図は v050 と同じ。) (v050: 雑誌別フォレスト図(fig8_journal_forest・fig8_journal_forest_review)の横軸の目盛りを、表示範囲に合わせて 1 より小さい側にも付けるようにした(従来は 1・1.4・2 だけで、1 未満の値が読めなかった)。推定・表・他の図は v049 と同じ。) (v049: --check-wos-gap を追加(WoS 未照合が集中する期間[既定 IJERPH 2023 年以降・Heliyon 2025 年、--gap-spec で変更]を除いた主モデルの再推定。Main・Cells[その期間だけ除く]・Journals[その雑誌を全期間で除く]の DAS の率比・Holm 後の p・Main とのずれ・除いた行の類型の件数を出す) / v048: --check-adjust-sets の注の誤りを修正(集合は入れ子 FE ⊂ D ⊂ B ⊂ A ⊂ Main。表示のみ、計算は変えない) / v047: --check-adjust-sets を追加(調整集合を替えた DAS の率比の比較。FE=共変量なし、D=DAS に先行する共変量だけ[著者数・責任著者数・ORCID・国数・機関数・共著の形態・等貢献・助成・責任著者の国]、B・A=論文の tab:mediator、Main=全共変量。同じ行・同じ固定効果で NB を推定し、率比・95%区間・Holm 後の p・Main に対する対数率比の最大のずれを出す)/ v046: --check-vif の要約で --vif-threshold 10 のとき「10 以上」が重複して出るのを直し、NB の分析対象の行の「被引用数の平均」を --dv review_days では「査読期間(日)の平均」と表示する(表示のみ。計算は変えない) / v045: --check-vif を追加(多重共線性の診断。主モデルの設計行列で、固定効果込みの分散拡大係数 VIF(NB の重みつき・重みなし)、共変量だけの VIF、ブロックごとの一般化 VIF(GVIF^(1/(2df)))を出し、check_vif_<tag>.txt・.csv に保存する)。OpenAlex 窓の --exposure covariate で、主モデルの推定直後に log_age の弾力性(係数 ÷ 標準化に使った SD)とクラスタ頑健な 95% 区間を表示する / v044: 出力フォルダに実行条件の印を付けて上書きを防ぐ。既定の出力先は --exposure off 以外のとき <出力先>__exp-<方式> になり、--run-label で任意の名前も付けられる。既存の結果がある出力先で再推定するときは、直下のファイルを <出力先>/_archive/<日時>/ にコピーしてから走らせる(--no-archive で止める)。実行ごとの日時・コマンド・版・入力 CSV を <出力先>/RUNINFO.log に追記する。--oa-report も上書き前に退避する / v042: OpenAlex の年次被引用数(counts_by_year)を従属変数に追加 --fetch-counts・--merge-counts・--dv oa_c<k>/oa_a<j>/oa_l<k>/oa_total・--oa-suite(窓ごとの DAS の率比・寄与の比較) / v040: --check-extra subfield が分野(field・domain・subfield 上位 N)の係数の表(率比・95%信頼区間・p・Holm 後の p・件数)を check_extra_subfield_coef_<仕様>_<tag>.csv に保存し、--supp-field で補足表 S3(被引用数)・S4(査読期間)の tex を作る / ダミー列の追加で出る PerformanceWarning を止めた / v039: OpenAlex の primary_topic の取得・結合・subfield を入れた感度分析を統合(--topics-pipeline) / v038: fig3 ヒートマップの脚注に星印(*・**・***)の定義を追加 / v037: 表 5・fig6c の PMC 列がどの標本から作られたかを確かめる --check-fig6c を追加し、fig6c の組み立て時に各系列の N・クラスタ数・元の CSV を robustness_fig6c_provenance.csv に残す / v036: 補足表 S1・S2 の脚注で、全係数にかける Holm の「全係数」に DAS の行が含まれることを明記 / v035: 頑健性(fig6c と頑健性の表)を、主モデルと同じ設定の 4 つの実行から組み立てる(--fig6c-*)。読み込む表が主モデルとずれていれば警告 / v034: fig5c(調整前後の比較)の凡例を軸の外(図の下)に出し、M の行の記号との重なりを解消 / v033: --main-figs を追加(本論で使う図 7 点を PNG だけで作る) / v032: 論文用の図を改訂(fig7 の並びと名称・ヒートマップの色の目盛りを修正、被引用数と査読期間を並べる fig4c・fig5c・fig6c・fig8 を追加) / v030: --check-misclass-ext fm を追加(F→M の誤分類率を変えたときの M の率比の感度分析。--fm-rates・--fm-reps) / v029: --check-misclass-ext の出力ファイル名に、参照セット・層の分け方・最小件数・反復数・φ を入れて、条件の違う実行で上書きしないようにした / v028: --noise-strata two(big3 とそれ以外の 2 層)を追加し、strat・diff の出力に補正後の類型ごとの件数の分布(最小・中央値・最大・--noise-min-count 以上の反復数)を追加 / v027: 雑誌名の短縮形(SciRep・NatCommun など)を big3 に振り分けるよう _jgroup を修正し、--check-misclass-ext strat で参照セットの層ごとの雑誌数を表示 / v026: 修正 3 点(--check-extra aft を被引用数の実行でも査読期間データで自動実行・--check-misclass-ext の参照 CSV を推定の前に確認・係数表の標準誤差の sqrt 警告を解消) / v025: --check-extra を追加(aft・window を含む)・--exposure spline・--check-misclass-ext(雑誌層別・差異的誤分類の感度分析) / v024: --shapley-nb を全行で実行できるようにした(論文の NB 版 Shapley 分解を 5 万行の標本から全行へ置き換える用)。部分集合ごとの結果を shapley_nb_cache_<tag>.json に保存して中断後に再開でき(--shapley-fresh で破棄)、親モデルの係数を初期値にして収束を速め、未収束は反復を倍にして再推定し、進捗と残り時間を出す。--shapley-nb-both で被引用数(wos_TC)と査読期間(review_days)を続けて実行する。出力に N・標本の有無・未収束数・本文用の割合の 1 行を追加 / v023: --check-misclass で、引いた真の類型の件数が --noise-min-count 未満の反復を、その類型の統合から除く(件数が極端に少ない類型の係数が不定になり、率比が 1 の方へ引かれるのを防ぐ)。出力に有効な反復数 n_valid_reps と引いた件数の平均 mean_n を追加 / v022: --audit-misclass(check_misclass の実装を抽出して論文の説明と照合する)・--check-misclass に補正後の類型ごとの件数の出力を追加 / v021: 査読コメント対応 --field-col・--das-source・--das-agree-only・--check-label-noise・--check-misclass / v020: 査読コメント対応 --exposure・--check-exposure・--check-zero・--check-cluster・--shapley-nb / v019: 補足表 S1・S2 の DAS 類型の名称を論文の表2に合わせた(SUPP_DAS を DAS_NAMES_LEGEND と同じにした) / v018: 基準を替えた対比(--check-contrast、既定は N 基準)と、交互作用の自由度の内訳(--check-df)を追加 / v017: 件数の表示 --check-sample / v016: 論文 3.1節の数値(年別・雑誌別の割合、WoS 被引用数の平均)を確かめる --check-section31・図の凡例の名称を表2に合わせた / v015: 年ごとの雑誌グループ別の件数を確かめる --check-journal-groups / v014: 送るファイルをまとめる --pack-send / v001: ICADL2026 の分析・検定に対応する部分を追加 / v002: 雑誌名の表示・雑誌別NBの標準誤差・列名検索を修正 / v003: 頑健性の確認 --robustness を追加 / v004: 論文用の図表 --paper-figs・--paper-only を追加 / v005: 査読期間(--dv review_days)を被引用数と同じ分析にかける・図表に査読期間と並置図を追加 / v006: 図表を 1 つのフォルダにまとめる・DAS カテゴリの年次変化(雑誌別)の図 fig0 を追加 / v007: 雑誌別フォレスト図の軸ラベルを従属変数に合わせる / v008: 対数軸の目盛りを表示範囲に合わせて細かくする(fig7 の査読期間パネル・雑誌別フォレスト図で目盛りが「1」だけになる問題を修正) / v009: fig5 の n 表示の重なりを解消・fig0 の凡例に A・C・N の名称を追加 / v010: 図の雑誌名が途中で切れる問題を修正(IJERPH・IJMS を正式な略称で表示) / v013: --pmc-on-wos-sample(PMC cited-by のモデルを WoS 照合のある論文だけで推定) / v012: WoS と PMC の被引用数を比べる記述統計・相関 --cb-compare を追加 / v011: Supplementary Table S1(被引用数)・S2(査読期間)の tex を自動作成。主モデルの N・クラスタ数を nb_model_*.csv に保存)

使い方
  python3 analyze_citation_review.py --labels            # 1) ラベル(das_*)の点検だけ。読むだけ
  python3 analyze_citation_review.py                     # 2) 被引用数と査読期間の両方を分析
  python3 analyze_citation_review.py --review-as-iv      #    被引用数のモデルに査読期間を説明変数として加える
  python3 analyze_citation_review.py --dv pmc_citedby_n  #    被引用数を PMC の cited-by に替える(頑健性の確認)
  python3 analyze_citation_review.py --target review     #    査読期間だけ / --target citations で被引用数だけ
  python3 analyze_citation_review.py --require-title-fit --require-journal-ok   # WoS 照合が怪しい行の被引用数を除く(頑健性)
  python3 analyze_citation_review.py --corr-top 0        #    責任著者の国のダミーを使わない

モデル
  従属変数   log(1+wos_TC)  と  log(1+days_received_to_accepted) を別々に分析
  固定効果   雑誌(journal_key)×出版年(pub_year)の平均を、全変数から引く
  推定       OLS。標準誤差は HC1(自由度は N-k-固定効果の数で補正)
  説明変数   連続量は log1p したうえで「雑誌×年の中での標準偏差」で割る(1SD あたりの効果)。
             0/1 の変数と DAS のダミーは標準化しない(0→1 の効果)。DAS は --das-ref(既定 F)が基準
  検定       係数ごとの t 検定(正規近似)と、グループごとの Wald 同時検定(DAS 全体など)
  寄与       Shapley 分解(雑誌×年を除いた後の R² をグループ別・因子別に配分)と、グループを抜いたときの ΔR²
注意  観察データの関連であり、因果ではない。

v001 で追加した分析(ICADL2026 の論文の分析・検定に対応。被引用数のモデルで実行。--no-nb / --no-rank / --no-by-journal / --no-interactions で個別に止められる)
  NB 回帰       被引用数(整数)を負の二項回帰(NB2、numpy だけで推定)。固定効果は雑誌+出版年(論文と同じ)。率比 IRR と 95% 区間
  標準誤差      モデルに基づく値と、雑誌×年でクラスタした頑健値(OLS の方にもクラスタ頑健を追加)
  同時検定      DAS 全体などの Wald 検定(通常・クラスタ頑健の両方)
  LRT 重要度    ブロック(DAS・雑誌・出版年・各説明変数)を 1 つずつ外して再推定した LR(論文の LRT 重要度表)
  交互作用      DAS×雑誌、DAS×出版年(--interaction-year 以降)の LRT
  雑誌別        雑誌ごとの NB で DAS の率比。雑誌×類型の全比較に Holm 補正。フォレスト図 nb_forest_by_journal.png
  多重比較      DAS の比較(類型の数)と全係数の 2 通りの Holm 補正
  順位検定      雑誌ごとの Kruskal-Wallis(そのまま・雑誌×年内の順位)と、類型どうしの Mann-Whitney(Holm 補正)
  感度分析      --dedup-key(例 pmcid)の重複を除いて NB を再推定
  記述統計      雑誌×DAS の件数、DAS 類型ごとの被引用数の要約
  論文との違い  使える列が違う(Concept・OpenAlex の列は使わない)ため、共変量・FE・被引用数の窓(3 年 vs 累積)が違い、数値は一致しない。

v003 で追加した頑健性の確認(DAS 類型の効果の並び・向きが、設定を変えても同じか)
  python3 analyze_citation_review_v003.py --robustness                 # 通常の分析のあと、4 通りの設定で NB を走らせ直して比べる
  python3 analyze_citation_review_v003.py --robustness-only            # 通常の分析は飛ばし、頑健性の確認だけ行う(base も走らせる)
  設定  base=wos_TC・FE 雑誌+年 / jy=wos_TC・FE 雑誌×年 / pmc=pmc_citedby_n・FE 雑誌+年 / pmc_jy=pmc_citedby_n・FE 雑誌×年
  比較  DAS 類型の率比の並び・順位相関・向き・有意性の一致、雑誌×類型ごとの向きの一致、向きが逆になった有意セル
  補助  --robust-runs base,jy / --robust-skip-existing(走らせ済みの出力を使う)/ --robust-outroot 保存先
  注意  他の引数(--das-ref、--dedup-key、--require-title-fit など)は子の実行にそのまま引き継ぐ。通常の分析が wos_TC・FE 雑誌+年なら base はその出力を使い回す。

v004・v005 の論文用の図表(分析が保存した CSV から作る。ラベルは英語、図は PNG 300dpi と PDF、表は CSV と paper_tables.xlsx)
  python3 analyze_citation_review_v010.py --dedup-key PMCID --robustness --paper-figs   # 分析・頑健性のあとに図表まで作る
  python3 analyze_citation_review_v010.py --dv review_days --robustness --paper-figs  # 査読期間(日数)を従属変数に、被引用数と同じ分析。出力先は既定で analysis_review
  python3 analyze_citation_review_v010.py --paper-only [--das-ref N]                    # 保存済みの出力から図表だけ作り直す(数秒)
  図  fig1 DAS 類型の率比 / fig2 共変量の率比 / fig3 雑誌×類型の率比ヒートマップ / fig4 因子別寄与(Shapley)/ fig5 類型別の被引用数(または査読期間) / fig6 頑健性の比較 / fig7 被引用数と査読期間の並置(両方を走らせた後、--dv wos_TC の --paper-only で作る)
  表  Table1 雑誌×DAS の件数 / Table2 類型別の被引用数 / Table3 NB の率比 / Table4 Wald・LRT / Table5 雑誌別 / Table6 頑健性
  注意  --paper-only でも --dv、--das-ref、--outdir は分析時と同じにする。入力 CSV がない図表は作らず、一覧を表示する。

v011 で追加した Supplementary Table S1・S2(全係数の NB 推定値)
  python3 analyze_citation_review_v011.py --paper-only                 # 保存済みの出力から図表と S1・S2 を作り直す(数秒)
  python3 analyze_citation_review_v011.py --paper-only --supp-pdf      # さらに pdflatex で PDF まで作る(pdflatex があるとき)
  入力  被引用数: nb_irr_citations_wos_TC.csv(--outdir、既定 analysis)/ 査読期間: nb_irr_review_days.csv(--paper-review-dir、既定 analysis_review)
        N・クラスタ数: 同じフォルダの nb_model_<tag>.csv(v011 の実行が保存)。ない場合は summary.txt から読む
  出力  <paper-dir>/supplementary/IJDL_supplementary_tables.tex(--supp-pdf なら .pdf も)
  注意  査読期間の入力は主モデル(--nb-fe additive)の出力でなければならない。jy(雑誌×年)の出力だと表と本文が食い違うので、
        nb_model_*.csv か summary.txt の FE を見て、additive 以外なら作らずに止める。
        --paper-only を --dv review_days で実行したときは、被引用数の出力フォルダを --paper-citation-dir で指定できる。

v012 で追加した WoS と PMC の被引用数の比較(--cb-compare。論文 3.6節の頑健性・Discussion の根拠。NB は走らせず、数十秒で終わる)
  python3 analyze_citation_review_v012.py --cb-compare            # desc_wos_vs_pmc.csv と desc_wos_vs_pmc_by_journal.csv を --outdir に保存
  対象  WoS 照合あり(wos_matched)かつ PMC cited-by 取得済み(cb_fetched=1)で、両方の値がある論文(NB の共変量による絞り込みの前)
  出力  全体・雑誌別・DAS 類型別に、件数、平均、分散、中央値、四分位、最大、0 の割合、PMC/WoS の平均の比、
        log(1+x) の Pearson 相関、Spearman 相関

v013 で追加  --pmc-on-wos-sample  --dv pmc_citedby_n のとき、WoS 照合のない論文(主に IJERPH 2023 年以降)の被引用数を欠損にして、WoS のモデルと同じ論文集合で比べる
  python3 analyze_citation_review_v013.py --dv pmc_citedby_n --pmc-on-wos-sample --outdir ~/output_covariates_v27/analysis_pmc_samewos
  (NB の N が WoS の主モデルの 648,217 に近くなる。--robustness の子の実行にも引き継がれる)

v014 で追加  --pack-send  Claude に送る結果ファイルを 1 つのフォルダと zip にまとめる(分析は走らせない。数秒で終わる)
  python3 analyze_citation_review_v014.py --pack-send
  入力フォルダ(既定): ~/output_covariates_v27 の下の analysis, analysis/robustness, analysis_pmc_samewos, analysis_pmc_samewos_jy
        (--pack-root で親フォルダ、--pack-dirs でフォルダ名をカンマ区切りで変えられる)
  集める  summary.txt, robustness_*.csv/txt, log_*.txt, nb_irr_*.csv, nb_model_*.csv, nb_by_journal.csv, nb_wald_*.csv, desc_wos_vs_pmc*.csv
        (--pack-max-mb を超える大きなファイルは入れない。名前がぶつからないよう「フォルダ名__ファイル名」にして保存)
  作る    pack_compare_pmc_samewos.csv(WoS 主モデル・PMC 全件・PMC を WoS と同じ論文集合にした 3 通り×FE 2 通りの DAS 率比と、最大差)
        pack_manifest.txt(入れたファイル・見つからなかったファイル・件数)
  出力  --pack-out(既定 ~/output_covariates_v27/send)/ とその zip(--pack-no-zip で zip を作らない)

v015 で追加  --check-journal-groups  論文 3.1節の「981 of 32,206 articles in 2020」「40,563 of 75,937 articles in 2021」が、どの雑誌の集合の件数かを確かめる(分析は走らせない。数秒)
  python3 analyze_citation_review_v015.py --check-journal-groups
  対象  fig0(DAS の年次変化)と同じ論文集合: DAS ラベルあり・--article-type・注記なし・--min-year 以上(合計が論文の 659,437 になるはず)
  雑誌グループ  big3=PLOS ONE・Scientific Reports・Nature Communications / heliyon=Heliyon(MDPI ではない)/ mdpi6=それ以外の 6 誌(MDPI)
  出力  年ごとの 全体・big3・Heliyon・MDPI 6 誌・big3 以外の 7 誌 の件数(journal_groups_by_year.csv を --outdir に保存)
        --check-ref(既定 2020:981:32206,2021:40563:75937。年:該当件数:その年の全体)の件数が、7 誌と 6 誌のどちらに一致するかの判定と、本文の書き換え案

v016 で追加  --check-section31  論文 3.1節の数値が、どの論文集合の値かを確かめる(分析は走らせない。数十秒)
  python3 analyze_citation_review_v016.py --check-section31
  1) 年別の割合(P・A・F・N の 2014〜2025 年の値)を、注記を除いた標本(659,437)と注記を除かない標本(661,282)の両方で計算し、本文の値との一致を判定
  2) 雑誌別の割合(F・P・A・N が最も多い雑誌の値)を、WoS 被引用数のある論文(651,617)と DAS ラベルのある全論文(659,437)の両方で計算し、本文の値との一致を判定
  3) WoS 被引用数の平均・分散・最大を、4 通りの論文集合で計算(本文は 3.1節が 19.55・2,305・8,061、3.7節が 19.50・2,296)
     3.1節の値が NB モデルの対象(648,217 件)なら、どの集合とも一致しない。その場合は analysis/summary.txt の「[NB] 分析対象」の行を見る
  出力  section31_year_shares.csv、section31_journal_shares.csv を --outdir に保存
  図の凡例の名称  DAS_NAMES の M を「Mixed Public Repository + Author Request」、P を「Public Within Article/Supplement Only」に直した(論文の表2と同じ)。
     fig1・fig7・fig0 に出る名称が変わるので、図は --paper-only で作り直す

v017 で追加  分析に使った件数(論文の表1・抄録・結論の件数)を表示・保存する
  1) 通常の実行: summary.txt に「[標本の件数]」を入れる(行の絞り込みの各段階、モデルごとの N と雑誌×年のグループ数)。sample_flow.csv も --outdir に保存
  2) --check-sample  回帰を走らせず、件数だけを数える(CSV を 5 回読むので数分)。次の 5 つの標本を数え、論文の値(--check-n-ref)と照合する
       WoS 被引用数のモデル / PMC cited-by のモデル / 査読期間のモデル / PMC を WoS 照合のある論文に限ったモデル / 題名が合う WoS 照合に限ったモデル
     WoS 被引用数のモデルの標本については、平均・分散・最大も出す(論文 3.1節の 19.55・2,305・8,061 がモデルの標本の値かの確認になる)
     結論・抄録に入れる英文(「648,217 in the citation models and 655,763 in the peer review models」の形)も出す
     python3 analyze_citation_review_v017.py --check-sample
  出力  sample_check.csv を --outdir に保存

v019 で修正  補足表 S1・S2(--paper-only で作る IJDL_supplementary_tables.tex)の DAS 類型の名称を、論文の表2の名称に合わせた
  変更前 P: Public in Article/Supplement Only / N: No Data/Not Applicable / R: Reuse of Third-Party Data Only / M: Mixed Repository + On Request
  変更後 P: Public Within Article/Supplement Only / N: No Data Generated/Not Applicable / R: Reuse of Public Third-Party Data Only / M: Mixed Public Repository + Author Request(A・C・F は同じ)
  付表の tex を作り直すには  python3 analyze_citation_review_v019.py --paper-only

v018 で追加  論文 3.6節の「N を基準にした対比の p 値」と、3.5節の「DAS×雑誌の LRT の df = 49」を確かめる(どちらも CSV を 1 回読む。df の確認は回帰を推定しないので数分、対比は主モデルを 1 回推定する)
  1) --check-contrast  主 NB モデル(基準 F)を 1 回だけ推定し、別の基準(--contrast-ref、既定 N)との対比を出す
       python3 analyze_citation_review_v018.py --check-contrast                    # 被引用数(WoS)。論文 3.6節の F・C・M・R・P・A と N の比較
       python3 analyze_citation_review_v018.py --check-contrast --dv review_days   # 査読期間
     対比は β_k − β_N(F は −β_N)で、モデルを --das-ref N で推定し直したときの係数・標準誤差・p と同じ値になる(再パラメータ化。クラスタ頑健分散も同じ)
     出力  各対比の IRR・95%区間・p(クラスタ頑健とモデルに基づく値)・Holm 調整後の p(6 比較)・Holm の順位と倍率・論文に貼る英文
           nb_contrast_<tag>_ref<N>.csv を --outdir に保存。通常の実行(nb_suite)でも同じ表を summary.txt に出す
  2) --check-df  DAS×雑誌・DAS×出版年の交互作用の自由度(df)の内訳を、回帰を推定せずに調べる
       python3 analyze_citation_review_v018.py --check-df                          # 被引用数
       python3 analyze_citation_review_v018.py --check-df --dv review_days         # 査読期間
     出力  類型×雑誌の件数表(--min-inter 未満のセルに印)、交互作用の列数(最大 (類型数−1)×(雑誌数−1) = 54)、
           件数が足りなくて除いた列、階数の増分(df)、雑誌別の NB で比較できるセル数(論文の「54 comparisons」に対応)
           nb_das_journal_cells_<tag>.csv を --outdir に保存。通常の実行でも nb_interaction_<tag>.csv に列数・階数を加える

v025 で追加  --check-extra  追加の確認 8 つ(すべて全行で推定。--nb-sample は無視。1 つ終わるごとに check_extra_<tag>.txt を保存。1 つが失敗しても続ける)
  python3 analyze_citation_review_v030.py --check-extra                      # 被引用数(WoS)で全部(field は --field-col があるときだけ)
  python3 analyze_citation_review_v030.py --check-extra --dv review_days     # 査読期間(age は被引用数用なので飛ばす)
  python3 analyze_citation_review_v030.py --check-extra tost,meta            # 一部だけ
  tost    同等性検定(TOST)。率比が [1/(1+δ), 1+δ] に入るか(δ は --tost-bounds、既定 0.05 と 0.10)。t(G−1)、Holm は類型の数。同等と言える最小の範囲も出す
  meta    雑誌別の率比(nb_by_journal.csv)の変量効果メタ分析。DL と Hartung–Knapp の区間、τ、I²、予測区間。推定し直さない(数秒)
  revalt  日数のモデル違い。NB・log(1+y) の OLS・ガンマ GLM(対数リンク、y>0)・M を除く・M を基準に統合(--revalt-cat)。--dv review_days 用
  loo     雑誌を 1 つずつ除いた主モデル(10 回の NB)。向きと有意性が保たれた回数、率比の範囲
  age     log 経過年数の折れ線スプライン(--age-knots 個の結び目)と、雑誌別の傾きを加えたモデル。主モデルと DAS の率比・AIC を比べる(--dv wos_TC / pmc_citedby_n)
  field   --field-col の分野ダミーを加えたモデルと加えないモデルの比較、分野ブロックの LRT・Wald。先に --find-cols で列を探す
  aft     査読期間の AFT。対数正規(打ち切りなしでは log y の OLS と同じ)、log(y+shift) の対数正規(日数 0 を残す、--aft-shift)、Weibull(ニュートン法、クラスタ頑健)、ガンマ GLM を NB と並べる。
          時間比と Holm 後 p、対数正規と Weibull の AIC(y のスケール)、残差の分位点を出す。--dv review_days 用。受理された論文だけなので右打ち切りはなく、選択(却下の除外)は直らないことを出力に書く
  window  経過年数(調査日−出版日)が --window-ages(既定 3,5)年以上の論文に絞り、main・age_cov(log 経過年数)・spline の 3 仕様で DAS の率比・AIC・弾力性を比べる。--dv wos_TC / pmc_citedby_n 用
  出力  check_extra_<名前>_<tag>.csv と check_extra_<tag>.txt を --outdir に保存。通常の実行の summary.txt には「[NB] 全行で推定(標本抽出なし)」を入れる

v058 で追加  --check-extra ratiodir  WoS と PMC の雑誌×類型の率比(各 DAS 類型 × 雑誌、基準 F)が 1 の同じ側にある数(本文 3.6 の「same direction in N of 54 comparisons」の根拠)
  python3 analyze_citation_review_v060.py --dv wos_TC --check-extra ratiodir     # 保存済みの check_extra_ratio_by_journal_citations_wos_TC.csv を読むだけ(数秒。先に --check-extra ratio が必要)
  python3 analyze_citation_review_v060.py --dv wos_TC --check-extra ratio        # 推定してから、同じ要約も出力(パイプライン)
  出力  比較の数・同じ向きの数・逆向きの数、WoS か PMC の率比が 1 に近い(|IRR−1|<0.005)組、両方が Holm 後 p<0.05 の組での同じ向きの数、逆向きの組の一覧。check_extra_ratiodir_<tag>.csv に組ごとの表を保存
  注意: 「同じ向き」は率比の点推定が 1 の同じ側にあるかだけで、有意性は問わない。1 にきわめて近い組は偶然で向きが変わるので、数を本文に書くときは近い組の扱い(含める・除く)を決めておく。

v057 で追加  --check-extra repo の 1 にする類型の組に FMC(F+M+C)・FMPC(F+M+P+C)を使えるようにした(JASIST 査読対応: PLOS OSI は条件付きアクセスの共有も数えるので、制限付きアクセスの C を含めた感度)
  python3 analyze_citation_review_v057.py --check-extra repo --repo-defs FM,FMP,FMC,FMPC --repo-specs all,pa --repo-adj main,fe
  組の指定は v055 から類型の文字の並びで任意に書けるので、推定の仕組みは v056 と同じ(組 FMC の比較対象は all = A+N+P+R、pa = P+A、a = A)。変更は、help と読み方の文、出力ファイル名の接尾辞(--repo-suffix)だけ。
  --repo-suffix  出力 check_extra_repo_<tag><接尾辞>.csv と check_extra_<tag><接尾辞>.txt の末尾に付ける文字(既定は空)。組を分けて走らせるとき、先の結果が上書きされないように使う(例 --repo-suffix _fmc)。
  注意: 既定の組と同じ名前で走らせると、先の check_extra_repo_<tag>.csv と check_extra_<tag>.txt は上書きされる。FM・FMP の結果を残すには、接尾辞を付けるか、組を 1 回にまとめて走らせる。

v056 で追加  --das-platform-report  P(識別子なし)のうち、リポジトリらしい文の量の概算(回帰は走らせない)
  python3 analyze_citation_review_v056.py --das-platform-report --csv ~/output_covariates_v27/pmc_wos_v27_3llms.csv --outdir ~/output_covariates_v27/analysis_platform
  対象: --csv の DAS ラベルあり・--article-type・WoS の注記なし・--min-year 以上の行(論文の分析の母集団と同じ条件)。DAS の本文は --csv の das_text 列を使う(別のファイルは要らない)
  数えるもの: データ置き場の名前(Zenodo・Figshare・Dryad・OSF・Mendeley Data・Dataverse・Kaggle・Hugging Face など)/ コード置き場の名前(GitHub・GitLab・Bitbucket・SourceForge)
              それぞれについて、識別子らしい文字列(DOI・doi.org・GEO/SRA/PRJNA などの受入番号・Zenodo/Figshare の番号つき URL・osf.io/5 文字)が同じ文にあるかで、「識別子あり」「識別子なし」に分ける
  --platform-extra  置き場の名前を足す正規表現(例 'openneuro|synapse|mendeley')。データ置き場の側に入る
  --platform-sample  P のうち「データ置き場の名前あり・識別子なし」「コード置き場の名前だけ・識別子なし」から人手の確認用に抜く件数(各 N、既定 60、--seed で固定)
  出力  das_platform_by_category.csv(類型ごと)・das_platform_P_by_journalgroup.csv・das_platform_P_by_year.csv・das_platform_P_sample.csv(manual_repo_like 列を人手で 1/0 にする)・das_platform_report.txt
  注意: 語句の検索なので、名前が出ても否定文(「GitHub にはない」など)や参考文献としての言及を含みうる(上限側の概算)。標本の人手の確認で適合率を出し、割合に掛けて点推定にする。
        P の定義上、識別子があれば F になるはずなので、P で「識別子あり」が多ければ、分類の誤りか識別子の判定基準のずれを示す。

v055 で追加  --check-extra repo  「リポジトリ共有か否か」の 2 値の DAS による NB(査読の PLOS OSI との「reconcile」への対応)
  python3 analyze_citation_review_v055.py --check-extra repo                          # 被引用数(WoS)
  python3 analyze_citation_review_v055.py --check-extra repo --dv review_days         # 査読期間
  python3 analyze_citation_review_v055.py --check-extra repo --repo-defs FM --repo-specs all,pa --repo-adj main   # 絞って速く
  --repo-defs   1 にする類型の組(カンマ区切り、既定 FM,FMP)。FM = F+M(リポジトリ共有の正味)、FMP = F+M+P(P に識別子なしのリポジトリ共有が含まれる可能性の上限側)、FMC = F+M+C(v057: 制限付きアクセスの C を含める)、FMPC = F+M+P+C
  --repo-specs  0 側(比較対象)の取り方(既定 all,pa,a)。all = 1 の組以外すべて / pa = P と A だけ / a = A だけ(文字の並びで任意の類型を指定できる。例 an)
                1 の組と重なる類型は比較対象から除く。比較対象に使う行だけで推定する(他の類型の行は入れない)
  --repo-adj    調整(既定 main,fe)。main = 主モデルと同じ全共変量 / fe = 雑誌+出版年の固定効果だけ(共変量なし)
  --repo-ref-pct 本文が引く値(%)(既定 4.3)。被引用数のとき、推定の変化率(%)の 95% 区間にこの値が入るかを表示する(区間の包含の表示だけで、検定ではない)
  率比 = 「1 の組であること」の 0→1 の率比(1 の組以外・比較対象に対して)。変化率(%) = (率比 − 1) × 100。標準誤差は主モデルと同じ雑誌×年クラスタ頑健。
  出力  check_extra_repo_<tag>.csv(組×比較対象×調整ごとの率比・95% 区間・変化率・p・N・1 の組の件数・クラスタ数・収束)
  注意: 主モデルの 6 つの類型ダミー(基準 F)とは別のモデルで、類型ごとの違いは平均される(F と M の効果が違えば、2 値の係数はその件数による加重平均になる)。
        誤分類(特に M の低い再現率・適合率)の補正はしていない。

v031 で追加  --check-extra ratio  PMC と WoS の被引用数の差(網羅の偏り)の確認(査読 2 の「PMC と WoS で向きが逆になる類型の機序をもっと調べる」への対応)
  python3 analyze_citation_review_v031.py --check-extra ratio                 # --dv wos_TC のまま(WoS が使える論文のうち WoS≧1 かつ PMC の cited-by を取得できた論文)
  同じ論文の集合で、次の 3 つの NB(基準 F、雑誌+年の固定効果、32 共変量、雑誌×年クラスタ)を並べる
    wos        従属変数 = WoS の被引用数
    pmc        従属変数 = PMC の cited-by 数
    pmc_per_wos 従属変数 = PMC の cited-by 数、オフセット = log(WoS の被引用数)。DAS の率比 = 「PMC/WoS の比」が基準 F に対して何倍か
  読み方: pmc_per_wos の率比が 1 から外れる類型は、その類型の論文が PMC 内の論文に引用される割合(WoS に対する)が F と違う。wos と pmc の率比の差(pmc/wos)が、pmc_per_wos とほぼ一致する。
  雑誌別(各雑誌で同じ 3 つ)も出す。逆転が特定の雑誌で起きているか、雑誌をまたいで同じ向きかを見る。雑誌ごとの Holm は雑誌×類型の全比較にかける。
  記述統計: 類型×雑誌ごとの Σ PMC / Σ WoS(比の和)と、論文ごとの PMC/WoS の中央値。
  出力  check_extra_ratio_<tag>.csv(全体の 3 モデル)、check_extra_ratio_by_journal_<tag>.csv、check_extra_ratio_desc_<tag>.csv
  注意: PMC の cited-by は PMC に収録された論文からの引用だけを数えるので、引用する側の分野の PMC 収録率に依存する(生物医学に偏る)。この確認は、そう読める証拠を出すだけで、機序を特定するものではない。
         WoS=0 の論文はオフセットが使えないため除く。主モデルの標本より小さくなる(除いた行数を出力に書く)。

v033 で追加  --main-figs  本論で使う図を、保存済みの CSV から PNG だけ(300dpi)で作る。分析は走らせない。表・補足表・PDF は作らない
  python3 analyze_citation_review_v035.py --main-figs [--outdir 被引用数の出力] [--paper-review-dir 査読期間の出力] [--paper-dir 保存先]
  v035 頑健性の 4 系列: WoS・雑誌+年=--outdir の主モデル / WoS・雑誌×年=--fig6c-wos-jy(既定 <outdir>/robustness_nospline/jy)/ PMC・雑誌+年=--fig6c-pmc(既定 analysis_pmc_samewos)/ PMC・雑誌×年=--fig6c-pmc-jy(既定 analysis_pmc_samewos_jy)。そろわなければ従来の robustness/robustness_das_overall.csv を使い、主モデルとずれていれば警告する
  雑誌×年の WoS を年齢の項なしで作る: python3 analyze_citation_review_v035.py --robustness-only --robust-runs jy --pmc-on-wos-sample --noise-min-count 5 --noise-reps 20 --robust-outroot ~/output_covariates_v27/analysis/robustness_nospline
  出力  <paper-dir>/figures_main/ に 7 点: fig0_das_trend_by_journal / fig7_citations_vs_review_irr / fig3_das_irr_by_journal_heatmap / fig3_das_irr_by_journal_heatmap_review / fig4c_shapley_both / fig5c_crude_vs_adjusted / fig6c_robustness_both
  入力  fig0 は --csv(元の CSV)から作る。ほかは被引用数(--outdir)と査読期間(--paper-review-dir)の出力。ない図は作らず、最後に一覧を出す

v032 で追加  論文用の図の改訂(--paper-figs / --paper-only。分析は走らせず、保存済みの CSV から作る)
  修正  fig7: 類型の並びを本文の表(P, A, N, C, R, M)に合わせ、全類型に名称を付けた。fig1・fig7 の名称は表2と同じ(DAS_NAMES_LEGEND)にした
        fig3(ヒートマップ): 色の目盛りを log IRR から率比(0.75〜1.3)に替えた(セルの数値と同じ単位)
  追加  fig4c_shapley_both       RQ3: 因子別の Shapley 寄与を被引用数と査読期間で並べる(因子の並びを共通にする。DAS を赤)
        fig5c_crude_vs_adjusted  RQ1・RQ2: 調整前(平均の比)と調整後(NB の率比と95%区間)を類型ごとに並べる。調整で向きが変わる類型(M など)を見せる
        fig6c_robustness_both    頑健性: 被引用数(WoS・PMC×固定効果 4 通り)と査読期間(2 通り)を 1 枚に
        fig8_journal_forest(_review)  雑誌別の率比を95%区間つきで示す(ヒートマップは区間を示さない)。補足資料向き
  入力  査読期間の出力は --paper-review-dir(既定 analysis_review)。shapley_factor_review_days.csv・desc_das_citation_summary.csv・robustness/robustness_das_overall.csv・nb_by_journal.csv を読む。ない図は作らず、一覧に出す
  注意  --dv wos_TC で作る(fig7 と同じ)。fig1・fig2・fig4・fig5・fig6 の単独の図は従来どおり作る(補足資料用)

v025 で追加(続き)  査読コメント(累積被引用数・査読期間の分布・非差異的誤分類)への対応
  1) --exposure spline  通常の実行(NB・LRT・交互作用・雑誌別・頑健性)に log 経過年数の折れ線スプライン(--age-knots 個の結び目)を共変量として入れる。年齢を主モデルに入れる版
       python3 analyze_citation_review_v030.py --exposure spline --robustness --paper-figs
  2) --check-misclass-ext  誤分類の補正の拡張(--check-misclass の後に実行すると、全体の混同行列の結果との比較も出す)
       strat  参照セットの混同行列を雑誌のグループ(big3・MDPI 6 誌・Heliyon、--noise-strata journal なら雑誌ごと)で作り、各行に全体の行の割合×--noise-shrink を足して縮め、Dirichlet から引いて補正
       diff   雑誌×年内の結果の順位で上位半分・下半分に分け、上位では誤分類のオッズを φ 倍、下では 1/φ 倍にして補正(--diff-phi、--diff-reps)。φ ごとの率比と、結論が変わる φ を出す
       python3 analyze_citation_review_v030.py --check-misclass-ext strat --reference-csv ~/reference_1200.csv --ref-cols journal,human,pred --noise-reps 20
       python3 analyze_citation_review_v030.py --check-misclass-ext diff --reference-csv ~/reference_1200.csv --diff-phi 0.5,1,2,3 --diff-reps 5
       参照セットの CSV は 1 行 1 文(雑誌、人手のラベル、予測ラベル。予測は交差検証の out-of-fold)。strat には必須、diff は --confusion-csv(全体の行列)でも動く
  3) --check-extra aft / window  上の check-extra の項を参照(aft は --dv review_days、window は --dv wos_TC)
  4) --check-extra 全体の実行時間: window は 3 つの標本×3 仕様の NB(9 回)なので、tost,meta,revalt,loo,age,field,aft,window をすべて走らせると長い。必要なものだけカンマ区切りで指定できる

v020 で追加  査読コメント(技術的な指摘 4 点)への対応。いずれも被引用数(--dv wos_TC または pmc_citedby_n)の NB を対象にする
  1) 経過時間の扱い(「出版年の固定効果だけでは経過時間の残差が残る」)
       python3 analyze_citation_review_v020.py --find-cols 'date|month|day'     # まず出版日の列名を探す
       python3 analyze_citation_review_v020.py --check-exposure --exposure-cols pub_date,date_published,pub_month   # 4 通りの NB を比べる
         none=出版年の固定効果のみ(主モデル)/ offset=log(経過年数)をオフセット / covariate=log(経過年数)を係数つきで(係数=弾力性、1 ならオフセット妥当)/ jy_offset=雑誌×年の固定効果+オフセット
       --exposure offset|covariate を付けると、通常の実行(NB・LRT・交互作用・雑誌別・頑健性)にも同じ設定が入る。経過年数=(調査日−出版日)/365.25
       --exposure-ref-date 調査日(既定: WoS 2026-06-15、PMC 2026-10-29)/ --exposure-min-age 経過年数の下限(既定 0.05)
       出版日の列がなければ、受理日などで代用できる(--exposure-cols の左の列を先に使い、ない行は次の列、最後は出版年の 7/1)
  2) ゼロの多い PMC の被引用数(「ゼロ過剰・ハードルとの比較がない」)
       python3 analyze_citation_review_v020.py --check-zero --dv pmc_citedby_n --outdir ~/output_covariates_v27/analysis_zero
         NB2 が予測するゼロの割合(全体・雑誌別)と実際、ハードルモデル(ロジット+ゼロ切断 NB)の DAS の関連、AIC を出す。nb_hurdle_*.csv
  3) 小さいクラスタ数(「72〜74 クラスタ。CR2・WCB などで補強を」)
       python3 analyze_citation_review_v020.py --check-cluster [--boot-reps 999] [--boot-weights webb|rademacher]
       python3 analyze_citation_review_v051.py --check-wos-gap [--dv wos_TC] [--gap-spec ENVIRON:2023,HELIYON:2025]   # WoS 未照合が集中する期間を除いた感度分析
       python3 analyze_citation_review_v051.py --check-adjust-sets [--dv wos_TC|review_days] [--adjust-sets FE,D,B,A,Main]   # 調整集合を替えた DAS の率比の比較(D=DAS に先行する共変量だけ)
       python3 analyze_citation_review_v051.py --check-vif [--dv wos_TC|review_days] [--vif-threshold 5]   # 多重共線性(VIF・GVIF)。固定効果込み・共変量だけ・ブロック別
         正規近似・t(G−1)・wild cluster score bootstrap(スチューデント化)の p と区間。NB(GLM)には CR2 の標準形がないため bootstrap で補う。nb_cluster_inference_*.csv
  4) Shapley が OLS の代理モデルである点(「NB との不一致」)
       python3 analyze_citation_review_v024.py --shapley-nb                       # 全行(論文にはこれを使う)
       python3 analyze_citation_review_v024.py --shapley-nb --dv review_days   # 査読期間
       python3 analyze_citation_review_v024.py --shapley-nb-both               # 被引用数と査読期間を続けて実行
       python3 analyze_citation_review_v024.py --shapley-nb --nb-sample 50000  # 動作確認用の標本(暫定値)
         NB の対数尤度の改善(固定効果だけのモデルに対する ΔLL)を、グループ間で Shapley 配分(グループ数 k に対して 2^k 回の NB)。OLS 版との順位相関も出す。shapley_nb_group_*.csv
  どの確認も --outdir は分析時と同じ(OLS 版の shapley_group_*.csv を読むため)。--exposure は 1〜4 のどれとも組み合わせられる(オフセットつきで推定)。
v042 で追加  OpenAlex の年次被引用数(counts_by_year)を従属変数にする(WoS の TC・PMC の cited-by に加える)
  1) 取得と結合(DOI ごと。取得は再開できる。--oa-batch 100 で呼び出し回数が半分):
     export OPENALEX_API_KEY=...
     python3 analyze_citation_review_v042.py --fetch-counts --oa-mailto あなたのメール --oa-batch 100        # --csv の既定は topic 結合後の CSV
     python3 analyze_citation_review_v042.py --merge-counts                                                   # pmc_wos_v27_3llms_topic_counts.csv を作る。取得できる年の範囲の確認表も出る
     新しい列  oa_found, oa_pubyear, oa_pubdate, oa_cited_total, oa_cy_<年>(その年の被引用数。OpenAlex が 0 の年を省くので空は 0 扱い、ただし取得範囲の外は使わない)
     取得範囲  OpenAlex の counts_by_year は「おおむね直近 10 年」。出版年が古い論文の窓が範囲にかかる場合は、その論文を窓の従属変数から除く(--oa-cover-from で上書き、既定は自動判定)
     今年(--oa-last-year、既定 2025 の次の年)は途中なので窓に入れない
  2) 従属変数(--dv。既存の分析がそのまま動く。出力先の既定は analysis_<dv>):
     oa_c<k>   出版年を含む k 年の累積(出版年〜出版年+k-1)。例 oa_c2, oa_c3, oa_c4, oa_c5
     oa_a<j>   出版年から j 年後の 1 年分(0=出版年)。DAS の効果が何年目に出るかを見る
     oa_l<k>   直近 k 暦年(--oa-last-year まで)。出版年は問わない(出版年の固定効果で古さを調整)
     oa_total  OpenAlex の cited_by_count(全期間)
     python3 analyze_citation_review_v042.py --dv oa_c3 [--exposure offset] [--oa-field field]
     --exposure offset  窓の終わり(12/31)までの経過年数をオフセットにする(出版月の違いの調整。oa_c<k> と oa_a0 のみ)
     --oa-field none|field|domain|sub<N>  OpenAlex の分野のダミーを共変量に加える(既定 field=26 分野。短い窓ほど分野による引用の速さの違いが大きいので既定で入れる。none で WoS の主モデルと同じ説明変数)
     NB 版 Shapley も同じ指定で動く: python3 analyze_citation_review_v042.py --dv oa_c3 --shapley-nb
  3) 窓ごとの比較 --oa-suite(同じ説明変数・同じ固定効果で、窓と標本だけを変えて主モデルを推定):
     python3 analyze_citation_review_v042.py --oa-suite [--oa-windows 2,3,4,5] [--oa-lags 0,1,2,3] [--oa-suite-extra wos_TC,pmc_citedby_n] [--oa-sample both] [--oa-lrt on] [--oa-skip-existing]
     標本  own=各従属変数で使える行すべて / common=すべての OpenAlex 窓が使える行(長い窓ほど古い論文だけになる標本の違いを除く)
     出力  oa_suite_irr_<dv>_<標本>.csv(全係数の率比・Holm 後 p)/ oa_suite_ame_*.csv(DAS の平均限界効果。全論文をその類型にしたときの基準との期待被引用数の差、1,000 本あたり)/
           oa_suite_lrt_*.csv(グループを外したときの LR=説明変数グループの寄与)/ oa_suite_*_all.csv / oa_suite_cov_irr_<標本>.csv / oa_suite_das_irr_<標本>.png / oa_suite_summary.txt
     寄与の見方  率比=相対的な効果の大きさ、平均限界効果=件数での大きさ、LR=モデルの当てはまりへの寄与(DAS を他のグループと比べる)。Shapley は --dv oa_c<k> --shapley-nb で別に行う
     注意  窓が重なる従属変数の率比の差は検定しない(同じ論文・重なる期間のため独立でない)。観察データの関連であり因果ではない
v040 で追加  分野の係数の補足表(Supplementary Table S3・S4)
  1) 分野の係数を保存する(被引用数と査読期間の両方で、1 回ずつ実行する。各約 1 分):
     python3 analyze_citation_review_v040.py --csv ~/output_covariates_v27/pmc_wos_v27_3llms_topic.csv --check-extra subfield --subfield-variants field,domain,sub50
     python3 analyze_citation_review_v040.py --csv ~/output_covariates_v27/pmc_wos_v27_3llms_topic.csv --check-extra subfield --dv review_days --subfield-variants field,domain,sub50
     出力  check_extra_subfield_coef_field_<tag>.csv など(水準名・モデルの標本での件数・率比・95%CI・p・Holm 後の p。Holm はそのモデルの分野の係数全体にかける)
  2) tex を作る:
     python3 analyze_citation_review_v040.py --supp-field [--outdir 被引用数の出力] [--paper-review-dir 査読期間の出力] [--supp-field-specs field,domain,sub50]
     出力  <--paper-dir>/supplementary/IJDL_supplementary_field_tables.tex(S3・S4。本文の tex の longtable に貼る。番号は S3・S4 から)
v039 で追加  OpenAlex の論文単位の分野(primary_topic: topic → subfield → field → domain)の取得から感度分析までを 1 本にした(fetch_openalex_topics.py を統合)
  python3 analyze_citation_review_v039.py --topics-pipeline --oa-mailto あなたのメール         # 取得(再開可)→結合→subfield を入れた NB(被引用数・査読期間)まで続けて行う
  python3 analyze_citation_review_v039.py --fetch-topics --oa-mailto あなたのメール            # 取得だけ。キーは環境変数 OPENALEX_API_KEY か --oa-api-key。取得済みは飛ばして続きから
  python3 analyze_citation_review_v039.py --merge-topics                                          # 結合だけ(付与率・水準数・topic_subfield_counts.csv を出す)
  python3 analyze_citation_review_v039.py --csv ~/output_covariates_v27/pmc_wos_v27_3llms_topic.csv --check-extra subfield [--dv review_days] [--subfield-variants field,sub50,sub100]
  取得   DOI を --oa-batch 件(既定 50、最大 100)ずつ OR で束ねて 1 回の list で取る(1 回 1 クレジット)。429 のときは rate-limit を調べ、予算切れなら再試行せず
         リセット時刻(UTC と Mac の時刻)を出して止まる(取得済みは保存済み。翌日に同じコマンドで再開)。取得日・条件は openalex_topics_meta.json に残る(Methods・Zenodo 用)
  結合   openalex_topics.jsonl(生データ。従来と同じ形式)を CSV に結合し、oa_topic・oa_subfield・oa_field・oa_domain・oa_topic_score を足す
  感度分析 subfield   主モデル(分野なし)と、field(26)・domain(4)・subfield 上位 N のダミーを加えたモデルで DAS の率比・Holm 後 p・LRT・Wald・AIC を並べる。
         subfield と雑誌の関係(Cramér の V、雑誌ごとの水準数)も出す。OpenAlex の分類器は雑誌名を入力に使うので、雑誌の固定効果と重なる点に注意。
         全 247 水準は入れず、上位だけをダミーにして残りは基準側にまとめる(行列が大きくなるため)。出力 check_extra_subfield_<tag>.csv など
v052 で追加  JASIST 査読対応(分類性能のカテゴリ別の報告と、DOI ごとのラベルの公開)。どちらも回帰は走らせず、数十秒〜数分で終わる
  1) --classifier-report  参照セット(--reference-csv: 1 行 1 文、雑誌・人手のラベル・予測ラベル。--ref-cols で列名)から、カテゴリ別の分類性能を出す
       python3 analyze_citation_review_v052.py --classifier-report --reference-csv ~/reference_1200.csv --ref-cols journal,human,pred
       python3 analyze_citation_review_v052.py --classifier-report --reference-csv ~/reference_1200.csv --ref-lojo-col pred_lojo --clf-corpus
         --ref-lojo-col  leave-one-journal-out の予測の列名(あれば交差検証の予測と並べて出す)
         --clf-corpus    --csv の DAS ラベルの割合(注記なし・--article-type・--min-year 以上)から、「予測が k のとき真も k である確率(PPV)」と補正後の件数の点推定も出す(モデルは推定しない。論文 3.6節の 0.006 などに対応)
         --clf-order     類型の並び(既定 F,M,P,R,C,A,N = 表 2 の順)
       出力(<outdir>/classifier_report/)
         confusion_matrix_cv.csv(・_lojo)        行=人手、列=予測の件数(--confusion-csv にそのまま使える)
         classifier_metrics_cv.csv(・_lojo)      類型ごとの人手の件数・予測の件数・適合率・再現率(Wilson 95% 区間)・F1(・PPV)
         classifier_metrics_by_group_cv.csv      雑誌群(big3・Heliyon・MDPI 6 誌)ごとの再現率・適合率・件数、全体の正解率・κ
         classifier_by_journal_cv.csv            雑誌ごとの件数・正解率
         tab_classifier_performance.tex・tab_confusion_matrix.tex・tab_classifier_by_group.tex   本文・補足にそのまま貼れる表(--ref-lojo-col があれば _lojo 付きも作る)
         classifier_report.txt                   上の要約
  2) --export-labels  DOI ごとの DAS ラベルと、その検証に必要な参照セット・混同行列を Zenodo 用のフォルダにまとめる
       python3 analyze_citation_review_v052.py --export-labels --reference-csv ~/reference_1200.csv --ref-lojo-col pred_lojo
         --export-dir      保存先(既定 <outdir>/zenodo_deposit)
         --export-id-cols  識別子の列名(既定 pmcid,doi。大文字小文字は区別しない)。CSV にある列だけを出す
         --export-extra-cols  追加で出す列(カンマ区切り)。WoS 由来の列(wos_ で始まる列)は規約上出さない
         --export-expect   論文に書いた件数(既定 661,365)。違えば警告
       出力  das_labels_per_article.csv(識別子・雑誌・出版年・アンサンブルのラベル・3 LLM の個別ラベル・3 者一致)/ das_labels_summary_by_journal.csv /
             reference_set.csv(雑誌・人手・予測の列だけ)・混同行列・分類性能の表(--reference-csv があるとき)/ README_labels.txt / MANIFEST.sha256
       注意  WoS の被引用数・照合結果・WoS の注記による除外の印は含めない(Clarivate の規約)。通常は DAS の本文(das_text)も含めない。

v061 で追加  --export-public  公開用データ(GitHub に置き、受理後に Zenodo へ)を 1 つのフォルダにまとめる(回帰は走らせない)
  python3 analyze_citation_review_v061.py --export-public --export-dir ~/das-citation-review-data/data --reference-csv ~/reference_1200.csv --ref-lojo-col pred_lojo --wos-query-file ~/wos_query.txt
    出力  articles_public_data.csv.gz(論文単位。--export-max-mb[既定 90]を超えると雑誌ごとに分割)/ data_dictionary.csv / das_labels_summary_by_journal.csv /
          reference_set.csv・混同行列・分類性能の表(--reference-csv があるとき)/ openalex_raw/(OpenAlex の生データ jsonl.gz と取得記録 json。--export-no-openalex-raw で出さない)/
          wos_doi_list.csv・WOS_RETRIEVAL.txt(・wos_query.txt)/ code/(この .py。--export-no-code で出さない)/ settings.json / README_data.md / MANIFEST.sha256 / export_public_log.txt
    列    識別子(--export-id-cols)・雑誌・年・DAS ラベル(アンサンブルと 3 LLM)・SPEC の元の列・has_body・責任著者の国・査読期間の日数・PMC cited-by・OpenAlex の列(oa_*・oa_cy_<年>)・--exposure-cols の日付の列・--export-extra-cols
          列名は分析スクリプトのものと同じ(出力を --csv にそのまま渡せる)。wos で始まる列と das_text は出さない。--export-drop-cols で列を除ける
    注意  WoS の被引用数・照合結果・注記は含めない。公開前に data_dictionary.csv と出力した列を目で確かめる。GitHub は 1 ファイル 100 MB まで

v064 で追加  --export-public の title_words_adj
  title_len_source が wos の行(題名の長さを WoS の題名から取った行。論文の公開用データでは 276 行)は、title_words_adj を PMC の題名から数えた title_words に置き換えて出す。
  title_words・title_len_source は出さない。--export-keep-wos-title で置き換えない(WoS 由来の値が入るので公開には使わない)
  置き換えた行では公開データの共変量が分析時の値と違う(語数のみ。0.04%)。再現の結果への影響は小さいが、気になるなら公開データで主モデルを推定して率比を比べる

v063 で追加  --export-public の取得記録まわり
  python3 analyze_citation_review_v063.py --export-public --export-oa-topics-date "2026-11-08 to 2026-11-09" --csv ... (他の指定は v061 と同じ)
    --export-oa-topics-date  OpenAlex の分野(primary_topic)を取得した日。取得記録 openalex_topics_meta.json がないときだけ使い、
                             openalex_raw/openalex_topics_retrieval_note.txt(著者が記録した日付であることを明記)と README_data.md に書く。記録ファイルがあればそちらを優先し、この指定は使わない
    警告  counts・topics の記録(openalex*meta*.json)の片方が欠けると、どちらが欠けたかを出す。code/ に別の版の .py があれば名前を出す(削除はしない)
    注意  README_data.md は実行のたびに作り直すので、日付は手で追記せずこの引数で渡す
"""

import argparse, glob, hashlib, itertools, json, math, os, re, sys, time
import numpy as np
import pandas as pd

VERSION = "v064"
DEFAULT_CSV = "~/output_covariates_v27/pmc_wos_v27_3llms.csv"
DEFAULT_OUT = "~/output_covariates_v27/analysis"
DEFAULT_PAPER = "~/output_covariates_v27/paper"   # 論文用の図表の保存先(被引用数・査読期間の両方をここにまとめる)
DEFAULT_OUT_REVIEW = "~/output_covariates_v27/analysis_review"   # --dv review_days の既定の出力先


# ---- v044: 出力フォルダの版管理 -------------------------------------------------------------
def _run_suffix(a):
    """既定の出力先に付ける印。--exposure が off 以外なら exp-<方式>、--run-label があればそれも付ける"""
    parts = []
    if getattr(a, "exposure", "off") != "off":
        parts.append(f"exp-{a.exposure}")
    lab = getattr(a, "run_label", "") or ""
    if lab:
        parts.append(re.sub(r"[^0-9A-Za-z_.-]+", "-", lab))
    return ("__" + "__".join(parts)) if parts else ""


def _suffix_outdir(a):
    """--outdir を指定していない(既定のフォルダを使う)ときだけ、出力先に実行条件の印を付ける。1 回だけ働く"""
    if getattr(a, "_suffixed", False):
        return
    a._suffixed = True
    if getattr(a, "_outdir_default", False):
        a.outdir = a.outdir.rstrip("/") + _run_suffix(a)


def _archive_existing(a, folder):
    """既存の結果がある出力先で上書きする前に、直下のファイルを <folder>/_archive/<日時>/ にコピーする(サブフォルダは対象外)"""
    if getattr(a, "no_archive", False) or getattr(a, "oa_skip_existing", False):
        return
    import shutil, datetime
    folder = os.path.expanduser(folder)
    if not os.path.isdir(folder):
        return
    skip = lambda f: f == "RUNINFO.log" or f.startswith("shapley_nb_cache")
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and not skip(f)]
    if not any(f.endswith((".csv", ".tex")) for f in files):
        return
    dst = os.path.join(folder, "_archive", datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    os.makedirs(dst, exist_ok=True)
    for f in files:
        shutil.copy2(os.path.join(folder, f), os.path.join(dst, f))
    print(f"[退避] 既存の結果 {len(files)} 個を {dst} にコピーしてから実行します(止めるには --no-archive)", file=sys.stderr, flush=True)


def _write_runinfo(a, folder):
    """実行の記録(日時・コマンド・版・入力 CSV)を <folder>/RUNINFO.log に追記する"""
    import datetime
    folder = os.path.expanduser(folder)
    os.makedirs(folder, exist_ok=True)
    csvp = os.path.expanduser(a.csv) if getattr(a, "csv", "") else ""
    mt = datetime.datetime.fromtimestamp(os.path.getmtime(csvp)).strftime("%Y-%m-%d %H:%M") if csvp and os.path.exists(csvp) else "不明"
    rec = [f"日時: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}", f"版: {VERSION}",
           "コマンド: python3 " + " ".join(sys.argv), f"従属変数: {getattr(a, 'dv', '')} / 経過時間: {getattr(a, 'exposure', '')} / 固定効果: {getattr(a, 'nb_fe', '')}",
           f"入力 CSV: {csvp}(更新 {mt})", "-" * 60]
    with open(os.path.join(folder, "RUNINFO.log"), "a", encoding="utf-8") as fh:
        fh.write("\n".join(rec) + "\n")


def _tag(dv):
    """出力ファイル名に使う印。被引用数は citations_<列名>、査読期間(日数)は review_days"""
    return "review_days" if dv == "review_days" else f"citations_{dv}"


def _is_rv(dv):
    return dv == "review_days"

# 名前が分かっている類型だけ書く(C, A などは CSV に現れるが、定義はこのファイルでは仮定しない)
DAS_NAMES = {"F": "Fully Public Repository Deposition", "M": "Mixed Public Repository + Author Request",
             "P": "Public Within Article/Supplement Only", "R": "Reuse of Public Third-Party Data Only"}
DAS_NAMES_LEGEND = {**DAS_NAMES, "A": "Author Upon Request Only", "C": "Controlled-Access Repository", "N": "No Data Generated/Not Applicable"}   # 年次推移図(fig0)の凡例用。表2の名称に合わせる
LLM_COLS = ["das_ds32", "das_gpt5", "das_mil3"]

# (新しい列名, 元の列, 変換, グループ, 説明)   変換: log1p / raw / bin(>0) / flag(0/1 のまま)
SPEC = [
    ("n_authors",          "n_authors",            "log1p", "著者・国・共著", "著者数"),
    ("collab_any",         "n_collab",             "bin",   "著者・国・共著", "コンソーシアム著者あり"),
    ("n_corresp",          "n_corresp",            "log1p", "著者・国・共著", "責任著者数"),
    ("equal_contrib_any",  "equal_contrib_any",    "flag",  "著者・国・共著", "同等貢献の注記あり"),
    ("n_orcid",            "n_orcid",              "log1p", "著者・国・共著", "ORCID 付き著者数"),
    ("n_countries",        "pmc_n_countries_u",    "log1p", "著者・国・共著", "国数(英国統合・領土統合)"),
    ("n_institutions",     "n_institutions_ror",   "log1p", "著者・国・共著", "機関数(ROR)"),
    ("n_refs",             "n_refs",               "log1p", "参考文献・助成", "参考文献数"),
    ("ref_age_median",     "ref_age_median",       "raw",   "参考文献・助成", "参考文献の年齢(中央値)"),
    ("has_data_citation",  "n_refs_data",          "bin",   "参考文献・助成", "データの引用あり"),
    ("has_funding",        "has_funding_positive", "flag",  "参考文献・助成", "助成の記載あり"),
    ("body_words",         "body_words",           "log1p", "図表・文章量",   "本文の語数"),
    ("n_figures",          "n_figures",            "log1p", "図表・文章量",   "図の数"),
    ("n_tables",           "n_tables",             "log1p", "図表・文章量",   "表の数"),
    ("n_equations",        "n_equations",          "log1p", "図表・文章量",   "数式の数"),
    ("n_supplementary",    "n_supplementary",      "log1p", "図表・文章量",   "補足資料の数"),
    ("abstract_words",     "abstract_words",       "log1p", "図表・文章量",   "抄録の語数"),
    ("title_words",        "title_words_adj",      "raw",   "題名",           "題名の語数(WoS の注記を除いた補正値)"),
    ("title_has_colon",    "title_has_colon",      "flag",  "題名",           "題名にコロン"),
    ("title_has_question", "title_has_question",   "flag",  "題名",           "題名が疑問形"),
]
BODY_DERIVED = {"body_words", "n_figures", "n_tables", "n_equations", "n_supplementary"}   # has_body=0 なら欠損にする
G_DAS, G_REVIEW, G_CORR = "DAS", "査読期間", "責任著者の国"
FIT_OK = "±3 以内"   # wos_title_fit の「照合が妥当」とみなす値(--labels で実際の値の分布を確認できる)


# ----------------------------------------------------------------------------- 共通
def num(s):
    return pd.to_numeric(s, errors="coerce")


JOURNAL_DISPLAY = {"INTERNATIONAL JOURNAL OF ENVIR": "INT. J. ENVIRON. RES. PUBLIC HEALTH",
                   "INTERNATIONAL JOURNAL OF MOLEC": "INT. J. MOL. SCI."}   # 表示用の正式な略称(キーは先頭が一致すれば適用)


def jshort(series, width=30):
    """雑誌名を表示用に短くする。短くした結果が別の雑誌と同じになる場合は、区別できるまで長くする(先頭が同じ雑誌名の混同を防ぐ)"""
    keys = pd.Series(series).astype(str)
    uniq = keys.unique()
    for w in range(width, 80):
        m = {u: u[:w] for u in uniq}
        if len(set(m.values())) == len(uniq):
            break
    out = keys.map(m)
    for pre, nice in JOURNAL_DISPLAY.items():
        out = out.where(~keys.str.startswith(pre), nice)
    return out


def kappa(a, b):
    ct = pd.crosstab(a, b)
    labs = sorted(set(ct.index) | set(ct.columns))
    ct = ct.reindex(index=labs, columns=labs, fill_value=0).values.astype(float)
    n = ct.sum()
    po = np.trace(ct) / n
    pe = float((ct.sum(1) * ct.sum(0)).sum()) / n ** 2
    return (po - pe) / (1 - pe) if pe < 1 else float("nan")


def chi2_sf(x, k):
    """自由度 k のカイ二乗分布の上側確率 P(X >= x)。正則化不完全ガンマ関数 Q(k/2, x/2) を自前で計算(scipy 不要)"""
    if x <= 0:
        return 1.0
    a, z = k / 2.0, x / 2.0
    lg = math.lgamma(a)
    if z < a + 1:                                   # 級数展開
        term = total = 1.0 / a
        for n in range(1, 2000):
            term *= z / (a + n)
            total += term
            if abs(term) < abs(total) * 1e-15:
                break
        return max(0.0, 1.0 - total * math.exp(-z + a * math.log(z) - lg))
    tiny = 1e-300                                   # 連分数展開(Lentz 法)
    b = z + 1 - a
    c, d = 1 / tiny, 1 / b
    h = d
    for i in range(1, 2000):
        an = -i * (i - a)
        b += 2
        d = an * d + b
        d = tiny if abs(d) < tiny else d
        c = b + an / c
        c = tiny if abs(c) < tiny else c
        d = 1 / d
        delta = d * c
        h *= delta
        if abs(delta - 1) < 1e-15:
            break
    return min(1.0, math.exp(-z + a * math.log(z) - lg) * h)


def read_cols(path, cols):
    path = os.path.expanduser(path)
    head = pd.read_csv(path, nrows=0).columns
    miss = [c for c in cols if c not in head]
    keep = [c for c in cols if c in head]
    d = pd.read_csv(path, usecols=keep, dtype=str, keep_default_na=False, low_memory=False)
    return d, miss


# ----------------------------------------------------------------------------- ラベルの点検
def labels_report(a):
    cols = ["journal_key", "pub_year", "das_found", "das_has_label", "das_text", "das_label", "das_llm_agree"] + LLM_COLS
    d, miss = read_cols(a.csv, cols)
    if miss:
        print("見つからない列:", miss)
    n = len(d)
    print(f"行数 {n:,}")
    print("das_found:", d.das_found.value_counts().to_dict(), "/ das_has_label:", d.das_has_label.value_counts().to_dict())
    print("das_found=1 なのにラベルなし:", int(((d.das_found == "1") & (d.das_has_label != "1")).sum()),
          "/ das_found=0 なのにラベルあり:", int(((d.das_found != "1") & (d.das_label != "")).sum()))
    for c in LLM_COLS + ["das_label"]:
        if c in d:
            print(f"\n[{c}]", d[c].replace("", "(空)").value_counts().to_dict())
    h = d[d.das_has_label == "1"].copy()
    print(f"\nラベルあり {len(h):,} 行")
    # 3つの LLM の一致
    print("\n[LLM どうしの一致率と kappa]")
    for x, y in itertools.combinations(LLM_COLS, 2):
        m = (h[x] != "") & (h[y] != "")
        print(f"  {x} vs {y}: 一致 {(h.loc[m, x] == h.loc[m, y]).mean():.3f}  kappa {kappa(h.loc[m, x], h.loc[m, y]):.3f}  (n={int(m.sum()):,})")
    votes = h[LLM_COLS].values
    all_same = (votes[:, 0] == votes[:, 1]) & (votes[:, 1] == votes[:, 2])
    print(f"  3つとも一致: {all_same.mean():.3f}  / das_llm_agree=1 の割合: {(h.das_llm_agree == '1').mean():.3f}"
          f"  / 食い違い(das_llm_agree と実際の一致): {int(((h.das_llm_agree == '1') != all_same).sum())} 行")
    # 多数決との関係
    maj = []
    for v in votes:
        vals, cnt = np.unique(v, return_counts=True)
        maj.append(vals[cnt.argmax()] if cnt.max() >= 2 else "")
    h["majority"] = maj
    nomaj = h.majority == ""
    print(f"\n[das_label と多数決] 多数決あり {int((~nomaj).sum()):,} 行のうち das_label が一致 "
          f"{(h.loc[~nomaj, 'das_label'] == h.loc[~nomaj, 'majority']).mean():.4f}"
          f" / 3つとも別の答え(多数決なし) {int(nomaj.sum()):,} 行")
    if nomaj.any():
        print("  多数決なしの行の das_label が各 LLM と一致する割合:",
              {c: round(float((h.loc[nomaj, 'das_label'] == h.loc[nomaj, c]).mean()), 3) for c in LLM_COLS})
    bad = h[(~nomaj) & (h.das_label != h.majority)]
    if len(bad):
        print(f"  多数決と違うラベルの行 {len(bad):,}。例:")
        print(bad[["journal_key", "pub_year"] + LLM_COLS + ["das_label"]].head(8).to_string(index=False))
    # 雑誌別・年別
    print("\n[雑誌別のラベルの割合]")
    ct = pd.crosstab(h.journal_key.str[:34], h.das_label, normalize="index").round(3)
    ct.insert(0, "n", h.groupby(h.journal_key.str[:34]).size())
    print(ct.to_string())
    print("\n[雑誌別の 3 LLM 完全一致率]")
    print(pd.Series(all_same, index=h.index).groupby(h.journal_key.str[:34]).mean().round(3).to_string())
    h["y"] = num(h.pub_year)
    print("\n[出版年別のラベルの割合(2014 年以降)]")
    hy = h[h.y >= 2014]
    ct = pd.crosstab(hy.y.astype(int), hy.das_label, normalize="index").round(3)
    ct.insert(0, "n", hy.groupby(hy.y.astype(int)).size())
    print(ct.to_string())
    # キーワードによる目視の代わりの点検
    print("\n[DAS の本文にキーワードを含む行のラベル分布(行の割合)]  — 想定と大きく違う行が混ざっていないかの目安")
    kws = {"dbgap": r"dbgap", "on/upon request": r"(?:on|upon) (?:reasonable )?request|by request",
           "corresponding author": r"corresponding author", "supplement": r"supplement",
           "figshare/zenodo/dryad": r"figshare|zenodo|dryad", "GEO/SRA/PRJNA": r"\bGSE\d|\bSRR\d|PRJNA|ArrayExpress",
           "not applicable/no data": r"not applicable|no data|no new data|not available"}
    t = h.das_text
    rows = {}
    for k, pat in kws.items():
        m = t.str.contains(pat, regex=True, case=False)
        if m.sum():
            rows[k] = {"n": int(m.sum()), **h.loc[m, "das_label"].value_counts(normalize=True).round(3).to_dict()}
    print(pd.DataFrame(rows).T.fillna(0).to_string())
    print("\n[ラベルありで das_text が空の行]", int((h.das_text == "").sum()))
    d2, _ = read_cols(a.csv, ["wos_matched", "wos_journal_ok", "wos_title_fit", "wos_title_prefix_suspect", "wos_missing_reason",
                              "wos_notice_type", "wos_merged_any", "corr_country_u", "corr_country_status"])
    print("\n[WoS 照合の品質と責任著者の国の点検(全行)]")
    for c in d2.columns:
        vc = d2[c].replace("", "(空)").value_counts()
        print(f"  {c}:", vc.head(8).to_dict(), "" if len(vc) <= 8 else f"... 他 {len(vc) - 8} 種")


# ----------------------------------------------------------------------------- 件数の記録と表示(v017)
def _flow(a, key, n):
    """行の絞り込みの各段階の件数を a.flow(辞書)に記録する。a.flow がなければ何もしない"""
    fl = getattr(a, "flow", None)
    if fl is not None:
        fl[key] = int(n)


def model_sample(d, dv, ivs, args):
    """run_model と同じ手順で分析対象の行を決める(欠損の多い説明変数を外す→欠損のある行を除く→雑誌×年が --min-group 件未満の群を除く)。
    戻り値: (use, 使う説明変数, 外した説明変数, 欠損率, 件数の辞書)"""
    use = d[["gid", dv] + ivs].copy()
    miss = use[ivs].isna().mean()
    drop = [c for c in ivs if miss[c] > args.max_missing and c != "log_review"]
    ivs2 = [c for c in ivs if c not in drop]
    n_dv = int(use[dv].notna().sum())
    use = use.dropna(subset=[dv] + ivs2)
    n_cov = len(use)
    cnt = use.gid.value_counts()
    small = cnt[cnt < args.min_group]
    use = use[use.gid.isin(cnt[cnt >= args.min_group].index)]
    info = dict(n_dv=n_dv, n_cov=n_cov, n_final=len(use), groups=int(use.gid.nunique()),
                small_groups=int(len(small)), small_rows=int(small.sum()))
    return use, ivs2, drop, miss, info


FLOW_LABELS = [
    ("csv_rows", "CSV の行数"),
    ("label", "DAS ラベルあり"),
    ("type", "article_type で絞った後(論文の表1 (b))"),
    ("notice", "取り下げ・懸念表明などの注記を除いた後(表1 (c))"),
    ("year", "出版年が --min-year 以降(表1 (d))"),
    ("mincat", "件数が --min-cat 未満の DAS 類型を除いた後(論文では除かれる類型なし)"),
    ("dv", "従属変数が使える行(WoS 被引用数なら表1 (e)、査読期間なら (g))"),
]


def sample_report(a, flow, infos):
    """件数の表(文字列のリスト)を作る。flow: 段階ごとの件数、infos: {モデル名: model_sample の件数の辞書}"""
    L = ["", "[標本の件数]  論文の表1・抄録・結論に使う件数。表1 (a)(DOI の数 701,063)は CSV にないのでここでは数えない"]
    prev = None
    for k, lab in FLOW_LABELS:
        if k in flow:
            diff = "" if prev is None else f"  (前の段階から {flow[k] - prev:+,})"
            L.append(f"  {lab:<62s}{flow[k]:>10,}{diff}")
            prev = flow[k]
    for tag, f in infos.items():
        L.append(f"  モデル [{tag}]")
        L.append(f"    従属変数が使える行 {f['n_dv']:,} → 説明変数に欠損のない行 {f['n_cov']:,} → 雑誌×年が {a.min_group} 件以上の群の行 {f['n_final']:,}"
                 f"(群 {f['groups']}、除いた群 {f['small_groups']} 個・{f['small_rows']:,} 行)")
    return L


def save_flow_csv(a, flow, infos, outdir):
    rows = [dict(kind="flow", name=k, label=lab, n=flow[k]) for k, lab in FLOW_LABELS if k in flow]
    for tag, f in infos.items():
        rows += [dict(kind="model", name=f"{tag}:{k}", label=k, n=v) for k, v in f.items()]
    pd.DataFrame(rows).to_csv(os.path.join(outdir, "sample_flow.csv"), index=False, encoding="utf-8-sig")


def parse_n_ref(text):
    out = {}
    for part in text.split(","):
        if "=" in part:
            k, v = part.split("=", 1)
            out[k.strip()] = int(v.strip().replace("_", ""))
    return out


def check_sample(a):
    """回帰を走らせずに、論文の表1・抄録・結論の件数を数えて、論文の値と照合する"""
    import copy
    ref = parse_n_ref(a.check_n_ref)
    outdir = os.path.expanduser(a.outdir)
    os.makedirs(outdir, exist_ok=True)
    runs = [
        ("wos", "WoS 被引用数のモデル", dict(dv="wos_TC")),
        ("pmc", "PMC cited-by のモデル", dict(dv="pmc_citedby_n")),
        ("rev", "査読期間のモデル", dict(dv="review_days")),
        ("pmc_on_wos", "PMC cited-by を WoS 照合のある論文に限ったモデル", dict(dv="pmc_citedby_n", pmc_on_wos_sample=True)),
        ("title_fit", "題名が合う WoS 照合に限った WoS 被引用数のモデル", dict(dv="wos_TC", require_title_fit=True)),
    ]
    excl = {c.strip() for c in a.exclude.split(",") if c.strip()}
    res, rows, stats = {}, [], {}
    for key, label, over in runs:
        print(f"[進捗] {label} の件数を数えています", file=sys.stderr, flush=True)
        b = copy.copy(a)
        for k, v in over.items():
            setattr(b, k, v)
        b.flow = {}
        d, meta, das_cols, _ref, _log = prepare(b)
        flow = dict(b.flow)
        base_ivs = [c for c in meta if c not in excl and c != "log_review" and c not in das_cols]
        use, ivs2, drop, miss, info = model_sample(d, "log_tc", das_cols + base_ivs, b)
        res[key] = (flow, info)
        for k, lab in FLOW_LABELS:
            if k in flow:
                rows.append(dict(run=key, kind="flow", name=k, label=lab, n=flow[k]))
        for k, v in info.items():
            rows.append(dict(run=key, kind="model", name=k, label=k, n=v))
        if key in ("wos", "pmc"):
            y = np.round(d.loc[use.index, "tc"].values.astype(float))
            stats[key] = (len(y), float(y.mean()), float(y.var()), int(y.max()))
        if drop:
            print(f"  [{label}] 欠損が {a.max_missing:.0%} を超えて外した説明変数: {drop}", file=sys.stderr)
    # ---- 表示
    print("\n[標本の件数]  論文の表1・抄録・結論の件数(表1 (a) の DOI 数 701,063 は CSV にないので数えない)")
    for key, label, _ in runs:
        flow, info = res[key]
        print(f"\n■ {label}")
        for k, lab in FLOW_LABELS:
            if k in flow:
                print(f"  {lab:<62s}{flow[k]:>10,}")
        print(f"  従属変数が使える行 {info['n_dv']:,} → 説明変数に欠損のない行 {info['n_cov']:,} → 雑誌×年が {a.min_group} 件以上の群の行 {info['n_final']:,}"
              f"(群 {info['groups']}、除いた群 {info['small_groups']} 個・{info['small_rows']:,} 行)")
    # ---- 論文の値との照合
    wos_f, wos_i = res["wos"]
    pmc_f, pmc_i = res["pmc"]
    rev_f, rev_i = res["rev"]
    tf_f, tf_i = res["title_fit"]
    pw_f, pw_i = res["pmc_on_wos"]
    checks = [
        ("b", "表1 (b) 研究論文で DAS ラベルあり", wos_f.get("type")),
        ("c", "表1 (c) 注記を除いた後", wos_f.get("notice")),
        ("d", "表1 (d) 2014 年以降", wos_f.get("year")),
        ("e", "表1 (e) WoS 被引用数あり", wos_f.get("dv")),
        ("f", "表1 (f) 被引用数のモデル", wos_i["n_final"]),
        ("g", "表1 (g) 受付・受理日が妥当", rev_f.get("dv")),
        ("h", "表1 (h) 査読期間のモデル", rev_i["n_final"]),
        ("pmc", "PMC cited-by のモデル(3.7節)", pmc_i["n_final"]),
        ("pmc_on_wos", "PMC を WoS 照合のある論文に限ったモデル(3.7節。WoS のモデルと同じはず)", pw_i["n_final"]),
        ("title_fit", "題名が合う照合に限ったモデル(3.6節)", tf_i["n_final"]),
        ("groups_cit", "被引用数のモデルの雑誌×年の群", wos_i["groups"]),
        ("groups_rev", "査読期間のモデルの雑誌×年の群", rev_i["groups"]),
        ("groups_pmc", "PMC のモデルの雑誌×年の群", pmc_i["groups"]),
    ]
    print("\n[論文の値との照合]  論文の値は --check-n-ref(既定は現在の原稿の値)")
    out_rows = []
    for k, lab, got in checks:
        want = ref.get(k)
        ok = "" if want is None else ("一致" if want == got else f"× 論文 {want:,} と違う(差 {got - want:+,})")
        print(f"  {lab:<62s}{got:>10,}   {ok}")
        out_rows.append(dict(run="paper_check", kind="check", name=k, label=lab, n=got, paper=want, match=(want == got) if want is not None else None))
    # ---- 3.1節の値
    print("\n[WoS 被引用数のモデルの標本の平均・分散・最大]  論文 3.1節は 19.55・2,305・8,061(分散は NB の分析対象の行と同じ母分散)")
    for key, lab in (("wos", "WoS 被引用数のモデル"), ("pmc", "PMC cited-by のモデル")):
        n, m, v, mx = stats[key]
        print(f"  {lab}: N={n:,}  平均 {m:.2f}  分散 {v:,.0f}  最大 {mx:,}")
    # ---- 結論・抄録に入れる英文
    print("\n[結論・抄録に入れる件数の英文案]  件数を確認してから使ってください")
    print(f"  ... of open-access research articles ({wos_i['n_final']:,} in the citation models and {rev_i['n_final']:,} in the peer review models).")
    print(f"  (抄録の「about 650,000 articles in the models」: 被引用数 {wos_i['n_final']:,}、査読期間 {rev_i['n_final']:,})")
    pd.DataFrame(rows + out_rows).to_csv(os.path.join(outdir, "sample_check.csv"), index=False, encoding="utf-8-sig")
    print("\n保存:", os.path.join(outdir, "sample_check.csv"))


# ----------------------------------------------------------------------------- 分析データの作成
def prepare(a):
    base = ["journal_key", "pub_year", "das_label", "das_has_label", "wos_matched", "wos_TC", "pmc_citedby_n", "cb_fetched",
            "article_type", "wos_notice_type", "wos_merged_any", "days_received_to_accepted", "has_body",
            "wos_journal_ok", "wos_title_fit", "wos_title_prefix_suspect", "corr_country_u", "corr_country_status"]
    cols = list(dict.fromkeys(base + [s[1] for s in SPEC] + ([a.dedup_key] if a.dedup_key else []) + LLM_COLS   # v021: LLM 3 種のラベルも読む
                              + ([a.field_col] if getattr(a, "field_col", "") else [])
                              + (["oa_domain", "oa_field", "oa_subfield"]   # v039: --check-extra subfield のとき(結合後の CSV にある列)
                                 if {"subfield", "all"} & {x.strip() for x in (getattr(a, "check_extra", "") or "").split(",")} else [])
                              + _oa_needed_cols(a)))
    d, miss = read_cols(a.csv, cols)
    log = []
    log.append(f"読み込み {len(d):,} 行 / 見つからない列: {miss if miss else 'なし'}")
    _flow(a, "csv_rows", len(d))
    if a.journal:
        d = d[d.journal_key.str.contains(a.journal, case=False, regex=False)]
        log.append(f"--journal '{a.journal}' で {len(d):,} 行")
    src_ = getattr(a, "das_source", "ensemble")
    if src_ != "ensemble":
        col_ = {"ds32": "das_ds32", "gpt5": "das_gpt5", "mil3": "das_mil3"}[src_]
        if col_ not in d:
            sys.exit(f"--das-source {src_}: 列 {col_} が CSV にありません")
        d["das_label"] = d[col_]
        log.append(f"--das-source {src_}: DAS ラベルにアンサンブルではなく {col_} を使う")
    d = d[(d.get("das_has_label", "1") == "1") & (d.das_label != "")]
    log.append(f"DAS ラベルあり {len(d):,} 行")
    if getattr(a, "das_agree_only", False):
        if all(c in d for c in LLM_COLS):
            same = (d[LLM_COLS[0]] == d[LLM_COLS[1]]) & (d[LLM_COLS[0]] == d[LLM_COLS[2]]) & (d[LLM_COLS[0]] != "")
            log.append(f"--das-agree-only: 3 つの LLM が一致しない {int((~same).sum()):,} 行を除く(一致 {same.mean():.1%})")
            d = d[same]
        else:
            sys.exit("--das-agree-only: LLM のラベル列(das_ds32, das_gpt5, das_mil3)が CSV にありません")
    _flow(a, "label", len(d))
    if "article_type" in d and a.article_type:
        d = d[d.article_type == a.article_type]
        log.append(f"article_type={a.article_type} {len(d):,} 行")
    _flow(a, "type", len(d))
    if "wos_notice_type" in d and not a.keep_notice:
        k = int((d.wos_notice_type != "").sum())
        d = d[d.wos_notice_type == ""]
        log.append(f"取り下げ・懸念表明などの注記あり {k:,} 行を除外")
    _flow(a, "notice", len(d))
    if a.drop_merged and "wos_merged_any" in d:
        k = int((d.wos_merged_any == "1").sum())
        d = d[d.wos_merged_any != "1"]
        log.append(f"WoS のレコードが合体した行 {k:,} 行を除外")
    d = d.copy()
    d["year"] = num(d.pub_year)
    d = d[d.year >= a.min_year]
    log.append(f"出版年 {a.min_year} 年以降 {len(d):,} 行")
    _flow(a, "year", len(d))
    # 従属変数
    if a.dv == "review_days":
        # 査読期間(受付→受理の日数、整数)を被引用数と同じ枠組み(列 tc)で扱う。WoS・PMC の照合条件は使わない
        dd_ = num(d["days_received_to_accepted"]) if "days_received_to_accepted" in d else pd.Series(np.nan, index=d.index)
        d["tc"] = dd_.where((dd_ >= 0) & (dd_ <= a.max_review_days))
        log.append(f"--dv review_days: 従属変数は査読期間(受付→受理の日数、0〜{a.max_review_days} 日)。使える行 {int(d.tc.notna().sum()):,}")
    elif _oa_dv(a.dv):
        d["tc"], _end = oa_dv_series(d, a, a.dv, log)   # v042: OpenAlex の年次被引用数の窓
        if _end is not None:
            d["oa_win_end"] = _end
    else:
        d["tc"] = num(d["wos_TC"]) if a.dv == "wos_TC" else num(d["pmc_citedby_n"])
    if a.dv == "wos_TC" and "wos_matched" in d:
        d.loc[d.wos_matched.str.lower() != "true", "tc"] = np.nan
    if a.dv == "pmc_citedby_n" and "cb_fetched" in d:
        d.loc[d.cb_fetched != "1", "tc"] = np.nan
    if a.dv == "pmc_citedby_n" and a.pmc_on_wos_sample and "wos_matched" in d:
        k = int((d.tc.notna() & (d.wos_matched.str.lower() != "true")).sum())
        d.loc[d.wos_matched.str.lower() != "true", "tc"] = np.nan
        log.append(f"--pmc-on-wos-sample: WoS 照合のない {k:,} 行の PMC cited-by を欠損にする(WoS のモデルと同じ論文集合)")
    d.loc[d.tc < 0, "tc"] = np.nan
    if a.dv == "wos_TC":
        m = d.wos_matched.str.lower() == "true" if "wos_matched" in d else pd.Series(True, index=d.index)
        if "wos_title_fit" in d:
            log.append("WoS 照合の題名の近さ(wos_title_fit、照合できた行): " + str(d.loc[m, "wos_title_fit"].replace("", "(空)").value_counts().to_dict()))
        if "wos_journal_ok" in d:
            log.append("wos_journal_ok(照合できた行): " + str(d.loc[m, "wos_journal_ok"].replace("", "(空)").value_counts().to_dict()))
        if a.require_journal_ok and "wos_journal_ok" in d:
            bad = m & (d.wos_journal_ok != "1")
            d.loc[bad, "tc"] = np.nan
            log.append(f"--require-journal-ok: 雑誌が合わない照合 {int(bad.sum()):,} 行の被引用数を欠損にする")
        if a.require_title_fit:
            bad = m & (d.wos_title_fit != FIT_OK)
            if "wos_title_prefix_suspect" in d:
                bad = bad | (m & (d.wos_title_prefix_suspect == "1"))
            d.loc[bad, "tc"] = np.nan
            log.append(f"--require-title-fit: 題名が近くない照合 {int(bad.sum()):,} 行の被引用数を欠損にする")
    d["log_tc"] = np.log1p(d.tc)
    _flow(a, "dv", int(d.tc.notna().sum()))
    days = num(d["days_received_to_accepted"]) if "days_received_to_accepted" in d else pd.Series(np.nan, index=d.index)
    days = days.where((days >= 0) & (days <= a.max_review_days))
    d["log_review"] = np.log1p(days)
    log.append("査読期間(受付→受理)が使える行 / 雑誌別: " + str(days.notna().groupby(jshort(d.journal_key)).sum().astype(int).to_dict()))
    # 説明変数
    meta = {}
    for new, src, tr, grp, desc in SPEC:
        if src not in d:
            log.append(f"[警告] 列 {src} がないので {new} を使いません")
            continue
        x = num(d[src])
        if new in BODY_DERIVED and "has_body" in d:
            x = x.where(d.has_body != "0")
        if tr == "log1p":
            x = np.log1p(x.clip(lower=0))
        elif tr == "bin":
            x = (x > 0).astype(float).where(x.notna())
        d[new] = x
        meta[new] = dict(group=grp, desc=desc, kind="cont" if tr in ("log1p", "raw") else "bin", src=src, tr=tr)
    # DAS ダミー
    vc = d.das_label.value_counts()
    keep_cat = [c for c in vc.index if vc[c] >= a.min_cat]
    dropped = {c: int(vc[c]) for c in vc.index if c not in keep_cat}
    if dropped:
        log.append(f"件数が {a.min_cat} 未満の類型は除外: {dropped}")
    d = d[d.das_label.isin(keep_cat)]
    _flow(a, "mincat", len(d))
    _flow(a, "dv", int(d.tc.notna().sum()))   # 類型の絞り込みの後の値で上書き(表1 (e)(g) はこの値)
    ref = a.das_ref if a.das_ref in keep_cat else keep_cat[0]
    das_cols = []
    for c in keep_cat:
        if c == ref:
            continue
        name = f"das_{c}"
        d[name] = (d.das_label == c).astype(float)
        meta[name] = dict(group=G_DAS, desc=f"DAS={c} ({DAS_NAMES.get(c, '定義はこのスクリプトでは未設定')}) / 基準 {ref}", kind="bin", src="das_label", tr="dummy")
        das_cols.append(name)
    if a.corr_top > 0 and "corr_country_u" in d:
        cc = d["corr_country_u"].replace("", np.nan)
        vc2 = cc.value_counts()
        top = [c for c in vc2.index[:a.corr_top] if vc2[c] >= a.min_cat]
        if top and int((cc.notna() & ~cc.isin(top)).sum()) < a.min_cat:
            top = top[:-1]   # 「その他の国」が足りないと完全な共線性になるので、最小の国を基準側に回す
        log.append(f"責任著者の国(corr_country_u): 欠損 {cc.isna().mean():.1%} / ダミーにした国 {top} / それ以外の国が基準")
        if "corr_country_status" in d:
            log.append("corr_country_status: " + str(d.corr_country_status.replace("", "(空)").value_counts().to_dict()))
        for c in top:
            name = "corr_" + re.sub(r"\W+", "_", c).strip("_")
            d[name] = (cc == c).astype(float).where(cc.notna())
            meta[name] = dict(group=G_CORR, desc=f"責任著者の国={c} / 基準 その他の国", kind="bin", src="corr_country_u", tr="dummy")
    if getattr(a, "field_col", "") and a.field_col in d:
        # v021: 分野の代理(CSV の列。複数値は ; | の先頭を使う(カンマは分野名に含まれるので切らない))の上位 --field-top 個をダミーにする。残りと欠損は基準側
        fv = d[a.field_col].astype(str).str.split(r"[;|]", regex=True).str[0].str.strip().replace({"": np.nan, "nan": np.nan})
        vcf = fv.value_counts()
        topf = [c for c in vcf.index[:a.field_top] if vcf[c] >= a.min_cat]
        if topf and int((fv.isna() | ~fv.isin(topf)).sum()) < a.min_cat:
            topf = topf[:-1]   # 基準側が足りないと完全な共線性になるので、最小の水準を基準側に回す
        log.append(f"分野の列 {a.field_col}: 欠損 {fv.isna().mean():.1%} / 水準 {len(vcf)} / ダミーにした水準 {len(topf)}(上位 {a.field_top}、{a.min_cat} 件以上)/ それ以外と欠損が基準")
        for c in topf:
            name = "field_" + re.sub(r"\W+", "_", c).strip("_")[:40]
            if name in d:
                name += "_" + str(len(meta))
            d[name] = (fv == c).astype(float)
            meta[name] = dict(group="分野", desc=f"分野 {a.field_col}={c} / 基準 その他", kind="bin", src=a.field_col, tr="dummy")
    elif getattr(a, "field_col", ""):
        log.append(f"[警告] --field-col {a.field_col} の列が CSV にないので分野を使いません(--find-cols で探せます)")
    if _need_oa(a) and getattr(a, "oa_field", "field") != "none":
        # v042: OpenAlex の分野(field 26 / domain 4 / subfield 上位 N)のダミー。残りと欠損が基準側
        m_ = re.fullmatch(r"(field|domain|sub(\d*))", a.oa_field)
        if not m_:
            sys.exit(f"--oa-field の指定が不明です: {a.oa_field}(none, field, domain, sub<個数>)")
        col_, top_, pre_ = (("oa_field", 999, "oaf_") if a.oa_field == "field" else (("oa_domain", 999, "oad_") if a.oa_field == "domain"
                            else ("oa_subfield", int(m_.group(2) or 50), "oas_")))
        if col_ in d:
            _nm, _inf = _topic_dummies(d, meta, col_, top_, a.min_cat, pre_)
            log.append(f"[分野] OpenAlex {col_}: 水準 {_inf['levels']} / ダミー {_inf['dummies']} / 欠損 {_inf['missing']:.1%} / 基準側 {_inf['baseline_share']:.1%}")
        else:
            log.append(f"[警告] 列 {col_} が CSV にないので OpenAlex の分野を使いません(--oa-field none で消せます)")
    meta["log_review"] = dict(group=G_REVIEW, desc="査読期間 log(1+受付→受理の日数)", kind="cont", src="days_received_to_accepted", tr="log1p")
    d["gid"] = d.journal_key + "|" + d.pub_year
    return d, meta, das_cols, ref, log


# ----------------------------------------------------------------------------- 推定
def demean(arr, codes, counts):
    out = np.empty_like(arr, dtype=float)
    for j in range(arr.shape[1]):
        m = np.bincount(codes, weights=arr[:, j]) / counts
        out[:, j] = arr[:, j] - m[codes]
    return out


def r2_of(idx, XtX, Xty, yy):
    if len(idx) == 0:
        return 0.0
    ix = np.asarray(sorted(idx))
    A, b = XtX[np.ix_(ix, ix)], Xty[ix]
    try:
        beta = np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        beta = np.linalg.lstsq(A, b, rcond=None)[0]
    return float(b @ beta) / yy


def shapley_exact(players, value):
    n = len(players)
    phi = {p: 0.0 for p in players}
    fact = [math.factorial(i) for i in range(n + 1)]
    cache = {}

    def v(s):
        s = frozenset(s)
        if s not in cache:
            cache[s] = value(s)
        return cache[s]
    for p in players:
        others = [q for q in players if q != p]
        for r in range(n):
            for s in itertools.combinations(others, r):
                w = fact[r] * fact[n - r - 1] / fact[n]
                phi[p] += w * (v(set(s) | {p}) - v(set(s)))
    return phi


def shapley_perm(players, value, n_perm, seed):
    rng = np.random.default_rng(seed)
    phi = {p: 0.0 for p in players}
    for _ in range(n_perm):
        order = list(rng.permutation(len(players)))
        cur, prev = set(), 0.0
        for i in order:
            cur.add(players[i])
            val = value(cur)
            phi[players[i]] += val - prev
            prev = val
    return {p: phi[p] / n_perm for p in players}


def run_model(d, dv, ivs, meta, das_cols, args, tag, outdir, lines):
    """d: 前処理済み。dv: 従属変数の列名。ivs: 使う説明変数の列名(DAS ダミーを含む)"""
    P = lines.append
    P(f"\n{'=' * 78}\n[{tag}]  従属変数 {dv}\n{'=' * 78}")
    use, ivs, drop, miss, info = model_sample(d, dv, ivs, args)   # 査読期間は指定されたら外さず、行を絞る
    if drop:
        P(f"欠損が {args.max_missing:.0%} を超える説明変数を外す: " + ", ".join(f"{c}({miss[c]:.0%})" for c in drop))
    N = len(use)
    P(f"分析対象 {N:,} 行 / 雑誌×年 {use.gid.nunique():,} グループ / 説明変数 {len(ivs)} 個")
    P(f"  件数の内訳: 従属変数が使える行 {info['n_dv']:,} → 説明変数に欠損のない行 {info['n_cov']:,} → 雑誌×年が {args.min_group} 件以上の群の行 {info['n_final']:,}"
      f"(除いた群 {info['small_groups']} 個・{info['small_rows']:,} 行)")
    mi = getattr(args, "model_info", None)
    if mi is not None:
        mi[tag] = info
    if N < 1000:
        P("行数が少なすぎるので中止します")
        return
    codes, uniq = pd.factorize(use.gid)
    counts = np.bincount(codes).astype(float)
    G = len(uniq)
    Xraw = use[ivs].values.astype(float)
    yraw = use[dv].values.astype(float)
    X = demean(Xraw, codes, counts)
    y = demean(yraw[:, None], codes, counts)[:, 0]
    sd = X.std(axis=0)
    zero = [ivs[j] for j in range(len(ivs)) if sd[j] < 1e-9]
    if zero:
        P("雑誌×年の中でばらつきがない説明変数を外す: " + ", ".join(zero))
        keep = [j for j in range(len(ivs)) if sd[j] >= 1e-9]
        ivs = [ivs[j] for j in keep]
        X, sd = X[:, keep], sd[keep]
    k = len(ivs)
    scale = np.ones(k)
    for j, c in enumerate(ivs):
        if meta[c]["kind"] == "cont":
            scale[j] = sd[j]
    X = X / scale
    XtX, Xty = X.T @ X, X.T @ y
    yy = float(y @ y)
    sst_tot = float(((yraw - yraw.mean()) ** 2).sum())
    beta = np.linalg.solve(XtX, Xty)
    e = y - X @ beta
    ssr = float(e @ e)
    bread = np.linalg.inv(XtX)
    Xe = X * e[:, None]
    meat = Xe.T @ Xe                      # X' diag(e^2) X
    V = bread @ meat @ bread * N / (N - k - G)
    se = np.sqrt(np.diag(V))
    S = np.empty((G, k))                  # 雑誌×年でクラスタした頑健分散(同じ雑誌×年の論文どうしの相関を考慮)
    for j in range(k):
        S[:, j] = np.bincount(codes, weights=Xe[:, j], minlength=G)
    V_cl = bread @ (S.T @ S) @ bread * (G / max(G - 1, 1)) * ((N - 1) / max(N - k, 1))
    se_cl = np.sqrt(np.diag(V_cl))
    if G < 30:
        P(f"[注意] クラスタ(雑誌×年)が {G} しかなく、クラスタ頑健な標準誤差は小さめに出ます")
    R = np.corrcoef(X, rowvar=False)
    vif = np.diag(np.linalg.inv(R)) if k > 1 else np.ones(1)
    r2_fe = 1 - yy / sst_tot
    r2_within = 1 - ssr / yy
    r2_full = 1 - ssr / sst_tot
    P(f"R²: 雑誌×年だけ {r2_fe:.3f} / 雑誌×年を除いた後(within) {r2_within:.3f} / 全体 {r2_full:.3f}")

    t = beta / se
    pval = np.array([math.erfc(abs(x) / math.sqrt(2)) for x in t])
    pcl = np.array([math.erfc(abs(x) / math.sqrt(2)) for x in beta / se_cl])
    coef = pd.DataFrame({
        "variable": ivs, "group": [meta[c]["group"] for c in ivs], "description": [meta[c]["desc"] for c in ivs],
        "scale": ["0→1" if meta[c]["kind"] == "bin" else "1 SD(雑誌×年内)" for c in ivs],
        "coef": beta, "se": se, "t": t, "p": pval, "ci_low": beta - 1.96 * se, "ci_high": beta + 1.96 * se,
        "pct_effect": (np.exp(beta) - 1) * 100, "pct_low": (np.exp(beta - 1.96 * se) - 1) * 100,
        "pct_high": (np.exp(beta + 1.96 * se) - 1) * 100, "vif": vif,
        "se_cluster": se_cl, "p_cluster": pcl})
    coef["p_holm_all"] = holm(coef.p_cluster.values)          # クラスタ頑健 p を、全係数を 1 つの族として Holm 補正
    coef["p_holm_das"] = np.nan                                # DAS の比較(類型の数)だけを族とした Holm 補正
    dm = (coef.group == G_DAS).values
    if dm.any():
        coef.loc[dm, "p_holm_das"] = holm(coef.loc[dm, "p_cluster"].values)
    coef.to_csv(os.path.join(outdir, f"coef_{tag}.csv"), index=False, encoding="utf-8-sig")
    P("\n[係数] 従属変数は log なので pct_effect が %効果。連続量は 1SD 増えたとき、0/1 は 0→1 のとき。p は HC1、p_cluster は雑誌×年クラスタ頑健、p_holm_das は DAS の比較だけを族とした Holm 補正(クラスタ頑健 p に対して)")
    show = coef.assign(sig=np.where(coef.p < 0.001, "***", np.where(coef.p < 0.01, "**", np.where(coef.p < 0.05, "*", ""))))
    P(show[["variable", "group", "scale", "coef", "se", "p", "p_cluster", "p_holm_das", "pct_effect", "pct_low", "pct_high", "vif", "sig"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4g}"))
    big = coef[coef.vif > 5]
    if len(big):
        P("\n[注意] VIF が 5 を超える変数: " + ", ".join(f"{r.variable}({r.vif:.1f})" for r in big.itertuples()))

    # ---- 同時検定(Wald): 「そのグループの係数がすべて 0」
    wrows = []
    gidx = {}
    for j, c in enumerate(ivs):
        gidx.setdefault(meta[c]["group"], []).append(j)
    for g, idx in gidx.items():
        b, Vg = beta[idx], V[np.ix_(idx, idx)]
        try:
            w = float(b @ np.linalg.solve(Vg, b))
        except np.linalg.LinAlgError:
            w = float("nan")
        try:
            wc = float(b @ np.linalg.solve(V_cl[np.ix_(idx, idx)], b))
        except np.linalg.LinAlgError:
            wc = float("nan")
        wrows.append({"group": g, "df": len(idx), "wald_chi2": w, "p": chi2_sf(w, len(idx)) if w == w else float("nan"),
                      "wald_chi2_cluster": wc, "p_cluster": chi2_sf(wc, len(idx)) if wc == wc else float("nan")})
    wt = pd.DataFrame(wrows)
    wt.to_csv(os.path.join(outdir, f"wald_{tag}.csv"), index=False, encoding="utf-8-sig")
    P("\n[同時検定(Wald)] 帰無仮説: そのグループの係数がすべて 0。p は HC1、p_cluster は雑誌×年クラスタ頑健。DAS の行が「DAS 全体」の検定(論文の LRT に相当)")
    P(wt.to_string(index=False, float_format=lambda x: f"{x:.4g}"))

    # ---- グループ別 Shapley
    gcols = {}
    for j, c in enumerate(ivs):
        gcols.setdefault(meta[c]["group"], []).append(j)
    gnames = list(gcols)

    def val_g(s):
        idx = [j for g in s for j in gcols[g]]
        return r2_of(idx, XtX, Xty, yy)
    phi = shapley_exact(gnames, val_g) if len(gnames) <= 12 else shapley_perm(gnames, val_g, 500, args.seed)
    full = val_g(set(gnames))
    rows = []
    for g in gnames:
        uniq_r2 = full - val_g(set(gnames) - {g})
        rows.append({"group": g, "n_vars": len(gcols[g]), "shapley_r2": phi[g], "share_of_within_r2": phi[g] / full if full > 0 else np.nan,
                     "unique_delta_r2": uniq_r2, "r2_of_total_variance": phi[g] * (1 - r2_fe)})
    gt = pd.DataFrame(rows).sort_values("shapley_r2", ascending=False)
    gt.to_csv(os.path.join(outdir, f"shapley_group_{tag}.csv"), index=False, encoding="utf-8-sig")
    P(f"\n[グループ別の寄与] within R² = {full:.4f} を Shapley で配分(全体の分散に対する寄与は r2_of_total_variance)")
    P(gt.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- 因子別 Shapley(DAS のダミーは 1 つの因子にまとめる)
    factors = {}
    for j, c in enumerate(ivs):
        key = "DAS(類型)" if meta[c]["group"] == G_DAS else ("責任著者の国" if meta[c]["group"] == G_CORR else c)
        factors.setdefault(key, []).append(j)
    fnames = list(factors)

    def val_f(s):
        return r2_of([j for f in s for j in factors[f]], XtX, Xty, yy)
    if len(fnames) <= 10:
        phif, how = shapley_exact(fnames, val_f), "厳密"
    else:
        phif, how = shapley_perm(fnames, val_f, args.n_perm, args.seed), f"並べ替え {args.n_perm} 回の近似"
    ft = pd.DataFrame([{"factor": f, "group": meta[ivs[factors[f][0]]]["group"], "shapley_r2": phif[f],
                        "share_of_within_r2": phif[f] / full if full > 0 else np.nan} for f in fnames]).sort_values("shapley_r2", ascending=False)
    ft.to_csv(os.path.join(outdir, f"shapley_factor_{tag}.csv"), index=False, encoding="utf-8-sig")
    P(f"\n[因子別の寄与] ({how})  合計 {ft.shapley_r2.sum():.4f}")
    P(ft.head(25).to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- 参考: DAS 類型ごとの記述
    if das_cols:
        P("\n[参考] 分析に残った行での DAS 類型の件数と、雑誌×年を除いた従属変数の平均(基準との差)")
        tmp = d.loc[use.index, ["das_label", dv, "gid"]].copy()
        tmp["dv_dm"] = tmp[dv] - tmp.groupby("gid")[dv].transform("mean")
        P(tmp.groupby("das_label").agg(n=("dv_dm", "size"), mean_dm=("dv_dm", "mean")).round(4).to_string())


# ----------------------------------------------------------------------------- 負の二項回帰(NB2)を numpy だけで推定する
def _gammaln(x):
    x = np.asarray(x, dtype=float)
    try:
        from scipy.special import gammaln
        return gammaln(x)
    except Exception:
        return np.array([math.lgamma(v) for v in x.ravel()]).reshape(x.shape)


class NBData:
    """y が整数の計数であることを使い、lgamma を y の種類ごとに 1 回だけ計算して対数尤度を速くする"""
    def __init__(self, y):
        self.y = np.asarray(y, dtype=float)
        self.yu, self.inv = np.unique(self.y, return_inverse=True)
        self.lgy1 = _gammaln(self.y + 1.0)

    def llf(self, mu, alpha):
        r = 1.0 / alpha
        lg = _gammaln(self.yu + r)[self.inv] - _gammaln(np.array([r]))[0] - self.lgy1
        lr = np.log(r + mu)
        return float(np.sum(lg + r * (math.log(r) - lr) + self.y * (np.log(mu) - lr)))


def _golden_max(f, lo, hi, n=32):
    g = (math.sqrt(5) - 1) / 2
    c, d = hi - g * (hi - lo), lo + g * (hi - lo)
    fc, fd = f(c), f(d)
    for _ in range(n):
        if fc > fd:
            hi, d, fd = d, c, fc
            c = hi - g * (hi - lo)
            fc = f(c)
        else:
            lo, c, fc = c, d, fd
            d = lo + g * (hi - lo)
            fd = f(d)
    return (c + 1e-12 if fc > fd else d)


def nb_fit(X, nbd, b0=None, a0=None, maxit=100, tol=1e-9, offset=None):
    """NB2(対数リンク、分散 = mu + alpha*mu²)の最尤推定。beta は IRLS(半歩戻し付き)、alpha は 1 次元探索で交互に更新する。
    返り値: dict(beta, alpha, llf, A=X'WX(期待情報), mu, converged, iters)"""
    y = nbd.y
    n, p = X.shape
    off = np.zeros(n) if offset is None else np.asarray(offset, dtype=float)   # v020: 露出時間のオフセット(log 経過年数)
    if b0 is None:
        mu0 = (y + y.mean()) / 2.0
        b = np.linalg.lstsq(X, np.log(mu0) - off, rcond=None)[0]
    else:
        b = np.array(b0, dtype=float)
    alpha = float(a0) if a0 else 0.5
    eta = np.clip(X @ b + off, -30, 30)
    mu = np.exp(eta)
    ll = nbd.llf(mu, alpha)
    conv, it = False, 0
    for it in range(1, maxit + 1):
        w = mu / (1.0 + alpha * mu)
        z = eta - off + (y - mu) / mu
        A = (X * w[:, None]).T @ X
        rhs = X.T @ (w * z)
        try:
            bn = np.linalg.solve(A, rhs)
        except np.linalg.LinAlgError:
            bn = np.linalg.lstsq(A, rhs, rcond=None)[0]
        ok = False
        for h in range(12):
            bt = b + (bn - b) / 2 ** h
            et = np.clip(X @ bt + off, -30, 30)
            mt = np.exp(et)
            lt = nbd.llf(mt, alpha)
            if lt >= ll - 1e-9:
                b, eta, mu, ok = bt, et, mt, True
                break
        la = math.log(alpha)
        la = _golden_max(lambda t: nbd.llf(mu, math.exp(t)), max(-11.0, la - 2.5), min(5.0, la + 2.5))
        alpha = math.exp(la)
        ll_new = nbd.llf(mu, alpha)
        if abs(ll_new - ll) < tol * (1.0 + abs(ll_new)) and ok:
            ll, conv = ll_new, True
            break
        ll = ll_new
    w = mu / (1.0 + alpha * mu)
    A = (X * w[:, None]).T @ X
    return dict(beta=b, alpha=alpha, llf=ll, A=A, mu=mu, converged=conv, iters=it)


def nb_cov(fit, X, y, codes=None):
    """モデルに基づく分散(A⁻¹)と、codes(雑誌×年など)でクラスタした頑健分散(サンドイッチ)を返す"""
    try:
        Ainv = np.linalg.inv(fit["A"])
    except np.linalg.LinAlgError:
        Ainv = np.linalg.pinv(fit["A"])
    out = {"model": Ainv}
    if codes is not None:
        mu, alpha = fit["mu"], fit["alpha"]
        s = X * ((y - mu) / (1.0 + alpha * mu))[:, None]
        G = int(codes.max()) + 1
        S = np.empty((G, X.shape[1]))
        for j in range(X.shape[1]):
            S[:, j] = np.bincount(codes, weights=s[:, j], minlength=G)
        n, p = X.shape
        out["cluster"] = Ainv @ (S.T @ S) @ Ainv * (G / max(G - 1, 1)) * ((n - 1) / max(n - p, 1))
    return out


def holm(p):
    p = np.asarray(p, dtype=float)
    adj = np.full(p.shape, np.nan)
    valid = np.where(np.isfinite(p))[0]
    order = valid[np.argsort(p[valid])]
    run, m = 0.0, len(valid)
    for rank, i in enumerate(order):
        run = max(run, (m - rank) * p[i])
        adj[i] = min(1.0, run)
    return adj


def norm_p(t):
    return np.array([math.erfc(abs(x) / math.sqrt(2)) if x == x else np.nan for x in np.atleast_1d(t)])



# ----------------------------------------------------------------------------- NB 回帰(論文の Table 4・LRT・交互作用・雑誌別に対応する部分)
def nb_build(d, meta, das_cols, base_ivs, a, log):
    """被引用数(整数)の NB 回帰用の設計行列を作る。FE は雑誌+出版年のダミー(論文と同じ。--nb-fe jy で雑誌×年)。
    連続量は全体の 1SD で標準化(係数は 1SD あたりの対数率比)、0/1 は 0→1。全モデルで同じ行の集合を使う。"""
    ivs = list(das_cols) + list(base_ivs) + (["log_review"] if a.review_as_iv else [])
    extra = ["age_years"] if (getattr(a, "exposure", "off") == "offset" and "age_years" in d) else []   # v020
    use = d.loc[d.tc.notna() & d.year.notna(), ["gid", "journal_key", "year", "tc"] + extra + ivs].copy()
    miss = use[ivs].isna().mean()
    drop = [c for c in ivs if miss[c] > a.max_missing and c != "log_review"]
    if drop:
        log.append("[NB] 欠損が %.0f%% を超える説明変数を外す: " % (a.max_missing * 100) + ", ".join(f"{c}({miss[c]:.0%})" for c in drop))
    ivs = [c for c in ivs if c not in drop]
    use = use.dropna(subset=ivs + extra)
    cnt = use.gid.value_counts()
    use = use[use.gid.isin(cnt[cnt >= a.min_group].index)]
    if a.nb_sample and len(use) > a.nb_sample:
        use = use.sample(a.nb_sample, random_state=a.seed)
        log.append(f"[NB] --nb-sample により {a.nb_sample:,} 行を無作為抽出")
    sd0 = use[ivs].std()
    zero = [c for c in ivs if not sd0[c] > 1e-9]
    if zero:
        log.append("[NB] ばらつきがない説明変数を外す: " + ", ".join(zero))
        ivs = [c for c in ivs if c not in zero]
    sds = {c: float(use[c].std()) for c in ivs if meta[c]["kind"] == "cont"}   # 標準化に使う SD(弾力性の計算用に保存)
    for c in ivs:
        if meta[c]["kind"] == "cont":
            use[c] = (use[c] - use[c].mean()) / use[c].std()
    y = np.round(use.tc.values.astype(float))
    jc, jl = pd.factorize(use.journal_key, sort=True)
    yc, yl = pd.factorize(use.year, sort=True)
    gc, gl = pd.factorize(use.gid)
    names, cols, blocks = ["(切片)"], [np.ones(len(use))], {}

    def add(nm, v, blk):
        names.append(nm)
        cols.append(np.asarray(v, dtype=float))
        blocks.setdefault(blk, []).append(len(names) - 1)
    if a.nb_fe == "jy":
        for k in range(1, len(gl)):
            add(f"fe_gid:{gl[k]}", gc == k, "雑誌×年")
    else:
        for k in range(1, len(jl)):
            add(f"fe_journal:{jl[k]}", jc == k, "雑誌")
        for k in range(1, len(yl)):
            add(f"fe_year:{int(yl[k])}", yc == k, "出版年")
    for c in ivs:
        g = meta[c]["group"]
        blk = "DAS(類型)" if g == G_DAS else ("責任著者の国" if g == G_CORR else (c if a.nb_lrt == "variable" else g))
        add(c, use[c].values, blk)
    X = np.column_stack(cols)
    log.append(f"[NB] 分析対象 {len(use):,} 行 / 雑誌 {len(jl)} / 出版年 {len(yl)} / 列数 {X.shape[1]} / FE={a.nb_fe} / {'査読期間(日)' if getattr(a, 'dv', '') == 'review_days' else '被引用数'}の平均 {y.mean():.2f}, 分散 {y.var():.1f}, 最大 {int(y.max())} / {'標本抽出あり(--nb-sample %d)' % a.nb_sample if (a.nb_sample and len(use) <= a.nb_sample) else '全行で推定(標本抽出なし)'}")
    off = np.log(use.age_years.values.astype(float)) if extra else None
    return dict(use=use, ivs=ivs, names=names, X=X, y=y, nbd=NBData(y), offset=off, blocks=blocks, gcodes=gc, jcodes=jc, jlabels=list(jl),
                year=use.year.values, das_cols=[c for c in das_cols if c in ivs], meta=meta, sds=sds)


def _irr_table(fit, cov, names, idx, meta):
    b = fit["beta"][idx]
    def _se(V):   # v026: 先に idx で絞ってから sqrt(DAS 以外の列の分散が負でも警告しない)。負の分散は NaN にする
        v = np.asarray(np.diag(V), dtype=float)[idx]
        v = np.where(v >= 0, v, np.nan)
        return np.sqrt(v)
    se_m = _se(cov["model"])
    se_c = _se(cov["cluster"])
    t = pd.DataFrame({"variable": [names[i] for i in idx], "coef": b, "se_model": se_m, "p_model": norm_p(b / se_m),
                      "se_cluster": se_c, "p_cluster": norm_p(b / se_c),
                      "irr": np.exp(b), "irr_low": np.exp(b - 1.96 * se_c), "irr_high": np.exp(b + 1.96 * se_c),
                      "irr_low_model": np.exp(b - 1.96 * se_m), "irr_high_model": np.exp(b + 1.96 * se_m)})
    t["scale"] = [("0→1" if meta[v]["kind"] == "bin" else "1 SD") if v in meta else "" for v in t.variable]
    t["group"] = [meta[v]["group"] if v in meta else "固定効果" for v in t.variable]
    return t


def _wald(beta, V, idx):
    b = beta[idx]
    try:
        Vg = V[np.ix_(idx, idx)]
        if np.linalg.cond(Vg) > 1e10:       # 分散行列が特異に近いと χ² が桁違いに大きくなるので、検定しない
            return float("nan"), float("nan")
        w = float(b @ np.linalg.solve(Vg, b))
    except np.linalg.LinAlgError:
        return float("nan"), float("nan")
    return w, chi2_sf(w, len(idx))


def nb_lrt(ctx, full, a, P):
    """ブロックを 1 つずつ外して再推定し、LR = 2(LL_full − LL_reduced) を出す(論文の LRT 重要度表に対応)"""
    X, nbd, names = ctx["X"], ctx["nbd"], ctx["names"]
    rows = []
    for blk, idx in ctx["blocks"].items():
        keep = [i for i in range(X.shape[1]) if i not in set(idx)]
        fr = nb_fit(X[:, keep], nbd, b0=full["beta"][keep], a0=full["alpha"], offset=ctx.get("offset"))
        lr = 2 * (full["llf"] - fr["llf"])
        print(f"[進捗] LRT {len(rows) + 1}/{len(ctx['blocks'])}: {blk}", file=sys.stderr, flush=True)
        rows.append({"block": blk, "df": len(idx), "LR_chi2": lr, "p": chi2_sf(lr, len(idx)) if lr >= -1e-6 else float("nan"),
                     "LR_per_df": lr / len(idx), "llf_full": full["llf"], "llf_reduced": fr["llf"], "reliable": bool(lr >= -1e-6 and fr["converged"])})
        if not rows[-1]["reliable"]:
            P(f"  [注意] LRT {blk}: 収束または LR の非負性に問題があります(LR={lr:.2f})。この行は参考値です")
    return pd.DataFrame(rows).sort_values("LR_chi2", ascending=False).reset_index(drop=True)


def interaction_df_info(ctx, a, extra_cols, extra_names):
    """交互作用の列のうち件数が --min-inter 以上の列を残し、主効果モデルと交互作用ありモデルの階数から df を求める(NB は推定しない)。
    階数は X'X と X1'X1 の行列の階数(X1 = [X, E])。X1'X1 のブロックから作るので、大きな X1 を作らずに済む"""
    X = ctx["X"]
    sums = extra_cols.sum(axis=0)
    keep_j = [j for j in range(len(extra_names)) if sums[j] >= a.min_inter]
    dropped = [(extra_names[j], int(sums[j])) for j in range(len(extra_names)) if j not in set(keep_j)]
    XtX = X.T @ X
    r0 = int(np.linalg.matrix_rank(XtX))
    if keep_j:
        E = extra_cols[:, keep_j]
        XtE = X.T @ E
        G1 = np.block([[XtX, XtE], [XtE.T, E.T @ E]])
        r1 = int(np.linalg.matrix_rank(G1))
    else:
        r1 = r0
    return dict(keep_j=keep_j, dropped=dropped, n_cols=len(extra_names), n_kept=len(keep_j), rank_main=r0, rank_inter=r1, df=r1 - r0)


def interaction_df_lines(info, a, max_df=None, note=""):
    """df の内訳の説明文(文字列のリスト)"""
    L = [f"    自由度の内訳: 交互作用の列 {info['n_cols']} 個 → 件数が --min-inter({a.min_inter}) 未満の {len(info['dropped'])} 個を除く → 残り {info['n_kept']} 個 / 階数 {info['rank_main']} → {info['rank_inter']} で df = {info['df']}"]
    if max_df is not None:
        L.append(f"    理論上の最大 df = {max_df}{note}。実際の df = {info['df']}(差 {max_df - info['df']})")
    if info["df"] != info["n_kept"]:
        L.append(f"    [注意] 残した列の数 {info['n_kept']} と df {info['df']} が違います(差 {info['n_kept'] - info['df']} 列は他の列と一次従属)")
    if info["dropped"]:
        L.append("    除いた列: " + ", ".join(f"{n}(n={c})" for n, c in info["dropped"]))
    return L


def nb_interaction(ctx, full, a, P, label, extra_cols, extra_names, max_df=None, note=""):
    """主効果モデルに交互作用の列を足した入れ子モデルとの LRT。自由度は階数の増分で数える(空のセルで列が落ちても正しい)"""
    X, nbd = ctx["X"], ctx["nbd"]
    info = interaction_df_info(ctx, a, extra_cols, extra_names)
    keep_j = info["keep_j"]
    if not keep_j:
        P(f"  {label}: 件数が足りず交互作用の列を作れませんでした")
        return None
    E = extra_cols[:, keep_j]
    X1 = np.column_stack([X, E])
    r0, r1, df = info["rank_main"], info["rank_inter"], info["df"]
    b0 = np.r_[full["beta"], np.zeros(E.shape[1])]
    f1 = nb_fit(X1, nbd, b0=b0, a0=full["alpha"], offset=ctx.get("offset"))
    lr = 2 * (f1["llf"] - full["llf"])
    p = chi2_sf(lr, df) if df > 0 and lr >= -1e-6 else float("nan")
    aic0 = -2 * full["llf"] + 2 * (r0 + 1)
    aic1 = -2 * f1["llf"] + 2 * (r1 + 1)
    P(f"  {label}: LR={lr:.2f} df={df} p={p:.4g}  ΔAIC={aic1 - aic0:.1f}(負なら交互作用ありが良い)  列 {len(extra_names)}→{len(keep_j)}")
    for ln in interaction_df_lines(info, a, max_df, note):
        P(ln)
    return {"test": label, "LR_chi2": lr, "df": df, "p": p, "delta_AIC": aic1 - aic0, "llf_main": full["llf"], "llf_interaction": f1["llf"], "converged": f1["converged"],
            "n_cols": info["n_cols"], "n_cols_kept": info["n_kept"], "rank_main": r0, "rank_inter": r1, "max_df": max_df if max_df is not None else np.nan}


def das_journal_cols(ctx):
    """DAS ダミー × 雑誌ダミー(最初の雑誌は基準なので除く)の列。戻り値: (E, 列名, D, J, 最大の df)。nb_suite と --check-df で同じ列を使う"""
    D = ctx["use"][ctx["das_cols"]].values.astype(float)
    nj = len(ctx["jlabels"])
    if nj <= 1:
        return None, [], D, None, 0
    J = np.column_stack([(ctx["jcodes"] == j).astype(float) for j in range(1, nj)])
    E = np.column_stack([D[:, k] * J[:, j] for k in range(D.shape[1]) for j in range(J.shape[1])])
    en = [f"{ctx['das_cols'][k]}×{ctx['jlabels'][j + 1]}" for k in range(D.shape[1]) for j in range(J.shape[1])]
    return E, en, D, J, D.shape[1] * J.shape[1]


def das_journal_cells(ctx, ref, a, P, outdir, tag):
    """類型×雑誌の件数表。--min-inter 未満(交互作用の列から除かれる)と、雑誌別の NB で比較できないセルに印をつける。nb_das_journal_cells_<tag>.csv に保存"""
    use, das_cols = ctx["use"], ctx["das_cols"]
    jn = dict(zip(ctx["jlabels"], jshort(pd.Series(ctx["jlabels"]))))
    cats = [ref] + [c[4:] for c in das_cols]
    rows = []
    for j, jl in enumerate(ctx["jlabels"]):
        s_ = use[ctx["jcodes"] == j]
        nj_ = len(s_)
        for c in cats:
            n_c = int(nj_ - s_[das_cols].values.sum()) if c == ref else int(s_["das_" + c].sum())
            if c == ref:
                by_ok, inter_col, inter_keep = np.nan, False, np.nan
            else:
                by_ok = bool(n_c >= a.min_cat_j and (nj_ - n_c) >= a.min_cat_j and nj_ >= 500)
                inter_col = bool(j >= 1)
                inter_keep = bool(j >= 1 and n_c >= a.min_inter)
            rows.append(dict(journal=jn[jl], journal_key=jl, das=c, n_cell=n_c, n_journal=nj_, is_ref=(c == ref),
                             interaction_column=inter_col, interaction_kept=inter_keep, by_journal_ok=by_ok))
    t = pd.DataFrame(rows)
    t.to_csv(os.path.join(outdir, f"nb_das_journal_cells_{tag}.csv"), index=False, encoding="utf-8-sig")
    piv = t.pivot(index="das", columns="journal", values="n_cell").reindex(cats)
    piv = piv[[jn[x] for x in ctx["jlabels"]]]
    mark = t.assign(txt=lambda x: x.n_cell.map(lambda v: f"{v:,}") + np.where((~x.is_ref) & (x.interaction_column) & (~x.interaction_kept.astype(bool)), "*", "")
                    + np.where((~x.is_ref) & (~x.by_journal_ok.fillna(True).astype(bool)), "†", "")).pivot(index="das", columns="journal", values="txt").reindex(cats)
    mark = mark[[jn[x] for x in ctx["jlabels"]]]
    nonref = t[~t.is_ref]
    n_cells = len(nonref)
    n_inter_cols = int(nonref.interaction_column.sum())
    n_inter_dropped = int((nonref.interaction_column & ~nonref.interaction_kept.astype(bool)).sum())
    n_by_ok = int(nonref.by_journal_ok.astype(bool).sum())
    P(f"\n[類型×雑誌の件数(基準 {ref} を含む)]  * = 件数が --min-inter({a.min_inter}) 未満で交互作用の列から除かれるセル / † = 雑誌別の NB で比較できないセル(類型か、それ以外の件数が --min-cat-j({a.min_cat_j}) 未満)")
    P(mark.to_string())
    P(f"  基準以外の類型×雑誌のセル {n_cells} 個 / 交互作用の列になるセル {n_inter_cols} 個(最初の雑誌 {jn[ctx['jlabels'][0]]} は雑誌の基準なので列がない)/ うち件数が足りず除かれるセル {n_inter_dropped} 個 → 交互作用の列 {n_inter_cols - n_inter_dropped} 個")
    P(f"  雑誌別の NB で基準 {ref} と比較できるセル {n_by_ok} 個(論文の「54 journal-by-category comparisons」に対応)")
    return t


def das_contrasts(full, cov, names, das_cols, ref, alt, P, outdir, tag):
    """別の基準 alt との対比を、主モデル(基準 ref)の係数と分散から作る。β_k − β_alt(ref は −β_alt)。
    モデルを --das-ref alt で推定し直したときと同じ値になる(再パラメータ化)。Holm は 6 比較(ref を含む類型の数 − 1)にかける"""
    alt_col = f"das_{alt}"
    if alt == ref:
        P(f"\n[別の基準との対比] 主モデルの基準が {alt} なので、主モデルの係数がそのまま対比です")
        return None
    if alt_col not in names:
        P(f"\n[別の基準との対比] 基準 {alt} の列がモデルにないため作れません")
        return None
    b = full["beta"]
    ia = names.index(alt_col)
    cats = [(ref, None)] + [(c[4:], names.index(c)) for c in das_cols if c in names and c != alt_col]
    rows = []
    for lab, k in cats:
        w = np.zeros(len(b))
        if k is not None:
            w[k] = 1.0
        w[ia] = -1.0
        nz = np.nonzero(w)[0]
        est = float(w @ b)
        row = {"contrast": f"{lab} vs {alt}", "das": lab, "coef": est, "irr": math.exp(est)}
        for kind, key in (("cluster", "cluster"), ("model", "model")):
            V = cov[key]
            se = math.sqrt(float(w[nz] @ V[np.ix_(nz, nz)] @ w[nz]))
            row[f"se_{kind}"] = se
            row[f"p_{kind}"] = float(norm_p(est / se)[0])
            if kind == "cluster":
                row["irr_low"], row["irr_high"] = math.exp(est - 1.96 * se), math.exp(est + 1.96 * se)
        rows.append(row)
    t = pd.DataFrame(rows)
    m = len(t)
    for kind in ("cluster", "model"):
        t[f"p_holm_{kind}"] = holm(t[f"p_{kind}"].values)
    order = np.argsort(t.p_cluster.values)
    rank = np.empty(m, dtype=int)
    rank[order] = np.arange(1, m + 1)
    t["holm_rank_cluster"] = rank
    t["holm_multiplier_cluster"] = m - rank + 1
    t.to_csv(os.path.join(outdir, f"nb_contrast_{tag}_ref{alt}.csv"), index=False, encoding="utf-8-sig")
    P(f"\n[基準を {alt} にした対比(主モデルの基準 {ref} の係数と分散から計算。--das-ref {alt} で推定し直した結果と同じ)]  p_cluster は雑誌×年のクラスタ頑健、Holm は {m} 比較にかけた値(倍率 = Holm の係数。p の小さい順に {m}, {m - 1}, …)")
    P(t[["contrast", "irr", "irr_low", "irr_high", "p_cluster", "p_holm_cluster", "holm_rank_cluster", "holm_multiplier_cluster", "p_model", "p_holm_model"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4g}"))

    def _pt(p):
        return "$p < 0.001$" if p < 0.001 else f"$p = {p:.3f}$"
    below = t[t.irr < 1].sort_values("irr")
    above = t[t.irr >= 1].sort_values("irr", ascending=False)
    P(f"[論文に貼る形(Holm 調整後の p)]  {alt} より低い: " + ", ".join(f"{r.das} (IRR {r.irr:.2f}, Holm {_pt(r.p_holm_cluster)})" for r in below.itertuples())
      + f" / {alt} より高い: " + ", ".join(f"{r.das} (IRR {r.irr:.2f}, Holm {_pt(r.p_holm_cluster)})" for r in above.itertuples()))
    return t


def nb_by_journal(ctx, a, P, outdir, ref):
    """雑誌ごとに NB を推定し、DAS 類型の効果(基準との率比)を出す。Holm 補正は雑誌×類型の全比較にかける"""
    use, ivs, meta = ctx["use"], ctx["ivs"], ctx["meta"]
    rows = []
    jsn = dict(zip(ctx["jlabels"], jshort(pd.Series(ctx["jlabels"]))))
    for j, jname in enumerate(ctx["jlabels"]):
        s = use[ctx["jcodes"] == j]
        das_ok = [c for c in ctx["das_cols"] if s[c].sum() >= a.min_cat_j and (len(s) - s[c].sum()) >= a.min_cat_j]
        oth = [c for c in ivs if c not in ctx["das_cols"] and s[c].std() > 1e-9]
        yl = sorted(s.year.unique())
        cols, nm = [np.ones(len(s))], ["(切片)"]
        for yv in yl[1:]:
            cols.append((s.year.values == yv).astype(float)); nm.append(f"fe_year:{int(yv)}")
        for c in das_ok + oth:
            cols.append(s[c].values.astype(float)); nm.append(c)
        if len(das_ok) == 0 or len(s) < 500:
            continue
        Xj = np.column_stack(cols)
        yj = np.round(s.tc.values.astype(float))
        fj = nb_fit(Xj, NBData(yj), offset=(None if ctx.get("offset") is None else ctx["offset"][ctx["jcodes"] == j]))
        cj = nb_cov(fj, Xj, yj, codes=np.arange(len(yj)))   # 1 つの雑誌には雑誌×年が十数個しかなく、クラスタ頑健は成り立たないので、観測値ごとの頑健(HC)を使う
        idx = [nm.index(c) for c in das_ok]
        t = _irr_table(fj, cj, nm, idx, meta).rename(columns={"se_cluster": "se_robust", "p_cluster": "p_robust"})
        t.insert(0, "journal", jname)
        t["n_journal"] = len(s)
        t["n_class"] = [int(s[c].sum()) for c in das_ok]
        t["das"] = [c[4:] for c in das_ok]
        t["alpha"] = fj["alpha"]
        w, pw = _wald(fj["beta"], cj["cluster"], idx)
        t["wald_all_das_chi2_robust"], t["wald_all_das_p_robust"] = w, pw
        rows.append(t)
        P(f"  {jsn[jname]}: N={len(s):,} 類型 {len(das_ok)} 個 / DAS 全体 Wald(頑健) χ²({len(idx)})={w:.1f} p={pw:.3g}" + ("" if fj["converged"] else "  [収束せず]"))
    if not rows:
        P("  雑誌別に推定できる雑誌がありませんでした")
        return None
    r = pd.concat(rows, ignore_index=True)
    r["p_holm_robust"] = holm(r.p_robust.values)
    r["p_holm_model"] = holm(r.p_model.values)
    cols = ["journal", "das", "n_journal", "n_class", "irr", "irr_low", "irr_high", "p_robust", "p_holm_robust", "p_model", "p_holm_model", "alpha",
            "wald_all_das_chi2_robust", "wald_all_das_p_robust"]
    r[cols].to_csv(os.path.join(outdir, "nb_by_journal.csv"), index=False, encoding="utf-8-sig")
    P(f"\n[雑誌別の DAS 効果(基準 {ref} との率比 IRR、95%区間と p は観測値ごとの頑健(HC)標準誤差)]  Holm は雑誌×類型の {len(r)} 比較全体にかけた値。件数が少ない類型は区間が不安定")
    P(r[["journal", "das", "n_class", "irr", "irr_low", "irr_high", "p_robust", "p_holm_robust"]].assign(journal=jshort(r.journal))
      .to_string(index=False, float_format=lambda x: f"{x:.4g}"))
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.ticker
        ds = sorted(r.das.unique())
        fig, axes = plt.subplots(1, len(ds), figsize=(3.2 * len(ds), 0.45 * r.journal.nunique() + 1.6), sharey=True, squeeze=False)
        js = list(r.journal.unique())
        for ax, dv_ in zip(axes[0], ds):
            s = r[r.das == dv_]
            ypos = [js.index(x) for x in s.journal]
            ax.errorbar(s.irr, ypos, xerr=[s.irr - s.irr_low, s.irr_high - s.irr], fmt="o", capsize=2)
            ax.axvline(1, color="gray", lw=0.8)
            ax.set_xscale("log"); ax.set_title(f"DAS={dv_} vs {ref}", fontsize=9)
            _log_ticks(ax, None, fontsize=7)
            ax.set_yticks(range(len(js))); ax.set_yticklabels(list(jshort(pd.Series(js))), fontsize=7)
        fig.supxlabel("IRR (" + ("expected days" if _is_rv(a.dv) else "citation count") + ", log scale)", fontsize=8)
        fig.tight_layout()
        fig.savefig(os.path.join(outdir, "nb_forest_by_journal.png"), dpi=150)
        plt.close(fig)
    except Exception as e:
        P(f"  (フォレスト図は作りませんでした: {type(e).__name__})")
    return r


def nb_suite(d, meta, das_cols, base_ivs, ref, a, outdir, lines, log):
    P = lines.append
    tag = _tag(a.dv)
    P(f"\n{'=' * 78}\n[NB 回帰(論文の Table 4・LRT に対応)]  従属変数 {a.dv}(整数の計数)\n{'=' * 78}")
    P("モデル: NB2(対数リンク)。固定効果は雑誌+出版年のダミー(--nb-fe jy で雑誌×年)。標準誤差は モデルに基づく値と、雑誌×年でクラスタした頑健値の両方を出す。")
    P(_nb_note(a.dv))
    ctx = nb_build(d, meta, das_cols, base_ivs, a, log)
    P(log[-1])
    if a.nb_sample:
        P(f"[注意] --nb-sample {a.nb_sample:,} のため、NB 回帰は一部の行だけの暫定結果です。論文や本文には全行の結果を使ってください")
    if len(ctx["y"]) < 1000:
        P("行数が少なすぎるので NB を中止します")
        return
    P("主モデルを推定中...")
    full = nb_fit(ctx["X"], ctx["nbd"], offset=ctx.get("offset"))
    cov = nb_cov(full, ctx["X"], ctx["y"], codes=ctx["gcodes"])
    if "log_age" in ctx["names"] and "log_age" in ctx.get("sds", {}):   # 経過時間の対数を共変量にしたとき、弾力性を出す(係数 ÷ 標準化に使った SD)
        _i = ctx["names"].index("log_age"); _sd = ctx["sds"]["log_age"]
        _b = float(full["beta"][_i]); _se = math.sqrt(max(float(cov["cluster"][_i, _i]), 0.0))
        P(f"[弾力性] log_age: n={len(ctx['y']):,} / 標準化に使った SD {_sd:.6f} / 係数 {_b:.5f}(クラスタ頑健 SE {_se:.5f})/ 弾力性 {_b / _sd:.3f}(95% 区間 {(_b - 1.96 * _se) / _sd:.3f}〜{(_b + 1.96 * _se) / _sd:.3f})")
    P(f"対数尤度 {full['llf']:.2f} / alpha(過分散) {full['alpha']:.4f} / 反復 {full['iters']} / 収束 {full['converged']} / クラスタ数 {int(ctx['gcodes'].max()) + 1}")
    if int(ctx["gcodes"].max()) + 1 < 30:
        P("[注意] クラスタ(雑誌×年)が 30 未満で、頑健な標準誤差は小さめに出ます")
    pd.DataFrame([{"dv": a.dv, "fe": a.nb_fe, "n": int(len(ctx["y"])), "n_clusters": int(ctx["gcodes"].max()) + 1,
                   "n_journals": len(ctx["jlabels"]), "n_years": int(len(np.unique(ctx["year"]))), "llf": float(full["llf"]),
                   "alpha": float(full["alpha"]), "converged": bool(full["converged"]), "das_ref": ref, "nb_sample": int(a.nb_sample),
                   "review_as_iv": bool(a.review_as_iv), "dedup_key": a.dedup_key, "version": VERSION}]
                 ).to_csv(os.path.join(outdir, f"nb_model_{tag}.csv"), index=False, encoding="utf-8-sig")   # 補足表(S1・S2)の脚注用
    names, meta_ = ctx["names"], ctx["meta"]
    idx_all = [i for i, n in enumerate(names) if n in meta_]
    irr = _irr_table(full, cov, names, idx_all, meta_)
    das_mask = irr.group == G_DAS
    irr["p_holm_cluster"] = np.nan
    irr["p_holm_model"] = np.nan
    irr.loc[das_mask, "p_holm_cluster"] = holm(irr.loc[das_mask, "p_cluster"].values)   # DAS の比較(類型の数)を 1 つの族として補正
    irr.loc[das_mask, "p_holm_model"] = holm(irr.loc[das_mask, "p_model"].values)
    irr["p_holm_all_cluster"] = holm(irr.p_cluster.values)                                 # 全係数を 1 つの族として補正
    irr.to_csv(os.path.join(outdir, f"nb_irr_{tag}.csv"), index=False, encoding="utf-8-sig")
    P("\n[率比 IRR] 連続量は 1SD、0/1 は 0→1。p_holm_* は DAS の比較だけを族とした Holm 補正、p_holm_all_cluster は全係数を族とした補正")
    P(irr[["variable", "group", "scale", "irr", "irr_low", "irr_high", "p_model", "p_cluster", "p_holm_cluster", "p_holm_all_cluster"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4g}"))
    # 同時検定(Wald)をグループごとに
    wr = []
    for g in dict.fromkeys(meta_[names[i]]["group"] for i in idx_all):
        idx = [i for i in idx_all if meta_[names[i]]["group"] == g]
        wm, pm = _wald(full["beta"], cov["model"], idx)
        wc, pc = _wald(full["beta"], cov["cluster"], idx)
        wr.append({"group": g, "df": len(idx), "wald_chi2_model": wm, "p_model": pm, "wald_chi2_cluster": wc, "p_cluster": pc})
    wt = pd.DataFrame(wr)
    wt.to_csv(os.path.join(outdir, f"nb_wald_{tag}.csv"), index=False, encoding="utf-8-sig")
    P("\n[NB の同時検定(Wald)] 帰無仮説: そのグループの係数がすべて 0。_model は通常の分散、_cluster は雑誌×年でクラスタした頑健分散")
    P(wt.to_string(index=False, float_format=lambda x: f"{x:.4g}"))
    # 基準を替えた対比(論文 3.6節の「N を基準にした」結果)
    try:
        das_contrasts(full, cov, names, das_cols, ref, a.contrast_ref, P, outdir, tag)
    except Exception as e:
        P(f"[警告] 別の基準との対比を作れませんでした: {type(e).__name__}: {e}")
    # LRT の重要度表
    if a.nb_lrt != "off":
        P(f"\n[LRT による重要度(ブロックを 1 つずつ外して再推定。粒度 {a.nb_lrt})]")
        lt = nb_lrt(ctx, full, a, P)
        lt.to_csv(os.path.join(outdir, f"nb_lrt_{tag}.csv"), index=False, encoding="utf-8-sig")
        P(lt.drop(columns=["llf_full", "llf_reduced"]).to_string(index=False, float_format=lambda x: f"{x:.4g}"))
        P("LR は標本が大きいほど大きくなるため、ブロック間の相対比較(LR_per_df も参照)と、IRR の大きさの両方で読むこと。DAS の行が「DAS 全体」の LRT(論文の LR(6) に相当)。")
    # 交互作用
    if not a.no_interactions:
        P("\n[交互作用の LRT(主効果モデルとの入れ子比較)]")
        irows = []
        try:
            das_journal_cells(ctx, ref, a, P, outdir, tag)
        except Exception as e:
            P(f"[警告] 類型×雑誌の件数表を作れませんでした: {type(e).__name__}: {e}")
        E, en, D, J, max_df = das_journal_cols(ctx)
        if J is not None:
            r = nb_interaction(ctx, full, a, P, "DAS × 雑誌", E, en, max_df=max_df, note="(DAS 類型の数 − 1)×(雑誌の数 − 1)")
            if r: irows.append(r)
        post = (ctx["year"] >= a.interaction_year).astype(float)
        if 0 < post.mean() < 1:
            E = D * post[:, None]
            r = nb_interaction(ctx, full, a, P, f"DAS × 出版年{a.interaction_year}以降", E, [f"{c}×post" for c in ctx["das_cols"]], max_df=len(ctx["das_cols"]))
            if r: irows.append(r)
        if irows:
            pd.DataFrame(irows).to_csv(os.path.join(outdir, f"nb_interaction_{tag}.csv"), index=False, encoding="utf-8-sig")
        P("COVID の話題フラグは v27 CSV の列に確実にあるか分からないため、論文の DAS×COVID は「出版年が基準年以降か」で代用している。")
    # 雑誌別
    if not a.no_by_journal:
        P("\n[雑誌別の NB(各雑誌で DAS の効果を推定)]")
        nb_by_journal(ctx, a, P, outdir, ref)
    # 重複除外の感度分析
    if a.dedup_key and a.dedup_key in d.columns:
        dd = d[d[a.dedup_key] != ""]
        dd = dd.drop_duplicates(subset=a.dedup_key, keep="first")
        k = len(d[d.tc.notna()]) - len(dd[dd.tc.notna()])
        P(f"\n[感度分析: {a.dedup_key} の重複を除く(先頭行を残す)] 被引用数ありの行で {k:,} 行を除外")
        if k == 0:
            P("  重複がないので主モデルと同じ結果です")
        else:
            ctx2 = nb_build(dd, meta, das_cols, base_ivs, a, [])
            f2 = nb_fit(ctx2["X"], ctx2["nbd"], offset=ctx2.get("offset"))
            c2 = nb_cov(f2, ctx2["X"], ctx2["y"], codes=ctx2["gcodes"])
            i2 = [i for i, n in enumerate(ctx2["names"]) if n in ctx2["ivs"] and n in ctx2["das_cols"]]
            t2 = _irr_table(f2, c2, ctx2["names"], i2, meta_)[["variable", "irr", "irr_low", "irr_high", "p_cluster"]]
            cmp_ = irr.loc[das_mask, ["variable", "irr", "irr_low", "irr_high", "p_cluster"]].merge(t2, on="variable", suffixes=("_main", "_dedup"))
            cmp_["irr_pct_diff"] = (cmp_.irr_dedup / cmp_.irr_main - 1) * 100
            cmp_.to_csv(os.path.join(outdir, f"nb_dedup_compare_{tag}.csv"), index=False, encoding="utf-8-sig")
            P(f"  N={len(ctx2['y']):,}(主モデル {len(ctx['y']):,})")
            P(cmp_.to_string(index=False, float_format=lambda x: f"{x:.4g}"))
    elif a.dedup_key:
        P(f"\n[感度分析] 重複を判定する列 {a.dedup_key} が CSV にないため行いません(--dedup-key で列名を指定できます)")


# ----------------------------------------------------------------------------- 記述統計と順位検定(論文の Kruskal-Wallis・対比較に対応)
def _tie_term(vals):
    _, c = np.unique(vals, return_counts=True)
    return float(((c ** 3) - c).sum())


def kruskal(groups):
    allv = np.concatenate(groups)
    N = len(allv)
    rk = pd.Series(allv).rank(method="average").values
    H, pos = 0.0, 0
    for g in groups:
        r = rk[pos:pos + len(g)]
        H += r.sum() ** 2 / len(g)
        pos += len(g)
    H = 12.0 / (N * (N + 1)) * H - 3 * (N + 1)
    C = 1 - _tie_term(allv) / (N ** 3 - N)
    H = H / C if C > 0 else float("nan")
    return H, chi2_sf(H, len(groups) - 1) if H == H else float("nan")


def mannwhitney(x, y):
    n1, n2 = len(x), len(y)
    allv = np.concatenate([x, y])
    N = n1 + n2
    rk = pd.Series(allv).rank(method="average").values
    U1 = rk[:n1].sum() - n1 * (n1 + 1) / 2.0
    mu = n1 * n2 / 2.0
    var = n1 * n2 / 12.0 * ((N + 1) - _tie_term(allv) / (N * (N - 1)))
    if var <= 0:
        return float("nan"), float("nan"), 0.5
    z = (abs(U1 - mu) - 0.5) / math.sqrt(var)
    return z * np.sign(U1 - mu), math.erfc(max(z, 0) / math.sqrt(2)), U1 / (n1 * n2)


def rank_tests(d, ref, a, outdir, P):
    t = d[d.tc.notna()].copy()
    t["tc_pct"] = t.groupby("gid").tc.rank(pct=True)   # 雑誌×年の中での順位(0〜1)。出版年の違いを調整した値
    P(f"\n{'=' * 78}\n[記述統計と順位検定]  従属変数 {a.dv}(論文の Kruskal-Wallis・対比較に対応)\n{'=' * 78}")
    ct = pd.crosstab(jshort(t.journal_key), t.das_label)
    ct["合計"] = ct.sum(axis=1)
    ct.loc["合計"] = ct.sum(axis=0)
    ct.to_csv(os.path.join(outdir, "desc_journal_das_counts.csv"), encoding="utf-8-sig")
    P("\n[雑誌×DAS の件数(被引用数あり)]")
    P(ct.to_string())
    ds = t.groupby("das_label").agg(n=("tc", "size"), mean=("tc", "mean"), median=("tc", "median"), q1=("tc", lambda s: s.quantile(.25)),
                                      q3=("tc", lambda s: s.quantile(.75)), mean_pct_in_journal_year=("tc_pct", "mean"))
    ds.to_csv(os.path.join(outdir, "desc_das_citation_summary.csv"), encoding="utf-8-sig")
    P("\n[DAS 類型ごとの被引用数。mean_pct_in_journal_year は雑誌×年の中の順位の平均(0.5 が真ん中)]")
    P(ds.round(3).to_string())
    kw_rows, pw_rows = [], []
    for jn, s in t.groupby("journal_key"):
        cats = [c for c in sorted(s.das_label.unique()) if (s.das_label == c).sum() >= a.min_cat_j]
        if len(cats) < 2:
            continue
        for lab, col in (("raw", "tc"), ("adj", "tc_pct")):
            H, p = kruskal([s.loc[s.das_label == c, col].values for c in cats])
            kw_rows.append({"journal": jn, "value": lab, "k": len(cats), "n": int(s.das_label.isin(cats).sum()), "H": H, "p": p})
        for i, c1 in enumerate(cats):
            for c2 in cats[i + 1:]:
                z, p, A = mannwhitney(s.loc[s.das_label == c1, "tc_pct"].values, s.loc[s.das_label == c2, "tc_pct"].values)
                pw_rows.append({"journal": jn, "A": c1, "B": c2, "n_A": int((s.das_label == c1).sum()), "n_B": int((s.das_label == c2).sum()), "z": z, "p": p, "prob_A_gt_B": A})
    if kw_rows:
        kw = pd.DataFrame(kw_rows)
        kw["p_holm"] = np.nan
        for lab in ("raw", "adj"):
            m = kw.value == lab
            kw.loc[m, "p_holm"] = holm(kw.loc[m, "p"].values)
        kw.to_csv(os.path.join(outdir, "rank_kruskal_by_journal.csv"), index=False, encoding="utf-8-sig")
        P("\n[Kruskal-Wallis(雑誌ごと)] raw=被引用数そのまま(論文と同じ)/ adj=雑誌×年の中の順位。p_holm は雑誌の数で補正")
        P(kw.assign(journal=jshort(kw.journal)).to_string(index=False, float_format=lambda x: f"{x:.4g}"))
    if pw_rows:
        pw = pd.DataFrame(pw_rows)
        pw["p_holm"] = holm(pw.p.values)
        pw.to_csv(os.path.join(outdir, "rank_pairwise_by_journal.csv"), index=False, encoding="utf-8-sig")
        r = pw[(pw.A == ref) | (pw.B == ref)]
        P(f"\n[対比較(Mann-Whitney、雑誌×年内の順位)のうち基準 {ref} を含むもの] prob_A_gt_B は A が B より多く引用される確率(0.5 で差なし)。全 {len(pw)} 比較は rank_pairwise_by_journal.csv")
        P(r.assign(journal=jshort(r.journal)).to_string(index=False, float_format=lambda x: f"{x:.4g}"))


# ----------------------------------------------------------------------------- 頑健性の確認(設定を変えて NB を走らせ直し、DAS 類型の効果の並び・向きを比べる)
ROBUST_RUNS_REVIEW = {"base": ("review_days", "additive"), "jy": ("review_days", "jy")}   # --dv review_days のときの設定(PMC の cited-by は査読期間と無関係)
ROBUST_RUNS = {
    "base": ("wos_TC", "additive"),     # 被引用数 = wos_TC、固定効果 = 雑誌+出版年(主分析)
    "jy": ("wos_TC", "jy"),             # 固定効果 = 雑誌×年
    "pmc": ("pmc_citedby_n", "additive"),   # 被引用数 = PMC の cited-by
    "pmc_jy": ("pmc_citedby_n", "jy"),
}
_ROBUST_OPTS = {"--robustness": 0, "--robustness-only": 0, "--robust-skip-existing": 0, "--robust-runs": 1, "--robust-outroot": 1,
                "--outdir": 1, "--target": 1, "--dv": 1, "--nb-fe": 1, "--nb-lrt": 1, "--no-interactions": 0, "--no-rank": 0}


def _child_args(argv):
    """子の実行に渡す引数。頑健性の設定と、上書きするオプションを取り除く(--opt=値 の形も扱う)"""
    out, i = [], 0
    while i < len(argv):
        t = argv[i]
        key = t.split("=", 1)[0]
        if key in _ROBUST_OPTS:
            if "=" not in t:
                i += _ROBUST_OPTS[key]
        else:
            out.append(t)
        i += 1
    return out


def _spearman(x, y):
    rx, ry = pd.Series(x).rank(), pd.Series(y).rank()
    return float(np.corrcoef(rx, ry)[0, 1]) if len(rx) > 2 else float("nan")


def robustness_compare(names, outs, outroot, das_ref, P):
    tabs = {}
    for n in names:
        t = pd.read_csv(os.path.join(outs[n], f"nb_irr_{_tag(ROBUST_RUNS[n][0])}.csv"))
        t = t[t.group == G_DAS].copy()
        t["das"] = t.variable.str.replace("das_", "", regex=False)
        tabs[n] = t.set_index("das")
    b = names[0]
    classes = list(tabs[b].index)
    comp = pd.DataFrame({"das": classes})
    for n in names:
        t = tabs[n].reindex(classes)
        comp[f"irr_{n}"], comp[f"low_{n}"], comp[f"high_{n}"], comp[f"p_holm_{n}"] = t.irr.values, t.irr_low.values, t.irr_high.values, t.p_holm_cluster.values
    comp.to_csv(os.path.join(outroot, "robustness_das_overall.csv"), index=False, encoding="utf-8-sig")
    P(f"DAS 類型の率比の頑健性(基準 {das_ref}、{len(classes)} 類型、雑誌をまとめたモデル)。比べる設定: " + ", ".join(f"{n}=[{ROBUST_RUNS[n][0]}, FE={ROBUST_RUNS[n][1]}]" for n in names))
    P(("率比は 1 より大きいと、基準より査読期間(日数)が長い。" if ROBUST_RUNS["base"][0] == "review_days" else "率比は 1 より大きいと、基準より被引用数が多い。") + "p_holm はクラスタ頑健 p を DAS の比較で Holm 補正した値。\n")
    P(comp[["das"] + [f"irr_{n}" for n in names] + [f"p_holm_{n}" for n in names]].to_string(index=False, float_format=lambda x: f"{x:.4g}"))
    P("\n率比の大きい順の並び:")
    for n in names:
        P(f"  {n:7s} " + " > ".join(comp.sort_values(f"irr_{n}", ascending=False).das.tolist()))
    if len(names) > 1:
        P(f"\n基準({b})との比較:")
        rows = []
        for n in names[1:]:
            rows.append({"run": n, "spearman_rank": _spearman(comp[f"irr_{b}"], comp[f"irr_{n}"]),
                         "same_direction": float(((comp[f"irr_{b}"] > 1) == (comp[f"irr_{n}"] > 1)).mean()),
                         "same_significance": float(((comp[f"p_holm_{b}"] < 0.05) == (comp[f"p_holm_{n}"] < 0.05)).mean()),
                         "max_abs_log_irr_diff": float((np.log(comp[f"irr_{n}"]) - np.log(comp[f"irr_{b}"])).abs().max())})
        P(pd.DataFrame(rows).to_string(index=False, float_format=lambda x: f"{x:.3f}"))
        P("  spearman_rank: 類型の並び順の一致(1 で完全一致)/ same_direction: 率比が 1 を挟んで同じ側にある類型の割合 /")
        P("  same_significance: Holm 補正後 p<0.05 かどうかが同じ類型の割合 / max_abs_log_irr_diff: 率比の最大のずれ(0.05 なら約 5%)")
        P(f"\n基準で有意(p_holm<0.05)な類型が、変種でも同じ向きで有意か:")
        for n in names[1:]:
            sb = comp[comp[f"p_holm_{b}"] < 0.05]
            if len(sb) == 0:
                P(f"  {n}: 基準で有意な類型がない")
                continue
            ok = sb[(sb[f"p_holm_{n}"] < 0.05) & ((sb[f"irr_{n}"] > 1) == (sb[f"irr_{b}"] > 1))]
            lost = sorted(set(sb.das) - set(ok.das))
            P(f"  {n}: {len(ok)}/{len(sb)} 類型が同じ向きで有意" + (f"(外れたのは {', '.join(lost)})" if lost else ""))
    cells = None
    for n in names:
        f = os.path.join(outs[n], "nb_by_journal.csv")
        if not os.path.exists(f):
            P(f"\n[{n}] nb_by_journal.csv がないため雑誌別の比較から外す")
            continue
        t = pd.read_csv(f)[["journal", "das", "n_class", "irr", "irr_low", "irr_high", "p_holm_robust"]]
        t = t.rename(columns={"irr": f"irr_{n}", "irr_low": f"low_{n}", "irr_high": f"high_{n}", "p_holm_robust": f"p_holm_{n}"})
        cells = t if cells is None else cells.merge(t.drop(columns=["n_class"]), on=["journal", "das"], how="outer")
    if cells is not None and len(names) > 1 and f"irr_{b}" in cells:
        cells.to_csv(os.path.join(outroot, "robustness_by_journal_cells.csv"), index=False, encoding="utf-8-sig")
        P(f"\n雑誌×類型ごとの率比(各雑誌で別々に推定)の頑健性: 基準 {b} で推定できた {int(cells[f'irr_{b}'].notna().sum())} セル")
        rows, flips = [], []
        for n in names[1:]:
            if f"irr_{n}" not in cells:
                continue
            m = cells.dropna(subset=[f"irr_{b}", f"irr_{n}"])
            lb, ln = np.log(m[f"irr_{b}"]), np.log(m[f"irr_{n}"])
            sb = m[m[f"p_holm_{b}"] < 0.05]
            keep = sb[(sb[f"p_holm_{n}"] < 0.05) & (np.sign(np.log(sb[f"irr_{n}"])) == np.sign(np.log(sb[f"irr_{b}"])))]
            fl = m[(np.sign(lb) != np.sign(ln)) & ((m[f"p_holm_{b}"] < 0.05) | (m[f"p_holm_{n}"] < 0.05))]
            rows.append({"run": n, "cells": len(m), "same_direction": float((np.sign(lb) == np.sign(ln)).mean()), "corr_log_irr": float(np.corrcoef(lb, ln)[0, 1]),
                         "base_significant": len(sb), "still_significant_same_direction": len(keep), "direction_flipped_and_significant": len(fl)})
            if len(fl):
                flips.append((n, fl[["journal", "das", f"irr_{b}", f"p_holm_{b}", f"irr_{n}", f"p_holm_{n}"]]))
        P(pd.DataFrame(rows).to_string(index=False, float_format=lambda x: f"{x:.3f}"))
        P("  still_significant_same_direction: 基準で Holm 補正後 p<0.05 のセルのうち、変種でも同じ向きで有意なもの")
        P("  direction_flipped_and_significant: 向きが逆になり、どちらかで有意だったセル")
        for n, fl in flips:
            P(f"\n  [{n}] 向きが逆になった有意セル")
            P(fl.to_string(index=False, float_format=lambda x: f"{x:.4g}"))
    P("\n読み方の目安: 並びと向きが一致し、基準で有意な類型の大半が残れば頑健。")
    if ROBUST_RUNS["base"][0] != "review_days":
        P("pmc_citedby_n は PMC に引用された論文数だけを数えるので、WoS より少なく、分野によって偏る。向きが同じなら補強、違っても直ちに主結果の誤りとは言えず、WoS の累積引用に依存した結果として注意して書く。")


def run_robustness(a, outdir, reuse_main, lines):
    """設定を変えた実行を、このスクリプト自身を子として走らせて行い、結果を比べる"""
    import subprocess
    outroot = os.path.expanduser(a.robust_outroot) if a.robust_outroot else os.path.join(outdir, "robustness")
    os.makedirs(outroot, exist_ok=True)
    names = [n.strip() for n in a.robust_runs.split(",") if n.strip()]
    bad = [n for n in names if n not in ROBUST_RUNS]
    if bad:
        sys.exit(f"--robust-runs に不明な設定: {bad}(使えるのは {', '.join(ROBUST_RUNS)})")
    outs = {}
    for n in names:
        dv, fe = ROBUST_RUNS[n]
        if n == "base" and reuse_main:
            outs[n] = outdir
            print("[頑健性] base は今回の主分析の出力を使います", file=sys.stderr, flush=True)
            continue
        out = os.path.join(outroot, n)
        outs[n] = out
        if a.robust_skip_existing and os.path.exists(os.path.join(out, f"nb_irr_{_tag(dv)}.csv")):
            print(f"[頑健性] {n}: 既存の出力を使います", file=sys.stderr, flush=True)
            continue
        cmd = [sys.executable, os.path.abspath(sys.argv[0])] + _child_args(sys.argv[1:]) + [
            "--outdir", out, "--target", "citations", "--dv", dv, "--nb-fe", fe, "--nb-lrt", "off", "--no-interactions", "--no-rank"]
        print(f"[頑健性] {n}: dv={dv}, FE={fe} を実行中(数分〜十数分)", file=sys.stderr, flush=True)
        r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        with open(os.path.join(outroot, f"log_{n}.txt"), "w", encoding="utf-8") as f:
            f.write(r.stdout + "\n" + r.stderr)
        if r.returncode != 0 or not os.path.exists(os.path.join(out, f"nb_irr_{_tag(dv)}.csv")):
            print(r.stderr[-1500:], file=sys.stderr)
            sys.exit(f"[頑健性] {n} が失敗しました。{os.path.join(outroot, f'log_{n}.txt')} を確認してください")
    out_lines = [f"\n{'=' * 78}\n[頑健性の確認: DAS 類型の効果(NB の率比)を、被引用数の定義と固定効果を替えて比べる]\n{'=' * 78}"]
    robustness_compare(names, outs, outroot, a.das_ref, out_lines.append)
    txt = "\n".join(out_lines)
    with open(os.path.join(outroot, "robustness_summary.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    lines.append(txt)
    print(txt)
    print("\n頑健性の保存先:", outroot)


# ----------------------------------------------------------------------------- 論文用の図表(v004)
# 分析が保存した CSV を読んで、論文向けの図(英語ラベル、PNG 300dpi と PDF)と表(CSV と 1 つの xlsx)を作る。
# 分析を再実行せずに作り直せる(--paper-only)。出力: <outdir>/paper/figures, <outdir>/paper/tables
EN_VAR = {"n_authors": "Number of authors (log)", "collab_any": "Consortium authorship", "n_corresp": "Corresponding authors (log)",
          "equal_contrib_any": "Equal-contribution note", "n_orcid": "Authors with ORCID (log)", "n_countries": "Number of countries (log)",
          "n_institutions": "Number of institutions (log)", "n_refs": "Number of references (log)", "ref_age_median": "Median reference age",
          "has_data_citation": "Data citation present", "has_funding": "Funding statement present", "body_words": "Body length, words (log)",
          "n_figures": "Number of figures (log)", "n_tables": "Number of tables (log)", "n_equations": "Number of equations (log)",
          "n_supplementary": "Supplementary files (log)", "abstract_words": "Abstract length, words (log)", "title_words": "Title length, words",
          "title_has_colon": "Title contains colon", "title_has_question": "Title is a question", "log_review": "Review duration (log days)"}
EN_GROUP = {"著者・国・共著": "Authors, countries, collaboration", "参考文献・助成": "References and funding", "図表・文章量": "Figures, tables, length",
            "題名": "Title", "DAS": "DAS category", "査読期間": "Review duration", "責任著者の国": "Corresponding-author country", "固定効果": "Fixed effects"}


def _en(v):
    if v.startswith("das_"):
        return f"DAS {v[4:]}"
    if v.startswith("corr_"):
        return "Corr. author country: " + v[5:].replace("_", " ")
    return EN_VAR.get(v, v)


def _fp(p):
    if p != p:
        return ""
    return "<0.001" if p < 0.001 else f"{p:.3f}"


def _stars(p):
    return "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""


def _paper_plt():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False, "axes.titlesize": 10,
                         "figure.dpi": 100, "savefig.bbox": "tight", "font.family": "sans-serif"})
    return plt


_PAPER_SFX = ""   # 査読期間の図表には _review を付けて、被引用数の図表と同じフォルダで名前がぶつからないようにする


_MAIN_ONLY = False   # v033: --main-figs のとき True(本論の図だけを PNG で保存する)
MAIN_FIGS = ("fig0_das_trend_by_journal", "fig7_citations_vs_review_irr", "fig3_das_irr_by_journal_heatmap", "fig3_das_irr_by_journal_heatmap_review",
             "fig4c_shapley_both", "fig5c_crude_vs_adjusted", "fig6c_robustness_both")


def _save(fig, figdir, name, made):
    name = name + ("" if name.startswith(("fig0", "fig7")) else _PAPER_SFX)
    import matplotlib.pyplot as plt
    if _MAIN_ONLY and name not in MAIN_FIGS:
        plt.close(fig)
        return
    for ext, kw in (("png", {"dpi": 300}),) if _MAIN_ONLY else (("png", {"dpi": 300}), ("pdf", {})):
        fig.savefig(os.path.join(figdir, f"{name}.{ext}"), **kw)
    plt.close(fig)
    made.append(name)


def _nice_log_ticks(lo, hi, max_n=6):
    """対数軸の目盛りを、表示範囲の広さに合わせて選ぶ。範囲が狭い(例: 0.95〜1.05)ときは 0.01〜0.05 刻み、広いときは従来の固定リスト。"""
    for step in (0.01, 0.02, 0.05, 0.1, 0.2):
        k0, k1 = math.ceil(lo / step - 1e-9), math.floor(hi / step + 1e-9)
        tk = [round(k * step, 3) for k in range(k0, k1 + 1)]
        if 3 <= len(tk) <= max_n:
            return tk
    return [v for v in (0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.4, 1.7, 2.0, 3.0) if lo <= v <= hi]


def _log_ticks(ax, vals, fontsize=None):
    import matplotlib.ticker
    ax.set_xscale("log")
    lo, hi = ax.get_xlim()
    tk = _nice_log_ticks(lo, hi)
    ax.set_xticks(tk)
    ax.set_xticklabels([f"{v:g}" for v in tk], **({"fontsize": fontsize} if fontsize else {}))
    ax.set_xlim(lo, hi)
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())


def _das_trend(a, plt, figdir, made, tables):
    """DAS カテゴリの年次変化を雑誌別に示す(積み上げ棒、全雑誌+雑誌ごとの小さな図)。WoS 照合の有無に関係なく、DAS ラベルのある論文すべてを使う"""
    from matplotlib.patches import Patch
    d, _ = read_cols(a.csv, ["journal_key", "pub_year", "das_label", "das_has_label", "article_type", "wos_notice_type"])
    if a.journal:
        d = d[d.journal_key.str.contains(a.journal, case=False, regex=False)]
    d = d[(d.get("das_has_label", "1") == "1") & (d.das_label != "")]
    if "article_type" in d and a.article_type:
        d = d[d.article_type == a.article_type]
    if "wos_notice_type" in d and not a.keep_notice:
        d = d[d.wos_notice_type == ""]
    d = d.copy()
    d["year"] = num(d.pub_year)
    d = d[d.year >= a.min_year].dropna(subset=["year"])
    if len(d) == 0:
        print("[論文用の図] DAS の年次変化: 該当する論文がないため作りませんでした", file=sys.stderr)
        return
    d["year"] = d.year.astype(int)
    pref = ["F", "M", "P", "R", "A", "C", "N"]
    cats = [c for c in pref if c in set(d.das_label)] + sorted(set(d.das_label) - set(pref))
    pal = {"F": "#0072B2", "M": "#56B4E9", "P": "#009E73", "R": "#E69F00", "A": "#D55E00", "C": "#CC79A7", "N": "#8c8c8c"}
    cmap = plt.get_cmap("tab20")
    colors = {c: pal.get(c, cmap(i)) for i, c in enumerate(cats)}
    d["jname"] = jshort(d.journal_key, 30)
    order = d.jname.value_counts().index.tolist()
    panels = [("All journals", d)] + [(j, d[d.jname == j]) for j in order]
    years = list(range(int(d.year.min()), int(d.year.max()) + 1))
    ncol = 4
    nrow = math.ceil((len(panels) + 1) / ncol)
    min_n = 20
    fig, axes = plt.subplots(nrow, ncol, figsize=(2.9 * ncol, 2.2 * nrow + 0.6), sharey=True, squeeze=False)
    rows = []
    for k, (name, s) in enumerate(panels):
        ax = axes[k // ncol][k % ncol]
        ct = pd.crosstab(s.year, s.das_label).reindex(index=years, columns=cats, fill_value=0)
        tot = ct.sum(axis=1)
        pct = ct.div(tot.replace(0, np.nan), axis=0) * 100
        shown = pct.where(tot >= min_n)
        bottom = np.zeros(len(years))
        for c in cats:
            v = shown[c].fillna(0).values
            ax.bar(years, v, bottom=bottom, color=colors[c], width=0.85, linewidth=0)
            bottom += v
        # v060: 先頭のパネルは 10 誌の合算。雑誌別のパネルと見分けがつくよう、題名を太字にして誌数を示す
        ax.set_title(f"All {len(order)} journals combined (n={len(s):,})" if k == 0 else f"{name} (n={len(s):,})", fontsize=8, fontweight="bold" if k == 0 else "normal")
        ax.set_ylim(0, 100)
        ax.set_xticks(years[::2])
        ax.tick_params(axis="both", labelsize=7)
        ax.tick_params(axis="x", labelrotation=90)
        if k % ncol == 0:
            ax.set_ylabel("Share of articles (%)", fontsize=7)
        for y in years:
            r = {"Journal": name, "Year": y, "N": int(tot[y])}
            for c in cats:
                r[f"{c} (%)"] = round(float(pct.loc[y, c]), 1) if tot[y] > 0 else np.nan
            rows.append(r)
    k = len(panels)
    lax = axes[k // ncol][k % ncol]
    lax.axis("off")
    lax.legend(handles=[Patch(color=colors[c]) for c in cats], labels=[f"{c}: {DAS_NAMES_LEGEND[c]}" if c in DAS_NAMES_LEGEND else c for c in cats],
               loc="center", fontsize=7, frameon=False, title="DAS category", title_fontsize=8)
    for j in range(k + 1, nrow * ncol):
        axes[j // ncol][j % ncol].axis("off")
    fig.supxlabel("Publication year", fontsize=8)
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.text(0.01, 0.005, f"Research articles with a DAS label. The first panel combines all {len(order)} journals. Years with fewer than {min_n} articles are not drawn. The latest year may be partial.", fontsize=7, va="top")
    _save(fig, figdir, "fig0_das_trend_by_journal", made)
    tables["Table0_das_by_journal_year"] = pd.DataFrame(rows)


DAS_ORDER_TEXT = ["P", "A", "N", "C", "R", "M"]   # 本文の表(tab:das_irr)の並び。基準 F は含まない


def _dname(x):
    n = DAS_NAMES_LEGEND.get(x, "")
    return f"{x}: {n}" if n else str(x)


def _das_order(vals):
    vals = [str(v) for v in vals]
    return [x for x in DAS_ORDER_TEXT if x in vals] + sorted(x for x in vals if x not in DAS_ORDER_TEXT)


def _rd_opt(path):
    return pd.read_csv(path) if os.path.exists(path) else None


def _fac_label(f):
    return "DAS category" if f == "DAS(類型)" else "Corr. author country" if f == "責任著者の国" else _en(f)


def _fig_shapley_both(plt, sc, sr, figdir, made, top=12):
    """RQ3: 因子別の Shapley 寄与(within-journal-year R²の割合)を被引用数と査読期間で並べる。因子の並びは共通"""
    c = sc[["factor", "share_of_within_r2"]].rename(columns={"share_of_within_r2": "c"})
    r = sr[["factor", "share_of_within_r2"]].rename(columns={"share_of_within_r2": "r"})
    m = c.merge(r, on="factor", how="outer")
    keep = set(m.nlargest(top, "c").factor) | set(m.nlargest(top, "r").factor) | {"DAS(類型)"}
    m = m[m.factor.isin(keep)].copy()
    m["mean"] = m[["c", "r"]].mean(axis=1)
    m = m.sort_values("mean").reset_index(drop=True)
    lab = [_fac_label(f) for f in m.factor]
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 0.25 * len(m) + 1.3), sharey=True)   # v059: 行の高さ 0.30→0.25 インチ
    for ax, col, ttl in ((axes[0], "c", "Citation count"), (axes[1], "r", "Peer review duration")):
        ax.barh(range(len(m)), m[col] * 100, color=["#c0504d" if l == "DAS category" else "#7f7f7f" for l in lab])
        ax.set_title(ttl)
        ax.set_xlabel("Share of within-journal-year R² (%, Shapley)")
    axes[0].set_yticks(range(len(m)))
    axes[0].set_yticklabels(lab, fontsize=8)
    fig.tight_layout()
    _save(fig, figdir, "fig4c_shapley_both", made)


def _fig_crude_adjusted(plt, ref, irrC, irrR, dsC, dsR, figdir, made):
    """RQ1・RQ2: 調整前(類型ごとの平均 ÷ F の平均)と調整後(NB の率比、95%区間)を並べる"""
    order = _das_order([v[4:] for v in irrC[irrC.group == G_DAS].variable])
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 0.40 * len(order) + 1.7), sharey=True)   # v059: 行の高さ 0.55→0.40 インチ
    for ax, irr_, ds, ttl in ((axes[0], irrC, dsC, "Citation count"), (axes[1], irrR, dsR, "Peer review duration")):
        t = irr_[irr_.group == G_DAS].copy()
        t["das"] = t.variable.str.replace("das_", "", regex=False)
        t = t.set_index("das")
        ds = ds.assign(das_label=ds.das_label.astype(str)).set_index("das_label")
        for i, x in enumerate(order):
            if x in ds.index and ref in ds.index and x in t.index:
                ax.plot(ds.loc[x, "mean"] / ds.loc[ref, "mean"], i - 0.13, "D", color="#c0504d", ms=5, label="Crude (ratio of means)" if i == 0 else None)
            if x in t.index and t.loc[x, "irr"] == t.loc[x, "irr"]:
                r = t.loc[x]
                ax.errorbar(r.irr, i + 0.13, xerr=[[r.irr - r.irr_low], [r.irr_high - r.irr]], fmt="o", ms=5, color="#1f4e79", capsize=3,
                            mfc="#1f4e79" if r.p_holm_cluster < 0.05 else "white", label="Adjusted (NB IRR, 95% CI)" if i == 0 else None)
        ax.axvline(1, color="gray", lw=0.8, ls="--")
        ax.set_yticks(range(len(order)))
        ax.set_yticklabels([_dname(x) for x in order], fontsize=8)
        ax.set_ylim(len(order) - 0.5, -0.5)
        ax.set_xlabel(f"Ratio vs DAS {ref} (log scale)")
        ax.set_title(ttl)
        ax.set_xscale("log")
        lo_, hi_ = ax.get_xlim()
        tk_ = [v for v in (0.3, 0.4, 0.5, 0.7, 0.85, 1.0, 1.2, 1.4, 1.7, 2.0, 3.0) if lo_ <= v <= hi_]
        ax.set_xticks(tk_)
        ax.set_xticklabels([f"{v:g}" for v in tk_])
        ax.set_xlim(lo_, hi_)
        ax.xaxis.set_minor_formatter(__import__("matplotlib").ticker.NullFormatter())
    # v034: 凡例を軸の外(図の下)に出す。M の行の記号と重ならない
    h_, l_ = axes[0].get_legend_handles_labels()
    fig.tight_layout(rect=(0, 0.10, 1, 1))
    fig.legend(h_, l_, frameon=False, fontsize=8, loc="lower center", ncol=2, bbox_to_anchor=(0.5, 0.0))
    fig.text(0.01, -0.01, "Crude: mean of the category divided by the mean of F, without adjustment. Adjusted: negative binomial model with journal and year fixed effects and covariates; filled: Holm-adjusted p < 0.05.", fontsize=7, va="top")
    _save(fig, figdir, "fig5c_crude_vs_adjusted", made)


def _rob_panel(ax, rob, order, lab, cols, ttl, ref):
    runs = [c[4:] for c in rob.columns if c.startswith("irr_")]
    rb = rob.assign(das=rob.das.astype(str)).set_index("das")
    done = set()
    for k, n in enumerate(runs):
        off = (k - (len(runs) - 1) / 2) * 0.17
        for i, x in enumerate(order):
            if x not in rb.index or rb.loc[x, f"irr_{n}"] != rb.loc[x, f"irr_{n}"]:
                continue
            r = rb.loc[x]
            ax.errorbar(r[f"irr_{n}"], i + off, xerr=[[r[f"irr_{n}"] - r[f"low_{n}"]], [r[f"high_{n}"] - r[f"irr_{n}"]]], fmt="o", ms=4, capsize=2,
                        color=cols[k % len(cols)], label=lab.get(n, n) if n not in done else None)
            done.add(n)
    ax.axvline(1, color="gray", lw=0.8, ls="--")
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([f"DAS {x}" for x in order])
    ax.set_ylim(len(order) - 0.5, -0.5)
    ax.set_xlabel(f"Incidence rate ratio vs DAS {ref} (log scale)")
    ax.set_title(ttl)
    _log_ticks(ax, None)
    ax.legend(frameon=False, fontsize=7, loc="best")


def _fig_robust_both(plt, robC, robR, ref, figdir, made):
    """頑健性: 被引用数(WoS・PMC × 固定効果)と査読期間(固定効果 2 通り)を 1 枚に"""
    order = _das_order(robC.das)
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 0.58 * len(order) + 1.6), sharey=True)   # v059: 行の高さ 0.8→0.58 インチ
    cols = ["#1f4e79", "#2e8b57", "#c0504d", "#e69f00"]
    _rob_panel(axes[0], robC, order, {"base": "WoS, journal+year FE (main)", "jy": "WoS, journal×year FE", "pmc": "PMC cited-by, journal+year FE", "pmc_jy": "PMC cited-by, journal×year FE"}, cols, "Citation count", ref)
    _rob_panel(axes[1], robR, order, {"base": "Journal+year FE (main)", "jy": "Journal×year FE"}, cols, "Peer review duration", ref)
    fig.tight_layout()
    _save(fig, figdir, "fig6c_robustness_both", made)


def _fig_journal_forest(plt, byj, ref, ttl, name, figdir, made):
    """雑誌別の率比を 95%区間つきで示す(類型ごとのパネル、雑誌が行)。塗り=Holm 補正後 p<0.05(雑誌×類型の全比較)
    v051: 6 パネルを 1 行ではなく 2 段×3 列に並べ、縦置きの紙の幅(約 6 インチ)に収めても文字が小さくならないようにした。
    図の大きさは約 6.6×7.6 インチで、文字は 7〜10 pt。雑誌名は各段の左端だけに出す。"""
    import matplotlib.ticker
    d = byj.copy()
    d["jn"] = list(jshort(d.journal, 34))
    d["das"] = d.das.astype(str)
    cats = _das_order(d.das.unique())
    js = sorted(d.jn.unique())
    lo = max(0.4, float(np.nanmin(d.irr_low))) if d.irr_low.notna().any() else 0.5
    hi = min(2.5, float(np.nanmax(d.irr_high))) if d.irr_high.notna().any() else 2.0
    ncol = 3
    nrow = int(math.ceil(len(cats) / ncol))
    fig_w = 6.6
    fig_h = nrow * (0.24 * len(js) + 0.95) + 1.1   # v059: 行の高さ 0.27→0.24 インチ
    fig, axes = plt.subplots(nrow, ncol, figsize=(fig_w, fig_h), sharey=True, sharex=True, squeeze=False)
    xmin_, xmax_ = lo * 0.97, hi * 1.03
    for k, ax in enumerate(axes.ravel()):
        if k >= len(cats):
            ax.set_visible(False)
            continue
        c = cats[k]
        for r in d[d.das == c].itertuples():
            if r.irr != r.irr:
                continue
            ax.errorbar(r.irr, js.index(r.jn), xerr=[[max(r.irr - r.irr_low, 0)], [max(r.irr_high - r.irr, 0)]], fmt="o", ms=3.8, capsize=1.8,
                        color="#1f4e79", mfc="#1f4e79" if r.p_holm_robust < 0.05 else "white")
        ax.axvline(1, color="gray", lw=0.8, ls="--")
        ax.set_xscale("log")
        ax.set_title(f"{c} vs {ref}", fontsize=10)
    axes[0, 0].set_ylim(len(js) - 0.5, -0.5)
    axes[0, 0].set_yticks(range(len(js)))
    for i in range(nrow):
        axes[i, 0].set_yticks(range(len(js)))
        axes[i, 0].set_yticklabels(js, fontsize=7.5)
    axes[0, 0].set_xlim(xmin_, xmax_)
    # v050: 目盛りは表示範囲の広さに合わせて選ぶ。1.0 を必ず入れ、優先順に、隣と対数で離れているものだけ足す(1 未満の側にも付ける)
    min_sep = 0.16 * math.log(xmax_ / xmin_)
    tk = []
    for v in (1.0, 0.8, 1.4, 2.0, 0.7, 0.5, 0.9, 1.2, 1.7):
        if xmin_ <= v <= xmax_ and all(abs(math.log(v / k)) >= min_sep for k in tk):
            tk.append(v)
    tk = sorted(tk)
    for ax in axes.ravel():
        if not ax.get_visible():
            continue
        ax.set_xticks(tk)
        ax.set_xticklabels([f"{v:g}" for v in tk], fontsize=8)
        ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
        ax.tick_params(axis="x", labelbottom=True)   # 上段にも目盛りの数字を出す
    fig.suptitle(f"Journal-specific rate ratios for {ttl}", fontsize=10.5, y=0.995)
    # 雑誌名が左の余白に入るよう、3 列の幅を同じにしたまま左を空ける(tight_layout は列幅が不揃いになるので使わない)
    fig.subplots_adjust(left=0.34, right=0.985, top=0.93 if nrow > 1 else 0.86, bottom=0.085, wspace=0.12, hspace=0.34)
    for i in range(nrow):
        pos = axes[i, 0].get_position()
        pos2 = axes[i, min(ncol, len(cats)) - 1].get_position()
        fig.text((pos.x0 + pos2.x1) / 2, pos.y0 - 0.052 * (7.6 / fig_h), f"Rate ratio vs DAS {ref} (log scale)", ha="center", va="top", fontsize=8.5)
    fig.text(0.01, 0.004, f"Bars: 95% CI (clipped at {lo * 0.97:.2f}-{hi * 1.03:.2f}). Filled: Holm-adjusted p < 0.05 over all journal x category comparisons. Blank: too few articles.", fontsize=7, va="bottom")
    _save(fig, figdir, name, made)


def main_figures(a):
    """v033: 本論の図(fig0・fig7・fig3 の 2 枚・fig4c・fig5c・fig6c)を PNG だけで作る。被引用数の実行と査読期間の実行(fig3 の査読期間版)の両方から"""
    import copy
    global _MAIN_ONLY
    _MAIN_ONLY = True
    try:
        ac = copy.copy(a)
        ac.dv = "wos_TC"
        paper_outputs(ac, os.path.expanduser(a.outdir))
        ar = copy.copy(a)
        ar.dv = "review_days"
        paper_outputs(ar, os.path.expanduser(a.paper_review_dir))
    finally:
        _MAIN_ONLY = False


def _fig6c_rob(a, outdir, rob_old):
    """v035: 頑健性の表(fig6c・補足の頑健性表)を、主モデルと同じ設定の 4 つの実行から組み立てる。
    base=主モデル(WoS・雑誌+年) / jy=WoS・雑誌×年(年齢の項なし) / pmc=PMC・雑誌+年 / pmc_jy=PMC・雑誌×年(PMC は WoS と同じ論文集合)。
    4 つがそろい、年齢の項(age_s*)がなければ組み立てた表を返す。そうでなければ従来の表を返し、主モデルとずれていれば警告する。"""
    root = os.path.dirname(os.path.expanduser(outdir).rstrip("/"))
    wjy = os.path.expanduser(a.fig6c_wos_jy) if a.fig6c_wos_jy else os.path.join(os.path.expanduser(outdir), "robustness_nospline", "jy")
    pmc = os.path.expanduser(a.fig6c_pmc) if a.fig6c_pmc else os.path.join(root, "analysis_pmc_samewos")
    pmcj = os.path.expanduser(a.fig6c_pmc_jy) if a.fig6c_pmc_jy else os.path.join(root, "analysis_pmc_samewos_jy")
    src = [("base", os.path.join(os.path.expanduser(outdir), "nb_irr_citations_wos_TC.csv")),
           ("jy", os.path.join(wjy, "nb_irr_citations_wos_TC.csv")),
           ("pmc", os.path.join(pmc, "nb_irr_citations_pmc_citedby_n.csv")),
           ("pmc_jy", os.path.join(pmcj, "nb_irr_citations_pmc_citedby_n.csv"))]
    main_irr = None
    tabs, why = {}, ""
    for n, f in src:
        if not os.path.exists(f):
            why = f"見つかりません: {f}"
            break
        t = pd.read_csv(f)
        if any(str(v).startswith("age_s") for v in t.variable):
            why = f"年齢の項(age_s*)が入っています(主モデルと設定が違う): {f}"
            break
        t = t[t.group == G_DAS].copy()
        t["das"] = t.variable.str.replace("das_", "", regex=False)
        tabs[n] = t.set_index("das")
    if not why:
        classes = list(tabs["base"].index)
        comp = pd.DataFrame({"das": classes})
        for n, _ in src:
            t = tabs[n].reindex(classes)
            comp[f"irr_{n}"], comp[f"low_{n}"], comp[f"high_{n}"], comp[f"p_holm_{n}"] = t.irr.values, t.irr_low.values, t.irr_high.values, t.p_holm_cluster.values
        od = os.path.join(os.path.expanduser(outdir), "robustness_fig6c")
        os.makedirs(od, exist_ok=True)
        comp.to_csv(os.path.join(od, "robustness_das_overall.csv"), index=False, encoding="utf-8-sig")
        print(f"[頑健性] 主モデルと同じ設定の 4 つの実行から組み立てました → {od}/robustness_das_overall.csv", file=sys.stderr)
        prov = []       # v037: どの出力から作ったか(N・クラスタ数)を残す。PMC が 648,217 件なら WoS と同じ論文集合、655,860 件なら全 PMC
        for (n, f), (_, d, _, fm) in zip(src, _fig6c_sources(a, outdir)[:4]):
            r = dict(series=n, irr_csv=f)
            if os.path.exists(fm):
                m = pd.read_csv(fm).iloc[0]
                r.update(n=int(m["n"]), n_clusters=int(m["n_clusters"]), fe=str(m["fe"]))
            prov.append(r)
        pd.DataFrame(prov).to_csv(os.path.join(od, "robustness_fig6c_provenance.csv"), index=False, encoding="utf-8-sig")
        print("[頑健性] 各系列の N: " + " / ".join(f"{r['series']} {r.get('n', '?'):,}" if 'n' in r else f"{r['series']} ?" for r in prov), file=sys.stderr)
        return comp
    print(f"[頑健性] 4 つの実行をそろえられませんでした({why})。従来の robustness_das_overall.csv を使います", file=sys.stderr)
    if rob_old is not None and len(rob_old) and os.path.exists(src[0][1]):
        m = pd.read_csv(src[0][1])
        m = m[m.group == G_DAS].copy()
        m["das"] = m.variable.str.replace("das_", "", regex=False)
        m = m.set_index("das").irr
        d = (rob_old.set_index("das").irr_base - m.reindex(rob_old.das).values).abs()
        if d.max() > 0.002:
            print(f"[警告] 頑健性の表の主モデル列が、主モデルの率比と最大 {d.max():.3f} ずれています。頑健性が古い実行か、別の設定(年齢の項など)の可能性があります。"
                  "図と本文の表がずれるので、--robustness-only で作り直すか、--fig6c-* で出力を指定してください", file=sys.stderr)
    return rob_old


def _fig6c_sources(a, outdir):
    """v037: fig6c・頑健性の表(表 5)の 4 系列の出力フォルダ。(系列名, nb_irr の CSV, nb_model の CSV) の一覧を返す"""
    root = os.path.dirname(os.path.expanduser(outdir).rstrip("/"))
    wjy = os.path.expanduser(a.fig6c_wos_jy) if a.fig6c_wos_jy else os.path.join(os.path.expanduser(outdir), "robustness_nospline", "jy")
    pmc = os.path.expanduser(a.fig6c_pmc) if a.fig6c_pmc else os.path.join(root, "analysis_pmc_samewos")
    pmcj = os.path.expanduser(a.fig6c_pmc_jy) if a.fig6c_pmc_jy else os.path.join(root, "analysis_pmc_samewos_jy")
    full = os.path.expanduser(a.fig6c_pmc_full) if a.fig6c_pmc_full else os.path.join(root, "analysis_pmc")
    o = os.path.expanduser(outdir)
    spec = [("WoS・雑誌+年(主モデル)", o, "wos_TC"), ("WoS・雑誌×年", wjy, "wos_TC"),
            ("PMC・雑誌+年(fig6c が読む)", pmc, "pmc_citedby_n"), ("PMC・雑誌×年(fig6c が読む)", pmcj, "pmc_citedby_n"),
            ("PMC・雑誌+年(WoS 照合なしを含む全 PMC。比較用)", full, "pmc_citedby_n")]
    return [(n, d, os.path.join(d, f"nb_irr_citations_{t}.csv"), os.path.join(d, f"nb_model_citations_{t}.csv")) for n, d, t in spec]


def check_fig6c(a):
    """v037: 表 5・fig6c の PMC 列が、WoS と同じ論文集合(648,217 件)の実行から作られたのか、全 PMC(655,860 件)の実行なのかを確かめる。
    回帰は走らせず、保存済みの nb_model_*.csv(N・クラスタ数)と nb_irr_*.csv(DAS の率比・Holm p)を読んで並べる。
    表 5 の PMC 列(論文の値: P 0.98 (0.319)、C 1.01 (0.614)、M 1.03 (0.471))と、どのフォルダの値が一致するかを示す"""
    outdir = os.path.expanduser(a.outdir)
    paper = {"P": 0.319, "C": 0.614, "M": 0.471}
    rows = []
    print("\n[fig6c・表 5 の PMC 列の標本の確認]  N が 648,217 なら WoS と同じ論文集合、655,860 なら全 PMC")
    for name, d, fi, fm in _fig6c_sources(a, outdir):
        r = dict(series=name, folder=d, irr_csv=fi, irr_exists=os.path.exists(fi), model_csv=fm, model_exists=os.path.exists(fm))
        if os.path.exists(fm):
            m = pd.read_csv(fm).iloc[0]
            r.update(n=int(m["n"]), n_clusters=int(m["n_clusters"]), fe=str(m["fe"]), version=str(m.get("version", "")))
        if os.path.exists(fi):
            t = pd.read_csv(fi)
            r["has_age_term"] = any(str(v).startswith("age_s") for v in t.variable)
            t = t[t.group == G_DAS].copy()
            t["das"] = t.variable.str.replace("das_", "", regex=False)
            t = t.set_index("das")
            for k in ("P", "A", "N", "C", "R", "M"):
                if k in t.index:
                    r[f"irr_{k}"] = float(t.loc[k, "irr"])
                    r[f"holm_{k}"] = float(t.loc[k, "p_holm_cluster"])
        rows.append(r)
        print(f"\n  {name}\n    フォルダ {d}")
        if not r["irr_exists"]:
            print("    nb_irr の CSV がありません")
            continue
        print(f"    N = {r.get('n', '?'):,}  クラスタ {r.get('n_clusters', '?')}  FE = {r.get('fe', '?')}  年齢の項 {'あり' if r.get('has_age_term') else 'なし'}" if 'n' in r else "    nb_model の CSV がありません(N は不明)")
        print("    Holm p  " + "  ".join(f"{k} {r[f'holm_{k}']:.3f}" for k in ("P", "A", "N", "C", "R", "M") if f"holm_{k}" in r))
        hit = [k for k, v in paper.items() if f"holm_{k}" in r and abs(r[f"holm_{k}"] - v) < 0.0005]
        if "PMC" in name and hit:
            print(f"    → 表 5 の PMC 列の値(P 0.319・C 0.614・M 0.471)と一致する類型: {', '.join(hit)}")
    df = pd.DataFrame(rows)
    f = os.path.join(outdir, "check_fig6c_sources.csv")
    df.to_csv(f, index=False, encoding="utf-8-sig")
    print(f"\n[保存] {f}")
    print("読み方: 表 5 の PMC 列と Holm p が一致するのが「WoS と同じ論文集合」のフォルダなら、図 6c のキャプションは正しい。"
          "「全 PMC」のフォルダと一致するなら、図 6c のキャプション(same articles)を直すか、fig6c を WoS と同じ論文集合の実行から作り直す")


def paper_outputs(a, outdir):
    global _PAPER_SFX
    plt = _paper_plt()
    pdir = os.path.expanduser(a.paper_dir or DEFAULT_PAPER)
    figdir, tabdir = os.path.join(pdir, "figures_main" if _MAIN_ONLY else "figures"), os.path.join(pdir, "tables")
    os.makedirs(figdir, exist_ok=True)
    os.makedirs(tabdir, exist_ok=True)
    tag = _tag(a.dv) + ("_with_review" if a.review_as_iv and not _is_rv(a.dv) else "")
    rv = _is_rv(a.dv)
    _PAPER_SFX = "_review" if rv else ""
    OUT = "Peer review duration" if rv else "Citation count"
    ref = a.das_ref
    made, tables, skipped = [], {}, []

    def rd(name, folder=outdir):
        f = os.path.join(folder, name)
        if os.path.exists(f):
            return pd.read_csv(f)
        skipped.append(name)
        return None

    irr = rd(f"nb_irr_{_tag(a.dv)}.csv")
    byj = rd("nb_by_journal.csv")
    shap = rd(f"shapley_factor_{tag}.csv")
    dsum = rd("desc_das_citation_summary.csv")
    jcount = rd("desc_journal_das_counts.csv")
    wald = rd(f"nb_wald_{_tag(a.dv)}.csv")
    lrt = rd(f"nb_lrt_{_tag(a.dv)}.csv")
    rob_dir = os.path.expanduser(a.robust_outroot) if a.robust_outroot else os.path.join(outdir, "robustness")
    rob = rd("robustness_das_overall.csv", rob_dir)
    if not rv:
        rob = _fig6c_rob(a, outdir, rob)

    # ---- 図 1: DAS 類型の率比(雑誌をまとめた NB)
    if irr is not None:
        t = irr[irr.group == G_DAS].copy()
        if len(t):
            t["das"] = t.variable.str.replace("das_", "", regex=False)
            t = t.sort_values("irr").reset_index(drop=True)
            fig, ax = plt.subplots(figsize=(6.0, 0.55 * len(t) + 1.3))
            for i, r in t.iterrows():
                sig = r.p_holm_cluster < 0.05
                ax.errorbar(r.irr, i, xerr=[[r.irr - r.irr_low], [r.irr_high - r.irr]], fmt="o", color="#1f4e79", capsize=3,
                            mfc="#1f4e79" if sig else "white")
                ax.text(1.02, i, f"{r.irr:.2f} [{r.irr_low:.2f}, {r.irr_high:.2f}] {_stars(r.p_holm_cluster)}", transform=ax.get_yaxis_transform(),
                        va="center", fontsize=8)
            ax.axvline(1, color="gray", lw=0.8, ls="--")
            ax.set_yticks(range(len(t)))
            ax.set_yticklabels([_dname(r.das) for r in t.itertuples()])
            ax.set_xlabel(f"{'Rate ratio of days' if rv else 'Incidence rate ratio'} vs DAS {ref} (log scale)")
            ax.set_title(f"{OUT} by data availability statement category")
            _log_ticks(ax, t.irr)
            ax.annotate("Filled: Holm-adjusted p < 0.05 (cluster-robust). Bars: 95% CI. NB model, journal and year fixed effects.", xy=(0, 0), xycoords="axes fraction", xytext=(0, -42), textcoords="offset points", fontsize=7, annotation_clip=False)
            _save(fig, figdir, "fig1_das_irr_forest", made)
        # ---- 図 2: 共変量の率比
        c = irr[irr.group != G_DAS].copy()
        if len(c):
            c["label"] = [_en(v) for v in c.variable]
            c = c.sort_values("irr").reset_index(drop=True)
            fig, ax = plt.subplots(figsize=(6.4, 0.26 * len(c) + 1.2))
            for i, r in c.iterrows():
                sig = r.p_holm_all_cluster < 0.05
                ax.errorbar(r.irr, i, xerr=[[r.irr - r.irr_low], [r.irr_high - r.irr]], fmt="o", ms=4, color="#444444", capsize=2, mfc="#444444" if sig else "white")
            ax.axvline(1, color="gray", lw=0.8, ls="--")
            ax.set_yticks(range(len(c)))
            ax.set_yticklabels(c.label, fontsize=8)
            ax.set_xlabel("Incidence rate ratio (continuous: per 1 SD; binary: 0→1; log scale)")
            ax.set_title(f"Covariates in the {OUT.lower()} model")
            _log_ticks(ax, c.irr)
            ax.annotate("Filled: Holm-adjusted p < 0.05 over all coefficients. Bars: 95% CI (cluster-robust).", xy=(0, 0), xycoords="axes fraction", xytext=(0, -42), textcoords="offset points", fontsize=7, annotation_clip=False)
            _save(fig, figdir, "fig2_covariate_irr_forest", made)

    # ---- 図 3: 雑誌×類型の率比(ヒートマップ)
    if byj is not None and len(byj):
        jn = dict(zip(byj.journal.unique(), jshort(pd.Series(byj.journal.unique()), 34)))
        piv = byj.pivot(index="journal", columns="das", values="irr")
        ph = byj.pivot(index="journal", columns="das", values="p_holm_robust")
        piv = piv.reindex(sorted(piv.index, key=lambda x: jn[x]))
        ph = ph.reindex(piv.index)
        lg = np.log(piv.values.astype(float))
        vmax = max(0.3, np.nanpercentile(np.abs(lg), 95))
        fig, ax = plt.subplots(figsize=(1.1 * piv.shape[1] + 3.5, 0.34 * piv.shape[0] + 1.4))
        im = ax.imshow(lg, cmap="RdBu_r", vmin=-vmax, vmax=vmax, aspect="auto")
        for i in range(piv.shape[0]):
            for j in range(piv.shape[1]):
                v = piv.values[i, j]
                if v == v:
                    ax.text(j, i, f"{v:.2f}{_stars(ph.values[i, j])}", ha="center", va="center", fontsize=7, color="white" if abs(lg[i, j]) > 0.6 * vmax else "black")
        ax.set_xticks(range(piv.shape[1]))
        ax.set_xticklabels([f"{c} vs {ref}" for c in piv.columns])
        ax.set_yticks(range(piv.shape[0]))
        ax.set_yticklabels([jn[j] for j in piv.index], fontsize=7)
        ax.spines[:].set_visible(False)
        cb = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02)
        tk_ = [v for v in (0.7, 0.75, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4) if abs(math.log(v)) <= vmax + 1e-9]
        cb.set_ticks([math.log(v) for v in tk_])
        cb.set_ticklabels([f"{v:g}" for v in tk_])
        cb.set_label("Rate ratio (colour scale is logarithmic)")
        ax.set_title(f"DAS category association with {OUT.lower()}, by journal (rate ratio)")
        ax.annotate("Holm-adjusted p over all journal × category comparisons (robust SE): * < 0.05, ** < 0.01, *** < 0.001. Blank: too few articles.", xy=(0, 0), xycoords="axes fraction", xytext=(0, -28), textcoords="offset points", fontsize=7, annotation_clip=False)
        _save(fig, figdir, "fig3_das_irr_by_journal_heatmap", made)

    # ---- 図 4: 因子別の寄与(Shapley)
    if shap is not None and len(shap):
        s = shap.sort_values("shapley_r2", ascending=False).head(15).iloc[::-1]
        lab = [("DAS category" if f == "DAS(類型)" else "Corr. author country" if f == "責任著者の国" else _en(f)) for f in s.factor]
        fig, ax = plt.subplots(figsize=(5.6, 0.3 * len(s) + 1.2))
        ax.barh(lab, s.share_of_within_r2 * 100, color=["#c0504d" if "DAS" in l else "#7f7f7f" for l in lab])
        ax.set_xlabel("Share of within-journal-year R² (%, Shapley)")
        ax.set_title(f"Contribution of factors to log {OUT.lower()} (OLS)")
        _save(fig, figdir, "fig4_shapley_factors", made)

    # ---- 図 5: DAS 類型ごとの被引用数の分布の要約
    if dsum is not None and len(dsum):
        s = dsum.sort_values("median", ascending=False).reset_index(drop=True)
        fig, ax = plt.subplots(figsize=(6.4, 3.4))
        ax.errorbar(range(len(s)), s["median"], yerr=[s["median"] - s.q1, s.q3 - s["median"]], fmt="o", color="#1f4e79", capsize=3, label="Median (IQR)")
        ax.plot(range(len(s)), s["mean"], "D", color="#c0504d", ms=4, label="Mean")
        ax.set_xticks(range(len(s)))
        ax.set_xticklabels([f"{r.das_label}\nn={int(r.n):,}" for r in s.itertuples()], fontsize=7)
        ax.set_ylabel("Days from receipt to acceptance" if rv else "Citation count")
        ax.legend(frameon=False)
        ax.set_title(f"{OUT} by DAS category (unadjusted)")
        _save(fig, figdir, "fig5_outcome_by_das_summary", made)

    # ---- 図 6: 頑健性(設定を変えた率比)
    if rob is not None and len(rob):
        runs = [c[4:] for c in rob.columns if c.startswith("irr_")]
        lab = {"base": ("Journal+year FE (main)" if rv else "WoS, journal+year FE (main)"), "jy": ("Journal×year FE" if rv else "WoS, journal×year FE"), "pmc": "PMC cited-by, journal+year FE", "pmc_jy": "PMC cited-by, journal×year FE"}
        cols = ["#1f4e79", "#2e8b57", "#c0504d", "#e69f00"]
        fig, ax = plt.subplots(figsize=(6.2, 0.9 * len(rob) + 1.4))
        for k, n in enumerate(runs):
            off = (k - (len(runs) - 1) / 2) * 0.16
            y = np.arange(len(rob)) + off
            ax.errorbar(rob[f"irr_{n}"], y, xerr=[rob[f"irr_{n}"] - rob[f"low_{n}"], rob[f"high_{n}"] - rob[f"irr_{n}"]], fmt="o", ms=4,
                        capsize=2, color=cols[k % 4], label=lab.get(n, n))
        ax.axvline(1, color="gray", lw=0.8, ls="--")
        ax.set_yticks(range(len(rob)))
        ax.set_yticklabels([f"DAS {d}" for d in rob.das])
        ax.invert_yaxis()
        ax.set_xlabel(f"Incidence rate ratio vs DAS {ref} (log scale)")
        _log_ticks(ax, None)
        ax.legend(frameon=False, fontsize=7, loc="best")
        ax.set_title("Robustness of DAS category associations")
        _save(fig, figdir, "fig6_robustness_irr", made)

    # ---- 図 0: DAS カテゴリの年次変化(雑誌別)。分析の出力は使わず CSV から直接作る(被引用数の実行のときだけ)
    if not rv:
        try:
            _das_trend(a, plt, figdir, made, tables)
        except Exception as e:
            print(f"[論文用の図] DAS の年次変化は作れませんでした({type(e).__name__}: {e})", file=sys.stderr)

    # ---- 図 7: 被引用数と査読期間の並置(両方の出力があるとき。--dv wos_TC の --paper-only/--paper-figs で作る)
    rvdir = os.path.expanduser(a.paper_review_dir)
    f_rv = os.path.join(rvdir, "nb_irr_review_days.csv")
    if not rv and irr is not None and os.path.exists(f_rv):
        r2 = pd.read_csv(f_rv)
        order7 = _das_order([v[4:] for v in irr[irr.group == G_DAS].variable])
        fig, axes = plt.subplots(1, 2, figsize=(9.6, 0.36 * max(1, len(order7)) + 1.5), sharey=True)   # v059: 行の高さ 0.55→0.36 インチ
        for ax, tb, ttl in ((axes[0], irr, "Citation count"), (axes[1], r2, "Peer review duration")):
            t = tb[tb.group == G_DAS].copy()
            t["das"] = t.variable.str.replace("das_", "", regex=False)
            t = t.set_index("das").reindex(order7).reset_index()
            for i, r in t.iterrows():
                if r.irr != r.irr:
                    continue
                sig = r.p_holm_cluster < 0.05
                ax.errorbar(r.irr, i, xerr=[[r.irr - r.irr_low], [r.irr_high - r.irr]], fmt="o", color="#1f4e79", capsize=3, mfc="#1f4e79" if sig else "white")
            ax.axvline(1, color="gray", lw=0.8, ls="--")
            ax.set_yticks(range(len(order7)))
            ax.set_yticklabels([_dname(x) for x in order7], fontsize=8)
            ax.set_ylim(len(order7) - 0.5, -0.5)
            ax.set_xlabel(f"Rate ratio vs DAS {ref} (log scale)")
            ax.set_title(ttl)
            _log_ticks(ax, None)
        fig.suptitle("DAS category associations with citations and review duration", fontsize=10)
        fig.tight_layout()
        _save(fig, figdir, "fig7_citations_vs_review_irr", made)
        tabs_extra = {"Table7_review_NB_IRR": pd.DataFrame({"Variable": [_en(v) for v in r2.variable], "IRR (95% CI)": [f"{r.irr:.2f} ({r.irr_low:.2f}–{r.irr_high:.2f})" for r in r2.itertuples()],
                      "p (cluster-robust)": [_fp(p) for p in r2.p_cluster], "p (Holm, DAS family)": [_fp(p) for p in r2.p_holm_cluster]})}
        tables.update(tabs_extra)

    # ---- v032: 被引用数と査読期間を並べる図(査読期間の出力があるとき)と、雑誌別の区間つき図
    if not rv:
        def _try(fn, label):
            try:
                fn()
            except Exception as e:
                print(f"[論文用の図] {label}は作れませんでした({type(e).__name__}: {e})", file=sys.stderr)
        irrR = _rd_opt(f_rv)
        shapR = _rd_opt(os.path.join(rvdir, "shapley_factor_review_days.csv"))
        dsR = _rd_opt(os.path.join(rvdir, "desc_das_citation_summary.csv"))
        robR = _rd_opt(os.path.join(rvdir, "robustness", "robustness_das_overall.csv"))
        byjR = _rd_opt(os.path.join(rvdir, "nb_by_journal.csv"))
        if shap is not None and shapR is not None:
            _try(lambda: _fig_shapley_both(plt, shap, shapR, figdir, made), "fig4c(Shapley の並置)")
        else:
            skipped.append("fig4c: shapley_factor_review_days.csv")
        if irr is not None and irrR is not None and dsum is not None and dsR is not None:
            _try(lambda: _fig_crude_adjusted(plt, ref, irr, irrR, dsum, dsR, figdir, made), "fig5c(調整前後の比較)")
        else:
            skipped.append("fig5c: desc_das_citation_summary.csv(査読期間)")
        if rob is not None and robR is not None:
            _try(lambda: _fig_robust_both(plt, rob, robR, ref, figdir, made), "fig6c(頑健性の並置)")
        else:
            skipped.append("fig6c: robustness/robustness_das_overall.csv(査読期間)")
        if byj is not None and len(byj):
            _try(lambda: _fig_journal_forest(plt, byj, ref, "citation count", "fig8_journal_forest", figdir, made), "fig8(雑誌別・被引用数)")
        if byjR is not None and len(byjR):
            _try(lambda: _fig_journal_forest(plt, byjR, ref, "peer review duration", "fig8_journal_forest_review", figdir, made), "fig8(雑誌別・査読期間)")

    if _MAIN_ONLY:   # v033: 本論の図だけ。表・補足表は作らない
        print(f"[本論の図] {', '.join(made) if made else 'なし'} → {figdir}")
        sk = [x for x in skipped if x.startswith("fig") or x.startswith(("nb_irr", "nb_by_journal", "shapley_factor", "desc_das_citation_summary", "robustness_das_overall"))]
        if sk:
            print("  本論の図に必要で、見つからなかった入力: " + ", ".join(sk))
        return
    # ---- 表
    if jcount is not None:
        t = jcount.rename(columns={jcount.columns[0]: "Journal"})
        tables["Table1_journal_by_DAS_counts"] = t
    if dsum is not None:
        t = dsum.rename(columns={"das_label": "DAS category", "n": "N", "mean": "Mean", "median": "Median", "q1": "Q1", "q3": "Q3",
                                 "mean_pct_in_journal_year": "Mean within journal-year percentile"}).round(3)
        tables["Table2_outcome_by_DAS"] = t
    if irr is not None:
        t = pd.DataFrame({"Variable": [_en(v) for v in irr.variable], "Group": [EN_GROUP.get(g, g) for g in irr.group], "Scale": irr.scale,
                          "IRR (95% CI)": [f"{r.irr:.2f} ({r.irr_low:.2f}–{r.irr_high:.2f})" for r in irr.itertuples()],
                          "p (cluster-robust)": [_fp(p) for p in irr.p_cluster],
                          "p (Holm, DAS family)": [_fp(p) for p in irr.p_holm_cluster],
                          "p (Holm, all)": [_fp(p) for p in irr.p_holm_all_cluster]})
        tables["Table3_NB_IRR"] = t
    if wald is not None:
        t = wald.copy()
        t["group"] = [EN_GROUP.get(g, g) for g in t.group]
        tables["Table4a_NB_Wald_tests"] = t.round(4)
    if lrt is not None:
        t = lrt.drop(columns=[c for c in ("llf_full", "llf_reduced") if c in lrt]).copy()
        t["block"] = [("DAS category" if b == "DAS(類型)" else "Corr. author country" if b == "責任著者の国" else EN_GROUP.get(b, _en(b))) for b in t.block]
        tables["Table4b_NB_LRT_importance"] = t.round(4)
    if byj is not None:
        t = byj[["journal", "das", "n_class", "irr", "irr_low", "irr_high", "p_robust", "p_holm_robust"]].copy()
        t["journal"] = jshort(t.journal, 34)
        t["IRR (95% CI)"] = [f"{r.irr:.2f} ({r.irr_low:.2f}–{r.irr_high:.2f})" for r in t.itertuples()]
        t["p (robust)"] = [_fp(p) for p in t.p_robust]
        t["p (Holm)"] = [_fp(p) for p in t.p_holm_robust]
        tables["Table5_NB_by_journal"] = t[["journal", "das", "n_class", "IRR (95% CI)", "p (robust)", "p (Holm)"]].rename(
            columns={"journal": "Journal", "das": "DAS category", "n_class": "N in category"})
    if rob is not None:
        runs = [c[4:] for c in rob.columns if c.startswith("irr_")]
        t = pd.DataFrame({"DAS category": rob.das})
        for n in runs:
            t[f"{n}: IRR (95% CI)"] = [f"{r[f'irr_{n}']:.2f} ({r[f'low_{n}']:.2f}–{r[f'high_{n}']:.2f})" for _, r in rob.iterrows()]
            t[f"{n}: p (Holm)"] = [_fp(p) for p in rob[f"p_holm_{n}"]]
        tables["Table6_robustness"] = t
    for k, t in tables.items():
        kk = k if k.startswith(("Table0", "Table7")) else k + _PAPER_SFX
        t.to_csv(os.path.join(tabdir, kk + ".csv"), index=False, encoding="utf-8-sig")
    try:   # フォルダにある表の CSV を、1 つの xlsx にまとめる(被引用数・査読期間の両方が入る)
        with pd.ExcelWriter(os.path.join(tabdir, "paper_tables.xlsx")) as w:
            used = set()
            for f in sorted(x for x in os.listdir(tabdir) if x.endswith(".csv")):
                nm, i = f[:-4][:31], 1
                while nm in used:
                    nm, i = f[:-4][:28] + f"_{i}", i + 1
                used.add(nm)
                pd.read_csv(os.path.join(tabdir, f), encoding="utf-8-sig").to_excel(w, sheet_name=nm, index=False)
    except Exception as e:
        print(f"[論文用の表] xlsx は作りませんでした({type(e).__name__})。CSV は保存済みです", file=sys.stderr)
    print(f"\n[論文用の図表] 図 {len(made)} 点: {', '.join(made) if made else 'なし'} / 表 {len(tables)} 点 → {pdir}")
    if skipped:
        print("  見つからなかった入力(該当する図表は作っていません): " + ", ".join(skipped))
        print("  先に通常の分析(--robustness も含めたい場合は --robustness)を実行してください")
    try:
        supplementary_tables(a, outdir, pdir)
    except Exception as e:
        print(f"[補足表] 作れませんでした({type(e).__name__}: {e})", file=sys.stderr)


# ----------------------------------------------------------------------------- Supplementary Table S1・S2(v011)
SUPP_TITLE = "Data Availability Statement Categories in Relation to Citation Counts and Peer Review Duration: An Observational Study of Open-Access Articles"
SUPP_WOS_DATE = "June 2026"   # 被引用数を取得した時期(脚注の Outcome に書く)。取得し直したら直す
SUPP_DAS = dict(DAS_NAMES_LEGEND)   # 付表の類型の名称。論文の表2と同じ(図の凡例 DAS_NAMES_LEGEND と共通にして、名称がずれないようにする)
SUPP_GROUP = {"著者・国・共著": "Authors, countries, collaboration", "参考文献・助成": "References and funding",
              "図表・文章量": "Figures, tables, and text length", "題名": "Title features",
              "責任著者の国": "Corresponding author’s country (reference: other countries)", "査読期間": "Review duration"}


def _tex(x):
    for k, v in (("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("_", r"\_"), ("#", r"\#"), ("$", r"\$")):
        x = x.replace(k, v)
    return x


def _supp_p(p):
    if p != p:
        return ""
    return r"$<$0.001" if p < 0.001 else f"{p:.3f}"


def _supp_info(folder, tag):
    """主モデルの N・クラスタ数・FE。nb_model_<tag>.csv(v011 以降)がなければ summary.txt から読む。読めなければ None"""
    f = os.path.join(folder, f"nb_model_{tag}.csv")
    if os.path.exists(f):
        r = pd.read_csv(f).iloc[0]
        return {"n": int(r["n"]), "k": int(r["n_clusters"]), "fe": str(r["fe"]), "nb_sample": int(r.get("nb_sample", 0)), "src": "nb_model"}
    f = os.path.join(folder, "summary.txt")
    if os.path.exists(f):
        t = open(f, encoding="utf-8").read()
        m1 = re.search(r"\[NB\] 分析対象 ([\d,]+) 行.*?FE=(\w+)", t)
        m2 = re.search(r"クラスタ数 (\d+)", t)
        if m1 and m2:
            return {"n": int(m1.group(1).replace(",", "")), "k": int(m2.group(1)), "fe": m1.group(2), "nb_sample": 0, "src": "summary.txt"}
    return None


def _supp_table(irr, info, caption, label, ref, outcome):
    n_das = int((irr.group == G_DAS).sum())
    w = r"p{6.2cm}@{\hspace{4pt}}l@{\hspace{4pt}}c@{\hspace{4pt}}c@{\hspace{4pt}}c"
    head = "Variable & Scale & IRR (95\\% CI) & $p$ & Holm $p$ \\\\"
    fe = "journal and publication-year fixed effects" if info and info["fe"] == "additive" else "journal-by-year fixed effects"
    size = (f"; N = {info['n']:,} articles in {info['k']} journal-by-year groups" if info else "")
    note = (f"Negative binomial (NB2) models with {fe}{size}. IRR: incidence rate ratio with 95\\% confidence interval based on standard errors "
            f"clustered by journal-by-year group. Continuous covariates are standardized (IRR per 1 SD) after the transformation described in Section 2.4; "
            f"binary covariates are 0-to-1 contrasts. $p$: cluster-robust $p$-value. Holm $p$: Holm-adjusted $p$-value over the {_NUMW.get(n_das, n_das)} DAS comparisons "
            f"(DAS rows) or over all {len(irr)} coefficients, including the DAS rows (other rows). Outcome: {outcome}")
    L = [rf"\begin{{longtable}}{{{w}}}", rf"\caption{{{caption}}}\label{{{label}}}\\", r"\toprule", head, r"\midrule", r"\endfirsthead",
         r"\multicolumn{5}{l}{\small\textit{Supplementary Table \thetable\ (continued)}}\\", r"\toprule", head, r"\midrule", r"\endhead",
         r"\midrule", r"\multicolumn{5}{r}{\small\textit{Continued on next page}}\\", r"\endfoot", r"\bottomrule",
         r"\multicolumn{5}{p{14.8cm}}{\footnotesize " + note + r"}\\", r"\endlastfoot"]
    if not info:
        L.insert(0, "% CHECK: N and the number of clusters were not found (nb_model_*.csv / summary.txt); add them to the table note.")
    for g in dict.fromkeys(irr.group):
        t = irr[irr.group == g]
        isd = g == G_DAS
        gl = f"DAS category (reference: {ref})" if isd else SUPP_GROUP.get(g, EN_GROUP.get(g, g))
        L.append(rf"\multicolumn{{5}}{{l}}{{\textit{{{_tex(gl)}}}}} \\")
        for r in t.itertuples():
            if isd:
                k = r.variable.replace("das_", "")
                nm = f"{k}: {SUPP_DAS.get(k, '')}".rstrip(": ")
            else:
                nm = _en(r.variable)
            ph = r.p_holm_cluster if isd else r.p_holm_all_cluster
            sc = r.scale.replace("→", r"$\to$")
            L.append(rf"\quad {_tex(nm)} & {sc} & {r.irr:.3f} ({r.irr_low:.3f}--{r.irr_high:.3f}) & {_supp_p(r.p_cluster)} & {_supp_p(ph)} \\")
    L.append(r"\end{longtable}")
    return "\n".join(L)


_NUMW = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight"}


def supplementary_tables(a, outdir, pdir):
    """Supplementary Table S1(被引用数)・S2(査読期間)を tex で作る。入力は保存済みの nb_irr_*.csv と nb_model_*.csv"""
    rv = _is_rv(a.dv)
    cdir = os.path.expanduser(a.paper_citation_dir) if rv else outdir
    rdir = outdir if rv else os.path.expanduser(a.paper_review_dir)
    specs = [("S1", cdir, "citations_wos_TC", "Complete negative binomial estimates for WoS citation counts.", "tab:s1",
              f"Web of Science Times Cited ({SUPP_WOS_DATE})."),
             ("S2", rdir, "review_days", "Complete negative binomial estimates for peer review duration.", "tab:s2",
              "days from receipt to acceptance; an IRR below 1 means a shorter expected review duration.")]
    blocks, made = [], []
    for sid, folder, tag, cap, lab, outcome in specs:
        f = os.path.join(folder, f"nb_irr_{tag}.csv")
        if not os.path.exists(f):
            print(f"[補足表] {sid}: {f} がないため作りません(先に該当の分析を実行してください)", file=sys.stderr)
            continue
        info = _supp_info(folder, tag)
        if info and info["fe"] != "additive":
            print(f"[補足表] {sid}: {folder} の出力は固定効果が {info['fe']}(雑誌×年)で、主モデル(additive)ではありません。"
                  f"主モデルの出力フォルダ(通常は robustness の外)を指定してください。{sid} は作りません", file=sys.stderr)
            continue
        if info is None:
            print(f"[補足表] {sid}: N・クラスタ数が nb_model_{tag}.csv にも summary.txt にもありません。v011 で主モデルを走らせ直すと保存されます。脚注の N は空にして % CHECK を入れます", file=sys.stderr)
        elif info["nb_sample"]:
            print(f"[補足表] {sid}: --nb-sample による一部の行の結果です。論文には全行の結果を使ってください", file=sys.stderr)
        irr = pd.read_csv(f)
        if "p_holm_all_cluster" not in irr.columns:
            print(f"[補足表] {sid}: {f} に p_holm_all_cluster 列がありません(v001 以降の出力が必要)", file=sys.stderr)
            continue
        blocks.append(_supp_table(irr, info, cap, lab, a.das_ref, outcome))
        made.append(sid)
    if not blocks:
        return
    pre = "\n".join([r"\documentclass[10pt,a4paper]{article}", r"\usepackage[margin=2.2cm]{geometry}", r"\usepackage{longtable,booktabs,amsmath}",
                     r"\renewcommand{\tablename}{Supplementary Table}", r"\renewcommand{\thetable}{S\arabic{table}}", r"\begin{document}",
                     r"\begin{center}{\large\bfseries Supplementary tables}\\[2pt]", _tex(SUPP_TITLE) + r"\end{center}", r"\vspace{1em}"])
    if made == ["S2"]:
        pre += "\n" + r"\setcounter{table}{1}"   # S2 だけ作るときも番号は S2 のまま
    doc = pre + "\n" + "\n\n\\clearpage\n".join(blocks) + "\n\n\\end{document}\n"
    sdir = os.path.join(pdir, "supplementary")
    os.makedirs(sdir, exist_ok=True)
    ftex = os.path.join(sdir, "IJDL_supplementary_tables.tex")
    with open(ftex, "w", encoding="utf-8") as fh:
        fh.write(doc)
    print(f"[補足表] {', '.join(made)} → {ftex}")
    if getattr(a, "supp_pdf", False):
        import shutil, subprocess
        if not shutil.which("pdflatex"):
            print("[補足表] pdflatex が見つからないため PDF は作りません。tex をお手元で組んでください", file=sys.stderr)
            return
        for _ in range(2):   # longtable の列幅・参照のため 2 回
            r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", os.path.basename(ftex)], cwd=sdir, capture_output=True, text=True)
        print("[補足表] PDF を作りました" if r.returncode == 0 else "[補足表] pdflatex が失敗しました(tex のログを確認してください)", file=sys.stderr if r.returncode else sys.stdout)


# ----------------------------------------------------------------------------- WoS と PMC の被引用数の比較(v012)
def cb_compare(d, a, outdir):
    """WoS の被引用数と PMC の cited-by の記述統計と相関。全体・雑誌別・DAS 類型別。NB は使わない"""
    w = num(d["wos_TC"]) if "wos_TC" in d else pd.Series(np.nan, index=d.index)
    p = num(d["pmc_citedby_n"]) if "pmc_citedby_n" in d else pd.Series(np.nan, index=d.index)
    if "wos_matched" in d:
        w = w.where(d.wos_matched.str.lower() == "true")
    if "cb_fetched" in d:
        p = p.where(d.cb_fetched == "1")
    w, p = w.where(w >= 0), p.where(p >= 0)
    ok = w.notna() & p.notna()
    x = pd.DataFrame({"w": w[ok], "p": p[ok], "journal": jshort(d.journal_key[ok]), "das": d.das_label[ok], "year": d.year[ok]})

    def row(g, label, kind):
        r = {"kind": kind, "group": label, "n_both": len(g)}
        for nm, v in (("wos", g.w), ("pmc", g.p)):
            r.update({f"{nm}_mean": v.mean(), f"{nm}_var": v.var(), f"{nm}_median": v.median(), f"{nm}_q1": v.quantile(.25), f"{nm}_q3": v.quantile(.75),
                      f"{nm}_max": v.max(), f"{nm}_zero_share": (v == 0).mean()})
        r["mean_ratio_pmc_over_wos"] = r["pmc_mean"] / r["wos_mean"] if r["wos_mean"] else np.nan
        r["pearson_log1p"] = np.log1p(g.w).corr(np.log1p(g.p)) if len(g) > 2 else np.nan
        r["spearman"] = g.w.corr(g.p, method="spearman") if len(g) > 2 else np.nan
        return r
    rows = [row(x, "all", "overall")]
    rows += [row(g, k, "journal") for k, g in sorted(x.groupby("journal"), key=lambda t: str(t[0]))]
    rows += [row(g, k, "das") for k, g in sorted(x.groupby("das"), key=lambda t: str(t[0]))]
    rows += [row(g, str(int(k)), "year") for k, g in sorted(x.groupby("year"), key=lambda t: t[0]) if len(g) >= a.min_group]
    t = pd.DataFrame(rows)
    # 件数の内訳(どちらかだけある論文の数)も全体の行に付ける
    t.loc[0, "n_wos_available"] = int(w.notna().sum())
    t.loc[0, "n_pmc_available"] = int(p.notna().sum())
    t.loc[0, "n_rows"] = len(d)
    os.makedirs(outdir, exist_ok=True)
    t[t.kind == "overall"].to_csv(os.path.join(outdir, "desc_wos_vs_pmc.csv"), index=False, encoding="utf-8-sig")
    t[t.kind != "overall"].to_csv(os.path.join(outdir, "desc_wos_vs_pmc_by_journal.csv"), index=False, encoding="utf-8-sig")
    o = t.iloc[0]
    print(f"[WoS と PMC の比較] 両方ある論文 {int(o.n_both):,} 件(WoS あり {int(o.n_wos_available):,} / PMC あり {int(o.n_pmc_available):,} / 全 {int(o.n_rows):,} 行)")
    print(f"  WoS: 平均 {o.wos_mean:.2f}, 分散 {o.wos_var:.0f}, 中央値 {o.wos_median:g}, 最大 {o.wos_max:g} / PMC: 平均 {o.pmc_mean:.2f}, 分散 {o.pmc_var:.0f}, 中央値 {o.pmc_median:g}, 最大 {o.pmc_max:g}")
    print(f"  PMC/WoS の平均の比 {o.mean_ratio_pmc_over_wos:.3f} / log1p の Pearson {o.pearson_log1p:.3f} / Spearman {o.spearman:.3f}")
    print("保存先:", outdir)


# ----------------------------------------------------------------------------- 送るファイルをまとめる(v014)
PACK_DEFAULT_DIRS = ["analysis", "analysis/robustness", "analysis_pmc_samewos", "analysis_pmc_samewos_jy"]
PACK_PATTERNS = ["summary.txt", "robustness_*.csv", "robustness_*.txt", "log_*.txt", "nb_irr_*.csv", "nb_model_*.csv",
                 "nb_by_journal.csv", "nb_wald_*.csv", "desc_wos_vs_pmc*.csv"]
# (表示名, フォルダ(親からの相対), 被引用数の列名)  DAS の率比を並べる元
PACK_COMPARE = [
    ("wos_main", "analysis", "wos_TC"),
    ("pmc_full", "analysis/robustness/pmc", "pmc_citedby_n"),
    ("pmc_samewos", "analysis_pmc_samewos", "pmc_citedby_n"),
    ("wos_jy", "analysis/robustness/jy", "wos_TC"),
    ("pmc_full_jy", "analysis/robustness/pmc_jy", "pmc_citedby_n"),
    ("pmc_samewos_jy", "analysis_pmc_samewos_jy", "pmc_citedby_n"),
]


def pack_send(a):
    """送るファイルを 1 つのフォルダ(と zip)にまとめ、PMC の 3 通りの DAS 率比の比較表も作る。分析は走らせない"""
    import glob, shutil, zipfile
    root = os.path.expanduser(a.pack_root)
    out = os.path.expanduser(a.pack_out)
    if os.path.isdir(out):
        for f in glob.glob(os.path.join(out, "*")):      # 前回の中身を消して、古いファイルが混ざらないようにする
            if os.path.isfile(f):
                os.remove(f)
    os.makedirs(out, exist_ok=True)
    dirs = [x.strip() for x in a.pack_dirs.split(",") if x.strip()] if a.pack_dirs else PACK_DEFAULT_DIRS
    got, miss, big = [], [], []
    for dname in dirs:
        folder = os.path.join(root, dname)
        if not os.path.isdir(folder):
            miss.append(f"{dname}/ (フォルダがありません)")
            continue
        prefix = dname.strip("/").replace("/", "_")
        files = sorted({f for p in PACK_PATTERNS for f in glob.glob(os.path.join(folder, p))})
        if not files:
            miss.append(f"{dname}/ (対象のファイルがありません)")
        for f in files:
            mb = os.path.getsize(f) / 1e6
            if mb > a.pack_max_mb:
                big.append(f"{dname}/{os.path.basename(f)} ({mb:.1f} MB)")
                continue
            dst = f"{prefix}__{os.path.basename(f)}"
            shutil.copy2(f, os.path.join(out, dst))
            got.append(dst)
    # DAS の率比の比較表
    comp, base_idx = {}, None
    for name, rel, dv in PACK_COMPARE:
        f = os.path.join(root, rel, f"nb_irr_{_tag(dv)}.csv")
        if not os.path.exists(f):
            miss.append(f"比較表の入力 {rel}/nb_irr_{_tag(dv)}.csv ({name})")
            continue
        t = pd.read_csv(f)
        t = t[t.group == G_DAS].copy()
        t["das"] = t.variable.str.replace("das_", "", regex=False)
        t = t.set_index("das")
        comp[name] = t
    if comp:
        classes = list(next(iter(comp.values())).index)
        tab = pd.DataFrame({"das": classes})
        for name, t in comp.items():
            t = t.reindex(classes)
            tab[f"irr_{name}"], tab[f"low_{name}"], tab[f"high_{name}"], tab[f"p_holm_{name}"] = t.irr.values, t.irr_low.values, t.irr_high.values, t.p_holm_cluster.values
        for x, y in (("pmc_full", "pmc_samewos"), ("pmc_full_jy", "pmc_samewos_jy")):
            if f"irr_{x}" in tab and f"irr_{y}" in tab:
                tab[f"absdiff_{x}_vs_{y}"] = (tab[f"irr_{x}"] - tab[f"irr_{y}"]).abs()
        tab.to_csv(os.path.join(out, "pack_compare_pmc_samewos.csv"), index=False, encoding="utf-8-sig")
        got.append("pack_compare_pmc_samewos.csv")
        dcols = [c for c in tab.columns if c.startswith("absdiff_")]
        for c in dcols:
            print(f"[比較] {c}: 最大 {tab[c].max():.4f}", file=sys.stderr)
    # 記録
    import datetime
    man = [f"送るファイルの一覧 ({VERSION}) {datetime.datetime.now():%Y-%m-%d %H:%M}", f"入力の親フォルダ: {root}", f"入れたファイル {len(got)} 個:"]
    man += [f"  {g}" for g in got]
    if miss:
        man += [f"見つからなかったもの {len(miss)} 件:"] + [f"  {m}" for m in miss]
    if big:
        man += [f"大きいので入れなかったもの(--pack-max-mb {a.pack_max_mb}):"] + [f"  {b}" for b in big]
    with open(os.path.join(out, "pack_manifest.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(man))
    print("\n".join(man))
    if not a.pack_no_zip:
        zp = out.rstrip("/") + ".zip"
        with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(glob.glob(os.path.join(out, "*"))):
                z.write(f, os.path.basename(f))
        print(f"\nzip: {zp}")
    print(f"保存先: {out}")


# ----------------------------------------------------------------------------- 雑誌グループ別の年次件数の確認(v015)
BIG3_KEYS = ("PLOS", "SCIENTIFIC REPORTS", "NATURE COMMUN")   # journal_key(大文字)にこの文字列を含む雑誌を big3 とする
HELIYON_KEY = "HELIYON"                                       # MDPI ではない雑誌


BIG3_SHORT_KEYS = ("SCIREP", "NATCOMMUN", "PLOSONE")           # v027: 参照セットの短縮形(SciRep・NatCommun・PLoSOne)も big3 にする


def _jgroup(key):
    k = str(key).upper()
    kn = re.sub(r"[^A-Z0-9]", "", k)                                # 空白・記号を除いた形でも照合する
    if any(b in k for b in BIG3_KEYS) or any(b in kn for b in BIG3_SHORT_KEYS):
        return "big3"
    if HELIYON_KEY in k:
        return "heliyon"
    return "mdpi6"


def check_journal_groups(a):
    """fig0 と同じ論文集合で、年ごとに big3 / Heliyon / MDPI 6 誌の件数を数え、本文の 981・40,563 がどの集合の件数かを判定する"""
    d, miss = read_cols(a.csv, ["journal_key", "pub_year", "das_label", "das_has_label", "article_type", "wos_notice_type"])
    if "journal_key" not in d or "pub_year" not in d:
        sys.exit("journal_key か pub_year の列がありません: " + str(miss))
    n0 = len(d)
    if a.journal:
        d = d[d.journal_key.str.contains(a.journal, case=False, regex=False)]
    d = d[(d.get("das_has_label", "1") == "1") & (d.das_label != "")]
    if "article_type" in d and a.article_type:
        d = d[d.article_type == a.article_type]
    if "wos_notice_type" in d and not a.keep_notice:
        d = d[d.wos_notice_type == ""]
    d = d.copy()
    d["year"] = num(d.pub_year)
    d = d[d.year >= a.min_year].dropna(subset=["year"])
    d["year"] = d.year.astype(int)
    d["grp"] = d.journal_key.map(_jgroup)
    print(f"CSV {n0:,} 行 → fig0 と同じ条件で {len(d):,} 件(論文の 659,437 と一致するか確認してください)")

    jt = d.groupby(["journal_key", "grp"]).size().rename("n").reset_index()
    jt["journal"] = jshort(jt.journal_key)
    print("\n雑誌とグループの対応(big3=3 誌、heliyon=1 誌、mdpi6=6 誌になっているか確認):")
    print(jt[["journal", "grp", "n"]].sort_values(["grp", "n"], ascending=[True, False]).to_string(index=False))
    cnt = jt.groupby("grp").size().to_dict()
    if cnt.get("big3") != 3 or cnt.get("heliyon") != 1 or cnt.get("mdpi6") != 6:
        print(f"\n[警告] グループの雑誌数が想定(big3=3, heliyon=1, mdpi6=6)と違います: {cnt}。"
              "上の表の対応が正しいか確認し、必要なら BIG3_KEYS・HELIYON_KEY を直してください", file=sys.stderr)

    ct = pd.crosstab(d.year, d.grp).reindex(columns=["big3", "heliyon", "mdpi6"], fill_value=0)
    ct.insert(0, "all", ct.sum(axis=1))
    ct["others7"] = ct.heliyon + ct.mdpi6          # big3 以外の 7 誌(Heliyon を含む)
    ct["others7_share_%"] = (100 * ct.others7 / ct["all"]).round(1)
    out = os.path.join(os.path.expanduser(a.outdir), "journal_groups_by_year.csv")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    ct.to_csv(out, encoding="utf-8-sig")
    print("\n年ごとの件数(others7 = Heliyon + MDPI 6 誌 = big3 以外の 7 誌):")
    print(ct.to_string())
    print("保存:", out)

    print("\n本文の数値の判定:")
    for item in [x.strip() for x in a.check_ref.split(",") if x.strip()]:
        try:
            y, nsub, nall = (int(v.replace("_", "")) for v in item.split(":"))
        except ValueError:
            print(f"  [読めません] {item}(年:該当件数:その年の全体 の形で指定してください)")
            continue
        if y not in ct.index:
            print(f"  {y} 年: データにありません")
            continue
        r = ct.loc[y]
        print(f"\n  {y} 年: 本文は「{nsub:,} of {nall:,}」")
        print(f"    この集計の全体 {int(r['all']):,}  / big3 {int(r['big3']):,}  / big3 以外の 7 誌 {int(r['others7']):,}"
              f"(内訳: Heliyon {int(r['heliyon']):,} + MDPI 6 誌 {int(r['mdpi6']):,})")
        if int(r["all"]) != nall:
            print(f"    [注意] 全体が本文の {nall:,} と一致しません。条件(--article-type, --keep-notice, --min-year)を確認してください")
        m7, m6 = nsub == int(r["others7"]), nsub == int(r["mdpi6"])
        if m7 and not m6:
            print("    判定: big3 以外の 7 誌(Heliyon を含む)の件数と一致 → 本文の「six remaining MDPI journals」は誤り。")
            print(f"    書き換え案: ... {nsub:,} of {nall:,} articles in {y} came from the seven other journals")
        elif m6 and not m7:
            print("    判定: MDPI 6 誌(Heliyon を除く)の件数と一致 → Heliyon は含まれていない。")
            print(f"    書き換え案: ... {nsub:,} of {nall:,} articles in {y} came from the six MDPI journals"
                  f"(「remaining」は使えない。big3 以外は 7 誌で、Heliyon が {int(r['heliyon']):,} 件ある)")
        elif m6 and m7:
            print("    判定: 7 誌と 6 誌の件数が同じです(Heliyon が 0 件)。上の対応表を確認してください")
        else:
            print("    判定: 7 誌・6 誌のどちらとも一致しません。上の年別の表から、本文の数値の元の集計を確認してください")
            print(f"    参考: 7 誌なら {int(r['others7']):,}、6 誌なら {int(r['mdpi6']):,}")


# ----------------------------------------------------------------------------- 論文 3.1節の数値の確認(v016)
# 本文(IJDL_sn-article_020)の数値。(類型, 年, 値%)
CLAIM_YEAR = [("P", 2014, 74.7), ("P", 2022, 26.3), ("P", 2025, 37.9), ("A", 2014, 2.6), ("A", 2023, 36.5), ("A", 2025, 34.6),
              ("F", 2014, 14.7), ("F", 2020, 23.5), ("F", 2021, 13.8), ("F", 2025, 17.7), ("N", 2022, 20.2), ("N", 2025, 2.4)]
# (類型, 雑誌の名前に含まれる文字列(大文字), 表示名, 値%)
CLAIM_JOURNAL = [("F", "NATURE COMMUN", "Nature Communications", 46.6), ("F", "PLOS", "PLOS ONE", 19.8),
                 ("P", "PLOS", "PLOS ONE", 64.7), ("P", "MOLECULES", "Molecules", 42.4), ("P", "MATERIALS", "Materials", 37.4),
                 ("P", "MOLECULAR SCIENCES", "IJMS", 34.0),
                 ("A", "CLINICAL MEDICINE", "J. Clin. Med.", 66.6), ("A", "ENVIRONMENTAL RESEARCH", "IJERPH", 56.4),
                 ("A", "HELIYON", "Heliyon", 51.1), ("A", "SCIENTIFIC REPORTS", "Scientific Reports", 49.9),
                 ("N", "SENSORS", "Sensors", 29.3), ("N", "MATERIALS", "Materials", 24.9), ("N", "MOLECULES", "Molecules", 23.5)]
CLAIM_F_UNDER4 = [("MATERIALS", "Materials"), ("MOLECULES", "Molecules"), ("SENSORS", "Sensors"),
                  ("CLINICAL MEDICINE", "J. Clin. Med."), ("ENVIRONMENTAL RESEARCH", "IJERPH")]
TOL = 0.05   # 本文は小数第 1 位。これ以内なら一致とみなす


def _mark(claim, v):
    return "一致" if abs(claim - v) <= TOL else f"×(差 {v - claim:+.1f})"


def check_section31(a):
    cols = ["journal_key", "pub_year", "das_label", "das_has_label", "article_type", "wos_notice_type", "wos_matched", "wos_TC"]
    d, miss = read_cols(a.csv, cols)
    for c in ("journal_key", "pub_year", "das_label"):
        if c not in d:
            sys.exit("必要な列がありません: " + c)
    if "wos_notice_type" not in d:
        d["wos_notice_type"] = ""
    if "wos_matched" not in d:
        d["wos_matched"] = ""
        print("[注意] wos_matched 列がありません。WoS の部分は計算できません", file=sys.stderr)
    if "wos_TC" not in d:
        d["wos_TC"] = ""
    d = d[(d.get("das_has_label", "1") == "1") & (d.das_label != "")]
    if "article_type" in d and a.article_type:
        d = d[d.article_type == a.article_type]
    d = d.copy()
    d["year"] = num(d.pub_year)
    d = d.dropna(subset=["year"])
    d["year"] = d.year.astype(int)
    d["J"] = d.journal_key.astype(str).str.upper()
    tc = num(d.wos_TC).where(d.wos_matched.str.lower() == "true")
    d["tc"] = tc.where(tc >= 0)
    s_all = d
    s_in = d[d.year >= a.min_year]                       # 注記を除かない(2014 年以降)
    s_ex = s_in[s_in.wos_notice_type == ""]               # 注記を除く(2014 年以降)= 論文の標本
    print(f"全 {len(s_all):,} 件(年の制限なし)/ 2014 年以降・注記を含む {len(s_in):,} 件 / 2014 年以降・注記を除く {len(s_ex):,} 件(論文は 659,437)")

    # 1) 年別の割合
    print("\n1) 年別の割合(全雑誌、DAS ラベルのある論文):本文の値と、2 通りの標本の値")
    sh = {}
    for name, s_ in (("注記を除く", s_ex), ("注記を含む", s_in)):
        ct = pd.crosstab(s_.year, s_.das_label)
        sh[name] = ct.div(ct.sum(axis=1), axis=0) * 100
    rows = []
    print(f"  {'類型':>3} {'年':>5} {'本文':>6} | {'注記を除く':>10} {'判定':<12} | {'注記を含む':>10} {'判定':<12}")
    for c, y, v in CLAIM_YEAR:
        r = {}
        for name in ("注記を除く", "注記を含む"):
            t = sh[name]
            r[name] = float(t.loc[y, c]) if (y in t.index and c in t.columns) else float("nan")
        print(f"  {c:>3} {y:>5} {v:>6.1f} | {r['注記を除く']:>10.1f} {_mark(v, r['注記を除く']):<12} | {r['注記を含む']:>10.1f} {_mark(v, r['注記を含む']):<12}")
        rows.append({"cat": c, "year": y, "text_%": v, "excl_notice_%": round(r["注記を除く"], 2), "incl_notice_%": round(r["注記を含む"], 2)})
    for c, claim_y in (("N", 2022), ("P", 2022), ("A", 2023)):
        for name in ("注記を除く", "注記を含む"):
            t = sh[name][c]
            print(f"  [{name}] {c} の割合が" + ("最小" if c == "P" else "最大") + "の年: " + (str(int(t.idxmin())) if c == "P" else str(int(t.idxmax()))) + f"  (本文: {claim_y})")
    out1 = os.path.join(os.path.expanduser(a.outdir), "section31_year_shares.csv")
    os.makedirs(os.path.dirname(out1), exist_ok=True)
    pd.DataFrame(rows).to_csv(out1, index=False, encoding="utf-8-sig")

    # 2) 雑誌別の割合
    print("\n2) 雑誌別の割合:本文は「WoS 被引用数のある論文のうち」。2 通りの標本で計算")
    samples = {"WoS あり(注記を除く)": s_ex[s_ex.tc.notna()], "DAS ラベルのある全論文(注記を除く)": s_ex}
    for k, v in samples.items():
        print(f"  標本 {k}: {len(v):,} 件")
    rows = []
    hdr = list(samples)
    print(f"  {'類型':>3} {'雑誌':<22} {'本文':>6} | " + " | ".join(f"{h[:14]:>14} {'判定':<12}" for h in hdr))
    for c, key, disp, v in CLAIM_JOURNAL:
        r = {}
        for h, s_ in samples.items():
            sj = s_[s_.J.str.contains(key, regex=False)]
            r[h] = 100 * (sj.das_label == c).mean() if len(sj) else float("nan")
        print(f"  {c:>3} {disp:<22} {v:>6.1f} | " + " | ".join(f"{r[h]:>14.1f} {_mark(v, r[h]):<12}" for h in hdr))
        rows.append({"cat": c, "journal": disp, "text_%": v, **{h: round(r[h], 2) for h in hdr}})
    print("  F が 4% 未満とされた雑誌:")
    for key, disp in CLAIM_F_UNDER4:
        vals = []
        for h, s_ in samples.items():
            sj = s_[s_.J.str.contains(key, regex=False)]
            vals.append(100 * (sj.das_label == "F").mean() if len(sj) else float("nan"))
        print(f"    {disp:<22} " + "  ".join(f"{x:5.1f}% ({'<4 OK' if x < 4 else '4 以上'})" for x in vals))
    out2 = os.path.join(os.path.expanduser(a.outdir), "section31_journal_shares.csv")
    pd.DataFrame(rows).to_csv(out2, index=False, encoding="utf-8-sig")
    # 同じ文字列が複数の雑誌に当たっていないかの点検
    for key in sorted({k for _, k, _, _ in CLAIM_JOURNAL}):
        hit = sorted(s_ex.loc[s_ex.J.str.contains(key, regex=False), "J"].unique())
        if len(hit) != 1:
            print(f"  [警告] 検索語 '{key}' に合う雑誌が {len(hit)} 誌: {hit}", file=sys.stderr)

    # 3) WoS 被引用数の平均・分散・最大
    print("\n3) WoS 被引用数(wos_TC)の平均・分散・最大。本文: 3.1節 19.55 / 2,305 / 8,061、3.7節 19.50 / 2,296")
    w_ex = s_ex[s_ex.tc.notna()]
    n_g = w_ex.groupby(["journal_key", "year"]).tc.transform("size")
    cand = {"A 注記を除く・2014 年以降(論文の 651,617)": w_ex,
            "B A のうち 雑誌×年が %d 件以上の群" % a.min_group: w_ex[n_g >= a.min_group],
            "C 注記を含む・2014 年以降": s_in[s_in.tc.notna()],
            "D 年・注記の制限なし": s_all[s_all.tc.notna()]}
    for k, v in cand.items():
        print(f"  {k}: N={len(v):,}  平均 {v.tc.mean():.2f}  分散 {v.tc.var():,.0f}  最大 {int(v.tc.max()):,}")
    print("  どれも 19.55 / 2,305 / 8,061 と一致しなければ、3.1節の値は NB モデルの対象(共変量が揃った 648,217 件)のもの。")
    print("  確認: grep '\\[NB\\] 分析対象' ~/output_covariates_v27/analysis/summary.txt")
    print("保存:", out1, "と", out2)


def _check_ctx(a):
    """--check-contrast・--check-df 用: データを読み、NB の設計行列まで作る(推定はしない)"""
    d, meta, das_cols, ref, log = prepare(a)
    if getattr(a, "exposure", "off") != "off":
        attach_exposure(a, d, meta)   # v020
    excl = {c.strip() for c in a.exclude.split(",") if c.strip()}
    base_ivs = [c for c in meta if c not in excl and c != "log_review" and c not in das_cols]
    print("\n".join(log), file=sys.stderr)
    ctx = nb_build(d, meta, das_cols, base_ivs, a, log)
    return ctx, ref, log


def check_df(a, outdir):
    """交互作用の df(論文 3.5節の df = 49)の内訳を、回帰を推定せずに調べる"""
    ctx, ref, log = _check_ctx(a)
    tag = _tag(a.dv)
    lines = []
    P = lines.append
    P(f"交互作用の自由度の確認 ({VERSION})  従属変数 {a.dv}")
    P(log[-1])
    das_journal_cells(ctx, ref, a, P, outdir, tag)
    E, en, D, J, max_df = das_journal_cols(ctx)
    rows = []
    if J is not None:
        info = interaction_df_info(ctx, a, E, en)
        P(f"\n[DAS × 雑誌] 列 {info['n_cols']} → {info['n_kept']}、df = {info['df']}")
        for ln in interaction_df_lines(info, a, max_df, "(DAS 類型の数 − 1)×(雑誌の数 − 1)"):
            P(ln)
        rows.append(dict(test="DAS × 雑誌", max_df=max_df, **{k: info[k] for k in ("n_cols", "n_kept", "rank_main", "rank_inter", "df")}, dropped="; ".join(f"{n}(n={c})" for n, c in info["dropped"])))
    post = (ctx["year"] >= a.interaction_year).astype(float)
    if 0 < post.mean() < 1:
        E2 = D * post[:, None]
        info2 = interaction_df_info(ctx, a, E2, [f"{c}×post" for c in ctx["das_cols"]])
        P(f"\n[DAS × 出版年{a.interaction_year}以降] 列 {info2['n_cols']} → {info2['n_kept']}、df = {info2['df']}")
        for ln in interaction_df_lines(info2, a, len(ctx["das_cols"]), "(DAS 類型の数 − 1)"):
            P(ln)
        rows.append(dict(test=f"DAS × 出版年{a.interaction_year}以降", max_df=len(ctx["das_cols"]), **{k: info2[k] for k in ("n_cols", "n_kept", "rank_main", "rank_inter", "df")}, dropped="; ".join(f"{n}(n={c})" for n, c in info2["dropped"])))
    if rows:
        pd.DataFrame(rows).to_csv(os.path.join(outdir, f"nb_df_check_{tag}.csv"), index=False, encoding="utf-8-sig")
    P("\n読み方: 論文の df = 49 が、理論上の最大 df(類型数−1)×(雑誌数−1) から何列を除いた値かは、上の「除いた列」で分かる。"
      "階数の増分が残した列の数より小さい場合は、列の間に一次従属がある。雑誌別の NB の比較数(54)は交互作用の df とは別の基準(--min-cat-j)で数えるので、同じ数になるとは限らない。")
    txt = "\n".join(lines)
    print(txt)
    with open(os.path.join(outdir, f"check_df_{tag}.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    print("\n保存先:", outdir)


def check_contrast(a, outdir):
    """主 NB モデル(基準 F)を 1 回だけ推定し、別の基準(既定 N)との対比と Holm 調整後の p を出す"""
    ctx, ref, log = _check_ctx(a)
    tag = _tag(a.dv)
    lines = []
    P = lines.append
    P(f"基準を替えた対比の確認 ({VERSION})  従属変数 {a.dv} / 主モデルの基準 {ref} / 対比の基準 {a.contrast_ref}")
    P(log[-1])
    print("[進捗] 主 NB モデルを推定中(行数が多いと数分かかります)", file=sys.stderr, flush=True)
    full = nb_fit(ctx["X"], ctx["nbd"], offset=ctx.get("offset"))
    cov = nb_cov(full, ctx["X"], ctx["y"], codes=ctx["gcodes"])
    P(f"対数尤度 {full['llf']:.2f} / alpha(過分散) {full['alpha']:.4f} / 反復 {full['iters']} / 収束 {full['converged']} / クラスタ数 {int(ctx['gcodes'].max()) + 1}")
    names, meta_ = ctx["names"], ctx["meta"]
    idx = [i for i, n in enumerate(names) if n in ctx["das_cols"]]
    t0 = _irr_table(full, cov, names, idx, meta_)
    t0["p_holm_cluster"] = holm(t0.p_cluster.values)
    P(f"\n[主モデル(基準 {ref})の DAS の率比 — 論文の表3・3.2節と照合する]")
    P(t0[["variable", "irr", "irr_low", "irr_high", "p_cluster", "p_holm_cluster"]].to_string(index=False, float_format=lambda x: f"{x:.4g}"))
    das_contrasts(full, cov, names, ctx["das_cols"], ref, a.contrast_ref, P, outdir, tag)
    txt = "\n".join(lines)
    print(txt)
    with open(os.path.join(outdir, f"check_contrast_{tag}.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    print("\n保存先:", outdir)


# ----------------------------------------------------------------------------- v020: 査読コメントへの対応(露出時間・ゼロ過剰・小クラスタ・NB 尤度の Shapley)
G_AGE = "露出時間"
EN_VAR["log_age"] = "Article age (log years)"
EN_VAR.update({f"age_s{i}": ("Article age, linear term (log years)" if i == 0 else f"Article age spline, knot {i}") for i in range(0, 13)})   # v025


def _age_meta():
    return dict(group=G_AGE, desc="論文の経過時間 log(調査日 − 出版日、年)", kind="cont", src="pub_date", tr="log1p")


def _add_age_spline(d, meta, K, la=None):
    """v025: log 経過年数 la(既定は d.log_age)の折れ線スプライン列を d に作り、meta に加える。age_s0=線形の項、age_s1〜age_sK=結び目での折れ。
    結び目は la の分位点(K 個、等間隔の分位)。返り値: (結び目の log 年, 作った列名)"""
    la = d["log_age"] if la is None else la
    K = max(1, int(K))
    knots = np.quantile(la.dropna(), np.linspace(0, 1, K + 2)[1:-1])
    d["age_s0"] = la
    cols = ["age_s0"]
    for i, k in enumerate(knots, 1):
        d[f"age_s{i}"] = (la - k).clip(lower=0)
        cols.append(f"age_s{i}")
    for c_ in cols:
        meta[c_] = dict(group=G_AGE, desc="log 経過年数の折れ線スプライン", kind="cont", src="pub_date", tr="log1p")
    return knots, cols


def attach_exposure(a, d, meta):
    """出版日から調査日(WoS 取得日または PMC 取得日)までの経過年数 age_years と log_age を d に付ける。
    日付は --exposure-cols の列を左から順に使う(ない行は次の列、最後は出版年の 7 月 1 日)。--exposure covariate のときは meta に log_age を、spline のときは折れ線スプラインの列を加える"""
    cand = [c.strip() for c in a.exposure_cols.split(",") if c.strip()]
    src, miss = read_cols(a.csv, list(dict.fromkeys(cand)))
    src = src.reindex(d.index)
    date = pd.Series(pd.NaT, index=d.index, dtype="datetime64[ns]")
    used = {}
    for c in cand:
        if c not in src:
            continue
        s = src[c]
        try:
            if c.lower().endswith("month"):
                dt = pd.to_datetime(dict(year=d.year, month=num(s), day=15), errors="coerce")
            else:
                s2 = s.replace("", np.nan)
                try:
                    dt = pd.to_datetime(s2, errors="coerce", format="mixed")
                except (TypeError, ValueError):
                    dt = pd.to_datetime(s2, errors="coerce")
        except Exception as e:
            print(f"[露出時間] 列 {c} を日付に変換できませんでした: {type(e).__name__}", file=sys.stderr)
            continue
        fill = date.isna() & dt.notna()
        date = date.where(~fill, dt)
        used[c] = int(fill.sum())
    n_fb = int(date.isna().sum())
    if n_fb:
        mid = pd.to_datetime(dict(year=d.year.fillna(2000).astype(int).clip(1900, 2100), month=7, day=1))
        date = date.where(date.notna(), mid)
    ref = pd.Timestamp(a.exposure_ref_date or ("2026-10-29" if a.dv == "pmc_citedby_n" else "2026-06-15"))
    ref_ser = d["oa_win_end"] if "oa_win_end" in d else ref   # v042: OpenAlex の窓の終わり(12/31)を論文ごとの基準日にする
    age = ((ref_ser - date).dt.days / 365.25).clip(lower=a.exposure_min_age)
    d["age_years"] = age
    d["log_age"] = np.log(age)
    sd_w = float(d.groupby("gid")["log_age"].std().mean())
    info = dict(used=used, missing_cols=miss, n_fallback_year=n_fb, ref=("窓の終わり(論文ごと)" if "oa_win_end" in d else str(ref.date())), sd_within=sd_w,
                age_min=float(age.min()), age_med=float(age.median()), age_max=float(age.max()))
    print(f"[露出時間] 調査日 {info['ref']} / 使った日付の列(補った行数): {used if used else 'なし'} / 列がない: {miss if miss else 'なし'} / "
          f"出版年の 7/1 で補った行 {n_fb:,} / 経過年数 最小 {info['age_min']:.2f} 中央値 {info['age_med']:.2f} 最大 {info['age_max']:.2f} / "
          f"雑誌×年の中での log 経過年数の標準偏差(平均) {sd_w:.3f}", file=sys.stderr)
    if not used or sd_w < 0.01:
        print("[警告] 日付の列が使えず、経過年数が雑誌×年の中でほぼ一定です。オフセットは固定効果に吸収され、情報がありません。"
              "--find-cols 'date|month|day' で出版日の列を探し、--exposure-cols で指定してください", file=sys.stderr)
    if a.exposure == "covariate":
        meta["log_age"] = _age_meta()
    elif a.exposure == "spline":   # v025: log 経過年数の折れ線スプライン(--age-knots 個の結び目)を共変量として入れる
        knots, cols_ = _add_age_spline(d, meta, getattr(a, "age_knots", 4))
        info["knots_years"] = [float(np.exp(k)) for k in knots]
        print("[露出時間] --exposure spline: 折れ線スプライン " + str(len(cols_)) + " 項(結び目 " + ", ".join(f"{np.exp(k):.2f}年" for k in knots) + ")", file=sys.stderr)
    return info


def _cluster_cov(Ainv, s, codes, n, p):
    """スコア s(行ごと)をクラスタで集めたサンドイッチ分散。nb_cov と同じ有限標本補正"""
    G = int(codes.max()) + 1
    S = np.empty((G, s.shape[1]))
    for j in range(s.shape[1]):
        S[:, j] = np.bincount(codes, weights=s[:, j], minlength=G)
    return Ainv @ (S.T @ S) @ Ainv * (G / max(G - 1, 1)) * ((n - 1) / max(n - p, 1))


def _t_sf2(t, df):
    """両側 p(t 分布、自由度 df)。scipy がなければ正規近似"""
    try:
        from scipy import stats
        return float(2 * stats.t.sf(abs(t), df))
    except Exception:
        return float(norm_p(t)[0])


# ---- (1) 露出時間
def check_exposure(a, outdir):
    """経過時間(出版日からの日数)を扱う 4 通りの NB を比べる: none(出版年の固定効果のみ)/ offset(log 経過年数をオフセット)/
    covariate(log 経過年数を係数つきで入れる。係数 = 経過時間への弾力性、1 ならオフセットが妥当)/ jy_offset(雑誌×年の固定効果+オフセット)"""
    import copy
    if _is_rv(a.dv):
        sys.exit("--check-exposure は被引用数(--dv wos_TC または pmc_citedby_n)用です")
    d, meta, das_cols, ref, log = prepare(a)
    info = attach_exposure(a, d, meta)
    excl = {c.strip() for c in a.exclude.split(",") if c.strip()}
    tag = _tag(a.dv)
    specs = [("none", "additive", "off"), ("offset", "additive", "offset"), ("covariate", "additive", "covariate"), ("jy_offset", "jy", "offset")]
    rows, res = [], {}
    lines = []
    P = lines.append
    P(f"経過時間の扱いの比較 ({VERSION}) 従属変数 {a.dv} / 参照: 主モデルの DAS 基準 {ref}")
    P(f"調査日 {info['ref']}、日付の列 {info['used']}、出版年の 7/1 で補った行 {info['n_fallback_year']:,}、雑誌×年内の log 経過年数の SD {info['sd_within']:.3f}")
    for name, fe, mode in specs:
        print(f"[進捗] {name} を推定中", file=sys.stderr, flush=True)
        b = copy.copy(a)
        b.exposure, b.nb_fe = mode, fe
        m2 = dict(meta)
        if mode == "covariate":
            m2["log_age"] = _age_meta()
        base_ivs = [c for c in m2 if c not in excl and c != "log_review" and c not in das_cols]
        ctx = nb_build(d, m2, das_cols, base_ivs, b, [])
        full = nb_fit(ctx["X"], ctx["nbd"], offset=ctx.get("offset"))
        cov = nb_cov(full, ctx["X"], ctx["y"], codes=ctx["gcodes"])
        names = ctx["names"]
        idx = [i for i, n in enumerate(names) if n in ctx["das_cols"]]
        t = _irr_table(full, cov, names, idx, ctx["meta"])
        t["p_holm"] = holm(t.p_cluster.values)
        npar = int(np.linalg.matrix_rank(full["A"])) + 1
        aic = -2 * full["llf"] + 2 * npar
        res[name] = (t, full["llf"], aic, len(ctx["y"]))
        for r in t.itertuples():
            rows.append(dict(spec=name, fe=fe, exposure=mode, variable=r.variable, irr=r.irr, low=r.irr_low, high=r.irr_high,
                             p_cluster=r.p_cluster, p_holm=r.p_holm, llf=full["llf"], aic=aic, n=len(ctx["y"])))
        if mode == "covariate" and "log_age" in names:
            i = names.index("log_age")
            sd = float(d.loc[ctx["use"].index, "log_age"].std())
            se = math.sqrt(cov["cluster"][i, i])
            el, el_se = full["beta"][i] / sd, se / sd
            P(f"\n[covariate] log 経過年数の係数(弾力性)= {el:.3f}(クラスタ頑健 SE {el_se:.3f}、95% 区間 {el - 1.96 * el_se:.3f}〜{el + 1.96 * el_se:.3f})。1 に近ければ「被引用数は露出時間に比例」というオフセットの仮定が妥当")
            rows.append(dict(spec=name, fe=fe, exposure=mode, variable="log_age_elasticity", irr=el, low=el - 1.96 * el_se, high=el + 1.96 * el_se,
                             p_cluster=float("nan"), p_holm=float("nan"), llf=full["llf"], aic=aic, n=len(ctx["y"])))
    base = res["none"][0].set_index("variable")
    P("\n[DAS の率比(基準 %s)。括弧内は Holm 補正後の p(クラスタ頑健)]" % ref)
    cmp_ = pd.DataFrame({"variable": base.index})
    for name, _, _ in specs:
        t = res[name][0].set_index("variable")
        cmp_[name] = [f"{t.loc[v, 'irr']:.3f} ({t.loc[v, 'p_holm']:.3g})" for v in base.index]
        cmp_[f"dlog_{name}"] = [math.log(t.loc[v, "irr"]) - math.log(base.loc[v, "irr"]) for v in base.index]
    P(cmp_[["variable"] + [s[0] for s in specs]].to_string(index=False))
    P("\n[主モデル(none)との率比の最大のずれ(対数)] " + ", ".join(f"{s[0]}: {cmp_[f'dlog_{s[0]}'].abs().max():.4f}" for s in specs[1:]))
    P("\n[対数尤度・AIC(同じ行・同じ固定効果なら比較できる。none と offset はパラメータ数が同じ)]")
    for name, _, _ in specs:
        P(f"  {name:10s} llf {res[name][1]:,.1f}  AIC {res[name][2]:,.1f}  N {res[name][3]:,}")
    P("\n読み方: DAS の率比・有意性が 4 通りで変わらなければ、出版年の固定効果で時間の影響を十分に調整できていたと言える。"
      "covariate の弾力性が 1 から大きく離れる場合は、オフセットよりも係数つきの log 経過年数(または経過年数のスプライン)を主とする。")
    txt = "\n".join(lines)
    print(txt)
    pd.DataFrame(rows).to_csv(os.path.join(outdir, f"nb_exposure_check_{tag}.csv"), index=False, encoding="utf-8-sig")
    with open(os.path.join(outdir, f"check_exposure_{tag}.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    print("保存先:", outdir)


# ---- (2) ゼロ過剰・ハードル
def _logit_fit(X, z, maxit=60, ridge=1e-8):
    n, p = X.shape
    pbar = min(max(z.mean(), 1e-6), 1 - 1e-6)
    b = np.zeros(p)
    b[0] = math.log(pbar / (1 - pbar))
    R = ridge * np.eye(p)
    R[0, 0] = 0.0

    def ll_of(bb):
        eta = np.clip(X @ bb, -30, 30)
        return float(np.sum(z * eta - np.logaddexp(0, eta))) - 0.5 * ridge * float(bb @ bb)
    ll = ll_of(b)
    conv = False
    for it in range(1, maxit + 1):
        eta = np.clip(X @ b, -30, 30)
        pi = 1 / (1 + np.exp(-eta))
        w = np.clip(pi * (1 - pi), 1e-10, None)
        H = (X * w[:, None]).T @ X + R
        g = X.T @ (z - pi) - R @ b
        step = np.linalg.lstsq(H, g, rcond=None)[0]
        for h in range(12):
            bt = b + step / 2 ** h
            lt = ll_of(bt)
            if lt >= ll - 1e-9:
                break
        done = abs(lt - ll) < 1e-10 * (1 + abs(ll))
        b, ll = bt, lt
        if done:
            conv = True
            break
    eta = np.clip(X @ b, -30, 30)
    pi = 1 / (1 + np.exp(-eta))
    w = np.clip(pi * (1 - pi), 1e-10, None)
    return dict(beta=b, pi=pi, llf=ll, A=(X * w[:, None]).T @ X + R, converged=conv, iters=it)


def _tnb_parts(theta, Xp, yp, nbd_p, off_p):
    b, alpha = theta[:-1], math.exp(theta[-1])
    mu = np.exp(np.clip(Xp @ b + off_p, -30, 30))
    logp0 = -np.log1p(alpha * mu) / alpha
    one_m = np.maximum(-np.expm1(logp0), 1e-300)
    ll = nbd_p.llf(mu, alpha) - float(np.log(one_m).sum())
    return ll, mu, alpha, np.exp(logp0), one_m


def _tnb_g(eta, yp, alpha):
    mu = np.exp(np.clip(eta, -30, 30))
    logp0 = -np.log1p(alpha * mu) / alpha
    one_m = np.maximum(-np.expm1(logp0), 1e-300)
    return (yp - mu) / (1 + alpha * mu) - np.exp(logp0) * mu / ((1 + alpha * mu) * one_m)


def _tnb_fit(Xp, yp, off_p, b0, alpha0):
    """ゼロ切断 NB2(y>0 だけ)の最尤。beta の勾配は解析式、log alpha の勾配は 1 回の差分"""
    from scipy.optimize import minimize
    nbd_p = NBData(yp)

    def fun(theta):
        ll, mu, alpha, p0, one_m = _tnb_parts(theta, Xp, yp, nbd_p, off_p)
        g = (yp - mu) / (1 + alpha * mu) - p0 * mu / ((1 + alpha * mu) * one_m)
        th2 = theta.copy()
        th2[-1] += 1e-5
        ll2 = _tnb_parts(th2, Xp, yp, nbd_p, off_p)[0]
        return -ll, np.r_[-(Xp.T @ g), -(ll2 - ll) / 1e-5]
    th0 = np.r_[b0, math.log(alpha0)]
    r = minimize(fun, th0, jac=True, method="L-BFGS-B", options=dict(maxiter=500, maxfun=1000, ftol=1e-13, gtol=1e-6))
    b, alpha = r.x[:-1], math.exp(r.x[-1])
    eta = Xp @ b + off_p
    e = 1e-5
    dg = (_tnb_g(eta + e, yp, alpha) - _tnb_g(eta - e, yp, alpha)) / (2 * e)
    A = (Xp * (-dg)[:, None]).T @ Xp
    g = _tnb_g(eta, yp, alpha)
    return dict(beta=b, alpha=alpha, llf=-float(r.fun), A=A, score=Xp * g[:, None], converged=bool(r.success), nit=int(r.nit))


def check_zero(a, outdir):
    """被引用数のゼロの多さへの対応: (i) NB2 が予測するゼロの割合と実際の割合、(ii) ハードルモデル(ゼロかどうかのロジット+正の値のゼロ切断 NB)で DAS の関連を 2 つに分ける"""
    import copy
    if _is_rv(a.dv):
        sys.exit("--check-zero は被引用数(--dv wos_TC または pmc_citedby_n)用です")
    ctx, ref, log = _check_ctx(a)
    tag = _tag(a.dv)
    X, y, off = ctx["X"], ctx["y"], ctx.get("offset")
    n, p = X.shape
    lines = []
    P = lines.append
    P(f"ゼロ過剰・ハードルモデルの確認 ({VERSION}) 従属変数 {a.dv} / 基準 {ref}")
    P(log[-1])
    print("[進捗] NB2 を推定中", file=sys.stderr, flush=True)
    full = nb_fit(X, ctx["nbd"], offset=off)
    cov = nb_cov(full, X, y, codes=ctx["gcodes"])
    mu, alpha = full["mu"], full["alpha"]
    p0 = (1 + alpha * mu) ** (-1 / alpha)
    obs0 = float((y == 0).mean())
    P(f"\n[ゼロの割合] 実際 {obs0:.4f} / NB2 が予測する割合 {p0.mean():.4f} / 差 {obs0 - p0.mean():+.4f}(正ならゼロが NB2 の予想より多い)")
    jn = jshort(pd.Series(np.array(ctx["jlabels"])[ctx["jcodes"]]))
    tb = pd.DataFrame({"journal": jn.values, "obs_zero": (y == 0).astype(float), "nb_zero": p0}).groupby("journal").mean()
    tb["diff"] = tb.obs_zero - tb.nb_zero
    P("[雑誌別のゼロの割合]\n" + tb.round(4).to_string())
    names = ctx["names"]
    idx = [i for i, nm in enumerate(names) if nm in ctx["das_cols"]]
    # ロジット(正の値になるか)
    print("[進捗] ロジット部分(y>0 か)", file=sys.stderr, flush=True)
    z = (y > 0).astype(float)
    lg = _logit_fit(X, z)
    Vl = _cluster_cov(np.linalg.pinv(lg["A"]), X * (z - lg["pi"])[:, None], ctx["gcodes"], n, p)
    # ゼロ切断 NB
    print("[進捗] ゼロ切断 NB 部分(y>0 の行だけ。数分かかります)", file=sys.stderr, flush=True)
    pos = y > 0
    Xp, yp = X[pos], y[pos]
    op = None if off is None else off[pos]
    tn = _tnb_fit(Xp, yp, np.zeros(len(yp)) if op is None else op, full["beta"], alpha)
    Vt = _cluster_cov(np.linalg.pinv(tn["A"]), tn["score"], ctx["gcodes"][pos], len(yp), p)
    P(f"\nロジット: 収束 {lg['converged']} / ゼロ切断 NB: 収束 {tn['converged']}(反復 {tn['nit']})、alpha {tn['alpha']:.4f}(通常の NB2 は {alpha:.4f})")
    P("注意: ゼロ切断 NB の標準誤差は alpha を固定した条件つきの情報行列を使う(alpha の推定の不確かさは含まない)。")
    rows = []
    for k in idx:
        nm = names[k]
        r = dict(variable=nm, n_class=int(X[:, k].sum()))
        for lab, b, V in (("nb2", full["beta"], cov["cluster"]), ("logit_pos", lg["beta"], Vl), ("tnb", tn["beta"], Vt)):
            se = math.sqrt(V[k, k])
            r[f"{lab}_ratio"] = math.exp(b[k])
            r[f"{lab}_low"], r[f"{lab}_high"] = math.exp(b[k] - 1.96 * se), math.exp(b[k] + 1.96 * se)
            r[f"{lab}_p"] = float(norm_p(b[k] / se)[0])
        rows.append(r)
    t = pd.DataFrame(rows)
    for lab in ("nb2", "logit_pos", "tnb"):
        t[f"{lab}_p_holm"] = holm(t[f"{lab}_p"].values)
    t.to_csv(os.path.join(outdir, f"nb_hurdle_{tag}.csv"), index=False, encoding="utf-8-sig")
    P(f"\n[DAS の関連(基準 {ref})]  nb2=通常の NB2 の率比 / logit_pos=被引用が 1 件以上になるオッズ比(1 より大きいと、ゼロが少ない) / tnb=被引用が 1 件以上の論文の中での期待被引用数の率比。p は Holm 補正(DAS の比較)後、クラスタ頑健")
    cols = ["variable", "n_class"] + [f"{l}_{s}" for l in ("nb2", "logit_pos", "tnb") for s in ("ratio", "low", "high", "p_holm")]
    P(t[cols].to_string(index=False, float_format=lambda x: f"{x:.4g}"))
    ll_h = lg["llf"] + tn["llf"]
    k_nb, k_h = int(np.linalg.matrix_rank(full["A"])) + 1, 2 * int(np.linalg.matrix_rank(lg["A"])) + 1
    P(f"\n[当てはまり(同じ y に対する対数尤度)] NB2 {full['llf']:,.1f}(AIC {-2 * full['llf'] + 2 * k_nb:,.1f}) / ハードル {ll_h:,.1f}(AIC {-2 * ll_h + 2 * k_h:,.1f})。"
      "ハードルは NB2 を含む入れ子ではない(パラメータ数が約 2 倍)ので AIC・BIC で比べる。")
    P("読み方: NB2 の率比とハードルの 2 つの部分の向きが同じなら、NB2 は結論に影響しない。向きが分かれるなら、「被引用がゼロになるか」と「被引用の多さ」で DAS の関連が違うことを本文に書く。")
    txt = "\n".join(lines)
    print(txt)
    with open(os.path.join(outdir, f"check_zero_{tag}.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    print("保存先:", outdir)


# ---- (3) 小クラスタ(72〜74 個)の推論
def check_cluster(a, outdir):
    """クラスタ頑健 SE を、t(G−1) 分布と wild cluster score bootstrap(Kline–Santos 型、スチューデント化)で補う。
    NB は GLM なので CR2 は標準的でない。スコアを雑誌×年ごとに集め、Webb(6 点)または Rademacher の重みで摂動して β* − β を作り、
    各回で SE を再計算した t* の分布で p 値と区間を出す。全係数に対して計算する"""
    ctx, ref, log = _check_ctx(a)
    tag = _tag(a.dv)
    X, y, off = ctx["X"], ctx["y"], ctx.get("offset")
    n, p = X.shape
    codes = ctx["gcodes"]
    G = int(codes.max()) + 1
    lines = []
    P = lines.append
    P(f"小クラスタの推論の確認 ({VERSION}) 従属変数 {a.dv} / クラスタ数 {G} / 反復 {a.boot_reps} / 重み {a.boot_weights}")
    P(log[-1])
    print("[進捗] 主モデルを推定中", file=sys.stderr, flush=True)
    full = nb_fit(X, ctx["nbd"], offset=off)
    cov = nb_cov(full, X, y, codes=codes)
    mu, alpha, beta = full["mu"], full["alpha"], full["beta"]
    A = full["A"]
    Ainv = np.linalg.pinv(A)
    w = mu / (1 + alpha * mu)
    s = X * ((y - mu) / (1 + alpha * mu))[:, None]
    S = np.empty((G, p))
    for j in range(p):
        S[:, j] = np.bincount(codes, weights=s[:, j], minlength=G)
    order = np.argsort(codes, kind="stable")
    bounds = np.searchsorted(codes[order], np.arange(G + 1))
    Ag = np.empty((G, p, p))
    for g in range(G):
        r = order[bounds[g]:bounds[g + 1]]
        Xg = X[r]
        Ag[g] = (Xg * w[r, None]).T @ Xg
    c = (G / max(G - 1, 1)) * ((n - 1) / max(n - p, 1))
    names = ctx["names"]
    idx = [i for i, nm in enumerate(names) if nm in ctx["meta"]]
    se_cl = np.sqrt(np.diag(cov["cluster"]))[idx]
    t_obs = beta[idx] / se_cl
    rng = np.random.default_rng(a.seed)
    if a.boot_weights == "webb":
        vals = np.array([-math.sqrt(1.5), -1.0, -math.sqrt(0.5), math.sqrt(0.5), 1.0, math.sqrt(1.5)])
        draw = lambda: rng.choice(vals, size=G)
    else:
        draw = lambda: rng.choice([-1.0, 1.0], size=G)
    Ai = Ainv[idx]
    tstar = np.empty((a.boot_reps, len(idx)))
    for bi in range(a.boot_reps):
        wv = draw()
        delta = Ainv @ (S.T @ wv)
        Sb = wv[:, None] * S - np.einsum("gpq,q->gp", Ag, delta)
        M = Sb.T @ Sb
        v = np.einsum("ip,pq,iq->i", Ai, M, Ai) * c
        tstar[bi] = delta[idx] / np.sqrt(np.maximum(v, 1e-300))
        if (bi + 1) % 200 == 0:
            print(f"[進捗] bootstrap {bi + 1}/{a.boot_reps}", file=sys.stderr, flush=True)
    tab = _irr_table(full, cov, names, idx, ctx["meta"])
    tab["p_normal"] = tab["p_cluster"]
    tab["p_t_G1"] = [_t_sf2(t, G - 1) for t in t_obs]
    absb = np.abs(tstar)
    tab["p_boot"] = (1 + (absb >= np.abs(t_obs)[None, :]).sum(axis=0)) / (a.boot_reps + 1)
    q = np.quantile(absb, 0.95, axis=0)
    tab["irr_low_boot"], tab["irr_high_boot"] = np.exp(tab.coef - q * se_cl), np.exp(tab.coef + q * se_cl)
    q_t = _t_sf2_inv(G - 1)
    tab["irr_low_t"], tab["irr_high_t"] = np.exp(tab.coef - q_t * se_cl), np.exp(tab.coef + q_t * se_cl)
    dm = (tab.group == G_DAS).values
    for col in ("p_normal", "p_t_G1", "p_boot"):
        tab[f"{col}_holm_das"] = np.nan
        tab.loc[dm, f"{col}_holm_das"] = holm(tab.loc[dm, col].values)
        tab[f"{col}_holm_all"] = holm(tab[col].values)
    tab.to_csv(os.path.join(outdir, f"nb_cluster_inference_{tag}.csv"), index=False, encoding="utf-8-sig")
    P(f"\n[DAS の率比(基準 {ref})。正規近似・t({G - 1})・wild cluster score bootstrap の p(DAS 6 比較で Holm 補正)と、区間]")
    P(tab.loc[dm, ["variable", "irr", "irr_low", "irr_high", "irr_low_t", "irr_high_t", "irr_low_boot", "irr_high_boot",
                   "p_normal_holm_das", "p_t_G1_holm_das", "p_boot_holm_das"]].to_string(index=False, float_format=lambda x: f"{x:.4g}"))
    sig = lambda col: set(tab.loc[dm & (tab[col] < 0.05), "variable"])
    P(f"\n有意(Holm<0.05)な DAS 類型: 正規近似 {sorted(sig('p_normal_holm_das'))} / t({G - 1}) {sorted(sig('p_t_G1_holm_das'))} / bootstrap {sorted(sig('p_boot_holm_das'))}")
    nd = (~dm)
    flips = tab.loc[nd & ((tab.p_normal_holm_all < 0.05) != (tab.p_boot_holm_all < 0.05)), "variable"].tolist()
    P(f"共変量(全係数で Holm)で、正規近似と bootstrap の有意性が食い違う変数: {flips if flips else 'なし'}")
    P(f"注意: bootstrap の p の下限は 1/({a.boot_reps}+1) = {1 / (a.boot_reps + 1):.4f}(Holm 後は最大 6 倍)。有意水準 0.05 での判定には 999 回で足りるが、0.001 を示すには --boot-reps 9999 にする。")
    P("注意: 区間は対称なスチューデント化 bootstrap の 95% 点(|t*| の分位点)で作る。Webb の重みは G が小さいとき Rademacher より分布が滑らか。")
    txt = "\n".join(lines)
    print(txt)
    with open(os.path.join(outdir, f"check_cluster_{tag}.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    print("保存先:", outdir)


def _gram_w(X, w=None, chunk=100000):
    """v045: X'X(w があれば X'WX)・列和・重みの和を、行を分けて足し上げる(65 万行 × 100 列でも設計行列のコピーを作らない)"""
    n, p = X.shape
    G = np.zeros((p, p))
    cs = np.zeros(p)
    sw = 0.0
    for s0 in range(0, n, chunk):
        Xc = X[s0:s0 + chunk]
        if w is None:
            G += Xc.T @ Xc
            cs += Xc.sum(axis=0)
            sw += float(len(Xc))
        else:
            wc = w[s0:s0 + chunk]
            G += Xc.T @ (Xc * wc[:, None])
            cs += wc @ Xc
            sw += float(wc.sum())
    return G, cs, sw


def _corr_from_gram(G, cs, sw):
    """切片の列(先頭)を除き、(重みつき)平均で中心化した相関行列を返す。ばらつきのない列は相関 0 とし、戻り値の 2 番目でその印を返す"""
    m = cs / sw
    C = (G - sw * np.outer(m, m))[1:, 1:]
    sd = np.sqrt(np.clip(np.diag(C), 0.0, None))
    ok = sd > 1e-12
    s_ = np.where(ok, sd, 1.0)
    R = C / np.outer(s_, s_)
    R[~ok, :] = 0.0
    R[:, ~ok] = 0.0
    R[np.arange(len(sd)), np.arange(len(sd))] = 1.0
    return R, ~ok


def _vif_diag(R):
    """VIF_j = (R^-1)_jj(相関行列の逆行列の対角)= 1/(1−R²_j)。条件数が大きいときは擬似逆行列にして印を返す"""
    try:
        cond = float(np.linalg.cond(R))
        Ri = np.linalg.inv(R) if cond < 1e12 else np.linalg.pinv(R)
    except np.linalg.LinAlgError:
        cond = float("inf")
        Ri = np.linalg.pinv(R)
    return np.diag(Ri).copy(), cond


def _gvif(R, idx):
    """一般化 VIF(Fox & Monette 1992): det(R_BB) det(R_rest) / det(R)。k 列のブロックは GVIF^(1/(2k)) が、1 列の VIF の平方根(標準誤差の拡大)に相当する"""
    k = len(idx)
    sidx = set(idx)
    rest = [i for i in range(R.shape[0]) if i not in sidx]
    s_all = np.linalg.slogdet(R)[1]
    s_b = np.linalg.slogdet(R[np.ix_(idx, idx)])[1]
    s_r = np.linalg.slogdet(R[np.ix_(rest, rest)])[1] if rest else 0.0
    g = math.exp(s_b + s_r - s_all)
    return g, g ** (1.0 / (2 * k))


def check_vif(a, outdir):
    """v045: 多重共線性の診断(査読コメント対応)。主モデルと同じ設計行列(切片・雑誌と出版年の固定効果・説明変数)で次を出す。
    (i) 固定効果込みの VIF: 各列を他のすべての列で回帰した決定係数から 1/(1−R²)。NB の最終の重み(mu/(1+alpha·mu))つきと、重みなしの 2 通り。標準誤差は約 √VIF 倍に拡がる。
    (ii) 共変量だけの VIF(固定効果を入れない参考値、重みなし)。
    (iii) ブロック(DAS の類型、責任著者の国など、複数の列で 1 つの変数になるもの)の GVIF と GVIF^(1/(2df))。
    VIF は推定の精度(標準誤差)に関する指標で、偏りを示すものではない。DAS の類型の VIF が小さければ、共変量との相関で DAS の係数が不安定になってはいない。"""
    ctx, ref, log = _check_ctx(a)
    tag = _tag(a.dv)
    X, y, off = ctx["X"], ctx["y"], ctx.get("offset")
    names = ctx["names"]
    n, p = X.shape
    thr = float(getattr(a, "vif_threshold", 5.0))
    lines = []
    P = lines.append
    P(f"多重共線性の診断 ({VERSION}) 従属変数 {a.dv} / 基準 {ref} / 行数 {n:,} / 列数 {p}(切片を含む)/ FE={a.nb_fe}")
    P(log[-1])
    print("[進捗] NB を推定して重みを得る", file=sys.stderr, flush=True)
    full = nb_fit(X, ctx["nbd"], offset=off)
    mu, alpha = full["mu"], full["alpha"]
    w = mu / (1.0 + alpha * mu)
    print("[進捗] 相関行列と VIF を計算", file=sys.stderr, flush=True)
    Gw, csw, sww = _gram_w(X, w)
    Gu, csu, swu = _gram_w(X, None)
    Rw, zw = _corr_from_gram(Gw, csw, sww)
    Ru, zu = _corr_from_gram(Gu, csu, swu)
    nm = list(names[1:])
    vif_w, cond_w = _vif_diag(Rw)
    vif_u, cond_u = _vif_diag(Ru)
    is_fe = np.array([x.startswith("fe_") for x in nm])
    cov_idx = np.where(~is_fe)[0]
    vif_c = np.full(len(nm), np.nan)
    cond_c = float("nan")
    if len(cov_idx) >= 2:
        v_, cond_c = _vif_diag(Ru[np.ix_(cov_idx, cov_idx)])
        vif_c[cov_idx] = v_
    else:
        vif_c[cov_idx] = 1.0
    meta = ctx["meta"]
    das = set(ctx["das_cols"])
    grp = [(meta[x]["group"] if x in meta else "固定効果") for x in nm]
    tab = pd.DataFrame({"variable": nm, "group": grp, "is_das": [x in das for x in nm], "vif_fe_weighted": vif_w, "vif_fe_unweighted": vif_u,
                        "vif_covariates_only": vif_c, "sqrt_vif_fe_weighted": np.sqrt(np.clip(vif_w, 0, None)),
                        "zero_variance": zw})
    tv = tab[~is_fe].copy()
    P(f"\n[条件数] 固定効果込み 重みつき {cond_w:.3g} / 重みなし {cond_u:.3g} / 共変量だけ {cond_c:.3g}(1e12 以上なら擬似逆行列を使う)")
    if zw.any():
        P(f"[注意] ばらつきのない列(相関 0 として扱う): {[x for x, z in zip(nm, zw) if z]}")
    fmt = lambda x: f"{x:.3f}"
    cols = ["variable", "group", "vif_fe_weighted", "vif_fe_unweighted", "vif_covariates_only", "sqrt_vif_fe_weighted"]
    P(f"\n[DAS の類型(基準 {ref} との対比のダミー)の VIF]")
    P(tv[tv.is_das][cols].to_string(index=False, float_format=fmt))
    ts = tv.sort_values("vif_fe_weighted", ascending=False)
    P(f"\n[説明変数の VIF(固定効果込み・重みつきの大きい順、上位 {min(15, len(ts))})]")
    P(ts.head(15)[cols].to_string(index=False, float_format=fmt))
    P(f"\n[要約] 説明変数 {len(tv)} 個(DAS を含む): 固定効果込み・重みつき VIF の最大 {tv.vif_fe_weighted.max():.2f}(中央値 {tv.vif_fe_weighted.median():.2f})/ "
      f"{thr:g} 以上 {int((tv.vif_fe_weighted >= thr).sum())} 個 / " + ("" if thr == 10 else f"10 以上 {int((tv.vif_fe_weighted >= 10).sum())} 個 / ") +
      f""
      f"DAS の類型の最大 {tv[tv.is_das].vif_fe_weighted.max():.2f}")
    hi = ts[ts.vif_fe_weighted >= thr]
    if len(hi):
        P(f"[{thr:g} 以上の説明変数] " + ", ".join(f"{r.variable}({r.vif_fe_weighted:.2f})" for r in hi.itertuples()))
    # ブロックごとの GVIF(設計行列の列の番号は、切片を除いたので −1)
    rows = []
    for blk, idx in ctx["blocks"].items():
        ix = [i - 1 for i in idx if i >= 1]
        if not ix:
            continue
        gw_, gaw = _gvif(Rw, ix)
        gu_, gau = _gvif(Ru, ix)
        rows.append(dict(block=blk, n_cols=len(ix), is_fe=bool(all(is_fe[i] for i in ix)), gvif_weighted=gw_, gvif_adj_weighted=gaw, gvif_unweighted=gu_, gvif_adj_unweighted=gau))
    gt = pd.DataFrame(rows)
    gv = gt[~gt.is_fe].sort_values("gvif_adj_weighted", ascending=False)
    P("\n[ブロックごとの一般化 VIF(固定効果のブロックを除く、GVIF^(1/(2df)) の大きい順)]")
    P(gv.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    fe_g = gt[gt.is_fe]
    if len(fe_g):
        P("[固定効果のブロック(参考)]  " + "; ".join(f"{r.block}: GVIF^(1/(2df)) {r.gvif_adj_weighted:.2f}" for r in fe_g.itertuples()))
    P("\n読み方: VIF は他の列で説明される度合いを表し、標準誤差が約 √VIF 倍に拡がる目安である(1 なら相関なし)。目安は 5 未満で小さい、5〜10 で注意、10 以上で強い共線性とされるが、境界に理論上の根拠はない。")
    P("      VIF は精度の指標で、偏りは示さない。DAS の類型の VIF が小さければ、共変量との相関で DAS の係数の標準誤差が大きく膨らんではいない。VIF の大きい共変量(例: 出版年・雑誌の固定効果と強く関係する変数)は、DAS の推定には直接は影響しない。")
    P("      固定効果込みの VIF は、雑誌・出版年の固定効果を含む設計行列の列どうしの相関で計算している。重みつきは NB の推定量の分散に対応し、重みなしは通常の最小二乗に対応する。GVIF^(1/(2df)) は、複数列のブロックを 1 変数の VIF の平方根と比べるための量である。")
    txt = "\n".join(lines)
    print(txt)
    tab.to_csv(os.path.join(outdir, f"check_vif_{tag}.csv"), index=False, encoding="utf-8-sig")
    gt.to_csv(os.path.join(outdir, f"check_vif_blocks_{tag}.csv"), index=False, encoding="utf-8-sig")
    with open(os.path.join(outdir, f"check_vif_{tag}.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    print("出力先:", outdir)



# ----------------------------------------------------------------------------- v047: 調整集合の比較(査読コメント: 共変量の多さ・DAG)
ADJ_PRE_DAS = ["n_authors", "n_corresp", "n_orcid", "n_countries", "n_institutions", "collab_any", "equal_contrib_any", "has_funding"]   # DAS に先行すると考える共変量(+ 責任著者の国)
ADJ_DROP_A = ["has_data_citation", "n_supplementary"]                                                  # 論文の表 tab:mediator の A で除く変数
ADJ_DROP_B = ADJ_DROP_A + ["body_words", "n_figures", "n_tables", "n_equations"]                          # 同じく B で除く変数


def _adj_fmt_p(p):
    return "<0.001" if p < 0.001 else f"{p:.3f}"


def check_adjust_sets(a, outdir):
    """v047: 調整集合を替えた DAS の率比の比較。同じ行・同じ固定効果(雑誌+出版年)で、次の集合の NB を推定する。
    FE = 共変量なし(論文の C)/ D = DAS に先行すると考える共変量だけ(著者・機関・国・ORCID・共著の形態・助成・責任著者の国)/
    B・A = 論文の tab:mediator の B・A(媒介の候補を除く)/ Main = 全共変量。D は設計上の判断で、DAG に基づく調整集合ではない。
    集合は入れ子(FE ⊂ D ⊂ B ⊂ A ⊂ Main)。行の集合は Main と同じ(全共変量がそろった行)。"""
    ctx, ref, log = _check_ctx(a)
    tag = _tag(a.dv)
    names, meta = ctx["names"], ctx["meta"]
    das = list(ctx["das_cols"])
    covs = [c for c in ctx["ivs"] if c not in das]
    is_corr = lambda c: meta[c]["group"] == G_CORR
    for lst_name, lst in (("D", ADJ_PRE_DAS), ("A", ADJ_DROP_A), ("B", ADJ_DROP_B)):
        miss = [c for c in lst if c not in covs]
        if miss:
            print(f"[警告] 集合 {lst_name} で指定した変数が設計行列にありません(列名を確かめてください): {miss}", file=sys.stderr)
    defs = {
        "FE": ("共変量なし(固定効果のみ。論文の C)", []),
        "D": ("DAS に先行する共変量だけ", [c for c in covs if c in ADJ_PRE_DAS or is_corr(c)]),
        "B": ("A に加えて本文長・図・表・式の数も除く", [c for c in covs if c not in ADJ_DROP_B]),
        "A": ("データ引用・補足資料数を除く", [c for c in covs if c not in ADJ_DROP_A]),
        "Main": ("全共変量", list(covs)),
    }
    want = [x.strip() for x in a.adjust_sets.split(",") if x.strip()]
    bad = [x for x in want if x not in defs]
    if bad:
        raise SystemExit(f"--adjust-sets に未知の名前があります: {bad}(使えるのは {list(defs)})")
    lines = []
    P = lines.append
    P(f"調整集合の比較 ({VERSION})  従属変数 {a.dv} / 基準 {ref} / 行数 {len(ctx['y']):,} / クラスタ数 {int(ctx['gcodes'].max()) + 1} / FE={a.nb_fe}")
    P(log[-1])
    P("全モデルで同じ行・同じ固定効果(雑誌+出版年)。率比は基準に対する比、95% 区間・p はクラスタ頑健、Holm は DAS の類型の数で調整。")
    P("\n[集合の定義]")
    for k in want:
        P(f"  {k}: {defs[k][0]} — 共変量 {len(defs[k][1])} 個")
        P("     " + (", ".join(defs[k][1]) if defs[k][1] else "(なし)"))
    res = {}
    for k in want:
        kept = set(defs[k][1])
        keep = [i for i, n in enumerate(names) if n == "(切片)" or n.startswith("fe_") or n in das or n in kept]
        nm = [names[i] for i in keep]
        Xs = ctx["X"][:, keep]
        print(f"[進捗] 集合 {k}({len(kept)} 個の共変量、列 {Xs.shape[1]})を推定中", file=sys.stderr, flush=True)
        fit = nb_fit(Xs, ctx["nbd"], offset=ctx.get("offset"))
        cov = nb_cov(fit, Xs, ctx["y"], codes=ctx["gcodes"])
        idx = [i for i, n in enumerate(nm) if n in das]
        t = _irr_table(fit, cov, nm, idx, meta)
        t["p_holm_cluster"] = holm(t.p_cluster.values)
        t["set"] = k
        t["n_covariates"] = len(kept)
        t["llf"] = fit["llf"]
        t["alpha"] = fit["alpha"]
        t["converged"] = fit["converged"]
        res[k] = t
        P(f"  {k}: 対数尤度 {fit['llf']:.1f} / alpha {fit['alpha']:.4f} / 収束 {fit['converged']}")
    P("\n[DAS の率比(Holm 後の p)]")
    cat = list(das)
    hdr = f"{'category':<10}" + "".join(f"{k:>20}" for k in want)
    P(hdr)
    for c in cat:
        row = f"{c:<10}"
        for k in want:
            r = res[k][res[k].variable == c].iloc[0]
            row += f"{r.irr:>9.2f} ({_adj_fmt_p(r.p_holm_cluster):>6})  "
        P(row.rstrip())
    if "Main" in res:
        P("\n[Main に対する、対数率比の最大のずれ(論文 tab:mediator の「at most … on the log scale」と同じ尺度)]")
        m = res["Main"].set_index("variable")
        for k in want:
            if k == "Main":
                continue
            t = res[k].set_index("variable")
            dl = (np.log(t.irr) - np.log(m.irr)).reindex(cat)
            worst = dl.abs().idxmax()
            P(f"  {k}: 最大 {abs(dl[worst]):.3f}({worst})")
            flips = []
            for c in cat:
                same_dir = (t.irr[c] - 1) * (m.irr[c] - 1) > 0
                same_sig = (t.p_holm_cluster[c] < 0.05) == (m.p_holm_cluster[c] < 0.05)
                if not (same_dir and same_sig):
                    flips.append(f"{c}(向き{'同じ' if same_dir else '逆'}・有意{'同じ' if same_sig else '変化'})")
            P(f"     向きまたは Holm 後の有意性が Main と異なる類型: {', '.join(flips) if flips else 'なし'}")
    P("\n注意: D は「DAS に先行する」と私たちが判断した共変量の集合で、DAG から導いた調整集合ではない。どの集合の率比も条件付きの関連であり、DAS を選ぶことの効果ではない。")
    P("      集合は FE ⊂ D ⊂ B ⊂ A ⊂ Main の入れ子。FE の行数は Main と同じなので、論文の C(共変量なしの全行)とは行数が異なりうる。")
    txt = "\n".join(lines)
    print(txt)
    allt = pd.concat([res[k] for k in want], ignore_index=True)
    allt.to_csv(os.path.join(outdir, f"check_adjust_sets_{tag}.csv"), index=False, encoding="utf-8-sig")
    with open(os.path.join(outdir, f"check_adjust_sets_{tag}.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    print("出力先:", outdir)


# ----------------------------------------------------------------------------- v049: WoS 未照合の偏りの感度分析(査読コメント)
def _gap_parse(spec):
    """'KEY:YEAR,KEY:YEAR' -> [(KEY(大文字), YEAR)]。KEY は雑誌名(journal_key)に含まれる文字列、YEAR 以降を除く"""
    out = []
    for item in [x.strip() for x in spec.split(",") if x.strip()]:
        k, _, y = item.rpartition(":")
        if not k or not y.strip().isdigit():
            raise SystemExit(f"--gap-spec の書式は 雑誌名の一部:年 をカンマ区切りで並べる形です(例: ENVIRON:2023,HELIYON:2025): {item!r}")
        out.append((k.strip().upper(), int(y)))
    return out


def _subset_ctx(ctx, mask):
    """mask の行だけを残した NB 用の文脈(固定効果の列のうち定数になった列は外す。クラスタは振り直す)"""
    X = ctx["X"][mask]
    keep = [0] + [j for j in range(1, X.shape[1]) if X[:, j].std() > 1e-12]
    y = ctx["y"][mask]
    gc, _ = pd.factorize(ctx["gcodes"][mask])
    off = ctx["offset"][mask] if ctx.get("offset") is not None else None
    return dict(X=X[:, keep], names=[ctx["names"][j] for j in keep], y=y, nbd=NBData(y), offset=off, gcodes=gc,
                use=ctx["use"].loc[mask] if hasattr(ctx["use"], "loc") else ctx["use"][mask], das_cols=ctx["das_cols"], meta=ctx["meta"])


def check_wos_gap(a, outdir):
    """v049: WoS と照合できなかった論文が集中する期間(既定: IJERPH の 2023 年以降、Heliyon の 2025 年)を除いて主モデルを再推定し、
    DAS の率比が動くかを調べる。Main=全行、Cells=指定の雑誌×期間だけを除く、Journals=指定の雑誌を全期間で除く(より厳しい版)。
    分析は WoS 照合を条件としているため、照合できなかった論文との偏りは測れない。ここでは照合の欠けが集中する期間を落としたときの頑健性だけを見る。"""
    ctx, ref, log = _check_ctx(a)
    tag = _tag(a.dv)
    spec = _gap_parse(a.gap_spec)
    use = ctx["use"]
    jk = use["journal_key"].astype(str).str.upper().values
    yr = np.asarray(ctx["year"], dtype=float)
    cell = np.zeros(len(jk), dtype=bool)
    whole = np.zeros(len(jk), dtype=bool)
    detail = []
    for k, y0 in spec:
        m_j = np.array([k in j for j in jk])
        if not m_j.any():
            print(f"[警告] --gap-spec の {k!r} に当たる雑誌がありません(journal_key を確かめてください)", file=sys.stderr)
        cell |= m_j & (yr >= y0)
        whole |= m_j
        detail.append((k, y0, int((m_j & (yr >= y0)).sum()), int(m_j.sum())))
    sets = [("Main", "全行", np.ones(len(jk), dtype=bool)),
            ("Cells", "指定の雑誌×期間を除く", ~cell),
            ("Journals", "指定の雑誌を全期間で除く", ~whole)]
    lines = []
    P = lines.append
    P(f"WoS 未照合期間を除いた感度分析 ({VERSION})  従属変数 {a.dv} / 基準 {ref} / FE={a.nb_fe}")
    P(log[-1])
    if a.dv == "review_days":
        P("[注意] 査読期間のモデルは WoS 照合を条件にしていない。この分析は被引用数(--dv wos_TC)のためのもの。")
    P("[除く条件] --gap-spec " + a.gap_spec)
    for k, y0, n_c, n_j in detail:
        P(f"   {k}: {y0} 年以降 {n_c:,} 行 / 雑誌全体 {n_j:,} 行")
    P("\n[DAS の類型の件数(全行・除いた行・残った行)]")
    das = list(ctx["das_cols"])
    cnt = pd.DataFrame({"all": use[das].sum(), "excluded_cells": use.loc[cell, das].sum() if hasattr(use, "loc") else 0,
                        "kept_cells": use.loc[~cell, das].sum()})
    cnt["share_in_excluded_%"] = 100 * cnt["excluded_cells"] / max(int(cell.sum()), 1)
    cnt["share_in_kept_%"] = 100 * cnt["kept_cells"] / max(int((~cell).sum()), 1)
    P("(DAS の列は基準 F との対比のダミー。基準 F の件数は含まれない。連続量を標準化した列ではなく 0/1 の列)")
    P(cnt.round(1).to_string())
    res = {}
    for k, label, mask in sets:
        sub = _subset_ctx(ctx, mask)
        print(f"[進捗] 集合 {k}({label}、{int(mask.sum()):,} 行)を推定中", file=sys.stderr, flush=True)
        fit = nb_fit(sub["X"], sub["nbd"], offset=sub["offset"])
        cov = nb_cov(fit, sub["X"], sub["y"], codes=sub["gcodes"])
        idx = [i for i, n in enumerate(sub["names"]) if n in das]
        t = _irr_table(fit, cov, sub["names"], idx, ctx["meta"])
        t["p_holm_cluster"] = holm(t.p_cluster.values)
        t["set"] = k
        t["n_rows"] = int(mask.sum())
        t["n_clusters"] = int(sub["gcodes"].max()) + 1
        t["converged"] = fit["converged"]
        res[k] = t
        P(f"  {k}: {label} / 行数 {int(mask.sum()):,} / クラスタ数 {int(sub['gcodes'].max()) + 1} / 収束 {fit['converged']}")
    keys = [k for k, _, _ in sets]
    P("\n[DAS の率比(Holm 後の p)]")
    P(f"{'category':<10}" + "".join(f"{k:>20}" for k in keys))
    for c in das:
        row = f"{c:<10}"
        for k in keys:
            r = res[k][res[k].variable == c]
            if r.empty:
                row += f"{'n.e.':>20}"
            else:
                r = r.iloc[0]
                row += f"{r.irr:>9.2f} ({_adj_fmt_p(r.p_holm_cluster):>6})  "
        P(row.rstrip())
    P("\n[Main に対する対数率比の最大のずれ]")
    m = res["Main"].set_index("variable")
    for k in keys[1:]:
        t = res[k].set_index("variable")
        dl = (np.log(t.irr) - np.log(m.irr)).reindex(das)
        worst = dl.abs().idxmax()
        flips = []
        for c in das:
            if c not in t.index:
                continue
            same_dir = (t.irr[c] - 1) * (m.irr[c] - 1) > 0
            same_sig = (t.p_holm_cluster[c] < 0.05) == (m.p_holm_cluster[c] < 0.05)
            if not (same_dir and same_sig):
                flips.append(f"{c}(向き{'同じ' if same_dir else '逆'}・有意{'同じ' if same_sig else '変化'})")
        P(f"  {k}: 最大 {abs(dl[worst]):.3f}({worst}) / 向きまたは Holm 後の有意性が Main と異なる類型: {', '.join(flips) if flips else 'なし'}")
    P("\n注意: 照合できなかった論文は標本に入っていないので、その偏りそのものは測れない。除いた行は照合の欠けが集中する期間の照合できた論文で、"
      "率比が動かなければ、この期間が結果を左右していないことを示す。")
    txt = "\n".join(lines)
    print(txt)
    allt = pd.concat([res[k] for k in keys], ignore_index=True)
    allt.to_csv(os.path.join(outdir, f"check_wos_gap_{tag}.csv"), index=False, encoding="utf-8-sig")
    with open(os.path.join(outdir, f"check_wos_gap_{tag}.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    print("出力先:", outdir)


def _t_sf2_inv(df):
    """t 分布の両側 5% 点(scipy がなければ 1.96)"""
    try:
        from scipy import stats
        return float(stats.t.ppf(0.975, df))
    except Exception:
        return 1.96


# ---- (4) NB 尤度に基づく Shapley
def _save_json_atomic(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False)
    os.replace(tmp, path)


def shapley_nb(a, outdir):
    """NB の対数尤度の改善(固定効果だけのモデルに対する ΔLL)を、説明変数のグループ間で Shapley 配分する。OLS の代理モデルを使わない。
    プレーヤーはグループ(DAS・著者・参考文献と助成・図表と文章量・題名・責任著者の国、経過時間を入れたときはそれも)で、グループ数 k に対し 2^k 回の NB を推定する。
    v024: 全行で実行する前提(--nb-sample を付けない)。部分集合ごとの ΔLL を shapley_nb_cache_<tag>.json に保存し、中断しても同じ設定なら続きから再開する。
    親モデル(グループを 1 つ少なくしたモデル)の係数を初期値にし、未収束なら反復数を倍にして推定し直す"""
    ctx, ref, log = _check_ctx(a)
    tag = _tag(a.dv)
    X, nbd, names, meta, off = ctx["X"], ctx["nbd"], ctx["names"], ctx["meta"], ctx.get("offset")
    groups = {}
    for i, nm in enumerate(names):
        if nm in meta:
            groups.setdefault(meta[nm]["group"], []).append(i)
    base = [i for i, nm in enumerate(names) if nm not in meta]
    players = list(groups)
    k = len(players)
    n_obs = int(len(ctx["y"]))
    maxit = int(getattr(a, "shapley_maxit", 100))
    t_begin = time.time()
    sample_note = ""
    if a.nb_sample:
        sample_note = (f"[注意] --nb-sample {a.nb_sample:,} による一部の行の暫定値です。"
                       "論文には --nb-sample を付けず全行で実行した結果を使ってください")
        print(sample_note, file=sys.stderr, flush=True)
    print(f"[進捗] プレーヤー {k} 個({players})→ NB を 2^{k} - 1 = {2 ** k - 1} 回推定します。N = {n_obs:,} / 列数 {X.shape[1]}"
          f"(行数が多いと時間がかかります。中断しても同じ設定で再実行すれば続きから再開します)", file=sys.stderr, flush=True)

    sig = json.loads(json.dumps({
        "dv": a.dv, "n": n_obs, "p": int(X.shape[1]), "nb_fe": a.nb_fe, "nb_sample": int(a.nb_sample),
        "seed": int(a.seed) if a.nb_sample else None, "exposure": getattr(a, "exposure", "off"),
        "players": players, "n_vars": {g: len(groups[g]) for g in players}, "y_sum": float(ctx["y"].sum()), "offset": off is not None,
    }, ensure_ascii=False))
    cache_path = os.path.join(outdir, f"shapley_nb_cache_{tag}.json")
    store = {"signature": sig, "ll0": None, "values": {}, "converged": {}, "secs": {}}
    if os.path.exists(cache_path):
        old = None
        if not getattr(a, "shapley_fresh", False):
            try:
                with open(cache_path, encoding="utf-8") as fh:
                    old = json.load(fh)
            except Exception:
                old = None
        if old is not None and old.get("signature") == sig:
            store = old
            print(f"[再開] {cache_path} の {len(store['values'])} 件を使います", file=sys.stderr, flush=True)
        else:
            print(f"[注意] {cache_path} は設定が異なるか破棄指定のため、最初から推定します", file=sys.stderr, flush=True)

    f0 = nb_fit(X[:, base], nbd, offset=off, maxit=maxit)
    ll0 = f0["llf"]
    if store["ll0"] is not None and abs(store["ll0"] - ll0) > 1e-4 * (1.0 + abs(ll0)):
        print("[注意] キャッシュの基準尤度が今回と合わないため、最初から推定します", file=sys.stderr, flush=True)
        store = {"signature": sig, "ll0": None, "values": {}, "converged": {}, "secs": {}}
    store["ll0"] = float(ll0)
    betas = {frozenset(): (list(base), f0["beta"].copy(), float(f0["alpha"]))}

    def key_str(s):
        return json.dumps(sorted(s), ensure_ascii=False)
    todo = [frozenset(c) for r in range(1, k + 1) for c in itertools.combinations(sorted(players), r)]
    total = len(todo)
    n_new = sum(1 for s in todo if key_str(s) not in store["values"])
    n_fit, t_fit = 0, 0.0
    for s in todo:
        ks = key_str(s)
        if ks in store["values"]:
            continue
        cols = base + [i for g in sorted(s) for i in groups[g]]
        parent = None
        for g in sorted(s):
            parent = betas.get(s - {g})
            if parent is not None:
                break
        if parent is None:
            parent = betas[frozenset()]
        pcols, pbeta, palpha = parent
        cm = dict(zip(pcols, pbeta))
        b0 = np.array([cm.get(c, 0.0) for c in cols], dtype=float)
        t1 = time.time()
        fr = nb_fit(X[:, cols], nbd, b0=b0, a0=palpha, offset=off, maxit=maxit)
        if not fr["converged"]:
            fr2 = nb_fit(X[:, cols], nbd, b0=fr["beta"], a0=fr["alpha"], offset=off, maxit=2 * maxit)
            if fr2["llf"] >= fr["llf"] - 1e-9:
                fr = fr2
        sec = time.time() - t1
        betas[s] = (cols, fr["beta"].copy(), float(fr["alpha"]))
        store["values"][ks] = float(fr["llf"] - ll0)
        store["converged"][ks] = bool(fr["converged"])
        store["secs"][ks] = round(sec, 1)
        del fr
        _save_json_atomic(cache_path, store)
        n_fit += 1
        t_fit += sec
        left = (n_new - n_fit) * (t_fit / n_fit)
        print(f"[進捗] {len(store['values'])}/{total}  今回 {n_fit}/{n_new}  {sec:,.0f} 秒  残り約 {left / 60:,.1f} 分"
              + ("  [未収束]" if not store["converged"][ks] else ""), file=sys.stderr, flush=True)

    def val(sub):
        key = frozenset(sub)
        return 0.0 if not key else float(store["values"][key_str(key)])
    phi = shapley_exact(players, val)
    full = val(set(players))
    n_nc = sum(1 for v in store["converged"].values() if not v)
    rows = [{"group": g, "n_vars": len(groups[g]), "shapley_dLL": phi[g], "share_of_dLL": phi[g] / full if full > 0 else float("nan"),
             "unique_dLL": full - val(set(players) - {g})} for g in players]
    t = pd.DataFrame(rows).sort_values("shapley_dLL", ascending=False).reset_index(drop=True)
    f_ols = os.path.join(outdir, f"shapley_group_{tag}.csv")
    lines = []
    P = lines.append
    P(f"NB 尤度に基づく Shapley 分解 ({VERSION}) 従属変数 {a.dv} / N {n_obs:,} / 固定効果だけのモデルに対する ΔLL(全説明変数)= {full:,.1f}")
    if sample_note:
        P(sample_note)
    else:
        P(f"全行で推定(標本抽出なし)。推定したモデル {total + 1} 個(未収束 {n_nc} 個)。所要時間 {(time.time() - t_begin) / 60:,.1f} 分(今回の推定 {n_fit} 回)")
    if n_nc:
        P(f"[注意] 未収束のモデルが {n_nc} 個あります(反復を倍にしても収束せず)。値の扱いに注意してください")
    rho, changed = float("nan"), []
    if os.path.exists(f_ols):
        o = pd.read_csv(f_ols)[["group", "share_of_within_r2"]].rename(columns={"share_of_within_r2": "share_ols_within_r2"})
        t = t.merge(o, on="group", how="left")
        t["rank_nb"] = t.share_of_dLL.rank(ascending=False)
        t["rank_ols"] = t.share_ols_within_r2.rank(ascending=False)
        rho = float(t[["rank_nb", "rank_ols"]].corr(method="spearman").iloc[0, 1]) if len(t) > 2 else float("nan")
        changed = [str(g) for g, x, y in zip(t.group, t.rank_nb, t.rank_ols) if x != y]
        P(f"OLS(log(1+y) の within R²)の Shapley の配分 {f_ols} と並べる。順位相関 {rho:.2f}")
    else:
        P(f"[注意] OLS 版の {f_ols} がないため並べません(同じ --dv・--outdir で通常の分析を先に走らせてください)")
    t["n_obs"] = n_obs
    t["nb_sample"] = int(a.nb_sample)
    P(t.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("本文用(NB 版の割合): " + ", ".join(f"{g} {100 * s:.1f}%" for g, s in zip(t.group, t.share_of_dLL)))
    if changed:
        P("OLS 版と順位が異なるグループ: " + ", ".join(changed))
    elif os.path.exists(f_ols):
        P("OLS 版と順位が異なるグループ: なし")
    P("読み方: share_of_dLL は NB の対数尤度の改善のうち各グループに帰属する割合。OLS 版と順位・割合が近ければ、代理モデルの不一致は結論に影響しない。")
    txt = "\n".join(lines)
    print(txt)
    t.to_csv(os.path.join(outdir, f"shapley_nb_group_{tag}.csv"), index=False, encoding="utf-8-sig")
    with open(os.path.join(outdir, f"shapley_nb_{tag}.txt"), "w", encoding="utf-8") as fh:
        fh.write(txt)
    print("保存先:", outdir)



# ---- v021: 査読コメント(分類器の誤分類・分野)への対応
def _relabel_data(d, das_cols, ref, labels, keep_mask):
    """labels(Series)で DAS ダミーを作り直す。基準・類型以外のラベルの行と keep_mask が偽の行は被引用数を欠損にして使わない"""
    cats = [ref] + [c[4:] for c in das_cols]
    ok = labels.isin(cats) & keep_mask
    d.loc[~ok, "tc"] = np.nan
    for c in das_cols:
        d[c] = (labels == c[4:]).astype(float)
    return int(ok.sum())


def _fit_das(d, meta, das_cols, ref, excl, a, label):
    ctx = nb_build(d, meta, das_cols, [c for c in meta if c not in excl and c != "log_review" and c not in das_cols], a, [])
    full = nb_fit(ctx["X"], ctx["nbd"])
    cov = nb_cov(full, ctx["X"], ctx["y"], codes=ctx["gcodes"])
    names = ctx["names"]
    idx = [i for i, n in enumerate(names) if n in ctx["das_cols"]]
    t = _irr_table(full, cov, names, idx, ctx["meta"])
    t["p_holm"] = holm(t.p_cluster.values)
    return ctx, full, cov, idx, t


def check_label_noise(a, outdir):
    """分類器のラベルのばらつきに対する感度: DAS ラベルを (1) アンサンブル(主分析)(2) 3 つの LLM それぞれの単独ラベル
    (3) 3 つの LLM が一致した論文だけ、に替えて主モデルを推定し直し、DAS の率比を並べる"""
    import copy
    if _is_rv(a.dv):
        pass   # 査読期間(--dv review_days)でも使える。IRR は期待日数の比
    a2 = copy.copy(a)
    a2.das_source, a2.das_agree_only = "ensemble", False
    d, meta, das_cols, ref, log = prepare(a2)
    if not all(c in d for c in LLM_COLS):
        sys.exit("LLM のラベル列(das_ds32, das_gpt5, das_mil3)が CSV にありません")
    excl = {c.strip() for c in a.exclude.split(",") if c.strip()}
    tag = _tag(a.dv)
    tc0 = d.tc.copy()
    ens = d.das_label.copy()
    same = (d[LLM_COLS[0]] == d[LLM_COLS[1]]) & (d[LLM_COLS[0]] == d[LLM_COLS[2]]) & (d[LLM_COLS[0]] != "")
    variants = [("ensemble", ens, pd.Series(True, index=d.index)), ("ds32", d.das_ds32, pd.Series(True, index=d.index)),
                ("gpt5", d.das_gpt5, pd.Series(True, index=d.index)), ("mil3", d.das_mil3, pd.Series(True, index=d.index)),
                ("agree3", ens, same)]
    rows, res, lines = [], {}, []
    P = lines.append
    P(f"分類器ラベルの感度分析 ({VERSION}) 従属変数 {a.dv} / 基準 {ref}")
    P(f"3 つの LLM が一致した論文の割合 {same.mean():.1%}(DAS ラベルがある行 {len(d):,} 中)")
    for name, lab, keep in variants:
        print(f"[進捗] {name} を推定中", file=sys.stderr, flush=True)
        d["tc"] = tc0
        n_ok = _relabel_data(d, das_cols, ref, lab, keep)
        cc_ = lab[keep & lab.isin([ref] + [c[4:] for c in das_cols])].value_counts()
        P(f"[{name}] 類型の件数: " + ", ".join(f"{c}={int(cc_.get(c, 0)):,}" for c in [ref] + [c[4:] for c in das_cols]))
        agree_ens = float((lab[keep] == ens[keep]).mean())
        ctx, full, cov, idx, t = _fit_das(d, meta, das_cols, ref, excl, a, name)
        res[name] = (t, len(ctx["y"]), agree_ens)
        for r in t.itertuples():
            rows.append(dict(variant=name, variable=r.variable, irr=r.irr, low=r.irr_low, high=r.irr_high, p_cluster=r.p_cluster,
                             p_holm=r.p_holm, n=len(ctx["y"]), agree_with_ensemble=agree_ens))
    base = res["ensemble"][0].set_index("variable")
    P("\n[DAS の率比(基準 %s)。括弧内は Holm 補正後の p(クラスタ頑健)]" % ref)
    cmp_ = pd.DataFrame({"variable": base.index})
    for name, _, _ in variants:
        t = res[name][0].set_index("variable")
        cmp_[name] = [(f"{t.loc[v, 'irr']:.3f} ({t.loc[v, 'p_holm']:.3g})" if v in t.index else "NA(モデルから外れた)") for v in base.index]
        cmp_[f"dlog_{name}"] = [(math.log(t.loc[v, "irr"]) - math.log(base.loc[v, "irr"]) if v in t.index else float("nan")) for v in base.index]
    P(cmp_[["variable"] + [v[0] for v in variants]].to_string(index=False))
    P("注意: NA は、その類型のラベルがほとんどない(件数が --min-group 未満、またはばらつきがない)ためモデルから外れたことを示す。その行は、基準側に回ったのではなく、推定できなかった。")
    P("\n[主分析(ensemble)との率比の最大のずれ(対数)] " + ", ".join(f"{v[0]}: {cmp_[f'dlog_{v[0]}'].abs().max():.4f}" for v in variants[1:]))
    P("[分析した行数 / アンサンブルのラベルとの一致率] " + ", ".join(f"{k}: {v[1]:,} / {v[2]:.3f}" for k, v in res.items()))
    P("\n読み方: 単独の LLM のラベルや一致した論文だけでも向きと有意性が変わらなければ、アンサンブルの誤分類のばらつきは結論に影響しにくい。"
      "ただし 3 つの LLM は誤りが相関しうるので、独立な誤分類の評価にはならない(--check-misclass を参照)。")
    txt = "\n".join(lines)
    print(txt)
    pd.DataFrame(rows).to_csv(os.path.join(outdir, f"nb_label_noise_{tag}.csv"), index=False, encoding="utf-8-sig")
    with open(os.path.join(outdir, f"check_label_noise_{tag}.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    print("保存先:", outdir)


def check_misclass(a, outdir):
    """誤分類の確率的感度分析(確率的バイアス分析)。参照セット(人手のラベル)での混同行列 C[真, 予測] を --confusion-csv で与える。
    各反復で (1) 混同行列の各行を Dirichlet(件数+--noise-prior)から引き(参照セットの小ささによる不確かさ)、
    (2) 真の類型の割合を EM で推定し、(3) 予測ラベルごとに P(真 | 予測) を作って各論文の真のラベルを引き直し、
    (4) NB を推定し直す。--noise-reps 回の結果を Rubin の規則(クラスタ頑健な分散を使う)で統合する。誤分類は被引用数と無関係(非差異的)と仮定する"""
    if not a.confusion_csv:
        sys.exit("--check-misclass には --confusion-csv が必要です。形式: 1 列目=人手(真)の類型、1 行目=予測した類型、中身=件数の正方行列(CSV)。"
                 "類型の並びは何でもよいが、分析に使う全類型(基準を含む)が行・列の両方にあること。"
                 "交差検証の予測(out-of-fold)から作るのが望ましい")
    d, meta, das_cols, ref, log = prepare(a)
    excl = {c.strip() for c in a.exclude.split(",") if c.strip()}
    tag = _tag(a.dv)
    cats = [ref] + [c[4:] for c in das_cols]
    conf = pd.read_csv(os.path.expanduser(a.confusion_csv), index_col=0)
    conf.index, conf.columns = [str(x).strip() for x in conf.index], [str(x).strip() for x in conf.columns]
    miss = [c for c in cats if c not in conf.index or c not in conf.columns]
    if miss:
        sys.exit(f"混同行列に類型 {miss} の行または列がありません(必要な類型: {cats})")
    cnt = conf.loc[cats, cats].values.astype(float)
    K = len(cats)
    print("[進捗] 主モデル(ラベルを替えない)を推定中", file=sys.stderr, flush=True)
    ctx, full, cov, idx, t0 = _fit_das(d, meta, das_cols, ref, excl, a, "main")
    X, y, nbd, gc, names = ctx["X"], ctx["y"], ctx["nbd"], ctx["gcodes"], ctx["names"]
    das_idx = {n: i for i, n in enumerate(names) if n in ctx["das_cols"]}
    pred = pd.Categorical(d.loc[ctx["use"].index, "das_label"].values, categories=cats).codes
    n = len(pred)
    p_pred = np.bincount(pred, minlength=K) / n
    rng = np.random.default_rng(a.seed)
    betas, vars_ = [], []
    pis, ppv, ncls = [], [], []
    R = a.noise_reps
    for r in range(R):
        print(f"[進捗] 反復 {r + 1}/{R}", file=sys.stderr, flush=True)
        C = np.vstack([rng.dirichlet(cnt[k] + a.noise_prior) for k in range(K)])      # P(予測 j | 真 k)
        pi = p_pred.copy()
        for _ in range(500):                                                           # 既知の誤分類確率のもとでの真の割合(EM)
            post = C * pi[:, None]
            post = post / post.sum(axis=0, keepdims=True)
            pi_new = post @ p_pred
            if np.abs(pi_new - pi).max() < 1e-10:
                pi = pi_new
                break
            pi = pi_new
        Q = C * pi[:, None]
        Q = Q / Q.sum(axis=0, keepdims=True)                                           # P(真 k | 予測 j)
        new = np.empty(n, dtype=int)
        for j in range(K):
            ii = np.where(pred == j)[0]
            if len(ii):
                new[ii] = rng.choice(K, size=len(ii), p=Q[:, j])
        nc_r = np.bincount(new, minlength=K)
        ncls.append(nc_r)                                                             # v022: この反復で引いた真の類型ごとの件数
        for nm, i in das_idx.items():
            X[:, i] = (new == cats.index(nm[4:])).astype(float)
        fr = nb_fit(X, nbd, b0=full["beta"], a0=full["alpha"])
        cv = nb_cov(fr, X, y, codes=gc)
        ii = [das_idx[c] for c in ctx["das_cols"]]
        bb, vv = fr["beta"][ii].copy(), np.diag(cv["cluster"])[ii].copy()
        for q, c_ in enumerate(ctx["das_cols"]):                                        # v023: 件数が少なすぎる類型の係数は不定なので、この反復では使わない
            if nc_r[cats.index(c_[4:])] < a.noise_min_count:
                bb[q], vv[q] = np.nan, np.nan
        betas.append(bb)
        vars_.append(vv)
        pis.append(pi)
        ppv.append(np.array([Q[j, j] for j in range(K)]))
    betas, vars_ = np.array(betas), np.array(vars_)
    Rk = np.isfinite(betas).sum(axis=0)                                                # v023: 類型ごとの有効な反復数
    with np.errstate(all="ignore"):
        qbar, ubar = np.nanmean(betas, axis=0), np.nanmean(vars_, axis=0)
        B = np.where(Rk > 1, np.nanvar(betas, axis=0, ddof=1), np.nan)
        T = ubar + (1 + 1 / Rk) * B
        rr = np.where(ubar > 0, (1 + 1 / Rk) * B / ubar, np.nan)
        dfr = (Rk - 1) * (1 + 1 / np.where(rr > 0, rr, np.nan)) ** 2
    dfr = np.where(np.isfinite(dfr), dfr, 1e6)
    se = np.sqrt(T)
    pv = np.array([_t_sf2(q / s, df) if np.isfinite(q) and np.isfinite(s) else np.nan for q, s, df in zip(qbar, se, dfr)])
    try:
        from scipy import stats
        crit = np.array([stats.t.ppf(0.975, df) for df in dfr])
    except Exception:
        crit = np.full(len(dfr), 1.96)
    fmi = (rr + 2 / (dfr + 3)) / (rr + 1)
    out = pd.DataFrame({"variable": ctx["das_cols"], "irr_naive": t0.irr.values, "p_holm_naive": t0.p_holm.values,
                        "irr_pooled": np.exp(qbar), "irr_low": np.exp(qbar - crit * se), "irr_high": np.exp(qbar + crit * se),
                        "p_pooled": pv, "p_holm_pooled": np.where(np.isfinite(pv), holm(np.where(np.isfinite(pv), pv, 1.0)), np.nan),
                        "between_sd": np.sqrt(B), "fmi": fmi, "n_valid_reps": Rk,
                        "mean_n": [float(np.mean([c_[cats.index(v[4:])] for c_ in ncls])) for v in ctx["das_cols"]],
                        "dlog_vs_naive": qbar - np.log(t0.irr.values)})
    lines = []
    P = lines.append
    P(f"誤分類の確率的感度分析 ({VERSION}) 従属変数 {a.dv} / 基準 {ref} / 反復 {R} / 混同行列 {a.confusion_csv}(Dirichlet の事前件数 {a.noise_prior})")
    P(f"分析した行 {n:,}。参照セットの件数: " + ", ".join(f"{c}={int(cnt[k].sum())}" for k, c in enumerate(cats)))
    P("[参照セットでの再現率(真の類型ごとの正しく予測された割合)] " + ", ".join(f"{c}={cnt[k, k] / max(cnt[k].sum(), 1):.3f}" for k, c in enumerate(cats)))
    P("[予測ラベルの割合と、EM で推定した真の割合(平均)] " + ", ".join(f"{c}: {p_pred[k]:.3f}→{np.mean([p[k] for p in pis]):.3f}" for k, c in enumerate(cats)))
    nc = np.array(ncls)
    P("[件数: 予測ラベル → 引いた真の類型(反復の平均、最小〜最大)] " + ", ".join(
        f"{c}: {int((pred == k).sum()):,}→{nc[:, k].mean():,.0f}({nc[:, k].min():,}〜{nc[:, k].max():,})" for k, c in enumerate(cats)))
    P("[予測 j のとき真も j である確率(平均)] " + ", ".join(f"{c}={np.mean([p[k] for p in ppv]):.3f}" for k, c in enumerate(cats)))
    P("\n[DAS の率比(基準 %s)] naive=ラベルを替えない主モデル / pooled=Rubin の規則で統合(分類の不確かさを含む)/ fmi=誤分類の不確かさによる情報の欠落の割合" % ref)
    P(out.to_string(index=False, float_format=lambda x: f"{x:.4g}"))
    bad = [f"{v[4:]}({int(k)}/{R})" for v, k in zip(ctx["das_cols"], Rk) if k < R]
    if bad:
        P(f"注意(v023): 引いた件数が --noise-min-count({a.noise_min_count})未満の反復を除いた類型(有効な反復数/全反復): " + ", ".join(bad)
          + "。有効な反復が 2 回未満の類型は NA。有効な反復が少ない類型の統合値は、件数の多い反復だけに条件づけた値で、信頼できない。")
    P("\n[naive との率比の最大のずれ(対数)] %.4f" % float(np.nanmax(np.abs(out.dlog_vs_naive))))
    P("読み方: pooled の向きと Holm 後の有意性が naive と同じなら、混同行列が表す程度の誤分類は結論を変えない。"
      "非差異的な誤分類は多くの場合、率比を 1 の方へ引き寄せる(例外あり)。混同行列が参照セット(雑誌ごとに 120 件の層化)に由来するため、"
      "雑誌によって誤り方が違えば推定は偏る。誤分類が被引用数や査読期間と関連する(差異的)場合は扱えない。")
    txt = "\n".join(lines)
    print(txt)
    out.to_csv(os.path.join(outdir, f"nb_misclass_{tag}.csv"), index=False, encoding="utf-8-sig")
    with open(os.path.join(outdir, f"check_misclass_{tag}.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    print("保存先:", outdir)


# ---- v022: check_misclass の実装が論文の説明と合っているかを確認する(このファイルを ast で読むだけで、何も実行しない)
AUDIT_MISCLASS_CHECKS = [
    ("(1) 混同行列を CSV から読む(行=人手の真の類型、列=予測)", [r"read_csv", r"confusion"], "行・列の向き(転置 .T の有無)。"),
    ("(1') 行・列の順序を類型の順にそろえる", [r"conf\.loc\[|reindex|cats"], "混同行列の順序と DAS 類型の順序の一致。"),
    ("(2) Dirichlet から混同行列を引く", [r"dirichlet"], "行ごと(真の類型ごと)に引いているか。"),
    ("(2') 事前件数(--noise-prior、既定 0.5)", [r"noise_prior"], "既定値とログの値の一致。"),
    ("(2'') 反復ごとに引き直す", [r"for\s+\w+\s+in\s+range\(R\)"], "Dirichlet が反復の内側か。"),
    ("(3) EM で真の割合を推定", [r"pi_new", r"post"], "更新式 π = P(真|予測) の予測割合での平均。"),
    ("(3') EM は反復ごとに、その反復の混同行列で行う", [r"for\s+_\s+in\s+range\(500\)"], "EM が反復の内側か。"),
    ("(4) 予測ラベルを条件として真の類型を事後確率で引く", [r"rng\.choice", r"Q\["], "多重代入(1つ引く)か、重み付けか。"),
    ("(5) 割り当てた類型で主 NB モデルを再推定", [r"nb_fit", r"nb_cov"], "同じ行・同じ固定効果で再推定しているか。"),
    ("(6) Rubin の規則で統合", [r"\(1 \+ 1 / R\)", r"fmi"], "総分散 = 平均 + (1 + 1/m) × 反復間の分散。"),
    ("(6') 統合後の p に Holm", [r"holm\(pv\)"], "Holm を6類型にかけているか。"),
    ("(7) 乱数の種", [r"default_rng\(a\.seed\)"], "種を固定しているか。"),
]


def audit_misclass(a):
    """--audit-misclass: check_misclass(と、それが呼ぶ同ファイル内の関数)のソースを行番号つきで書き出し、
    論文 2.5節の説明の各主張に対応する記述があるかを表にする。実行はせず ast で読むだけ。"""
    import ast
    path = os.path.abspath(__file__)
    with open(path, encoding="utf-8") as f:
        src = f.read()
    lines = src.splitlines()
    tree = ast.parse(src)
    funcs = {n.name: n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    root = "check_misclass"

    def called(fn):
        out = set()
        for n in ast.walk(fn):
            if isinstance(n, ast.Call):
                f_ = n.func
                out.add(f_.id if isinstance(f_, ast.Name) else getattr(f_, "attr", ""))
        return out
    names = [root]
    helpers = sorted(c for c in called(funcs[root]) if c in funcs and c != root)
    out = [f"対象ファイル: {path}({len(lines)} 行) / バージョン {VERSION}", f"確認する関数: {root}(呼んでいる同ファイル内の関数: {', '.join(helpers)}。必要ならその定義も送ってください)", ""]
    body = "\n".join("\n".join(lines[funcs[n].lineno - 1:funcs[n].end_lineno]) for n in names)
    out += ["=" * 70, "[A] 説明の各主張に対応する記述(有=該当する語や式がある、無=見つからない。内容の正しさは [B] で確認する)", "=" * 70]
    for title, pats, note in AUDIT_MISCLASS_CHECKS:
        ok = all(re.search(p, body) for p in pats)
        out.append(f"  [{'有' if ok else '無'}] {title}")
        out.append(f"        確認点: {note}")
    out += ["", "=" * 70, "[B] 関数のソース(行番号つき)", "=" * 70]
    for nm in names:
        fn = funcs[nm]
        out.append(f"\n--- def {nm}({fn.lineno}–{fn.end_lineno} 行) ---")
        out += [f"{i:5d}  {lines[i - 1]}" for i in range(fn.lineno, fn.end_lineno + 1)]
    txt = "\n".join(out)
    print(txt)
    dst = os.path.join(os.path.expanduser(a.outdir), "audit_check_misclass.txt")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(txt + "\n")
    print("保存先:", dst)


# ----------------------------------------------------------------------------- v025: 追加の確認(--check-extra)
# 査読・論文の弱点に対応する 6 つの確認。どれも全行で推定する(--nb-sample は無視して 0 に固定)。
#   tost    同等性検定(TOST): 「DAS の関連は小さい」を検定で支える
#   meta    雑誌別の率比のメタ分析(変量効果・I²・予測区間)。nb_by_journal.csv を読むだけで、推定し直さない
#   loo     雑誌を 1 つずつ除いた主モデルの再推定
#   revalt  査読期間のモデル違い(log OLS・ガンマ GLM・M を除く・M を F に統合)
#   age     経過年数の柔軟な調整(log 経過年数の折れ線スプライン、雑誌別の傾き)
#   field   分野(--field-col)を加えたモデルとの比較と、分野ブロックの LRT
def _t_ppf(q, df):
    try:
        from scipy import stats
        return float(stats.t.ppf(q, df))
    except Exception:
        return {0.95: 1.645, 0.975: 1.96}.get(q, 1.96)


def _t_sf1(t, df):
    """片側(上側)p"""
    try:
        from scipy import stats
        return float(stats.t.sf(t, df))
    except Exception:
        return float(0.5 * math.erfc(t / math.sqrt(2)))


def _fit_main(ctx, maxit=100):
    f = nb_fit(ctx["X"], ctx["nbd"], offset=ctx.get("offset"), maxit=maxit)
    if not f["converged"]:
        f = nb_fit(ctx["X"], ctx["nbd"], b0=f["beta"], a0=f["alpha"], offset=ctx.get("offset"), maxit=maxit * 3)
    return f


def _das_idx(ctx):
    return [i for i, n in enumerate(ctx["names"]) if n in ctx["das_cols"]]


def _das_table(ctx, full, cov):
    t = _irr_table(full, cov, ctx["names"], _das_idx(ctx), ctx["meta"])
    t["p_holm"] = holm(t.p_cluster.values)
    return t


def _fit_ctx(d, meta, das_cols, excl, a, drop_groups=()):
    """主モデル(NB2・雑誌+年の固定効果・雑誌×年クラスタ)を推定する。drop_groups の共変量グループは外す"""
    base_ivs = [c for c in meta if c not in excl and c != "log_review" and c not in das_cols and meta[c]["group"] not in drop_groups]
    ctx = nb_build(d, meta, das_cols, base_ivs, a, [])
    full = _fit_main(ctx)
    cov = nb_cov(full, ctx["X"], ctx["y"], codes=ctx["gcodes"])
    return ctx, full, cov, _das_table(ctx, full, cov)


def _fmt_irr(t, v):
    if v not in t.index:
        return "NA"
    return f"{t.loc[v, 'irr']:.3f} ({t.loc[v, 'p_holm']:.3g})"


def _compare_table(res, order, P, note=""):
    """res: {名前: DAS の率比の表}。変数×名前の表(率比と Holm 後の p)と、最初の名前との対数のずれを出す"""
    base = res[order[0]].set_index("variable")
    tab = pd.DataFrame({"variable": base.index})
    for nm in order:
        t = res[nm].set_index("variable")
        tab[nm] = [_fmt_irr(t, v) for v in base.index]
    P(tab.to_string(index=False))
    if note:
        P(note)
    P("[" + order[0] + " との率比の最大のずれ(対数)] " + ", ".join(
        f"{nm}: " + (f"{max(abs(math.log(res[nm].set_index('variable').loc[v, 'irr']) - math.log(base.loc[v, 'irr'])) for v in base.index if v in res[nm].set_index('variable').index):.4f}")
        for nm in order[1:]))


# ---- tost
def _extra_tost(a, d, meta, das_cols, ref, excl, outdir, tag, P):
    ctx, full, cov, t = _fit_ctx(d, meta, das_cols, excl, a)
    G = int(ctx["gcodes"].max()) + 1
    df = G - 1
    bounds = [float(x) for x in a.tost_bounds.split(",") if x.strip()]
    tc90 = _t_ppf(0.95, df)
    P(f"\n===== 同等性検定(TOST) =====  N={len(ctx['y']):,}(全行) / クラスタ {G} / t({df}) / 主モデルの収束 {full['converged']}")
    P("率比が [1/(1+δ), 1+δ] に入るかを、t(G−1) の 2 つの片側検定(クラスタ頑健 SE)で調べる。p_tost は 2 つの片側 p の大きい方、Holm は DAS 6 比較にかける。"
      "「差がある」は同じ t(G−1) の両側検定の Holm 補正後 p < 0.05。")
    rows = []
    for r in t.itertuples():
        b, se = r.coef, r.se_cluster
        p_nh = _t_sf2(b / se, df)
        for bd in bounds:
            dl = math.log(1 + bd)
            rows.append(dict(variable=r.variable, bound=bd, irr=r.irr, ci90_low=math.exp(b - tc90 * se), ci90_high=math.exp(b + tc90 * se),
                             p_tost=max(_t_sf1((b + dl) / se, df), _t_sf1((dl - b) / se, df)), p_diff_t=p_nh,
                             min_ratio_bound=math.exp(abs(b) + tc90 * se)))
    r_ = pd.DataFrame(rows)
    r_["p_diff_t_holm"] = np.nan
    for bd in bounds:
        m = r_.bound == bd
        r_.loc[m, "p_tost_holm"] = holm(r_.loc[m, "p_tost"].values)
    first = r_.bound == bounds[0]
    ph = dict(zip(r_.loc[first, "variable"], holm(r_.loc[first, "p_diff_t"].values)))
    r_["p_diff_t_holm"] = r_.variable.map(ph)

    def cls(x):
        eq, df_ = x.p_tost_holm < 0.05, x.p_diff_t_holm < 0.05
        return ("差あり・かつ同等の範囲内" if eq and df_ else "同等(差なし)" if eq else "差あり・範囲外" if df_ else "どちらとも言えない")
    r_["class"] = r_.apply(cls, axis=1)
    r_.to_csv(os.path.join(outdir, f"check_extra_tost_{tag}.csv"), index=False, encoding="utf-8-sig")
    for bd in bounds:
        s = r_[r_.bound == bd]
        P(f"\n[δ = {bd:.2f}: 率比の同等の範囲 {1 / (1 + bd):.3f}〜{1 + bd:.3f}]")
        P(s[["variable", "irr", "ci90_low", "ci90_high", "p_tost_holm", "p_diff_t_holm", "class"]].to_string(index=False, float_format=lambda x: f"{x:.4g}"))
    s = r_[r_.bound == bounds[0]]
    P("\n[同等と言える最小の範囲(90% 区間の絶対値の大きい側 = 1 + δ*)] " + ", ".join(f"{v}: {m:.3f}" for v, m in zip(s.variable, s.min_ratio_bound)))
    P("読み方: 90% 区間が範囲に入る(p_tost が小さい)なら、その大きさ以上の差はないと言える。範囲に入らなければ「小さい」とは言えない。"
      "差ありと同等が両立する類型は、有意だが効果が小さい。範囲 δ は研究者が決める値で、結果から選んではならない(0.05 と 0.10 の両方を出す)。")


# ---- meta
def _extra_meta(a, outdir, tag, P):
    path = os.path.join(outdir, "nb_by_journal.csv")
    P(f"\n===== 雑誌別の率比のメタ分析(変量効果) =====  入力 {path}")
    if not os.path.exists(path):
        P("  nb_by_journal.csv がありません。先に通常の実行(--no-by-journal なし)で作ってください")
        return
    r = pd.read_csv(path)
    r = r[(r.irr > 0) & (r.irr_low > 0) & (r.irr_high > 0)].copy()
    r["y"] = np.log(r.irr)
    r["se"] = (np.log(r.irr_high) - np.log(r.irr_low)) / (2 * 1.96)
    rows = []
    for das, g in r.groupby("das"):
        k = len(g)
        if k < 3:
            continue
        y, se = g.y.values, g.se.values
        w = 1 / se ** 2
        mu_f = float((w * y).sum() / w.sum())
        Q = float((w * (y - mu_f) ** 2).sum())
        c = float(w.sum() - (w ** 2).sum() / w.sum())
        tau2 = max(0.0, (Q - (k - 1)) / c)
        wr = 1 / (se ** 2 + tau2)
        mu = float((wr * y).sum() / wr.sum())
        se_re = math.sqrt(1 / wr.sum())
        se_hk = math.sqrt(max(float((wr * (y - mu) ** 2).sum() / ((k - 1) * wr.sum())), 1e-300))
        tq = _t_ppf(0.975, k - 1)
        pi = _t_ppf(0.975, k - 2) * math.sqrt(tau2 + se_re ** 2)
        rows.append(dict(das=das, k_journals=k, irr_fixed=math.exp(mu_f), irr_random=math.exp(mu),
                         ci_low_dl=math.exp(mu - 1.96 * se_re), ci_high_dl=math.exp(mu + 1.96 * se_re), p_dl=float(norm_p(mu / se_re)[0]),
                         ci_low_hk=math.exp(mu - tq * se_hk), ci_high_hk=math.exp(mu + tq * se_hk), p_hk=_t_sf2(mu / se_hk, k - 1),
                         tau=math.sqrt(tau2), Q=Q, p_Q=chi2_sf(Q, k - 1), I2=(max(0.0, (Q - (k - 1)) / Q) if Q > 0 else 0.0),
                         pi_low=math.exp(mu - pi), pi_high=math.exp(mu + pi), n_above1=int((g.irr > 1).sum())))
    if not rows:
        P("  3 つ以上の雑誌で推定できた類型がありません")
        return
    m = pd.DataFrame(rows)
    m["p_hk_holm"] = holm(m.p_hk.values)
    m["p_dl_holm"] = holm(m.p_dl.values)
    m.to_csv(os.path.join(outdir, f"check_extra_meta_{tag}.csv"), index=False, encoding="utf-8-sig")
    P("DerSimonian–Laird の変量効果。区間は DL(正規)と Hartung–Knapp(t(k−1))の 2 通り、予測区間は新しい雑誌での率比の範囲(t(k−2))。"
      "各セルの SE は nb_by_journal.csv の 95% 区間から逆算(観測値ごとの頑健 SE)。Holm は類型の数にかける。")
    P(m[["das", "k_journals", "irr_random", "ci_low_hk", "ci_high_hk", "p_hk_holm", "tau", "I2", "p_Q", "pi_low", "pi_high", "n_above1"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4g}"))
    P("読み方: I² が大きく予測区間が 1 をまたげば、平均は小さくても雑誌によって向きが変わる(RQ4 の主張)。"
      "雑誌が 10 個以下なので、τ と I² の精度は低い。")


# ---- loo
def _extra_loo(a, d, meta, das_cols, ref, excl, outdir, tag, P):
    P("\n===== 雑誌を 1 つずつ除いた主モデル(leave-one-journal-out) =====")
    ctx, full, cov, t0 = _fit_ctx(d, meta, das_cols, excl, a)
    P(f"全雑誌: N={len(ctx['y']):,} / 収束 {full['converged']}")
    rows = [dict(left_out="(なし)", variable=r.variable, irr=r.irr, low=r.irr_low, high=r.irr_high, p_holm=r.p_holm, n=len(ctx["y"]), converged=full["converged"])
            for r in t0.itertuples()]
    res = {"全雑誌": t0}
    js = sorted(d.journal_key.unique())
    for i, j in enumerate(js):
        print(f"[進捗] 雑誌除外 {i + 1}/{len(js)}: {j}", file=sys.stderr, flush=True)
        d2 = d[d.journal_key != j]
        ctx2, full2, cov2, t2 = _fit_ctx(d2, meta, das_cols, excl, a)
        nm = "−" + str(jshort(pd.Series([j])).iloc[0])
        res[nm] = t2
        for r in t2.itertuples():
            rows.append(dict(left_out=j, variable=r.variable, irr=r.irr, low=r.irr_low, high=r.irr_high, p_holm=r.p_holm, n=len(ctx2["y"]), converged=full2["converged"]))
    df_ = pd.DataFrame(rows)
    df_.to_csv(os.path.join(outdir, f"check_extra_loo_{tag}.csv"), index=False, encoding="utf-8-sig")
    P("[各雑誌を除いたときの DAS の率比(Holm 補正後の p)。列名の「−雑誌」はその雑誌を除いたモデル]")
    base = t0.set_index("variable")
    out = pd.DataFrame({"variable": base.index})
    for nm, t in res.items():
        out[nm] = [_fmt_irr(t.set_index("variable"), v) for v in base.index]
    P(out.to_string(index=False))
    P("\n[類型ごとの要約: 全雑誌の向きと同じ向きだった回数 / Holm<0.05 で同じ向きだった回数 / 率比の範囲]")
    loo = df_[df_.left_out != "(なし)"]
    for v in base.index:
        s = loo[loo.variable == v]
        b0 = math.log(base.loc[v, "irr"])
        same = int((np.sign(np.log(s.irr)) == np.sign(b0)).sum())
        sig = int(((np.sign(np.log(s.irr)) == np.sign(b0)) & (s.p_holm < 0.05)).sum())
        P(f"  {v}: {same}/{len(s)} / {sig}/{len(s)} / {s.irr.min():.3f}〜{s.irr.max():.3f}(全雑誌 {base.loc[v, 'irr']:.3f}、全雑誌で Holm p={base.loc[v, 'p_holm']:.3g})")
    P("読み方: どの雑誌を除いても向きと有意性が保たれる類型は、1 つの雑誌(特に PLOS ONE)に引きずられていない。")


# ---- revalt
def _ols_cluster(X, y, codes):
    Ainv = np.linalg.pinv(X.T @ X)
    b = Ainv @ (X.T @ y)
    res = y - X @ b
    n, p = X.shape
    s2 = float((res ** 2).sum() / (n - p))
    return b, {"model": Ainv * s2, "cluster": _cluster_cov(Ainv, X * res[:, None], codes, n, p)}


def _gamma_cluster(X, y, codes, maxit=60, tol=1e-9):
    """ガンマ GLM(対数リンク、分散 ∝ mu²)。重みが一定なので (X'X)⁻¹ を 1 回だけ作り、反復再重み付けする。クラスタ頑健分散つき"""
    Ainv = np.linalg.pinv(X.T @ X)
    b = Ainv @ (X.T @ np.log(y))
    conv = False
    for _ in range(maxit):
        eta = np.clip(X @ b, -30, 30)
        mu = np.exp(eta)
        bn = Ainv @ (X.T @ (eta + (y - mu) / mu))
        if float(np.max(np.abs(bn - b))) < tol:
            b, conv = bn, True
            break
        b = bn
    mu = np.exp(np.clip(X @ b, -30, 30))
    r = (y - mu) / mu
    n, p = X.shape
    phi = float((r ** 2).sum() / (n - p))
    return b, {"model": Ainv * phi, "cluster": _cluster_cov(Ainv, X * r[:, None], codes, n, p)}, phi, conv


def _extra_revalt(a, d, meta, das_cols, ref, excl, outdir, tag, P):
    P("\n===== 査読期間のモデル違い(従属変数 %s) =====" % a.dv)
    if not _is_rv(a.dv):
        P("  [注意] --dv review_days 用です。ここでは %s で実行しますが、ガンマ GLM は 0 の行を除きます" % a.dv)
    ctx, full, cov, t0 = _fit_ctx(d, meta, das_cols, excl, a)
    X, y, codes, names = ctx["X"], ctx["y"], ctx["gcodes"], ctx["names"]
    idx = _das_idx(ctx)
    res = {"nb": t0}
    # (1) log(1+y) の OLS(固定効果は NB と同じ雑誌+年のダミー)。係数 exp(β) は 1+日数の幾何平均の比
    b, c = _ols_cluster(X, np.log1p(y), codes)
    t = _irr_table({"beta": b}, c, names, idx, ctx["meta"]); t["p_holm"] = holm(t.p_cluster.values)
    res["ols_log1p"] = t
    # (2) ガンマ GLM(y>0)
    keep = y > 0
    n0 = int((~keep).sum())
    gc = pd.factorize(codes[keep])[0]
    bg, cg, phi, convg = _gamma_cluster(X[keep], y[keep], gc)
    t = _irr_table({"beta": bg}, cg, names, idx, ctx["meta"]); t["p_holm"] = holm(t.p_cluster.values)
    res["gamma_log"] = t
    P(f"NB: N={len(y):,} 収束 {full['converged']} alpha={full['alpha']:.4f} / ガンマ GLM: N={int(keep.sum()):,}(y=0 の {n0:,} 行を除く)収束 {convg} 分散パラメータ {phi:.4f}")
    # (3)(4) 類型 M(--revalt-cat)を除く / 基準に統合する。主モデルと同じ NB
    cat = a.revalt_cat
    dc = "das_" + cat
    if dc in das_cols:
        das2 = [c_ for c_ in das_cols if c_ != dc]
        meta2 = {k: v for k, v in meta.items() if k != dc}
        d1 = d.copy()
        _relabel_data(d1, das2, ref, d1.das_label, pd.Series(True, index=d1.index))
        ctx1, full1, cov1, t1 = _fit_ctx(d1, meta2, das2, excl, a)
        res[f"nb_drop_{cat}"] = t1
        P(f"{cat} を除く: N={len(ctx1['y']):,}(除いた行 {len(ctx['y']) - len(ctx1['y']):,})")
        del d1
        d2 = d.copy()
        _relabel_data(d2, das2, ref, d2.das_label.where(d2.das_label != cat, ref), pd.Series(True, index=d2.index))
        ctx2, full2, cov2, t2 = _fit_ctx(d2, meta2, das2, excl, a)
        res[f"nb_merge_{cat}_into_{ref}"] = t2
        P(f"{cat} を {ref} に統合: N={len(ctx2['y']):,}")
        del d2
    else:
        P(f"  類型 {cat} がモデルにないので、除く・統合の確認は行いません")
    order = list(res)
    rows = []
    for nm in order:
        for r in res[nm].itertuples():
            rows.append(dict(spec=nm, variable=r.variable, irr=r.irr, low=r.irr_low, high=r.irr_high, p_cluster=r.p_cluster, p_holm=r.p_holm))
    pd.DataFrame(rows).to_csv(os.path.join(outdir, f"check_extra_revalt_{tag}.csv"), index=False, encoding="utf-8-sig")
    P("[DAS の率比(基準 %s)。括弧内は Holm 補正後の p(クラスタ頑健)。ols_log1p の率比は 1+日数の幾何平均の比]" % ref)
    _compare_table(res, order, P, "注意: M を除く・統合した列は、M の行の扱いが変わるので、ほかの類型の率比も少し動く。ols_log1p と gamma_log は M を含む。")
    P("読み方: 日数の分布の仮定(NB・対数正規・ガンマ)を変えても向きと有意性が変わらなければ、結果は NB という選択に依存していない。")


# ---- age
def _extra_age(a, d, meta, das_cols, ref, excl, outdir, tag, P):
    import copy
    P("\n===== 経過年数の柔軟な調整(折れ線スプライン) =====")
    if _is_rv(a.dv):
        P("  被引用数(--dv wos_TC または pmc_citedby_n)用です。査読期間では行いません")
        return
    a2 = copy.copy(a)
    a2.exposure = "covariate"
    meta2 = dict(meta)
    info = attach_exposure(a2, d, meta2)
    meta2.pop("log_age", None)
    la = d["log_age"]
    K = max(1, int(a.age_knots))
    knots = np.quantile(la.dropna(), np.linspace(0, 1, K + 2)[1:-1])
    P(f"経過年数の日付の列(補った行数) {info['used']} / 出版年の 7/1 で補った行 {info['n_fallback_year']:,} / 雑誌×年内の log 経過年数の SD {info['sd_within']:.3f} / "
      f"結び目 {K} 個(log 年齢の分位点): " + ", ".join(f"{np.exp(k):.2f}年" for k in knots))
    spl = ["age_s0"]
    d["age_s0"] = la
    for i, k in enumerate(knots, 1):
        d[f"age_s{i}"] = (la - k).clip(lower=0)
        spl.append(f"age_s{i}")
    for c_ in spl:
        meta2[c_] = dict(group=G_AGE, desc="log 経過年数の折れ線スプライン", kind="cont", src="pub_date", tr="log1p")
    meta3 = dict(meta2)
    js = sorted(d.journal_key.unique())
    jsl = []
    for i, j in enumerate(js[1:], 1):
        c_ = f"age_j{i}"
        d[c_] = la * (d.journal_key == j).astype(float)
        meta3[c_] = dict(group=G_AGE, desc=f"log 経過年数 × 雑誌 {j}", kind="cont", src="pub_date", tr="log1p")
        jsl.append(c_)
    specs = [("main", meta), ("spline", meta2), ("spline+journal_slope", meta3)]
    res, aics = {}, {}
    for nm, m_ in specs:
        print(f"[進捗] {nm} を推定中", file=sys.stderr, flush=True)
        ctx, full, cov, t = _fit_ctx(d, m_, das_cols, excl, a)
        res[nm] = t
        aics[nm] = (full["llf"], -2 * full["llf"] + 2 * (int(np.linalg.matrix_rank(full["A"])) + 1), len(ctx["y"]), full["converged"])
        if nm != "main":
            names = ctx["names"]
            ii = [names.index(c_) for c_ in spl if c_ in names]
            w, pw = _wald(full["beta"], cov["cluster"], ii)
            P(f"  [{nm}] 年齢スプライン {len(ii)} 項の同時 Wald(クラスタ頑健) χ²({len(ii)})={w:.1f} p={pw:.3g}")
    rows = []
    for nm in res:
        for r in res[nm].itertuples():
            rows.append(dict(spec=nm, variable=r.variable, irr=r.irr, low=r.irr_low, high=r.irr_high, p_cluster=r.p_cluster, p_holm=r.p_holm,
                             llf=aics[nm][0], aic=aics[nm][1], n=aics[nm][2]))
    pd.DataFrame(rows).to_csv(os.path.join(outdir, f"check_extra_age_{tag}.csv"), index=False, encoding="utf-8-sig")
    P("[DAS の率比(基準 %s)。括弧内は Holm 補正後の p]" % ref)
    _compare_table(res, list(res), P)
    P("[対数尤度・AIC(同じ行なので比較できる)] " + " / ".join(f"{k}: llf {v[0]:,.1f} AIC {v[1]:,.1f} N {v[2]:,} 収束 {v[3]}" for k, v in aics.items()))
    P("読み方: 弾力性が 1 でなかった(オフセットが成り立たなかった)ので、スプラインでも DAS の率比、とくに N の有意性が変わらないかを見る。")


# ---- field
def _extra_field(a, d, meta, das_cols, ref, excl, outdir, tag, P):
    P("\n===== 分野の統制 =====")
    fcols = [c for c in meta if meta[c]["group"] == "分野"]
    if not fcols:
        P("  分野の列が使われていません。--find-cols 'subject|categor|area|field|mesh|topic' で列を探し、--field-col で指定してください。"
          "WoS の研究分野は複数値(; 区切り)のとき先頭だけを使います(厳密には 1 論文に複数の分野がつくため)")
        return
    ctx0, full0, cov0, t0 = _fit_ctx(d, meta, das_cols, excl, a, drop_groups=("分野",))
    ctx1, full1, cov1, t1 = _fit_ctx(d, meta, das_cols, excl, a)
    fi = [i for i, n in enumerate(ctx1["names"]) if n in fcols]
    lr = 2 * (full1["llf"] - full0["llf"])
    w, pw = _wald(full1["beta"], cov1["cluster"], fi)
    P(f"分野の列 {a.field_col}: ダミー {len(fi)} 個 / N(分野なし)={len(ctx0['y']):,}、N(分野あり)={len(ctx1['y']):,} / "
      f"LRT χ²({len(fi)})={lr:.1f} p={chi2_sf(lr, len(fi)):.3g} / Wald(クラスタ頑健) χ²({len(fi)})={w:.1f} p={pw:.3g}")
    res = {"分野なし(主モデル)": t0, "分野あり": t1}
    rows = []
    for nm, t in res.items():
        for r in t.itertuples():
            rows.append(dict(spec=nm, variable=r.variable, irr=r.irr, low=r.irr_low, high=r.irr_high, p_cluster=r.p_cluster, p_holm=r.p_holm))
    pd.DataFrame(rows).to_csv(os.path.join(outdir, f"check_extra_field_{tag}.csv"), index=False, encoding="utf-8-sig")
    P("[DAS の率比(基準 %s)。括弧内は Holm 補正後の p]" % ref)
    _compare_table(res, list(res), P)
    P(f"[AIC] 分野なし {-2 * full0['llf'] + 2 * (int(np.linalg.matrix_rank(full0['A'])) + 1):,.1f} / "
      f"分野あり {-2 * full1['llf'] + 2 * (int(np.linalg.matrix_rank(full1['A'])) + 1):,.1f}")
    P("読み方: 分野を入れても向きと有意性が変わらなければ、DAS の関連は分野の違いだけでは説明されない。変わる類型は、分野の代理だった可能性がある。"
      "上位 --field-top 個以外の分野は基準側にまとめられる。")


# ---- window(v025 追加): 経過年数で絞った推定
def _extra_window(a, d, meta, das_cols, ref, excl, outdir, tag, P):
    import copy
    P("\n===== 経過年数で絞った推定(固定引用窓の代用) =====")
    if _is_rv(a.dv):
        P("  被引用数(--dv wos_TC または pmc_citedby_n)用です。査読期間では行いません")
        return
    a2 = copy.copy(a)
    a2.exposure = "covariate"
    info = attach_exposure(a2, d, dict(meta))      # d に age_years・log_age を付ける(meta は変えない)
    ages = [float(x) for x in str(a.window_ages).split(",") if x.strip()]
    K = max(1, int(a.age_knots))
    P(f"調査日 {info['ref']} / 経過年数 最小 {info['age_min']:.2f} 中央値 {info['age_med']:.2f} 最大 {info['age_max']:.2f} / 出版年の 7/1 で補った行 {info['n_fallback_year']:,}")
    P("WoS の Times Cited は調査日までの累積値で、年ごとの被引用数は使っていない。出版後 k 年未満の論文を除くと、経過年数のばらつきと、まだ引用が溜まっていない論文の影響が減る。"
      "固定窓(出版後 3 年・5 年など)そのものは、年ごとの被引用数が得られれば同じ NB で推定できる。ここでは累積値のまま、経過年数の下限だけを変える。")
    subsets = [("all", None)] + [(f"age>={k:g}y", k) for k in ages]
    res, aics, rows, order = {}, {}, [], []
    for sname, kmin in subsets:
        sub = d if kmin is None else d[d.age_years >= kmin].copy()
        n_dv = int(sub.tc.notna().sum())
        cc = sub.loc[sub.tc.notna(), "das_label"].value_counts()
        P(f"\n[{sname}] 被引用数が使える行 {n_dv:,} / 類型の件数: " + ", ".join(f"{c}={int(cc.get(c, 0)):,}" for c in [ref] + [x[4:] for x in das_cols]))
        for spec in ("main", "age_cov", "spline"):
            nm = f"{sname}|{spec}"
            print(f"[進捗] {nm} を推定中", file=sys.stderr, flush=True)
            m_ = dict(meta)
            try:
                if spec == "age_cov":
                    m_["log_age"] = _age_meta()
                elif spec == "spline":
                    _add_age_spline(sub, m_, K)
                ctx, full, cov, t = _fit_ctx(sub, m_, das_cols, excl, a)
            except Exception as e:
                P(f"  [失敗] {nm}: {type(e).__name__}: {e}")
                continue
            npar = int(np.linalg.matrix_rank(full["A"])) + 1
            aics[nm] = (full["llf"], -2 * full["llf"] + 2 * npar, len(ctx["y"]), full["converged"])
            res[nm] = t
            order.append(nm)
            for r in t.itertuples():
                rows.append(dict(spec=nm, subset=sname, model=spec, variable=r.variable, irr=r.irr, low=r.irr_low, high=r.irr_high,
                                 p_cluster=r.p_cluster, p_holm=r.p_holm, llf=full["llf"], aic=aics[nm][1], n=len(ctx["y"])))
            if spec == "age_cov" and "log_age" in ctx["names"]:
                i = ctx["names"].index("log_age")
                sd = float(sub.loc[ctx["use"].index, "log_age"].std())
                se = math.sqrt(cov["cluster"][i, i])
                el, el_se = full["beta"][i] / sd, se / sd
                P(f"  [{nm}] log 経過年数の係数(弾力性)= {el:.3f}(クラスタ頑健 SE {el_se:.3f}、95% 区間 {el - 1.96 * el_se:.3f}〜{el + 1.96 * el_se:.3f})。1 ならオフセットの仮定(比例)が妥当")
                rows.append(dict(spec=nm, subset=sname, model=spec, variable="log_age_elasticity", irr=el, low=el - 1.96 * el_se, high=el + 1.96 * el_se,
                                 p_cluster=float("nan"), p_holm=float("nan"), llf=full["llf"], aic=aics[nm][1], n=len(ctx["y"])))
        if kmin is not None:
            del sub
    if not res:
        P("  推定できた仕様がありません")
        return
    pd.DataFrame(rows).to_csv(os.path.join(outdir, f"check_extra_window_{tag}.csv"), index=False, encoding="utf-8-sig")
    P("\n[DAS の率比(基準 %s)。括弧内は Holm 補正後の p。列名は 経過年数の下限|モデル(main=雑誌+年の固定効果のみ / age_cov=log 経過年数を係数つきで / spline=折れ線スプライン)]" % ref)
    _compare_table(res, order, P, "注意: 下限を上げると標本が変わるので、率比のずれには標本の違いも含まれる。同じ標本の中の main・age_cov・spline の比較が、経過年数の調整の効果になる。")
    P("[対数尤度・AIC(同じ下限の中でだけ比較できる)]")
    for k_ in order:
        v = aics[k_]
        P(f"  {k_:22s} llf {v[0]:,.1f}  AIC {v[1]:,.1f}  N {v[2]:,}  収束 {v[3]}")
    P("読み方: 経過年数の下限を上げても、スプラインで調整しても、DAS の向きと Holm 後の有意性が主モデルと同じなら、累積被引用数を使ったことによる偏りは結論を変えていない。"
      "弾力性が下限を上げると 1 に近づくなら、未成熟な論文が比例の仮定を崩していた。N の有意性が動くときは、仕様依存と書く。")


# ---- ratio(v031 追加): PMC と WoS の被引用数の比(網羅の偏りの確認)
def _ratio_ctx(sub, meta, das_cols, excl, a, y_col, off_col=None):
    """sub の列 y_col を従属変数(tc)にして主モデルを推定する。off_col があれば log(その列)をオフセットにする"""
    s_ = sub.copy()
    s_["tc"] = s_[y_col]
    base_ivs = [c for c in meta if c not in excl and c != "log_review" and c not in das_cols]
    ctx = nb_build(s_, meta, das_cols, base_ivs, a, [])
    if off_col:
        ctx["offset"] = np.log(s_.loc[ctx["use"].index, off_col].values.astype(float))
    full = _fit_main(ctx)
    cov = nb_cov(full, ctx["X"], ctx["y"], codes=ctx["gcodes"])
    return ctx, full, cov, _das_table(ctx, full, cov)


def _ratio_by_journal(ctx, a):
    """雑誌ごとの DAS の率比(nb_by_journal と同じ推定。観測値ごとの頑健(HC)SE)。オフセットがあれば雑誌ごとに切り出して使う"""
    use, ivs, meta = ctx["use"], ctx["ivs"], ctx["meta"]
    rows = []
    for j, jname in enumerate(ctx["jlabels"]):
        m = ctx["jcodes"] == j
        s_ = use[m]
        das_ok = [c for c in ctx["das_cols"] if s_[c].sum() >= a.min_cat_j and (len(s_) - s_[c].sum()) >= a.min_cat_j]
        oth = [c for c in ivs if c not in ctx["das_cols"] and s_[c].std() > 1e-9]
        if len(das_ok) == 0 or len(s_) < 500:
            continue
        yl = sorted(s_.year.unique())
        cols, nm = [np.ones(len(s_))], ["(切片)"]
        for yv in yl[1:]:
            cols.append((s_.year.values == yv).astype(float)); nm.append(f"fe_year:{int(yv)}")
        for c in das_ok + oth:
            cols.append(s_[c].values.astype(float)); nm.append(c)
        Xj = np.column_stack(cols)
        yj = np.round(s_.tc.values.astype(float))
        off = None if ctx.get("offset") is None else ctx["offset"][m]
        fj = nb_fit(Xj, NBData(yj), offset=off)
        cj = nb_cov(fj, Xj, yj, codes=np.arange(len(yj)))
        idx = [nm.index(c) for c in das_ok]
        t = _irr_table(fj, cj, nm, idx, meta)
        t.insert(0, "journal", jname)
        t["das"] = [c[4:] for c in das_ok]
        t["n_journal"] = len(s_)
        t["n_class"] = [int(s_[c].sum()) for c in das_ok]
        t["converged"] = fj["converged"]
        rows.append(t[["journal", "das", "n_journal", "n_class", "irr", "irr_low", "irr_high", "p_cluster", "converged"]]
                    .rename(columns={"p_cluster": "p_robust"}))
    if not rows:
        return pd.DataFrame()
    r = pd.concat(rows, ignore_index=True)
    r["p_holm_robust"] = holm(r.p_robust.values)
    return r


def _extra_ratio(a, d, meta, das_cols, ref, excl, outdir, tag, P):
    P("\n===== PMC と WoS の被引用数の差(網羅の偏りの確認) =====")
    if _is_rv(a.dv):
        P("  被引用数用です。--dv wos_TC で実行してください")
        return
    if a.dv != "wos_TC":
        P("  [注意] --dv wos_TC のときの標本(WoS が使える論文)を基準にします。--dv pmc_citedby_n では行いません")
        return
    for c in ("pmc_citedby_n",):
        if c not in d:
            P(f"  列 {c} が CSV にありません")
            return
    w = d["tc"]                              # WoS の被引用数(照合できた論文だけ。主モデルの標本)
    p = num(d["pmc_citedby_n"])
    if "cb_fetched" in d:
        p = p.where(d.cb_fetched == "1")
    n_w = int(w.notna().sum())
    ok = w.notna() & (w >= 1) & p.notna() & (p >= 0)
    n_w0 = int((w == 0).sum())
    sub = d[ok].copy()
    sub["_w"] = w[ok].astype(float)
    sub["_p"] = p[ok].astype(float)
    P(f"WoS が使える行 {n_w:,} → WoS=0 の {n_w0:,} 行を除く(オフセットが使えない)/ PMC の cited-by がない行を除く → {len(sub):,} 行")
    P(f"全体の Σ PMC / Σ WoS = {sub._p.sum() / sub._w.sum():.3f} / 論文ごとの PMC/WoS の中央値 = {(sub._p / sub._w).median():.3f}")
    # 記述統計: 類型×雑誌の Σ PMC / Σ WoS
    g = sub.groupby(["journal_key", "das_label"]).agg(n=("_w", "size"), sum_wos=("_w", "sum"), sum_pmc=("_p", "sum")).reset_index()
    g["ratio_sum"] = g.sum_pmc / g.sum_wos
    ga = sub.groupby("das_label").agg(n=("_w", "size"), sum_wos=("_w", "sum"), sum_pmc=("_p", "sum")).reset_index()
    ga["ratio_sum"] = ga.sum_pmc / ga.sum_wos
    ga["median_ratio"] = sub.assign(r_=sub._p / sub._w).groupby("das_label").r_.median().reindex(ga.das_label).values
    ga.insert(0, "journal_key", "ALL")
    desc = pd.concat([ga, g], ignore_index=True)
    desc.to_csv(os.path.join(outdir, f"check_extra_ratio_desc_{tag}.csv"), index=False, encoding="utf-8-sig")
    P("\n[類型ごとの Σ PMC / Σ WoS と論文ごとの比の中央値(全体)]")
    P(ga[["das_label", "n", "ratio_sum", "median_ratio"]].round(3).to_string(index=False))
    pv = g.pivot(index="journal_key", columns="das_label", values="ratio_sum").round(3)
    pv.index = jshort(pd.Series(pv.index)).values
    P("\n[雑誌×類型の Σ PMC / Σ WoS]")
    P(pv.to_string())
    # 3 つのモデル(同じ論文の集合)
    specs = [("wos", "_w", None), ("pmc", "_p", None), ("pmc_per_wos", "_p", "_w")]
    res, ctxs, rows, info = {}, {}, [], {}
    for nm, ycol, ocol in specs:
        print(f"[進捗] ratio: 全体 {nm} を推定中", file=sys.stderr, flush=True)
        try:
            ctx, full, cov, t = _ratio_ctx(sub, meta, das_cols, excl, a, ycol, ocol)
        except Exception as e:
            P(f"  [失敗] {nm}: {type(e).__name__}: {e}")
            continue
        res[nm], ctxs[nm] = t, ctx
        info[nm] = (len(ctx["y"]), full["alpha"], full["converged"])
        for r in t.itertuples():
            rows.append(dict(model=nm, variable=r.variable, irr=r.irr, low=r.irr_low, high=r.irr_high, p_cluster=r.p_cluster, p_holm=r.p_holm,
                             n=len(ctx["y"]), alpha=full["alpha"]))
    if not res:
        P("  推定できたモデルがありません")
        return
    pd.DataFrame(rows).to_csv(os.path.join(outdir, f"check_extra_ratio_{tag}.csv"), index=False, encoding="utf-8-sig")
    for nm in res:
        P(f"  {nm:12s} N={info[nm][0]:,} alpha={info[nm][1]:.4f} 収束 {info[nm][2]}")
    order = [k for k in ("wos", "pmc", "pmc_per_wos") if k in res]
    P("\n[DAS の率比(基準 %s)。括弧内は Holm 補正後の p(雑誌×年クラスタ頑健)。wos / pmc は同じ論文の集合での WoS と PMC の NB、pmc_per_wos は PMC を log(WoS) をオフセットにして推定した率比(=PMC/WoS の比が F の何倍か)]" % ref)
    _compare_table(res, order, P, "注意: pmc_per_wos の率比は、対数でほぼ pmc − wos の差に等しい(オフセットの分だけ違う)。1 から外れる類型は、WoS の引用に対する PMC 内の引用の割合が基準 F と違う。")
    # 雑誌別
    jr = {}
    for nm in order:
        print(f"[進捗] ratio: 雑誌別 {nm} を推定中", file=sys.stderr, flush=True)
        try:
            jr[nm] = _ratio_by_journal(ctxs[nm], a)
        except Exception as e:
            P(f"  [失敗] 雑誌別 {nm}: {type(e).__name__}: {e}")
    if jr:
        allj = pd.concat([v.assign(model=k) for k, v in jr.items() if len(v)], ignore_index=True)
        allj.to_csv(os.path.join(outdir, f"check_extra_ratio_by_journal_{tag}.csv"), index=False, encoding="utf-8-sig")
        for nm in order:
            v = jr.get(nm)
            if v is None or not len(v):
                continue
            tb = v.assign(cell=[f"{i:.2f} ({ph:.2g})" for i, ph in zip(v.irr, v.p_holm_robust)]).pivot(index="journal", columns="das", values="cell").fillna("")
            tb.index = jshort(pd.Series(tb.index)).values
            P(f"\n[雑誌別の率比 {nm}(括弧内は雑誌×類型の全比較にかけた Holm 後の p。観測値ごとの頑健 SE)]")
            P(tb.to_string())
        if "wos" in jr and "pmc" in jr and len(jr["wos"]) and len(jr["pmc"]):
            m_ = jr["wos"].merge(jr["pmc"], on=["journal", "das"], suffixes=("_wos", "_pmc"))
            m_["opposite"] = (np.log(m_.irr_wos) * np.log(m_.irr_pmc)) < 0
            both = m_[(m_.p_holm_robust_wos < 0.05) | (m_.p_holm_robust_pmc < 0.05)]
            sig2 = m_[(m_.p_holm_robust_wos < 0.05) & (m_.p_holm_robust_pmc < 0.05)]
            P(f"\n[雑誌×類型 {len(m_)} 個のうち、WoS と PMC で向きが逆 {int(m_.opposite.sum())} 個。どちらかが Holm 後 p<0.05 の {len(both)} 個のうち逆向き {int(both.opposite.sum())} 個。"
              f"両方が Holm 後 p<0.05 の {len(sig2)} 個のうち逆向き {int(sig2.opposite.sum())} 個(有意でない側の向きは偶然でも変わるので、この数が「確かな逆転」)]")
            if len(both):
                P(both[["journal", "das", "irr_wos", "irr_pmc", "p_holm_robust_wos", "p_holm_robust_pmc", "opposite"]]
                  .assign(journal=lambda x: jshort(x.journal)).round(3).to_string(index=False))
        if "wos" in jr and "pmc" in jr and len(jr["wos"]) and len(jr["pmc"]):
            _ratio_dir_report(jr["wos"], jr["pmc"], P)   # v058: 同じ向きの数(本文の「same direction in N of 54」)
    P("読み方: (1) 全体の pmc_per_wos で A・N などの率比が 1 を下回る(Holm 後に有意)なら、WoS に比べて PMC 内での引用が少ない論文であり、WoS と PMC の向きの違いは PMC の網羅の違いを反映している可能性がある。"
      "(2) 1 に近ければ、向きの違いは網羅の偏りでは説明できない。(3) 雑誌別で逆転が特定の雑誌に集中するなら、分野(引用する側の PMC 収録率)の差の可能性がある。"
      "ただし、この確認は機序を特定せず、引用する側の分野は測っていない。")


# ---- aft(v025 追加): 査読期間の AFT モデル
def _weibull_aft(X, y, codes, maxit=200, tol=1e-10):
    """Weibull AFT(打ち切りなし)。log y = Xβ + σ ε、ε は標準最小極値分布。対数尤度は y のスケール(-log y を含む)で、対数正規と比べられる。
    ニュートン法(行き過ぎは半歩ずつ戻す)で β と log σ を同時に推定し、観測情報とクラスタ頑健(サンドイッチ)の分散を返す。X の 1 列目は切片"""
    n, p = X.shape
    ly = np.log(y)
    b = np.linalg.lstsq(X, ly, rcond=None)[0]
    sig0 = max(float((ly - X @ b).std()) * math.sqrt(6.0) / math.pi, 1e-3)
    b[0] += 0.5772156649015329 * sig0           # 最小極値分布の平均は −γ
    ls = math.log(sig0)

    def ll_of(b_, ls_):
        z_ = (ly - X @ b_) / math.exp(ls_)
        ez_ = np.exp(np.clip(z_, -60, 60))
        return float(np.sum(z_ - ez_ - ls_ - ly)), z_, ez_
    ll, z, ez = ll_of(b, ls)
    conv, it = False, 0
    for it in range(1, maxit + 1):
        s = math.exp(ls)
        g = np.concatenate([X.T @ (ez - 1.0) / s, [float(np.sum(z * (ez - 1.0) - 1.0))]])
        Hbb = -(X * (ez / s ** 2)[:, None]).T @ X
        Hbl = -(X.T @ (z * ez + ez - 1.0)) / s
        Hll = -float(np.sum(z * (ez + z * ez - 1.0)))
        negH = np.empty((p + 1, p + 1))
        negH[:p, :p], negH[:p, p], negH[p, :p], negH[p, p] = -Hbb, -Hbl, -Hbl, -Hll
        ridge, step = 0.0, None
        for _ in range(10):
            try:
                st = np.linalg.solve(negH + ridge * np.eye(p + 1), g)
                if np.all(np.isfinite(st)) and float(g @ st) > 0:
                    step = st
                    break
            except np.linalg.LinAlgError:
                pass
            ridge = max(ridge * 10.0, 1e-6 * abs(float(np.trace(negH))) / (p + 1))
        if step is None:
            break
        ok = False
        for h in range(14):
            bt, lt_ = b + step[:p] / 2 ** h, ls + step[p] / 2 ** h
            llt, zt, ezt = ll_of(bt, lt_)
            if np.isfinite(llt) and llt >= ll - 1e-9:
                ok = True
                break
        if not ok:
            break
        done = abs(llt - ll) < tol * (1.0 + abs(llt))
        b, ls, ll, z, ez = bt, lt_, llt, zt, ezt
        if done:
            conv = True
            break
    s = math.exp(ls)
    Hbb = -(X * (ez / s ** 2)[:, None]).T @ X
    Hbl = -(X.T @ (z * ez + ez - 1.0)) / s
    Hll = -float(np.sum(z * (ez + z * ez - 1.0)))
    negH = np.empty((p + 1, p + 1))
    negH[:p, :p], negH[:p, p], negH[p, :p], negH[p, p] = -Hbb, -Hbl, -Hbl, -Hll
    Ainv = np.linalg.pinv(negH)
    sc = np.column_stack([X * ((ez - 1.0) / s)[:, None], z * (ez - 1.0) - 1.0])
    Vc = _cluster_cov(Ainv, sc, codes, n, p + 1)
    return dict(beta=b, sigma=s, llf=ll, converged=conv, iters=it, z=z), {"model": Ainv[:p, :p], "cluster": Vc[:p, :p]}


def _extra_aft(a, d, meta, das_cols, ref, excl, outdir, tag, P):
    P("\n===== 査読期間の AFT モデル(対数正規・Weibull) =====")
    if not _is_rv(a.dv):
        P("  --dv review_days 用です。被引用数では行いません")
        return
    ctx, full, cov, t0 = _fit_ctx(d, meta, das_cols, excl, a)
    X, y, codes, names = ctx["X"], ctx["y"], ctx["gcodes"], ctx["names"]
    idx = _das_idx(ctx)
    n_all = len(y)
    keep = y > 0
    n0 = int((~keep).sum())
    gc = pd.factorize(codes[keep])[0]
    Xk, yk = X[keep], y[keep]
    rk = int(np.linalg.matrix_rank(Xk))
    P(f"N={n_all:,}(日数 0 の {n0:,} 行は、対数をとる 3 モデルのうち shift 版以外では除く)/ クラスタ {int(codes.max()) + 1} / NB の収束 {full['converged']}")
    P("打ち切りについて: 分析の対象は受理された論文だけで、却下・取り下げで終わった査読は含まれない。受付から受理までの日数は全論文で観測されており、"
      "受理前に追跡が終わった(右打ち切り)論文はない。したがって、打ち切りを扱うことが AFT の利点になる場面ではなく、日数が正の連続量であることに合う分布の仮定を確かめる目的で使う。"
      "別の問題として、受理された論文だけを見ているための選択(却下された論文が除かれる)があり、これは AFT でも直らない。")
    res = {"nb": t0}
    # 対数正規 AFT(打ち切りなしの最尤推定は log y の OLS と同じ)。時間比 = exp(β)
    b, c = _ols_cluster(Xk, np.log(yk), gc)
    t = _irr_table({"beta": b}, c, names, idx, ctx["meta"])
    t["p_holm"] = holm(t.p_cluster.values)
    res["lognormal_aft"] = t
    r_ln = np.log(yk) - Xk @ b
    s2 = float((r_ln ** 2).mean())
    ll_ln = float(-0.5 * len(yk) * (math.log(2 * math.pi * s2) + 1.0) - np.log(yk).sum())
    # 0 日の行を含める対数正規(log(y+shift))。0 日は y>0 の分布から外れるので、補助として示す
    b2, c2 = _ols_cluster(X, np.log(y + a.aft_shift), codes)
    t2 = _irr_table({"beta": b2}, c2, names, idx, ctx["meta"])
    t2["p_holm"] = holm(t2.p_cluster.values)
    res[f"lognormal_shift{a.aft_shift:g}"] = t2
    # Weibull AFT
    print("[進捗] Weibull AFT を推定中", file=sys.stderr, flush=True)
    fw, cw = _weibull_aft(Xk, yk, gc)
    t3 = _irr_table(fw, cw, names, idx, ctx["meta"])
    t3["p_holm"] = holm(t3.p_cluster.values)
    res["weibull_aft"] = t3
    # ガンマ GLM(参考)
    bg, cg, phi, convg = _gamma_cluster(Xk, yk, gc)
    t4 = _irr_table({"beta": bg}, cg, names, idx, ctx["meta"])
    t4["p_holm"] = holm(t4.p_cluster.values)
    res["gamma_log"] = t4
    order = list(res)
    rows = []
    for nm in order:
        for r in res[nm].itertuples():
            rows.append(dict(spec=nm, variable=r.variable, ratio=r.irr, low=r.irr_low, high=r.irr_high, p_cluster=r.p_cluster, p_holm=r.p_holm))
    pd.DataFrame(rows).to_csv(os.path.join(outdir, f"check_extra_aft_{tag}.csv"), index=False, encoding="utf-8-sig")
    P(f"[当てはまり(y>0 の {len(yk):,} 行、y のスケールの対数尤度なので 2 分布を比べられる)] "
      f"対数正規: σ̂={math.sqrt(s2):.4f} llf {ll_ln:,.1f} AIC {-2 * ll_ln + 2 * (rk + 1):,.1f} / "
      f"Weibull: σ̂={fw['sigma']:.4f}(形状 1/σ={1 / fw['sigma']:.3f}) llf {fw['llf']:,.1f} AIC {-2 * fw['llf'] + 2 * (rk + 1):,.1f} 収束 {fw['converged']}({fw['iters']} 回) / "
      f"ガンマ GLM: 分散パラメータ {phi:.4f} 収束 {convg}")
    qs = [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]
    try:
        from scipy import stats
        zn = np.quantile(r_ln / math.sqrt(s2), qs)
        zw = np.quantile(fw["z"], qs)
        P("[残差の分位点: 対数正規の標準化残差 / 理論(標準正規)] " + ", ".join(f"{q:g}: {v:.2f}/{stats.norm.ppf(q):.2f}" for q, v in zip(qs, zn)))
        P("[残差の分位点: Weibull の z / 理論(最小極値)] " + ", ".join(f"{q:g}: {v:.2f}/{math.log(-math.log(1 - q)):.2f}" for q, v in zip(qs, zw)))
    except Exception:
        pass
    P("[DAS の比(基準 %s)。nb の列は期待日数の比(率比)、AFT の列は日数(の中央値または幾何平均)の比 = 時間比。括弧内は Holm 補正後の p(クラスタ頑健)]" % ref)
    _compare_table(res, order, P, "注意: 時間比が 1 より小さければ受理までの日数が短い。")
    P("読み方: NB・対数正規・Weibull・ガンマで向きと有意性が同じなら、日数を整数のカウントとして NB で扱ったことは結論を変えていない。"
      "AIC は対数正規と Weibull の間でだけ比べる(NB は日数を離散とみなす別の尤度)。")


def _run_aft(a, d, meta, das_cols, ref, excl, outdir, tag, P):
    """v026: aft は査読期間用。--dv が被引用数のときは、査読期間(review_days)のデータを読み直して実行する(--dv review_days を別に指定しなくてよい)"""
    if _is_rv(a.dv):
        return _extra_aft(a, d, meta, das_cols, ref, excl, outdir, tag, P)
    import copy
    a2 = copy.copy(a)
    a2.dv = "review_days"
    P("\n(aft は査読期間用なので、--dv review_days に切り替えてデータを読み直します)")
    d2, meta2, das2, ref2, log2 = prepare(a2)
    excl2 = {c.strip() for c in a2.exclude.split(",") if c.strip()}
    P("\n".join(log2))
    return _extra_aft(a2, d2, meta2, das2, ref2, excl2, outdir, _tag(a2.dv), P)


def _extra_repo(a, d, meta, das_cols, ref, excl, outdir, tag, P):
    """v055: 「リポジトリ共有か否か」の 2 値の DAS(F+M など)で主モデルと同じ NB を推定する。
    PLOS OSI など、リポジトリ共有を 1 つの 2 値として扱う先行研究の効果量と、本稿の類型別の率比を同じ土俵に並べるため。"""
    if "das_label" not in d:
        raise RuntimeError("das_label の列がありません")
    labs = d["das_label"].astype(str)
    present = set(labs.unique())
    defs = [x.strip().upper() for x in a.repo_defs.split(",") if x.strip()]
    specs = [x.strip() for x in a.repo_specs.split(",") if x.strip()]
    adjs = [x.strip().lower() for x in a.repo_adj.split(",") if x.strip()]
    bad = [x for x in adjs if x not in ("main", "fe")]
    if bad:
        raise RuntimeError(f"--repo-adj の指定が不明です: {bad}(main, fe)")
    other_groups = tuple(sorted({v["group"] for v in meta.values()} - {G_DAS}))   # fe: DAS 以外の共変量のグループをすべて外す
    excl2 = set(excl) | set(das_cols)   # 元の DAS ダミー(das_P など)は共変量に入れない
    is_rv = _is_rv(a.dv)
    P("\n===== リポジトリ共有か否か(2 値の DAS)=====")
    P(f"従属変数 {a.dv} / 1 にする類型の組 {defs} / 比較対象 {specs} / 調整 {adjs} / 全行で推定 / 標準誤差は雑誌×年クラスタ頑健")
    P("類型の件数(推定に入る前): " + ", ".join(f"{k}={v:,}" for k, v in labs.value_counts().items()))
    P("率比は「1 の組であること」の 0→1 の率比。比較対象に使う行だけで推定する(他の類型の行は入れない)。")
    rows = []
    for dn in defs:
        pos = set(dn)
        if not pos <= present:
            P(f"\n[省略] 組 {dn}: CSV にない類型 {sorted(pos - present)} を含む(CSV の類型 {sorted(present)})")
            continue
        nm = f"repo_{dn}"
        meta2 = dict(meta)
        meta2[nm] = dict(group=G_DAS, desc=f"リポジトリ共有 = {'+'.join(sorted(pos))}(1)/ 比較対象(0)", kind="bin", src="das_label", tr="dummy")
        done = set()
        for sp in specs:
            comp = (present - pos) if sp.lower() == "all" else ({c for c in sp.upper()} - pos)
            comp &= present
            if not comp:
                P(f"\n[省略] 組 {dn} × 比較対象 {sp}: 比較対象の類型が空(1 の組と重なる、または CSV にない)")
                continue
            if (dn, frozenset(comp)) in done:
                P(f"\n[省略] 組 {dn} × 比較対象 {sp}: 比較対象の類型 {''.join(sorted(comp))} が先の指定と同じ(1 の組と重なる類型を除いた結果)")
                continue
            done.add((dn, frozenset(comp)))
            keep = pos | comp
            d2 = d.loc[labs.isin(keep).values].copy()
            d2[nm] = d2["das_label"].astype(str).isin(pos).astype(float)
            for adj in adjs:
                print(f"[進捗] repo: 組 {dn} / 比較対象 {sp}({'+'.join(sorted(comp))}) / 調整 {adj}", file=sys.stderr, flush=True)
                ctx, full, cov, t = _fit_ctx(d2, meta2, [nm], excl2, a, drop_groups=() if adj == "main" else other_groups)
                if nm not in ctx["das_cols"] or not len(t):
                    P(f"\n[省略] 組 {dn} × 比較対象 {sp} × {adj}: 2 値の列が推定から外れた(ばらつきなし・欠損)")
                    continue
                r = t.iloc[0]
                irr, lo, hi = float(r.irr), float(r.irr_low), float(r.irr_high)
                rows.append(dict(pos=dn, comparator=sp, comparator_cats="".join(sorted(comp)), adjust=adj, irr=irr, low=lo, high=hi,
                                 pct=(irr - 1) * 100, pct_low=(lo - 1) * 100, pct_high=(hi - 1) * 100, p_cluster=float(r.p_cluster),
                                 se_cluster=float(r.se_cluster), n=len(ctx["y"]), n_pos=int(ctx["use"][nm].sum()),
                                 clusters=int(ctx["gcodes"].max()) + 1, converged=bool(full["converged"])))
    if not rows:
        P("\n[結果なし] 推定できた組がありません")
        return
    df_ = pd.DataFrame(rows)
    df_.to_csv(os.path.join(outdir, f"check_extra_repo_{tag}{getattr(a, 'repo_suffix', '') or ''}.csv"), index=False, encoding="utf-8-sig")
    show = df_.copy()
    show["IRR (95% CI)"] = [f"{x.irr:.3f} ({x.low:.3f}, {x.high:.3f})" for x in show.itertuples()]
    show["変化率 % (95% CI)"] = [f"{x.pct:+.1f} ({x.pct_low:+.1f}, {x.pct_high:+.1f})" for x in show.itertuples()]
    P("\n[結果]")
    P(show[["pos", "comparator", "comparator_cats", "adjust", "IRR (95% CI)", "変化率 % (95% CI)", "p_cluster", "n", "n_pos", "clusters", "converged"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4g}"))
    if not is_rv and a.repo_ref_pct is not None:
        ref_ = float(a.repo_ref_pct)
        inc = [f"{x.pos}/{x.comparator}/{x.adjust}: {'入る' if x.pct_low <= ref_ <= x.pct_high else '外れる'}" for x in df_.itertuples()]
        P(f"\n[参考値 {ref_:+.1f}% が 95% 区間に入るか(包含の表示のみ。先行研究の値の定義[何を 1 としたか・何で調整したか]が同じとは限らない)]\n  " + "\n  ".join(inc))
    if not df_.converged.all():
        P("\n[注意] 収束しなかった推定があります: " + ", ".join(f"{x.pos}/{x.comparator}/{x.adjust}" for x in df_.itertuples() if not x.converged))
    P("読み方: 組=FM と FMP の差は、P(本文内・補足資料のみの共有)をリポジトリ共有に含めるかの感度。FMC は C(制限付きアクセス)を含める感度(FM との差が C の扱いの効果)。fe(共変量なし)と main(全共変量)の差は、"
      "共変量による調整の効果。比較対象を all→pa→a と狭めると、「データを生成しなかった・再利用だけ」の論文(N・R・C)を比較から外した推定になる。")


def _ratio_dir_report(w, m, P, tol=0.005):
    """v058: WoS と PMC の雑誌×類型の率比が 1 の同じ側にある数(w・m は journal・das・irr・p_holm_robust をもつ表)。組ごとの表を返す"""
    j = w.merge(m, on=["journal", "das"], suffixes=("_wos", "_pmc"))
    j["same"] = (np.log(j.irr_wos) * np.log(j.irr_pmc)) > 0
    j["near1"] = ((j.irr_wos - 1).abs() < tol) | ((j.irr_pmc - 1).abs() < tol)
    sig2 = (j.p_holm_robust_wos < 0.05) & (j.p_holm_robust_pmc < 0.05)
    n = len(j)
    P(f"\n[WoS と PMC の雑誌×類型の率比が 1 の同じ側にある数(有意性を問わない)] 比較 {n} 個 / 同じ向き {int(j.same.sum())} 個 / 逆向き {int((~j.same).sum())} 個")
    P(f"  両方が Holm 後 p<0.05 の {int(sig2.sum())} 個のうち、同じ向き {int((j.same & sig2).sum())} 個")
    nr = j[j.near1]
    if len(nr):
        P(f"  率比が 1 にきわめて近い(|IRR−1|<{tol})組 {len(nr)} 個(向きの数に含まれている。含める・除くで数が変わる):")
        P(nr[["journal", "das", "irr_wos", "irr_pmc", "same"]].assign(journal=lambda x: jshort(x.journal)).round(4).to_string(index=False))
    if (~j.same).any():
        P("  逆向きの組:")
        P(j[~j.same][["journal", "das", "irr_wos", "irr_pmc"]].assign(journal=lambda x: jshort(x.journal)).round(3).to_string(index=False))
    return j


def _extra_ratiodir(a, outdir, tag, P):
    """v058: 保存済みの check_extra_ratio_by_journal_<tag>.csv から、WoS と PMC の向きが同じ数を数える(回帰は走らせない)"""
    P("\n===== WoS と PMC の雑誌×類型の率比の向き(保存済みの表から) =====")
    f = os.path.join(outdir, f"check_extra_ratio_by_journal_{tag}.csv")
    if not os.path.isfile(f):
        P(f"  {f} がありません。先に --check-extra ratio を --dv wos_TC で実行してください")
        return
    d_ = pd.read_csv(f)
    if "model" not in d_ or not {"wos", "pmc"} <= set(d_.model):
        P("  表に wos と pmc の両方の行がありません")
        return
    j = _ratio_dir_report(d_[d_.model == "wos"], d_[d_.model == "pmc"], P)
    j.to_csv(os.path.join(outdir, f"check_extra_ratiodir_{tag}.csv"), index=False, encoding="utf-8-sig")


EXTRA_ALL = ["tost", "meta", "revalt", "loo", "age", "field", "subfield", "aft", "window", "ratio", "ratiodir", "repo"]


def check_extra(a, outdir):
    import copy
    a = copy.copy(a)
    a.nb_sample, a.exposure = 0, "off"   # 全行で推定する。経過時間の扱いは各確認が自分で決める
    want = {x.strip() for x in a.check_extra.split(",") if x.strip()}
    if "all" in want:
        want = set(EXTRA_ALL)
    bad = want - set(EXTRA_ALL)
    if bad:
        sys.exit(f"--check-extra の指定が不明です: {sorted(bad)}(使えるもの: all, {', '.join(EXTRA_ALL)})")
    tag = _tag(a.dv)
    lines = []
    P = lines.append
    P(f"追加の確認 ({VERSION}) 従属変数 {a.dv} / 実行: {[x for x in EXTRA_ALL if x in want]} / 全行で推定(--nb-sample なし)/ 出力 {outdir}")
    d = meta = das_cols = ref = excl = None
    if want - {"meta", "ratiodir"}:
        d, meta, das_cols, ref, log = prepare(a)
        excl = {c.strip() for c in a.exclude.split(",") if c.strip()}
        P("\n".join(log))
    jobs = [("tost", lambda: _extra_tost(a, d, meta, das_cols, ref, excl, outdir, tag, P)),
            ("meta", lambda: _extra_meta(a, outdir, tag, P)),
            ("revalt", lambda: _extra_revalt(a, d, meta, das_cols, ref, excl, outdir, tag, P)),
            ("loo", lambda: _extra_loo(a, d, meta, das_cols, ref, excl, outdir, tag, P)),
            ("age", lambda: _extra_age(a, d, meta, das_cols, ref, excl, outdir, tag, P)),
            ("field", lambda: _extra_field(a, d, meta, das_cols, ref, excl, outdir, tag, P)),
            ("subfield", lambda: _extra_subfield(a, d, meta, das_cols, ref, excl, outdir, tag, P)),
            ("aft", lambda: _run_aft(a, d, meta, das_cols, ref, excl, outdir, tag, P)),
            ("window", lambda: _extra_window(a, d, meta, das_cols, ref, excl, outdir, tag, P)),
            ("ratio", lambda: _extra_ratio(a, d, meta, das_cols, ref, excl, outdir, tag, P)),
            ("ratiodir", lambda: _extra_ratiodir(a, outdir, tag, P)),
            ("repo", lambda: _extra_repo(a, d, meta, das_cols, ref, excl, outdir, tag, P))]
    for name, fn in jobs:
        if name not in want:
            continue
        print(f"[進捗] 追加の確認: {name}", file=sys.stderr, flush=True)
        t0 = time.time()
        try:
            fn()
        except Exception as e:   # 1 つの確認が失敗しても、ほかは続ける
            import traceback
            P(f"\n[失敗] {name}: {type(e).__name__}: {e}")
            traceback.print_exc()
        P(f"  ({name} の所要時間 {time.time() - t0:.0f} 秒)")
        txt = "\n".join(lines)
        with open(os.path.join(outdir, f"check_extra_{tag}{getattr(a, 'repo_suffix', '') or ''}.txt"), "w", encoding="utf-8") as f:   # 1 つ終わるたびに保存
            f.write(txt)
    print("\n".join(lines))
    print("保存先:", outdir)


# ---- v025 追加: 誤分類の補正の拡張(雑誌層別の混同行列・差異的な誤分類の感度分析)
def _em_pi(C, p_pred):
    """混同行列 C[真, 予測] が既知のとき、予測ラベルの割合 p_pred から真の類型の割合を EM で推定する"""
    pi = p_pred.copy()
    for _ in range(500):
        post = C * pi[:, None]
        post = post / post.sum(axis=0, keepdims=True)
        pi_new = post @ p_pred
        if np.abs(pi_new - pi).max() < 1e-10:
            return pi_new
        pi = pi_new
    return pi


def _scale_err(C, phi):
    """混同行列の各行(真の類型)で、誤分類される確率のオッズを phi 倍する。誤りの行き先の配分(正しくない列の比)は変えない"""
    C2 = C.copy()
    for k in range(C.shape[0]):
        e = 1.0 - C[k, k]
        if e <= 0 or e >= 1:
            continue
        odds = e / (1.0 - e) * phi
        e2 = odds / (1.0 + odds)
        off = C[k].copy()
        off[k] = 0.0
        if off.sum() > 0:
            C2[k] = off * (e2 / off.sum())
            C2[k, k] = 1.0 - e2
    return C2


def _rubin(betas, vars_):
    """Rubin の規則による統合。betas, vars_: 反復×係数(使えない反復は NaN)"""
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        Rk = np.isfinite(betas).sum(axis=0)
        with np.errstate(all="ignore"):
            qbar, ubar = np.nanmean(betas, axis=0), np.nanmean(vars_, axis=0)
            B = np.where(Rk > 1, np.nanvar(betas, axis=0, ddof=1), np.nan)
            T = ubar + (1 + 1 / Rk) * B
            rr = np.where(ubar > 0, (1 + 1 / Rk) * B / ubar, np.nan)
            dfr = (Rk - 1) * (1 + 1 / np.where(rr > 0, rr, np.nan)) ** 2
    dfr = np.where(np.isfinite(dfr), dfr, 1e6)
    se = np.sqrt(T)
    pv = np.array([_t_sf2(q / s, df) if np.isfinite(q) and np.isfinite(s) and s > 0 else np.nan for q, s, df in zip(qbar, se, dfr)])
    try:
        from scipy import stats
        crit = np.array([stats.t.ppf(0.975, df) for df in dfr])
    except Exception:
        crit = np.full(len(dfr), 1.96)
    with np.errstate(all="ignore"):
        fmi = (rr + 2 / (dfr + 3)) / (rr + 1)
    return dict(q=qbar, se=se, p=pv, crit=crit, B=B, fmi=fmi, Rk=Rk)


def _misclass_reps(a, ctx, full, cats, pred, strata, C_maker, R, label):
    """反復 R 回。各反復で C_maker(rng) が返す層ごとの混同行列(リスト)から、層ごとに EM で真の割合を推定し、
    予測ラベルを条件に真の類型を引き直して主 NB モデルを推定する。戻り値: (betas, vars_, 引いた件数の配列)"""
    X, y, nbd, gc, names = ctx["X"], ctx["y"], ctx["nbd"], ctx["gcodes"], ctx["names"]
    das_idx = {n: i for i, n in enumerate(names) if n in ctx["das_cols"]}
    K, n = len(cats), len(pred)
    S = int(strata.max()) + 1
    rng = np.random.default_rng(a.seed)
    betas, vars_, ncls = [], [], []
    ii_das = [das_idx[c] for c in ctx["das_cols"]]
    for r in range(R):
        print(f"[進捗] {label} 反復 {r + 1}/{R}", file=sys.stderr, flush=True)
        Cs = C_maker(rng)
        new = np.empty(n, dtype=int)
        for s in range(S):
            ii = np.where(strata == s)[0]
            if len(ii) == 0:
                continue
            ps = pred[ii]
            p_s = np.bincount(ps, minlength=K) / len(ii)
            pi = _em_pi(Cs[s], p_s)
            Q = Cs[s] * pi[:, None]
            Q = Q / Q.sum(axis=0, keepdims=True)
            for j in range(K):
                jj = ii[ps == j]
                if len(jj):
                    new[jj] = rng.choice(K, size=len(jj), p=Q[:, j])
        nc_r = np.bincount(new, minlength=K)
        ncls.append(nc_r)
        for nm, i in das_idx.items():
            X[:, i] = (new == cats.index(nm[4:])).astype(float)
        fr = nb_fit(X, nbd, b0=full["beta"], a0=full["alpha"])
        cv = nb_cov(fr, X, y, codes=gc)
        bb, vv = fr["beta"][ii_das].copy(), np.diag(cv["cluster"])[ii_das].copy()
        for q, c_ in enumerate(ctx["das_cols"]):
            if nc_r[cats.index(c_[4:])] < a.noise_min_count:
                bb[q], vv[q] = np.nan, np.nan
        betas.append(bb)
        vars_.append(vv)
    return np.array(betas), np.array(vars_), np.array(ncls)


def _ncls_summary(ncls, cats, das_names, min_count):
    """v028: 補正後に類型 k と判定された件数(反復ごと)の分布。少ない類型が有効な反復から外れる理由を見るため"""
    rows = []
    for v in das_names:
        k = cats.index(v[4:])
        x = ncls[:, k]
        rows.append({"variable": v, "min": int(x.min()), "median": float(np.median(x)), "max": int(x.max()),
                     "reps_ge_min_count": int((x >= min_count).sum()), "reps": len(x)})
    return pd.DataFrame(rows)


def _ext_suffix(a, what):
    """v029: 出力ファイル名に付ける、実行条件を表す接尾辞(例 _5fold_cv_group_min30_r20 / _phi0.5-1-2-3_r5)"""
    import re as _re
    parts = []
    src = a.reference_csv or a.confusion_csv or ""
    st = os.path.splitext(os.path.basename(os.path.expanduser(src)))[0]
    st = _re.sub(r"^annotation_1200_prediction_", "", st)
    if st:
        parts.append(_re.sub(r"[^A-Za-z0-9._-]+", "-", st)[:40])
    if "strat" in what:
        parts += [str(a.noise_strata), f"min{a.noise_min_count}", f"r{a.noise_reps}"]
        if float(a.noise_shrink) != 10.0:
            parts.append(f"shrink{a.noise_shrink:g}")
    if "diff" in what:
        phis = "-".join(x.strip() for x in str(a.diff_phi).split(",") if x.strip())
        parts += [f"phi{phis}", f"dr{a.diff_reps}"]
    if "fm" in what:
        parts += ["fm" + "-".join(x.strip() for x in str(a.fm_rates).split(",") if x.strip()), f"fr{a.fm_reps}", f"min{a.noise_min_count}"]
    return "_" + "_".join(parts) if parts else ""


def check_misclass_ext(a, outdir):
    """誤分類の補正の拡張。(strat) 参照セットの混同行列を雑誌のグループごとに作り(少ない件数は全体の行で縮める)、雑誌によって誤り方が違う場合の補正を行う。
    (diff) 誤分類の確率が被引用数(または日数)の高い論文と低い論文で違う(差異的)場合の感度分析。雑誌×年内の順位で上位半分・下半分に分け、
    上位半分では誤分類のオッズを φ 倍、下半分では 1/φ 倍にして補正し、DAS の率比が φ でどう動くかを見る"""
    what = {w.strip() for w in a.check_misclass_ext.split(",") if w.strip()}
    if "all" in what:
        what = {"strat", "diff"}
    bad = what - {"strat", "diff", "fm"}
    if bad:
        sys.exit(f"--check-misclass-ext の指定が不明です: {sorted(bad)}(使えるもの: all(=strat,diff), strat, diff, fm)")
    if not a.reference_csv and not a.confusion_csv:
        sys.exit("--check-misclass-ext には --reference-csv(1 行 1 文: 雑誌・人手のラベル・予測ラベル)が必要です。diff だけなら --confusion-csv(全体の混同行列)でも動きます")
    if "strat" in what and not a.reference_csv:
        sys.exit("strat には --reference-csv が必要です(雑誌ごとの混同行列を作るため)")
    for opt, path in (("--reference-csv", a.reference_csv), ("--confusion-csv", a.confusion_csv)):   # v026: 時間のかかる推定の前にファイルの有無を確かめる
        if path and not os.path.isfile(os.path.expanduser(path)):
            import glob
            cand = sorted(set(glob.glob(os.path.expanduser("~/*.csv")) + glob.glob("*.csv") + glob.glob(os.path.join(outdir, "**", "*.csv"), recursive=True)))
            cand = [c for c in cand if any(k in os.path.basename(c).lower() for k in ("ref", "confus", "human", "label", "annot"))][:10]
            sys.exit(f"{opt} のファイルが見つかりません: {os.path.expanduser(path)}\n"
                     + ("近い名前の CSV: " + ", ".join(cand) + "\n" if cand else "")
                     + "(例の reference_1200.csv は仮の名前です。実際の参照セット(1 行 1 文: 雑誌・人手のラベル・予測ラベル)のパスを指定してください。"
                       "diff だけなら、集計済みの混同行列 --confusion-csv でも動きます)")
    sfx = _ext_suffix(a, what)   # v029
    d, meta, das_cols, ref, log = prepare(a)
    excl = {c.strip() for c in a.exclude.split(",") if c.strip()}
    tag = _tag(a.dv)
    cats = [ref] + [c[4:] for c in das_cols]
    K = len(cats)
    print("[進捗] 主モデル(ラベルを替えない)を推定中", file=sys.stderr, flush=True)
    ctx, full, cov, idx, t0 = _fit_das(d, meta, das_cols, ref, excl, a, "main")
    n = len(ctx["y"])
    pred = pd.Categorical(d.loc[ctx["use"].index, "das_label"].values, categories=cats).codes
    lines = []
    P = lines.append
    P(f"誤分類の補正の拡張 ({VERSION}) 従属変数 {a.dv} / 基準 {ref} / 分析した行 {n:,} / 層化: {a.noise_strata} / 最小件数 {a.noise_min_count}")
    # 参照セット
    ref_df = None
    if a.reference_csv:
        ref_df = pd.read_csv(os.path.expanduser(a.reference_csv), dtype=str, keep_default_na=False)
        cj, ch, cp = [c.strip() for c in a.ref_cols.split(",")]
        for c_ in (cj, ch, cp):
            if c_ not in ref_df:
                sys.exit(f"--reference-csv に列 {c_} がありません(列: {list(ref_df.columns)}。--ref-cols 雑誌,人手,予測 で指定)")
        ref_df = ref_df.rename(columns={cj: "journal", ch: "human", cp: "pred"})
        ref_df["human"], ref_df["pred"] = ref_df.human.str.strip(), ref_df.pred.str.strip()
        n_raw = len(ref_df)
        ref_df = ref_df[ref_df.human.isin(cats) & ref_df.pred.isin(cats)].copy()
        P(f"参照セット {a.reference_csv}: {n_raw} 行 → 使う類型のみ {len(ref_df)} 行")
        cnt_pool = np.zeros((K, K))
        for h, p_ in zip(ref_df.human, ref_df.pred):
            cnt_pool[cats.index(h), cats.index(p_)] += 1
    else:
        conf = pd.read_csv(os.path.expanduser(a.confusion_csv), index_col=0)
        conf.index, conf.columns = [str(x).strip() for x in conf.index], [str(x).strip() for x in conf.columns]
        miss = [c for c in cats if c not in conf.index or c not in conf.columns]
        if miss:
            sys.exit(f"混同行列に類型 {miss} の行または列がありません(必要な類型: {cats})")
        cnt_pool = conf.loc[cats, cats].values.astype(float)
    P("[全体の混同行列(行=人手、列=予測)の件数: " + ", ".join(f"{c}={int(cnt_pool[k].sum())}" for k, c in enumerate(cats)) + "]")
    P("[全体の再現率] " + ", ".join(f"{c}={cnt_pool[k, k] / max(cnt_pool[k].sum(), 1):.3f}" for k, c in enumerate(cats)))
    ii_das = [i for i, nm in enumerate(ctx["names"]) if nm in ctx["das_cols"]]
    das_names = ctx["das_cols"]

    def table(pool, ncls, extra=None):
        out = pd.DataFrame({"variable": das_names, "irr_naive": t0.irr.values, "p_holm_naive": t0.p_holm.values,
                            "irr_pooled": np.exp(pool["q"]), "irr_low": np.exp(pool["q"] - pool["crit"] * pool["se"]),
                            "irr_high": np.exp(pool["q"] + pool["crit"] * pool["se"]), "p_pooled": pool["p"]})
        ok = np.isfinite(pool["p"])
        out["p_holm_pooled"] = np.nan
        if ok.any():
            out.loc[ok, "p_holm_pooled"] = holm(pool["p"][ok])
        out["between_sd"], out["fmi"], out["n_valid_reps"] = np.sqrt(pool["B"]), pool["fmi"], pool["Rk"]
        out["mean_n"] = [float(ncls[:, cats.index(v[4:])].mean()) for v in das_names]
        out["dlog_vs_naive"] = pool["q"] - np.log(t0.irr.values)
        return out

    old_path = os.path.join(outdir, f"nb_misclass_{tag}.csv")
    # ---- (strat)
    if "strat" in what:
        P("\n" + "=" * 78 + "\n[strat] 雑誌のグループごとの混同行列による補正\n" + "=" * 78)
        jk = d.loc[ctx["use"].index, "journal_key"].astype(str).str.upper().values
        if a.noise_strata == "journal":
            ref_df["stratum"] = ref_df.journal.str.strip().str.upper()
            art_s = pd.Series(jk)
        elif a.noise_strata == "two":   # v028: big3 とそれ以外の 2 層(M の参照セットが少ないときに層を減らす用)
            _g2 = lambda j_: "big3" if _jgroup(j_) == "big3" else "other"
            ref_df["stratum"] = [_g2(j_) for j_ in ref_df.journal]
            art_s = pd.Series([_g2(j_) for j_ in jk])
        else:
            ref_df["stratum"] = [_jgroup(j_) for j_ in ref_df.journal]
            art_s = pd.Series([_jgroup(j_) for j_ in jk])
        names_s = sorted(set(art_s.unique()) | set(ref_df.stratum.unique()))
        strata = pd.Categorical(art_s.values, categories=names_s).codes
        cnt_s = {}
        for s_ in names_s:
            m = ref_df[ref_df.stratum == s_]
            c_ = np.zeros((K, K))
            for h, p_ in zip(m.human, m.pred):
                c_[cats.index(h), cats.index(p_)] += 1
            cnt_s[s_] = c_
        P(f"層(論文数 / 参照セットの文数): " + ", ".join(f"{s_}({int((art_s == s_).sum()):,} / {int(cnt_s[s_].sum())})" for s_ in names_s))
        if a.noise_strata == "group":
            _rj = ref_df.groupby("stratum").journal.nunique().to_dict()
            P(f"[v027 確認] 参照セットの層ごとの雑誌数: {_rj}(big3=3, heliyon=1, mdpi6=6 が想定)")
            if _rj.get("big3") != 3 or _rj.get("heliyon") != 1 or _rj.get("mdpi6") != 6:
                print(f"[警告] 参照セットの雑誌の振り分けが想定と違います: {_rj}。雑誌名の表記と BIG3_KEYS・BIG3_SHORT_KEYS を確認してください", file=sys.stderr)
        empt = [s_ for s_ in names_s if cnt_s[s_].sum() == 0 and (art_s == s_).any()]
        if empt:
            P(f"[注意] 参照セットに文がない層 {empt} は、全体の混同行列だけ(縮め先)で補正する。--noise-strata の指定や雑誌名の対応(BIG3_KEYS・HELIYON_KEY)を確認してください")
        P("[層ごとの再現率(真の類型ごと。参照セットの件数が 5 未満は NA)]")
        rec = pd.DataFrame({s_: [(cnt_s[s_][k, k] / cnt_s[s_][k].sum() if cnt_s[s_][k].sum() >= 5 else np.nan) for k in range(K)] for s_ in names_s}, index=cats)
        rec["全体"] = [cnt_pool[k, k] / max(cnt_pool[k].sum(), 1) for k in range(K)]
        P(rec.to_string(float_format=lambda x: f"{x:.3f}"))
        Pp = (cnt_pool + a.noise_prior)
        Pp = Pp / Pp.sum(axis=1, keepdims=True)

        def make_strat(rng):
            Cs = []
            for s_ in names_s:
                Cs.append(np.vstack([rng.dirichlet(cnt_s[s_][k] + a.noise_prior + a.noise_shrink * Pp[k]) for k in range(K)]))
            return Cs
        betas, vars_, ncls = _misclass_reps(a, ctx, full, cats, pred, strata, make_strat, a.noise_reps, "strat")
        out = table(_rubin(betas, vars_), ncls)
        P(f"\n[strat: DAS の率比(基準 {ref})。反復 {a.noise_reps} / Dirichlet の事前件数 {a.noise_prior} + 全体の行の割合 × {a.noise_shrink:g}(縮め)]")
        P(out.to_string(index=False, float_format=lambda x: f"{x:.4g}"))
        if os.path.exists(old_path):
            o = pd.read_csv(old_path).set_index("variable")
            P("[参考: --check-misclass(全体の混同行列)の統合値 irr_pooled(Holm 後 p) → strat]")
            for r in out.itertuples():
                if r.variable in o.index:
                    P(f"  {r.variable}: {o.loc[r.variable, 'irr_pooled']:.3f} ({o.loc[r.variable, 'p_holm_pooled']:.3g}) → {r.irr_pooled:.3f} ({r.p_holm_pooled:.3g})")
        out.to_csv(os.path.join(outdir, f"nb_misclass_strat_{tag}{sfx}.csv"), index=False, encoding="utf-8-sig")
        P(f"[v028 補正後の類型ごとの件数の分布(反復ごと)。--noise-min-count={a.noise_min_count} 以上の反復だけが統合に使われる]")
        P(_ncls_summary(ncls, cats, das_names, a.noise_min_count).to_string(index=False))
        P("読み方: 層別にしても pooled の向きと Holm 後の有意性が全体の混同行列の結果と同じなら、雑誌(分野)によって誤り方が違うことは結論を変えていない。"
          "ただし、層ごとの参照セットは 120〜720 件と少なく、縮めの強さ(--noise-shrink)に依存する。同じ雑誌の中の誤り方の違いは扱えない。")
    # ---- (diff)
    if "diff" in what:
        P("\n" + "=" * 78 + "\n[diff] 差異的な誤分類(誤り方が結果の大小と関連する場合)の感度分析\n" + "=" * 78)
        pct = pd.Series(ctx["y"]).groupby(ctx["gcodes"]).rank(pct=True, method="average").values
        strata = (pct > 0.5).astype(int)
        P(f"雑誌×年の中の順位で、上位半分(1)= {int(strata.sum()):,} 行、下半分(0)= {int((1 - strata).sum()):,} 行。"
          "上位半分では各類型の誤分類のオッズを φ 倍、下半分では 1/φ 倍にする。φ=1 は非差異的(全体の混同行列)。φ>1 は、結果の大きい論文ほど誤分類されやすいという想定。")
        phis = [float(x) for x in str(a.diff_phi).split(",") if x.strip()]
        rows_all, summ = [], {}
        for phi in phis:
            def make_diff(rng, phi=phi):
                C = np.vstack([rng.dirichlet(cnt_pool[k] + a.noise_prior) for k in range(K)])
                return [_scale_err(C, 1.0 / phi), _scale_err(C, phi)]          # 層 0(下半分)、層 1(上半分)
            betas, vars_, ncls = _misclass_reps(a, ctx, full, cats, pred, strata, make_diff, a.diff_reps, f"diff φ={phi:g}")
            out = table(_rubin(betas, vars_), ncls)
            out.insert(0, "phi", phi)
            rows_all.append(out)
            summ[phi] = out
        allr = pd.concat(rows_all, ignore_index=True)
        allr.to_csv(os.path.join(outdir, f"nb_misclass_diff_{tag}{sfx}.csv"), index=False, encoding="utf-8-sig")
        P(f"\n[diff: DAS の率比 pooled(Holm 後 p)。φ ごとに {a.diff_reps} 回の反復を Rubin の規則で統合。naive は補正なしの主モデル]")
        tab = pd.DataFrame({"variable": das_names, "naive": [f"{r.irr:.3f} ({r.p_holm:.3g})" for r in t0.itertuples()]})
        for phi in phis:
            o = summ[phi]
            tab[f"φ={phi:g}"] = [f"{r.irr_pooled:.3f} ({r.p_holm_pooled:.3g})" if np.isfinite(r.irr_pooled) else "NA" for r in o.itertuples()]
        P(tab.to_string(index=False))
        P("\n[各類型の結論が変わる φ(向きが 1 をまたぐ、または Holm 後 p が 0.05 以上になる)]")
        for k, v in enumerate(das_names):
            flips = []
            for phi in phis:
                r = summ[phi].iloc[k]
                if not np.isfinite(r.irr_pooled):
                    continue
                sig0 = t0.p_holm.values[k] < 0.05
                if (np.log(r.irr_pooled) * np.log(t0.irr.values[k]) < 0) or (sig0 and not r.p_holm_pooled < 0.05) or ((not sig0) and r.p_holm_pooled < 0.05):
                    flips.append(f"{phi:g}")
            P(f"  {v[4:]}: " + (", ".join(flips) if flips else "試した範囲では変わらない"))
        P("読み方: 試した φ の範囲(例: 0.5〜3 = 誤分類のオッズが上位・下位で 2〜3 倍違う)で P・A・R の向きと有意性が変わらなければ、"
          "分類の誤りが分野などを通じて被引用数と関連していても、結論は保たれる。φ の値は研究者が決める想定で、結果から選ばない。"
          "反復が少ない(--diff-reps)と、反復間の分散の推定が粗く p は不安定になる。誤分類の確率の差し方はこの一通りで、ほかの形の差異的誤分類は扱えない。")
    # ---- (fm) v030: F→M の誤分類率の感度分析
    if "fm" in what:
        P("\n" + "=" * 78 + "\n[fm] F→M の誤分類率を変えたときの M の率比の感度分析\n" + "=" * 78)
        if ref not in cats or "M" not in cats:
            sys.exit("fm には基準類型と M が必要です")
        kF, kM = cats.index(ref), cats.index("M")
        rates = [float(x) for x in str(a.fm_rates).split(",") if x.strip()]
        x_fm, n_fm = int(cnt_pool[kF, kM]), int(cnt_pool[kF].sum())
        try:
            from scipy import stats as _st
            lo = _st.beta.ppf(0.025, x_fm, n_fm - x_fm + 1) if x_fm > 0 else 0.0
            hi = _st.beta.ppf(0.975, x_fm + 1, n_fm - x_fm) if x_fm < n_fm else 1.0
        except Exception:
            lo = hi = float("nan")
        p_cnt = np.bincount(pred, minlength=K)
        P(f"参照セットの {ref}→M: {x_fm} / {n_fm} = {x_fm / max(n_fm, 1):.4f}(Clopper-Pearson 95% 区間 {lo:.4f}〜{hi:.4f})")
        P(f"補正前の予測の件数: {ref}={int(p_cnt[kF]):,}, M={int(p_cnt[kM]):,}(分析した行)")

        def with_fm(C, r):
            C2 = C.copy()
            oth = [j for j in range(K) if j not in (kF, kM)]
            C2[kF, kM] = r
            C2[kF, kF] = 1.0 - r - C2[kF, oth].sum()
            if C2[kF, kF] < 0.5:
                sys.exit(f"F→M = {r} では F の再現率が 0.5 を下回ります。--fm-rates を小さくしてください")
            return C2
        Pp0 = cnt_pool + a.noise_prior
        Pp0 = Pp0 / Pp0.sum(axis=1, keepdims=True)
        psh = p_cnt / p_cnt.sum()
        P("\n[点推定の混同行列(モデルを当てない概算): F→M の率ごとの、補正後の M の件数と P(真の M | 予測 M)]")
        pre = []
        for r in rates:
            C0 = with_fm(Pp0, r)
            pi = _em_pi(C0, psh)
            Q = C0 * pi[:, None]
            Q = Q / Q.sum(axis=0, keepdims=True)
            pre.append({"F→M の率": r, "F→M の期待件数": r * pi[kF] * len(pred), "補正後の M の件数": pi[kM] * len(pred), "P(真の M|予測 M)": Q[kM, kM]})
        P(pd.DataFrame(pre).to_string(index=False, float_format=lambda x: f"{x:.4g}"))
        zer = np.zeros(len(pred), dtype=int)
        rows_fm, summ_fm = [], {}
        for r in rates:
            def make_fm(rng, r=r):
                C = np.vstack([rng.dirichlet(cnt_pool[k] + a.noise_prior) for k in range(K)])
                return [with_fm(C, r)]
            betas, vars_, ncls = _misclass_reps(a, ctx, full, cats, pred, zer, make_fm, a.fm_reps, f"fm F→M={r:g}")
            out = table(_rubin(betas, vars_), ncls)
            out.insert(0, "fm_rate", r)
            rows_fm.append(out)
            summ_fm[r] = (out, ncls)
        allfm = pd.concat(rows_fm, ignore_index=True)
        allfm.to_csv(os.path.join(outdir, f"nb_misclass_fm_{tag}{sfx}.csv"), index=False, encoding="utf-8-sig")
        kMv = das_names.index("das_M")
        naive_M = t0.irr.values[kMv]
        P(f"\n[fm: M の率比(基準 {ref})。補正なしは {naive_M:.3f}(Holm 後 p {t0.p_holm.values[kMv]:.3g})。反復 {a.fm_reps}、--noise-min-count={a.noise_min_count} 未満の反復は除く]")
        mt, lost = [], None
        for r in rates:
            o, nc = summ_fm[r]
            rM = o.iloc[kMv]
            ok = bool(np.isfinite(rM.irr_pooled))
            keep = ok and (np.log(rM.irr_pooled) * np.log(naive_M) > 0) and (rM.p_holm_pooled < 0.05)
            if (not keep) and lost is None:
                lost = r
            mt.append({"F→M の率": r, "補正後の M の件数(平均)": rM.mean_n, "有効な反復": int(rM.n_valid_reps), "irr_pooled": rM.irr_pooled,
                       "irr_low": rM.irr_low, "irr_high": rM.irr_high, "p_holm": rM.p_holm_pooled,
                       "M の結論": "保たれる" if keep else ("推定不能" if not ok else "消える")})
        P(pd.DataFrame(mt).to_string(index=False, float_format=lambda x: f"{x:.4g}"))
        P("\n[fm: 全類型の率比 pooled(Holm 後 p)]")
        tab = pd.DataFrame({"variable": das_names, "naive": [f"{r_.irr:.3f} ({r_.p_holm:.3g})" for r_ in t0.itertuples()]})
        for r in rates:
            o = summ_fm[r][0]
            tab[f"F→M={r:g}"] = [f"{q.irr_pooled:.3f} ({q.p_holm_pooled:.3g})" if np.isfinite(q.irr_pooled) else "NA" for q in o.itertuples()]
        P(tab.to_string(index=False))
        if lost is None:
            P(f"\n[結論] 試した範囲(F→M = {min(rates):g}〜{max(rates):g})では、M の向きと Holm 後の有意性は変わらない。")
        else:
            below = [r for r in rates if r < lost]
            P(f"\n[結論] M の結論(向きが補正なしと同じで Holm 後 p<0.05)は、F→M の率が {lost:g} 以上で保てなくなる"
              + (f"({max(below):g} までは保たれる)。" if below else "(試した最小の率でも保てない)。")
              + f" 参照セットの実測は {x_fm / max(n_fm, 1):.4f}(95% 区間 {lo:.4f}〜{hi:.4f})。")
        P("読み方: 率は研究者が決める候補で、結果から選ばない。F→M 以外の誤り(F の他の行き先、M→F など)は参照セットの値のまま。"
          "F→M を大きくするときは、F の再現率が下がる分だけで調整している。M の参照セットは 12 件と少なく、M の再現率の不確かさは、反復の中の Dirichlet 抽出にだけ反映される。"
          "予測が M の件数に比べて F→M の期待件数が大きいと、補正後の M の件数が 0 に近づき、M は推定できなくなる(その率が実質的な境目)。")
    txt = "\n".join(lines)
    print(txt)
    with open(os.path.join(outdir, f"check_misclass_ext_{tag}{sfx}.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    print("保存先:", outdir)


# ---- v039 追加: OpenAlex primary_topic の取得 → 結合 → subfield を入れた感度分析(パイプライン)
# fetch_openalex_topics.py(取得・結合)を統合し、論文単位の分野(OpenAlex の topic→subfield→field→domain)を
# 統制した NB を --check-extra subfield として追加した。取得結果の形式(openalex_topics.jsonl)は従来と同じ。
import datetime
import urllib.error
import urllib.parse
import urllib.request

OA_COLS = ["oa_topic", "oa_subfield", "oa_field", "oa_domain", "oa_topic_score"]
OA_ENDPOINT = "https://api.openalex.org/works"


class OABudgetExhausted(Exception):
    """OpenAlex の 1 日の予算(クレジット)を使い切った。リセット時刻(UTC の文字列)を持つ"""


def _oa_norm(d):
    d = str(d).strip().lower()
    for p in ("https://doi.org/", "http://doi.org/", "https://dx.doi.org/", "doi:"):
        if d.startswith(p):
            d = d[len(p):]
    return d


def _oa_rate_limit(api_key):
    """残りの予算を OpenAlex に問い合わせる(失敗したら空の dict)。キーは表示しない"""
    try:
        url = "https://api.openalex.org/rate-limit?" + urllib.parse.urlencode({"api_key": api_key})
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.load(r).get("rate_limit", {}) or {}
    except Exception:
        return {}


def _oa_reset_text(resets_at):
    try:
        t = datetime.datetime.fromisoformat(str(resets_at).replace("Z", "+00:00"))
        return f"{t.strftime('%Y-%m-%d %H:%M')} UTC(この Mac の時刻では {t.astimezone().strftime('%Y-%m-%d %H:%M')})"
    except Exception:
        return str(resets_at)


def _oa_fetch(batch, mailto, api_key, select="doi,primary_topic"):
    """DOI の束(最大 100)の primary_topic を取る。予算切れなら OABudgetExhausted、再試行を使い切ったら None"""
    q = {"filter": "doi:" + "|".join(batch), "select": select, "per-page": str(len(batch))}
    if mailto:
        q["mailto"] = mailto
    q["api_key"] = api_key
    url = OA_ENDPOINT + "?" + urllib.parse.urlencode(q, quote_via=urllib.parse.quote, safe=":|/")
    for k in range(5):
        wait = 5 * 2 ** k
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)["results"]
        except urllib.error.HTTPError as e:
            if e.code == 401:
                sys.exit("HTTP 401: API キーが無効か、渡せていません。--oa-api-key か環境変数 OPENALEX_API_KEY を確認してください"
                         "(キーを再発行した場合は新しいキーを使います)")
            if e.code == 429:
                rl = _oa_rate_limit(api_key)
                rem, cr = rl.get("daily_remaining_usd"), rl.get("credits_remaining")
                if (rem is not None and rem < 0.0002) or (cr is not None and cr < 2):
                    raise OABudgetExhausted(rl.get("resets_at", ""))
                print(f"HTTP 429(一時的な制限): {wait} 秒待って再試行", file=sys.stderr)
            elif e.code in (500, 502, 503, 504):
                print(f"HTTP {e.code}: {wait} 秒待って再試行", file=sys.stderr)
            else:
                sys.exit(f"HTTP {e.code}: {e.read()[:300]!r}")
        except Exception as e:
            print(f"通信エラー {type(e).__name__}: {wait} 秒待って再試行", file=sys.stderr)
        time.sleep(wait)
    return None


def _oa_rec(doi, w):
    t = (w or {}).get("primary_topic") or {}
    g = lambda k: (t.get(k) or {}).get("display_name", "")
    return {"doi": doi, "oa_topic": t.get("display_name", ""), "oa_subfield": g("subfield"),
            "oa_field": g("field"), "oa_domain": g("domain"), "oa_topic_score": t.get("score", "")}


def _oa_paths(a):
    return (os.path.expanduser(a.csv), os.path.expanduser(a.oa_cache), os.path.expanduser(a.oa_out))


def _oa_save_meta(a, cachep, n_dois, n_done):
    """取得日・取得条件を記録する(論文の Methods と Zenodo の寄託用)。openalex_topics_meta.json"""
    mp = os.path.join(os.path.dirname(cachep), "openalex_topics_meta.json")
    meta = {}
    if os.path.exists(mp):
        try:
            meta = json.load(open(mp, encoding="utf-8"))
        except Exception:
            meta = {}
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    meta.setdefault("first_run_utc", now)
    meta.update(dict(last_run_utc=now, script_version=VERSION, endpoint=OA_ENDPOINT, select="doi,primary_topic",
                     filter="doi (OR で束ねる)", batch_size=int(a.oa_batch), n_dois=int(n_dois), n_cached=int(n_done)))
    with open(mp, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    return mp


def oa_fetch_topics(a):
    """--csv の DOI の primary_topic を OpenAlex から取り、キャッシュ(jsonl)に追記する。取得済みは飛ばす(再開できる)。
    全件そろえば True、予算切れ・再試行切れで止まれば False"""
    csvp, cachep, _ = _oa_paths(a)
    api_key = a.oa_api_key or os.environ.get("OPENALEX_API_KEY", "").strip()
    if not api_key:
        sys.exit("OpenAlex の API キーがありません。--oa-api-key か環境変数 OPENALEX_API_KEY で渡してください(無料: https://openalex.org/settings/api-key)")
    api_key = "".join(api_key.split())
    batch_n = max(1, min(int(a.oa_batch), 100))
    dois = pd.read_csv(csvp, usecols=["DOI"], dtype=str, keep_default_na=False)["DOI"].map(_oa_norm)
    dois = [x for x in dict.fromkeys(dois) if x]
    if a.oa_limit:
        dois = dois[:a.oa_limit]
    done = set()
    if os.path.exists(cachep):
        done = {json.loads(l)["doi"] for l in open(cachep, encoding="utf-8") if l.strip()}
    todo = [x for x in dois if x not in done]
    skip = [x for x in todo if "," in x]
    todo = [x for x in todo if "," not in x]
    print(f"DOI {len(dois):,} / 取得済み {len(done):,} / 今回 {len(todo):,} / カンマを含み除外 {len(skip)} / 1 回 {batch_n} 件", flush=True)
    rl = _oa_rate_limit(api_key)
    if rl:
        need = -(-len(todo) // batch_n)   # list は 1 回 1 クレジット
        print(f"今日の残り {rl.get('credits_remaining', '?')} クレジット / 必要 約 {need:,} クレジット / リセット {_oa_reset_text(rl.get('resets_at', ''))}", flush=True)
    os.makedirs(os.path.dirname(cachep) or ".", exist_ok=True)
    t0, complete = time.time(), True
    with open(cachep, "a", encoding="utf-8") as f:
        for i in range(0, len(todo), batch_n):
            batch = todo[i:i + batch_n]
            try:
                res = _oa_fetch(batch, a.oa_mailto, api_key)
            except OABudgetExhausted as e:
                print(f"\n今日の予算を使い切りました。取得済みは保存されています。{_oa_reset_text(str(e))} 以降に、同じコマンドで続きを取得してください。")
                complete = False
                break
            if res is None:
                print("\n再試行を使い切りました。しばらくしてから同じコマンドで再開してください。")
                complete = False
                break
            got = {_oa_norm(w["doi"]): w for w in res if w.get("doi")}
            for d_ in batch:
                f.write(json.dumps(_oa_rec(d_, got.get(d_)), ensure_ascii=False) + "\n")
            f.flush()
            n = i + len(batch)
            if (i // batch_n) % 20 == 0:
                left = (len(todo) - n) * (time.time() - t0) / n
                print(f"{n:,}/{len(todo):,}  残り約 {left / 60:.0f} 分", flush=True)
            time.sleep(a.oa_sleep)
    n_cached = sum(1 for l in open(cachep, encoding="utf-8") if l.strip())
    mp = _oa_save_meta(a, cachep, len(dois), n_cached)
    print(("取得完了。" if complete else "途中まで。") + f" 取得条件と日時: {mp}")
    return complete


def oa_merge_topics(a):
    """取得済みの結果を CSV に結合して書き出し、付与率・水準数を表示する。書き出した CSV のパスを返す"""
    csvp, cachep, outp = _oa_paths(a)
    rows = [json.loads(l) for l in open(cachep, encoding="utf-8") if l.strip()]
    t = pd.DataFrame(rows).drop_duplicates("doi", keep="last")
    d = pd.read_csv(csvp, dtype=str, keep_default_na=False, low_memory=False)
    d = d.drop(columns=[c for c in OA_COLS if c in d.columns])   # 結合済みの CSV を --csv に指定しても重複しない
    d["_doi"] = d["DOI"].map(_oa_norm)
    d = d.merge(t.rename(columns={"doi": "_doi"}), on="_doi", how="left").drop(columns="_doi")
    for c in OA_COLS:
        d[c] = d[c].fillna("")
    os.makedirs(os.path.dirname(outp) or ".", exist_ok=True)
    d.to_csv(outp, index=False, encoding="utf-8")
    print("書き出し:", outp, "行数", len(d))
    print("subfield あり:", f"{(d.oa_subfield != '').mean():.1%}")
    print(d.groupby(d.journal_key.str[:30]).oa_subfield.apply(lambda s: (s != "").mean()).round(3).to_string())
    print("subfield の水準数:", d.oa_subfield.replace("", pd.NA).nunique(), "/ field の水準数:", d.oa_field.replace("", pd.NA).nunique())
    cnt = d.assign(oa_field=d.oa_field, oa_subfield=d.oa_subfield).groupby(["oa_domain", "oa_field", "oa_subfield"]).size().rename("n").reset_index().sort_values("n", ascending=False)
    cp = os.path.join(os.path.dirname(outp), "topic_subfield_counts.csv")
    cnt.to_csv(cp, index=False, encoding="utf-8-sig")
    print("subfield 別の件数:", cp)
    return outp


# ---- 論文単位の分野(subfield・field)を統制した NB
def _topic_dummies(d, meta, col, top, min_n, prefix):
    """d[col] の上位 top 個(min_n 件以上)をダミーにして d と meta に加える。残りと欠損が基準側。加えた列名と情報を返す。
    d には列を直接加える(コピーしない。メモリのため)。呼び出し側が使い終わったら drop する。
    v040: info に map(列名→水準名)と baseline_levels(基準側の水準名)を加えた。列の追加で出る PerformanceWarning は止める"""
    import warnings
    fv = d[col].astype(str).str.strip().replace({"": np.nan, "nan": np.nan})
    vc = fv.value_counts()
    keep = [c for c in vc.index[:top] if vc[c] >= min_n]
    if keep and int((fv.isna() | ~fv.isin(keep)).sum()) < min_n:
        keep = keep[:-1]   # 基準側が足りないと完全な共線性になるので、最小の水準を基準側に回す
    names, lvl_map = [], {}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", pd.errors.PerformanceWarning)
        for c in keep:
            nm = prefix + re.sub(r"\W+", "_", c).strip("_")[:40]
            while nm in d or nm in meta:
                nm += "_x"
            d[nm] = (fv == c).astype(float)
            meta[nm] = dict(group="分野", desc=f"{col}={c} / 基準 その他", kind="bin", src=col, tr="dummy")
            names.append(nm)
            lvl_map[nm] = c
    ref_share = float((fv.isna() | ~fv.isin(keep)).mean())
    return names, dict(col=col, levels=int(len(vc)), dummies=len(names), missing=float(fv.isna().mean()), baseline_share=ref_share,
                       map=lvl_map, baseline_levels=[c for c in vc.index if c not in keep])


def _save_topic_coef(d, ctx, full, cov, names, info, sp, label, outdir, tag, P):
    """v040: 分野のダミーの係数(率比・95%CI・p・Holm 後の p・モデルの標本での件数)を CSV に保存する。補足表 S3・S4 の元"""
    want = set(names)
    idx = [i for i, n_ in enumerate(ctx["names"]) if n_ in want]
    t = _irr_table(full, cov, ctx["names"], idx, ctx["meta"])
    t["p_holm"] = holm(t.p_cluster.values)
    rows = ctx["use"].index
    t["level"] = [info["map"].get(v, v) for v in t.variable]
    t["n_articles"] = [int(d.loc[rows, v].sum()) for v in t.variable]
    t["spec"], t["spec_label"], t["n_model"] = sp, label, int(len(rows))
    t["baseline_n"] = int(len(rows) - t.n_articles.sum())
    bl = info["baseline_levels"]
    t["baseline_levels"] = "; ".join(bl) if len(bl) <= 5 else f"{len(bl)} other levels"
    t["col"] = info["col"]
    t = t.sort_values("n_articles", ascending=False)
    fn = os.path.join(outdir, f"check_extra_subfield_coef_{sp}_{tag}.csv")
    t.to_csv(fn, index=False, encoding="utf-8-sig")
    P(f"  分野の係数の表を保存: {fn}(係数 {len(t)} 個、基準側 {t.baseline_n.iloc[0]:,} 件)" if len(t) else "  分野の係数がありません")


def _topic_journal_dependence(d, P, outdir, tag):
    """subfield が雑誌とどれだけ重なるか(OpenAlex の分類器は雑誌名を入力に使うので、雑誌の固定効果と重なる)"""
    j = jshort(d.journal_key)
    s = d["oa_subfield"].replace("", np.nan)
    m = s.notna()
    if not m.any():
        P("  oa_subfield がすべて空です")
        return
    tab = pd.crosstab(j[m], s[m])
    obs = tab.values.astype(float)
    n = obs.sum()
    exp = np.outer(obs.sum(1), obs.sum(0)) / n
    chi2 = float(((obs - exp) ** 2 / exp).sum())
    k = min(obs.shape) - 1
    v = math.sqrt(chi2 / (n * k)) if k > 0 else float("nan")
    rows = []
    for jn in tab.index:
        r = tab.loc[jn]
        rows.append(dict(journal=jn, n=int(r.sum()), subfield_levels=int((r > 0).sum()), top_subfield=r.idxmax(),
                         top_share=float(r.max() / r.sum()), levels_for_80pct=int((r.sort_values(ascending=False).cumsum() / r.sum() < 0.8).sum() + 1)))
    t = pd.DataFrame(rows)
    t.to_csv(os.path.join(outdir, f"check_extra_subfield_journal_{tag}.csv"), index=False, encoding="utf-8-sig")
    P(f"[subfield と雑誌の関係] 件数 {int(n):,} / 雑誌 {tab.shape[0]} × subfield {tab.shape[1]} / Cramér の V = {v:.3f}(0 は無関係、1 は雑誌で subfield がほぼ決まる)")
    P(t.round(3).to_string(index=False))
    P("読み方: V が大きいほど、subfield は雑誌の固定効果とほぼ同じ情報になり、subfield を加えても DAS の率比は変わりにくい。"
      "OpenAlex の topic は題名・抄録・引用・雑誌名から機械学習で推定されるため、雑誌とは完全に独立ではない(OpenAlex の記載)。")


def _extra_subfield(a, d, meta, das_cols, ref, excl, outdir, tag, P):
    P("\n===== 論文単位の分野(OpenAlex primary_topic)の統制 =====")
    miss = [c for c in ("oa_subfield", "oa_field") if c not in d]
    if miss:
        P(f"  列 {miss} が CSV にありません。--fetch-topics → --merge-topics を実行し、--csv に結合後の CSV(pmc_wos_v27_3llms_topic.csv)を指定してください")
        return
    _topic_journal_dependence(d, P, outdir, tag)
    meta0 = {k: v for k, v in meta.items() if v["group"] != "分野"}   # --field-col で入れた分野は、ここでは使わない
    ctx0, full0, cov0, t0 = _fit_ctx(d, meta0, das_cols, excl, a)
    aic = lambda full: -2 * full["llf"] + 2 * (int(np.linalg.matrix_rank(full["A"])) + 1)
    res = {"分野なし(主モデル)": t0}
    summ = [dict(spec="分野なし(主モデル)", n=len(ctx0["y"]), dummies=0, lrt=np.nan, lrt_p=np.nan, wald=np.nan, wald_p=np.nan, aic=aic(full0))]
    specs = [s.strip() for s in a.subfield_variants.split(",") if s.strip()]
    for sp in specs:
        m_ = re.fullmatch(r"(field|domain|sub(\d*))", sp)
        if not m_:
            P(f"  --subfield-variants の指定が不明です: {sp}(field, domain, sub<個数> のどれか)")
            continue
        col, top, pre = (("oa_field", 999, "oaf_") if sp == "field" else (("oa_domain", 999, "oad_") if sp == "domain"
                         else ("oa_subfield", int(m_.group(2) or 50), "oas_")))
        if col not in d:
            P(f"  {sp}: 列 {col} がありません")
            continue
        meta1 = dict(meta0)
        names, info = _topic_dummies(d, meta1, col, top, a.min_cat, pre)
        label = {"field": "field(OpenAlex 26 分野)", "domain": "domain(4)"}.get(sp, f"subfield 上位{top}")
        P(f"[{label}] 列 {col}: 水準 {info['levels']} / ダミー {info['dummies']} / 欠損 {info['missing']:.1%} / 基準側(その他と欠損) {info['baseline_share']:.1%}")
        try:
            if not names:
                P("  ダミーがありません(件数の下限 --min-cat を満たす水準がない)")
                continue
            ctx1, full1, cov1, t1 = _fit_ctx(d, meta1, das_cols, excl, a)
            fi = [i for i, n_ in enumerate(ctx1["names"]) if n_ in set(names)]
            lr = 2 * (full1["llf"] - full0["llf"])
            w, pw = _wald(full1["beta"], cov1["cluster"], fi)
            P(f"  N={len(ctx1['y']):,}(分野なし {len(ctx0['y']):,})/ LRT χ²({len(fi)})={lr:.1f} p={chi2_sf(lr, len(fi)):.3g} / "
              f"Wald(クラスタ頑健) χ²({len(fi)})={w:.1f} p={pw:.3g} / AIC {aic(full1):,.1f}(分野なし {aic(full0):,.1f})")
            try:
                _save_topic_coef(d, ctx1, full1, cov1, names, info, sp, label, outdir, tag, P)
            except Exception as e:   # 係数表の保存に失敗しても、ほかの出力は続ける
                P(f"  [分野の係数表の保存に失敗] {type(e).__name__}: {e}")
            res[label] = t1
            summ.append(dict(spec=label, n=len(ctx1["y"]), dummies=len(fi), lrt=lr, lrt_p=chi2_sf(lr, len(fi)), wald=w, wald_p=pw, aic=aic(full1)))
        finally:
            d.drop(columns=[c for c in names if c in d], inplace=True)
    if len(res) > 1:
        rows = []
        for nm, t in res.items():
            for r in t.itertuples():
                rows.append(dict(spec=nm, variable=r.variable, irr=r.irr, low=r.irr_low, high=r.irr_high, p_cluster=r.p_cluster, p_holm=r.p_holm))
        vtag = "_".join(specs)   # v054: 指定した variants を名前に入れ、別の指定の実行で上書きされないようにする
        for stem, df_ in (("check_extra_subfield", pd.DataFrame(rows)), ("check_extra_subfield_fit", pd.DataFrame(summ))):
            df_.to_csv(os.path.join(outdir, f"{stem}_{tag}.csv"), index=False, encoding="utf-8-sig")        # 従来名(直近の実行)
            df_.to_csv(os.path.join(outdir, f"{stem}_{vtag}_{tag}.csv"), index=False, encoding="utf-8-sig")  # variants 入り(上書きされない)
        P(f"[DAS の率比(基準 {ref})。括弧内は Holm 補正後の p]")
        _compare_table(res, list(res), P)
        P("読み方: 分野を入れても向きと有意性が変わらなければ、DAS の関連は(OpenAlex の分類で測った)分野の違いだけでは説明されない。"
          "変わる類型は、分野の代理だった可能性がある。subfield は機械学習による推定で、全 247 水準を入れると行列が大きくなるため、上位だけをダミーにして、残りは基準側にまとめる。")


def topics_pipeline(a):
    """取得(再開可)→結合→subfield を入れた感度分析(被引用数と査読期間)を続けて行う。予算切れで止まったら、同じコマンドで再開する"""
    import copy
    if not oa_fetch_topics(a):
        print("\n取得が終わっていないので、結合と分析は行いません。同じコマンドで再開してください。")
        return
    outp = oa_merge_topics(a)
    for dv_ in ("wos_TC", "review_days"):
        b = copy.copy(a)
        b.csv, b.dv, b.check_extra = outp, dv_, "subfield"
        if _is_rv(dv_):
            b.review_as_iv, b.target = False, "citations"
        b.outdir = a.outdir if dv_ == "wos_TC" else DEFAULT_OUT_REVIEW
        od = os.path.expanduser(b.outdir)
        os.makedirs(od, exist_ok=True)
        print(f"\n===== subfield を入れた NB: {dv_} -> {od} =====", file=sys.stderr, flush=True)
        check_extra(b, od)


SUPP_FIELD_PANEL = {"field": "OpenAlex field (26 levels; one level and missing values form the baseline)",
                    "domain": "OpenAlex domain (4 levels; one level and missing values form the baseline)"}


def _supp_field_table(frames, caption, label, outcome):
    """v040: 分野の係数の補足表(longtable)。frames: [(仕様名, 係数の DataFrame)]。1 つの表に field・domain・subfield のパネルを並べる"""
    w = r"p{7.2cm}@{\hspace{4pt}}r@{\hspace{4pt}}c@{\hspace{4pt}}c@{\hspace{4pt}}c"
    head = "Level & Articles & IRR (95\\% CI) & $p$ & Holm $p$ \\\\"
    n_model = int(frames[0][1].n_model.iloc[0])
    note = (f"Negative binomial (NB2) models with journal and publication-year fixed effects, the 32 covariates, and the DAS categories (reference: F), "
            f"estimated in {n_model:,} articles with indicators for one OpenAlex classification at a time (one model per panel). IRR: incidence rate ratio with 95\\% confidence interval "
            f"based on standard errors clustered by journal-by-year group; the baseline of each panel has IRR 1. Articles: number of articles of the level in the model. "
            f"$p$: cluster-robust $p$-value. Holm $p$: Holm-adjusted $p$-value over the indicators of the panel. The DAS estimates of these models are in Table~\\ref{{tab:field}}. "
            f"OpenAlex classes are assigned by a machine classifier that uses the journal name, so the IRRs are conditional associations within journals and "
            f"should not be read as effects of the subject. Outcome: {outcome}")
    L = [rf"\begin{{longtable}}{{{w}}}", rf"\caption{{{caption}}}\label{{{label}}}\\", r"\toprule", head, r"\midrule", r"\endfirsthead",
         r"\multicolumn{5}{l}{\small\textit{Supplementary Table \thetable\ (continued)}}\\", r"\toprule", head, r"\midrule", r"\endhead",
         r"\midrule", r"\multicolumn{5}{r}{\small\textit{Continued on next page}}\\", r"\endfoot", r"\bottomrule",
         r"\multicolumn{5}{p{15.6cm}}{\footnotesize " + note + r"}\\", r"\endlastfoot"]
    for sp, t in frames:
        if sp in SUPP_FIELD_PANEL:
            ttl = SUPP_FIELD_PANEL[sp]
        else:
            m_ = re.fullmatch(r"sub(\d+)", sp)
            ttl = f"OpenAlex subfield (the {m_.group(1)} most frequent of 247; all other subfields and missing values form the baseline)" if m_ else sp
        bl = t.baseline_levels.iloc[0]
        bl_lab = f"Baseline (IRR 1): {_tex(bl)}" if isinstance(bl, str) and bl and sp in SUPP_FIELD_PANEL else "Baseline (IRR 1)"
        L.append(rf"\multicolumn{{5}}{{l}}{{\textit{{{_tex(ttl)}}}}} \\")
        L.append(rf"\quad {bl_lab} & {int(t.baseline_n.iloc[0]):,} & 1 & & \\")
        for r in t.itertuples():
            L.append(rf"\quad {_tex(str(r.level))} & {int(r.n_articles):,} & {r.irr:.3f} ({r.irr_low:.3f}--{r.irr_high:.3f}) & {_supp_p(r.p_cluster)} & {_supp_p(r.p_holm)} \\")
    L.append(r"\end{longtable}")
    return "\n".join(L)


def supp_field_tables(a):
    """v040: --check-extra subfield が保存した分野の係数の CSV から、補足表 S3(被引用数)・S4(査読期間)の tex を作る"""
    specs = [x.strip() for x in a.supp_field_specs.split(",") if x.strip()]
    pdir = os.path.expanduser(a.paper_dir or DEFAULT_PAPER)
    jobs = [("S3", os.path.expanduser(a.outdir), "citations_wos_TC", "Estimates for the OpenAlex subject classes in the negative binomial models for WoS citation counts.",
             "tab:s3", f"Web of Science Times Cited ({SUPP_WOS_DATE})."),
            ("S4", os.path.expanduser(a.paper_review_dir), "review_days", "Estimates for the OpenAlex subject classes in the negative binomial models for peer review duration.",
             "tab:s4", "days from receipt to acceptance; an IRR below 1 means a shorter expected review duration.")]
    blocks, made = [], []
    for sid, folder, tag, cap, lab, outcome in jobs:
        frames = []
        for sp in specs:
            f = os.path.join(folder, f"check_extra_subfield_coef_{sp}_{tag}.csv")
            if not os.path.exists(f):
                print(f"[補足表] {sid}: {f} がありません。--check-extra subfield を{'--dv review_days で' if tag == 'review_days' else ''}--subfield-variants {a.supp_field_specs} で実行してください", file=sys.stderr)
                continue
            frames.append((sp, pd.read_csv(f, keep_default_na=False)))
        if not frames:
            continue
        ns = {int(t.n_model.iloc[0]) for _, t in frames}
        if len(ns) > 1:
            print(f"[補足表] {sid}: 仕様ごとにモデルの件数が違います({sorted(ns)})。同じ標本で比べられません", file=sys.stderr)
        blocks.append(_supp_field_table(frames, cap, lab, outcome))
        made.append(sid)
    if not blocks:
        return
    pre = "\n".join([r"\documentclass[10pt,a4paper]{article}", r"\usepackage[margin=2.2cm]{geometry}", r"\usepackage{longtable,booktabs,amsmath}",
                     r"\renewcommand{\tablename}{Supplementary Table}", r"\renewcommand{\thetable}{S\arabic{table}}", r"\providecommand{\botrule}{\bottomrule}",
                     r"\begin{document}",
                     r"\begin{center}{\large\bfseries Supplementary tables}\\[2pt]", _tex(SUPP_TITLE) + r"\end{center}", r"\vspace{1em}",
                     r"\setcounter{table}{%d}" % (2 if made[0] == "S3" else 3)])
    doc = pre + "\n" + "\n\n\\clearpage\n".join(blocks) + "\n\n\\end{document}\n"
    sdir = os.path.join(pdir, "supplementary")
    os.makedirs(sdir, exist_ok=True)
    ftex = os.path.join(sdir, "IJDL_supplementary_field_tables.tex")
    with open(ftex, "w", encoding="utf-8") as fh:
        fh.write(doc)
    print(f"[補足表] {', '.join(made)} → {ftex}")
    if getattr(a, "supp_pdf", False):
        import shutil, subprocess
        if not shutil.which("pdflatex"):
            print("[補足表] pdflatex が見つからないため PDF は作りません。tex をお手元で組んでください", file=sys.stderr)
            return
        for _ in range(2):
            r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", os.path.basename(ftex)], cwd=sdir, capture_output=True, text=True)
        print("[補足表] PDF を作りました" if r.returncode == 0 else "[補足表] pdflatex が失敗しました(tex のログを確認してください)", file=sys.stderr if r.returncode else sys.stdout)



# ---- v042 追加: OpenAlex の年次被引用数(counts_by_year)を従属変数に使う
# 1) --fetch-counts / --merge-counts : DOI ごとに counts_by_year・cited_by_count・publication_year を取得して CSV に結合(oa_cy_<年>)
# 2) --dv oa_c<k> / oa_a<j> / oa_l<k> / oa_total : 従属変数。既存の分析(NB・LRT・交互作用・雑誌別・Shapley など)がそのまま動く
# 3) --oa-suite : 窓(2〜5 年)・出版後の年(0〜4 年目)・WoS・PMC を同じ設定で推定し、DAS の率比・寄与(LRT・平均限界効果)を並べる
OA_CNT_SELECT = "doi,publication_year,publication_date,cited_by_count,counts_by_year"
OA_CNT_COLS = ["oa_found", "oa_pubyear", "oa_pubdate", "oa_cited_total"]


def _oa_dv(dv):
    """従属変数名が OpenAlex の年次被引用数なら (種類, k) を返す。oa_c<k>=出版年を含む k 年の累積(k≥1)/ oa_a<j>=出版年から j 年後の 1 年分(j≥0)/
    oa_l<k>=直近の k 暦年(--oa-last-year まで。論文の出版年は問わない)/ oa_total=cited_by_count(全期間)。それ以外は None"""
    m = re.fullmatch(r"oa_([cal])(\d+)", str(dv))
    if m:
        k = int(m.group(2))
        if m.group(1) in ("c", "l") and k < 1:
            sys.exit(f"--dv {dv}: 窓の年数は 1 以上にしてください")
        return m.group(1), k
    if dv == "oa_total":
        return "t", 0
    return None


def _need_oa(a):
    return bool(_oa_dv(a.dv)) or bool(getattr(a, "oa_suite", False))


def _oa_needed_cols(a):
    """prepare が CSV から読む OpenAlex の列(年次の列は見出しから探す)"""
    if not _need_oa(a):
        return []
    head = pd.read_csv(os.path.expanduser(a.csv), nrows=0).columns
    cols = [c for c in OA_CNT_COLS if c in head] + [c for c in head if re.fullmatch(r"oa_cy_\d{4}", c)]
    fl = getattr(a, "oa_field", "field")
    if fl != "none":
        cols += [c for c in ("oa_domain", "oa_field", "oa_subfield") if c in head]
    return cols


def _oa_year_cols(d):
    return sorted((int(c[6:]), c) for c in d.columns if re.fullmatch(r"oa_cy_\d{4}", c))


def _oa_coverage_table(d, ycols):
    """v042: 出版年 Y ごとの確認。「全期間の被引用数が 20 以上の論文」について、Y 年以降の年次の値の合計が cited_by_count(全期間)と
    どれだけ一致するかを見る。値がない年(OpenAlex は 0 の年を省く)は 0 として足すので、出版直後の被引用 0 の年と、取得範囲の外を区別できる。
    一致する(差が 0)なら、Y 年以降の引用はすべて取得範囲に入っている。差が大きければ、Y 年以降の一部が範囲外(取得できる年より前)。
    share_exact=合計が全期間とちょうど一致する割合 / share_tol=差が max(1, 全期間の 2%) 以内の割合 / median_gap=差の全期間に対する割合の中央値"""
    found = ((d["oa_found"] == "1") & (num(d["oa_cited_total"]) >= 20)).to_numpy()
    yr = d["year"].to_numpy(float)
    tot = num(d["oa_cited_total"]).to_numpy(float)
    ys = np.array([t for t, _ in ycols])
    M = np.column_stack([num(d[c]).fillna(0).to_numpy(float) for _, c in ycols])
    rows = []
    for Y in sorted({int(v) for v in yr[found & ~np.isnan(yr)]}):
        m = found & (yr == Y)
        if m.sum() < 20:
            continue
        S = M[m][:, ys >= Y].sum(axis=1)
        gap = tot[m] - S
        tol = np.maximum(1.0, 0.02 * tot[m])
        rows.append(dict(year=Y, n_base=int(m.sum()), share_exact=float((gap == 0).mean()),
                         share_tol=float((np.abs(gap) <= tol).mean()), median_gap=float(np.median(gap / tot[m]))))
    return pd.DataFrame(rows)


def _oa_cover_year(d, ycols, a, log=None):
    """年次の値が使える最初の年。--oa-cover-from があればそれ。なければ、出版年別の share_tol が 0.9 以上に最後までとどまる最初の出版年
    (その出版年以降の論文は、出版年からの引用がすべて取得範囲に入っている)。窓は出版年を含むので、この年が窓の開始に使える最初の年になる"""
    if int(getattr(a, "oa_cover_from", 0) or 0):
        return int(a.oa_cover_from)
    t = _oa_coverage_table(d, ycols)
    t = t[t.year <= int(a.oa_last_year)].reset_index(drop=True)
    ok = (t.share_tol >= 0.9).to_numpy()
    cover = None
    for i in range(len(t)):
        if ok[i:].all():
            cover = int(t.year.iloc[i])
            break
    if cover is None:
        cover = int(t.year.iloc[-1])
    if log is not None:
        log.append("[OpenAlex 年次の被引用数] 取得できる年の範囲(出版年 Y の論文で、Y 年以降の年次の合計が全期間の累積と一致=差が 2% または 1 件以内の割合が 90% 以上): "
                   f"{cover} 年以降(--oa-cover-from で上書き可)/ 割合: " + ", ".join(f"{r.year}:{r.share_tol:.2f}" for r in t.itertuples()))
    return cover


def oa_dv_series(d, a, dv, log=None):
    """OpenAlex の年次被引用数から従属変数(窓の合計)を作る。戻り値: (tc の Series(使えない行は NaN), 窓の終わりの日付の Series または None)。
    使える行: OpenAlex で見つかった(oa_found=1)・窓の全部の年が取得範囲内(cover 以降)・窓が --oa-last-year 以内(今年は途中なので使わない)。
    値のない年は 0(OpenAlex は 0 の年を省く)"""
    mode, k = _oa_dv(dv)
    L = int(a.oa_last_year)
    n = len(d)
    found = (d["oa_found"] == "1").to_numpy() if "oa_found" in d else np.zeros(n, bool)
    yr = d["year"].to_numpy(float)
    if mode == "t":
        tc = num(d["oa_cited_total"]).where(pd.Series(found, index=d.index))
        if log is not None:
            log.append(f"--dv oa_total: OpenAlex の cited_by_count(全期間の累積)。使える行 {int(tc.notna().sum()):,}")
        return tc, None
    ycols = _oa_year_cols(d)
    if not ycols:
        sys.exit("oa_cy_<年> の列が CSV にありません。--fetch-counts → --merge-counts を実行し、--csv に結合後の CSV(--oa-counts-out)を指定してください")
    cover = _oa_cover_year(d, ycols, a, log)
    M = np.column_stack([num(d[c]).fillna(0).to_numpy(float) for _, c in ycols])
    col = {t: i for i, (t, _) in enumerate(ycols)}

    def cy(tt):
        out = np.zeros(n)
        for t, i in col.items():
            m = tt == t
            out[m] = M[m, i]
        return out
    endy = None
    if mode == "c":
        W = sum(cy(yr + j) for j in range(k))
        valid = found & (yr >= cover) & (yr + k - 1 <= L)
        endy = yr + k - 1
        desc = f"出版年を含む {k} 年(出版年〜出版年+{k - 1})の累積"
    elif mode == "a":
        W = cy(yr + k)
        valid = found & (yr + k >= cover) & (yr + k <= L)
        endy = yr + k if k == 0 else None
        desc = f"出版年の {k} 年後の 1 年分(0=出版年)"
    else:
        W = sum(cy(np.full(n, float(t))) for t in range(L - k + 1, L + 1))
        valid = found & (L - k + 1 >= cover) & (yr <= L)
        desc = f"{L - k + 1}〜{L} 年の {k} 年分(出版年は問わない。出版年の固定効果で古さを調整)"
    valid = valid & ~np.isnan(yr)
    tc = pd.Series(np.where(valid, W, np.nan), index=d.index)
    end = None
    if endy is not None:
        ey = np.where(valid & ~np.isnan(endy), endy, 2000).astype(int)
        end = pd.to_datetime(pd.DataFrame({"year": ey, "month": 12, "day": 31}), errors="coerce")
        end = pd.Series(end.to_numpy(), index=d.index).where(pd.Series(valid, index=d.index))
    if log is not None:
        v = tc.dropna()
        log.append(f"--dv {dv}: {desc}。取得範囲 {cover} 年以降・{L} 年まで。使える行 {len(v):,}(OpenAlex で見つからない行 {int((~found).sum()):,})/ "
                   f"平均 {v.mean():.2f} / 0 の割合 {(v == 0).mean():.1%} / 出版年別の件数 "
                   + str(d.loc[tc.notna(), "year"].astype(int).value_counts().sort_index().to_dict()))
    return tc, end


def _nb_note(dv):
    if _is_rv(dv):
        return "注意: 査読期間(日数)の NB の率比は、基準に対する期待日数の比(1 より小さいと査読期間が短い)。"
    o = _oa_dv(dv)
    if o:
        return ("注意: OpenAlex の年次被引用数(counts_by_year)の合計。窓の定義は --dv の名前(oa_c<k>=出版年を含む k 年 / oa_a<j>=出版 j 年後の 1 年 / oa_l<k>=直近 k 暦年)。"
                "窓がそろっているため古い論文の有利さは小さいが、出版月の違い(12 月出版は出版年の露出が短い)は残る(--exposure offset で窓の終わりまでの経過年数をオフセットにできる)。")
    return "注意: WoS の被引用数は「調査時点までの累積」で、論文の 3 年窓とは定義が違う。出版年の固定効果で古い論文の有利さを調整するが、年ごとの傾きの違いは残る。"


# ---- 取得・結合
def _oa_rec_counts(doi, w):
    if not w:
        return {"doi": doi, "oa_found": "0"}
    cby = {}
    for x in (w.get("counts_by_year") or []):
        if x.get("year") is not None:
            cby[str(int(x["year"]))] = int(x.get("cited_by_count") or 0)
    return {"doi": doi, "oa_found": "1", "oa_pubyear": w.get("publication_year"), "oa_pubdate": w.get("publication_date") or "",
            "oa_cited_total": w.get("cited_by_count"), "oa_cby": cby}


def oa_fetch_counts(a):
    """--csv の DOI の counts_by_year などを OpenAlex から取り、--oa-counts-cache(jsonl)に追記する。取得済みは飛ばす(再開できる)"""
    csvp = os.path.expanduser(a.csv)
    cachep = os.path.expanduser(a.oa_counts_cache)
    api_key = a.oa_api_key or os.environ.get("OPENALEX_API_KEY", "").strip()
    if not api_key:
        sys.exit("OpenAlex の API キーがありません。--oa-api-key か環境変数 OPENALEX_API_KEY で渡してください")
    api_key = "".join(api_key.split())
    batch_n = max(1, min(int(a.oa_batch), 100))
    dois = pd.read_csv(csvp, usecols=["DOI"], dtype=str, keep_default_na=False)["DOI"].map(_oa_norm)
    dois = [x for x in dict.fromkeys(dois) if x]
    if a.oa_limit:
        dois = dois[:a.oa_limit]
    done = set()
    if os.path.exists(cachep):
        done = {json.loads(l)["doi"] for l in open(cachep, encoding="utf-8") if l.strip()}
    todo = [x for x in dois if x not in done]
    skip = [x for x in todo if "," in x]
    todo = [x for x in todo if "," not in x]
    print(f"DOI {len(dois):,} / 取得済み {len(done):,} / 今回 {len(todo):,} / カンマを含み除外 {len(skip)} / 1 回 {batch_n} 件(--oa-batch 100 で回数が半分)", flush=True)
    rl = _oa_rate_limit(api_key)
    if rl:
        need = -(-len(todo) // batch_n)
        print(f"今日の残り {rl.get('credits_remaining', '?')} クレジット / 必要 約 {need:,} クレジット / リセット {_oa_reset_text(rl.get('resets_at', ''))}", flush=True)
    os.makedirs(os.path.dirname(cachep) or ".", exist_ok=True)
    t0, complete = time.time(), True
    with open(cachep, "a", encoding="utf-8") as f:
        for i in range(0, len(todo), batch_n):
            batch = todo[i:i + batch_n]
            try:
                res = _oa_fetch(batch, a.oa_mailto, api_key, select=OA_CNT_SELECT)
            except OABudgetExhausted as e:
                print(f"\n今日の予算を使い切りました。取得済みは保存されています。{_oa_reset_text(str(e))} 以降に、同じコマンドで続きを取得してください。")
                complete = False
                break
            if res is None:
                print("\n再試行を使い切りました。しばらくしてから同じコマンドで再開してください。")
                complete = False
                break
            got = {_oa_norm(w["doi"]): w for w in res if w.get("doi")}
            for d_ in batch:
                f.write(json.dumps(_oa_rec_counts(d_, got.get(d_)), ensure_ascii=False) + "\n")
            f.flush()
            n = i + len(batch)
            if (i // batch_n) % 20 == 0:
                left = (len(todo) - n) * (time.time() - t0) / n
                print(f"{n:,}/{len(todo):,}  残り約 {left / 60:.0f} 分", flush=True)
            time.sleep(a.oa_sleep)
    n_cached = sum(1 for l in open(cachep, encoding="utf-8") if l.strip())
    mp = os.path.join(os.path.dirname(cachep), "openalex_counts_meta.json")
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    meta = {}
    if os.path.exists(mp):
        try:
            meta = json.load(open(mp, encoding="utf-8"))
        except Exception:
            meta = {}
    meta.setdefault("first_run_utc", now)
    meta.update(dict(last_run_utc=now, script_version=VERSION, endpoint=OA_ENDPOINT, select=OA_CNT_SELECT, batch_size=batch_n,
                     n_dois=len(dois), n_cached=n_cached))
    with open(mp, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=2)
    print(("取得完了。次に --merge-counts を実行してください。" if complete else "途中まで。") + f" 取得条件と日時: {mp}")
    return complete


def oa_merge_counts(a):
    """取得済みの年次被引用数を --csv に結合して --oa-counts-out に書き出す(列: oa_found・oa_pubyear・oa_pubdate・oa_cited_total・oa_cy_<年>)。
    年の列は、値がない(OpenAlex が省いた)セルを空にする。0 として扱うかどうかは分析側が取得範囲を見て決める"""
    csvp, cachep, outp = os.path.expanduser(a.csv), os.path.expanduser(a.oa_counts_cache), os.path.expanduser(a.oa_counts_out)
    rows = [json.loads(l) for l in open(cachep, encoding="utf-8") if l.strip()]
    t = pd.DataFrame(rows).drop_duplicates("doi", keep="last")
    yrs = sorted({int(y) for c in t.get("oa_cby", pd.Series(dtype=object)) if isinstance(c, dict) for y in c})
    if yrs:
        yrs = list(range(yrs[0], yrs[-1] + 1))
    for y in yrs:
        t[f"oa_cy_{y}"] = [(str(c[str(y)]) if isinstance(c, dict) and str(y) in c else "") for c in t["oa_cby"]]
    t = t.drop(columns=["oa_cby"], errors="ignore")
    for c in OA_CNT_COLS:
        if c not in t:
            t[c] = ""
    d = pd.read_csv(csvp, dtype=str, keep_default_na=False, low_memory=False)
    d = d.drop(columns=[c for c in d.columns if c in OA_CNT_COLS or re.fullmatch(r"oa_cy_\d{4}", c)])
    d["_doi"] = d["DOI"].map(_oa_norm)
    d = d.merge(t.rename(columns={"doi": "_doi"}), on="_doi", how="left").drop(columns="_doi")
    keep = OA_CNT_COLS + [f"oa_cy_{y}" for y in yrs]
    for c in keep:
        d[c] = d[c].fillna("").astype(str).str.replace(r"\.0$", "", regex=True)
    os.makedirs(os.path.dirname(outp) or ".", exist_ok=True)
    d.to_csv(outp, index=False, encoding="utf-8")
    print("書き出し:", outp, "行数", len(d))
    print("OpenAlex で見つかった割合:", f"{(d.oa_found == '1').mean():.1%}")
    if "pub_year" in d:
        m = (d.oa_found == "1") & (d.oa_pubyear != "")
        print("出版年が PMC の pub_year と一致する割合(見つかった行):", f"{(d.loc[m, 'oa_pubyear'] == d.loc[m, 'pub_year']).mean():.1%}")
    d["year"] = num(d["pub_year"]) if "pub_year" in d else np.nan
    yc = [(y, f"oa_cy_{y}") for y in yrs]
    tab = _oa_coverage_table(d, yc)
    print("[取得できる年の範囲の確認] 出版年ごとに、Y 年以降の年次の合計が全期間の累積と一致する論文の割合(全期間 20 以上の論文)。share_tol が 0.9 を超える最初の出版年から窓に使える")
    print(tab.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    tab.to_csv(os.path.join(os.path.dirname(outp), "openalex_counts_coverage.csv"), index=False, encoding="utf-8-sig")
    return outp


# ---- 分析の窓ごとの比較(--oa-suite)
def _oa_ame(ctx, full, cov, h=1e-6):
    """DAS の平均限界効果(標準化): 全論文を類型 c にしたときと基準にしたときの、期待被引用数の平均の差。
    率比が同じでも、被引用数が多い窓・論文集合ほど絶対数の差は大きくなる(寄与の大きさを件数で見る)。標準誤差は delta 法(クラスタ頑健分散)"""
    X, names, beta = ctx["X"], ctx["names"], np.asarray(full["beta"], float)
    off = ctx.get("offset")
    didx = [names.index(c) for c in ctx["das_cols"]]
    p = len(beta)
    D = X[:, didx]
    eta0 = X @ beta + (off if off is not None else 0.0)

    def f(eta, bd):
        base = np.exp(eta - D @ bd)               # 全員を基準にしたときの期待値
        return np.array([np.mean(base * (np.exp(bd[j]) - 1.0)) for j in range(len(didx))]), float(np.mean(base))
    bd0 = beta[didx]
    est, base_mean = f(eta0, bd0)
    Gm = np.empty((len(didx), p))
    pos = {k: j for j, k in enumerate(didx)}
    for k in range(p):
        bd = bd0.copy()
        if k in pos:
            bd[pos[k]] += h
        e1, _ = f(eta0 + h * X[:, k], bd)
        Gm[:, k] = (e1 - est) / h
    V = np.asarray(cov["cluster"], float)[:p, :p]
    se = np.sqrt(np.clip(np.einsum("ij,jk,ik->i", Gm, V, Gm), 0, None))
    return pd.DataFrame({"variable": ctx["das_cols"], "ame": est, "ame_per_1000": 1000 * est, "se": se,
                         "low": est - 1.96 * se, "high": est + 1.96 * se, "mean_if_all_ref": base_mean})


def _oa_fit_one(d, meta, das_cols, base_ivs, a, label, outdir, sample, P):
    """d["tc"] を従属変数にして主モデルを推定し、率比・LRT(グループ)・平均限界効果を保存する"""
    lg = []
    ctx = nb_build(d, meta, das_cols, base_ivs, a, lg)
    P("  " + lg[-1])
    if len(ctx["y"]) < 1000:
        P("  行数が少なすぎるので中止")
        return None
    t0 = time.time()
    full = _fit_main(ctx)
    cov = nb_cov(full, ctx["X"], ctx["y"], codes=ctx["gcodes"])
    names, meta_ = ctx["names"], ctx["meta"]
    idx_all = [i for i, nm in enumerate(names) if nm in meta_]
    irr = _irr_table(full, cov, names, idx_all, meta_)
    dm = irr.group == G_DAS
    irr["p_holm_cluster"] = np.nan
    irr.loc[dm, "p_holm_cluster"] = holm(irr.loc[dm, "p_cluster"].values)
    irr["p_holm_all_cluster"] = holm(irr.p_cluster.values)
    for k_, v_ in dict(dv=label, sample=sample, n=int(len(ctx["y"])), n_clusters=int(ctx["gcodes"].max()) + 1, mean_y=float(ctx["y"].mean()),
                       zero_share=float((ctx["y"] == 0).mean()), alpha=float(full["alpha"]), converged=bool(full["converged"])).items():
        irr[k_] = v_
    tagx = f"{label}_{sample}"
    irr.to_csv(os.path.join(outdir, f"oa_suite_irr_{tagx}.csv"), index=False, encoding="utf-8-sig")
    try:
        am = _oa_ame(ctx, full, cov)
        am["dv"], am["sample"], am["n"] = label, sample, int(len(ctx["y"]))
        am.to_csv(os.path.join(outdir, f"oa_suite_ame_{tagx}.csv"), index=False, encoding="utf-8-sig")
    except Exception as e:
        P(f"  [平均限界効果を作れませんでした] {type(e).__name__}: {e}")
    if a.oa_lrt == "on":
        lt = nb_lrt(ctx, full, a, P)
        lt["dv"], lt["sample"] = label, sample
        lt.to_csv(os.path.join(outdir, f"oa_suite_lrt_{tagx}.csv"), index=False, encoding="utf-8-sig")
    P(f"  推定 {time.time() - t0:.0f} 秒 / N={len(ctx['y']):,} / 平均 {ctx['y'].mean():.2f} / 収束 {full['converged']}")
    return irr


def _oa_collect(outdir, labels, samples, P):
    """保存済みの CSV から、窓ごとの比較表を作る"""
    import glob
    out = {}
    for kind in ("irr", "ame", "lrt"):
        fr = []
        for s in samples:
            for lb in labels:
                f = os.path.join(outdir, f"oa_suite_{kind}_{lb}_{s}.csv")
                if os.path.exists(f):
                    fr.append(pd.read_csv(f))
        if fr:
            out[kind] = pd.concat(fr, ignore_index=True)
            out[kind].to_csv(os.path.join(outdir, f"oa_suite_{kind}_all.csv"), index=False, encoding="utf-8-sig")
    if "irr" not in out:
        return out
    irr = out["irr"]
    for s in samples:
        t = irr[(irr["sample"] == s) & (irr.group == G_DAS)]
        if t.empty:
            continue
        P(f"\n[DAS の率比(基準に対する NB の IRR)。括弧内は Holm 補正後の p(DAS の比較の族)。標本: {s}]")
        ns = t.drop_duplicates("dv").set_index("dv").n
        P("N: " + ", ".join(f"{lb}={int(ns[lb]):,}" for lb in labels if lb in ns.index))
        piv = t.assign(cell=[f"{r.irr:.3f} ({r.p_holm_cluster:.2g})" for r in t.itertuples()]).pivot(index="variable", columns="dv", values="cell")
        P(piv[[lb for lb in labels if lb in piv.columns]].to_string())
        # 向きと有意性の一致(Holm 後 p < 0.05)
        rows = []
        for v, g in t.groupby("variable"):
            g = g.set_index("dv")
            rows.append(dict(variable=v, n_dv=len(g), same_direction_all=bool(((g.irr > 1).all()) or ((g.irr < 1).all())),
                             n_sig_holm=int((g.p_holm_cluster < 0.05).sum()), irr_min=float(g.irr.min()), irr_max=float(g.irr.max())))
        P("向きがすべての従属変数で同じか・Holm 後 p<0.05 の従属変数の数・率比の範囲:")
        P(pd.DataFrame(rows).to_string(index=False, float_format=lambda x: f"{x:.3f}"))
        c = irr[(irr["sample"] == s) & (irr.group != G_DAS) & (irr.group != "固定効果")]
        if not c.empty:
            cp = c.assign(cell=[f"{r.irr:.3f}{'*' if r.p_holm_all_cluster < 0.05 else ''}" for r in c.itertuples()]).pivot(index="variable", columns="dv", values="cell")
            cp = cp[[lb for lb in labels if lb in cp.columns]]
            cp.to_csv(os.path.join(outdir, f"oa_suite_cov_irr_{s}.csv"), encoding="utf-8-sig")
            P(f"\n[共変量の率比(1SD または 0→1)。* は全係数にかけた Holm 後 p<0.05。標本: {s}。全表は oa_suite_cov_irr_{s}.csv]")
            P(cp.to_string())
    if "ame" in out:
        am = out["ame"]
        for s in samples:
            t = am[am["sample"] == s]
            if t.empty:
                continue
            P(f"\n[DAS の平均限界効果: 全論文をその類型にしたときの、基準類型との期待被引用数の差(1,000 本あたり。95% 区間)。標本: {s}]")
            piv = t.assign(cell=[f"{r.ame_per_1000:+.0f} ({1000 * r.low:+.0f}〜{1000 * r.high:+.0f})" for r in t.itertuples()]).pivot(index="variable", columns="dv", values="cell")
            P(piv[[lb for lb in labels if lb in piv.columns]].to_string())
    if "lrt" in out:
        lt = out["lrt"]
        for s in samples:
            t = lt[(lt["sample"] == s)]
            if t.empty:
                continue
            nonfe = t[~t.block.isin(["雑誌", "出版年", "雑誌×年"])].copy()
            nonfe["share"] = nonfe.LR_chi2 / nonfe.groupby("dv").LR_chi2.transform("sum")
            piv = nonfe.pivot(index="block", columns="dv", values="share")
            piv = piv[[lb for lb in labels if lb in piv.columns]]
            P(f"\n[グループを 1 つ外したときの LR の相対的な大きさ(固定効果を除く合計を 1 とした割合)。標本: {s}。Shapley ではなく LRT の簡易な寄与]")
            P(piv.to_string(float_format=lambda x: f"{x:.3f}"))
            piv.to_csv(os.path.join(outdir, f"oa_suite_lrt_share_{s}.csv"), encoding="utf-8-sig")
    return out


def _oa_plot(outdir, irr, labels, samples):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as e:
        print(f"[図] matplotlib を使えないので図は作りません: {e}", file=sys.stderr)
        return
    for s in samples:
        t = irr[(irr["sample"] == s) & (irr.group == G_DAS)]
        if t.empty:
            continue
        labs = [lb for lb in labels if lb in set(t.dv)]
        fig, ax = plt.subplots(figsize=(7.5, 4.5))
        cats = list(dict.fromkeys(t.variable))
        for j, c in enumerate(cats):
            g = t[t.variable == c].set_index("dv").reindex(labs)
            x = np.arange(len(labs)) + (j - (len(cats) - 1) / 2) * 0.09
            ax.errorbar(x, g.irr, yerr=[g.irr - g.irr_low, g.irr_high - g.irr], fmt="o-", ms=3, lw=1, capsize=2, label=c.replace("das_", ""))
        ax.axhline(1, color="gray", lw=0.8)
        ax.set_yscale("log")
        ax.set_xticks(np.arange(len(labs)))
        ax.set_xticklabels(labs, rotation=30, ha="right", fontsize=8)
        ax.set_ylabel("IRR vs reference (log scale)")
        ax.set_title(f"DAS category IRR by outcome window (sample: {s})", fontsize=9)
        ax.legend(fontsize=7, ncol=3, frameon=False)
        fig.tight_layout()
        fig.savefig(os.path.join(outdir, f"oa_suite_das_irr_{s}.png"), dpi=200)
        plt.close(fig)


def oa_suite(a):
    """窓の違う従属変数(OpenAlex の出版年を含む k 年・出版後 j 年目の 1 年、および WoS・PMC)を同じ説明変数・同じ固定効果で推定し、DAS の率比と寄与を並べる。
    標本: own=各従属変数で使える行すべて / common=すべての OpenAlex 窓で使える行(窓による違いが標本の違いでないことを確かめる)"""
    import copy
    a = copy.copy(a)
    a.nb_sample, a.target, a.nb_lrt, a.oa_suite = 0, "citations", "group", True
    if a.exposure not in ("off", "offset"):
        sys.exit("--oa-suite の --exposure は off か offset だけです(窓ごとに経過年数の作り方が違うため)")
    outdir = os.path.expanduser(a.outdir)
    _archive_existing(a, outdir)   # v044
    os.makedirs(outdir, exist_ok=True)
    _write_runinfo(a, outdir)   # v044
    wins = [int(x) for x in a.oa_windows.split(",") if x.strip()]
    lags = [int(x) for x in a.oa_lags.split(",") if x.strip()]
    extra = [x.strip() for x in a.oa_suite_extra.split(",") if x.strip()]
    labels = [f"oa_c{k}" for k in wins] + [f"oa_a{j}" for j in lags] + extra
    bad = [x for x in extra if x not in ("wos_TC", "pmc_citedby_n", "oa_total")]
    if bad or not labels:
        sys.exit(f"--oa-suite-extra は wos_TC, pmc_citedby_n, oa_total のカンマ区切りです(不正: {bad})")
    samples = {"own": ["own"], "common": ["common"], "both": ["own", "common"]}[a.oa_sample]
    a.dv = labels[0] if _oa_dv(labels[0]) else "oa_c2"
    a.flow, a.model_info = {}, {}
    d, meta, das_cols, ref, log = prepare(a)
    excl = {c.strip() for c in a.exclude.split(",") if c.strip()}
    base_ivs = [c for c in meta if c not in excl and c != "log_review" and c not in das_cols]
    lines = [f"OpenAlex 年次被引用数の窓ごとの比較 ({VERSION})", *log, f"DAS の基準: {ref} / 類型: {[ref] + [c[4:] for c in das_cols]}",
             f"従属変数: {labels} / 標本: {samples} / 固定効果 {a.nb_fe} / 分野の統制 {a.oa_field} / 経過時間 {a.exposure}"]
    P = lines.append
    # 各従属変数の系列と、common 標本(OpenAlex の窓すべてで使える行)
    series, ends = {}, {}
    for lb in labels:
        if _oa_dv(lb):
            series[lb], ends[lb] = oa_dv_series(d, a, lb, lines)
        elif lb == "wos_TC":
            s_ = num(d["wos_TC"])
            series[lb] = s_.where(d.wos_matched.str.lower() == "true") if "wos_matched" in d else s_
            ends[lb] = None
        else:
            s_ = num(d["pmc_citedby_n"])
            series[lb] = s_.where(d.cb_fetched == "1") if "cb_fetched" in d else s_
            ends[lb] = None
    oa_labels = [lb for lb in labels if _oa_dv(lb) and _oa_dv(lb)[0] in ("c", "a")]
    common = pd.Series(True, index=d.index)
    for lb in oa_labels:
        common &= series[lb].notna()
    common_extra = [lb for lb in labels if not (_oa_dv(lb) and _oa_dv(lb)[0] in ("c", "a"))]
    P(f"common 標本: OpenAlex の窓({oa_labels})がすべて使える行 {int(common.sum()):,}(出版年別 "
      + str(d.loc[common, "year"].astype(int).value_counts().sort_index().to_dict()) + ")")
    print("\n".join(lines), file=sys.stderr, flush=True)
    for s in samples:
        for lb in labels:
            f_ = os.path.join(outdir, f"oa_suite_irr_{lb}_{s}.csv")
            if a.oa_skip_existing and os.path.exists(f_):
                P(f"[{s}/{lb}] 出力があるので飛ばす(--oa-skip-existing)")
                continue
            tc = series[lb].copy()
            if s == "common":
                tc = tc.where(common)
            d["tc"] = tc
            a_dv = copy.copy(a)
            a_dv.dv = lb
            for c_ in ("age_years", "log_age", "oa_win_end"):
                if c_ in d:
                    d.drop(columns=[c_], inplace=True)
            if a.exposure == "offset":
                if ends.get(lb) is None:
                    P(f"  [{s}/{lb}] この従属変数には窓の終わりが定義できない(1 年後以降・WoS・PMC・total)ので、オフセットなしで推定")
                    a_dv.exposure = "off"
                else:
                    d["oa_win_end"] = ends[lb]
                    attach_exposure(a_dv, d, meta)
            P(f"\n[{s}/{lb}] 推定")
            print(f"[進捗] {s}/{lb}", file=sys.stderr, flush=True)
            try:
                _oa_fit_one(d, meta, das_cols, base_ivs, a_dv, lb, outdir, s, P)
            except Exception as e:
                import traceback
                P(f"  [失敗] {type(e).__name__}: {e}")
                traceback.print_exc()
            with open(os.path.join(outdir, "oa_suite_log.txt"), "w", encoding="utf-8") as fh:
                fh.write("\n".join(lines))
    col = _oa_collect(outdir, labels, samples, P)
    if "irr" in col:
        _oa_plot(outdir, col["irr"], labels, samples)
    P("\n読み方: 窓が長いほど累積が増えるが、DAS の率比が窓で大きく変わらなければ、関連は短い期間の引用の勢いと長期の蓄積に共通する。"
      "窓が重なる従属変数(c2⊂c3⊂…)と、同じ論文の別の年(a0, a1, …)の推定は互いに独立ではないので、率比の差を検定しない(区間の重なりと向きで見る)。"
      "own は窓ごとに論文集合が変わる(長い窓ほど古い論文だけ)ので、common で窓以外を固定した結果と並べて読む。観察データの関連であり、因果ではない。")
    txt = "\n".join(lines)
    print(txt)
    with open(os.path.join(outdir, "oa_suite_summary.txt"), "w", encoding="utf-8") as fh:
        fh.write(txt)
    print("保存先:", outdir)



# ---------------------------------------------------------------------------------------------
# v043: --oa-report  既存の CSV から fig9(窓ごとの率比、own と common を並べた図)と LaTeX の表を作る(再推定はしない)
#   入力  <oa-report-dir>/oa_suite_irr_*.csv(--oa-suite の出力)/ <oa-journal-dir>/nb_by_journal.csv(--dv oa_c3 の出力)/ <oa-wos-dir>/nb_by_journal.csv(WoS)
#   出力  <oa-report-out>/fig9_oa_windows_own_common.png・.pdf / tab_oawin.tex(tab:oawin の tabular)/ tab_oajournal.tex(R と M)/ tab_oajournal_all.tex(54 セル)
# ---------------------------------------------------------------------------------------------
OA_WIN_ORDER = [("oa_c2", "2"), ("oa_c3", "3"), ("oa_c4", "4"), ("oa_c5", "5"), ("oa_a0", "0"), ("oa_a1", "1"), ("oa_a2", "2"), ("oa_a3", "3")]
OA_DAS_ORDER = ["P", "A", "N", "C", "R", "M"]
OA_DAS_COLOR = {"P": "#009E73", "A": "#D55E00", "N": "#8C8C8C", "C": "#CC79A7", "R": "#E69F00", "M": "#56B4E9", "F": "#0072B2"}
OA_JOURNAL_TEX = {"HELIYON": "Heliyon", "INT. J. ENVIRON. RES. PUBLIC HEALTH": "IJERPH", "INT. J. MOL. SCI.": "IJMS",
                  "JOURNAL OF CLINICAL MEDICINE": "JCM", "MATERIALS": "Materials", "MOLECULES": "Molecules",
                  "NATURE COMMUNICATIONS": "Nature Communications", "PLOS ONE": "PLOS ONE", "SCIENTIFIC REPORTS": "Scientific Reports", "SENSORS": "Sensors"}


def _fmt_p(p, tex=True):
    if p is None or (isinstance(p, float) and np.isnan(p)):
        return "--"
    if p < 0.001:
        return "$<$0.001" if tex else "<0.001"
    if p >= 0.995:
        return "1"
    return f"{p:.2f}" if p >= 0.1 else f"{p:.3f}"


def _oa_read_irr(d):
    f = os.path.join(d, "oa_suite_irr_all.csv")
    if os.path.exists(f):
        t = pd.read_csv(f)
    else:
        fs = sorted(x for x in glob.glob(os.path.join(d, "oa_suite_irr_*.csv")) if not x.endswith("_all.csv"))
        if not fs:
            sys.exit(f"[oa-report] {d} に oa_suite_irr_*.csv がありません(先に --oa-suite を実行してください)")
        t = pd.concat([pd.read_csv(x) for x in fs], ignore_index=True)
    t = t[t.variable.astype(str).str.startswith("das_")].copy()
    t["das"] = t.variable.str[4:]
    return t


def _oa_fig9(t, outdir, P):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker
    samples = [s for s in ("own", "common") if s in set(t["sample"])]
    wl = [w for w, _ in OA_WIN_ORDER if w in set(t.dv)]
    if not samples or not wl:
        P("[oa-report] 図にできる窓がありません")
        return
    fig, axes = plt.subplots(1, len(samples), figsize=(5.2 * len(samples), 4.6), sharey=True, squeeze=False)
    nc = len(OA_DAS_ORDER)
    for ax, s in zip(axes[0], samples):
        for j, c in enumerate(OA_DAS_ORDER):
            g = t[(t["sample"] == s) & (t.das == c)].set_index("dv").reindex(wl)
            x = np.arange(len(wl)) + (j - (nc - 1) / 2) * 0.11
            ok = g.irr.notna().values
            col = OA_DAS_COLOR[c]
            ax.errorbar(x[ok], g.irr.values[ok], yerr=[(g.irr - g.irr_low).values[ok], (g.irr_high - g.irr).values[ok]], fmt="none", ecolor=col, elinewidth=1, capsize=1.5, zorder=2)
            sig = (g.p_holm_cluster.values < 0.05) & ok
            ax.plot(x[ok & sig], g.irr.values[ok & sig], "o", color=col, ms=3.8, zorder=3, label=f"{c}")
            ax.plot(x[ok & ~sig], g.irr.values[ok & ~sig], "o", mfc="white", mec=col, ms=3.8, zorder=3)
        ax.axhline(1, color="gray", lw=0.8, ls="--", zorder=1)
        ax.axvline(3.5, color="lightgray", lw=0.8, zorder=0) if len(wl) == 8 else None
        ax.set_yscale("log")
        ax.set_xticks(np.arange(len(wl)))
        ax.set_xticklabels([dict(OA_WIN_ORDER)[w] for w in wl], fontsize=9)
        ax.set_xlabel("Window (years; left: cumulative from publication year, right: single year after it)", fontsize=8)
        ax.set_title({"own": "Own sample (articles available for each window)", "common": "Common sample (same articles in every window)"}[s], fontsize=9)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    axes[0][0].set_ylabel("Rate ratio vs DAS F (log scale)")
    yt = [0.9, 1.0, 1.1, 1.2, 1.3]
    axes[0][0].set_yticks(yt)
    axes[0][0].set_yticklabels([f"{v:g}" for v in yt])
    axes[0][0].yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    h, l = axes[0][-1].get_legend_handles_labels()
    fig.legend(h, [f"DAS {x}" for x in l], loc="lower center", bbox_to_anchor=(0.5, 0.03), ncol=len(l), fontsize=8, frameon=False)
    fig.text(0.5, -0.045, "Filled: Holm-adjusted p < 0.05 within window; open: not significant. Bars: 95% CI (cluster-robust). Windows overlap and are not independent.", ha="center", fontsize=7)
    fig.tight_layout(rect=(0, 0.09, 1, 1))
    for ext, kw in (("png", {"dpi": 300}), ("pdf", {})):
        fig.savefig(os.path.join(outdir, f"fig9_oa_windows_own_common.{ext}"), bbox_inches="tight", **kw)
    plt.close(fig)
    P(f"[oa-report] 図: {os.path.join(outdir, 'fig9_oa_windows_own_common.png')}")


def _oa_tab_win(t, outdir, P):
    wl = [w for w, _ in OA_WIN_ORDER if w in set(t.dv)]
    L = ["% 自動生成(--oa-report)。tab:oawin の tabular の本体", "\\begin{tabular}{@{}lcccccccc@{}}", "\\toprule",
         "& \\multicolumn{4}{c}{Cumulative (years)} & \\multicolumn{4}{c}{Single year (after publication year)} \\\\",
         "\\cmidrule(lr){2-5}\\cmidrule(lr){6-9}", "Category & " + " & ".join(dict(OA_WIN_ORDER)[w] for w in wl) + " \\\\", "\\midrule"]
    for s, title in (("own", "Own sample"), ("common", "Common sample (256,798 articles in every window)")):
        g = t[t["sample"] == s]
        if g.empty:
            continue
        L.append(f"\\multicolumn{{9}}{{@{{}}l}}{{\\textit{{{title}}}}} \\\\")
        for c in OA_DAS_ORDER:
            cells = []
            for w in wl:
                r = g[(g.dv == w) & (g.das == c)]
                cells.append("--" if r.empty else f"{r.irr.iloc[0]:.3f} ({_fmt_p(r.p_holm_cluster.iloc[0])})")
            L.append(f"{c} & " + " & ".join(cells) + " \\\\")
        if s == "own":
            n = {w: g[g.dv == w].n.iloc[0] for w in wl if not g[g.dv == w].empty}
            L.append("Articles & " + " & ".join(f"{int(n[w]):,}" if w in n else "--" for w in wl).replace(",", "{,}") + " \\\\")
            L.append("\\midrule")
    L += ["\\botrule", "\\end{tabular}"]
    open(os.path.join(outdir, "tab_oawin.tex"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    P(f"[oa-report] 表: {os.path.join(outdir, 'tab_oawin.tex')}")


def _oa_read_byj(d):
    f = os.path.join(os.path.expanduser(d), "nb_by_journal.csv")
    if not os.path.exists(f):
        return None
    r = pd.read_csv(f)
    r["jname"] = jshort(r.journal).values
    return r


def _oa_tab_journal(a, outdir, P):
    oa = _oa_read_byj(a.oa_journal_dir)
    if oa is None:
        P(f"[oa-report] {a.oa_journal_dir}/nb_by_journal.csv がないので雑誌別の表は作りません(先に --dv {a.oa_journal_dv} を実行)")
        return
    wos = _oa_read_byj(a.oa_wos_dir)
    cnt = None
    fc = os.path.join(os.path.expanduser(a.oa_journal_dir), "desc_journal_das_counts.csv")
    if os.path.exists(fc):
        cnt = pd.read_csv(fc, index_col=0)
    jn = sorted(set(oa.jname) | (set(cnt.index) - {"合計"} if cnt is not None else set()), key=lambda x: OA_JOURNAL_TEX.get(x, x).lower())

    def cell(df, j, c):
        if df is None:
            return None
        r = df[(df.jname == j) & (df.das == c)]
        return None if r.empty else r.iloc[0]

    def nclass(j, c):
        r = cell(oa, j, c)
        if r is not None:
            return int(r.n_class)
        if cnt is not None and j in cnt.index and c in cnt.columns:
            return int(cnt.loc[j, c])
        return None

    def ci(r):
        return f"{r.irr:.2f} ({r.irr_low:.2f}--{r.irr_high:.2f})"

    def nfmt(n):
        return "--" if n is None else f"{n:,}".replace(",", "{,}")

    # 本文の表(R と M)
    H = "Journal & n & IRR (95\\% CI) & Holm $p$ & WoS & n & IRR (95\\% CI) & Holm $p$ & WoS \\\\"
    L = ["% 自動生成(--oa-report)。tab:oajournal の tabular の本体", "\\begin{tabular}{@{}l" + "rlll" * 2 + "@{}}", "\\toprule",
         "& \\multicolumn{4}{c}{R} & \\multicolumn{4}{c}{M} \\\\", "\\cmidrule(lr){2-5}\\cmidrule(lr){6-9}", H, "\\midrule"]
    for j in jn:
        parts = [OA_JOURNAL_TEX.get(j, j)]
        for c in ("R", "M"):
            r, w = cell(oa, j, c), cell(wos, j, c)
            parts += [nfmt(nclass(j, c)), ci(r) if r is not None else "n.e.", _fmt_p(r.p_holm_robust) if r is not None else "--", f"{w.irr:.2f}" if w is not None else "--"]
        L.append(" & ".join(parts) + " \\\\")
    L += ["\\botrule", "\\end{tabular}"]
    open(os.path.join(outdir, "tab_oajournal.tex"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    P(f"[oa-report] 表: {os.path.join(outdir, 'tab_oajournal.tex')}")

    # 補足の表(全 54 セル)。longtable
    A = ["% 自動生成(--oa-report)。補足表(全類型)。\\usepackage{longtable} が必要", "\\begin{longtable}{@{}llrllrll@{}}", "\\toprule",
         "Journal & DAS & n & IRR (95\\% CI) & Holm $p$ & \\multicolumn{3}{c}{WoS: IRR (Holm $p$)} \\\\", "\\midrule", "\\endhead", "\\botrule", "\\endfoot"]
    for j in jn:
        for c in OA_DAS_ORDER:
            r, w = cell(oa, j, c), cell(wos, j, c)
            A.append(" & ".join([OA_JOURNAL_TEX.get(j, j), c, nfmt(nclass(j, c)), ci(r) if r is not None else "n.e.",
                                 _fmt_p(r.p_holm_robust) if r is not None else "--",
                                 (f"{w.irr:.2f} ({_fmt_p(w.p_holm_robust)})" if w is not None else "--"), "", ""]) + " \\\\")
    A.append("\\end{longtable}")
    open(os.path.join(outdir, "tab_oajournal_all.tex"), "w", encoding="utf-8").write("\n".join(A) + "\n")
    sig = oa[oa.p_holm_robust < 0.05]
    P(f"[oa-report] 雑誌別({a.oa_journal_dv}): {len(oa)} 比較中 Holm 後に有意 {len(sig)}(WoS: " + (f"{int((wos.p_holm_robust < 0.05).sum())}" if wos is not None else "なし") + ")")
    both = oa.merge(wos, on=["jname", "das"], suffixes=("_oa", "_wos")) if wos is not None else None
    if both is not None and len(both):
        same = int((np.sign(np.log(both.irr_oa)) == np.sign(np.log(both.irr_wos))).sum())
        r_ = float(np.corrcoef(np.log(both.irr_oa), np.log(both.irr_wos))[0, 1])
        P(f"[oa-report] 雑誌別 IRR の WoS との比較: 同じ向き {same}/{len(both)}、対数 IRR の相関 {r_:.2f}(論文に書ける値)")


def oa_report(a):
    outdir = os.path.expanduser(a.oa_report_out)
    _archive_existing(a, outdir)   # v044: 図・表の tex を上書きする前に退避
    os.makedirs(outdir, exist_ok=True)
    lines = []
    P = lambda s: (print(s), lines.append(s))
    P(f"[oa-report] 版 {VERSION} / 入力: 窓={a.oa_report_dir} / 雑誌別={a.oa_journal_dir}(dv={a.oa_journal_dv}) / WoS={a.oa_wos_dir}")
    t = _oa_read_irr(os.path.expanduser(a.oa_report_dir))
    _oa_fig9(t, outdir, P)
    _oa_tab_win(t, outdir, P)
    _oa_tab_journal(a, outdir, P)
    open(os.path.join(outdir, "oa_report_log.txt"), "w", encoding="utf-8").write("\n".join(lines) + "\n")


# ----------------------------------------------------------------------------- v052: 分類性能の報告と DOI ごとのラベルの書き出し
def _wilson(k, n, z=1.959964):
    """二項割合の Wilson 95% 区間"""
    if n <= 0:
        return (np.nan, np.nan)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, c - h), min(1.0, c + h))


def _clf_counts(human, pred, cats):
    idx = {c: i for i, c in enumerate(cats)}
    cnt = np.zeros((len(cats), len(cats)))
    for h, p_ in zip(human, pred):
        if h in idx and p_ in idx:
            cnt[idx[h], idx[p_]] += 1
    return cnt


def _clf_table(cnt, cats):
    """混同行列 cnt[人手, 予測] から、類型ごとの適合率・再現率・F1 と、全体の正解率・κ・マクロ F1"""
    n = float(cnt.sum())
    rows = []
    for k, c in enumerate(cats):
        sup, npred, tp = float(cnt[k].sum()), float(cnt[:, k].sum()), float(cnt[k, k])
        rec = tp / sup if sup > 0 else np.nan
        prec = tp / npred if npred > 0 else np.nan
        f1 = (2 * prec * rec / (prec + rec)) if (np.isfinite(prec) and np.isfinite(rec) and prec + rec > 0) else np.nan
        rlo, rhi = _wilson(tp, sup)
        plo, phi = _wilson(tp, npred)
        rows.append(dict(code=c, name=DAS_NAMES_LEGEND.get(c, ""), n_human=int(sup), n_pred=int(npred), n_correct=int(tp),
                         precision=prec, precision_lo=plo, precision_hi=phi, recall=rec, recall_lo=rlo, recall_hi=rhi, f1=f1))
    t = pd.DataFrame(rows)
    acc = float(np.trace(cnt) / n) if n > 0 else np.nan
    pe = float((cnt.sum(axis=1) * cnt.sum(axis=0)).sum() / n ** 2) if n > 0 else np.nan
    kap = (acc - pe) / (1 - pe) if (n > 0 and pe < 1) else np.nan
    ok = t.n_human > 0
    mf1 = float(np.nanmean(t.loc[ok, "f1"])) if ok.any() and t.loc[ok, "f1"].notna().any() else np.nan
    return t, dict(n=int(n), accuracy=acc, kappa=kap, macro_f1=mf1)


def _ppv_corpus(cnt, p_pred):
    """check_misclass と同じ EM で真の割合 π を推定し、P(真 k | 予測 k)(PPV)を返す。混同行列は点推定(Dirichlet の引き直しなし)"""
    C = np.divide(cnt, cnt.sum(axis=1, keepdims=True), out=np.zeros_like(cnt), where=cnt.sum(axis=1, keepdims=True) > 0)
    pi = p_pred.copy()
    for _ in range(500):
        post = C * pi[:, None]
        cs = post.sum(axis=0, keepdims=True)
        post = np.divide(post, cs, out=np.zeros_like(post), where=cs > 0)
        pi_new = post @ p_pred
        if np.abs(pi_new - pi).max() < 1e-10:
            pi = pi_new
            break
        pi = pi_new
    Q = C * pi[:, None]
    cs = Q.sum(axis=0, keepdims=True)
    Q = np.divide(Q, cs, out=np.zeros_like(Q), where=cs > 0)
    return pi, np.diag(Q)


def _clf_corpus_shares(a, cats):
    """コーパス(DAS ラベルあり・--article-type・注記なし・--min-year 以上)の予測ラベルの割合と件数"""
    d, miss = read_cols(a.csv, ["das_label", "das_has_label", "article_type", "wos_notice_type", "pub_year"])
    if "das_label" not in d:
        sys.exit(f"--clf-corpus: --csv に das_label 列がありません(見つからない列: {miss})")
    d = d[(d.get("das_has_label", "1") == "1") & (d.das_label != "")]
    if "article_type" in d and a.article_type:
        d = d[d.article_type == a.article_type]
    if "wos_notice_type" in d and not a.keep_notice:
        d = d[d.wos_notice_type == ""]
    if "pub_year" in d:
        d = d[num(d.pub_year) >= a.min_year]
    vc = d.das_label.value_counts()
    cnts = np.array([float(vc.get(c, 0)) for c in cats])
    return cnts / cnts.sum(), int(cnts.sum()), int(len(d) - cnts.sum())


# ----------------------------------------------------------------------------- v056: P のうち、識別子のないリポジトリらしい文の量(語句検索)
PLATFORM_DATA = r"figshare|zenodo|dryad|\bosf\b|open science framework|mendeley data|dataverse|kaggle|hugging ?face|code ocean|openneuro|datadryad"
PLATFORM_CODE = r"github|gitlab|bitbucket|sourceforge"
ID_LIKE = (r"10\.\d{4,9}/\S+|doi\.org|\bdoi\s*:|\b(?:GSE|GSM|GSA|SRR|SRP|SRX|PRJNA|PRJEB|PRJDB|E-MTAB|E-GEOD|PXD|EGAS|EGAD|MSV|EMPIAR|EMD-)\d+"
           r"|zenodo\.org/records?/\d+|figshare\.com/\S*\d{5,}|osf\.io/[a-z0-9]{5}\b|\baccession (?:number|no\.?|code)s?\b")


def das_platform_report(a):
    """v056: DAS の本文(das_text)から、置き場の名前を含む文の割合を、識別子らしい文字列の有無で分けて数える。回帰は走らせない"""
    path = os.path.expanduser(a.csv)
    head = list(pd.read_csv(path, nrows=0).columns)
    idc = next((c for c in head if c.lower() == "pmcid"), None)
    cols = ["journal_key", "pub_year", "das_label", "das_has_label", "das_text", "article_type", "wos_notice_type"] + ([idc] if idc else [])
    d, miss = read_cols(path, cols)
    if "das_text" not in d or "das_label" not in d:
        sys.exit(f"--das-platform-report: --csv に das_text または das_label の列がありません(見つからない列: {miss})")
    out = os.path.expanduser(a.outdir)
    os.makedirs(out, exist_ok=True)
    lines = []
    P = lines.append
    P(f"識別子のないリポジトリらしい文の量(語句検索) ({VERSION}) {datetime.datetime.now():%Y-%m-%d %H:%M}\n入力 {path}")
    n0 = len(d)
    d = d[(d.get("das_has_label", "1") == "1") & (d.das_label != "")]
    n1 = len(d)
    if "article_type" in d and a.article_type:
        d = d[d.article_type == a.article_type]
    n2 = len(d)
    if "wos_notice_type" in d and not a.keep_notice:
        d = d[d.wos_notice_type == ""]
    n3 = len(d)
    d = d[num(d.pub_year) >= a.min_year].copy()
    P(f"行数 {n0:,} → DAS ラベルあり {n1:,} → article_type={a.article_type or '(絞らない)'} {n2:,} → 注記なし {n3:,} → {a.min_year} 年以降 {len(d):,}")
    empty = int((d.das_text.str.strip() == "").sum())
    P(f"das_text が空の行 {empty:,}({empty / max(len(d), 1):.2%})。空の行は「置き場の名前なし」として数える(割合は全行が分母)")
    extra = (a.platform_extra or "").strip()
    pat_data = PLATFORM_DATA + (("|" + extra) if extra else "")
    t = d.das_text.fillna("")
    d["data_pf"] = t.str.contains(pat_data, regex=True, case=False)
    d["code_pf"] = t.str.contains(PLATFORM_CODE, regex=True, case=False)
    d["id_like"] = t.str.contains(ID_LIKE, regex=True, case=False)
    d["any_pf"] = d.data_pf | d.code_pf
    d["data_noid"] = d.data_pf & ~d.id_like
    d["code_only_noid"] = d.code_pf & ~d.data_pf & ~d.id_like
    d["any_noid"] = d.any_pf & ~d.id_like
    d["group"] = d.journal_key.map(_jgroup)

    def summ(g):
        n = len(g)
        r = dict(n=n)
        for k in ("any_pf", "data_pf", "code_pf", "id_like", "data_noid", "code_only_noid", "any_noid"):
            r[k] = int(g[k].sum())
            r[k + "_pct"] = round(100 * g[k].mean(), 2) if n else np.nan
        return pd.Series(r)
    order = [c for c in ["F", "M", "P", "A", "N", "C", "R"] if c in set(d.das_label)] + sorted(set(d.das_label) - set("FMPANCR"))
    bycat = pd.DataFrame({c: summ(d[d.das_label == c]) for c in order}).T
    bycat.index.name = "das_label"
    bycat.to_csv(os.path.join(out, "das_platform_by_category.csv"), encoding="utf-8-sig")
    P("\n[類型ごと(件数と、%は各類型の文に対する割合)]")
    P(bycat[["n", "any_pf_pct", "data_pf_pct", "code_pf_pct", "id_like_pct", "data_noid_pct", "code_only_noid_pct", "any_noid_pct"]].to_string())
    p = d[d.das_label == "P"]
    if len(p):
        bg = pd.DataFrame({g: summ(p[p.group == g]) for g in ("big3", "heliyon", "mdpi6") if (p.group == g).any()}).T
        bg.index.name = "journal_group"
        bg.to_csv(os.path.join(out, "das_platform_P_by_journalgroup.csv"), encoding="utf-8-sig")
        P("\n[P の雑誌群別]")
        P(bg[["n", "data_noid", "data_noid_pct", "code_only_noid", "code_only_noid_pct", "any_noid_pct"]].to_string())
        by = pd.DataFrame({y: summ(p[p.pub_year == y]) for y in sorted(p.pub_year.unique())}).T
        by.index.name = "pub_year"
        by.to_csv(os.path.join(out, "das_platform_P_by_year.csv"), encoding="utf-8-sig")
        P("\n[P の出版年別(%)]")
        P(by[["n", "data_noid_pct", "code_only_noid_pct", "any_noid_pct"]].to_string())
        # 人手の確認用の標本
        rs = np.random.RandomState(a.seed)
        smp = []
        for lab, m in (("data_platform_no_id", p.data_noid), ("code_platform_only_no_id", p.code_only_noid)):
            q = p[m]
            if len(q):
                q = q.iloc[rs.permutation(len(q))[:a.platform_sample]]
                tt = q.das_text.fillna("")
                terms = [";".join(sorted(set(x.lower() for x in re.findall(pat_data + "|" + PLATFORM_CODE, s_, flags=re.I)))) for s_ in tt]
                smp.append(pd.DataFrame({"stratum": lab, "pmcid": q[idc].values if idc else "", "journal": q.journal_key.values, "year": q.pub_year.values,
                                         "terms": terms, "das_text": tt.str.slice(0, 700).values, "manual_repo_like": ""}))
        if smp:
            pd.concat(smp).to_csv(os.path.join(out, "das_platform_P_sample.csv"), index=False, encoding="utf-8-sig")
        nP = len(p)
        r = bycat.loc["P"]
        P(f"\n[本文に使える文(語句検索の上限側の概算)] P {nP:,} 件のうち、データ置き場の名前があり識別子らしい文字列がない文は {int(r.data_noid):,} 件({r.data_noid_pct:.1f}%)、"
          f"コード置き場の名前だけで識別子がない文は {int(r.code_only_noid):,} 件({r.code_only_noid_pct:.1f}%)、合わせて {int(r.any_noid):,} 件({r.any_noid_pct:.1f}%)。"
          f"全類型の件数に対する割合は {100 * r.any_noid / len(d):.2f}% 以下。")
        P(f"P で識別子らしい文字列がある文は {int(r.id_like):,} 件({r.id_like_pct:.1f}%)。F の {bycat.loc['F'].id_like_pct:.1f}% と比べる(定義上は P に識別子があれば F になるはず)。" if "F" in bycat.index else "")
        P(f"人手の確認: das_platform_P_sample.csv の manual_repo_like 列に、実際に『識別子はないが、リポジトリでデータが公開されている』なら 1、否定文・参考文献・コードだけなら 0 を入れる(層ごとに {a.platform_sample} 件まで)。"
          "層ごとの 1 の割合(適合率)を上の件数に掛けると、P のうち識別子のないリポジトリ共有の点推定が得られる。")
    txt = "\n".join(lines)
    with open(os.path.join(out, "das_platform_report.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    print(txt)
    print("保存先:", out)


def _tex_esc(x):
    return str(x).replace("&", r"\&").replace("%", r"\%").replace("_", r"\_").replace("#", r"\#")


def _f2(x):
    return "--" if not np.isfinite(x) else f"{x:.2f}"


def _tex_clf_table(tbl, summ, label, caption, with_ppv):
    cols = "llrrccc" + ("rc" if with_ppv else "")
    head = "Code & Category & $n$ (human) & $n$ (predicted) & Precision & Recall (95\\% CI) & F1"
    if with_ppv:
        head += " & $n$ (corpus, predicted) & PPV in corpus"
    out = ["\\begin{table}[htbp]", "\\centering", f"\\caption{{{caption}}}", f"\\label{{{label}}}", "\\small",
           f"\\begin{{tabular}}{{{cols}}}", "\\toprule", head + " \\\\", "\\midrule"]
    for _, r in tbl.iterrows():
        line = (f"{r.code} & {_tex_esc(r['name'])} & {int(r.n_human)} & {int(r.n_pred)} & {_f2(r.precision)} & "
                f"{_f2(r.recall)} ({_f2(r.recall_lo)}--{_f2(r.recall_hi)}) & {_f2(r.f1)}")
        if with_ppv:
            line += f" & {int(r.corpus_pred_n):,} & {r.ppv_corpus:.3f}".replace(",", "{,}")
        out.append(line + " \\\\")
    out += ["\\bottomrule", "\\end{tabular}", "\\par\\smallskip",
            f"\\footnotesize Accuracy {summ['accuracy']:.4f}, Cohen's $\\kappa$ {summ['kappa']:.3f}, macro-F1 {summ['macro_f1']:.3f} "
            f"($N={summ['n']}$ reference statements).", "\\end{table}"]
    return "\n".join(out) + "\n"


def _tex_confusion(cnt, cats, label, caption):
    out = ["\\begin{table}[htbp]", "\\centering", f"\\caption{{{caption}}}", f"\\label{{{label}}}", "\\small",
           "\\begin{tabular}{l|" + "r" * len(cats) + "|r}", "\\toprule",
           "Human \\textbackslash{} Predicted & " + " & ".join(cats) + " & Total \\\\", "\\midrule"]
    for k, c in enumerate(cats):
        cells = [(f"\\textbf{{{int(cnt[k, j])}}}" if j == k else str(int(cnt[k, j]))) for j in range(len(cats))]
        out.append(f"{c} & " + " & ".join(cells) + f" & {int(cnt[k].sum())} \\\\")
    out += ["\\midrule", "Total & " + " & ".join(str(int(cnt[:, j].sum())) for j in range(len(cats))) + f" & {int(cnt.sum())} \\\\",
            "\\bottomrule", "\\end{tabular}", "\\end{table}"]
    return "\n".join(out) + "\n"


def _tex_by_group(gdf, cats, groups, label, caption, min_n=5):
    out = ["\\begin{table}[htbp]", "\\centering", f"\\caption{{{caption}}}", f"\\label{{{label}}}", "\\small",
           "\\begin{tabular}{l" + "c" * len(groups) + "}", "\\toprule", "Category & " + " & ".join(_tex_esc(g) for g in groups) + " \\\\", "\\midrule"]
    for c in cats:
        cells = []
        for g in groups:
            r = gdf[(gdf.group == g) & (gdf.code == c)]
            if len(r) == 0 or int(r.n_human.iloc[0]) < min_n:
                cells.append("--")
            else:
                cells.append(f"{r.recall.iloc[0]:.2f} ({int(r.n_human.iloc[0])})")
        out.append(f"{c} & " + " & ".join(cells) + " \\\\")
    out += ["\\bottomrule", "\\end{tabular}", "\\par\\smallskip", f"\\footnotesize Cells: recall (number of human-labelled statements); -- : fewer than {min_n} human-labelled statements.", "\\end{table}"]
    return "\n".join(out) + "\n"


def classifier_report(a, outdir=None):
    """--classifier-report: 参照セットでのカテゴリ別の分類性能(混同行列・適合率・再現率・F1・雑誌群別)と LaTeX の表。回帰は走らせない"""
    if not a.reference_csv:
        sys.exit("--classifier-report には --reference-csv(1 行 1 文: 雑誌・人手のラベル・予測ラベル)が必要です。列名は --ref-cols 雑誌,人手,予測 で指定")
    path = os.path.expanduser(a.reference_csv)
    if not os.path.isfile(path):
        sys.exit(f"--reference-csv のファイルが見つかりません: {path}")
    outdir = outdir or os.path.join(os.path.expanduser(a.outdir), "classifier_report")
    os.makedirs(outdir, exist_ok=True)
    ref_df = pd.read_csv(path, dtype=str, keep_default_na=False)
    cj, ch, cp = [c.strip() for c in a.ref_cols.split(",")]
    need = [cj, ch, cp] + ([a.ref_lojo_col] if a.ref_lojo_col else [])
    miss = [c for c in need if c not in ref_df]
    if miss:
        sys.exit(f"--reference-csv に列 {miss} がありません(列: {list(ref_df.columns)}。--ref-cols・--ref-lojo-col で指定)")
    for c in need:
        ref_df[c] = ref_df[c].str.strip()
    cats = [c.strip() for c in a.clf_order.split(",") if c.strip()]
    lines = []
    P = lines.append
    P(f"分類性能の報告 ({VERSION}) 参照セット {a.reference_csv}: {len(ref_df)} 行 / 類型の並び {cats}")
    unk = ref_df.loc[~ref_df[ch].isin(cats), ch].value_counts()
    if len(unk):
        P(f"注意: 人手のラベルが類型の一覧にない行 {int(unk.sum())} 行を除く: {unk.to_dict()}")
    ref_df = ref_df[ref_df[ch].isin(cats)].copy()
    ref_df["group"] = ref_df[cj].map(_jgroup)
    P("雑誌群ごとの行数: " + str(ref_df.group.value_counts().to_dict()) + " / 雑誌ごとの行数: " + str(ref_df[cj].value_counts().to_dict()))
    p_pred, n_corpus = None, 0
    if a.clf_corpus:
        p_pred, n_corpus, n_other = _clf_corpus_shares(a, cats)
        P(f"コーパス(--csv の DAS ラベルあり・注記なし・{a.min_year} 年以降): {n_corpus:,} 件(類型の一覧にないラベル {n_other} 件)。"
          "論文の分析標本(共変量の欠損を除いた 648,217 件)より少し大きいため、PPV の点推定は本文の値と小数点以下でずれうる")
    variants = [("cv", cp, "cross-validated")] + ([("lojo", a.ref_lojo_col, "leave-one-journal-out")] if a.ref_lojo_col else [])
    for vname, pcol, vlabel in variants:
        sub = ref_df[ref_df[pcol].isin(cats)]
        if len(sub) < len(ref_df):
            P(f"\n注意: 予測ラベルが類型の一覧にない行 {len(ref_df) - len(sub)} 行を除く({pcol})")
        cnt = _clf_counts(sub[ch], sub[pcol], cats)
        tbl, summ = _clf_table(cnt, cats)
        if p_pred is not None:
            pi, ppv = _ppv_corpus(cnt, p_pred)
            tbl["corpus_pred_n"] = np.round(p_pred * n_corpus).astype(int)
            tbl["corpus_est_true_n"] = np.round(pi * n_corpus).astype(int)
            tbl["ppv_corpus"] = ppv
        pd.DataFrame(cnt.astype(int), index=cats, columns=cats).to_csv(os.path.join(outdir, f"confusion_matrix_{vname}.csv"), index_label="human_true", encoding="utf-8")
        tbl.to_csv(os.path.join(outdir, f"classifier_metrics_{vname}.csv"), index=False, encoding="utf-8-sig")
        P(f"\n===== {vlabel} 予測(列 {pcol}) N={summ['n']} =====")
        P(f"正解率 {summ['accuracy']:.4f} / Cohen の κ {summ['kappa']:.3f} / マクロ F1 {summ['macro_f1']:.3f}")
        P("[混同行列(行=人手、列=予測)]")
        P(pd.DataFrame(cnt.astype(int), index=cats, columns=cats).to_string())
        P("[類型ごとの性能]")
        P(tbl.drop(columns=["name"]).to_string(index=False, float_format=lambda x: f"{x:.3f}"))
        # 雑誌群別・雑誌別
        grows, gsum = [], []
        groups = [g for g in ("big3", "heliyon", "mdpi6") if g in set(sub.group)]
        for g in groups:
            sg = sub[sub.group == g]
            cg = _clf_counts(sg[ch], sg[pcol], cats)
            tg, su = _clf_table(cg, cats)
            tg.insert(0, "group", g)
            grows.append(tg[["group", "code", "n_human", "n_pred", "n_correct", "recall", "recall_lo", "recall_hi", "precision", "f1"]])
            gsum.append(dict(group=g, n=su["n"], accuracy=su["accuracy"], kappa=su["kappa"], macro_f1=su["macro_f1"]))
        gdf = pd.concat(grows, ignore_index=True) if grows else pd.DataFrame()
        gdf.to_csv(os.path.join(outdir, f"classifier_metrics_by_group_{vname}.csv"), index=False, encoding="utf-8-sig")
        pd.DataFrame(gsum).to_csv(os.path.join(outdir, f"classifier_summary_by_group_{vname}.csv"), index=False, encoding="utf-8-sig")
        P("[雑誌群別: 全体の正解率・κ]")
        P(pd.DataFrame(gsum).to_string(index=False, float_format=lambda x: f"{x:.3f}"))
        if len(gdf):
            P(f"[雑誌群別の再現率(人手の件数)。件数が {a.clf_min_n} 未満のセルは --]")
            pv = gdf.pivot(index="code", columns="group", values="recall").reindex(cats)
            pn = gdf.pivot(index="code", columns="group", values="n_human").reindex(cats)
            P(pd.DataFrame({g: [("--" if (pd.isna(pn.loc[c, g]) or pn.loc[c, g] < a.clf_min_n) else f"{pv.loc[c, g]:.2f} ({int(pn.loc[c, g])})") for c in cats] for g in groups}, index=cats).to_string())
        jr = []
        for j, sj in sub.groupby(cj):
            cj_ = _clf_counts(sj[ch], sj[pcol], cats)
            jr.append(dict(journal=j, group=_jgroup(j), n=int(cj_.sum()), accuracy=float(np.trace(cj_) / cj_.sum()) if cj_.sum() else np.nan))
        pd.DataFrame(jr).to_csv(os.path.join(outdir, f"classifier_by_journal_{vname}.csv"), index=False, encoding="utf-8-sig")
        # LaTeX
        sfx = "" if vname == "cv" else f"_{vname}"
        cap = (f"Classification performance of the ensemble labels against the human labels in the reference set "
               f"({vlabel} predictions). PPV in corpus: probability that an article predicted as the category belongs to it, "
               f"from the point estimate of the confusion matrix (no resampling) and the predicted shares of the corpus; values can differ from means over resampled confusion matrices.") if p_pred is not None else \
              f"Classification performance of the ensemble labels against the human labels in the reference set ({vlabel} predictions)."
        with open(os.path.join(outdir, f"tab_classifier_performance{sfx}.tex"), "w", encoding="utf-8") as f:
            f.write(_tex_clf_table(tbl, summ, f"tab:classifier_performance{sfx}", cap, p_pred is not None))
        with open(os.path.join(outdir, f"tab_confusion_matrix{sfx}.tex"), "w", encoding="utf-8") as f:
            f.write(_tex_confusion(cnt, cats, f"tab:confusion_matrix{sfx}",
                                   f"Confusion matrix of the reference set (rows: human labels; columns: ensemble predictions, {vlabel})."))
        if len(gdf):
            with open(os.path.join(outdir, f"tab_classifier_by_group{sfx}.tex"), "w", encoding="utf-8") as f:
                f.write(_tex_by_group(gdf, cats, groups, f"tab:classifier_by_group{sfx}",
                                      f"Recall by group of journals ({vlabel} predictions): the three largest journals (big3), Heliyon, and the six MDPI journals.", a.clf_min_n))
    txt = "\n".join(lines)
    print(txt)
    with open(os.path.join(outdir, "classifier_report.txt"), "w", encoding="utf-8") as f:
        f.write(txt + "\n")
    print("保存先:", outdir)


def _sha256(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def _export_reference(a, dep):
    """v061: 参照セットを reference_set.csv に書き、分類性能の表を dep に作る(--export-labels と --export-public で共通)。書き出したファイル名の一覧を返す"""
    rp = os.path.expanduser(a.reference_csv)
    if not os.path.isfile(rp):
        sys.exit(f"--reference-csv のファイルが見つかりません: {rp}")
    rd = pd.read_csv(rp, dtype=str, keep_default_na=False)
    cj, ch, cp = [c.strip() for c in a.ref_cols.split(",")]
    keep = [cj, ch, cp] + ([a.ref_lojo_col] if a.ref_lojo_col else [])
    idc = next((c for c in rd.columns if c.lower() == (a.ref_id_col or "").lower()), None)   # v053
    miss = [c for c in keep if c not in rd]
    if miss:
        sys.exit(f"--reference-csv に列 {miss} がありません(列: {list(rd.columns)})")
    if idc and idc not in keep:
        keep = [idc] + keep
    elif not idc:
        print(f"[注意] 参照セットに識別子の列 {a.ref_id_col} がないため、reference_set.csv に識別子は入りません(--ref-id-col で指定)", file=sys.stderr)
    ren = {cj: "journal", ch: "human_label", cp: "pred_ensemble_crossvalidated"}
    if a.ref_lojo_col:
        ren[a.ref_lojo_col] = "pred_ensemble_leave_one_journal_out"
    if idc:
        ren[idc] = "pmcid"
    rd = rd[keep].rename(columns=ren)
    rd.to_csv(os.path.join(dep, "reference_set.csv"), index=False, encoding="utf-8")
    files_note = ["reference_set.csv"]
    classifier_report(a, outdir=dep)
    files_note += ["confusion_matrix_cv.csv"] + (["confusion_matrix_lojo.csv"] if a.ref_lojo_col else []) + ["classifier_metrics_cv.csv", "classifier_report.txt (and tab_*.tex)"]
    return files_note


def export_labels(a):
    """--export-labels: DOI ごとの DAS ラベル(アンサンブルと 3 LLM)と、参照セット・混同行列を Zenodo 用のフォルダにまとめる。WoS 由来の列は出さない"""
    csv_path = os.path.expanduser(a.csv)
    if not os.path.isfile(csv_path):
        sys.exit(f"--csv のファイルが見つかりません: {csv_path}")
    dep = os.path.expanduser(a.export_dir) if a.export_dir else os.path.join(os.path.expanduser(a.outdir), "zenodo_deposit")
    os.makedirs(dep, exist_ok=True)
    head = list(pd.read_csv(csv_path, nrows=0).columns)
    low = {c.lower(): c for c in head}
    ids, seen = [], set()
    for c in [x.strip() for x in a.export_id_cols.split(",") if x.strip()]:
        if c.lower() in low and c.lower() not in seen:
            ids.append((low[c.lower()], c.lower()))
            seen.add(c.lower())
    if not ids:
        hit = [c for c in head if re.search(r"pmc|doi|_id$", c, flags=re.I)]
        sys.exit(f"識別子の列が見つかりません(--export-id-cols {a.export_id_cols})。それらしい列: {hit}。--export-id-cols で指定してください")
    extra = [x.strip() for x in a.export_extra_cols.split(",") if x.strip()]
    bad = [c for c in extra if c.lower().startswith("wos")]
    if bad:
        sys.exit(f"--export-extra-cols に WoS 由来の列 {bad} は指定できません(Clarivate の規約により公開できません)")
    extra = [c for c in extra if c in head and c not in [i[0] for i in ids]]
    core = ["journal_key", "pub_year", "article_type", "das_has_label", "das_label"]
    miss_core = [c for c in ("das_label", "das_has_label", "journal_key") if c not in head]
    if miss_core:
        sys.exit(f"--csv に必要な列がありません: {miss_core}")
    llm = [c for c in LLM_COLS if c in head]
    if len(llm) < 3:
        print(f"[警告] LLM の個別ラベルの列が足りません(見つかった列: {llm})。3 者一致は計算できません", file=sys.stderr)
    cols = list(dict.fromkeys([i[0] for i in ids] + [c for c in core if c in head] + llm + (["das_llm_agree"] if "das_llm_agree" in head else []) + extra))
    d, _ = read_cols(csv_path, cols)
    n0 = len(d)
    d = d[(d.das_has_label == "1") & (d.das_label != "")]
    if "article_type" in d and a.article_type:
        d = d[d.article_type == a.article_type]
    d = d.copy()
    out = pd.DataFrame(index=d.index)
    for src, nm in ids:
        out[nm] = d[src]
    out["journal"] = d["journal_key"]
    if "pub_year" in d:
        out["pub_year"] = d["pub_year"]
    if "article_type" in d:
        out["article_type"] = d["article_type"]
    out["das_ensemble"] = d["das_label"]
    names = {"das_ds32": "das_deepseek_v32", "das_gpt5": "das_gpt54", "das_mil3": "das_mistral_large3"}
    for c in llm:
        out[names[c]] = d[c]
    if len(llm) == 3:
        same = (d[llm[0]] == d[llm[1]]) & (d[llm[0]] == d[llm[2]]) & (d[llm[0]] != "")
        out["das_three_llm_agree"] = same.astype(int)
        if "das_llm_agree" in d:
            dis = int(((d.das_llm_agree == "1") != same).sum())
            print(f"[点検] 元の das_llm_agree と 3 者の一致の食い違い: {dis} 行")
    for c in extra:
        out[c] = d[c]
    key0 = ids[0][1]
    dup = int(out[key0].duplicated().sum())
    n = len(out)
    lines = []
    P = lines.append
    P(f"DAS ラベルの書き出し ({VERSION}) 元の CSV {a.csv}: {n0:,} 行 → ラベルあり・article_type={a.article_type or '(絞らない)'} {n:,} 行")
    P(f"識別子の列: {[i[1] for i in ids]} / {key0} の重複 {dup} 行")
    if a.export_expect and n != a.export_expect:
        P(f"[警告] 件数が論文の記載({a.export_expect:,})と違います: {n:,}。DAS 声明の 'For each of the {a.export_expect:,} articles' を確認してください")
    else:
        P(f"件数は論文の記載({a.export_expect:,})と一致")
    if "das_three_llm_agree" in out:
        y = num(out["pub_year"]) if "pub_year" in out else pd.Series(np.nan, index=out.index)
        P(f"3 LLM 完全一致の割合: 全体 {out.das_three_llm_agree.mean():.4f} / {a.min_year} 年以降 {out.loc[y >= a.min_year, 'das_three_llm_agree'].mean():.4f}(論文 2.2 節は 659,437 件で 86.7%)")
    P("類型別の件数: " + str(out.das_ensemble.value_counts().to_dict()))
    out.to_csv(os.path.join(dep, "das_labels_per_article.csv"), index=False, encoding="utf-8")
    ct = pd.crosstab(out.journal, out.das_ensemble, margins=True, margins_name="Total")
    ct.to_csv(os.path.join(dep, "das_labels_summary_by_journal.csv"), encoding="utf-8")
    files_note = ["das_labels_per_article.csv", "das_labels_summary_by_journal.csv"]
    if a.reference_csv:
        files_note += _export_reference(a, dep)
    readme = [
        "README: DAS labels for the study 'Data Availability Statement Categories in Relation to Citation Counts and Peer Review Duration'",
        f"Generated by analyze_citation_review_{VERSION}.py (--export-labels). Source table: {os.path.basename(csv_path)} (sha256 {_sha256(csv_path)}).",
        "",
        "Files",
        "  das_labels_per_article.csv  one row per article with a DAS label (PMC research articles).",
        "    pmcid, doi          identifiers (columns present in the source table)",
        "    journal             journal key; pub_year; article_type",
        "    das_ensemble        category assigned by the Random Forest stacking ensemble (the label used in the analyses)",
        "    das_deepseek_v32, das_gpt54, das_mistral_large3   labels of the three LLMs (DeepSeek-V3.2, GPT-5.4, Mistral-Large-3)",
        "    das_three_llm_agree 1 if the three LLM labels are identical, otherwise 0",
        "  das_labels_summary_by_journal.csv  counts of ensemble labels by journal.",
        "  reference_set.csv   reference statements: journal, human label, ensemble prediction (cross-validated; leave-one-journal-out if present).",
        "  confusion_matrix_*.csv  rows: human labels; columns: ensemble predictions.",
        "  classifier_metrics_*.csv, classifier_report.txt, tab_*.tex  per-category precision, recall, F1 and by-journal-group results.",
        "",
        "Category codes: F fully public repository deposition; M mixed public repository + author request; P public within article/supplement only;",
        "  R reuse of public third-party data only; C controlled-access repository; A author upon request only; N no data generated/not applicable.",
        "",
        f"Rows in das_labels_per_article.csv: {n:,}. Journals: {out.journal.nunique()}.",
        "No data obtained from Clarivate (WoS citation counts, WoS records, matching results, WoS notice flags) are included, because of the licence terms of the WoS Core Collection.",
        "Statement texts (das_text) are not included; they are available from PMC by PMCID.",
    ]
    with open(os.path.join(dep, "README_labels.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(readme) + "\n")
    P("書き出したファイル: " + ", ".join(files_note + ["README_labels.txt", "export_labels_log.txt", "MANIFEST.sha256"]))
    P("WoS 由来の列は含めていません。公開前に das_labels_per_article.csv の列を目で確かめてください")
    txt = "\n".join(lines)
    print(txt)
    with open(os.path.join(dep, "export_labels_log.txt"), "w", encoding="utf-8") as f:
        f.write(txt + "\n")
    man = []
    for fn in sorted(os.listdir(dep)):
        fp = os.path.join(dep, fn)
        if os.path.isfile(fp) and fn != "MANIFEST.sha256":
            man.append(f"{_sha256(fp)}  {fn}")
    with open(os.path.join(dep, "MANIFEST.sha256"), "w", encoding="utf-8") as f:
        f.write("\n".join(man) + "\n")
    print("保存先:", dep)


# ---- v061: 公開用データ(GitHub → Zenodo)の書き出し --------------------------------------------
# 論文の Data availability statement に書いた内容を 1 つのフォルダにまとめる。WoS(Clarivate)由来の列と DAS の本文は出さない。
EXPORT_DESC = {
    "journal_key": ("PMC", "Journal (journal key as in the source table)"),
    "pub_year": ("PMC", "Publication year"),
    "article_type": ("PMC", "Article type (research_article)"),
    "das_has_label": ("Classifier", "1 if the article has a DAS label"),
    "das_label": ("Classifier", "DAS category assigned by the Random Forest stacking ensemble (F, M, P, R, C, A, N); the label used in the analyses"),
    "das_ds32": ("Classifier", "DAS label by DeepSeek-V3.2"),
    "das_gpt5": ("Classifier", "DAS label by GPT-5.4"),
    "das_mil3": ("Classifier", "DAS label by Mistral-Large-3"),
    "das_llm_agree": ("Classifier", "1 if the three LLM labels are identical"),
    "n_authors": ("PMC full-text XML", "Number of authors"),
    "n_collab": ("PMC full-text XML", "Consortium (collaboration) authors; the analysis uses n_collab > 0"),
    "n_corresp": ("PMC full-text XML", "Number of corresponding authors"),
    "equal_contrib_any": ("PMC full-text XML", "1 if an equal-contribution note is present"),
    "n_orcid": ("PMC full-text XML", "Number of authors with an ORCID"),
    "pmc_n_countries_u": ("PMC full-text XML", "Number of countries in the author affiliations (UK nations merged, territories merged)"),
    "n_institutions_ror": ("PMC full-text XML", "Number of institutions (ROR)"),
    "n_refs": ("PMC full-text XML", "Number of references"),
    "ref_age_median": ("PMC full-text XML", "Median age of the references"),
    "n_refs_data": ("PMC full-text XML", "Data citations in the references; the analysis uses n_refs_data > 0"),
    "has_funding_positive": ("PMC full-text XML", "1 if a funding statement is present"),
    "body_words": ("PMC full-text XML", "Words in the article body"),
    "n_figures": ("PMC full-text XML", "Number of figures"),
    "n_tables": ("PMC full-text XML", "Number of tables"),
    "n_equations": ("PMC full-text XML", "Number of equations"),
    "n_supplementary": ("PMC full-text XML", "Number of supplementary files"),
    "abstract_words": ("PMC full-text XML", "Words in the abstract"),
    "title_words_adj": ("PMC full-text XML", "Words in the title, counted from the PMC title (articles whose adjusted title length in the analysis was taken from the Web of Science title carry the PMC count instead)"),
    "title_has_colon": ("PMC full-text XML", "1 if the title contains a colon"),
    "title_has_question": ("PMC full-text XML", "1 if the title is a question"),
    "has_body": ("PMC full-text XML", "1 if the article body is available (body-derived counts are missing otherwise)"),
    "corr_country_u": ("PMC full-text XML", "Country of the corresponding author"),
    "corr_country_status": ("PMC full-text XML", "How the corresponding-author country was assigned"),
    "days_received_to_accepted": ("PMC article history", "Days from receipt to acceptance (peer review duration)"),
    "pmc_citedby_n": ("PMC cited-by", "Number of PMC articles citing the article"),
    "cb_fetched": ("PMC cited-by", "1 if the PMC cited-by count was retrieved"),
    "oa_topic": ("OpenAlex", "Primary topic"), "oa_subfield": ("OpenAlex", "Subfield of the primary topic"),
    "oa_field": ("OpenAlex", "Field of the primary topic"), "oa_domain": ("OpenAlex", "Domain of the primary topic"),
    "oa_topic_score": ("OpenAlex", "Score of the primary topic"), "oa_found": ("OpenAlex", "1 if the DOI was found in OpenAlex"),
    "oa_pubyear": ("OpenAlex", "Publication year in OpenAlex"), "oa_pubdate": ("OpenAlex", "Publication date in OpenAlex"),
    "oa_cited_total": ("OpenAlex", "cited_by_count in OpenAlex (all years, at retrieval)"),
    "pub_month": ("PMC", "Publication month"), "date_accepted": ("PMC article history", "Date of acceptance"),
}


def _is_clarivate_col(c):
    cl = str(c).lower()
    return cl.startswith("wos") or "clarivate" in cl


def _gz_write_csv(df, path):
    df.to_csv(path, index=False, encoding="utf-8", compression={"method": "gzip", "compresslevel": 9, "mtime": 0})


def _gz_copy(src, dst):
    import gzip, shutil
    with open(src, "rb") as fi, open(dst, "wb") as fo:
        with gzip.GzipFile(filename="", mode="wb", fileobj=fo, compresslevel=9, mtime=0) as gz:
            shutil.copyfileobj(fi, gz)


def export_public(a):
    """--export-public: 公開用データ(論文単位の分析データ・参照セット・混同行列・OpenAlex の生データ・コード・設定)を 1 つのフォルダに書き出す。
    WoS(Clarivate)由来の列(wos で始まる列)と DAS の本文は出さない。GitHub の 100 MB 制限を超えそうなら雑誌ごとに分ける"""
    import platform, shutil
    csv_path = os.path.expanduser(a.csv)
    if not os.path.isfile(csv_path):
        sys.exit(f"--csv のファイルが見つかりません: {csv_path}")
    dep = os.path.expanduser(a.export_dir) if a.export_dir else os.path.join(os.path.expanduser(a.outdir), "zenodo_deposit")
    os.makedirs(dep, exist_ok=True)
    head = list(pd.read_csv(csv_path, nrows=0).columns)
    low = {c.lower(): c for c in head}
    ids = []
    for c in [x.strip() for x in a.export_id_cols.split(",") if x.strip()]:
        if c.lower() in low and low[c.lower()] not in ids:
            ids.append(low[c.lower()])
    if not ids:
        hit = [c for c in head if re.search(r"pmc|doi|_id$", c, flags=re.I)]
        sys.exit(f"識別子の列が見つかりません(--export-id-cols {a.export_id_cols})。それらしい列: {hit}")
    miss_core = [c for c in ("das_label", "das_has_label", "journal_key") if c not in head]
    if miss_core:
        sys.exit(f"--csv に必要な列がありません: {miss_core}")
    extra = [x.strip() for x in a.export_extra_cols.split(",") if x.strip()]
    bad = [c for c in extra if _is_clarivate_col(c)]
    if bad:
        sys.exit(f"--export-extra-cols に WoS 由来の列 {bad} は指定できません(Clarivate の規約により公開できません)")
    drop = {x.strip().lower() for x in a.export_drop_cols.split(",") if x.strip()}
    wanted = (ids + ["journal_key", "pub_year", "article_type", "das_has_label", "das_label"] + LLM_COLS + ["das_llm_agree"]
              + [s[1] for s in SPEC] + ["has_body", "corr_country_u", "corr_country_status", "days_received_to_accepted", "pmc_citedby_n", "cb_fetched"]
              + OA_COLS + OA_CNT_COLS + sorted(c for c in head if re.fullmatch(r"oa_cy_\d{4}", c))
              + [c.strip() for c in a.exposure_cols.split(",") if c.strip()] + extra)
    cols, absent = [], []
    for c in dict.fromkeys(wanted):
        if c not in head:
            absent.append(c)
        elif not _is_clarivate_col(c) and c.lower() not in drop and c.lower() != "das_text":
            cols.append(c)
    _helper = [c for c in ("title_words", "title_len_source") if c in head and c not in cols]   # v064: 公開しない補助列
    d, _ = read_cols(csv_path, cols + _helper)
    n0 = len(d)
    d = d[(d.das_has_label == "1") & (d.das_label != "")]
    n_lab = len(d)
    if "article_type" in d and a.article_type:
        d = d[d.article_type == a.article_type]
    d = d.copy()
    n = len(d)
    n_wos_title = 0   # v064
    if "title_words_adj" in cols and "title_words" in d and "title_len_source" in d and not a.export_keep_wos_title:
        _m = d["title_len_source"].str.contains("wos", case=False, na=False)
        n_wos_title = int(_m.sum())
        d.loc[_m, "title_words_adj"] = d.loc[_m, "title_words"]
    key0 = ids[0]
    dup = int(d[key0].duplicated().sum())
    year = num(d["pub_year"]) if "pub_year" in d else pd.Series(np.nan, index=d.index)
    days = num(d["days_received_to_accepted"]) if "days_received_to_accepted" in d else pd.Series(np.nan, index=d.index)
    lines = []
    P = lines.append
    _old = [f for f in os.listdir(dep) if f not in ("MANIFEST.sha256",)]
    if _old:
        P(f"[注意] 出力先 {dep} に既存のファイルが {len(_old)} 個あります。同じ名前のファイルは上書きします。前回の実行で作った古いファイルは残るので、不要なら出力先を空にしてから実行してください")
    P(f"公開用データの書き出し ({VERSION}) 元の CSV {os.path.basename(csv_path)}: {n0:,} 行")
    P(f"DAS ラベルあり {n_lab:,} 行 → article_type={a.article_type or '(絞らない)'} {n:,} 行 / {key0} の重複 {dup} 行")
    if a.export_expect and n != a.export_expect:
        P(f"[警告] 件数が論文の記載({a.export_expect:,})と違います: {n:,}")
    else:
        P(f"件数は論文の記載({a.export_expect:,})と一致")
    P(f"出版年 {a.min_year} 年以降: {int((year >= a.min_year).sum()):,} 行 / 査読期間 0〜{a.max_review_days} 日: {int(((days >= 0) & (days <= a.max_review_days)).sum()):,} 行 / "
      f"PMC cited-by 取得済み: {int((d['cb_fetched'] == '1').sum()):,} 行" if "cb_fetched" in d else "")
    if absent:
        P(f"[注意] CSV にない列(出力しません): {absent}")
    P(f"出力する列({len(cols)}): {cols}")
    P(f"除いた列: WoS(Clarivate)由来 {[c for c in head if _is_clarivate_col(c)]} / das_text / --export-drop-cols {sorted(drop)}")
    if "title_words_adj" in cols:
        if a.export_keep_wos_title:
            P("[警告] --export-keep-wos-title: title_words_adj に WoS の題名から取った値が含まれます。公開には使わないでください")
        elif "title_words" in d and "title_len_source" in d:
            P(f"[確認] title_words_adj のうち題名の長さを WoS の題名から取った {n_wos_title:,} 行(title_len_source が wos)は、PMC の題名から数えた title_words に置き換えました(title_words・title_len_source は出しません)")
        else:
            P("[警告] title_words・title_len_source が CSV にないため、title_words_adj の WoS 由来の値を確かめられません。--export-drop-cols title_words_adj で除くか、列を確かめてください")
    out = d[cols]
    assert not [c for c in out.columns if _is_clarivate_col(c)], "WoS 由来の列が混ざっています"
    max_b = float(a.export_max_mb) * 1024 * 1024
    files = []
    big = os.path.join(dep, "articles_public_data.csv.gz")
    _gz_write_csv(out, big)
    if os.path.getsize(big) > max_b:
        sz = os.path.getsize(big) / 1048576
        os.remove(big)
        P(f"articles_public_data.csv.gz は {sz:.0f} MB で --export-max-mb {a.export_max_mb} を超えるため、雑誌ごとに分けます")
        for j, g in out.groupby("journal_key", sort=True):
            slug = re.sub(r"[^A-Za-z0-9]+", "_", str(j)).strip("_")[:40] or "journal"
            fn = f"articles_public_data_{slug}.csv.gz"
            _gz_write_csv(g, os.path.join(dep, fn))
            files.append(fn)
            if os.path.getsize(os.path.join(dep, fn)) > max_b:
                P(f"[警告] {fn} も {os.path.getsize(os.path.join(dep, fn)) / 1048576:.0f} MB あります。Git LFS か、Zenodo だけに置いてください")
    else:
        files.append("articles_public_data.csv.gz")
    P("論文単位のデータ: " + ", ".join(f"{f} ({os.path.getsize(os.path.join(dep, f)) / 1048576:.1f} MB)" for f in files))
    dd = pd.DataFrame([{"column": c, "source": EXPORT_DESC.get(c, ("", ""))[0] or ("PMC" if c in ids else "OpenAlex" if re.fullmatch(r"oa_cy_\d{4}", c) else "(extra column)"),
                        "description": EXPORT_DESC.get(c, ("", ""))[1] or ((f"Citations in {c[6:]} according to OpenAlex counts_by_year (empty = none recorded)" + ("; partial year, counted up to the retrieval date" if c[6:] == "2026" else "")) if re.fullmatch(r"oa_cy_\d{4}", c) else
                                                                          ("Article identifier" if c in ids else "(extra column)"))} for c in cols])
    dd.to_csv(os.path.join(dep, "data_dictionary.csv"), index=False, encoding="utf-8")
    ct = pd.crosstab(out.journal_key, out.das_label, margins=True, margins_name="Total")
    ct.to_csv(os.path.join(dep, "das_labels_summary_by_journal.csv"), encoding="utf-8")
    files += ["data_dictionary.csv", "das_labels_summary_by_journal.csv"]
    doi_col = next((c for c in ids if c.lower() == "doi"), None)
    if doi_col:
        w = d[[doi_col, "journal_key"] + (["pub_year"] if "pub_year" in d else [])]
        w = w[w[doi_col] != ""].rename(columns={doi_col: "doi"})
        w.to_csv(os.path.join(dep, "wos_doi_list.csv"), index=False, encoding="utf-8")
        files.append("wos_doi_list.csv")
    wq = ["Web of Science Core Collection citation counts (Times Cited) are not included in this deposit (Clarivate licence).",
          "They were obtained by DOI (wos_doi_list.csv) in the WoS Core Collection and joined to the articles by DOI; the column used in the analyses is wos_TC.",
          "To reproduce the citation models, retrieve the counts under your own licence, join them by DOI to articles_public_data (columns wos_matched, wos_TC, wos_notice_type as in analyze_citation_review), and run the script with --csv on the joined table.",
          "Articles flagged in WoS as retractions or expressions of concern were excluded from the analyses reported in the paper (wos_notice_type); this flag is not part of the deposit."]
    if a.wos_query_file:
        qp = os.path.expanduser(a.wos_query_file)
        if not os.path.isfile(qp):
            sys.exit(f"--wos-query-file が見つかりません: {qp}")
        shutil.copy(qp, os.path.join(dep, "wos_query.txt"))
        wq += ["", "The query used is given in wos_query.txt."]
        files.append("wos_query.txt")
    else:
        P("[注意] --wos-query-file が未指定です。論文の Data availability statement は WoS の「the query used」を書いているので、実際の検索式のファイルを指定してください")
    with open(os.path.join(dep, "WOS_RETRIEVAL.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(wq) + "\n")
    files.append("WOS_RETRIEVAL.txt")
    if a.reference_csv:
        files += _export_reference(a, dep)
    oa_notes, has_topics_meta, topics_note = [], False, False   # v063
    if not a.export_no_openalex_raw:
        os.makedirs(os.path.join(dep, "openalex_raw"), exist_ok=True)
        got = []
        for pth in (a.oa_cache, a.oa_counts_cache):
            sp = os.path.expanduser(pth)
            if os.path.isfile(sp):
                dst = os.path.join(dep, "openalex_raw", os.path.basename(sp) + ".gz")
                _gz_copy(sp, dst)
                got.append(os.path.relpath(dst, dep))
                if os.path.getsize(dst) > max_b:
                    P(f"[警告] {os.path.relpath(dst, dep)} が {os.path.getsize(dst) / 1048576:.0f} MB あります。GitHub の制限を超える場合は Zenodo だけに置いてください")
            else:
                P(f"[注意] OpenAlex の生データがありません: {sp}")
        for pth in (a.oa_cache, a.oa_counts_cache):
            for mp in sorted(glob.glob(os.path.join(os.path.dirname(os.path.expanduser(pth)), "openalex*meta*.json"))):
                dst = os.path.join(dep, "openalex_raw", os.path.basename(mp))
                shutil.copy(mp, dst)
                if os.path.relpath(dst, dep) not in got:
                    got.append(os.path.relpath(dst, dep))
        _nm = [os.path.basename(g).lower() for g in got]   # v063: counts と topics を別々に確かめる
        has_counts_meta = any("counts" in n and "meta" in n and n.endswith(".json") for n in _nm)
        has_topics_meta = any("topics" in n and "meta" in n and n.endswith(".json") for n in _nm)
        if not has_counts_meta:
            P("[注意] OpenAlex の年次被引用数(counts)の取得記録 openalex_counts_meta.json が見つかりません")
        if not has_topics_meta:
            tdate = (a.export_oa_topics_date or "").strip()
            if tdate:
                note = os.path.join(dep, "openalex_raw", "openalex_topics_retrieval_note.txt")
                with open(note, "w", encoding="utf-8") as f:
                    f.write(f"OpenAlex primary_topic (openalex_topics.jsonl.gz) was retrieved on {tdate}.\n"
                            "This date was recorded by the authors; the retrieval script did not write a machine-readable record (openalex_topics_meta.json) for this run.\n")
                got.append(os.path.relpath(note, dep))
                topics_note = True
                P(f"[注意] OpenAlex の分野(topics)の取得記録 openalex_topics_meta.json は見つかりません。--export-oa-topics-date の「{tdate}」を openalex_topics_retrieval_note.txt と README_data.md に書きました")
            else:
                P("[注意] OpenAlex の分野(topics)の取得記録 openalex_topics_meta.json が見つかりません。取得日を --export-oa-topics-date で渡すと説明ファイルと README_data.md に書きます")
        files += got
        if topics_note:
            oa_notes.append(f"- OpenAlex topic fields (`oa_topic`, `oa_subfield`, `oa_field`, `oa_domain`, `oa_topic_score`) were retrieved on {(a.export_oa_topics_date or '').strip()}. The date was recorded by the authors (see `openalex_raw/openalex_topics_retrieval_note.txt`).")
        elif has_topics_meta:
            oa_notes.append("- OpenAlex retrieval dates and conditions are in `openalex_raw/openalex*meta*.json`.")
    if "oa_cy_2026" in cols:
        oa_notes.append("- `oa_cy_2026` is a partial year: citations recorded up to the retrieval of `counts_by_year`, not for the whole of 2026.")
    if not a.export_no_code:
        os.makedirs(os.path.join(dep, "code"), exist_ok=True)
        shutil.copy(os.path.abspath(__file__), os.path.join(dep, "code", f"analyze_citation_review_{VERSION}.py"))
        files.append(f"code/analyze_citation_review_{VERSION}.py")
        _stale = sorted(f for f in os.listdir(os.path.join(dep, "code")) if f.startswith("analyze_citation_review_") and f != f"analyze_citation_review_{VERSION}.py")   # v063
        if _stale:
            P(f"[注意] code/ に別の版のコードが残っています: {_stale}。公開するのは今回の版だけにするなら削除してから、もう一度実行して MANIFEST.sha256 を作り直してください")
    settings = dict(script_version=VERSION, created_utc=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    command=sys.argv, python=platform.python_version(), pandas=pd.__version__, numpy=np.__version__,
                    source_table=os.path.basename(csv_path), source_table_sha256=_sha256(csv_path),
                    defaults=dict(article_type=a.article_type, min_year=a.min_year, max_review_days=a.max_review_days, das_ref=a.das_ref),
                    rows=dict(source=n0, labelled=n_lab, exported=n), columns=cols)
    with open(os.path.join(dep, "settings.json"), "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)
    files.append("settings.json")
    readme = [
        "# Data for: Data Availability Statement Categories in Relation to Citation Counts and Peer Review Duration",
        "",
        f"Generated by analyze_citation_review_{VERSION}.py (--export-public). Source table: {os.path.basename(csv_path)} (sha256 {_sha256(csv_path)}).",
        "",
        "## Files",
        "- `articles_public_data.csv.gz` (or `articles_public_data_<journal>.csv.gz` if split by journal): one row per research article with a DAS label "
        f"({n:,} rows). Identifiers, journal, year, DAS labels (ensemble and three LLMs), article factors from the PMC full-text XML, "
        "receipt-to-acceptance days, PMC cited-by counts, and OpenAlex topic and citing works by year. Column names are those of the analysis script, so the file can be passed to it with `--csv`. See `data_dictionary.csv`.",
        "- `das_labels_summary_by_journal.csv`: counts of ensemble labels by journal.",
        "- `reference_set.csv`, `confusion_matrix_*.csv`, `classifier_metrics_*.csv`, `classifier_report.txt`, `tab_*.tex`: the 1,200-statement reference set (human and predicted labels) and the classification performance (if present).",
        "- `openalex_raw/`: OpenAlex responses as retrieved (gzip) and the retrieval dates and conditions (`openalex*meta*.json`).",
        "- `wos_doi_list.csv`, `WOS_RETRIEVAL.txt`: DOIs and the procedure to retrieve the Web of Science counts again.",
        "- `code/`, `settings.json`: the analysis script and the settings of this export (command line, versions, defaults).",
        "- `MANIFEST.sha256`: SHA-256 checksums of all files.",
        "",
        "## Not included",
        "- Web of Science data (citation counts, matching results, notice flags such as retractions): not redistributable under the Clarivate licence. The 1,845 articles flagged in WoS as retractions or expressions of concern and excluded in the paper cannot be identified from this deposit.",
        "- Text of the data availability statements (available from PMC by PMCID).",
        "",
        "## Reading the data",
        "```python",
        "import pandas as pd, glob",
        "d = pd.concat(pd.read_csv(f, dtype=str, keep_default_na=False) for f in sorted(glob.glob('articles_public_data*.csv.gz')))",
        "```",
        "",
        "## Category codes",
        "F fully public repository deposition; M mixed public repository + author request; P public within article/supplement only; R reuse of public third-party data only; C controlled-access repository; A author upon request only; N no data generated/not applicable.",
        *([""] + ["## OpenAlex"] + oa_notes if oa_notes else []),
        *(["", "## Notes on columns", f"- `title_words_adj`: for {n_wos_title:,} articles ({n_wos_title / max(n, 1):.2%}) the analysis took the adjusted title length from the Web of Science title; the deposit carries the word count of the PMC title for these articles instead, so this covariate differs from the analysis value for them."] if n_wos_title else []),
        "",
        "## Licence",
        f"Code: see the repository licence. Data files: {a.export_data_license}. OpenAlex-derived fields are from OpenAlex (CC0).",
    ]
    with open(os.path.join(dep, "README_data.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(readme) + "\n")
    files.append("README_data.md")
    P("書き出したファイル: " + ", ".join(files + ["export_public_log.txt", "MANIFEST.sha256"]))
    P("公開前に data_dictionary.csv と出力した列を目で確かめてください(WoS 由来の列は含めていません)")
    txt = "\n".join(x for x in lines if x)
    print(txt)
    with open(os.path.join(dep, "export_public_log.txt"), "w", encoding="utf-8") as f:
        f.write(txt + "\n")
    man = []
    for root, _, fns in os.walk(dep):
        for fn in sorted(fns):
            rel = os.path.relpath(os.path.join(root, fn), dep)
            if rel != "MANIFEST.sha256":
                man.append(f"{_sha256(os.path.join(root, fn))}  {rel}")
    with open(os.path.join(dep, "MANIFEST.sha256"), "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(man, key=lambda s: s.split('  ', 1)[1])) + "\n")
    print("保存先:", dep)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", default=DEFAULT_CSV)
    ap.add_argument("--outdir", default=DEFAULT_OUT)
    ap.add_argument("--labels", action="store_true", help="ラベルの点検だけ行う")
    ap.add_argument("--find-cols", default="", help="列名に含まれる文字列(正規表現可、例: pmc|doi|_id)で CSV の列名を探して表示するだけ。--dedup-key に使う列を探すとき用")
    ap.add_argument("--target", choices=["both", "citations", "review"], default="both")
    ap.add_argument("--dv", default="wos_TC", help="従属変数(wos_TC / pmc_citedby_n / review_days / v042: oa_c<k>・oa_a<j>・oa_l<k>・oa_total)。review_days=査読期間(受付→受理の日数)を被引用数と同じ分析(OLS・NB・LRT・交互作用・雑誌別・順位検定・頑健性)にかける。出力先の既定は analysis_review")
    ap.add_argument("--review-as-iv", action="store_true")
    ap.add_argument("--das-ref", default="F")
    ap.add_argument("--article-type", default="research_article", help="空文字なら絞らない")
    ap.add_argument("--keep-notice", action="store_true", help="取り下げ・懸念表明などの注記がある行も使う")
    ap.add_argument("--drop-merged", action="store_true", help="WoS のレコードが合体した行(wos_merged_any=1)を除く")
    ap.add_argument("--require-journal-ok", action="store_true", help="wos_journal_ok が 1 でない WoS 照合の被引用数を使わない")
    ap.add_argument("--require-title-fit", action="store_true", help="wos_title_fit が「±3 以内」でない、または題名の先頭が怪しい照合の被引用数を使わない")
    ap.add_argument("--corr-top", type=int, default=12, help="責任著者の国のダミーにする上位の国数(0 で使わない)")
    ap.add_argument("--journal", default="", help="雑誌名に含まれる文字列で絞る(例: PLOS)")
    ap.add_argument("--min-year", type=int, default=2014)
    ap.add_argument("--min-cat", type=int, default=300)
    ap.add_argument("--min-group", type=int, default=20)
    ap.add_argument("--max-missing", type=float, default=0.20)
    ap.add_argument("--max-review-days", type=int, default=1500)
    ap.add_argument("--exclude", default="", help="使わない説明変数(列名をカンマ区切り)")
    ap.add_argument("--n-perm", type=int, default=300)
    ap.add_argument("--no-nb", action="store_true", help="NB 回帰(LRT・交互作用・雑誌別・重複除外を含む)を行わない")
    ap.add_argument("--no-rank", action="store_true", help="記述統計と順位検定(Kruskal-Wallis・Mann-Whitney)を行わない")
    ap.add_argument("--no-interactions", action="store_true", help="交互作用の LRT を行わない")
    ap.add_argument("--no-by-journal", action="store_true", help="雑誌別の NB を行わない")
    ap.add_argument("--nb-fe", choices=["additive", "jy"], default="additive", help="NB の固定効果: additive=雑誌+出版年(論文と同じ) / jy=雑誌×年")
    ap.add_argument("--nb-lrt", choices=["variable", "group", "off"], default="variable", help="LRT 重要度の粒度(variable=説明変数ごと、group=グループごと、off=行わない)")
    ap.add_argument("--nb-sample", type=int, default=0, help="NB の行を無作為抽出して試す(0 で全行)。動作確認と所要時間の見積もり用")
    ap.add_argument("--interaction-year", type=int, default=2020, help="DAS×出版年の交互作用で「以降」とみなす年(論文の COVID の代用)")
    ap.add_argument("--min-inter", type=int, default=20, help="交互作用の列を残す最小の 1 の数")
    ap.add_argument("--min-cat-j", type=int, default=30, help="雑誌別の検定・推定で DAS 類型を使う最小件数")
    ap.add_argument("--dedup-key", default="", help="重複を除く感度分析に使う列名(例: pmcid)。空なら行わない")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--robustness", action="store_true", help="通常の分析のあと、被引用数の定義(wos_TC / pmc_citedby_n)と固定効果(雑誌+年 / 雑誌×年)を替えて NB を走らせ直し、DAS 類型の効果を比べる")
    ap.add_argument("--robustness-only", action="store_true", help="通常の分析は行わず、頑健性の確認だけ行う")
    ap.add_argument("--robust-runs", default="", help="頑健性で走らせる設定(カンマ区切り)。既定は全部(被引用数: " + ", ".join(ROBUST_RUNS) + " / 査読期間: base, jy)")
    ap.add_argument("--paper-review-dir", default=DEFAULT_OUT_REVIEW, help="被引用数と査読期間を並べる比較図(fig7)で、査読期間の出力があるフォルダ")
    ap.add_argument("--fig6c-wos-jy", default="", help="v035: fig6c・頑健性の表の WoS・雑誌×年(年齢の項なし)の出力フォルダ(既定: <outdir>/robustness_nospline/jy)")
    ap.add_argument("--fig6c-pmc", default="", help="v035: PMC・雑誌+年(WoS と同じ論文集合)の出力フォルダ(既定: analysis_pmc_samewos)")
    ap.add_argument("--fig6c-pmc-jy", default="", help="v035: PMC・雑誌×年(WoS と同じ論文集合)の出力フォルダ(既定: analysis_pmc_samewos_jy)")
    ap.add_argument("--fig6c-pmc-full", default="", help="v037: --check-fig6c で比べる、WoS 照合なしを含む全 PMC(N=655,860)・雑誌+年の出力フォルダ(既定: <outdir の親>/analysis_pmc)")
    ap.add_argument("--check-fig6c", action="store_true", help="v037: 表 5・fig6c の PMC 列が WoS と同じ論文集合の実行か全 PMC の実行かを、保存済みの nb_model_*.csv と nb_irr_*.csv から確かめる(回帰は走らせない)")
    ap.add_argument("--robust-outroot", default="", help="頑健性の出力先(既定: --outdir の下の robustness)")
    ap.add_argument("--paper-figs", action="store_true", help="分析のあと、論文用の図(PNG 300dpi と PDF)と表(CSV と xlsx)を 1 つのフォルダ(--paper-dir、既定 ~/output_covariates_v27/paper)に作る")
    ap.add_argument("--main-figs", action="store_true", help="v033: 本論で使う図 7 点だけを PNG で作る(保存済みの CSV から。分析・表・PDF は作らない)。出力は <paper-dir>/figures_main")
    ap.add_argument("--paper-only", action="store_true", help="分析は行わず、保存済みの CSV から論文用の図表だけ作り直す")
    ap.add_argument("--paper-dir", default="", help="論文用の図表の保存先(既定: ~/output_covariates_v27/paper。被引用数・査読期間の図表をここにまとめる)")
    ap.add_argument("--paper-citation-dir", default=DEFAULT_OUT, help="補足表 S1 で、被引用数(wos_TC)の主モデルの出力があるフォルダ(--dv review_days で図表を作るときに使う)")
    ap.add_argument("--pmc-on-wos-sample", action="store_true", help="--dv pmc_citedby_n で、WoS 照合のない論文を除く(WoS のモデルと同じ論文集合で比べる)")
    ap.add_argument("--cb-compare", action="store_true", help="WoS と PMC の被引用数の記述統計・相関だけ出す(NB は走らせない)")
    ap.add_argument("--supp-pdf", action="store_true", help="補足表(S1・S2)の tex を pdflatex で PDF にする(pdflatex があるとき)")
    ap.add_argument("--robust-skip-existing", action="store_true", help="頑健性で、出力がある設定は走らせない")
    ap.add_argument("--pack-send", action="store_true", help="送る結果ファイルを 1 つのフォルダ(と zip)にまとめる(分析は走らせない)")
    ap.add_argument("--pack-root", default="~/output_covariates_v27", help="--pack-send: 入力フォルダの親")
    ap.add_argument("--pack-dirs", default="", help="--pack-send: 親からの相対フォルダ(カンマ区切り)。既定: " + ", ".join(PACK_DEFAULT_DIRS))
    ap.add_argument("--pack-out", default="~/output_covariates_v27/send", help="--pack-send: まとめ先のフォルダ(zip は同じ名前に .zip を付ける)")
    ap.add_argument("--pack-max-mb", type=float, default=5.0, help="--pack-send: これより大きいファイルは入れない")
    ap.add_argument("--pack-no-zip", action="store_true", help="--pack-send: zip を作らない")
    ap.add_argument("--check-journal-groups", action="store_true", help="年ごとの big3・Heliyon・MDPI 6 誌の件数を数え、本文 3.1節の 981・40,563 がどの集合かを判定する(分析は走らせない)")
    ap.add_argument("--check-ref", default="2020:981:32206,2021:40563:75937", help="--check-journal-groups: 本文の数値(年:該当件数:その年の全体 をカンマ区切り)")
    ap.add_argument("--check-sample", action="store_true", help="分析に使う件数(論文の表1・抄録・結論の件数)を、回帰を走らせずに数えて、論文の値と照合する。WoS 被引用数のモデルの標本の平均・分散・最大も出す(CSV を 5 回読むので数分)")
    ap.add_argument("--check-n-ref", default="b=661365,c=659520,d=659437,e=651617,f=648217,g=659335,h=655763,pmc=655860,pmc_on_wos=648217,title_fit=646938,groups_cit=72,groups_rev=74,groups_pmc=74", help="--check-sample: 論文の値(キー=件数 をカンマ区切り。b〜h は表1の段階、pmc・pmc_on_wos・title_fit は 3.6・3.7節、groups_* は雑誌×年の群の数)")
    ap.add_argument("--check-section31", action="store_true", help="論文 3.1節の数値(年別・雑誌別の割合、WoS 被引用数の平均)がどの論文集合の値かを確かめる(分析は走らせない)")
    ap.add_argument("--check-contrast", action="store_true", help="主 NB モデルを 1 回推定し、別の基準(--contrast-ref)との対比と Holm 調整後の p を出す(論文 3.6節の N 基準の結果。通常の実行でも nb_suite が同じ表を出す)")
    ap.add_argument("--contrast-ref", default="N", help="--check-contrast と通常の実行で、対比の基準にする DAS 類型(既定 N)")
    ap.add_argument("--exposure", choices=["off", "offset", "covariate", "spline"], default="off", help="v020: 経過時間の扱い。off=出版年の固定効果のみ / offset=log(経過年数)をオフセット / covariate=log(経過年数)を係数つきで入れる / spline=log(経過年数)の折れ線スプライン(v025、--age-knots 個の結び目)")
    ap.add_argument("--exposure-cols", default="pub_date,date_published,pub_month,date_accepted", help="v020: 出版日(または年月・受理日)の列名(カンマ区切り、左から優先。列がなければ飛ばす。--find-cols 'date|month|day' で探す)")
    ap.add_argument("--exposure-ref-date", default="", help="v020: 被引用数を取得した日(既定: WoS 2026-06-15、PMC 2026-10-29)")
    ap.add_argument("--exposure-min-age", type=float, default=0.05, help="v020: 経過年数の下限(年)。出版直後の log を安定させる")
    ap.add_argument("--check-exposure", action="store_true", help="v020: 経過時間の扱い 4 通りの NB を比べる")
    ap.add_argument("--check-zero", action="store_true", help="v020: ゼロの多さ(NB2 の予測ゼロ割合、ハードルモデル)を確認する")
    ap.add_argument("--check-cluster", action="store_true", help="v020: t(G-1) と wild cluster score bootstrap で小クラスタの推論を補う")
    ap.add_argument("--check-vif", action="store_true", help="v045: 多重共線性の診断(VIF・GVIF)。主モデルの設計行列を使う。--dv wos_TC / pmc_citedby_n / review_days / oa_*")
    ap.add_argument("--check-adjust-sets", action="store_true", help="v047: 調整集合を替えた DAS の率比の比較(FE=共変量なし・D=DAS に先行する共変量だけ・B・A=論文の tab:mediator・Main=全共変量)。--dv wos_TC / review_days など。集合ごとに NB を推定する(数分×集合の数)")
    ap.add_argument("--adjust-sets", default="FE,D,B,A,Main", help="v047: --check-adjust-sets で推定する集合(カンマ区切り。FE,D,B,A,Main のうち)")
    ap.add_argument("--check-wos-gap", action="store_true", help="v049: WoS 未照合が集中する期間(既定: IJERPH の 2023 年以降・Heliyon の 2025 年)を除いて主モデルを再推定し、DAS の率比を比べる(--dv wos_TC)")
    ap.add_argument("--gap-spec", default="ENVIRON:2023,HELIYON:2025", help="v049: --check-wos-gap で除く雑誌と年(雑誌名の一部:年 をカンマ区切り。その年以降を除く。既定 ENVIRON:2023,HELIYON:2025)")
    ap.add_argument("--vif-threshold", type=float, default=5.0, help="v045: --check-vif で印を付ける VIF の目安(既定 5。10 でも別に数える)")
    ap.add_argument("--boot-reps", type=int, default=999, help="v020: bootstrap の反復数")
    ap.add_argument("--boot-weights", choices=["webb", "rademacher"], default="webb", help="v020: bootstrap の重み")
    ap.add_argument("--shapley-nb", action="store_true", help="v020: NB の対数尤度に基づく Shapley 分解(2^グループ数 回の NB)")
    ap.add_argument("--shapley-nb-both", action="store_true", help="v024: NB 版 Shapley 分解を被引用数(wos_TC)と査読期間(review_days)で続けて実行する(--dv は wos_TC のまま)")
    ap.add_argument("--shapley-review-outdir", default=DEFAULT_OUT_REVIEW, help="v024: --shapley-nb-both で査読期間の結果を保存する(OLS 版の shapley_group_review_days.csv もここから読む)フォルダ")
    ap.add_argument("--shapley-maxit", type=int, default=100, help="v024: NB 版 Shapley の各モデルの最大反復数(未収束なら 2 倍で推定し直す)")
    ap.add_argument("--shapley-fresh", action="store_true", help="v024: NB 版 Shapley のキャッシュ(shapley_nb_cache_<tag>.json)を使わず最初から推定する")
    ap.add_argument("--field-col", default="", help="v021: 分野の代理にする CSV の列名(主題・MeSH・キーワードなど。--find-cols 'subject|categor|mesh|kw|topic' で探す)。上位の水準をダミーにして共変量に加える")
    ap.add_argument("--fetch-topics", action="store_true", help="v039: OpenAlex から --csv の DOI の primary_topic を取得して --oa-cache に追記する(取得済みは飛ばす。再開できる)。キーは --oa-api-key か環境変数 OPENALEX_API_KEY")
    ap.add_argument("--merge-topics", action="store_true", help="v039: 取得済みの結果(--oa-cache)を --csv に結合して --oa-out に書き出し、付与率を表示する")
    ap.add_argument("--topics-pipeline", action="store_true", help="v039: 取得(再開可)→結合→subfield を入れた NB(被引用数と査読期間)を続けて行う。予算切れで止まったら同じコマンドで再開")
    ap.add_argument("--oa-cache", default="~/output_covariates_v27/openalex_topics.jsonl", help="v039: OpenAlex の生データ(1 行 1 DOI の jsonl)")
    ap.add_argument("--oa-out", default="~/output_covariates_v27/pmc_wos_v27_3llms_topic.csv", help="v039: 結合後の CSV の保存先")
    ap.add_argument("--oa-mailto", default="", help="v039: OpenAlex に渡す連絡先メール")
    ap.add_argument("--oa-api-key", default="", help="v039: OpenAlex の API キー(省略時は環境変数 OPENALEX_API_KEY)。シェルの履歴に残さないため、環境変数を勧める")
    ap.add_argument("--oa-batch", type=int, default=50, help="v039: 1 回のリクエストにまとめる DOI の数(最大 100)。大きいほど少ないクレジットで終わる")
    ap.add_argument("--oa-sleep", type=float, default=0.15, help="v039: リクエストの間隔(秒)")
    ap.add_argument("--oa-limit", type=int, default=0, help="v039: 試験用。先頭からこの件数だけ取得")
    ap.add_argument("--supp-field", action="store_true", help="v040: 分野の係数の補足表 S3・S4 の tex を作る(先に --check-extra subfield を被引用数と査読期間で実行して係数の CSV を保存しておく)")
    ap.add_argument("--supp-field-specs", default="field,domain,sub50", help="v040: 補足表に載せる分野の入れ方(カンマ区切り。--subfield-variants で実行済みのもの)")
    ap.add_argument("--subfield-variants", default="field,sub50", help="v039: --check-extra subfield で比べる分野の入れ方。field=OpenAlex 26 分野 / domain=4 / sub<N>=subfield の上位 N 個(例 sub50,sub100)。カンマ区切り")
    ap.add_argument("--field-top", type=int, default=30, help="v021: --field-col でダミーにする上位の水準の数")
    ap.add_argument("--das-source", choices=["ensemble", "ds32", "gpt5", "mil3"], default="ensemble", help="v021: DAS ラベルに使う列(ensemble=das_label / ds32・gpt5・mil3=各 LLM 単独のラベル)")
    ap.add_argument("--das-agree-only", action="store_true", help="v021: 3 つの LLM のラベルが一致した論文だけを使う")
    ap.add_argument("--check-label-noise", action="store_true", help="v021: DAS ラベルをアンサンブル・各 LLM 単独・3 LLM 一致のみに替えた NB を並べる")
    ap.add_argument("--check-misclass", action="store_true", help="v021: 混同行列(--confusion-csv)による誤分類の確率的感度分析(Rubin の規則で統合)")
    ap.add_argument("--confusion-csv", default="", help="v021: 人手(真)×予測の件数の正方行列。1 列目=真の類型、1 行目=予測の類型")
    ap.add_argument("--noise-reps", type=int, default=20, help="v021: --check-misclass の反復数(1 回が主モデル 1 回分の時間)")
    ap.add_argument("--audit-misclass", action="store_true", help="v022: check_misclass の実装(ソース)を行番号つきで書き出し、論文の説明の各主張に対応する記述があるかを表にする(何も実行しない)")
    ap.add_argument("--noise-min-count", type=int, default=30, help="v023: --check-misclass で、引いた真の類型の件数がこの値未満の反復は、その類型の統合から除く")
    ap.add_argument("--noise-prior", type=float, default=0.5, help="v021: 混同行列の各セルに足す Dirichlet の事前件数")
    ap.add_argument("--check-extra", nargs="?", const="all", default="", help="v025: 追加の確認(カンマ区切り。all / tost,meta,revalt,loo,age,field,subfield,aft,window,ratio,ratiodir,repo)。全行で推定する。ratio は v031: PMC と WoS の被引用数の比")
    ap.add_argument("--window-ages", default="3,5", help="v025: --check-extra window で、経過年数(調査日−出版日)がこの年以上の論文だけに絞る下限(年、カンマ区切り)")
    ap.add_argument("--aft-shift", type=float, default=0.5, help="v025: --check-extra aft の対数正規(shift 版)で、日数 0 の行を残すために足す値 log(日数+shift)")
    ap.add_argument("--check-misclass-ext", nargs="?", const="all", default="", help="v025: 誤分類の補正の拡張(カンマ区切り。all / strat / diff)。strat=雑誌のグループごとの混同行列、diff=誤分類が結果の大小と関連する場合(差異的)の感度分析")
    ap.add_argument("--reference-csv", default="", help="v025: 参照セット(人手の確認をした文)の CSV。1 行 1 文で、雑誌・人手(真)のラベル・予測ラベルの 3 列(--ref-cols)")
    ap.add_argument("--ref-cols", default="journal,human,pred", help="v025: --reference-csv の列名(雑誌,人手のラベル,予測ラベル の順にカンマ区切り)")
    ap.add_argument("--noise-strata", choices=["group", "journal", "two"], default="group", help="v025: strat の層。group=big3・MDPI 6 誌・Heliyon の 3 群(_jgroup)/ journal=雑誌ごと")
    ap.add_argument("--noise-shrink", type=float, default=10.0, help="v025: strat で、層の混同行列の各行に足す、全体の行の割合の重み(件数に換算)。大きいほど全体の混同行列に近づく")
    ap.add_argument("--diff-phi", default="0.5,1,2,3", help="v025: diff で試す φ(上位半分で誤分類のオッズを φ 倍、下半分で 1/φ 倍。カンマ区切り)")
    ap.add_argument("--diff-reps", type=int, default=5, help="v025: diff の φ ごとの反復数(1 反復が主モデル 1 回分の時間)")
    ap.add_argument("--fm-rates", default="0,0.0005,0.001,0.002,0.005,0.01,0.02,0.04", help="--check-misclass-ext fm: 人手が F の文が M と予測される確率(F→M の誤分類率)の候補をカンマ区切りで。参照セットの実測は 5/122 = 0.041")
    ap.add_argument("--fm-reps", type=int, default=5, help="--check-misclass-ext fm: 率ごとの反復数(1 反復が主モデル 1 回分の時間)")
    ap.add_argument("--repo-defs", default="FM,FMP", help="v055: --check-extra repo で 1 にする類型の組(カンマ区切り。FM=F+M / FMP=F+M+P / FMC=F+M+C / FMPC=F+M+P+C。v057 で FMC・FMPC を説明に追加、推定の仕組みは v055 と同じ)")
    ap.add_argument("--repo-suffix", default="", help="v057: --check-extra の出力ファイル名(check_extra_repo_<tag>.csv と check_extra_<tag>.txt)の末尾に付ける文字。組を分けて走らせるとき先の結果を上書きしないために使う(例 _fmc)")
    ap.add_argument("--repo-specs", default="all,pa,a", help="v055: --check-extra repo の比較対象(0 側)。all=1 の組以外すべて / 類型の文字の並び(pa=P と A、a=A だけ、など)")
    ap.add_argument("--repo-adj", default="main,fe", help="v055: --check-extra repo の調整。main=全共変量 / fe=雑誌+出版年の固定効果だけ")
    ap.add_argument("--repo-ref-pct", type=float, default=4.3, help="v055: --check-extra repo で、推定の変化率(%%)の 95%% 区間に入るかを見る参考値(%%)。既定 4.3(本文が引く PLOS OSI の値)")
    ap.add_argument("--tost-bounds", default="0.05,0.10", help="v025: TOST の同等の範囲 δ(率比が 1/(1+δ)〜1+δ。カンマ区切り)")
    ap.add_argument("--age-knots", type=int, default=4, help="v025: 経過年数スプラインの結び目の数")
    ap.add_argument("--revalt-cat", default="M", help="v025: --check-extra revalt で除く・基準に統合する類型")
    ap.add_argument("--check-df", action="store_true", help="DAS×雑誌・DAS×出版年の交互作用の自由度(df)の内訳を、NB を推定せずに調べる(論文 3.5節の df = 49)")
    ap.add_argument("--fetch-counts", action="store_true", help="v042: OpenAlex から --csv の DOI の counts_by_year・cited_by_count・publication_year を取得して --oa-counts-cache に追記する(取得済みは飛ばす。再開できる)")
    ap.add_argument("--merge-counts", action="store_true", help="v042: 取得済みの年次被引用数を --csv に結合して --oa-counts-out に書き出す(取得できる年の範囲の確認表も出す)")
    ap.add_argument("--oa-counts-cache", default="~/output_covariates_v27/openalex_counts.jsonl", help="v042: 年次被引用数の生データ(1 行 1 DOI の jsonl)")
    ap.add_argument("--oa-counts-out", default="~/output_covariates_v27/pmc_wos_v27_3llms_topic_counts.csv", help="v042: 結合後の CSV。--dv oa_*・--oa-suite の --csv の既定")
    ap.add_argument("--oa-last-year", type=int, default=2025, help="v042: 窓に使える最後の暦年(取得年は途中なので使わない)")
    ap.add_argument("--oa-cover-from", type=int, default=0, help="v042: 年次の値が使える最初の暦年(0 で自動判定。--merge-counts の確認表を見て決める)")
    ap.add_argument("--oa-field", default="field", help="v042: OpenAlex の分野のダミーを共変量に加える(none / field / domain / sub<N>)。--dv oa_*・--oa-suite で有効")
    ap.add_argument("--oa-suite", action="store_true", help="v042: 窓の違う従属変数(OpenAlex の出版年を含む k 年・出版後 j 年目、WoS・PMC)を同じ設定で推定し、DAS の率比・平均限界効果・LRT を並べる")
    ap.add_argument("--oa-windows", default="2,3,4,5", help="v042: --oa-suite の出版年を含む窓の年数(カンマ区切り)")
    ap.add_argument("--oa-lags", default="", help="v042: --oa-suite に加える出版後 j 年目の 1 年分(例 0,1,2,3)。空なら加えない")
    ap.add_argument("--oa-suite-extra", default="wos_TC,pmc_citedby_n", help="v042: --oa-suite に並べる既存の従属変数(wos_TC, pmc_citedby_n, oa_total。空で加えない)")
    ap.add_argument("--oa-sample", choices=["own", "common", "both"], default="both", help="v042: own=従属変数ごとに使える行 / common=すべての OpenAlex 窓が使える行 / both")
    ap.add_argument("--oa-lrt", choices=["on", "off"], default="on", help="v042: --oa-suite でグループごとの LRT(グループを外して再推定)も行う")
    ap.add_argument("--oa-report", action="store_true", help="v043: 既存の CSV から fig9(窓ごとの率比、own と common)と tab_oawin.tex・tab_oajournal.tex を作る(再推定なし)")
    ap.add_argument("--oa-report-dir", default="~/output_covariates_v27/analysis_oa_suite", help="v043: --oa-suite の出力フォルダ")
    ap.add_argument("--oa-journal-dir", default="~/output_covariates_v27/analysis_oa_c3", help="v043: 雑誌別(--dv oa_c3)の出力フォルダ")
    ap.add_argument("--oa-journal-dv", default="oa_c3", help="v043: 雑誌別の表の従属変数の名前(表示用)")
    ap.add_argument("--oa-wos-dir", default="~/output_covariates_v27/analysis", help="v043: WoS の主モデルの出力フォルダ(nb_by_journal.csv)")
    ap.add_argument("--oa-report-out", default="~/output_covariates_v27/paper/oa_report", help="v043: 図と tex の保存先")
    ap.add_argument("--run-label", default="", help="v044: 既定の出力先(analysis_oa_c3 など)に __<名前> を付けて別フォルダにする。--outdir を自分で指定したときは使われない")
    ap.add_argument("--no-archive", action="store_true", help="v044: 既存の結果がある出力先に上書きするとき、実行前の直下のファイルを _archive/<日時>/ にコピーする動作を止める")
    ap.add_argument("--oa-skip-existing", action="store_true", help="v042: --oa-suite で、出力がある従属変数・標本は飛ばす(中断後の再開用)")
    ap.add_argument("--classifier-report", action="store_true", help="v052: 参照セット(--reference-csv)でのカテゴリ別の分類性能(混同行列・適合率・再現率・F1・雑誌群別)と LaTeX の表を作る(回帰は走らせない)")
    ap.add_argument("--ref-lojo-col", default="", help="v052: --reference-csv の leave-one-journal-out の予測の列名(あれば交差検証の予測と並べて出す)")
    ap.add_argument("--clf-order", default="F,M,P,R,C,A,N", help="v052: --classifier-report の類型の並び(既定は表 2 の順)")
    ap.add_argument("--ref-id-col", default="PMCID", help="v053: --export-labels の reference_set.csv に入れる識別子の列名(--reference-csv にある場合だけ。大文字小文字は区別しない)")
    ap.add_argument("--clf-min-n", type=int, default=5, help="v053: --classifier-report の雑誌群別の表(tex と画面)で、人手の件数がこれ未満のセルを「--」にする")
    ap.add_argument("--clf-corpus", action="store_true", help="v052: --classifier-report で、--csv の DAS ラベルの割合から、予測が k のとき真も k である確率(PPV)と補正後の件数の点推定も出す")
    ap.add_argument("--export-labels", action="store_true", help="v052: DOI ごとの DAS ラベル(アンサンブルと 3 LLM)・参照セット・混同行列を Zenodo 用のフォルダにまとめる(WoS 由来の列は出さない)")
    ap.add_argument("--export-dir", default="", help="v052: --export-labels の保存先(既定 <outdir>/zenodo_deposit)")
    ap.add_argument("--export-id-cols", default="pmcid,doi", help="v052: --export-labels で出す識別子の列名(カンマ区切り、大文字小文字は区別しない。CSV にある列だけ)")
    ap.add_argument("--export-extra-cols", default="", help="v052: --export-labels で追加する列(カンマ区切り)。wos で始まる列は指定できない")
    ap.add_argument("--das-platform-report", action="store_true", help="v056: DAS の本文(das_text)から、P のうち識別子のないリポジトリらしい文の量を語句検索で概算する(回帰は走らせない)")
    ap.add_argument("--platform-extra", default="", help="v056: --das-platform-report で、データ置き場の名前に足す正規表現(例 'openneuro|synapse')")
    ap.add_argument("--platform-sample", type=int, default=60, help="v056: --das-platform-report で、人手の確認用に層ごとに抜く件数")
    ap.add_argument("--export-expect", type=int, default=661365, help="v052: --export-labels で、論文に書いた件数(違えば警告)")
    ap.add_argument("--export-public", action="store_true", help="v061: 公開用データ(論文単位の分析データ・参照セット・OpenAlex の生データ・コード・設定)を 1 つのフォルダに書き出す(WoS 由来の列と DAS の本文は出さない)")
    ap.add_argument("--export-max-mb", type=float, default=90.0, help="v061: --export-public で、論文単位のファイルがこのサイズ(MB)を超えたら雑誌ごとに分ける(GitHub は 100 MB まで)")
    ap.add_argument("--export-drop-cols", default="", help="v061: --export-public で出さない列(カンマ区切り、大文字小文字は区別しない)")
    ap.add_argument("--export-data-license", default="CC BY 4.0", help="v061: README_data.md に書くデータのライセンス")
    ap.add_argument("--wos-query-file", default="", help="v061: WoS の検索式(取得の手順)を書いたテキスト。wos_query.txt として入れる")
    ap.add_argument("--export-oa-topics-date", default="", help="v063: OpenAlex の分野(primary_topic)の取得日(例 \"2026-11-08 to 2026-11-09\")。取得記録 openalex_topics_meta.json がないときだけ、openalex_raw/ の説明ファイルと README_data.md に書く")
    ap.add_argument("--export-keep-wos-title", action="store_true", help="v064: --export-public で、title_len_source が wos の行の title_words_adj を PMC の語数に置き換えない(WoS 由来の値が入る)")
    ap.add_argument("--export-no-openalex-raw", action="store_true", help="v061: OpenAlex の生データを出さない")
    ap.add_argument("--export-no-code", action="store_true", help="v061: コード(この .py)を code/ に入れない")
    a = ap.parse_args()
    if a.shapley_nb_both:
        a.shapley_nb = True
        if a.dv != "wos_TC":
            sys.exit("--shapley-nb-both は --dv wos_TC(既定)のときだけ使えます(被引用数と査読期間を続けて実行するため)")
    a._outdir_default = (a.outdir == DEFAULT_OUT)   # v044: --outdir を自分で指定したか
    if a.oa_report:   # v043
        oa_report(a)
        return
    if (a.fetch_counts or a.merge_counts) and a.csv == DEFAULT_CSV:
        a.csv = a.oa_out   # v042: DOI を読む CSV の既定は topic 結合後の CSV
    if (_oa_dv(a.dv) or a.oa_suite) and a.csv == DEFAULT_CSV:
        a.csv = a.oa_counts_out   # v042: 年次の列がある結合後の CSV
    if a.oa_suite and a.outdir == DEFAULT_OUT:
        a.outdir = "~/output_covariates_v27/analysis_oa_suite"
    elif _oa_dv(a.dv) and a.outdir == DEFAULT_OUT:
        a.outdir = f"~/output_covariates_v27/analysis_{a.dv}"
    if a.oa_suite or _oa_dv(a.dv):
        _suffix_outdir(a)   # v044: --exposure・--run-label の印を付ける
    if _oa_dv(a.dv) and (a.robustness or a.robustness_only or a.paper_figs or a.paper_only or a.shapley_nb_both):
        sys.exit("OpenAlex の従属変数では --robustness・--paper-figs・--shapley-nb-both は使えません。窓の比較は --oa-suite を使ってください")
    if a.fetch_counts or a.merge_counts:   # v042
        if a.fetch_counts and not oa_fetch_counts(a):
            return
        if a.merge_counts:
            oa_merge_counts(a)
        return
    if a.oa_suite:   # v042
        oa_suite(a)
        return
    if a.audit_misclass:
        audit_misclass(a)
        return
    if a.pack_send:
        pack_send(a)
        return
    if a.classifier_report:   # v052
        classifier_report(a)
        return
    if a.export_public:   # v061
        export_public(a)
        return
    if a.export_labels:   # v052
        export_labels(a)
        return
    if a.das_platform_report:   # v056
        das_platform_report(a)
        return
    if a.check_journal_groups:
        check_journal_groups(a)
        return
    if a.check_section31:
        check_section31(a)
        return
    if a.check_sample:
        check_sample(a)
        return
    if a.check_fig6c:
        check_fig6c(a)
        return
    if _is_rv(a.dv):
        if a.review_as_iv:
            sys.exit("--dv review_days と --review-as-iv は同時に使えません(従属変数に査読期間を使うため)")
        a.target = "citations"       # 査読期間は主経路(log OLS・NB など)で分析する。別の査読期間 OLS は重複するので行わない
        if a.outdir == DEFAULT_OUT:
            a.outdir = DEFAULT_OUT_REVIEW
        ROBUST_RUNS.clear()
        ROBUST_RUNS.update(ROBUST_RUNS_REVIEW)
    _suffix_outdir(a)   # v044: 被引用数・査読期間の通常の実行にも印を付ける(oa は上で済み)
    if not a.robust_runs:
        a.robust_runs = ",".join(ROBUST_RUNS)
    if (a.robustness or a.robustness_only) and a.no_nb:
        sys.exit("--robustness には NB が必要です。--no-nb を外してください")
    if a.find_cols:
        head = pd.read_csv(os.path.expanduser(a.csv), nrows=0).columns
        hit = [c for c in head if re.search(a.find_cols, c, flags=re.I)]
        print(f"列は全部で {len(head)} 個。'{a.find_cols}' に合う列 {len(hit)} 個:")
        for c in hit:
            print("  ", c)
        return
    if a.fetch_topics or a.merge_topics or a.topics_pipeline:   # v039: OpenAlex の取得・結合・分析(分析用の出力フォルダは使わない)
        if a.topics_pipeline:
            topics_pipeline(a)
        else:
            if a.fetch_topics:
                oa_fetch_topics(a)
            if a.merge_topics:
                oa_merge_topics(a)
        return
    if a.supp_field:   # v040: 分野の係数の補足表(分析は行わない)
        supp_field_tables(a)
        return
    if a.labels:
        labels_report(a)
        return
    outdir = os.path.expanduser(a.outdir)
    _is_estimation = not (a.main_figs or a.paper_only or a.cb_compare or a.check_df or a.check_contrast or a.check_exposure
                          or a.check_zero or a.check_label_noise or a.check_misclass or a.check_misclass_ext or a.check_cluster or a.check_vif or a.check_adjust_sets or a.check_wos_gap
                          or a.check_extra or a.shapley_nb)
    if _is_estimation:
        _archive_existing(a, outdir)   # v044: 通常の再推定で上書きされる前の状態を退避
    os.makedirs(outdir, exist_ok=True)
    _write_runinfo(a, outdir)   # v044
    if a.check_exposure:
        check_exposure(a, outdir)
        return
    if a.check_zero:
        check_zero(a, outdir)
        return
    if a.check_label_noise:
        check_label_noise(a, outdir)
        return
    if a.check_misclass:
        check_misclass(a, outdir)
        return
    if a.check_misclass_ext:
        check_misclass_ext(a, outdir)
        return
    if a.check_cluster:
        check_cluster(a, outdir)
        return
    if a.check_vif:
        check_vif(a, outdir)
        return
    if a.check_adjust_sets:
        check_adjust_sets(a, outdir)
        return
    if a.check_wos_gap:
        check_wos_gap(a, outdir)
        return
    if a.check_extra:
        check_extra(a, outdir)
        return
    if a.shapley_nb:
        if a.shapley_nb_both:
            import copy
            for dv_, od_ in (("wos_TC", a.outdir), ("review_days", a.shapley_review_outdir)):
                b = copy.copy(a)
                b.dv = dv_
                if _is_rv(dv_):
                    b.review_as_iv, b.target = False, "citations"
                od = os.path.expanduser(od_)
                os.makedirs(od, exist_ok=True)
                print(f"\n===== NB 版 Shapley 分解: {dv_} -> {od} =====", file=sys.stderr, flush=True)
                shapley_nb(b, od)
            return
        shapley_nb(a, outdir)
        return
    if a.check_df:
        check_df(a, outdir)
        return
    if a.check_contrast:
        check_contrast(a, outdir)
        return
    if a.cb_compare:
        d_, _m, _dc, _r, _lg = prepare(a)
        print("\n".join(_lg))
        cb_compare(d_, a, outdir)
        return
    if a.main_figs:
        main_figures(a)
        return
    if a.paper_only:
        paper_outputs(a, outdir)
        return
    if a.robustness_only:
        run_robustness(a, outdir, False, [])
        if a.paper_figs:
            paper_outputs(a, outdir)
        return
    a.flow, a.model_info = {}, {}
    d, meta, das_cols, ref, log = prepare(a)
    if a.exposure != "off":
        attach_exposure(a, d, meta)   # v020
    flow_main = dict(a.flow)
    excl = {c.strip() for c in a.exclude.split(",") if c.strip()}
    base_ivs = [c for c in meta if c not in excl and c != "log_review" and c not in das_cols]
    lines = [f"DAS と被引用数・査読期間の分析 ({VERSION})", *log, f"DAS の基準: {ref} / 類型: {[ref] + [c[4:] for c in das_cols]}"]
    lines.append("雑誌別の件数: " + str(jshort(d.journal_key).value_counts().to_dict()))
    if a.target in ("both", "citations"):
        ivs = das_cols + base_ivs + (["log_review"] if a.review_as_iv else [])
        run_model(d, "log_tc", ivs, meta, das_cols, a, _tag(a.dv) + ("_with_review" if a.review_as_iv else ""), outdir, lines)
        if not a.no_rank:
            print("[進捗] 記述統計・順位検定", file=sys.stderr, flush=True)
            rank_tests(d, ref, a, outdir, lines.append)
        if not a.no_nb:
            print("[進捗] NB 回帰(行数が多いと数分〜数十分かかります)", file=sys.stderr, flush=True)
            nb_suite(d, meta, das_cols, base_ivs, ref, a, outdir, lines, log)
    if a.target in ("both", "review"):
        run_model(d, "log_review", das_cols + base_ivs, meta, das_cols, a, "review", outdir, lines)
    lines += sample_report(a, flow_main, dict(a.model_info))
    try:
        save_flow_csv(a, flow_main, dict(a.model_info), outdir)
    except Exception as e:
        print(f"[警告] sample_flow.csv を保存できませんでした: {e}", file=sys.stderr)
    lines.append("\n解釈の注意: 観察データの関連であり因果ではありません。雑誌×年の固定効果は雑誌ごとの DAS 方針や年の違いを除きますが、分野や論文の質の違いは残ります。")
    txt = "\n".join(lines)
    print(txt)
    with open(os.path.join(outdir, "summary.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    print("\n保存先:", outdir)
    if a.robustness:
        # 主分析が wos_TC・雑誌+年・全行・雑誌別 NB あり なら、その出力を base として使い回す
        reuse = (a.dv in ("wos_TC", "review_days") and a.nb_fe == "additive" and a.target in ("both", "citations") and not a.no_by_journal and not a.nb_sample)
        run_robustness(a, outdir, reuse, [])
    if a.paper_figs:
        paper_outputs(a, outdir)


if __name__ == "__main__":
    main()
