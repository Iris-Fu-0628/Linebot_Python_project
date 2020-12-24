from linebot.models import (
    TextSendMessage, MessageAction, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction,
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
    elif i == "prescription_category":
        msg = drug_refill_calculation
    else:
        msg = TextSendMessage(text = "FlexMessage Bug")
    return msg


drug_refill_calculation = TextSendMessage(
    text = "請確認您的處方箋種類",
    quick_reply = QuickReply(
        items = [
            QuickReplyButton(
                action=MessageAction(label="一般處方箋", text="一般處方箋")
            ),
            QuickReplyButton(
                action=MessageAction(label="慢性處方箋", text="慢性處方箋")
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

    summary = FlexSendMessage(
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
                                text = f"看診日期 {data[2]}",
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
                                    text = "visit_date"
                                )
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = f"處方天數 {data[3]} 天",
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
                                    text = "prescription_days"
                                )
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = f"處方箋可領取次數 {data[4]} 次",
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
                                    text = "total_refill_number"
                                )
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = f"已領取次數 {data[5]} 次",
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
                                    text = "已領取次數"
                                )
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = f"上次領藥日期 {data[6]}",
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
                                    text = "last_refill_date"
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
    return summary


# def drug_refill_cal(data):
#     today_dt = data[8]
#     visit_date = data[2]
#     prescription_days = int(data[3])
#     total_refill_number = int(data[4])
#     last_refill_number = int(data[5])
#     last_refill_date = data[6]
#
#     time_delta_all = datetime.timedelta(days=int(prescription_days * total_refill_number))
#     valid_dt = visit_date + time_delta_all  # 處方箋的有效期限
#
#     time_delta = datetime.timedelta(days=prescription_days)
#     second_refill_start_dt = last_refill_date + time_delta - datetime.timedelta(days=int(10))  # 第二次領藥起始日
#     second_refill_end_dt = last_refill_date + time_delta  # 第二次領藥截止日
#
#     if today_dt > valid_dt:
#         result = ('處方已過期，請重新掛號看診，領取新的處方箋')
#
#     elif total_refill_number == 2:  # 共 2 次
#         if today_dt < second_refill_start_dt:
#             result = ('現在還不能領喔！''建議領藥時間：{}年 {}月 {}日'.format(second_refill_start_dt.year, second_refill_start_dt.month,
#                                                             second_refill_start_dt.day) + '~{}年 {}月 {}日'.format(
#                 second_refill_end_dt.year,
#                 second_refill_end_dt.month,
#                 second_refill_end_dt.day)))
#
#             elif second_refill_start_dt <= today_dt <= second_refill_end_dt:
#             result = ('現在可以領！請您在 {}年 {}月 {}日前領取。'.format(second_refill_end_dt.year, second_refill_end_dt.month,
#                                                          second_refill_end_dt.day))
#             elif second_refill_end_dt <= today_dt <= valid_dt:
#             result = ('咦！請您確認是否按時服藥，並盡快領藥。務必在 {}年 {}月 {}日前領取。'.format(valid_dt.year, valid_dt.month, valid_dt.day))
#             elif last_refill_number == 2:  # 2 times
#             result = ('所有處方已領取完。請重新掛號看診。')
#
#             elif total_refill_number == 3:  # 共 3 次
#             if last_refill_number == 1:  # 只領第一次
#                 if
#             today_dt < second_refill_start_dt:
#             resturn = ('現在還不能領喔！' + '建議領藥時間：{}年 {}月 {}日'.format(second_refill_start_dt.year,
#                                                                 second_refill_start_dt.month,
#                                                                 second_refill_start_dt.day) + '~{}年 {}月 {}日'.format(
#                 second_refill_end_dt.year,
#                 second_refill_end_dt.month,
#                 second_refill_end_dt.day))
#             elif second_refill_start_dt <= today_dt <= second_refill_end_dt:
#             result = ('現在可以領！請您在' + second_refill_end_dt + '前領取。')
#
#             else:
#             result = ('咦！請您確認是否按時服藥，並盡快領藥。')
#
#             elif last_refill_number == 2:  # 已領 2次
#             third_refill_start_dt = last_refill_date + time_delta - datetime.timedelta(days=int(10))  # 第三次領藥起始日
#             third_refill_end_dt = last_refill_date + time_delta  # 第三次領藥截止日
#             if today_dt < third_refill_start_dt:
#                 result = ('現在還不能領喔！' + '建議領藥時間：{}年 {}月 {}日'.format(third_refill_start_dt.year,
#                                                                    third_refill_start_dt.month,
#                                                                    third_refill_start_dt.day) + '~{}年 {}月 {}日'.format(
#                     third_refill_end_dt.year,
#                     third_refill_end_dt.month,
#                     third_refill_end_dt.day))
#             elif third_refill_start_dt <= today_dt <= third_refill_end_dt:
#                 result = ('現在可以領！請您在請您在 {}年 {}月 {}日前領取。'.format(third_refill_end_dt.year, third_refill_end_dt.month,
#                                                                 third_refill_end_dt.day))
#             else:
#                 result = ('咦！請您確認是否按時服藥，並盡快領藥。務必在 {}年 {}月 {}日前領取。'.format(valid_dt.year, valid_dt.month, valid_dt.day))
#             elif last_refill_number == 3:
#             result = ('所有處方已領取完。請重新掛號看診。')
#
#     return result


def flex_drug(j,progress):
    if j == 1 or j == "drug_name":
        drug_info = drug_name(progress)
    elif j == 4  or j == "prescription_date":
        drug_info = prescription_date(progress)
    elif j == 5 or j == "duration":
        drug_info = duration(progress)
    elif j == 2 or j == "drug_amount":
        drug_info = drug_amount(progress)
    elif j == 3 or j == "frequency":
        drug_info = drug_frequency(progress)
    elif j == 7 or j == "generic_name":
        drug_info = generic_name
    elif j == 11 or j== 8 or j == "description":
        drug_info = description
    elif j == 10 or j == "photo":
        drug_info = photo
    elif j == "drug_category":
        drug_info = drug_category
    else:
        drug_info = TextSendMessage(text = "FlexMessage Bug !!!")
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
        alt_text = "藥品處方/取得日期",
        contents = BubbleContainer(
            direction = "ltr",
            body = BoxComponent(
                layout = "vertical",
                contents =[
                    TextComponent(
                        text = "藥品處方/取得日期",
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
                              ),
                  BoxComponent(layout = "vertical",
                                 margin = "md",
                                 contents = [
                                     ButtonComponent(
                                         DatetimePickerAction(
                                             label = "點我選日期",
                                             data = "prescription_date",
                                             mode = "date",
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
                                     TextComponent(text = "格式：數量/單位(+備註)",
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
    return drug_amount

def drug_frequency(progress):
    drug_frequency = FlexSendMessage(
        alt_text = "請填寫每日服用頻率",
        contents = BubbleContainer(
            direction = "ltr",
            body = BoxComponent(
              layout = "vertical",
                contents = [
                    TextComponent(text = "請填寫每日服用頻率", weight = "bold", size = "lg", align = "center"),
                    BoxComponent(layout = "baseline",
                                 margin = "lg",
                                 contents = [
                                     TextComponent(text = "一天?/次(數字)",
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
    return drug_frequency


generic_name = FlexSendMessage(
    alt_text = "請填寫藥品學名",
    contents = BubbleContainer(
        direction = "ltr",
        body = BoxComponent(
          layout = "vertical",
          contents = [
          TextComponent(
              text = "請填寫藥品學名",
              size = "lg",
              align = "center",
              weight = "bold"
              )
          ]
        )
    )
)

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
    if data_2[10]=='無':
        act=None
        col="#444444"
    else:
        act=URIAction(uri = f"{data_2[10]}")
        col="#229C8F"
        hero = ImageComponent(
            size="full",
            aspectMode="cover",
            margin="none",
            url=f"{data_2[10]}"
        )
    summary = FlexSendMessage(
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
                                text=f"學名 {data_2[8]}",
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
                                text=f"每次服用劑量 {data_2[3]}",
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
                                text = f"服用頻次 {data_2[4]}",
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
                        layout="horizontal",
                        contents=[
                            TextComponent(
                                text=f"預計服用天數 {data_2[6]}",
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
                                    text="duration"
                                )
                            )
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = f"服用結束日期 {data_2[7]}",
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
                                text = "-",
                                size = "md",
                                align = "end"
                            ),
                        ]
                    ),
                    BoxComponent(
                        layout = "horizontal",
                        contents = [
                            TextComponent(
                                text = f"藥品照片 {data_2[10]}",
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
    return summary


# 我的開團列表
def DrugList(data_2, _=0):
    if _ == 0:
        jj = 0
    else:
        jj = _ - 8

    if data_2:

        drug_lst = []

        # row [document_no, drug_category, drug_name, drug_amount, drug_frequency, prescription_date, ...]
        for j in range(_, len(data_2)):
            print("j = ", j)
            drug = f'''{{
              "type": "box",
              "layout": "horizontal",
              "contents": [
                {{
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                    {{
                        "type": "icon",
                        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                        "flex": 1,
                        "align": "start",
                        "size": "sm"
                     }}
                     ]
                }},
                {{
                  "type": "text",
                  "text": "{data_2[j][2]}",
                  "flex": 9,
                  "size": "md",
                  "align" :  "start",
                  "color" : "#227C9D",
                  "weight" :  "regular",
                  "margin": "sm",
                  "action": {{
                  "type": "postback",
                  "data": "藥品紀錄 {data_2[j][0]}"
                  }}

                }}
              ]
            }}'''
            drug_lst.append(json.loads(drug))

            if len(drug_lst) > 10:
                break

        index_drug = BubbleContainer(
            size="kilo",
            direction="ltr",
            header=BoxComponent(
                layout="horizontal",
                contents=[
                    TextComponent(
                        text="我的藥品紀錄表",
                        size="lg",
                        weight="bold",
                        color="#AAAAAA"
                    )
                ]
            ),
            body=BoxComponent(
                layout="vertical",
                spacing="md",
                contents=drug_lst
            ),
            footer=BoxComponent(
                layout="horizontal",
                contents=[
                    ButtonComponent(
                        action=PostbackAction(
                            label="上一頁",
                            data=f"backward_drug_{jj}"
                        ),
                        height="sm",
                        style="primary",
                        color="#A7D5E1",
                        gravity="bottom"
                    ),
                    SeparatorComponent(
                        margin="sm",
                        color="#FFFFFF"
                    ),
                    ButtonComponent(
                        action=PostbackAction(
                            label="下一頁",
                            data=f"forward_drug_{j + 1}"
                        ),
                        height="sm",
                        style="primary",
                        color="#A7D5E1",
                        gravity="bottom"
                    )
                ]
            )
        )

    drug_info = FlexSendMessage(
        alt_text = "我的藥品紀錄",
        contents = index_drug
    )
    return drug_info