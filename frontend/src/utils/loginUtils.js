export function validateForm(form, errors) {
    let valid = true;
    errors.email = '';
    errors.password = '';

    if (!form.email) {
        errors.email = 'Email обязателен';
        valid = false;
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
        errors.email = 'Некорректный email';
        valid = false;
    }

    if (!form.password) {
        errors.password = 'Пароль обязателен';
        valid = false;
    } else if (!/^(?=.*\d)(?=.*[!@#$%^&*_])(?=.*[a-z])(?=.*[A-Z]).{8,}$/.test(form.password)) {
        errors.password = "Пароль слишком слабый! Пароль должен содержать строчные и заглавные буквы латинского алфавита, быть не менее 8 символов, а также содержать спец. символы";
        valid = false;
    }

    return valid;
}
