/**
 * Unit tests for the API client
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mock the token module before importing client
vi.mock('../auth/token', () => ({
    getAccessToken: vi.fn(),
    clearAccessToken: vi.fn(),
}));

import { apiReview, apiCompare, apiChat, apiStats, apiSaveProfile, apiGetProfile } from './client';
import { getAccessToken, clearAccessToken } from '../auth/token';

const mockFetch = globalThis.fetch as unknown as ReturnType<typeof vi.fn>;

describe('API Client', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        vi.mocked(getAccessToken).mockReturnValue(null);
    });

    describe('apiReview', () => {
        it('should call /api/review with correct payload', async () => {
            const mockReview = { product_name: 'iPhone 15', predicted_rating: '8.5' };
            mockFetch.mockResolvedValueOnce({
                ok: true,
                json: () => Promise.resolve(mockReview),
            });

            const result = await apiReview('iPhone 15', 'web');

            expect(mockFetch).toHaveBeenCalledWith(
                expect.stringContaining('/api/review'),
                expect.objectContaining({
                    method: 'POST',
                    headers: expect.objectContaining({
                        'Content-Type': 'application/json',
                    }),
                    body: JSON.stringify({
                        product_name: 'iPhone 15',
                        data_mode: 'web',
                        user_id: null,
                    }),
                }),
            );
            expect(result).toEqual(mockReview);
        });

        it('should include auth header when token exists', async () => {
            vi.mocked(getAccessToken).mockReturnValue('test-token');
            const mockReview = { product_name: 'test' };
            mockFetch.mockResolvedValueOnce({
                ok: true,
                json: () => Promise.resolve(mockReview),
            });

            await apiReview('test');

            expect(mockFetch).toHaveBeenCalledWith(
                expect.any(String),
                expect.objectContaining({
                    headers: expect.objectContaining({
                        Authorization: 'Bearer test-token',
                    }),
                }),
            );
        });

        it('should throw error on non-ok response', async () => {
            mockFetch.mockResolvedValueOnce({
                ok: false,
                status: 400,
                json: () => Promise.resolve({ error: { message: 'Bad request' } }),
            });

            await expect(apiReview('test')).rejects.toThrow('Bad request');
        });

        it('should clear token on 401 response', async () => {
            mockFetch.mockResolvedValueOnce({
                ok: false,
                status: 401,
                json: () => Promise.resolve({ error: { message: 'Unauthorized' } }),
            });

            await expect(apiReview('test')).rejects.toThrow();
            expect(clearAccessToken).toHaveBeenCalledWith('unauthorized');
        });
    });

    describe('apiCompare', () => {
        it('should call /api/compare with products array', async () => {
            const mockComparison = { products: ['A', 'B'], winner: 'A' };
            mockFetch.mockResolvedValueOnce({
                ok: true,
                json: () => Promise.resolve(mockComparison),
            });

            const result = await apiCompare(['Product A', 'Product B']);

            expect(mockFetch).toHaveBeenCalledWith(
                expect.stringContaining('/api/compare'),
                expect.objectContaining({
                    method: 'POST',
                    body: JSON.stringify({ products: ['Product A', 'Product B'] }),
                }),
            );
            expect(result).toEqual(mockComparison);
        });
    });

    describe('apiChat', () => {
        it('should call /api/chat with message and history', async () => {
            const mockResponse = { reply: 'Hello!', session_id: 1 };
            mockFetch.mockResolvedValueOnce({
                ok: true,
                json: () => Promise.resolve(mockResponse),
            });

            const result = await apiChat({
                productName: 'iPhone',
                message: 'Is this good?',
                history: [{ role: 'user', content: 'Hi' }],
            });

            expect(mockFetch).toHaveBeenCalledWith(
                expect.stringContaining('/api/chat'),
                expect.objectContaining({
                    method: 'POST',
                }),
            );
            expect(result).toEqual(mockResponse);
        });
    });

    describe('apiStats', () => {
        it('should call /api/stats', async () => {
            const mockStats = {
                products_analyzed: 100,
                reviews_processed: 1000,
                active_users: 50,
            };
            mockFetch.mockResolvedValueOnce({
                ok: true,
                json: () => Promise.resolve(mockStats),
            });

            const result = await apiStats();

            expect(mockFetch).toHaveBeenCalledWith(
                expect.stringContaining('/api/stats'),
                expect.objectContaining({
                    headers: expect.any(Object),
                }),
            );
            expect(result).toEqual(mockStats);
        });
    });

    describe('apiSaveProfile', () => {
        it('should call /api/profile with profile data', async () => {
            mockFetch.mockResolvedValueOnce({
                ok: true,
                json: () => Promise.resolve({ status: 'ok' }),
            });

            await apiSaveProfile({
                min_budget: 50000,
                max_budget: 200000,
                use_cases: ['Gaming', 'Work'],
                preferred_brands: ['Apple', 'Samsung'],
            });

            expect(mockFetch).toHaveBeenCalledWith(
                expect.stringContaining('/api/profile'),
                expect.objectContaining({
                    method: 'POST',
                    body: expect.stringContaining('"min_budget":50000'),
                }),
            );
        });
    });

    describe('apiGetProfile', () => {
        it('should call /api/profile and return profile', async () => {
            const mockProfile = {
                min_budget: 50000,
                max_budget: 200000,
                use_cases: ['Gaming'],
                preferred_brands: ['Apple'],
            };
            mockFetch.mockResolvedValueOnce({
                ok: true,
                json: () => Promise.resolve(mockProfile),
            });

            const result = await apiGetProfile();

            expect(mockFetch).toHaveBeenCalledWith(
                expect.stringContaining('/api/profile'),
                expect.objectContaining({
                    headers: expect.any(Object),
                }),
            );
            expect(result).toEqual(mockProfile);
        });

        it('should return null on error', async () => {
            mockFetch.mockResolvedValueOnce({
                ok: false,
                status: 404,
            });

            const result = await apiGetProfile();

            expect(result).toBeNull();
        });

        it('should return null on empty response', async () => {
            mockFetch.mockResolvedValueOnce({
                ok: true,
                json: () => Promise.resolve({}),
            });

            const result = await apiGetProfile();

            expect(result).toBeNull();
        });
    });
});
