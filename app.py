# Linebot code
# 載入需要的模組

from __future__ import unicode_literals

from typing import List

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, PostbackEvent, LocationMessage, ImageMessage
import configparser
import flexmsg
import random
import json

from imgurpython import ImgurClient
import os, tempfile
import psycopg2


from datetime import datetime as dt
import time


app = Flask(__name__)
#存圖片
static_tmp_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'tmp')

"""
line-bot的基本資料 (建立一個config.ini的配置檔)

#Config.ini
[line-bot]
channel_access_token = oBtOINSU4GH40UshPoPtus6uEMdhz+YMGnsM74QPNRmEyfHK9I8rim/TiSpewb8AehJeELeetqtx3H/CQ5BSm2ZWJaUYrg7bMR21IJu7MSnW1skjtF+jwjK8ThQCFkFvJAwJraa4T4TLw+guvC/QTwdB04t89/1O/w1cDnyilFU=
channel_secret = 991ef928a89f1b5557e7a88954bceea4
"""

config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        print(body, signature)
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return 'OK'


# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":

        # Phoebe 愛唱歌
        pretty_note = '♫♪♬'
        pretty_text = ''

        for num in event.message.text:
            pretty_text += num
            pretty_text += random.choice(pretty_note)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=pretty_text)
        )


