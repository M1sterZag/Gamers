export const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return new Intl.DateTimeFormat('ru-RU', {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
    }).format(date);
};

export const validateMaxMembers = (hasSubscription, value) => {
    if (!hasSubscription && value > 5) {
        return 5;
    }
    return value;
};

export const isTeamMember = (team, userId) => {
    return team.owner_id === userId || team.members?.some(m => m.user_id === userId);
};
