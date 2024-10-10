from flask import Flask, request, render_template, render_template_string

app = Flask(__name__)

try:
    FLAG = open('flag.txt', 'r').read()
except:
    FLAG = '[**FLAG**]'

app.secret_key = FLAG

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    r = request.args.get('search')

    template = """
	<!DOCTYPE html>
	<html>
		<head>
			<meta charset="utf-8">
			<title>Search Page</title>
		</head>
		<body>
			<h1> %s page is not found. </h1>
		</body>
	</html>""" %r

    blacklist = ["{{config['secret_key']}}", "{{config.items()}}"]

    for i in blacklist:
        if r.lower() == i:
            return "I think that is bad idea.."
        
    return render_template_string(template)
    

app.run(host = "0.0.0.0", port = 5000, debug=True)
