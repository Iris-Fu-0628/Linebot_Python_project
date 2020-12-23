from linebot.models import (
    TextSendMessage, MessageAction, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent, FillerComponent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,CarouselContainer
)

from datetime import datetime as dt
import time
from datetime import datetime

import json


# 領藥時間查詢
def flex_prescription(i,progress):
    if i == 1 or i == "visit_date":
        msg = visit_date(progress)
    elif i == 2 or i == "prescription_days":
        msg = prescription_days(progress)
    elif i == 3 or i == "total_refill_number":
        msg = total_refill_number(progress)
    elif i == 4 or i == "last_refill_number":
        msg = last_refill_number(progress)
    elif i == 5 or i == "last_refill_date":
        msg = last_refill_date(progress)
    else:
        msg = TextSendMessage(text = "FlexMessage Bug 爆發中...")
    return msg


drug_refill_calculation = TextSendMessage(
    text = "請協助回答以下問題",
    quick_reply = QuickReply(
        items = [
            QuickReplyButton(
                action = MessageAction(label = "慢箋領藥時間查詢", text = "開始回答")
                )
            ]))


def visit_date(progress):
    visit_date = FlexSendMessage(
        alt_text = "請選擇看診日期",
        contents = BubbleContainer(
            direction = "ltr",
            body = BoxComponent(
                layout = "vertical",
                contents =[
                    TextComponent(
                        text = "請選擇看診日期",
                        size = "lg",
                        align = "center",
                        weight = "bold"
                    )
                ]
            ),
            footer = BoxComponent(
              layout = "vertical",
              contents = [
                  BoxComponent(layout = "vertical",
                                 margin = "md",
                                 contents = [TextComponent(text = f"{progress[1]} / {progress[0]} ", weight = "bold", size = "md"),
                                             BoxComponent(layout = "vertical",
                                                          margin = "md",
                                                          contents = [
                                                              BoxComponent(layout = "vertical",
                                                                           contents = [FillerComponent()]
                                                                          )
                                                          ],
                                                          width = f"{int(progress[1] / progress[0] * 100 + 0.5 )}%",
                                                          background_color = "#3DE1D0",
                                                          height = "6px"
                                                         )

                                            ]
                              ),
                  BoxComponent(layout = "vertical",
                                 margin = "md",
                                 contents = [
                                     ButtonComponent(
                                         DatetimePickerAction(
                                             label = "點我選日期",
                                             data = "Visit_date",
                                             mode = "date"
                                         ),
                                         height = "sm",
                                         margin = "none",
                                         style = "primary",
                                         color = "#A7D5E1",
                                         gravity = "bottom"
                                     )
                                 ]
                              )
              ]
            )
        )
    )
    return visit_date


def prescription_days(progress): # 處方天數
    prescription_days = FlexSendMessage(
        alt_text = "處方天數填寫",
        contents = BubbleContainer(
            direction = "ltr",
            body = BoxComponent(
              layout = "vertical",
              contents =[
              TextComponent(
                  text = "請填寫處方天數",
                  size = "lg",
                  align = "center",
                  weight = "bold"
                  )
              ]
            ),
            #進度條的本體
            footer=BoxComponent(
                layout = "vertical",
                margin = "md",
                contents = [TextComponent(text = f"{progress[2]} / {progress[0]} ", weight = "bold", size = "md"),
                            BoxComponent(layout = "vertical",
                                         margin = "md",
                                         contents = [
                                             BoxComponent(layout = "vertical",
                                                          contents = [FillerComponent()]
                                                         )
                                         ],
                                         width = f"{int(progress[2] / progress[0] * 100 + 0.5 )}%",
                                         background_color = "#3DE1D0",
                                         height = "6px"
                                        )
                           ]
            )
            #進度條的本體/
        )
    )
    return prescription_days

def total_refill_number(progress):  # 慢箋可領取次數
    total_refill_number = FlexSendMessage(
        alt_text = "請填寫處方箋可領取次數",
        contents = BubbleContainer(
            direction = "ltr",
            body = BoxComponent(
              layout = "vertical",
              contents =[
              TextComponent(
                  text = "請填寫處方箋可領取次數",
                  size = "lg",
                  align = "center",
                  weight = "bold"
                  )
              ]
            ),
            #進度條的本體
            footer=BoxComponent(
                layout = "vertical",
                margin = "md",
                contents = [TextComponent(text = f"{progress[3]} / {progress[0]} ", weight = "bold", size = "md"),
                            BoxComponent(layout = "vertical",
                                         margin = "md",
                                         contents = [
                                             BoxComponent(layout = "vertical",
                                                          contents = [FillerComponent()]
                                                         )
                                         ],
                                         width = f"{int(progress[3] / progress[0] * 100 + 0.5 )}%",
                                         background_color = "#3DE1D0",
                                         height = "6px"
                                        )
                           ]
            )
            #進度條的本體/
        )
    )
    return total_refill_number


