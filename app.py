from flask import Flask, render_template, request, session
import requests
from bs4 import BeautifulSoup

lst = []
arr = []

app = Flask(__name__)

app.secret_key = '02051105'

def fetch_gfg_details(Username):
    try:
        url = f"https://www.geeksforgeeks.org/user/{Username}/"
        response = requests.get(url) 
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser') 

        user = soup.find('div', class_='profilePicSection_head_userHandle__oOfFy')
        rank = soup.find('span', class_='educationDetails_head_left_userRankContainer--text__wt81s')
        streak = soup.find('div', class_='circularProgressBar_head_mid_streakCnt__MFOF1 tooltipped')

        nav_bar = soup.find('div')
        ssr = nav_bar.find_all(class_ = "scoreCard_head_left--score__oSi_x")

        if user:
            lst.append({
                'username': user.text.strip(),
                'score' : ssr[0].text.strip(),
                'rank': rank.text.strip() if rank else 'N/A',
                'streak': streak.text.strip(),
                'solved' : ssr[1].text.strip(),
                'rating' : ssr[2].text.strip()
            })

        print(lst)        ### Print the Details of the User

        return lst if lst else None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Error occurred: {req_err}")
    except AttributeError:
        print("Unable to find user details. Please check the username or the HTML structure.")


@app.route('/', methods=["GET", "POST"])
def submit():
    global arr
    if 'users' not in session:
        session['users'] = []

    if request.method == "POST":
        username = request.form['username']

        if username in arr:                 ###  check if user already in list or not
            return render_template('index.html',name="Guys!" , found = "User already exists in table!" , data = None)

        fetch_details = fetch_gfg_details(username)
        arr.append(username)
        
        if fetch_details:
            for x in fetch_details:
                session['users'].append(x) 

    users_data = session['users']
    return render_template('index.html', name = "Guys!", found = "" , data = users_data)
        
if __name__ == '__main__':
    app.run(debug=True)