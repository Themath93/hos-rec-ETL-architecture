#!/bin/bash


if [ $1 == "naverDocid" ]; then
	echo "naver_docid.py begin"
	python3 /home/worker/python_crawling/app/datajob/extract/crawl_docIds.py
elif [ $1 == "crawlQuestion" ]; then
	echo "crawl_questions.py begin"
	python3 /home/worker/python_crawling/app/datajob/extract/crawl_questions.py $2 
elif [ $1 == "Gathering" ]; then
	echo "save_hdfs.py begin"
	python3 /home/worker/python_crawling/app/datajob/extract/save_hdfs.py
	ssh hosapp sudo rm -r /home/worker/python_crawling/app/data/docIds*
	ssh hosapp sudo rm -r /home/worker/python_crawling/app/data/_crawl*
elif [ $1 == "Save" ]; then
	echo "write_file_to_hdfs"
	ssh namenode /home/worker/hadoop/bin/hdfs dfs -put /home/worker/volume/crawl-data/subjective_questions* /data/naver_crawl
	sudo rm /home/worker/volume/crawl-data/subjective_questions*
elif [ $1 == "Transform" ]; then
	python3 /home/worker/python_crawling/app/datajob/transform/transform.py
fi
