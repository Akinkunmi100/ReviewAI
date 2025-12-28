/**
 * Vitest Test Setup
 * 
 * This file is run before each test file.
 * It sets up global test utilities and mocks.
 */

import { vi, afterEach } from 'vitest';
import '@testing-library/jest-dom';

// Mock window.location.origin for API base URL
Object.defineProperty(window, 'location', {
    value: {
        origin: 'http://localhost:5173',
        href: 'http://localhost:5173',
        hostname: 'localhost',
        port: '5173',
        protocol: 'http:',
        pathname: '/',
    },
    writable: true,
});

// Mock import.meta.env
Object.defineProperty(import.meta, 'env', {
    value: {
        VITE_API_BASE_URL: 'http://localhost:8001',
        MODE: 'test',
        DEV: false,
        PROD: false,
    },
    writable: true,
});

// Mock localStorage
const localStorageMock = {
    getItem: vi.fn(),
    setItem: vi.fn(),
    removeItem: vi.fn(),
    clear: vi.fn(),
};
Object.defineProperty(window, 'localStorage', { value: localStorageMock });

// Global fetch mock
globalThis.fetch = vi.fn() as any;

// Reset mocks after each test
afterEach(() => {
    vi.clearAllMocks();
});
