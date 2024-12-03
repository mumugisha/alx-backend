import { createClient, print } from 'redis';
import { promisify } from 'util';

const client = createClient();

client.on('connect', function() {
  console.log('Redis client connected to the server');
});

client.on('error', function(err) {
  console.log(`Redis client not connected to the server: ${err}`);
});

async function setNewSchool(schoolName, value) {
  const set = promisify(client.set).bind(client);
  try {
    await set(schoolName, value);
    print(null, `Value set for ${schoolName}`);
  } catch (err) {
    console.log(`Error setting value for ${schoolName}: ${err}`);
  }
}

async function displaySchoolValue(schoolName) {
  const get = promisify(client.get).bind(client);
  try {
    const value = await get(schoolName);
    console.log(value || `No value found for ${schoolName}`);
  } catch (err) {
    console.log(`Error getting value for ${schoolName}: ${err}`);
  }
}

(async () => {
  try {
    await new Promise((resolve, reject) => {
      client.on('ready', resolve);
      client.on('error', reject);
    });

    await displaySchoolValue('Holberton');
    await setNewSchool('HolbertonSanFrancisco', '100');
    await displaySchoolValue('HolbertonSanFrancisco');
  } catch (error) {
    console.log(`Error during execution: ${error}`);
  } finally {
    client.quit();
  }
})();
