@app.route('/parse', methods=['POST'])
def parse():
    if request.method == 'POST':
        try:
            id = request.form['id']
            print(id)
