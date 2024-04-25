import dayjs from 'dayjs';

export const formatTime = (timestamp) => timestamp && dayjs(timestamp).format('YYYY/MM/DD HH:mm:ss')