def last_refill_number(progress):  # 上次領取
    last_refill_number = FlexSendMessage(
        alt_text = "已領取次數",
        contents = BubbleContainer(
            direction = "ltr",
            body = BoxComponent(
              layout = "vertical",
              contents =[
              TextComponent(
                  text = "請填寫已領取次數",
                  size = "lg",
                  align = "center",
                  weight = "bold"
                  )
              ]
            ),
            #進度條的本體
            footer=BoxComponent(
                layout = "vertical",
                margin = "md",
                contents = [TextComponent(text = f"{progress[4]} / {progress[0]} ", weight = "bold", size = "md"),
                            BoxComponent(layout = "vertical",
                                         margin = "md",
                                         contents = [
                                             BoxComponent(layout = "vertical",
                                                          contents = [FillerComponent()]
                                                         )
                                         ],
                                         width = f"{int(progress[4] / progress[0] * 100 + 0.5 )}%",
                                         background_color = "#3DE1D0",
                                         height = "6px"
                                        )
                           ]
            )
            #進度條的本體/
        )
    )
    return last_refill_number

def last_refill_date(progress):  # 上次(實際)領取第幾次
    last_refill_date = FlexSendMessage(
        alt_text = "請挑選上次領藥日期",
        contents = BubbleContainer(
            direction = "ltr",
            body = BoxComponent(
                layout = "vertical",
                contents =[
                    TextComponent(
                        text = "請選上次領藥日期",
                        size = "lg",
                        align = "center",
                        weight = "bold"
                    )
                ]
            ),
            footer = BoxComponent(
              layout = "vertical",
              contents = [
                  BoxComponent(layout = "vertical",
                                 margin = "md",
                                 contents = [TextComponent(text = f"{progress[5]} / {progress[0]} ", weight = "bold", size = "md"),
                                             BoxComponent(layout = "vertical",
                                                          margin = "md",
                                                          contents = [
                                                              BoxComponent(layout = "vertical",
                                                                           contents = [FillerComponent()]
                                                                          )
                                                          ],
                                                          width = f"{int(progress[5] / progress[0] * 100 + 0.5 )}%",
                                                          background_color = "#3DE1D0",
                                                          height = "6px"
                                                         )

                                            ]
                              ),
                  BoxComponent(layout = "vertical",
                                 margin = "md",
                                 contents = [
                                     ButtonComponent(
                                         DatetimePickerAction(
                                             label = "點我選日期",
                                             data = "last_refill_date",
                                             mode = "datetime"
                                         ),
                                         height = "sm",
                                         margin = "none",
                                         style = "primary",
                                         color = "#A7D5E1",
                                         gravity = "bottom"
                                     )
                                 ]
                              )
              ]
            )
        )
    )
    return last_refill_date


