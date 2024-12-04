import { createClient } from 'redis';

const client = createClient();

client.on('connect', function () {
  console.log('Redis client connected to the server');
});

client.on('error', function (err) {
  console.log(`Redis client not connected to the server: ${err}`);
});

function setNewSchool (schoolName, value) {
  client.set(schoolName, value, function (err, reply) {
    if (err) {
      console.log(err);
      throw err;
    }
    console.log(`Reply: ${reply}`);
  });
}

function displaySchoolValue (schoolName) {
  client.get(schoolName, function (error, result) {
    if (error) {
      console.log(error);
      throw error;
    }
    console.log(result);
  });
}

client.connect()
  .then(() => {
    displaySchoolValue('Holberton');
    setNewSchool('HolbertonSanFrancisco', '100');
    displaySchoolValue('HolbertonSanFrancisco');
  })
  .catch((err) => {
    console.log('Failed to connect to Redis:', err);
  });
