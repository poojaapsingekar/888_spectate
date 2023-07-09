import psycopg2

DB_NAME = "888"

def check_if_table_exists(table_name):
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


def create_sport_table():
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user=postgres password='Apooja@96'")
    cur = conn.cursor()
    cur.execute("CREATE TABLE sport (name varchar(255), slug varchar(255), active bool, num_active_events int, PRIMARY KEY (name));")
    cur.execute('commit')
    conn.close()
    cur.close()

def create_event_table():
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user=postgres password='Apooja@96'")
    cur = conn.cursor()
    cur.execute("CREATE TABLE event (name varchar(255), slug varchar(255), active bool, type varchar(255), event_sport varchar(255),status varchar(255), scheduled_start varchar(255),actual_start varchar(255),PRIMARY KEY (name));")
    cur.execute('commit')
    conn.close()
    cur.close()


def create_selection_table():
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user=postgres password='Apooja@96'")
    cur = conn.cursor()
    cur.execute("CREATE TABLE selection (name varchar(255), event varchar(255), price float(5), active bool,outcome varchar(255),PRIMARY KEY (name));")
    cur.execute('commit')
    conn.close()
    cur.close()

def create_sport(name, slug, active, num_active_events=0):
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user=postgres password='Apooja@96'")
    cur = conn.cursor()
    active = "TRUE" if active else "FALSE"
    cur.execute(f"INSERT INTO sport VALUES ('{name}', '{slug}', {active}, {num_active_events})")
    cur.execute('commit')
    conn.close()
    cur.close()

def create_event(name,slug,active,type,event_sport,status,scheduled_start,actual_start):
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user=postgres password='Apooja@96'")
    cur = conn.cursor()
    cur.execute(f"INSERT INTO event VALUES ('{name}', '{slug}', {active}, '{type}','{event_sport}','{status}', '{scheduled_start}' ,'{actual_start}')")
    cur.execute('commit')
    conn.close()
    cur.close()

def get_sports_with_namelike(pattern):
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user=postgres password='Apooja@96'")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM sport WHERE name ~ '{pattern}';")
    sports = cur.fetchall()
    return [{'name': sport[0], 'slug': sport[1], 'active': sport[2]} for sport in sports]

def get_sports_with_min_active_events(threshold):
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user=postgres password='Apooja@96'")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM sport WHERE num_active_events > {threshold};")
    sports = cur.fetchall()
    return [{'name': sport[0], 'slug': sport[1], 'active': sport[2]} for sport in sports]

def get_events_with_name_like(pattern):
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user=postgres password='Apooja@96'")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM event WHERE name ~ '{pattern}';")
    events = cur.fetchall()
    return [{'name':event[0],'slug':event[1],'active':event[2],'type':event[3],'event_sport':event[4],'status':event[5],'scheduled_start':event[6],'actual_start':event[7]} for event in events]

if not check_if_table_exists("sport"):
    create_sport_table()
if not check_if_table_exists("event"):
    create_event_table()
if not check_if_table_exists("selection"):
    create_selection_table()