def echo(event):
    # [0] 總題數 [1:]目前題數
    progress_list_drug_refill = [5, 1, 2, 3, 4, 5]
    progress_list_drug_documentation = [7, 1, 2, 3, 4, 5, 6 ,7]
    event.message.text = event.message.text.replace("'", "‘")
    # progress_target
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        # 連結到heroku資料庫
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()

        if event.message.text == "領藥時間查詢":
            line_bot_api.reply_message(
                event.reply_token,
                flexmsg.drug_refill_calculation)

            print("prepare to calculate refill date")

            # 把只創建卻沒有寫入資料的列刪除
            postgres_delete_query = f"""DELETE FROM refill_cal_data WHERE (condition, user_id) = ('initial', '{event.source.user_id}');"""
            cursor.execute(postgres_delete_query)
            conn.commit()

            # 創建一列(condition = initial)
            postgres_insert_query = f"""INSERT INTO refill_cal_data (condition, user_id, today_date) VALUES ('initial', '{event.source.user_id}', 'str({event.source.dt}.datetime.today())');"""
            cursor.execute(postgres_insert_query)
            conn.commit()

            cursor.close()
            conn.close()

        elif event.message.text == "新增藥品記錄":
            line_bot_api.reply_message(
                event.reply_token,
                flexmsg.drug_category)

            print("prepare to document the drugs")

            # 把只創建卻沒有寫入資料的列刪除
            postgres_delete_query = f"""DELETE FROM drug_data WHERE (condition, user_id) = ('initial', '{event.source.user_id}');"""
            cursor.execute(postgres_delete_query)
            conn.commit()

            # 創建一列(condition = initial)
            postgres_insert_query = f"""INSERT INTO drug_data (condition, user_id, generic_name, description, photo) VALUES ('initial', '{event.source.user_id}', '無', '無', '無');"""
            cursor.execute(postgres_insert_query)
            conn.commit()

            cursor.close()
            conn.close()

        # 中途想結束輸入~delete, 把initial那列刪除
        elif event.message.text == "取消":
            postgres_select_query = f'''SELECT * FROM refill_cal_data WHERE user_id = '{event.source.user_id}' AND condition = 'initial';'''
            cursor.execute(postgres_select_query)
            data = cursor.fetchone()

            postgres_delete_query = f"""DELETE FROM refill_cal_data WHERE (condition, user_id) = ('initial', '{event.source.user_id}');"""
            cursor.execute(postgres_delete_query)
            conn.commit()

            postgres_select_query = f'''SELECT * FROM drug_data WHERE user_id = '{event.source.user_id}' AND condition = 'initial';'''
            cursor.execute(postgres_select_query)
            data_2 = cursor.fetchone()

            postgres_delete_query = f"""DELETE FROM drug_data WHERE (condition, user_id) = ('initial', '{event.source.user_id}');"""
            cursor.execute(postgres_delete_query)
            conn.commit()

            if data or data_2:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='取消成功')
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='無可取消的紀錄')
                )


        # 如果有創建了一列, 則接下來的資料繼續寫入
        else:
            postgres_select_query = f"""SELECT * FROM drug_data WHERE condition = 'initial' AND user_id = '{event.source.user_id}';"""
            cursor.execute(postgres_select_query)
            # 準備寫入藥品記錄資料的那一列
            data_2 = cursor.fetchone()
            print("data_2 :", data_2)
            column_all_drug = ['document_no', 'drug_category', 'drug_name','generic_name',
                                       'drug_prescription_date', 'duration','drug_amount', 'frequency', 'due_date'
                                       'description', 'photo', 'user_id']

            # drug_category = ['處方藥', '非處方藥品', '中草藥', '保健食品']


            postgres_select_query = f"""SELECT * FROM refill_cal_data WHERE condition = 'initial' AND user_id = '{event.source.user_id}';"""
            cursor.execute(postgres_select_query)
            data = cursor.fetchone()
            print('data = ', data)
            column_all_refill = ['record_no', 'today_date', 'visit_date', 'prescription_days', 'total_refill_number', 'last_refill_number',
                          'last_refill_date', 'second_refill_start_dt','second_refill_end_dt', 'third_refill_start_dt',
                          'third_refill_end_dt','valid_dt','user_id']


            if data:
                try:
                    progress_target = progress_list_drug_refill
                except:
                    progress_target = progress_list_drug_refill

                while None in data:  # 如果還沒輸入到最後一格, 則繼續詢問下一題
                    i = data.index(None)
                    print("i = ", i)
                    record = event.message.text
                    try:
                        postgres_select_query = f"""SELECT * FROM refill_cal_data WHERE condition = 'initial'AND user_id = '{event.source.user_id}';"""
                        cursor.execute(postgres_select_query)
                        data = cursor.fetchone()

                        postgres_update_query = f"""UPDATE refill_cal_data SET {column_all_refill[i]} = '{record}' WHERE condition = 'initial' AND user_id = '{event.source.user_id}';"""
                        cursor.execute(postgres_update_query)
                        conn.commit()
                    except:  # 如果使用者輸入的資料不符合資料庫的資料型態, 則輸入N/A
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="請重新輸入")
                        )

                        if None in data:
                            msg = flexmsg.flex_prescription(i, data, progress_target)
                            line_bot_api.reply_message(
                                event.reply_token,
                                msg)
                        elif None not in data:
                            postgres_select_query = f"""SELECT * FROM refill_cal_data WHERE user_id = '{event.source.user_id}' ORDER BY activity_no DESC;"""
                            cursor.execute(postgres_select_query)
                            data = cursor.fetchone()
                            msg = flexmsg.summary(data)
                            line_bot_api.reply_message(
                                event.reply_token,
                                msg
                                )

            # 如果已經到最後一格, condition改為finish, 回覆summary
            # elif None not in data:

                postgres_select_query = f"""SELECT * FROM refill_cal_data WHERE user_id = '{event.source.user_id}' ORDER BY activity_no DESC;"""
                cursor.execute(postgres_select_query)
                data = cursor.fetchone()
                msg = flexmsg.summary(data)
                line_bot_api.reply_message(
                    event.reply_token,
                    msg
                    )

                if event.message.text == '確認填寫無誤':

                    postgres_update_query = f"""UPDATE refill_cal_data SET condition = 'pending' WHERE condition = 'initial' AND user_id = '{event.source.user_id}';"""
                    cursor.execute(postgres_update_query)
                    conn.commit()

                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="請等待計算結果")
                    )

                    cursor.close()
                    conn.close()

                else:
                    column = event.message.text

                    if column in column_all_refill:
                        postgres_update_query = f"""UPDATE refill_cal_data SET {column} = Null WHERE condition = 'initial' AND user_id = '{event.source.user_id}';"""
                        cursor.execute(postgres_update_query)
                        conn.commit()
                        progress_target = [5, 4, 4, 4, 4, 4]
                        msg = flexmsg.flex_presciption(i,progress)
                        line_bot_api.reply_message(
                            event.reply_token,
                            msg
                        )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='請輸入您想修改的欄位')
                        )


            elif data_2:
                try:
                    if len(data_2[6])>0:
                        drug_progress_target = progress_list_drug_documentation
                except:
                    drug_progress_target = progress_list_drug_documentation

                if None in data_2:
                    j = data_2.index(None)
                    print("j = ", j)
                    if j == 8:
                        postgres_update_query = f"""UPDATE drug_data SET {column_all_drug[j]} = '無' WHERE condition = 'initial' AND user_id = '{event.source.user_id}';"""
                        cursor.execute(postgres_update_query)
                        conn.commit()
                        postgres_select_query = f"""SELECT * FROM drug_data WHERE user_id = '{event.source.user_id}' ORDER BY docu_no DESC;"""
                        cursor.execute(postgres_select_query)
                        data_2 = cursor.fetchone()
                        drug_info = flexmsg.drug_info_summary(data_2)
                        line_bot_api.reply_message(
                            event.reply_token,
                            [TextSendMessage(text="上傳失敗。"), drug_info]
                        )
                    else:
                        record = event.message.text
                        # 如果使用者輸入的資料不符合資料庫的資料型態, 則輸入N/A
                        try:
                            postgres_update_query = f"""UPDATE drug_data SET {column_all_drug[j]} = '{record}' WHERE condition = 'initial' AND user_id = '{event.source.user_id}';"""
                            cursor.execute(postgres_update_query)
                            conn.commit()
                        except:
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text="請重新輸入")
                            )
                        # 如果還沒輸入到最後一格, 則繼續詢問下一題
                        postgres_select_query = f"""SELECT * FROM drug_data WHERE condition = 'initial'AND user_id = '{event.source.user_id}';"""
                        cursor.execute(postgres_select_query)
                        data_2 = cursor.fetchone()

                        if None in data_2:
                            drug_info = flexmsg.flex_drug(j, data_2, drug_progress_target)
                            line_bot_api.reply_message(
                                event.reply_token,
                                drug_info)

                        # 如果已經到最後一格, condition改為finish, 回覆summary，
                        elif None not in data_2:

                            postgres_select_query = f"""SELECT * FROM group_data WHERE user_id = '{event.source.user_id}' ORDER BY activity_no DESC;"""
                            cursor.execute(postgres_select_query)
                            data_2 = cursor.fetchone()
                            drug_info = flexmsg.drug_info_summary(data_2)
                            line_bot_api.reply_message(
                                event.reply_token,
                                drug_info
                            )

                else:
                    if event.message.text == '確認紀錄':
                        postgres_update_query = f"""UPDATE drug_data SET condition = 'pending' WHERE condition = 'initial' AND user_id = '{event.source.user_id}';"""
                        cursor.execute(postgres_update_query)
                        conn.commit()

                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="完成紀錄")
                        )

                        cursor.close()
                        conn.close()

                    else:
                        column_all_drug = event.message.text
                        if column in column_all_drug:
                            postgres_update_query = f"""UPDATE drug_data SET {column} = Null WHERE condition = 'initial' AND user_id = '{event.source.user_id}';"""
                            cursor.execute(postgres_update_query)
                            conn.commit()
                            drug_progress_target = [7, 6, 6, 6, 6, 6, 6, 6 ]
                            drug_info = flexmsg.flex_drug(column, data_2, drug_progress_target)
                            line_bot_api.reply_message(
                                event.reply_token,
                                drug_info
                            )
                        else :
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text = '請輸入您想修改的欄位')
                            )



