#!/bin/bash

set -e
cd corners442
python3 schema.py

sleep 3
scrapy crawl league
sleep 10
scrapy crawl fourfourtwo