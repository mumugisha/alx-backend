import { createQueue } from 'kue';

const queue = createQueue();

const notification = {
  phoneNumber: '4153518780',
  message: 'This is the code to verify your account'
};

// Creating a job in the queue
const job = queue.create('push_notification_code', notification)
  .save(function (error) {
    if (error) {
      console.log('Failed to create notification job');
    } else {
      console.log(`Notification job created: ${job.id}`);
    }
  });

// Listening for job completion and failure
job.on('complete', function () {
  console.log('Notification job completed');
}).on('failed', function () {
  console.log('Notification job failed');
});
