from flask import Flask,render_template,request,redirect
from utils import *
import datetime


app = Flask(__name__)

#  Routes
@app.route('/')
def index():
    bgs = get_relevant_bg()
    date = datetime.date.today().strftime("%d - %m - %Y")
    err = False
    try:
        day = get_daily_data()
        days = get_weekly_data()
        week_days = [datetime.datetime.utcfromtimestamp(day['dt']).strftime('%A') for day in days]
        bg = day['weather'][0]['description']
    except ValueError:
        err = True
        print("value exception")
        # return "Input Error mate.There is no such city. Please try again later."
    except ConnectionError:
        err = True
        print("connection exception")
        # return "Looks like there is no Internet Connection mate."
    except Exception:
        print("default exception")
        err = True
        
    if err:
        return  render_template('index.html',err=err)
    else:     
        return  render_template('index.html',day=day,days=days,bg=bgs[bg],week_days=week_days,date=date,err=err)

@app.route('/', methods=['POST'])
def get_user_input():
    if request.method == 'POST':
        city = request.form.get('city')
        if city == "":
            print("city cannot be empty")
            return redirect(request.referrer)    
        api['city'] = city
        return redirect(request.referrer)
    

if __name__ == '__main__':
    app.run(host="0.0.0.0",port="5000")
