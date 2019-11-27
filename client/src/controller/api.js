import apisauce from "apisauce";
import Cookie from "universal-cookie";

const API_URL= "http://" + window.location.hostname + ":8000";

let create = () => {

    console.log(API_URL);

    new Cookie();

    const api = apisauce.create({
        baseURL: API_URL,
        headers: {
            "Content-type": "application/json",
            Accept: "application/json",
            "Accept-Language": "sv",
            "Access-Control-Allow-Origin": "*",
        }
    });

    const headers = () => {
        return { headers: {} }
    };

    const transcodeSend = data => api.post("/transcode/", data, headers());

    return {
        transcodeSend,
    };

};

export default create();