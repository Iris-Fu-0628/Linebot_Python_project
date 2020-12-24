import os
import psycopg2

DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a drugtaking-linebot').read()[:-1]
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()


#創藥品記錄表單 drug_data
create_table =  '''CREATE TABLE drug_data(
           document_no serial PRIMARY KEY,
           drug_category VARCHAR (50),
           drug_name VARCHAR (50),
           drug_amount VARCHAR (50) ,
           drug_frequency Integer ,
           prescription_date DATE ,
           duration Integer ,
           due_date DATE DEFAULT DEFAULT timezone('CCT'::text, now()),
           generic_name VARCHAR (50),
           description TEXT,
           photo TEXT,
           condition VARCHAR (50),
           user_id VARCHAR (50)
        );'''

cursor.execute(create_table)
conn.commit()

#創慢箋查詢表單 refill_cal_data
create_table =  '''CREATE TABLE refill_cal_data(
           document_no serial PRIMARY KEY,
           prescription_category VARCHAR (50),
           visit_date DATE,
           prescription_days Integer,
           total_refill_number Integer,
           last_refill_number Integer,
           last_refill_date DATE,
           valid_dt DATE,
           today_date DATE DEFAULT timezone('CCT'::text, now()),           
           next_refill_start_dt DATE DEFAULT timezone('CCT'::text, now()),
           next_refill_end_dt DATE DEFAULT timezone('CCT'::text, now()),
           second_refill_start_dt VARCHAR (50),
           second_refill_end_dt VARCHAR (50),
           third_refill_start_dt VARCHAR (50),
           third_refill_end_dt VARCHAR (50),
           condition VARCHAR (50),
           user_id VARCHAR (50)
        );'''

cursor.execute(create_table)
conn.commit()


cursor.close()
conn.close()