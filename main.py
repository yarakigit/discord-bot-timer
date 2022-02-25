import sys
import datetime
import discord
from discord.ext import tasks
import pandas as pd
import io


# 自分のBotのアクセストークンに置き換えてください
TOKEN = sys.argv[1]
# チャンネルID
CHANNEL_ID = int(sys.argv[2])
# 締め切り時間
tmp_df = pd.read_csv(io.StringIO(sys.argv[3]), header=None)
TIME_DATA = tmp_df.iloc[:,0].apply(lambda x: pd.Series(x.split()))

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

    #bot 起動時の処理
    channel = client.get_channel(CHANNEL_ID)
    send_list = send_string()
    embed = discord.Embed(title="残り時間表示 BOT",description="by Github Actions",color=discord.Colour.orange())
    for row,list in enumerate(send_list):
        send_value = "期日 " + str(TIME_DATA.iat[row,1]) +"年"+ str(TIME_DATA.iat[row,2])+"月" + str(TIME_DATA.iat[row,3])+"日" + str(TIME_DATA.iat[row,4]) + "時"
        embed.add_field(name=str(TIME_DATA.iat[row,0])+"まで後、"+list,value=send_value,inline=False) # フィールドを追加。
    await channel.send(embed=embed)
    exit(0)#終了
# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/timer」と発言したら「残り時間」が返る処理
    if message.content == '/timer':
        #発言したチャンネルのIDを取得
        channel_id = message.channel.id
        send_message = await message.channel.send("timer start")
        #発現したメッセージのIDを取得
        message_id= send_message.id
        send_message_every.start(channel_id,message_id) #定期実行するメソッドの後ろに.start()をつける

# 1秒間間隔で実行        
@tasks.loop(seconds=1)
async def send_message_every(channel_id,message_id):
    # 上位関数で取得したチャンネルのIDを使う
    channel = client.get_channel(channel_id)
    msg= await channel.fetch_message(message_id)
    send_list = send_string()
    embed = discord.Embed(title="残り時間表示 BOT",description="by Github Actions",color=discord.Colour.orange())
    for row,list in enumerate(send_list):
        send_value = "期日 " + str(TIME_DATA.iat[row,1]) +"年"+ str(TIME_DATA.iat[row,2])+"月" + str(TIME_DATA.iat[row,3])+"日" + str(TIME_DATA.iat[row,4]) + "時"
        embed.add_field(name=str(TIME_DATA.iat[row,0])+"まで後、"+list,value=send_value,inline=False) # フィールドを追加。
    await msg.edit(embed=embed)
        

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

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
