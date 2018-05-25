#!/usr/bin/env python3
import logging
import argparse

from log_analysis.database import DBConnection

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")


parser = argparse.ArgumentParser()
parser.add_argument(
    '-a', '--answer', nargs='+', choices=['1', '2', '3', 'all'], default='all')
parser.add_argument(
    '-o', '--output-file', nargs='?')
parser.add_argument(
    '-w', '--web', action='store_true')
args = parser.parse_args()
logging.debug(args)


def main():
    if args.web:
        from log_analysis.webserver import app
        # DOESN'T WORK WITH A VAGRANT INSTANCE
        # import webbrowser
        # webbrowser.open_new('0.0.0.0:5000')
        app.run(host='0.0.0.0', port=5000)
    else:
        with_console()


def with_console():
    with DBConnection() as conn:
        answers = []
        if '1' in args.answer:
            answers.append(answer1(conn))
        if '2' in args.answer:
            answers.append(answer2(conn))
        if '3' in args.answer:
            answers.append(answer3(conn))
        if 'all' in args.answer:
            answers = answer_all(conn)
        if args.output_file:
            output_to_file(answers)
        else:
            for item in answers:
                print(item['question'])
                for i in item['answers']:
                    print(i)
                print('')


def answer_all(conn):
    answers = []
    answers.append(answer1(conn))
    answers.append(answer2(conn))
    answers.append(answer3(conn))
    return answers


def output_to_file(answers):
    with open(args.output_file, 'w') as f:
                for item in answers:
                    f.write(item['question'] + '\n')
                    for i in item['answers']:
                        f.write(i + '\n')
                    f.write("\n")


def answer1(conn):
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
    answers = []
    for item in data:
        name = item[0][9:].replace("-", " ").title()
        views = item[1]
        answers.append("'{}' — {} views".format(name, views))
    cur.close()
    return {
        'question': "1. What are the most popular three articles of all time?",
        'answers': answers
    }


def answer2(conn):
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
    answers = []
    for item in data:
        name = item[0]
        views = item[1]
        answers.append("'{}' — {} views".format(name, views))
    cur.close()
    return {
        'question': "2. Who are the most popular article authors of all time?",
        'answers': answers
    }


def answer3(conn):
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
    answers = []
    for item in data:
        day = item[0].strftime('%a %d %Y')
        percentage = item[1]
        answers.append("'{}' — {}% errors".format(day, round(percentage, 2)))
    cur.close()
    return {
        'question': "3. On which days did more than 1% of requests lead \
to errors?",
        'answers': answers
    }


if __name__ == "__main__":
    main()
