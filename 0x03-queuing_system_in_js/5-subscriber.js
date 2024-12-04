import { createClient } from 'redis';

const redisClient = createClient();

redisClient.on('connect', () => {
  console.log('Redis client connected to the server');
});

redisClient.on('error', (error) => {
  console.log(`Redis client not connected to the server: ${error.message}`);
});

redisClient.subscribe('holberton school channel');

redisClient.on('message', (channel, message) => {
  console.log(`Received message: ${message}`);
  if (message === 'KILL_SERVER') {
    redisClient.unsubscribe('holberton school channel', (err) => {
      if (err) {
        console.error(`Error unsubscribing: ${err.message}`);
      } else {
        console.log('Unsubscribed from channel');
        redisClient.quit((quitErr) => {
          if (quitErr) {
            console.error(`Error closing client: ${quitErr.message}`);
          } else {
            console.log('Redis client closed');
          }
        });
      }
    });
  }
});
