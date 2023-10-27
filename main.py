from flask import Flask, render_template, request, redirect, jsonify, make_response, url_for, Response
import db, datetime, pytz

app = Flask(__name__)

@app.route('/new_cafe', methods=['POST', 'GET']) 
def new_cafe():
    
    if request.method == "POST":
        form = request.form.to_dict()
        
        if "cafe_name" in form.keys() and "number_of_customers" in form.keys() and "average_spend" in form.keys():
            current_datetime = datetime.datetime.now(tz=pytz.timezone("Asia/Almaty"))
            current_datetime = current_datetime.replace(tzinfo=None)
            
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
            
            total_revenue = db.insert_cafe(form)
            
            return jsonify({"total_revenue": total_revenue})
            
        else:
            return Response(response="Missing field(s) in the form", status = 400)
        
    else:
        return Response(status=403)
    
@app.route('/last_cafes', methods=['GET']) 
def last_five_cafes():
    
    if request.method == "GET":
        return jsonify(db.get_last_five_cafes())


if __name__ == '__main__':
    app.run(debug=True)