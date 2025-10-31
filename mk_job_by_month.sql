--These commands can be run on the database here: http://lukeb.co/sql_jobs_db
CREATE TABLE jobs_month01 AS
SELECT *
FROM job_postings_fact
WHERE EXTRACT(MONTH FROM job_posted_date)=1;
