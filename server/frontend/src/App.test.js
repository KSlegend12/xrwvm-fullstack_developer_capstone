import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { BrowserRouter } from 'react-router-dom';
import Register from './components/Register/Register';
import Header from './components/Header/Header';
import Login from './components/Login/Login';

test('renders Header with Dealerships title and navigation links', () => {
  render(
    <BrowserRouter>
      <Header />
    </BrowserRouter>
  );
  const brandElements = screen.getAllByText(/Dealerships/i);
  expect(brandElements.length).toBeGreaterThan(0);
  expect(screen.getByText(/Home/i)).toBeInTheDocument();
  expect(screen.getByText(/About Us/i)).toBeInTheDocument();
  expect(screen.getByText(/Contact Us/i)).toBeInTheDocument();
});

test('renders Register component with all 5 required fields and submit button', () => {
  render(
    <BrowserRouter>
      <Register />
    </BrowserRouter>
  );
  expect(screen.getByPlaceholderText(/Username/i)).toBeInTheDocument();
  expect(screen.getByPlaceholderText(/First Name/i)).toBeInTheDocument();
  expect(screen.getByPlaceholderText(/Last Name/i)).toBeInTheDocument();
  expect(screen.getByPlaceholderText(/Email/i)).toBeInTheDocument();
  expect(screen.getByPlaceholderText(/Password/i)).toBeInTheDocument();
  expect(screen.getByRole('button', { name: /Register/i })).toBeInTheDocument();
});

test('renders Login component with username and password fields', () => {
  render(
    <BrowserRouter>
      <Login />
    </BrowserRouter>
  );
  expect(screen.getByPlaceholderText(/Username/i)).toBeInTheDocument();
  expect(screen.getByPlaceholderText(/Password/i)).toBeInTheDocument();
});
