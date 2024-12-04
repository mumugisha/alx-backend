import { createClient } from 'redis';
import { createQueue } from 'kue';
import { promisify } from 'util';
import express from 'express';

const redisClient = createClient();

redisClient.on('connect', function () {
  console.log('Redis client connected to the server');
});

redisClient.on('error', function (err) {
  console.error(`Redis client not connected to the server: ${err}`);
});

const asyncGet = promisify(redisClient.get).bind(redisClient);

function reserveSeat (number) {
  redisClient.set('available_seats', number);
}

async function getCurrentAvailableSeats () {
  const seats = await asyncGet('available_seats');
  return Number(seats || 0);
}

let reservationEnabled = true;

const queue = createQueue();
const app = express();
const port = 1245;

app.get('/available_seats', async function (req, res) {
  const availableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: availableSeats });
});

app.get('/reserve_seat', function (req, res) {
  if (!reservationEnabled) {
    res.json({ status: 'Reservations are blocked' });
    return;
  }

  const job = queue.create('reserve_seat', { seat: 1 }).save((error) => {
    if (error) {
      res.json({ status: 'Reservation failed' });
    } else {
      res.json({ status: 'Reservation in progress' });
      job.on('complete', function () {
        console.log(`Seat reservation job ${job.id} complete`);
      });
      job.on('failed', function (err) {
        console.error(`Seat reservation job ${job.id} failed: ${err}`);
      });
    }
  });
});

app.get('/process', function (req, res) {
  res.json({ status: 'Queue processing' });
  queue.process('reserve_seat', async function (job, done) {
    const seats = await getCurrentAvailableSeats();
    if (seats === 0) {
      reservationEnabled = false;
      done(new Error('Not enough seats available'));
    } else {
      reserveSeat(seats - 1);
      done();
    }
  });
});

app.listen(port, () => {
  console.log(`App is listening at http://localhost:${port}`);
});

// Initialize available seats
reserveSeat(50);
