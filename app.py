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


#check upload
@app.route("/")
def hello():
    return "Hello, world!"

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

@handler.add(MessageEvent, message=TextMessage)
def echo(event):
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a drugtaking-linebot').read()[:-1]
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()

        #藥品紀錄
        if event.message.text == "新增藥品紀錄":
            line_bot_api.reply_message(
                event.reply_token,
                flexmsg.drug_category)
            print("prepare to document the drugs")
            # 把只創建卻沒有寫入資料的列刪除
            postgres_delete_query = f"""DELETE FROM drug_data WHERE (condition, user_id) = ('initial', '{event.source.user_id}');"""
            cursor.execute(postgres_delete_query)
            conn.commit()

            # 創建一列(condition = initial)
            postgres_insert_query = f"""INSERT INTO drug_data (condition, user_id, generic_name, photo, description) VALUES ('initial', '{event.source.user_id}', '無', '無', '無');"""
            cursor.execute(postgres_insert_query)
            conn.commit()

            cursor.close()
            conn.close()


        # 中途想結束輸入~delete, 把initial那列刪除
        elif event.message.text == "取消":

            postgres_select_query = f'''SELECT * FROM drug_data WHERE user_id = '{event.source.user_id}' AND condition = 'initial';'''
            cursor.execute(postgres_select_query)
            data_2 = cursor.fetchone()

            postgres_delete_query = f"""DELETE FROM drug_data WHERE (condition, user_id) = ('initial', '{event.source.user_id}');"""
            cursor.execute(postgres_delete_query)
            conn.commit()


            if data_2 :
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='取消成功')
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='無可取消的紀錄')
                )

        #領藥時間查詢
        elif event.message.text == "領藥時間查詢":
            line_bot_api.reply_message(
                event.reply_token,
                flexmsg.drug_refill_calculation)
            print("prepare to calculate refill date")

            # 把只創建卻沒有寫入資料的列刪除
            postgres_delete_query = f"""DELETE FROM refill_cal_data WHERE (condition, user_id) = ('initial', '{event.source.user_id}');"""
            cursor.execute(postgres_delete_query)
            conn.commit()

            # 創建一列(condition = initial)
            postgres_insert_query = f"""INSERT INTO refill_cal_data (condition, user_id, second_refill_start_dt, second_refill_end_dt, third_refill_start_dt, third_refill_end_dt) VALUES ('initial', '{event.source.user_id}', '無', '無', '無', '無');"""
            cursor.execute(postgres_insert_query)
            conn.commit()

            cursor.close()
            conn.close()

            DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a drugtaking-linebot').read()[:-1]
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            cursor = conn.cursor()


        else:
            DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a drugtaking-linebot').read()[:-1]
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            cursor = conn.cursor()

            #藥品紀錄
            postgres_select_query = f"""SELECT * FROM drug_data WHERE condition = 'initial' AND user_id = '{event.source.user_id}';"""
            cursor.execute(postgres_select_query)
            data_2 = cursor.fetchone()
            print("data_2 :", data_2)
            column_all_drug = ['document_no', 'drug_category', 'drug_name', 'drug_amount', 'drug_frequency',
                                       'prescription_date', 'duration', 'due_date', 'generic_name'
                                       'description', 'photo', 'condition', 'user_id']


            if data_2:
                # [0] 總題數 [1:]目前題數
                progress_list_drug = [5, 1, 2, 3, 4, 5]
                if None in data_2:

                    j = data_2.index(None)
                    print("j = ", j)

                    if j == 10:
                        postgres_update_query = f"""UPDATE drug_data SET {column_all_drug[j]} = '無' WHERE condition = 'initial' AND user_id = '{event.source.user_id}';"""
                        cursor.execute(postgres_update_query)
                        conn.commit()
                        postgres_select_query = f"""SELECT * FROM group_data WHERE user_id = '{event.source.user_id}' ORDER BY document_no DESC;"""
                        cursor.execute(postgres_select_query)
                        data_2 = cursor.fetchone()
                        drug_info=flexmsg.drug_info_summary(data_2)
                        line_bot_api.reply_message(
                            event.reply_token,
                            [TextSendMessage(text = "上傳失敗。"), drug_info]
                        )
                    else:
                        record = event.message.text

                        try:
                            postgres_update_query = f"""UPDATE drug_data SET {column_all_drug[j]} = '{record}' WHERE condition = 'initial' AND user_id = '{event.source.user_id}';"""
                            cursor.execute(postgres_update_query)
                            conn.commit()
                            print("data_2 :", data_2)
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
                            progress_list_drug = [5, 1, 2, 3, 4, 5]

                            drug_info = flexmsg.flex_drug(j, progress_list_drug)
                            line_bot_api.reply_message(
                                event.reply_token,
                                drug_info)
                            print("data_2 :", data_2)


                        # 如果已經到最後一格, condition改為finish, 回覆summary，
                        elif None not in data_2:
                            postgres_select_query = f"""SELECT * FROM drug_data WHERE user_id = '{event.source.user_id}' ;"""
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
                            TextSendMessage(text="紀錄成功")
                        )

                        cursor.close()
                        conn.close()
                    else:
                        column = event.message.text

                        if column in column_all_drug:
                            postgres_update_query = f"""UPDATE group_data SET {column} = Null WHERE condition = 'initial' AND user_id = '{event.source.user_id}';"""
                            cursor.execute(postgres_update_query)
                            conn.commit()
                            progress_list_drug_all = [10, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
                            drug_info = flexmsg.flex_drug(column, progress_list_drug_all)
                            line_bot_api.reply_message(
                                event.reply_token,
                                drug_info
                            )
                        else:
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text='請輸入您想修改的欄位')
                            )
            # elif data:
            #     # [0] 總題數 [1:]目前題數
            #     progress_list_refill = [5, 1, 2, 3, 4, 5]
            #     if None in data:
            #
            #         i = data.index(None)
            #         print("i = ", i)
            #
            #         if event.message.text == '一般處方箋':
            #             line_bot_api.reply_message(
            #                 event.reply_token,
            #                 TextSendMessage(text="請在看診3日內領取")
            #             )
            #             postgres_delete_query = f"""DELETE FROM refill_cal_data WHERE (condition, user_id) = ('initial', '{event.source.user_id}');"""
            #             cursor.execute(postgres_delete_query)
            #             conn.commit()
            #
            #
            #         else:
            #             record = event.message.text
            #
            #             try:
            #                 postgres_update_query = f"""UPDATE refill_cal_data SET {column_all_refill[i]} = '{record}' WHERE condition = 'initial' AND user_id = '{event.source.user_id}';"""
            #                 cursor.execute(postgres_update_query)
            #                 conn.commit()
            #                 print("data :", data)
            #             except:
            #                 line_bot_api.reply_message(
            #                     event.reply_token,
            #                     TextSendMessage(text="請重新輸入")
            #                 )
            #             # 如果還沒輸入到最後一格, 則繼續詢問下一題
            #
            #             postgres_select_query = f"""SELECT * FROM refill_cal_data WHERE condition = 'initial'AND user_id = '{event.source.user_id}';"""
            #             cursor.execute(postgres_select_query)
            #             data = cursor.fetchone()
            #
            #             if None in data:
            #                 progress_list_refill = [5, 1, 2, 3, 4, 5]
            #
            #                 msg = flexmsg.flex_prescription(i, progress_list_refill)
            #                 line_bot_api.reply_message(
            #                     event.reply_token,
            #                     msg)
            #                 print("data :", data)
            #
            #
            #             # 如果已經到最後一格, condition改為finish, 回覆summary，
            #             elif None not in data:
            #                 postgres_select_query = f"""SELECT * FROM refill_cal_data WHERE user_id = '{event.source.user_id}' ;"""
            #                 cursor.execute(postgres_select_query)
            #                 data = cursor.fetchone()
            #
            #                 msg = flexmsg.summary(data)
            #                 line_bot_api.reply_message(
            #                     event.reply_token,
            #                     msg
            #                 )
            #     else:
            #
            #         if event.message.text == '確認填寫無誤':
            #             postgres_select_query = f"""SELECT * FROM refill_cal_data WHERE user_id = '{event.source.user_id}' ;"""
            #             cursor.execute(postgres_select_query)
            #             data = cursor.fetchone()
            #
            #             # valid_date = drug_refill_cal(data)
            #
            #             postgres_update_query = f"""UPDATE refill_cal_data SET valid_dt = DATE_ADD({data[2]}, INTERVAL ({data[3]}*{data[4]}) DAY) and condition = 'pending' WHERE condition = 'initial' AND user_id = '{event.source.user_id}';"""
            #             cursor.execute(postgres_update_query)
            #             conn.commit()
            #
            #
            #             line_bot_api.reply_message(
            #                 event_2.reply_token,
            #                 TextSendMessage(text="請等待計算結果")
            #             )
            #
            #             cursor.close()
            #             conn.close()
            #         else:
            #             column = event.message.text
            #
            #             if column in column_all_refill:
            #                 postgres_update_query = f"""UPDATE refill_cal_data SET {column} = Null WHERE condition = 'initial' AND user_id = '{event.source.user_id}';"""
            #                 cursor.execute(postgres_update_query)
            #                 conn.commit()
            #                 progress_list_refill_all = [5, 4, 4, 4, 4, 4]
            #                 msg = flexmsg.flex_prescription(column, progress_list_refill_all)
            #                 line_bot_api.reply_message(
            #                     event.reply_token,
            #                     msg
            #                 )
            #             else:
            #                 line_bot_api.reply_message(
            #                     event.reply_token,
            #                     TextSendMessage(text='請輸入您想修改的欄位')
            #                 )
