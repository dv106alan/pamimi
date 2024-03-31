#!/bin/bash

export SPATH="/home/alan/python/pyCrawler/pamimi/app"
source /home/alan/python/spider-venv/bin/activate
cd $SPATH
# IG reels
# python3 $SPATH/ig/reels/ig_spider_charli_get_list.py 60
# python3 $SPATH/ig/reels/ig_spider2_charli_get_post.py 50
# python3 $SPATH/ig/reels/ig_spider_dannybeeech_get_list.py 60
# python3 $SPATH/ig/reels/ig_spider2_dannybeeech_get_post.py 50

# IG post
# python3 $SPATH/ig/posy/charlie/ig_charlie_post.py
# python3 $SPATH/ig/posy/charlie/ig_danny_post.py

# YT
# python3 $SPATH/yt/charlie/cra.py
# python3 $SPATH/yt/Dannybeeech/cra.py

# FB
# python3 $SPATH/fb/fb_charlene.py
# python3 $SPATH/fb/fb_danny.py

# sync sql & gcp sql
python3 $SPATH/sql_sync.py

