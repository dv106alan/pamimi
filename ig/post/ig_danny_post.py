import instaloader
import csv
L = instaloader.Instaloader() 
L.login('user', 'pwd')
profile = instaloader.Profile.from_username(L.context, "dennybeeech")
#取得post迭代物件
post_iterator = profile.get_posts()
print(profile.followers)

with open('ig_data_danny.csv', mode='w', newline='', encoding='utf-8-sig') as file:

    writer = csv.writer(file)
    # 寫入標題列
    writer.writerow(['Like Count', 'Post Date', 'Comment Count', 'Hashtags','content'])
    print(len(post_iterator))
    # 每個貼文寫入一列
    for post in post_iterator:
        # 得到所有的 hashtags
        # hashtags = [tag for tag in post.caption_hashtags]
        # 寫入資料  #2023-2024年
         if post.date.year == 2023 or post.date.year == 2024:
            writer.writerow([post.likes, post.date, post.comments, post.caption_hashtags, post.caption])
    print("end...")