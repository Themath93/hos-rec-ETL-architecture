#!/bin/bash


if [ $1 == "naverDocid" ]; then
	echo "naver_docid.py begin"
	python3 /home/worker/python_crawling/app/datajob/extract/crawl_docIds.py
elif [ $1 == "crawlQuestion" ]; then
	echo "crawl_questions.py begin"
	python3 /home/worker/python_crawling/app/datajob/extract/crawl_questions.py $2 
fi
