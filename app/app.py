import sys

sys.path.append("..")

from flask import Flask, render_template, request, Response
import csv
import mysql.connector
from parse_to_db import main
from db_checker import checkDatabase
from MySqlCon import MySqlCon

app = Flask(__name__)


@app.route('/')
def upload_file():
    """
    this is the standard page where the main page is loaded
    :return:
    """
    checkDatabase()
    main()

    return (render_template('index.html'))


@app.route('/result', methods=['GET', 'POST'])
def upload_file_test():
    """
    After the user submits a file this function is called to treat and return the data
    :return:
    """
    if request.method == 'POST':

        f = request.files['file']

        text = f.read().decode("utf-8")

        text = text.split('\n')
        text = csv.reader(text)

        text = list(text)

        # change text from here
        headerList = []
        output = [[]]
        con = MySqlCon()


        headerList = text[0]
        text = text[1:]


        results = []
        for line in text:
            chromosome = line[0]
            position = line[1]
            changeFrom = line[2]
            changeTo = line[3]

            results += list(con.execute_res("""
            SELECT * 
            FROM alleleVariants
            WHERE chromosome = '{chromosome}'
            AND location = '{position}'
            AND reference = '{changeFrom}'
            AND alternative = '{changeTo}';
            
            """.format(chromosome=chromosome,position=position,changeFrom=changeFrom,changeTo=changeTo)))

        #result = list(con.execute_res('SELECT * from alleleVariants'))

        text = results

        file = open('output.txt', "w+")
        for value in output:
            for i in value:
                file.write(i + ',')
            file.write('\n')

        button = """
        <form action="/getPlotCSV">
    <input type="submit" value="Download results" />
</form>
"""

        return render_template('index.html', my_list=text, headerList=headerList, download=button)


@app.route("/getPlotCSV")
def getPlotCSV():
    """
    This function is called to return the found data.
    :return:
    """
    with open("output.txt") as fp:
        csv = fp.read()

    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                     "attachment; filename=myplot.csv"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
