select user_id, NULL as user_group
from restaurant.external_users
where login = '$login'
  and password = '$password'