def summary(data):
    if data[12]=='無':
        act=None
        col="#444444"
    else:
        act=URIAction(uri = f"{data[12]}")
        col="#229C8F"
    sumer = FlexSendMessage(
        alt_text = "請確認填寫資訊",
        contents = BubbleContainer(
            direction = "ltr",
            header = BoxComponent(
              layout = "vertical",
              contents = [
              TextComponent(
                  text = "請確認填寫資訊",
                  weight = "bold",
                  size = "md",
                  align = "start",
                  color = "#000000"
                  )
              ]
            ),
            body = BoxComponent(
                layout = "vertical",
                contents = [
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = f"活動類型 {data[1]}",
                                size = "md",
                                flex = 10,
                                align = "start"
                            ),
                            SeparatorComponent(
                                color = "#FFFFFF",margin = "lg"
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = "修改",
                                size = "md",
                                align = "end",
                                gravity = "top",
                                weight = "bold",
                                action = MessageAction(
                                    text = "activity_type"
                                )
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = f"活動名稱 {data[2]}",
                                size = "md",
                                flex = 10,
                                align = "start"
                            ),
                            SeparatorComponent(
                                color = "#FFFFFF",margin = "lg"
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = "修改",
                                size = "md",
                                align = "end",
                                gravity = "top",
                                weight = "bold",
                                action = MessageAction(
                                    text = "activity_name"
                                )
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = f"活動時間 {data[3]} {str(data[4])[:5]}",
                                size = "md",
                                flex = 10,
                                align = "start"
                            ),
                            SeparatorComponent(
                                color = "#FFFFFF",margin = "lg"
                            )
                        ]
                    ),BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = "修改",
                                size = "md",
                                align = "end",
                                gravity = "top",
                                weight = "bold",
                                action = MessageAction(
                                    text = "activity_date"
                                )
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = f"活動地點 {data[5]}",
                                size = "md",
                                flex = 10,
                                wrap = True,
                                align = "start"
                            ),
                            SeparatorComponent(
                                color = "#FFFFFF",margin = "lg"
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = "修改",
                                size = "md",
                                align = "end",
                                gravity = "top",
                                weight = "bold",
                                action = MessageAction(
                                    text = "location"
                                )
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = f"活動人數 {data[8]}",
                                size = "md",
                                flex = 10,
                                align = "start"
                            ),
                            SeparatorComponent(
                                color = "#FFFFFF",margin = "lg"
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = "修改",
                                size = "md",
                                align = "end",
                                gravity = "top",
                                weight = "bold",
                                action = MessageAction(
                                    text = "people"
                                )
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = f"活動費用 {data[9]}",
                                size = "md",
                                flex = 10,
                                align = "start"
                            ),
                            SeparatorComponent(
                                color = "#FFFFFF",margin = "lg"
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = "修改",
                                size = "md",
                                align = "end",
                                gravity = "top",
                                weight = "bold",
                                action = MessageAction(
                                    text = "cost"
                                )
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = f"報名截止日 {data[10]}",
                                size = "md",
                                flex = 10,
                                align = "start"
                            ),
                            SeparatorComponent(
                                color = "#FFFFFF",margin = "lg"
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = "修改",
                                size = "md",
                                align = "end",
                                gravity = "top",
                                weight = "bold",
                                action = MessageAction(
                                    text = "due_date"
                                )
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = f"活動敘述 {data[11]}",
                                size = "md",
                                flex = 10,
                                align = "start"
                            ),
                            SeparatorComponent(
                                color = "#FFFFFF",margin = "lg"
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = "修改",
                                size = "md",
                                align = "end",
                                gravity = "top",
                                weight = "bold",
                                action = MessageAction(
                                    text = "description"
                                )
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = f"活動照片 {data[12]}",
                                size = "md",
                                flex = 10,
                                align = "start",
                                action= act,
                                wrap = True,
                                color = f"{col}"
                            ),
                            SeparatorComponent(
                                color = "#FFFFFF",margin = "lg"
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = "修改",
                                size = "md",
                                align = "end",
                                gravity = "top",
                                weight = "bold",
                                action = MessageAction(
                                    text = "photo"
                                )
                            )
                        ]
                    ),
                ]
            ),
            footer = BoxComponent(
                layout = "horizontal",
                contents = [
                    ButtonComponent(
                        style = "link",
                        height = "sm",
                        margin = "none",
                        color = "#229C8F",
                        gravity = "bottom",
                        action = MessageAction(
                            label = "確認填寫無誤",
                            text = "確認填寫無誤"
                        )
                    ),
                    SeparatorComponent(),
                    ButtonComponent(
                        style = "link",
                        height = "sm",
                        margin = "none",
                        color = "#229C8F",
                        gravity = "bottom",
                        action = MessageAction(
                            label = "取消詢問",
                            text = "取消"
                        )
                    )
                ]
            )
        )
    )
    return sumer


