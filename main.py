import sys
import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
import pandas as pd
import io

# webhook
WEBHOOK = sys.argv[1]
# 締め切り時間
tmp_df = pd.read_csv(io.StringIO(sys.argv[2]), header=None)
TIME_DATA = tmp_df.iloc[:,0].apply(lambda x: pd.Series(x.split()))

webhook = DiscordWebhook(url=WEBHOOK)

def main():
    # 文字列生成
    send_list = send_string()
    embed = DiscordEmbed(title="残り時間表示 BOT",description="by Github Actions",color='ffa500')
    
    
    for row,list in enumerate(send_list):
        send_value = "期日 " + str(TIME_DATA.iat[row,1]) +"年"+ str(TIME_DATA.iat[row,2])+"月" + str(TIME_DATA.iat[row,3])+"日" + str(TIME_DATA.iat[row,4]) + "時"
        embed.add_embed_field(name=str(TIME_DATA.iat[row,0])+"まで後、"+list,value=send_value,inline=False)
    webhook.add_embed(embed)
    response = webhook.execute()

def cal_time(dead_time):
    dt_now = datetime.datetime.now() + datetime.timedelta(hours=9) #現在時刻取得(日本時間+9時間) 
    diff_time = dead_time - dt_now#現在時刻との差分
    days = diff_time.days
    seconds= diff_time.seconds
    hours= seconds//3600
    minutes= (seconds//60) % 60
    seconds= seconds - hours*3600 -minutes*60
    out_str = str(days)+'日 '+str(hours)+'時間 '+str(minutes)+'分 ' + str(seconds)+'秒'
    return out_str

def send_string():
    list = []
    for row in range(TIME_DATA.shape[0]):
        dead_time = datetime.datetime(year=int(TIME_DATA.iat[row,1]), month=int(TIME_DATA.iat[row,2]), day=int(TIME_DATA.iat[row,3]), hour=int(TIME_DATA.iat[row,4]))
        list.append(cal_time(dead_time))
    return list

main()