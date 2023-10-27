from flask import Flask, render_template, request, redirect, jsonify, make_response, url_for, Response
import db, datetime, pytz

app = Flask(__name__)

#Input: POST form with "cafe_name", "number_of_customers" and "average_speed" fields
#Output: calculated total revenue
#Note: adding endpoint new_cafe to receive POST request with new cafe information
@app.route('/new_cafe', methods=['POST']) 
def new_cafe():
    
    form = request.form.to_dict()
    
    #Check that all necessary fields in the request, if not return proper error message
    if "cafe_name" in form.keys() and "number_of_customers" in form.keys() and "average_spend" in form.keys():
        current_datetime = datetime.datetime.now(tz=pytz.timezone("Asia/Almaty"))
        current_datetime = current_datetime.replace(tzinfo=None)
        
        #Check that number_of_customers and average_spend are numbers, if not return error message
        try:
            number_of_customers = int(form['number_of_customers'])
        except:
            return Response(response="Number of customers is not number", status = 400)
        
        try:
            average_spend = float(form['average_spend'])
        except:
            return Response(response="Average spend per customer is not number", status = 400)
        
        form.update({
            "number_of_customers": number_of_customers,
            "average_spend": average_spend,
            "datetime": current_datetime
        })
        
        #Insert new cafe into database
        total_revenue = db.insert_cafe(form)
        
        #Return Total revenue to the frontend
        return jsonify({"total_revenue": total_revenue})
        
    else:
        #Return error message
        return Response(response="Missing field(s) in the form", status = 400)
        
#Input: GET request
#Output: last 5 cafe total revenue calculations with cafe name and total revenue
@app.route('/last_cafes', methods=['GET']) 
def last_five_cafes():
    
    if request.method == "GET":
        #Return last five total revenue calculations
        return jsonify(db.get_last_five_cafes())


if __name__ == '__main__':
    app.run(debug=True)