# def drug_refill_cal(prescription_days,total_refill_number,last_refill_number,last_refill_date):
#     datetime_dt = datetime.datetime.today()  # 獲得當地時間
#     today_dt = datetime_dt.date()  # 最小日期顯示到日
#
#     time_delta_all = datetime.timedelta(days=int(prescription_days * total_refill_number))
#     valid_dt = visit_date + time_delta_all  # 處方箋的有效期限
#
#     time_delta = datetime.timedelta(days = prescription_days)
#     second_refill_start_dt = last_refill_date + time_delta - datetime.timedelta(days=int(10))  # 第二次領藥起始日
#     second_refill_end_dt = last_refill_date + time_delta  # 第二次領藥截止日
#
#
#     if today_dt > valid_dt:
#         print('處方已過期，請重新掛號看診，領取新的處方箋')
#     elif total_refill_number == 2:  # 共 2 次
#         if today_dt < second_refill_start_dt:
#             print('現在還不能領喔！')
#             print('建議領藥時間：{}年 {}月 {}日'.format(second_refill_start_dt.year, second_refill_start_dt.month,
#                                               second_refill_start_dt.day) + '~{}年 {}月 {}日'.format(second_refill_end_dt.year,
#                                                                                                 second_refill_end_dt.month,
#                                                                                                 second_refill_end_dt.day))
#         elif second_refill_start_dt <= today_dt <= second_refill_end_dt:
#             print('現在可以領！請您在 {}年 {}月 {}日前領取。'.format(second_refill_end_dt.year, second_refill_end_dt.month,
#                                                      second_refill_end_dt.day))
#         elif second_refill_end_dt <= today_dt <= valid_dt:
#             print('咦！請您確認是否按時服藥，並盡快領藥。務必在 {}年 {}月 {}日前領取。'.format(valid_dt.year, valid_dt.month, valid_dt.day))
#         elif last_refill_number == 2:  # 2 times
#             print('所有處方已領取完。請重新掛號看診。')
#     elif total_refill_number == 3:  # 共 3 次
#         if last_refill_number == 1:  # 只領第一次
#             if today_dt < second_refill_start_dt:
#                 print('現在還不能領喔！')
#                 print('建議領藥時間：{}年 {}月 {}日'.format(second_refill_start_dt.year, second_refill_start_dt.month,
#                                                   second_refill_start_dt.day) + '~{}年 {}月 {}日'.format(second_refill_end_dt.year,
#                                                                                                     second_refill_end_dt.month,
#                                                                                                     second_refill_end_dt.day))
#             elif second_refill_start_dt <= today_dt <= second_refill_end_dt:
#                 print('現在可以領！請您在' + second_refill_end_dt + '前領取。')
#
#             else:
#                 print('咦！請您確認是否按時服藥，並盡快領藥。')
#         elif last_refill_number == 2:  # 已領 2次
#             third_refill_start_dt = last_refill_date + time_delta - datetime.timedelta(days = int(10))  # 第三次領藥起始日
#             third_refill_end_dt = last_refill_date + time_delta  # 第三次領藥截止日
#             if today_dt < third_refill_start_dt:
#                 print('現在還不能領喔！')
#                 print('建議領藥時間：{}年 {}月 {}日'.format(third_refill_start_dt.year, third_refill_start_dt.month,
#                                                   third_refill_start_dt.day) + '~{}年 {}月 {}日'.format(third_refill_end_dt.year,
#                                                                                                    third_refill_end_dt.month,
#                                                                                                    third_refill_end_dt.day))
#             elif third_refill_start_dt <= today_dt <= third_refill_end_dt:
#                 print('現在可以領！請您在請您在 {}年 {}月 {}日前領取。'.format(third_refill_end_dt.year, third_refill_end_dt.month,
#                                                             third_refill_end_dt.day))
#             else:
#                 print('咦！請您確認是否按時服藥，並盡快領藥。務必在 {}年 {}月 {}日前領取。'.format(valid_dt.year, valid_dt.month, valid_dt.day))
#         elif last_refill_number == 3:  # 3 times
#             print('所有處方已領取完。請重新掛號看診。')


def flex_drug(j,progress):
    if j == 1 or j == "drug_name":
        drug_info = drug_name(progress)
    elif j == 3 or j == "drug_prescription_date":
        drug_info = prescription_date(progress)
    elif j == 4 or j == "duration":
        drug_info = duration(progress)
    elif j == 5 or j == "drug_amount":
        drug_info = drug_amount(progress)
    elif j == 6 or j == "frequency":
        drug_info = drug_frequency(progress)
    elif j == 7 or j == "description":
        drug_info = description
    elif j == 8 or j == "photo":
        drug_info = photo
    else:
        drug_info = TextSendMessage(text = "FlexMessage Bug 爆發中...")
    return drug_info


