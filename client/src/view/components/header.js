import React, { Component } from 'react'
import { Link } from "react-router-dom";
import 'jqueryui'
import Cookies from "universal-cookie";

class Header extends Component {

    componentDidMount() {
    }

    numberWithCommas(x) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    render() {


        return (
            <div className="header-wrapper">

                <div className="header">
                    <h1>Video Converter</h1>
                </div>

            </div>
        )

    }

}

export default Header
