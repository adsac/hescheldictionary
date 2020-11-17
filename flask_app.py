from flask import Flask, render_template, request, Markup
import sqlite3

app = Flask(__name__, template_folder="templates")




@app.route("/hescheldictionary", methods=["GET", "POST"])
def index():
    """main search page"""

    #load the Hebrew word list into memory

    try:
        #get list of terms from database

        sqliteConnection = sqlite3.connect('dictionary.db')
        cursor = sqliteConnection.cursor()

        cursor.execute("SELECT Term FROM dictionary ORDER BY Term")

        

        # get list of tuples
        tempwordlist = cursor.fetchall()

        cursor.close()

        #convert to plain list
        wordlist = []
        
        for word in tempwordlist:
            wordlist.append(word[0])



    except:
        return render_template("index.html")

    # search page
    if request.method=="GET":       
        
        return render_template("index.html", wordlist=wordlist)

    # run search query and go to result page
    elif request.method=="POST":

        # get the word from the user and ensure it is valid
        try:
            hebword = request.form.get("hebword")
        except:
            return render_template("index.html")

        # look up word in Database

        try:
            sqliteConnection = sqlite3.connect('dictionary.db')
            cursor = sqliteConnection.cursor()

            cursor.execute("SELECT Term, Entry FROM dictionary WHERE Term=?", (hebword,))
            full_entry = cursor.fetchall()

            cursor.close()

        except:
            return render_template("index.html")

        finally:
            if (sqliteConnection):
                sqliteConnection.close()

                if len(full_entry) == 1:
                    # if there is exactly one Entry
                    if len(full_entry[0]) == 2:
                        hebrew = full_entry[0][0]
                        english = full_entry[0][1]
                elif len(full_entry) > 1:
                    # if there are more than one entry
                    hebrew = full_entry[0][0]
                    english=""
                    count = 1
                    for entry in full_entry:
                        english += f"{count}. {entry[1]}<br>"
                        count += 1
                else:
                    # no entry found
                    hebrew = hebword
                    english = "Entry not found"

            english=Markup(english)
            return render_template("result.html", english=english, hebrew=hebrew, wordlist=wordlist)

@app.route("/hescheldictionary/about")
def about():
    """about page"""
    return render_template("about.html")

