from dc_ore_packager import DCOREPackager
from flask import Flask, render_template, request, send_file
from urllib.parse import urlparse
from identifier_exceptions import idExceptions


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '553C1E52E8EDE813163D5CE322BBE'


def parseUrlList(urlList):
    handleList = []
    baseUrlList = []
    for url in urlList:
        o = urlparse(url)
        baseUrlList.append("://".join([o.scheme,o.netloc]))
        handleList.append(o.path.rsplit("/handle/").pop())

    baseURL = baseUrlList[0]
    for i in range(1,len(baseUrlList)):
        if (baseURL != baseUrlList[i]):
            raise

    return {"baseURL":baseURL, "handleList":handleList}


@app.route("/", methods=['GET','POST'])
def get_package():

    if request.method == 'GET':
        return render_template('home.html')

    else:
        urlList = request.form.get('urlList').splitlines()
        useIdPrefix = request.form.get('useIdPrefix') is not None
        repo = parseUrlList(urlList)
        pkg = DCOREPackager(repo['baseURL'], repo['handleList'],
                            idExceptions=idExceptions,
                            useIdPrefix=useIdPrefix,
                            verifySSL=False,
                            debug=True)
        ofile = pkg.getPackage()
        if (ofile is not None):
            return send_file(
                ofile,
                as_attachment=True,
                mimetype="application/zip",
                attachment_filename="item.zip")
        else:
            return render_template('home.html', error='Item not found')


if __name__ == "__main__":
    app.run(debug=False)
