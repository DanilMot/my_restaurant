SELECT waitress.w_id, waitress.w_name, waitress.birthday, waitress.passport
FROM waitress
JOIN external_users using (user_id) LEFT JOIN (select user_id, order_id from user_zakaz where year(order_date)='$input_year' AND month(order_date)='$input_month') as P using (user_id)
WHERE order_id IS NULL;