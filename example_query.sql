--Companies with the most job posts
CREATE TABLE qjx AS
SELECT job_postings_fact.*, company_dim.name, company_dim.link, company_dim.link_google, company_dim.thumbnail
FROM job_postings_fact
INNER JOIN company_dim ON job_postings_fact.company_id=company_dim.company_id;
--LIMIT 36;
SELECT name AS company, COUNT(job_id) AS n_job
FROM qjx
GROUP BY name
ORDER BY n_job DESC;
