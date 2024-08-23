select user_id, user_group
from restaurant.internal_users
where login = '$login'
  and password = '$password'