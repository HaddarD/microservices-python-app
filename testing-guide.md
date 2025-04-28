 # 🚀 NGINX Testing Guide for Cinema 3 Project 🎬

Welcome to my **NGINX Testing Guide**!
💥 Here’s where I put all the tests & commands to ensure your NGINX configuration is rock-solid!
🛠️ Let’s go!

---

## 1️⃣ Reverse Proxy 🎥

Let's make sure your frontend requests are routed correctly through NGINX to all your Flask services:

### Test Commands:

- **UI Service (Dashboard)**:  
  Visit [http://localhost/](http://localhost/) in your browser. You should see the UI. If not, NGINX might be hiding the movie magic. 🎭
  
- **Movies Service**:  
  Visit [http://localhost/movies/](http://localhost/movies/) to see the movies list.

- **Showtimes Service**:  
  Visit [http://localhost/showtimes/](http://localhost/showtimes/) to check the showtimes.

- **Bookings Service**:  
  Visit [http://localhost/bookings/](http://localhost/bookings/) to view booking info.

- **Users Service**:  
  Visit [http://localhost/users/](http://localhost/users/) to see user data.

### Expected Outcome:
- **UI Service** should show the cool dashboard. 😎
- **API Endpoints** should return data from the different endpoints. 🎉

---

## 2️⃣ Rate Limiting ⏱️

I've set a rate limit for `/users/` to 5 requests per second, with a burst of 10. Let’s test that out!

### Test Command:
```bash
curl http://localhost/users/
```

### Expected Outcome:
If you exceed 5 requests in a second, you should get a 429 Too Many Requests. 🚨

---

## 3️⃣ Load Balancing ⚖️

I've set up load balancing for the /movies/ route.
Let's check if NGINX is spreading the love across multiple servers. 🙌

### Test Command:
```bash
ab -n 100 -c 10 http://localhost/movies/
```

### Expected Outcome:
Requests should be distributed between localhost:5001 and localhost:5005 evenly. 📦

---

## 4️⃣ Failover Strategy 🚑

Let’s simulate a service failure. Stop one of the showtimes instances and make sure NGINX fails over gracefully.

### Test Command:
Stop one of the Showtimes services (e.g., localhost:5002) and try accessing http://localhost/showtimes/.

### Expected Outcome:
NGINX should switch to the backup server automatically. 👏

---

## 5️⃣ Caching 🧊
Let's Make sure NGINX caches /showtimes/ for 30 seconds to speed up responses.

### Test Command:
```bash
curl -I http://localhost/showtimes/
```

### Expected Outcome:
Check for Cache-Control and Expires headers in the response. 🕵️‍

---

## 6️⃣ Blocking Suspicious IP Range 🚫

Blocked IP? Let’s test the 403 Forbidden response from `192.168.56.0/24`

### Test Command:
```bash
curl http://localhost/ --header "X-Real-IP: 192.168.56.100"
```

### Expected Outcome:
403 Forbidden should show up if you’re from the blocked IP range. 🚷

---

## 7️⃣ HTTPS with SSL 🔒

Let's ensure your site redirects HTTP to HTTPS for secure browsing.

### Test Command:
```bash
curl -I http://localhost/
```

### Expected Outcome:
HTTP traffic should redirect to HTTPS. 🔒

---

## 8️⃣ Load Balancing Algorithm Change ⚙️

Now we’re testing the least connections load balancing algorithm.

### Test Command:
```bash
ab -n 100 -c 10 http://localhost/movies/
```

### Expected Outcome:
Requests should go to the server with the fewest active connections. 📉

---

## Everything is working smoothly? YAY! 🎉 `<(^-^<)<(^.^)>(>^-^)>` 🎉
If anything goes wrong, check your NGINX logs and fix those issues. Happy testing! 😄

