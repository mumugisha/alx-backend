import { createClient, print } from 'redis';

const redisClient = createClient();

redisClient.on('connect', function() {
   console.log('Redis client connected to the server');
});

redisClient.on('error', function(err) {
   console.log(`Redis client not connected to the server: ${err}`);
});

// Use hSet instead of hset and fix the syntax errors
redisClient.hSet('HolbertonSchools', 'Portland', '50', print);
redisClient.hSet('HolbertonSchools', 'Seattle', '80', print);
redisClient.hSet('HolbertonSchools', 'New York', '20', print);
redisClient.hSet('HolbertonSchools', 'Bogota', '20', print);
redisClient.hSet('HolbertonSchools', 'Cali', '40', print);
redisClient.hSet('HolbertonSchools', 'Paris', '2', print);

// Retrieve and log data from Redis
redisClient.hGetAll('HolbertonSchools', function(error, result) {
   if (error) {
      console.log(error);
      throw error;
   }
   console.log(result);
});

// Gracefully quit the Redis client
redisClient.quit();
