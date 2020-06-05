import apache_log_parser as par
import pandas as pd
import argparse
import datetime as dt
from pprint import pprint

#オプション引数とコマンドライン引数の定義
def get_args():
  parser = argparse.ArgumentParser(description='This is an Apache analysis application')
  parser.add_argument('-f', '--fname', default=['access_log'], nargs='*', type=str, help='This is input of file name')
  parser.add_argument('-s', '--sdate', default='', type=str, help='This is Start date of search period　example:2005/4/19')
  parser.add_argument('-l', '--ldate', default='', type=str, help='This is last date of search period example:2005/4/20')

  return parser.parse_args()

def main():
  args = get_args() #実行時のそれぞれの引数を保持

  #期間の指定のエラー表示
  if (not args.sdate == "" and args.ldate == ""):
    return print('ERROR: 指定期間の最終日を入力してください') 
  elif (args.sdate == "" and not args.ldate == ""):
    return print('ERROR: 指定器官の最初の日を入力してください')

  logformat="%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\""
  list_df = pd.DataFrame( columns = ['access_time','remote_host'])#リモートホストとアクセス時間のテーブル
  flag = 0 #テーブルが容量が大きくなる場合はフラグを1にする
  
  #複数ファイルをそれぞれ処理する
  for a in range(len(args.fname)):
    with open(args.fname[a]) as f:
      #メモリ節約のため1行ずつ処理
      for line in f:
        line = line.strip() #改行の削除

        #ログから日時とリモートホストを抽出してテーブルに保存
        line_parser = par.make_parser(logformat)
        log_line_data=line_parser(line)
        log_time = log_line_data['time_received_datetimeobj']
        log_host = log_line_data['remote_host']
        tmp_se = pd.Series( [ log_time, log_host], index=list_df.columns )
        list_df = list_df.append( tmp_se, ignore_index=True )

        list_df['access_time'] = list_df['access_time'].dt.round("H") #ログの時間を丸める(分と秒をまるめる)
        list_df['access_time'] = pd.to_datetime(list_df['access_time']) #指定期間で抽出できるように型変換

        #指定期間で抽出
        if (not args.sdate =="" and not args.ldate ==""):
          sdate = dt.datetime.strptime(args.sdate, '%Y/%m/%d')
          ldate = dt.datetime.strptime(args.ldate, '%Y/%m/%d')
          ldate = ldate + dt.timedelta(days=1)
          list_df = list_df[(list_df['access_time'] >= dt.datetime(sdate.year,sdate.month,sdate.day)) & (list_df['access_time'] < dt.datetime(ldate.year,ldate.month,ldate.day))]

        #テーブルのレコードが多い時の処理
        if len(list_df) >= 10000:
          list_store_remote = list_df.groupby('remote_host').size()
          list_store_time = list_df.groupby('access_time').size()
          if flag == 0:
            result_store_remote = list_store_remote
            result_store_time = list_store_time
            flag = 1
          else:
            result_store_remote = pd.concat([result_store_remote, list_store_remote])
            result_store_remote = result_store_remote.groupby('remote_host').sum()
            result_store_time = pd.concat([result_store_time, list_store_time])
            result_store_time = result_store_time.groupby('access_time').sum()
          list_df = list_df[:0]

  #結果を出力
  if (not args.sdate == "" and not args.ldate == ""):
    print(args.sdate + "から" + args.ldate + "までの各アクセス数")
  else:
    print('全期間の各アクセス数')
  if flag == 0:
    print('==================リモートホスト毎のアクセス数=================')
    print(list_df.groupby('remote_host').size())
    print('===============================================================')
    print('')
    print('==================時間帯毎(1時間毎)のアクセス数==================')
    print(list_df.groupby('access_time').size())
    print('=================================================================')
  else:
    print('==================リモートホスト毎のアクセス数=================')
    print(result_store_remote)
    print('===============================================================')
    print('')
    print('==================時間帯毎(1時間毎)のアクセス数==================')
    print(result_store_time)
    print('=================================================================')


if __name__ == '__main__':
  main()