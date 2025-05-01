# 🚀 NGINX Testing Guide for Cinema 3 Project 🎬

<div align="center">
<p><strong>Welcome to my NGINX Testing Guide!</strong><br>
💥 Here’s where I put all the tests & commands to ensure your NGINX configuration is rock-solid!<br>
🛠️ Let’s go!</p>
</div>

---

## Quick Testing:
First run the services with `make run-all` and then run `TestingScript.sh`
```bash
./TestingScript.sh
```
This will run a test for all requirements at once.

# Manual Testing

## 1️⃣ Reverse Proxy 🎥

Let's make sure your frontend requests are routed correctly through NGINX to all your Flask services:\
If you haven't yet, start by running the services:
```bash
make run-all
```

### Browser Testing:

- **UI Service (Dashboard)**:  
  Visit [http://localhost/](http://localhost/) in your browser. You should see the UI. If not, NGINX might be hiding the movie magic. 🎭
  
- **Movies Service**:  
  Visit [http://localhost/movies](http://localhost/movies/) to see the movies list.

- **Showtimes Service**:  
  Visit [http://localhost/showtimes](http://localhost/showtimes/) to check the showtimes.

- **Bookings Service**:  
  Visit [http://localhost/bookings](http://localhost/bookings/) to view booking info.

- **Users Service**:  
  Visit [http://localhost/users](http://localhost/users/) to see user data.

### Expected Outcome:
- **UI Service** should show the cool dashboard. 😎
- **API Endpoints** should return data from the different endpoints. 🎉

### Terminal Testing:
```bash
# Test UI Service
curl -v http://localhost/

# Test Movies Service
curl -v http://localhost/movies/

# Test Showtimes Service
curl -v http://localhost/showtimes/

# Test Bookings Service
curl -v http://localhost/bookings/

# Test Users Service
curl -v http://localhost/users/
```
### Expected Outcome:
All services should respond with 200 OK and return proper JSON data.

---

## 2️⃣ Rate Limiting ⏱️

I've set a rate limit for `/users/` to 5 requests per second, with a burst of 10. Let’s test that out!

### Test Command:
```bash
# Run 50 requests with 20 concurrent connections to trigger rate limiting
ab -n 50 -c 20 http://localhost/users/
```
To generate logs of rate limiting:
```bash
# Watch the rate limit log in real-time
sudo tail -f /var/log/nginx/rate_limit.log
```

### Expected Outcome:
If you exceed 5 requests in a second, some reqs should fail with 429 Too Many Requests. 🚨

---

## 3️⃣ Load Balancing ⚖️

I've set up load balancing for the /movies route.
Let's check if NGINX is spreading the love across both servers. 🙌

### Test Command:
```bash
ab -n 100 -c 10 http://localhost/movies
```

### Expected Outcome:
Requests should be distributed between localhost:5001 and localhost:5005 evenly. 📦

---

## 4️⃣ Failover Strategy 🚑

Let’s simulate a service failure. Stop one of the showtimes instances and make sure NGINX fails over gracefully.

### Test Command:
Stop one of the Showtimes services (e.g., localhost:5002) and try accessing http://localhost/showtimes.
#### Or

```bash
# First test that the primary showtimes service is responding
curl -v http://localhost/showtimes

# Kill the primary showtimes service (5002)
# If running with Makefile:
pkill -f "PORT=5002 python3 -m services.showtimes"

# Test again to verify failover to backup (5006)
curl -v http://localhost/showtimes
```

### Expected Outcome:
NGINX should switch to the backup server automatically & continue responding. 👏

---

## 5️⃣ Caching 🧊
Let's Make sure NGINX caches /showtimes for 30 seconds to speed up responses.

### Test Command:
```bash
curl -v http://localhost/showtimes
```
Make the same request again and check if it's served from cache

### Expected Outcome:
Look for 🕵️:
* Check for Cache-Control and Expires headers in the response.
* A faster response time on the second request

---

## 6️⃣ Blocking Suspicious IP Range 🚫

Blocked IP? Let’s test the 403 Forbidden response from `192.168.56.0/24`

### Test Command:
```bash
curl http://localhost --header "X-Real-IP: 192.168.56.100"
```
Or
```bash
# If you can spoof your IP or use a machine in the banned range:
curl -v --interface 192.168.56.123 http://localhost
```

### Expected Outcome:
403 Forbidden should show up for requests from the blocked IP range. 🚷

---

## 7️⃣ HTTPS with SSL 🔒

Let's ensure your site redirects HTTP to HTTPS for secure browsing.

### Test Command:
```bash
# Test HTTP to HTTPS redirect
curl -v http://localhost:8080/

# Test HTTPS direct access (ignore certificate validation for self-signed cert)
curl -v -k https://localhost:8443/
```

### Expected Outcome:
HTTP traffic should redirect to HTTPS. 🔒 \
The first command should show a 301 redirect, and the second should show a successful HTTPS connection.

---

## 8️⃣ Load Balancing Algorithm Change ⚙️

Now we’re testing the least connections load balancing algorithm.

### Test Commands:
```bash
# Test least connections algorithm
for i in {1..20}; do curl -s http://localhost/movies-leastconn | grep -o '"port": [0-9]*' || echo "No port found"; sleep 0.5; done

# Test ip_hash algorithm (should consistently route to the same backend)
# Run from the same IP multiple times
for i in {1..10}; do curl -s http://localhost/movies | grep -o '"port": [0-9]*' || echo "No port found"; sleep 0.5; done
```
Or an Apache Benchmark test
```bash
ab -n 100 -c 10 http://localhost/movies
```

### Expected Outcome:
Least connections requests should go to the server with the fewest active connections. 📉 \
IP_hash requests should always go to the same endpoint

---

## Everything is working smoothly? YAY! 🎉 <(^-^<)<(^.^)>(>^-^)> 🎉
If anything goes wrong, check your NGINX logs and fix those issues.
```bash
cat /var/log/nginx/rate_limit.log
```
```bash
cat /var/log/nginx/error.log
```
```bash
cat /var/log/nginx/access.log
```
## Happy testing! 😄

