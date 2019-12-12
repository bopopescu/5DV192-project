import React from 'react'
import Header from "./header";
import {Link} from "react-router-dom";
import Footer from "../components/footer";

export const Wrapper = (props) => (
    <div className="root-wrapper">
        <Header />
        <div className="content-wrapper">
            <div className="content">
                {props.children}
                <Footer />
            </div>
        </div>
    </div>
);