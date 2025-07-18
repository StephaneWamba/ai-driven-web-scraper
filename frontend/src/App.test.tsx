import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders app without crashing', () => {
  render(<App />);
  // Basic test to ensure app renders without errors
  expect(document.body).toBeInTheDocument();
});

test('app has main content', () => {
  render(<App />);
  // Check if the app has some content
  const appElement = document.querySelector('.min-h-screen');
  expect(appElement).toBeInTheDocument();
});
