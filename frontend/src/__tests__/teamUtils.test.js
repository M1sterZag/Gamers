import {describe, it, expect} from 'vitest';
import {formatDate, validateMaxMembers, isTeamMember} from '@/utils/teamUtils';

describe('formatDate', () => {
    it('should format ISO date string correctly', () => {
        const input = '2025-12-01T15:30:00.000Z';
        const result = formatDate(input);
        expect(result).toMatch(/\d+ \p{L}+ \d{4} г. в \d{2}:\d{2}/u); // flexible check
    });
});

describe('validateMaxMembers', () => {
    it('should return original value if user has subscription', () => {
        expect(validateMaxMembers(true, 10)).toBe(10);
    });

    it('should cap value to 5 if no subscription and value exceeds 5', () => {
        expect(validateMaxMembers(false, 10)).toBe(5);
    });

    it('should allow lower value without subscription', () => {
        expect(validateMaxMembers(false, 3)).toBe(3);
    });
});

describe('isTeamMember', () => {
    const userId = 1;

    it('should return true if user is owner', () => {
        const team = {owner_id: 1, members: []};
        expect(isTeamMember(team, userId)).toBe(true);
    });

    it('should return true if user is in members', () => {
        const team = {owner_id: 2, members: [{user_id: 1}]};
        expect(isTeamMember(team, userId)).toBe(true);
    });

    it('should return false if user is neither owner nor member', () => {
        const team = {owner_id: 2, members: [{user_id: 3}]};
        expect(isTeamMember(team, userId)).toBe(false);
    });
});
