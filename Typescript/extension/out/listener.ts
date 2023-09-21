import axios from 'axios';

export async function fetchData() {
    try {
        const response = await axios.get('http://localhost:8080/get_data');
        return response.data.message;
    } catch (error) {
        console.error('Error fetching data from Server.py:', error);
        return null;
    }
}
