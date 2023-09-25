// Importing 'axios' for making HTTP requests.
import axios from 'axios';

// Defining an async function 'fetchData' to fetch data from the server.
export async function fetchData(): Promise<{ pupil_size: any; cognitive_load: any; } | null> {
    try {
        const response = await axios.get('http://localhost:8080/get_data');
        
        // Extract and return the required data.
        const { pupil_size, cognitive_load } = response.data;
        return { pupil_size, cognitive_load };
    } catch (error) {
        console.error('Error fetching data from Server.py:', error);
        return null;
    }
}