drug_category = TextSendMessage(
    text = "請選擇您的藥品類別",
    quick_reply = QuickReply(
        items = [
            QuickReplyButton(
                action = MessageAction(label = "處方藥", text = "處方藥")
                ),
            QuickReplyButton(
                action = MessageAction(label = "非處方藥品", text = "非處方藥品")
                ),
            QuickReplyButton(
                action = MessageAction(label = "中草藥", text = "中草藥")
                ),
            QuickReplyButton(
                action = MessageAction(label = "保健食品", text = "保健食品")
                )
            ]))


def drug_name(progress):
    drug_name = FlexSendMessage(
        alt_text = "請填寫藥品名稱",
        contents = BubbleContainer(
            direction = "ltr",
            body = BoxComponent(
                layout = "vertical",
                contents = [
                    TextComponent(text = "藥品名稱", weight = "bold", size = "lg", align = "center"),
                    BoxComponent(layout = "baseline",
                                 margin = "lg",
                                 contents = [
                                     TextComponent(text = "藥品的中文或英文商品名(與含量)",
                                                   size = "md",
                                                   flex = 0,
                                                   color = "#666666"
                                                  )
                                 ]
                                )
                ]
            ),
            #進度條的本體
            footer=BoxComponent(
                layout = "vertical",
                margin = "md",
                contents = [TextComponent(text = f"{progress[1]} / {progress[0]} ", weight = "bold", size = "md"),
                            BoxComponent(layout = "vertical",
                                         margin = "md",
                                         contents = [
                                             BoxComponent(layout = "vertical",
                                                          contents = [FillerComponent()]
                                                         )
                                         ],
                                         width = f"{int(progress[1] / progress[0] * 100 + 0.5 )}%",
                                         background_color = "#3DE1D0",
                                         height = "6px"
                                        )
                           ]
            )
            #進度條的本體/
        )
    )
    return drug_name

def prescription_date(progress):
    prescription_date = FlexSendMessage(
        alt_text = "請挑選藥品處方/取得日期",
        contents = BubbleContainer(
            direction = "ltr",
            body = BoxComponent(
                layout = "vertical",
                contents =[
                    TextComponent(
                        text = "請選擇藥品處方/取得日期",
                        size = "lg",
                        align = "center",
                        weight = "bold"
                    )
                ]
            ),
            footer = BoxComponent(
              layout = "vertical",
              contents = [
                  BoxComponent(layout = "vertical",
                                 margin = "md",
                                 contents = [TextComponent(text = f"{progress[3]} / {progress[0]} ", weight = "bold", size = "md"),
                                             BoxComponent(layout = "vertical",
                                                          margin = "md",
                                                          contents = [
                                                              BoxComponent(layout = "vertical",
                                                                           contents = [FillerComponent()]
                                                                          )
                                                          ],
                                                          width = f"{int(progress[3] / progress[0] * 100 + 0.5 )}%",
                                                          background_color = "#3DE1D0",
                                                          height = "6px"
                                                         )

                                            ]
                              ),
                  BoxComponent(layout = "vertical",
                                 margin = "md",
                                 contents = [
                                     ButtonComponent(
                                         DatetimePickerAction(
                                             label = "點我選日期",
                                             data = "prescription_date",
                                             mode = "date"
                                         ),
                                         height = "sm",
                                         margin = "none",
                                         style = "primary",
                                         color = "#A7D5E1",
                                         gravity = "bottom"
                                     )
                                 ]
                              )
              ]
            )
        )
    )
    return prescription_date


def duration(progress):
    duration = FlexSendMessage(
        alt_text = "請填寫處方/預計服用天數",
        contents = BubbleContainer(
            direction = "ltr",
            body = BoxComponent(
              layout = "vertical",
              contents =[
              TextComponent(
                  text = "請填寫處方/預計服用天數",
                  size = "lg",
                  align = "center",
                  weight = "bold"
                  )
              ]
            ),
            #進度條的本體
            footer=BoxComponent(
                layout = "vertical",
                margin = "md",
                contents = [TextComponent(text = f"{progress[4]} / {progress[0]} ", weight = "bold", size = "md"),
                            BoxComponent(layout = "vertical",
                                         margin = "md",
                                         contents = [
                                             BoxComponent(layout = "vertical",
                                                          contents = [FillerComponent()]
                                                         )
                                         ],
                                         width = f"{int(progress[4] / progress[0] * 100 + 0.5 )}%",
                                         background_color = "#3DE1D0",
                                         height = "6px"
                                        )
                           ]
            )
            #進度條的本體/
        )
    )
    return duration


