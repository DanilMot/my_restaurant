SELECT w_id, w_name,COUNT(*) zakazi
FROM restaurant.user_zakaz join restaurant.waitress using (user_id) where year(order_date)='$input_year' AND month(order_date)='$input_month'
group by w_id

