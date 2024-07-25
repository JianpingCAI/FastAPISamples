# Setting up Redis on WSL

Setting up Redis on WSL (Windows Subsystem for Linux) is quite similar to setting it up on a regular Linux distribution. Here’s a step-by-step guide to help you get Redis up and running on WSL:

## Step 1: Open WSL

Open your WSL terminal. You can do this by searching for your preferred WSL distribution (e.g., Ubuntu) in the Windows Start menu and launching it.

## Step 2: Update Package Index

First, ensure your package index is up to date:

```bash
sudo apt update
```

## Step 3: Install Redis

Install Redis using the following command:

```bash
sudo apt install redis-server -y
```

## Step 4: Configure Redis

Open the Redis configuration file for editing:

```bash
sudo nano /etc/redis/redis.conf
```

Make the following changes:

- **Run Redis as a Daemon:**
  Change the line `supervised no` to `supervised systemd`.

- **Set a Password:**
  Uncomment the line `# requirepass foobared` and change `foobared` to your desired password.

Save and exit the editor (in nano, press `CTRL+X`, then `Y`, then `ENTER`).

## Step 5: Start and Enable Redis

Start the Redis service:

```bash
sudo service redis-server start
```

Enable Redis to start on boot:

```bash
sudo systemctl enable redis-server
```

## Step 6: Verify Redis Installation

Check if Redis is running:

```bash
sudo service redis-server status
```

You should see an output indicating that Redis is active and running.

You can also use `redis-cli` to interact with Redis:

```bash
redis-cli
```

Within the Redis CLI, run:

```bash
ping
```

You should get a response:

```bash
PONG
```

To exit the Redis CLI, type:

```bash
exit
```

## Step 7: Configure Redis to Allow External Connections (Optional)

By default, Redis will only allow connections from localhost. If you need to connect to Redis from outside WSL, you need to modify the `bind` directive in `/etc/redis/redis.conf`.

1. Open the configuration file:

   ```bash
   sudo nano /etc/redis/redis.conf
   ```

2. Find the line `bind 127.0.0.1 ::1` and modify it to allow connections from all IPs (or specify your preferred IP address):

   ```bash
   bind 0.0.0.0
   ```

3. Restart Redis:

   ```bash
   sudo service redis-server restart
   ```

## Step 8: Test Remote Connectivity

If you’ve allowed external connections, test from a remote client:

```bash
redis-cli -h your_redis_server_ip -a your_redis_password
```

Replace `your_redis_server_ip` with your WSL IP address and `your_redis_password` with the password you set in the configuration file.

## Troubleshooting Tips

- **Ensure Windows Firewall allows connections to WSL:** You might need to create a rule to allow connections to the Redis port (default is 6379).
- **Check the WSL IP Address:** You can find your WSL instance's IP address using `ip addr` or `ifconfig`.

With these steps, you should have Redis set up and running on WSL.
