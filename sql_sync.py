from mysqldb import SQLDB
from util import read_csv_line_by_line, remove_special_emoji
import csv

sqldb = SQLDB(host="localhost", port=3306, 
              user="root", password="123456", 
              db_name="pamimi")

sqldb_gcp = SQLDB(host="104.199.204.10", port=3306, 
              user="pamimi", password="000000", 
              db_name="pamimidb")

# IG Reels backup
# Iterate over each line in the CSV file
file_path = "output_ig_coindevanity_reels_post.csv"
table_name = "ig_reels_charlene"
columns = "url,likes,views,content,datetime"
for line in read_csv_line_by_line(file_path):
    text = remove_special_emoji(line[3])
    value = f"""("{line[0]}","{line[1]}","{line[2]}","{text.rstrip()}","{line[4].rstrip()}")"""
    sqldb.sql_update_table(table_name, columns, value)
    sqldb_gcp.sql_update_table(table_name, columns, value)
    
file_path = "output_ig_dannybeeech_reels_post.csv"
table_name = "ig_reels_danny"
columns = "url,likes,views,content,datetime"
for line in read_csv_line_by_line(file_path):
    text = remove_special_emoji(line[3])
    value = f"""("{line[0]}","{line[1]}","{line[2]}","{text.rstrip()}","{line[4].rstrip()}")"""
    sqldb.sql_update_table(table_name, columns, value)
    sqldb_gcp.sql_update_table(table_name, columns, value)

# YT
file_path = "Charlie_video_info.csv"
table_name = "yt_charlene"
columns = "title,views,date,likes,comments"

for line in read_csv_line_by_line(file_path):
    text = remove_special_emoji(line[0])
    value = f"""("{text}","{line[1]}","{line[2]}","{line[3]}","{line[4]}")"""
    sqldb.sql_update_table(table_name, columns, value)
    sqldb_gcp.sql_update_table(table_name, columns, value)

file_path = "Dannybeeech_video_info.csv"
table_name = "yt_danny"
columns = "title,views,date,likes,comments"

for line in read_csv_line_by_line(file_path):
    text = remove_special_emoji(line[0])
    value = f"""("{text}","{line[1]}","{line[2]}","{line[3]}","{line[4]}")"""
    sqldb.sql_update_table(table_name, columns, value)
    sqldb_gcp.sql_update_table(table_name, columns, value)

# FB
file_path = "fb_charlie.csv"
table_name = "fb_data"
columns = "title,date,content,likes,comments"

for line in read_csv_line_by_line(file_path):
    text = remove_special_emoji(line[2])
    value = f"""("{line[0]}","{line[1]}","{text}","{line[3]}","{line[4]}")"""
    sqldb.sql_update_table(table_name, columns, value)
    sqldb_gcp.sql_update_table(table_name, columns, value)

file_path = "fb_danny.csv"
for line in read_csv_line_by_line(file_path):
    text = remove_special_emoji(line[2])
    value = f"""("{line[0]}","{line[1]}","{text}","{line[3]}","{line[4]}")"""
    sqldb.sql_update_table(table_name, columns, value)
    sqldb_gcp.sql_update_table(table_name, columns, value)

# IG post
file_path = "ig_data_charlie.csv"
table_name = "ig_charlene"
columns = "likes,date,comments,hashtags,content"

for line in read_csv_line_by_line(file_path):
    content = remove_special_emoji(line[4])
    hashtag = remove_special_emoji(line[3])
    value = f"""("{line[0]}","{line[1]}","{line[2]}","{hashtag}","{content}")"""
    sqldb.sql_update_table(table_name, columns, value)
    sqldb_gcp.sql_update_table(table_name, columns, value)

file_path = "ig_data_danny.csv"
table_name = "ig_danny"
columns = "likes,date,comments,hashtags,content"

for line in read_csv_line_by_line(file_path):
    content = remove_special_emoji(line[4])
    hashtag = remove_special_emoji(line[3])
    value = f"""("{line[0]}","{line[1]}","{line[2]}","{hashtag}","{content}")"""
    sqldb.sql_update_table(table_name, columns, value)
    sqldb_gcp.sql_update_table(table_name, columns, value)


