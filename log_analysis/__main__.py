#!/usr/bin/env python3
import psycopg2
import logging
import argparse

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")

DBNAME = 'news'

parser = argparse.ArgumentParser()
parser.add_argument(
    '-a', '--answer', nargs='+', choices=['1', '2', '3', 'all'])
parser.add_argument(
    '-o', '--output-file', nargs='?')
args = parser.parse_args()
logging.debug(args)


def main():
    conn = psycopg2.connect("dbname=%s" % (DBNAME,))
    answer = []
    if '1' in args.answer or 'all' in args.answer:
        answer1(conn, answer)
    if '2' in args.answer or 'all' in args.answer:
        answer2(conn, answer)
    if '3' in args.answer or 'all' in args.answer:
        answer3(conn, answer)
    if args.output_file:
        with open(args.output_file, 'w') as f:
            for i in answer:
                f.write(i)
                f.write("\n")
    else:
        for i in answer:
            print(i)
    conn.close()


def answer1(conn, answer):
    answer.append("1. What are the most popular three articles of all time?")
    cur = conn.cursor()
    cur.execute("""
        SELECT path, COUNT(*) AS num FROM log
        GROUP BY path
        HAVING path LIKE '/article/%'
        ORDER BY num DESC
        LIMIT 3
    """)
    data = cur.fetchall()
    logging.debug(data)
    for i in data:
        name = i[0][9:].replace("-", " ").title()
        views = i[1]
        answer.append("'{}' — {} views".format(name, views))
    cur.close()
    return answer


def answer2(conn, answer):
    answer.append("2. Who are the most popular article authors of all time?")
    cur = conn.cursor()
    cur.execute("""
        SELECT authors.name, SUM(subq.num) as total
        FROM authors, articles, (
            SELECT SUBSTR(log.path, 10, 250) as path, COUNT(path) AS num
            FROM log
            GROUP BY log.path
            HAVING log.path LIKE '/article/%'
            ORDER BY num DESC
        ) subq
        WHERE articles.slug=subq.path
        AND articles.author=authors.id
        GROUP BY authors.name
        ORDER BY total DESC
    """)
    data = cur.fetchall()
    logging.debug(data)
    for i in data:
        name = i[0]
        views = i[1]
        answer.append("'{}' — {} views".format(name, views))
    cur.close()
    return answer


def answer3(conn, answer):
    answer.append("On which days did more than 1% of requests lead to errors?")
    cur = conn.cursor()
    cur.execute("""
        SELECT date_trunc('day', log.time) AS dday,
            100.0 * (SUM(nok.num) / SUM(ok.num)) AS percentage
        FROM log, (
            SELECT date_trunc('day', time) AS day, COUNT(*) AS num
            FROM log
            WHERE status='200 OK'
            GROUP BY day
        ) ok, (
            SELECT date_trunc('day', time) AS day, COUNT(*) AS num
            FROM log
            WHERE status!='200 OK'
            GROUP BY day
        ) nok
        WHERE date_trunc('day', log.time)=ok.day
        AND date_trunc('day', log.time)=nok.day
        GROUP BY dday
        HAVING 100.0 * (SUM(nok.num) / SUM(ok.num)) > 1
    """)
    data = cur.fetchall()
    logging.debug(data)
    for i in data:
        day = i[0].strftime('%a %d %Y')
        percentage = i[1]
        answer.append("'{}' — {}% errors".format(day, round(percentage, 2)))
    cur.close()
    return answer


if __name__ == "__main__":
    main()