def drug_amount(progress):
    drug_amount = FlexSendMessage(
        alt_text = "請填寫每次服用劑量",
        contents = BubbleContainer(
            direction = "ltr",
            body = BoxComponent(
              layout = "vertical",
                contents = [
                    TextComponent(text = "請填寫每次服用劑量", weight = "bold", size = "lg", align = "center"),
                    BoxComponent(layout = "baseline",
                                 margin = "lg",
                                 contents = [
                                     TextComponent(text = "服用劑量格式：數量/單位(錠、顆、mg或g...)",
                                                   size = "md",
                                                   flex = 0,
                                                   color = "#666666"
                                                  )
                                 ]
                                )
                ]
            ),
            #進度條的本體
            footer=BoxComponent(
                layout = "vertical",
                margin = "md",
                contents = [TextComponent(text = f"{progress[5]} / {progress[0]} ", weight = "bold", size = "md"),
                            BoxComponent(layout = "vertical",
                                         margin = "md",
                                         contents = [
                                             BoxComponent(layout = "vertical",
                                                          contents = [FillerComponent()]
                                                         )
                                         ],
                                         width = f"{int(progress[5] / progress[0] * 100 + 0.5 )}%",
                                         background_color = "#3DE1D0",
                                         height = "6px"
                                        )
                           ]
            )
            #進度條的本體/
        )
    )
    return drug_amount

def drug_frequency(progress):
    drug_frequency = FlexSendMessage(
        alt_text = "請填寫每次服用劑量",
        contents = BubbleContainer(
            direction = "ltr",
            body = BoxComponent(
              layout = "vertical",
                contents = [
                    TextComponent(text = "請填寫每次服用劑量", weight = "bold", size = "lg", align = "center"),
                    BoxComponent(layout = "baseline",
                                 margin = "lg",
                                 contents = [
                                     TextComponent(text = "服用劑量格式：數量/單位(錠、顆、mg或g...)",
                                                   size = "md",
                                                   flex = 0,
                                                   color = "#666666"
                                                  )
                                 ]
                                )
                ]
            ),
            #進度條的本體
            footer=BoxComponent(
                layout = "vertical",
                margin = "md",
                contents = [TextComponent(text = f"{progress[5]} / {progress[0]} ", weight = "bold", size = "md"),
                            BoxComponent(layout = "vertical",
                                         margin = "md",
                                         contents = [
                                             BoxComponent(layout = "vertical",
                                                          contents = [FillerComponent()]
                                                         )
                                         ],
                                         width = f"{int(progress[5] / progress[0] * 100 + 0.5 )}%",
                                         background_color = "#3DE1D0",
                                         height = "6px"
                                        )
                           ]
            )
            #進度條的本體/
        )
    )
    return drug_frequency


description = FlexSendMessage(
    alt_text = "請填寫藥品用途",
    contents = BubbleContainer(
        direction = "ltr",
        body = BoxComponent(
          layout = "vertical",
          contents = [
          TextComponent(
              text = "請填寫詳細藥品用途",
              size = "lg",
              align = "center",
              weight = "bold"
              )
          ]
        )
    )
)

photo = FlexSendMessage(
    alt_text = "請提供照片",
    contents = BubbleContainer(
        direction = "ltr",
        body = BoxComponent(
          layout = "vertical",
          contents = [
          TextComponent(
              text = "請傳送一張藥品的照片",
              size = "md",
              wrap = True,
              align = "center",
              weight = "bold"
              )
          ]
        )
    )
)


