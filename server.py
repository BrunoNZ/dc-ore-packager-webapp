from dc_ore_packager import DCOREPackager
from flask import Flask, render_template, request, send_file
from urllib.parse import urlparse

app = Flask(__name__)

pkg = DCOREPackager('http://demo.dspace.org', '10673/123123' )
x = pkg.getPackage()
print(x)

def parseURL(fullURL):
    o = urlparse(fullURL)
    baseURL = "://".join([o.scheme,o.netloc])
    handle = o.path.rsplit("/handle/").pop()
    return {"base":baseURL, "handle":handle}

@app.route("/")
def homepage():
    return render_template('home.html')

@app.route("/get")
def get_package():
    fullURL = request.args.get("fullurl")
    url = parseURL(fullURL)
    pkg = DCOREPackager(url['base'], url['handle'])
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
    app.run()
