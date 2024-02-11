'use strict';

const storage_key = 'light_mode';
const light_mode_val = 'light';
const dark_mode_val = 'dark';

function setMode(mode) {
    localStorage[storage_key] = mode;
    handleChange();
}

function clearMode() {
    localStorage.removeItem(storage_key);
    handleChange();
}

function handleChange() {
    function use_system() {
        const darkThemeMq = window.matchMedia("(prefers-color-scheme: dark)");
        return (darkThemeMq.matches ? dark_mode_val : light_mode_val);
    }
    const local = localStorage[storage_key];
    let mode = use_system();
    const html = document.documentElement;
    console.log({ local });
    if (local) {
        mode = local;
    }
    console.log({ mode });
    if (mode === dark_mode_val) {
        console.log('dark');
        html.setAttribute('data-bs-theme', 'dark');
    } else {
        console.log('light');
        html.setAttribute('data-bs-theme', 'light');
    }
}

handleChange();
