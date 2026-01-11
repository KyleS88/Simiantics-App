import axios from 'axios';

const apiURL: string = 'http://localhost:8000'

export const searchImages = async (query: string, isFileName: boolean) => {
    try {
        const response = await axios.get(`${apiURL}/search`, {
            params: {q: query, isFileName}
        })
        return response.data
    } catch (err) {
        if (axios.isAxiosError(err)) {
            throw new Error(err.response?.data?.detail ?? err.message);
        }
        throw err;
    }
}

export const uploadImage = async (file: File | undefined) => {
    try {
        if (typeof file === "undefined")
            throw Error("Undefined file was inputed");
        const formData = new FormData();
        formData.append("file", file);
        console.log("calling api")
            const response = await axios.post(`${apiURL}/upload`, formData);
        console.log("api complete")
        return response.data;
    } catch (err) {
        if (axios.isAxiosError(err)) {
            throw new Error(err.response?.data?.detail ?? err.message);
        }
        throw err;
    }
}