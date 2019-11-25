import apisauce from "apisauce";
import Cookie from "universal-cookie";

const API_URL= "http://" + window.location.hostname + ":8080";

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

    const userRegister = data => api.post("/auth/register/", data, headers());
    const userLogin = data => api.post("/auth/login/", data, headers());
    const userLogout = data => api.post("/auth/logout/", data, headers());
    const userGet = key => api.get("/auth/get/" + key, null, headers());

    return {

        userRegister,
        userLogin,
        userLogout,
        userGet,

    };

};

export default create();
