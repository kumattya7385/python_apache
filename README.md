# Apacheアクセスログカウントプログラム

このプログラムはapacheのアクセスログからリモートホスト、時間帯別にアクセス数を調べるためのプログラムです

# 環境

・python3.81  
・pandas  
・apache_log_parser

# ライブラリなどのインストール方法

```bash
pip install pandas

pip install apache_log_parser
```

# 実行方法
プログラムのディレクトリに移動後下のように実行する
```bash
python apache_research.py -f access_log1 access_log2 -s 2005/4/18 -l 2005/4/20
```
# オプション
-h --help オプションのヘルプを表示  
-f --fname 読み込みをするファイル名を指定。複数ファイル指定可能  
　デフォルトではaccess_logとなる ex: python apache_research.py -f access_log1 access_log2  
 -s --sdate 期間指定の最小の日を入力。入力形式は%Y/%M/%D ex: 2005/4/18  
 -l --ldate 期間指定の最終日を入力。入力形式は%Y/%M/%D ex: 2005/4/20
# Author

* 河合熊輔
* 工学院大学情報学部コンピュータ科学科
* kumaplayssoccer@icloud.com
