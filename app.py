from flask import Flask, render_template, request, session
import webbrowser

import sys

sys.path.append('./scripts')  # Append the scripts folder to the sys.path


from AppRecruitSearcher import *
#from FlipAppRecruitSearcher import * #use during the flip when Stat tables are not updated yet
from heightconverter import *

app = Flask(__name__)


@app.route('/')
def form():
    # Render the HTML form located in the 'templates' folder
    return render_template('RecruitPage.html')  # Make sure the HTML file is here

@app.route('/search', methods=['POST'])
def search():
    # Retrieve form data
    wantedYear = request.form.get('recruitYear')
    wantedRegion = request.form.get('region')
    recruited = request.form.get('isRecruited')
    
    
    developmentDiff = int(request.form.get('minDevelopment', 0))  
    min_potential = int(request.form.get('minPotential', 0))  
    min_si = int(request.form.get('minSI', 0))  
    min_height = request.form.get('minHeight')
    min_wingspan = request.form.get('minWingspan')
    min_vertical = request.form.get('minVertical')
    inside_shooting = request.form.get('InsideShooting')
    outside_shooting = request.form.get('OutsideShooting')
    rangeVal = request.form.get('Range')
    rebounding = request.form.get('Rebounding')
    plus_defense = request.form.get('PlusDefense')
    inside_defense = request.form.get('InsideDefense')
    perimeter_defense = request.form.get('PerimeterDefense')
    iq = request.form.get('IQ')
    passing = request.form.get('Passing')
    handling = request.form.get('Handling')
    speed = request.form.get('Speed')
    far_home = request.form.get('FarHome')
    early_commit = request.form.get("EarlyCommit")
    close_home = request.form.get("CloseHome")
    min_measureableDiff = request.form.get("MeasureableDiff") #Big Man Measureable Ratio
    pace = request.form.get("Pace")


    
    playersFoundArr = recruitSearchFunction(wantedYear, wantedRegion, recruited, developmentDiff, min_potential, min_si, min_height, min_wingspan, min_vertical,
                 inside_shooting, outside_shooting, rangeVal, rebounding, plus_defense, inside_defense, 
                 perimeter_defense, iq, passing, handling, speed, far_home,early_commit,close_home,min_measureableDiff,pace)

 

    return render_template('PlayerResultPage.html', players=playersFoundArr)




if __name__ == '__main__':
    app.run(port=5001)
    app.run(debug=True)
