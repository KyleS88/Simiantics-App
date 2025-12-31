import axios from 'axios';

const apiURL: String = 'http://localhost:8000'

export const searchImages = async (query: string, isFileName: boolean) => {
    const response = await axios.get(`${apiURL}/search`, {
        params: {q: query, isFileName}
    })
    return response.data?.results
}