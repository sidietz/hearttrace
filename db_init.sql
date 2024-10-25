CREATE TABLE hearttrace(
    id serial PRIMARY KEY,
    date timestamp,
    sys integer,
    dia integer,
    heart_rate integer
);

GRANT INSERT,UPDATE,SELECT ON ALL TABLES IN SCHEMA public to hearttrace;
GRANT USAGE ON SEQUENCE hearttrace_id_seq TO hearttrace;


curl -d '{"sys":"180", "dia":"140", "rate":"150"}' -H "Content-Type: application/json" -X POST http://localhost:5000/v1/add/hearttrace