@handler.add(MessageEvent, message=TextMessage)
def drug_refill_event(event_2):
    if event_2.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a drugtaking-linebot').read()[:-1]
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()


        if  event_2.message.text == "領藥時間查詢":
            line_bot_api.reply_message(
                event_2.reply_token,
                flexmsg.drug_refill_calculation)
            print("prepare to calculate refill date")

            # 把只創建卻沒有寫入資料的列刪除
            postgres_delete_query = f"""DELETE FROM refill_cal_data WHERE (condition, user_id) = ('initial', '{event_2.source.user_id}');"""
            cursor.execute(postgres_delete_query)
            conn.commit()

            # 創建一列(condition = initial)
            postgres_insert_query = f"""INSERT INTO refill_cal_data (condition, user_id, second_refill_start_dt, second_refill_end_dt, third_refill_start_dt, third_refill_end_dt) VALUES ('initial', '{event_2.source.user_id}', '無', '無', '無', '無');"""
            cursor.execute(postgres_insert_query)
            conn.commit()

            cursor.close()
            conn.close()

        # 中途想結束輸入~delete, 把initial那列刪除
        elif event_2.message.text == "取消":
            postgres_select_query = f'''SELECT * FROM refill_cal_data WHERE user_id = '{event_2.source.user_id}' AND condition = 'initial';'''
            cursor.execute(postgres_select_query)
            data = cursor.fetchone()

            postgres_delete_query = f"""DELETE FROM refill_cal_data WHERE (condition, user_id) = ('initial', '{event_2.source.user_id}');"""
            cursor.execute(postgres_delete_query)
            conn.commit()


            if data:
                line_bot_api.reply_message(
                    event_2.reply_token,
                    TextSendMessage(text='取消成功')
                )
            else:
                line_bot_api.reply_message(
                    event_2.reply_token,
                    TextSendMessage(text='無可取消的紀錄')
                )

        else:
            DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a drugtaking-linebot').read()[:-1]
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            cursor = conn.cursor()


            #領藥時間查詢
            postgres_select_query = f"""SELECT * FROM refill_cal_data WHERE condition = 'initial' AND user_id = '{event_2.source.user_id}';"""
            cursor.execute(postgres_select_query)
            data = cursor.fetchone()
            print("data :", data)
            column_all_refill = ['document_no', 'prescription_category','visit_date', 'prescription_days', 'total_refill_number',
                                 'last_refill_number', 'last_refill_date', 'today_date', 'second_refill_start_dt',
                                 'second_refill_end_dt', 'third_refill_start_dt',
                                 'third_refill_end_dt', 'valid_dt', 'user_id']

            if data:
                # [0] 總題數 [1:]目前題數
                progress_list_refill = [5, 1, 2, 3, 4, 5]
                if None in data:

                    i = data.index(None)
                    print("i = ", i)

                    if event_2.message.text == '一般處方箋':
                        line_bot_api.reply_message(
                            event_2.reply_token,
                            TextSendMessage(text="請在看診3日內領取")
                        )
                        postgres_delete_query = f"""DELETE FROM refill_cal_data WHERE (condition, user_id) = ('initial', '{event_2.source.user_id}');"""
                        cursor.execute(postgres_delete_query)
                        conn.commit()


                    else:
                        record = event_2.message.text

                        try:
                            postgres_update_query = f"""UPDATE refill_cal_data SET {column_all_refill[i]} = '{record}' WHERE condition = 'initial' AND user_id = '{event_2.source.user_id}';"""
                            cursor.execute(postgres_update_query)
                            conn.commit()
                            print("data :", data)
                        except:
                            line_bot_api.reply_message(
                                event_2.reply_token,
                                TextSendMessage(text="請重新輸入")
                            )
                        # 如果還沒輸入到最後一格, 則繼續詢問下一題

                        postgres_select_query = f"""SELECT * FROM refill_cal_data WHERE condition = 'initial'AND user_id = '{event_2.source.user_id}';"""
                        cursor.execute(postgres_select_query)
                        data = cursor.fetchone()

                        if None in data:
                            progress_list_refill = [5, 1, 2, 3, 4, 5]

                            msg = flexmsg.flex_prescription(i, progress_list_refill)
                            line_bot_api.reply_message(
                                event_2.reply_token,
                                msg)
                            print("data :", data)


                        # 如果已經到最後一格, condition改為finish, 回覆summary，
                        elif None not in data:
                            postgres_select_query = f"""SELECT * FROM refill_cal_data WHERE user_id = '{event_2.source.user_id}' ;"""
                            cursor.execute(postgres_select_query)
                            data = cursor.fetchone()

                            msg = flexmsg.summary(data)
                            line_bot_api.reply_message(
                                event_2.reply_token,
                                msg
                            )
                else:

                    if event_2.message.text == '確認填寫無誤':
                        postgres_select_query = f"""SELECT * FROM refill_cal_data WHERE user_id = '{event_2.source.user_id}' ;"""
                        cursor.execute(postgres_select_query)
                        data = cursor.fetchone()

                        # valid_date = drug_refill_cal(data)

                        valid_date = {data[2]}+ datetime.timedelta(days= ({data[3]} * {data[4]}))

                        postgres_update_query = f"""UPDATE refill_cal_data SET valid_dt = {valid_date} , condition = 'calculating' WHERE condition = 'initial' AND user_id = '{event_2.source.user_id}';"""
                        cursor.execute(postgres_update_query)
                        conn.commit()


                        line_bot_api.reply_message(
                            event_2.reply_token,
                            TextSendMessage(text=drug_refill_cal(data))
                        )

                        cursor.close()
                        conn.close()

                    else:
                        column = event_2.message.text

                        if column in column_all_refill:
                            postgres_update_query = f"""UPDATE refill_cal_data SET {column} = Null WHERE condition = 'initial' AND user_id = '{event_2.source.user_id}';"""
                            cursor.execute(postgres_update_query)
                            conn.commit()
                            progress_list_refill_all = [5, 4, 4, 4, 4, 4]
                            msg = flexmsg.flex_prescription(column, progress_list_refill_all)
                            line_bot_api.reply_message(
                                event_2.reply_token,
                                msg
                            )
                        else:
                            line_bot_api.reply_message(
                                event_2.reply_token,
                                TextSendMessage(text='請輸入您想修改的欄位')
                            )
