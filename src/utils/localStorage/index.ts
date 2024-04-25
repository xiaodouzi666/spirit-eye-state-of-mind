import { ACCESS_TOKEN } from '@/constants/user';

const getItem = (key: string) => {
    const value = localStorage.getItem(key);
    return value ? JSON.parse(value) : '';
}

const setItem = (key: string, value: any) => {
    const _value = JSON.stringify(value);
    localStorage.setItem(key, _value)
}

const removeItem = (key: string) => {
    localStorage.removeItem(key)
}


const storeToken = (token: string) => {
    setItem(ACCESS_TOKEN, token)
}

const getStoreToken = () => {
    return getItem(ACCESS_TOKEN)
}


export default {
    getItem,
    setItem,
    removeItem,
    storeToken,
    getStoreToken
}