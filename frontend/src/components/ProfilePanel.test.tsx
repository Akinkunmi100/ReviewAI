/**
 * Unit tests for ProfilePanel component
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import React from 'react';

// Mock the API client
vi.mock('../api/client', () => ({
    apiSaveProfile: vi.fn(),
}));

import ProfilePanel from './ProfilePanel';
import { apiSaveProfile } from '../api/client';

describe('ProfilePanel', () => {
    const mockOnChange = vi.fn();

    beforeEach(() => {
        vi.clearAllMocks();
        // Reset window.confirm mock
        vi.spyOn(window, 'confirm').mockReturnValue(true);
    });

    it('should render profile form with all fields', () => {
        render(<ProfilePanel value={null} onChange={mockOnChange} />);

        expect(screen.getByText('Your Profile')).toBeInTheDocument();
        expect(screen.getByPlaceholderText('e.g., 50000')).toBeInTheDocument();
        expect(screen.getByPlaceholderText('e.g., 200000')).toBeInTheDocument();
        expect(screen.getByText('Use cases:')).toBeInTheDocument();
        expect(screen.getByPlaceholderText('e.g., Samsung, Apple, Sony')).toBeInTheDocument();
    });

    it('should display all use case chips', () => {
        render(<ProfilePanel value={null} onChange={mockOnChange} />);

        const useCases = ['Gaming', 'Work', 'Photography', 'Travel', 'Students', 'Content Creation', 'Fitness', 'Music'];
        useCases.forEach((uc) => {
            expect(screen.getByText(uc)).toBeInTheDocument();
        });
    });

    it('should populate form with existing profile value', () => {
        const existingProfile = {
            min_budget: 50000,
            max_budget: 200000,
            use_cases: ['Gaming', 'Work'],
            preferred_brands: ['Apple', 'Samsung'],
        };

        render(<ProfilePanel value={existingProfile} onChange={mockOnChange} />);

        expect(screen.getByDisplayValue('50000')).toBeInTheDocument();
        expect(screen.getByDisplayValue('200000')).toBeInTheDocument();
        expect(screen.getByDisplayValue('Apple, Samsung')).toBeInTheDocument();
    });

    it('should toggle use case on click', () => {
        render(<ProfilePanel value={null} onChange={mockOnChange} />);

        const gamingCheckbox = screen.getByText('Gaming').closest('label')?.querySelector('input');
        expect(gamingCheckbox).not.toBeChecked();

        fireEvent.click(gamingCheckbox!);

        expect(gamingCheckbox).toBeChecked();
    });

    it('should validate budget range', async () => {
        render(<ProfilePanel value={null} onChange={mockOnChange} />);

        const minBudgetInput = screen.getByPlaceholderText('e.g., 50000');
        const maxBudgetInput = screen.getByPlaceholderText('e.g., 200000');
        const saveButton = screen.getByText('No Changes');

        // Set invalid budget range (min > max)
        fireEvent.change(minBudgetInput, { target: { value: '200000' } });
        fireEvent.change(maxBudgetInput, { target: { value: '50000' } });

        // Wait for button to enable
        await waitFor(() => {
            expect(screen.getByText('Save Profile')).toBeInTheDocument();
        });

        fireEvent.click(screen.getByText('Save Profile'));

        await waitFor(() => {
            expect(screen.getByText(/Minimum budget cannot be greater/)).toBeInTheDocument();
        });
    });

    it('should call apiSaveProfile on save', async () => {
        vi.mocked(apiSaveProfile).mockResolvedValueOnce(undefined);

        render(<ProfilePanel value={null} onChange={mockOnChange} userId="user123" />);

        const minBudgetInput = screen.getByPlaceholderText('e.g., 50000');
        fireEvent.change(minBudgetInput, { target: { value: '100000' } });

        await waitFor(() => {
            expect(screen.getByText('Save Profile')).toBeInTheDocument();
        });

        fireEvent.click(screen.getByText('Save Profile'));

        await waitFor(() => {
            expect(apiSaveProfile).toHaveBeenCalled();
        });
    });

    it('should call onChange with profile data on save', async () => {
        vi.mocked(apiSaveProfile).mockResolvedValueOnce(undefined);

        render(<ProfilePanel value={null} onChange={mockOnChange} />);

        const minBudgetInput = screen.getByPlaceholderText('e.g., 50000');
        fireEvent.change(minBudgetInput, { target: { value: '75000' } });

        await waitFor(() => {
            expect(screen.getByText('Save Profile')).toBeInTheDocument();
        });

        fireEvent.click(screen.getByText('Save Profile'));

        await waitFor(() => {
            expect(mockOnChange).toHaveBeenCalledWith(
                expect.objectContaining({
                    min_budget: 75000,
                }),
            );
        });
    });

    it('should clear profile on Clear All button click', async () => {
        const existingProfile = {
            min_budget: 50000,
            max_budget: 200000,
            use_cases: ['Gaming'],
            preferred_brands: ['Apple'],
        };

        render(<ProfilePanel value={existingProfile} onChange={mockOnChange} />);

        fireEvent.click(screen.getByText('Clear All'));

        expect(mockOnChange).toHaveBeenCalledWith(null);
    });

    it('should disable save button when no changes', () => {
        render(<ProfilePanel value={null} onChange={mockOnChange} />);

        const saveButton = screen.getByText('No Changes');
        expect(saveButton).toBeDisabled();
    });

    it('should show saving and saved states', async () => {
        vi.mocked(apiSaveProfile).mockImplementation(() => new Promise((r) => setTimeout(r, 100)));

        render(<ProfilePanel value={null} onChange={mockOnChange} />);

        const minBudgetInput = screen.getByPlaceholderText('e.g., 50000');
        fireEvent.change(minBudgetInput, { target: { value: '123456' } });

        await waitFor(() => {
            expect(screen.getByText('Save Profile')).toBeInTheDocument();
        });

        fireEvent.click(screen.getByText('Save Profile'));

        await waitFor(() => {
            expect(screen.getByText('Saving...')).toBeInTheDocument();
        });

        await waitFor(() => {
            expect(screen.getByText('✓ Saved!')).toBeInTheDocument();
        }, { timeout: 2000 });
    });
});