def drug_refill_cal(data):
    today_dt = data[8]
    visit_date = data[2]
    prescription_days = int(data[3])
    total_refill_number = int(data[4])
    last_refill_number = int(data[5])
    last_refill_date = data[6]

    time_delta_all = datetime.timedelta(days=int(prescription_days * total_refill_number))
    valid_dt = visit_date + time_delta_all  # 處方箋的有效期限

    time_delta = datetime.timedelta(days=prescription_days)
    second_refill_start_dt = last_refill_date + time_delta - datetime.timedelta(days=int(10))  # 第二次領藥起始日
    second_refill_end_dt = last_refill_date + time_delta  # 第二次領藥截止日

    if today_dt > valid_dt:
        result = ('處方已過期，請重新掛號看診，領取新的處方箋')

    elif total_refill_number == 2:  # 共 2 次
        if today_dt < second_refill_start_dt:
            result = ('現在還不能領喔！''建議領藥時間：{}年 {}月 {}日'.format(second_refill_start_dt.year, second_refill_start_dt.month,
                                                            second_refill_start_dt.day) + '~{}年 {}月 {}日'.format(
                second_refill_end_dt.year,
                second_refill_end_dt.month,
                second_refill_end_dt.day))

        elif second_refill_start_dt <= today_dt <= second_refill_end_dt:
            result = ('現在可以領！請您在 {}年 {}月 {}日前領取。'.format(second_refill_end_dt.year, second_refill_end_dt.month,
                                                         second_refill_end_dt.day))
        elif second_refill_end_dt <= today_dt <= valid_dt:
            result = ('咦！請您確認是否按時服藥，並盡快領藥。務必在 {}年 {}月 {}日前領取。'.format(valid_dt.year, valid_dt.month, valid_dt.day))
        elif last_refill_number == 2:  # 2 times
            result = ('所有處方已領取完。請重新掛號看診。')

    elif total_refill_number == 3:  # 共 3 次
        if last_refill_number == 1:  # 只領第一次
            if today_dt < second_refill_start_dt:
                result = ('現在還不能領喔！' + '建議領藥時間：{}年 {}月 {}日'.format(second_refill_start_dt.year,
                                                                    second_refill_start_dt.month,
                                                                    second_refill_start_dt.day) + '~{}年 {}月 {}日'.format(
                    second_refill_end_dt.year,
                    second_refill_end_dt.month,
                    second_refill_end_dt.day))
            elif second_refill_start_dt <= today_dt <= second_refill_end_dt:
                result = ('現在可以領！請您在' + second_refill_end_dt + '前領取。')

            else:
                result = ('咦！請您確認是否按時服藥，並盡快領藥。')

        elif last_refill_number == 2:  # 已領 2次
            third_refill_start_dt = last_refill_date + time_delta - datetime.timedelta(days=int(10))  # 第三次領藥起始日
            third_refill_end_dt = last_refill_date + time_delta  # 第三次領藥截止日
            if today_dt < third_refill_start_dt:
                result = ('現在還不能領喔！' + '建議領藥時間：{}年 {}月 {}日'.format(third_refill_start_dt.year,
                                                                   third_refill_start_dt.month,
                                                                   third_refill_start_dt.day) + '~{}年 {}月 {}日'.format(
                    third_refill_end_dt.year,
                    third_refill_end_dt.month,
                    third_refill_end_dt.day))
            elif third_refill_start_dt <= today_dt <= third_refill_end_dt:
                result = ('現在可以領！請您在請您在 {}年 {}月 {}日前領取。'.format(third_refill_end_dt.year, third_refill_end_dt.month,
                                                                third_refill_end_dt.day))
            else:
                result = ('咦！請您確認是否按時服藥，並盡快領藥。務必在 {}年 {}月 {}日前領取。'.format(valid_dt.year, valid_dt.month, valid_dt.day))
    elif last_refill_number == 3:
        result = ('所有處方已領取完。請重新掛號看診。')

    return result






