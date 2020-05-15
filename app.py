from flask import Flask, render_template, request, Response
import csv

app = Flask(__name__, static_folder="static", static_url_path="")



@app.route('/')
def upload_file():
    return render_template('index.html')


@app.route('/result', methods=['GET', 'POST'])
def upload_file_test():
    if request.method == 'POST':
        f = request.files['file']
        text = f.read().decode("utf-8")

        text = text.split('\n')
        text = csv.reader(text)

        text = list(text)

        # change text from here


        textList = list(text)

        headerList = text[0]
        del text[0]
        del text[-1]


        file = open('output.txt',"w+")
        for value in textList:
            for i in value:
                file.write(i +',')
            file.write('\n')

        button = """
        <form action="/getPlotCSV">
    <input type="submit" value="Download results" />
</form>
"""

        return render_template('index.html',my_list=text,headerList=headerList, download=button)

@app.route("/getPlotCSV")
def getPlotCSV():
    with open("output.txt") as fp:
         csv = fp.read()

    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=myplot.csv"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