@handler.add(MessageEvent, message=ImageMessage)
def pic(event):
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    postgres_select_query = f"""SELECT * FROM drug_data WHERE condition = 'initial' AND user_id = '{event.source.user_id}';"""
    cursor.execute(postgres_select_query)
    data_2 = cursor.fetchone()
    if data_2:
        j = data_2.index(None)
        print("i =", j)
        if j == 12:
            column_all_drug = ['document_no', 'drug_category', 'drug_name', 'generic_name', 'drug_prescription_date',
                               'duration', 'drug_amount', 'frequency', 'due_date',                                                                                                'description', 'photo',
                               'user_id']
            # 把圖片存下來並傳上去
            ext = 'jpg'
            message_content = line_bot_api.get_message_content(event.message.id)
            with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
                for chunk in message_content.iter_content():
                    tf.write(chunk)
                tempfile_path = tf.name

            dist_path = tempfile_path + '.' + ext
            dist_name = os.path.basename(dist_path)
            os.rename(tempfile_path, dist_path)

            try:
                config = configparser.ConfigParser()
                config.read('config.ini')
                client = ImgurClient(config.get('imgur', 'client_id'), config.get('imgur', 'client_secret'),
                                     config.get('imgur', 'access_token'), config.get('imgur', 'refresh_token'))
                con = {
                    'album': config.get('imgur', 'album_id'),
                    'name': f'{event.source.user_id}_{data_2[2]}',
                    'title': f'{event.source.user_id}_{data_2[2]}',
                    'description': f'{event.source.user_id}_{data_2[2]}'
                }
                path = os.path.join('static', 'tmp', dist_name)
                image = client.upload_from_path(path, config=con, anon=False)
                print("path = ", path)
                os.remove(path)
                print("image = ", image)
                # 把圖片網址存進資料庫
                postgres_update_query = f"""UPDATE group_data SET {column_all_drug[j]} = '{image['link']}' WHERE condition = 'initial' AND user_id = '{event.source.user_id}';"""
                cursor.execute(postgres_update_query)
                conn.commit()

                msg = [TextSendMessage(text='上傳成功')]

                postgres_select_query = f"""SELECT * FROM group_data WHERE user_id = '{event.source.user_id}' ORDER BY activity_no DESC;"""
                cursor.execute(postgres_select_query)
                data = cursor.fetchone()
                if None not in data:
                    msg.append(flexmsg.summary(data))

                line_bot_api.reply_message(
                    event.reply_token,
                    msg
                )
            except:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='上傳失敗'))

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="現在不用傳圖片給我")
        )
    return 0


@app.route('/static/<path:path>')
def send_static_content(path):
    return send_from_directory('static', path)


if __name__ == "__main__":
    app.run()