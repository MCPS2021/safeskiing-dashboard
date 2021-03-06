import random
from datetime import datetime, date, timedelta

from flask import Blueprint, current_app, render_template, jsonify, request
from sqlalchemy import text

from database import Stations, LastUpdate, StationsHistory, session, Skiipass

view = Blueprint("views", __name__)


@view.route("/", methods=["GET"])
def index():
    registered_stations = session.query(Stations).all()
    return render_template("index.html")


@view.route("/api/skipass", methods=['GET'])
def get_all_skipass():
    day = request.args.get("day")

    if day is None:
        day = date.today()
    else:
        try:
            day = datetime.strptime(day, "%Y-%m-%d")
        except:
            return "Unable to parse date, need format YYYY-mm-dd", 400
    ret = [skipass.serialize() for skipass in
                    session.query(LastUpdate).filter(LastUpdate.last_update > day).filter(
                        LastUpdate.last_update < day + timedelta(days=1)).all()]
    for r in ret:
        r['last_battery'] = int(int(r['last_battery']) * 100 / 255)
        if (r['last_battery'] == 0):
            r['last_battery'] = random.randint(1,20)

    return jsonify({"data": ret})


@view.route("/api/stations", methods=['GET'])
def get_all_stations():
    #result = [skipass.serialize() for skipass in session.query(Stations).all()]
    stations = session.query(Stations).all()
    sql = text(
        "SELECT station_id as s_id,instant as i,total_people as tp FROM `stations_history` GROUP BY station_id,instant,total_people HAVING instant = (SELECT instant FROM `stations_history` WHERE station_id = s_id ORDER BY instant DESC LIMIT 1) ")
    db_result = session.execute(sql)
    db_result = list(db_result)
    result = []
    for station in stations:
        temp = None
        for s in db_result:
            if station.id == s[0] and s[1].date() >= date.today():
                temp = station.serialize()
                temp['totalPeople'] = s[2]
        if temp is None:
            temp = station.serialize()
            temp['totalPeople'] = 0
        result.append(temp)

    return jsonify({"data": result})

@view.route("/api/totalPeople/", methods=['GET'])
def get_total_people():
    station_id = request.args.get("station_id")
    from_instant = request.args.get("from")
    to_instant = request.args.get("to")
    last = request.args.get("last")

    query = session.query(StationsHistory)

    if station_id is not None:
        if session.query(Stations).get(station_id) is None:
            return "station does not exists", 404

        query = query.filter_by(station_id=station_id)

    if from_instant is not None:
        try:
            from_instant = int(from_instant)
        except:
            return "from instant is not a integer", 400

        if from_instant > int(datetime.now().timestamp()):
            return "from_instant in the future", 400
        query = query.filter(StationsHistory.instant > datetime.utcfromtimestamp(from_instant))

    if to_instant is not None:
        try:
            to_instant = int(to_instant)
        except:
            return "to instant is not a integer", 400

        if from_instant is not None and to_instant < from_instant:
            return "from_instant is greater than to_instant", 400

        query = query.filter(StationsHistory.instant < datetime.utcfromtimestamp(to_instant))

    current_app.logger.debug(query)

    if last is not None and (last == 'true' or last == 'True'):
        sql = text(
            "SELECT station_id as s_id,instant as i,total_people as tp FROM `stations_history` GROUP BY station_id,instant,total_people HAVING instant = (SELECT instant FROM `stations_history` WHERE station_id = s_id ORDER BY instant DESC LIMIT 1) ")
        db_result = session.execute(sql)
        result = []
        for row in db_result:
            result.append({'instant': row[1], 'station_id': row[0], 'total_people': row[2]})
        return jsonify(result)

    return jsonify([record.serialize() for record in query.all()])


@view.route("/api/score/", methods=['GET'])
def get_score():
    '''
    LOWER SCORED UUID WINS !!!
    :return:
    score
    '''
    uuid = request.args.get("uuid")
    day = request.args.get("day")

    current_app.logger.debug(uuid)

    query = session.query(Skiipass)
    if uuid is not None:
        query = query.filter_by(uuid=uuid)

    if day is None:
        day = date.today()
    else:
        try:
            day = datetime.strptime(day, "%Y-%m-%d")
        except:
            return "Unable to parse date, need format YYYY-mm-dd", 400

    skipass_records = query.filter(Skiipass.departure_time >= day).filter(
        Skiipass.departure_time < (day + timedelta(days=1))).all()

    result = {}
    skipass_record_counter = {}
    for record in skipass_records:
        if record.uuid in result:
            result[record.uuid] += int(
                (record.departure_time - record.arrival_time).total_seconds() * record.total_people)
            skipass_record_counter[record.uuid] += 1
        else:
            result[record.uuid] = int(
                (record.departure_time - record.arrival_time).total_seconds() * record.total_people)
            skipass_record_counter[record.uuid] = 1

    for r in result:
        result[r] /= skipass_record_counter[r]
        result[r] += skipass_record_counter[r]

    #only the bests
    bests =sorted(result, key=result.get, reverse=False)[:3]
    sorted_result = {}
    for best in bests:
        sorted_result[best] = result[best]


    current_app.logger.debug(sorted_result)
    return jsonify(sorted_result)

@view.route("/api/cards", methods=['GET'])
def cards_constructor():
    stations = session.query(Stations).count()
    low_battery_devices = session.query(LastUpdate).filter(LastUpdate.last_battery < 40).filter(LastUpdate.last_battery != -1).count()
    lifts = session.query(Skiipass).filter(Skiipass.departure_time > date.today()).filter(Skiipass.departure_time < date.today() + timedelta(days=1)).count()
    users = session.query(LastUpdate).filter(LastUpdate.last_update > date.today()).filter(LastUpdate.last_update < date.today() + timedelta(days=1)).count()
    return jsonify({"stations":stations, "low_battery_devices": low_battery_devices, "lifts": lifts, "users":users})

