from app import MONGODB_THRESHOLD, app, db, mongo_logs_collection
from flask import render_template, request, jsonify, url_for, redirect
from datetime import datetime
from helper import get_data_size
from models import *

@app.route('/')
def home():
    return redirect(url_for("search_logs"))

@app.route('/ingest', methods=['GET', 'POST'])
def ingest_log():
    if request.method == "POST":
        try:
            log_data = request.get_json()
            
            data_size = get_data_size(log_data)

            try:
                if data_size > MONGODB_THRESHOLD:
                    # Data size is large, add it to MongoDB
                    mongo_logs_collection.insert_one(log_data)
                else:
                    # Data size is small, add it to MySQL
                    mysql_log = LogMySQL(
                        level=log_data['level'],
                        message=log_data['message'],
                        resourceId=log_data['resourceId'],
                        timestamp=datetime.now(),
                        traceId=log_data['traceId'],
                        spanId=log_data['spanId'],
                        commit=log_data['commit'],
                        parentResourceId=log_data['metadata.parentResourceId']
                    )
                    db.session.add(mysql_log)
                    db.session.commit()
            except Exception as mongo_error:
                # Log the MongoDB-specific error
                app.logger.error(f"MongoDB Error: {str(mongo_error)}")

                # Try adding the data to MySQL in case MongoDB fails
                mysql_log = LogMySQL(
                    level=log_data['level'],
                    message=log_data['message'],
                    resourceId=log_data['resourceId'],
                    timestamp=datetime.now(),
                    traceId=log_data['traceId'],
                    spanId=log_data['spanId'],
                    commit=log_data['commit'],
                    parentResourceId=log_data['metadata.parentResourceId']
                )
                db.session.add(mysql_log)
                db.session.commit()

            return jsonify({'status': 'success'})

        except Exception as e:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            app.logger.error(f"Error at {timestamp}: {str(e)}")
            return jsonify({'status': 'error', 'message': str(e)})
    return render_template('ingest.html')

@app.route('/search', methods=['GET', 'POST'])
def search_logs():
    try:
        if request.method == 'GET':
            try:
                mongo_result = list(mongo_logs_collection.find())
                mysql_result = LogMySQL.query.all()
                return render_template('search.html', mongo_logs=mongo_result, mysql_logs=mysql_result)
            except Exception as mongo_error:
                app.logger.error(f"MongoDB Error: {str(mongo_error)}")
                try:
                    # Try fetching data from MySQL in case MongoDB fails
                    mysql_result = LogMySQL.query.all()
                
                except Exception as mysql_error:
                    mongo_result = list(mongo_logs_collection.find())
                    app.logger.error(f"MySQL Error: {str(mysql_error)}")
                    return render_template('search.html', mongo_logs=mongo_result, mysql_logs=[])
                    # return jsonify({'status': 'error', 'message': f"Error fetching data: {str(mysql_error)}"})

        elif request.method == 'POST':
            query = build_query(request.form)
            mongo_result = list(mongo_logs_collection.find(query))
            
            try:
                mysql_result = LogMySQL.query.filter_by(**query).all()
            except Exception as mysql_error:
                app.logger.warning(f"MySQL error while searching logs: {str(mysql_error)}")
                mysql_result = []

            return render_template('search.html', form_value=request.form, mongo_logs=mongo_result, mysql_logs=mysql_result)
    except Exception as e:
        app.logger.error(f"Error searching logs: {str(e)}")


def build_query(form_data):
    query = {}
    for field, value in form_data.items():
        if value and field != 'submit':
            if field == 'start_date':
                start_date = datetime.strptime(value, '%Y-%m-%d')
                query['timestamp'] = {'$gte': start_date}
            elif field == 'end_date':
                end_date = datetime.strptime(value, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
                query.setdefault('timestamp', {}).update({'$lte': end_date})
            elif field == 'message':
                query[field] = {'$regex': value, '$options': 'i'}
            else:
                query[field] = value
    return query
