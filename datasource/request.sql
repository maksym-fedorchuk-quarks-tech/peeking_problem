SELECT ROW_NUMBER() OVER (ORDER BY registration_time) AS user_id,
       is_buyer

FROM (SELECT DISTINCT users.[registration_time] as registration_time,
                      CASE WHEN buyers.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_buyer

      FROM [table_with_users] AS users
               LEFT JOIN [table_with_buyers] AS buyers
                         ON buyers.user_id = users.id
                             AND buyers.[purchase_time] >= '2024-01-01'

      WHERE users.[registration_time] BETWEEN '2024-01-01' AND '2024-02-01') AS antient_user_data;
