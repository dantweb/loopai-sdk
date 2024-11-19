// test_client.js

const io = require('socket.io-client');

// Replace with a valid authentication token
const token = 'YOUR_AUTH_TOKEN';

const socket = io('http://web:5000', {
  query: {
    token: token,
  },
  transports: ['websocket'],
});

socket.on('connect', () => {
  console.log('Connected to Socket.IO server');

  // You can emit events to the server if needed
  // socket.emit('my_event', { data: 'test' });
});

socket.on('connect_error', (error) => {
  console.error('Connection error:', error);
});

socket.on('disconnect', (reason) => {
  console.log('Disconnected:', reason);
});

// Listen for messages from the server
socket.on('log', (data) => {
  console.log('Received log message:', data);
});

socket.on('info', (data) => {
  console.log('Received info message:', data);
});