def drug_info_summary(data_2):
    if data_2[8]=='無':
        act=None
        col="#444444"
    else:
        act=URIAction(uri = f"{data_2[8]}")
        col="#229C8F"
    summar = FlexSendMessage(
        alt_text = "請確認藥品資訊",
        contents = BubbleContainer(
            direction = "ltr",
            header = BoxComponent(
              layout = "vertical",
              contents = [
              TextComponent(
                  text = "請確認填寫資訊",
                  weight = "bold",
                  size = "md",
                  align = "start",
                  color = "#000000"
                  )
              ]
            ),
            body = BoxComponent(
                layout = "vertical",
                contents = [
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = f"藥品類別 {data_2[1]}",
                                size = "md",
                                flex = 10,
                                align = "start"
                            ),
                            SeparatorComponent(
                                color = "#FFFFFF",margin = "lg"
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = "修改",
                                size = "md",
                                align = "end",
                                gravity = "top",
                                weight = "bold",
                                action = MessageAction(
                                    text = "drug_category"
                                )
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = f"藥品名稱 {data_2[2]}",
                                size = "md",
                                flex = 10,
                                align = "start"
                            ),
                            SeparatorComponent(
                                color = "#FFFFFF",margin = "lg"
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = "修改",
                                size = "md",
                                align = "end",
                                gravity = "top",
                                weight = "bold",
                                action = MessageAction(
                                    text = "drug_name"
                                )
                            )
                        ]
                    ),
                    BoxComponent(
                        layout="horizontal",
                        contents=[
                            TextComponent(
                                text=f"學名 {data_2[3]}",
                                size="md",
                                flex=10,
                                align="start"
                            ),
                            SeparatorComponent(
                                color="#FFFFFF", margin="lg"
                            )
                        ]
                    ),
                    BoxComponent(
                        layout="horizontal",
                        contents=[
                            TextComponent(
                                text="修改",
                                size="md",
                                align="end",
                                gravity="top",
                                weight="bold",
                                action=MessageAction(
                                    text="generic_name"
                                )
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = f"藥品取得日期 {data_2[5]}",
                                size = "md",
                                flex = 10,
                                align = "start"
                            ),
                            SeparatorComponent(
                                color = "#FFFFFF",margin = "lg"
                            )
                        ]
                    ),BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = "修改",
                                size = "md",
                                align = "end",
                                gravity = "top",
                                weight = "bold",
                                action = MessageAction(
                                    text = "prescription_date"
                                )
                            )
                        ]
                    ),
                    BoxComponent(
                        layout="horizontal",
                        contents=[
                            TextComponent(
                                text=f"每次服用劑量 {data_2[7]}",
                                size="md",
                                flex=10,
                                align="start"
                            ),
                            SeparatorComponent(
                                color="#FFFFFF", margin="lg"
                            )
                        ]
                    ),
                    BoxComponent(
                        layout="horizontal",
                        contents=[
                            TextComponent(
                                text="修改",
                                size="md",
                                align="end",
                                gravity="top",
                                weight="bold",
                                action=MessageAction(
                                    text="drug_amount"
                                )
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = f"服用頻次 {data_2[8]}",
                                size = "md",
                                flex = 10,
                                align = "start"
                            ),
                            SeparatorComponent(
                                color = "#FFFFFF",margin = "lg"
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = "修改",
                                size = "md",
                                align = "end",
                                gravity = "top",
                                weight = "bold",
                                action = MessageAction(
                                    text = "drug_frequency"
                                )
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = f"藥品敘述 {data_2[9]}",
                                size = "md",
                                flex = 10,
                                align = "start"
                            ),
                            SeparatorComponent(
                                color = "#FFFFFF",margin = "lg"
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = "修改",
                                size = "md",
                                align = "end",
                                gravity = "top",
                                weight = "bold",
                                action = MessageAction(
                                    text = "description"
                                )
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = f"報名截止日 {data_2[10]}",
                                size = "md",
                                flex = 10,
                                align = "start"
                            ),
                            SeparatorComponent(
                                color = "#FFFFFF",margin = "lg"
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = "修改",
                                size = "md",
                                align = "end",
                                gravity = "top",
                                weight = "bold",
                                action = MessageAction(
                                    text = "due_date"
                                )
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = f"藥品照片 {data_2[11]}",
                                size = "md",
                                flex = 10,
                                align = "start",
                                action= act,
                                wrap = True,
                                color = f"{col}"
                            ),
                            SeparatorComponent(
                                color = "#FFFFFF",margin = "lg"
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = "修改",
                                size = "md",
                                align = "end",
                                gravity = "top",
                                weight = "bold",
                                action = MessageAction(
                                    text = "photo"
                                )
                            )
                        ]
                    ),
                ]
            ),
            footer = BoxComponent(
                layout = "horizontal",
                contents = [
                    ButtonComponent(
                        style = "link",
                        height = "sm",
                        margin = "none",
                        color = "#229C8F",
                        gravity = "bottom",
                        action = MessageAction(
                            label = "確認紀錄",
                            text = "確認紀錄"
                        )
                    ),
                    SeparatorComponent(),
                    ButtonComponent(
                        style = "link",
                        height = "sm",
                        margin = "none",
                        color = "#229C8F",
                        gravity = "bottom",
                        action = MessageAction(
                            label = "取消",
                            text = "取消"
                        )
                    )
                ]
            )
        )
    )
    return summar