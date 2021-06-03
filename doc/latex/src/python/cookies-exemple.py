# Error message because the two teams selected are not in the league selected.
response = make_response(redirect(url_for("h2h")))
response.set_cookie("error", "Teams not found in this league.", max_age=1)
return response