@handler.add(MessageEvent, message=ImageMessage)
def pic(event):
    DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a drugtaking-linebot').read()[:-1]
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    # DATABASE_URL = os.environ['DATABASE_URL']
    # conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    # cursor = conn.cursor()
    postgres_select_query = f"""SELECT * FROM drug_data WHERE condition = 'initial' AND user_id = '{event.source.user_id}';"""
    cursor.execute(postgres_select_query)
    data_2 = cursor.fetchone()
    if data_2:
        j = data_2.index(None)
        print("j =", j)
        if j == 10:
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
                    'name': f'{event.source.user_id}_{data_2[1]}',
                    'title': f'{event.source.user_id}_{data_2[1]}',
                    'description': f'{event.source.user_id}_{data_2[1]}'
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

                drug_info = [TextSendMessage(text='上傳成功')]

                postgres_select_query = f"""SELECT * FROM group_data WHERE user_id = '{event.source.user_id}' ORDER BY activity_no DESC;"""
                cursor.execute(postgres_select_query)
                data_2 = cursor.fetchone()
                if None not in data_2:
                    drug_info.append(flexmsg.drug_info_summary(data_2))

                line_bot_api.reply_message(
                    event.reply_token,
                    drug_info
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


# 處理postback 事件，例如datetime picker
@handler.add(PostbackEvent)
def documentation(event):
    progress_list_drug = [5, 1, 2, 3, 4, 5]

    # DATABASE_URL = os.environ['DATABASE_URL']
    # conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    # cursor = conn.cursor()
    DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a drugtaking-linebot').read()[:-1]
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    postgres_select_query = f"""SELECT * FROM drug_data WHERE condition = 'initial' AND user_id = '{event.source.user_id}';"""
    cursor.execute(postgres_select_query)
    data_2 = cursor.fetchone()
    postback_data_drug = event.postback.data_2

    progress_list_drug = [5, 1, 2, 3, 4, 5]

    postgres_select_query = f"""SELECT * FROM refill_cal_data WHERE condition = 'initial' AND user_id = '{event.source.user_id}';"""
    cursor.execute(postgres_select_query)
    data = cursor.fetchone()
    postback_data_refill = event.postback.data


    # 查看藥品紀錄 (藥品名稱、地點、時間、費用、已報名人數)
    if "藥品紀錄" in postback_data_drug:
        # 把只創建卻沒有寫入資料完成的列刪除
        postgres_delete_query = f"""DELETE FROM drug_data WHERE (condition, user_id) = ('initial', '{event.source.user_id}');"""
        cursor.execute(postgres_delete_query)
        conn.commit()

        postgres_select_query = f"""SELECT * FROM drug_data WHERE user_id = '{event.source.user_id}' AND due_date >= '{dt.date.today()}' ORDER BY prescription_date ASC;"""
        cursor.execute(postgres_select_query)
        drug_data = cursor.fetchall()

        print("drug_data = ", drug_data)

        drug_info = flexmsg.DrugList(drug_data)
        line_bot_api.reply_message(
            event.reply_token,
            drug_info
        )

    elif "慢箋查詢紀錄" in postback_data_refill:
        # 把只創建卻沒有寫入資料完成的列刪除
        postgres_delete_query = f"""DELETE FROM refill_cal_data WHERE (condition, user_id) = ('initial', '{event.source.user_id}');"""
        cursor.execute(postgres_delete_query)
        conn.commit()

        postgres_select_query = f"""SELECT * FROM refill_cal_data WHERE user_id = '{event.source.user_id}' AND due_date >= '{dt.date.today()}' ORDER BY prescription_date ASC;"""
        cursor.execute(postgres_select_query)
        refill_cal_data = cursor.fetchall()

        print("refill_cal_data = ", refill_cal_data)

        msg = flexmsg.DrugList(refill_cal_data)
        line_bot_api.reply_message(
            event.reply_token,
            msg
        )


    # elif "詳細資訊" in postback_data:
    #     record = postback_data.split("_")
    #     DATABASE_URL = os.environ['DATABASE_URL']
    #     conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    #     cursor = conn.cursor()
    #     postgres_select_query = f"""SELECT * FROM group_data WHERE activity_no = '{record[0]}' ;"""
    #     cursor.execute(postgres_select_query)
    #     data_tmp = cursor.fetchone()
    #     msg = flexmsg.MoreInfoSummary(data_tmp)
    #
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         msg
    #     )
    #
    #     # ~~點了carousel的"了解更多"，跳出該團的summary



    # elif "forward" in postback_data_drug or "backward" in postback_data_drug:
    #
    #     record = postback_data_drug.split("_")  # record[0] = forward, record[1] = command
    #
    #     if record[1] == "activity":
    #
    #         # record[2] = activity_type, record[3] = i
    #         j = int(record[3])
    #
    #         postgres_select_query = f"""SELECT * FROM group_data WHERE activity_date >= '{dt.date.today()}' AND due_date >= '{dt.date.today()}' AND activity_type = '{record[2]}' and people > attendee and condition = 'pending' ORDER BY activity_date ASC;"""
    #         cursor.execute(postgres_select_query)
    #         data = cursor.fetchall()
    #
    #         drug_info = flexmsg.flex_drug(data_2, j)
    #         line_bot_api.reply_message(
    #             event.reply_token,
    #             drug_info
    #         )
    #
    #     elif record[1] == "group":
    #
    #         # record[2] = j
    #         j = int(record[2])
    #         # 用user_id尋找該主揪所有的開團資料
    #         postgres_select_query = f"""SELECT * FROM drug_data WHERE user_id = '{event.source.user_id}' AND activity_date >= '{dt.date.today()}' ORDER BY activity_date ASC;"""
    #         cursor.execute(postgres_select_query)
    #         drug_data = cursor.fetchall()
    #
    #         print("group_data = ", drug_data)
    #
    #         # 回傳開團列表
    #         drug_info = flexmsg.DrugList(drug_data, j)
    #         line_bot_api.reply_message(
    #             event.reply_token,
    #             drug_info
    #         )
    #
    #     elif record[1] == "registration":
    #
    #         # record[2] = i
    #         i = int(record[2])
    #
    #         # 用user_id從database找出有報的團
    #         postgres_select_query = f"""SELECT * FROM registration_data WHERE user_id = '{event.source.user_id}' AND activity_date >= '{dt.date.today()}' ORDER BY activity_date ASC;"""
    #         cursor.execute(postgres_select_query)
    #
    #         # 避免look_up_data_registration裡的activity_name重複
    #         look_up_data_registration = []
    #         act_no = []
    #         alldata = cursor.fetchall()
    #         if alldata:
    #             for act in alldata:
    #                 if act[1] not in act_no:  # act[1]為activity_no, act[2]為activity_name
    #                     act_no.append(act[1])
    #                     look_up_data_registration.append(act)
    #
    #         msg = flexmsg.registration_list(look_up_data_registration, i)
    #         line_bot_api.reply_message(
    #             event.reply_token,
    #             msg
    #         )

    # 上一頁下一頁要寫在這個上面


    else:
        if data:

            i = data.index(None)
            print("i = ", i)
            progress_list_refill = [5, 1, 2, 3, 4, 5]

            column_all_refill = ['record_no', 'visit_date', 'prescription_days', 'total_refill_number',
                                 'last_refill_number', 'last_refill_date', 'today_date', 'second_refill_start_dt',
                                 'second_refill_end_dt', 'third_refill_start_dt',
                                 'third_refill_end_dt', 'valid_dt', 'user_id']
            # 處理 visit_date, last refill date
            if event.postback.data == "visit_date":
                record = event.postback.params['date']
                postgres_update_query = f"""UPDATE refill_cal_data SET {column_all_refill[i]} = '{record}' WHERE condition = 'initial' AND user_id = '{event.source.user_id}';"""
                cursor.execute(postgres_update_query)
                conn.commit()
            elif event.postback.data == "last_refill_date":
                record = event.postback.params['date']
                postgres_update_query = f"""UPDATE refill_cal_data SET {column_all_refill[i]} = '{record}' WHERE condition = 'initial' AND user_id = '{event.source.user_id}';"""
                cursor.execute(postgres_update_query)
                conn.commit()

            cursor.execute(postgres_select_query)
            data = cursor.fetchone()

            if None in data:
                msg = flexmsg.flex_prescription(i, progress_list_refill)
                line_bot_api.reply_message(
                    event.reply_token,
                    msg)
            elif None not in data:
                postgres_select_query = f"""SELECT * FROM refill_cal_data WHERE user_id = '{event.source.user_id}' ORDER BY documentation_no DESC;"""
                cursor.execute(postgres_select_query)
                data = cursor.fetchone()
                msg = flexmsg.summary(data)
                line_bot_api.reply_message(
                    event.reply_token,
                    msg
                )
            cursor.close()
            conn.close()


        elif data_2:
            j = data_2.index(None)
            print("j = ", j)
            column_all_drug = ['document_no', 'drug_category', 'drug_name', 'drug_amount', 'drug_frequency',
                               'prescription_date', 'duration', 'due_date', 'generic_name', 'description', 'photo', 'condition',
                               'user_id']
            # 處理 prescription date
            if event.postback.data_2 == "prescription_date":

                record = event.postback.params['date']
                postgres_update_query = f"""UPDATE drug_data SET {column_all[j]} = '{record}' WHERE condition = 'initial' AND user_id = '{event.source.user_id}';"""
                cursor.execute(postgres_update_query)
                conn.commit()

            cursor.execute(postgres_select_query)
            data_2 = cursor.fetchone()

            if None in data_2:
                drug_info = flexmsg.flex_drug(j, progress_list_drug)
                line_bot_api.reply_message(
                    event.reply_token,
                    drug_info)
            elif None not in data_2:
                postgres_select_query = f"""SELECT * FROM drug_data WHERE user_id = '{event.source.user_id}' ORDER BY documentation_no DESC;"""
                cursor.execute(postgres_select_query)
                data_2 = cursor.fetchone()
                drug_info = flexmsg.drug_info_summary(data_2)
                line_bot_api.reply_message(
                    event.reply_token,
                    drug_info
                )
            cursor.close()
            conn.close()



@app.route('/static/<path:path>')
def send_static_content(path):
    return send_from_directory('static', path)


if __name__ == "__main__":
    app.run()