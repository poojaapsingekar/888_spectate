import psycopg2

DB_NAME = "888"

def check_if_table_exists(table_name):
    
    """
    This method will connect to the db with the username and the password
    """
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user=postgres password=Apooja@96")
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(table_name.replace('\'', '\'\'')))
    if cur.fetchone()[0] == 1:
        cur.close()
        return True

    cur.close()
    return False

#The below method will create the sport table in the database
def create_sport_table():
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user=postgres password='Apooja@96'")
    cur = conn.cursor()
    cur.execute("CREATE TABLE sport (name varchar(255), slug varchar(255), active bool, num_active_events int, PRIMARY KEY (name));")
    cur.execute('commit')
    conn.close()
    cur.close()

#The below method will create the event table in the database
def create_event_table():
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user=postgres password='Apooja@96'")
    cur = conn.cursor()
    cur.execute("CREATE TABLE event (name varchar(255), slug varchar(255), active bool, type varchar(255), event_sport varchar(255),status varchar(255), scheduled_start varchar(255),actual_start varchar(255),num_active_selections int,PRIMARY KEY (name));")
    cur.execute('commit')
    conn.close()
    cur.close()

#The below method will create the selection table in the database
def create_selection_table():
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user=postgres password='Apooja@96'")
    cur = conn.cursor()
    cur.execute("CREATE TABLE selection (name varchar(255), event varchar(255), price float(5), active bool,outcome varchar(255),PRIMARY KEY (name));")
    cur.execute('commit')
    conn.close()
    cur.close()

#The below method will insert the values in the sport table in the database
def create_sport(name, slug, active, num_active_events=0):
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user=postgres password='Apooja@96'")
    cur = conn.cursor()
    active = "TRUE" if active else "FALSE"
    cur.execute(f"INSERT INTO sport VALUES ('{name}', '{slug}', {active}, {num_active_events})")
    cur.execute('commit')
    conn.close()
    cur.close()

#The below method will insert the values in the event table in the database
def create_event(name,slug,active,type,event_sport,status,scheduled_start,actual_start,num_active_selections=0):
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user=postgres password='Apooja@96'")
    cur = conn.cursor()
    cur.execute(f"INSERT INTO event VALUES ('{name}', '{slug}', {active}, '{type}','{event_sport}','{status}', '{scheduled_start}' ,'{actual_start},{num_active_selections}')")
    cur.execute('commit')
    conn.close()
    cur.close()

#The below method will insert the values in the selection table in the database
def create_selection(name,event,price,active,outcome):
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user=postgres password='Apooja@96'")
    cur = conn.cursor()
    cur.execute(f"INSERT INTO selection VALUES ('{name}', '{event}', {price}, '{active}','{outcome}')")
    cur.execute('commit')
    conn.close()
    cur.close()

#This method is to get the api end points from the sport table
def get_sports_with_namelike(pattern):
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user=postgres password='Apooja@96'")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM sport WHERE name ~ '{pattern}';")
    sports = cur.fetchall()
    conn.close()
    cur.close()
    return [{'name': sport[0], 'slug': sport[1], 'active': sport[2]} for sport in sports]

def get_sports_with_min_active_events(threshold):
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user=postgres password='Apooja@96'")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM sport WHERE num_active_events > {threshold};")
    sports = cur.fetchall()
    conn.close()
    cur.close()
    return [{'name': sport[0], 'slug': sport[1], 'active': sport[2]} for sport in sports]

#This method is to get the api end points from the event table
def get_events_with_name_like(pattern):
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user=postgres password='Apooja@96'")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM event WHERE name ~ '{pattern}';")
    events = cur.fetchall()
    conn.close()
    cur.close()
    return [{'name':event[0],'slug':event[1],'active':event[2],'type':event[3],'event_sport':event[4],'status':event[5],'scheduled_start':event[6],'actual_start':event[7]} for event in events]

