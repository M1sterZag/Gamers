import {describe, it, expect, beforeEach} from 'vitest';
import {validateForm} from '@/utils/loginUtils';

describe('validateForm', () => {
    let form, errors;

    beforeEach(() => {
        form = {email: '', password: ''};
        errors = {email: '', password: ''};
    });

    it('should require email and password', () => {
        const isValid = validateForm(form, errors);
        expect(isValid).toBe(false);
        expect(errors.email).toBe('Email обязателен');
        expect(errors.password).toBe('Пароль обязателен');
    });

    it('should validate email format', () => {
        form.email = 'invalid-email';
        form.password = 'Abcde123!';
        const isValid = validateForm(form, errors);
        expect(isValid).toBe(false);
        expect(errors.email).toBe('Некорректный email');
    });

    it('should validate password strength', () => {
        form.email = 'user@example.com';
        form.password = 'weak';
        const isValid = validateForm(form, errors);
        expect(isValid).toBe(false);
        expect(errors.password).toMatch(/Пароль слишком слабый/i);
    });

    it('should return true for valid data', () => {
        form.email = 'user@example.com';
        form.password = 'StrongPass1!';
        const isValid = validateForm(form, errors);
        expect(isValid).toBe(true);
        expect(errors.email).toBe('');
        expect(errors.password).toBe('');
    });
});
