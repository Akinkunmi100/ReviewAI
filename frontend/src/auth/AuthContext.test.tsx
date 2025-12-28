/**
 * Unit tests for AuthContext
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor, act } from '@testing-library/react';
import React from 'react';

// Mock token module
vi.mock('./token', () => ({
    getAccessToken: vi.fn(),
    setAccessToken: vi.fn(),
    clearAccessToken: vi.fn(),
    onAccessTokenChanged: vi.fn(() => () => { }),
}));

import { AuthProvider, useAuth } from './AuthContext';
import { getAccessToken, setAccessToken, clearAccessToken, onAccessTokenChanged } from './token';

const mockFetch = globalThis.fetch as unknown as ReturnType<typeof vi.fn>;

describe('AuthContext', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        vi.mocked(getAccessToken).mockReturnValue(null);
        vi.mocked(onAccessTokenChanged).mockReturnValue(() => { });
    });

    const wrapper = ({ children }: { children: React.ReactNode }) => (
        <AuthProvider>{children}</AuthProvider>
    );

    describe('useAuth hook', () => {
        it('should throw error when used outside AuthProvider', () => {
            expect(() => {
                renderHook(() => useAuth());
            }).toThrow('useAuth must be used within AuthProvider');
        });

        it('should provide auth context when used inside AuthProvider', async () => {
            const { result } = renderHook(() => useAuth(), { wrapper });

            await waitFor(() => {
                expect(result.current.loading).toBe(false);
            });

            expect(result.current.token).toBeNull();
            expect(result.current.user).toBeNull();
            expect(result.current.login).toBeInstanceOf(Function);
            expect(result.current.register).toBeInstanceOf(Function);
            expect(result.current.logout).toBeInstanceOf(Function);
        });
    });

    describe('login', () => {
        it('should login successfully and set token', async () => {
            const mockResponse = {
                access_token: 'new-token',
                user: { id: 1, email: 'test@example.com' },
            };
            mockFetch.mockResolvedValueOnce({
                ok: true,
                json: () => Promise.resolve(mockResponse),
            });

            const { result } = renderHook(() => useAuth(), { wrapper });

            await waitFor(() => {
                expect(result.current.loading).toBe(false);
            });

            await act(async () => {
                await result.current.login('test@example.com', 'password');
            });

            expect(mockFetch).toHaveBeenCalledWith(
                expect.stringContaining('/api/auth/login'),
                expect.objectContaining({ method: 'POST' }),
            );
            expect(setAccessToken).toHaveBeenCalledWith('new-token', 'login');
            expect(result.current.user).toEqual({ id: 1, email: 'test@example.com' });
        });

        it('should throw error on login failure', async () => {
            mockFetch.mockResolvedValueOnce({
                ok: false,
                status: 401,
                json: () => Promise.resolve({ detail: 'Invalid credentials' }),
            });

            const { result } = renderHook(() => useAuth(), { wrapper });

            await waitFor(() => {
                expect(result.current.loading).toBe(false);
            });

            await expect(
                act(async () => {
                    await result.current.login('test@example.com', 'wrong-password');
                }),
            ).rejects.toThrow('Invalid credentials');
        });
    });

    describe('register', () => {
        it('should register successfully and set token', async () => {
            const mockResponse = {
                access_token: 'new-token',
                user: { id: 1, email: 'new@example.com' },
            };
            mockFetch.mockResolvedValueOnce({
                ok: true,
                json: () => Promise.resolve(mockResponse),
            });

            const { result } = renderHook(() => useAuth(), { wrapper });

            await waitFor(() => {
                expect(result.current.loading).toBe(false);
            });

            await act(async () => {
                await result.current.register('new@example.com', 'password');
            });

            expect(mockFetch).toHaveBeenCalledWith(
                expect.stringContaining('/api/auth/register'),
                expect.objectContaining({ method: 'POST' }),
            );
            expect(setAccessToken).toHaveBeenCalledWith('new-token', 'login');
        });
    });

    describe('logout', () => {
        it('should clear token and user on logout', async () => {
            vi.mocked(getAccessToken).mockReturnValue('existing-token');
            mockFetch.mockResolvedValueOnce({
                ok: true,
                json: () => Promise.resolve({ id: 1, email: 'test@example.com' }),
            });

            const { result } = renderHook(() => useAuth(), { wrapper });

            await waitFor(() => {
                expect(result.current.loading).toBe(false);
            });

            act(() => {
                result.current.logout();
            });

            expect(clearAccessToken).toHaveBeenCalledWith('logout');
            expect(result.current.token).toBeNull();
            expect(result.current.user).toBeNull();
        });
    });

    describe('token restoration', () => {
        it('should fetch user info when token exists on mount', async () => {
            vi.mocked(getAccessToken).mockReturnValue('existing-token');
            mockFetch.mockResolvedValueOnce({
                ok: true,
                json: () => Promise.resolve({ id: 1, email: 'test@example.com' }),
            });

            const { result } = renderHook(() => useAuth(), { wrapper });

            await waitFor(() => {
                expect(result.current.loading).toBe(false);
            });

            expect(mockFetch).toHaveBeenCalledWith(
                expect.stringContaining('/api/auth/me'),
                expect.objectContaining({
                    headers: { Authorization: 'Bearer existing-token' },
                }),
            );
            expect(result.current.user).toEqual({ id: 1, email: 'test@example.com' });
        });

        it('should clear token if /me request fails', async () => {
            vi.mocked(getAccessToken).mockReturnValue('invalid-token');
            mockFetch.mockResolvedValueOnce({
                ok: false,
                status: 401,
                json: () => Promise.resolve({ detail: 'Unauthorized' }),
            });

            const { result } = renderHook(() => useAuth(), { wrapper });

            await waitFor(() => {
                expect(result.current.loading).toBe(false);
            });

            expect(clearAccessToken).toHaveBeenCalledWith('unauthorized');
            expect(result.current.user).toBeNull();
        });
    });
});
