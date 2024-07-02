from flask import Flask, render_template, request, session
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/')
def login():
    return render_template("index.html")

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        user_id = int(request.form["userid"])
        session['user_id'] = user_id

        contactList = []
        addressList = []
        nameList = []
        emailList = []
        df = pd.read_csv("data.csv")
        for i in range(df.shape[0]):
            if df.iloc[i]['user_id'] == user_id:
                contactList.append(df.iloc[i]['number'])
                addressList.append(df.iloc[i]['address'])
                nameList.append(df.iloc[i]['name'])
                emailList.append(df.iloc[i]['email'])
        return render_template('phoneBook.html', contactList=contactList, addressList=addressList, nameList=nameList,
                               emailList=emailList)


@app.route('/submitoptions', methods=['POST', 'GET'])
def checkOptions():
    option = request.form['options']

    user_id = session.get('user_id')
    contactList = []
    addressList = []
    nameList = []
    emailList = []
    df = pd.read_csv("data.csv")
    for i in range(df.shape[0]):
        if df.iloc[i]['user_id'] == user_id:
            contactList.append(df.iloc[i]['number'])
            addressList.append(df.iloc[i]['address'])
            nameList.append(df.iloc[i]['name'])
            emailList.append(df.iloc[i]['email'])
    return render_template('phoneBook.html',contactList=contactList, addressList=addressList, nameList=nameList, emailList=emailList, option=option)

@app.route('/addData', methods=['POST', 'GET'])
def addData():
    user_id = session.get('user_id')
    if request.method == 'POST':
        df = pd.read_csv("data.csv")
        user_id = session.get('user_id')
        contact = request.form["contact"]
        name = request.form['name']
        email = request.form['email']
        address = request.form["address"]
        new_data = pd.DataFrame([[int(user_id), name, email, contact, address]],columns=['user_id','name','email','number','address'])
        df = pd.concat((df, new_data))
        df.to_csv("data.csv", index=False)

    df = pd.read_csv("data.csv")
    contactList = []
    addressList = []
    nameList = []
    emailList = []
    for i in range(df.shape[0]):
        if df.iloc[i]['user_id'] == user_id:
            contactList.append(df.iloc[i]['number'])
            addressList.append(df.iloc[i]['address'])
            nameList.append(df.iloc[i]['name'])
            emailList.append(df.iloc[i]['email'])
    return render_template('phoneBook.html',contactList=contactList, addressList=addressList, nameList=nameList, emailList=emailList)

@app.route('/dropData', methods=['POST', 'GET'])
def dropData():
    user_id = session.get('user_id')
    if request.method == 'POST':
        df = pd.read_csv("data.csv")
        user_id = session.get('user_id')
        contact = request.form["contact"]

        new_df = pd.DataFrame(columns=['user_id','number','address'])
        for i in range(df.shape[0]):
            if (df.iloc[i]['user_id'] == user_id and df.iloc[i]['number']== int(contact)):
                pass
            else:
                new_df = pd.concat((new_df,pd.DataFrame([[df.iloc[i]['user_id'], df.iloc[i]['number'],df.iloc[i]['name'],df.iloc[i]['email'],df.iloc[i]['address']]], columns=['user_id', 'number','name','email', 'address'])))
        new_df.to_csv("data.csv")

    df = pd.read_csv("data.csv")
    contactList = []
    addressList = []
    nameList = []
    emailList = []
    for i in range(df.shape[0]):
        if df.iloc[i]['user_id'] == user_id:
            contactList.append(df.iloc[i]['number'])
            addressList.append(df.iloc[i]['address'])
            nameList.append(df.iloc[i]['name'])
            emailList.append(df.iloc[i]['email'])
    return render_template('phoneBook.html',contactList=contactList, addressList=addressList, nameList=nameList, emailList=emailList)

if __name__ == '__main__':
    app.run(debug=True)