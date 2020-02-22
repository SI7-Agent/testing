WITH T AS(SELECT * FROM test X(id_key)),
P AS (
SELECT SUM(CASE WHEN id_key<0 THEN 1 ELSE 0 END) neg,
SUM(CASE WHEN id_key>0 THEN 1 ELSE 0 END) pos,
COUNT(id_key) total
FROM T)
SELECT CASE WHEN total <> pos+neg  THEN 0 ELSE 
(CASE WHEN neg%2=1 THEN -1 ELSE +1 END) *exp(SUM(ln(abs(id_key))))
END
product  FROM T,P WHERE id_key <> 0 GROUP BY neg, pos, total;