// =========================================================
// App Configuration
// =========================================================
// Centralized environment variables and general settings.
// Note: In production, secrets like tokens should be stored
// in a hidden .env file and not committed to source control.
// =========================================================

// Base API URL from environment variable
export const API_URL = process.env.EXPO_PUBLIC_API_URL;

// Public auth token (should ideally be handled securely)
export const AUTH_TOKEN = process.env.EXPO_PUBLIC_AUTH_TOKEN;

// Local register endpoint
export const REGISTER_URL = "http://127.0.0.1:5000/user";

// Local login endpoint
export const LOGIN_URL = 'http://127.0.0.1:5000/login';