def get_events_with_min_active_selections(threshold):
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user=postgres password='Apooja@96'")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM event WHERE num_active_selections > {threshold};")
    selections = cur.fetchall()
    conn.close()
    cur.close()
    return [{'name': selection[0], 'slug': selection[1], 'active': selection[2],'type':selection[3],'sport':selection[4],'status':selection[5],'actual_start':selection[6],'scheduled_start':selection[7]} for selection in selections]

def edit_selection(name,new_selection):
    """
    This method is used to edit a selection resource. It takes in the name of the resource which needs to be modified and the new_selection
    is a selection objects with relevant new fields

    When a selection is set to inactive then we need to edit all the events which map it to the selection need to updated with the number of selections active for that event

    input -> name: str, new_selection: dict
    output -> dict
    """
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user=postgres password='Apooja@96'")
    cur = conn.cursor()
    if not new_selection['active']:
       selections = cur.execute(f"SELECT * FROM selection WHERE name='{name}'")
       for selection in selections:
           events = cur.execute(f"SELECT * FROM event WHERE name='{selection[2]}'")
           for e in events:
               event_name = e[0]
               present_active_selections=e[8]
               if present_active_selections>0:
                   cur.execute(f"UPDATE event SET num_active_selections={present_active_selections-1} WHERE name='{event_name}';")
                   cur.execute('commit')
    cur.execute(f"UPDATE event SET name='{new_selection['name']}', event='{new_selection['event']}', price={new_selection['price']}, active={new_selection['active']}, outcome='{new_selection['outcome']}' WHERE name='{name}';")
    cur.execute('commit')
    conn.close()
    cur.close()

def edit_event(name,new_event):
    """
    This method is used to edit a event resource. It takes in the name of the resource which needs to be modified and the new_event
    is a event objects with relevant new fields

    When a event is set to inactive then we need to edit all the events which map it to the event need to updated with the number of events active for that event

    input -> name: str, new_selection: dict
    output -> dict
    """
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user=postgres password='Apooja@96'")
    cur = conn.cursor()
    if not new_event['active']:
       events = cur.execute(f"SELECT * FROM event WHERE name='{name}'")
       for event in events:
           sports = cur.execute(f"SELECT * FROM sport WHERE name='{event[4]}'")
           for s in sports:
               sport_name = s[0]
               present_active_events=s[3]
               if present_active_events>0:
                   cur.execute(f"UPDATE sport SET num_active_events={present_active_events-1} WHERE name='{sport_name}';")
                   cur.execute('commit')

    cur.execute(f"UPDATE event SET name='{new_event['name']}', slug='{new_event['slug']}', active={new_event['active']}, type='{new_event['type']}', event_sport='{new_event['event_sport']}', status='{new_event['status']}', scheduled_start='{new_event['scheduled_start']}', actual_start='{new_event['actual_start']}' WHERE name='{name}';")
    cur.execute('commit')
    conn.close()
    cur.close()


def edit_sport(name,new_sport):
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user=postgres password='Apooja@96'")
    cur = conn.cursor()
    cur.execute(f"UPDATE sport SET name='{new_sport['name']}', slug='{new_sport['slug']}', active={new_sport['active']} WHERE name={name};")
    cur.execute('commit')
    conn.close()
    cur.close()


#This method is to get the api end points from the selection table
def get_selections_with_name_like(pattern):
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user=postgres password='Apooja@96'")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM selection WHERE name ~ '{pattern}';")
    selections = cur.fetchall()
    conn.close()
    cur.close()
    return [{'name':selection[0],'event':selection[1],'price':selection[2],'active':selection[3],'outcome':selection[4]} for selection in selections]

#Check if the table exisits then only create the sport table
if not check_if_table_exists("sport"):
    create_sport_table()
if not check_if_table_exists("event"):
    create_event_table()
if not check_if_table_exists("selection"):
    create_selection_table()

